import pathlib
import shutil
import logging
import errno
import socket
import asyncio
import signal
import webbrowser
import json
import datetime
import abc

import websockets
import watchdog.events, watchdog.observers

from . import reload
from .. import build
from ..utils import log

# from . import build


def view(folder):
    project_dir = pathlib.Path(folder).absolute()
    webbrowser.open(str(project_dir / "build" / "index.html"))


def preview(folder, rebuild=True):
    project_dir = pathlib.Path(folder).absolute()

    # deactivate external loggers
    # ---------------------------
    ws_logger = logging.getLogger("websockets")
    ws_logger.setLevel(logging.CRITICAL)
    aio_logger = logging.getLogger("asyncio")
    aio_logger.setLevel(logging.CRITICAL)
    wd_logger = logging.getLogger("watchdog.observers.inotify_buffer")
    wd_logger.setLevel(logging.CRITICAL)

    # init the logger
    # ---------------

    logger = logging.getLogger(__name__)

    loop = asyncio.get_event_loop()

    # add automatic build (if set)
    # ----------------------------
    # and keep watching

    build.build(project_dir)

    class PreviewHandler(watchdog.events.FileSystemEventHandler, abc.ABC):
        handler_interval = 1.0

        def __init__(self, *args, **kwargs):
            self.time = datetime.datetime.now()
            super().__init__(*args, **kwargs)

        @abc.abstractmethod
        def handle_event(self, event):
            pass

        def on_any_event(self, event):
            if event.is_directory or event.event_type == "closed":
                return

            if (datetime.datetime.now() - self.time) < datetime.timedelta(
                seconds=self.handler_interval
            ):
                self.handle_event(event)

            self.time = datetime.datetime.now()

    if rebuild:

        class BuildHandler(PreviewHandler):
            def handle_event(self, event):
                src_path = pathlib.Path(event.src_path)
                log.logger.info(
                    f"[green]BUILD <-[/] {event.event_type}: [i magenta]{src_path.relative_to(project_dir.parent)}[/]",
                    extra={"markup": True},
                )
                if src_path.parent.name == "assets":
                    logger.info("ASSETS")
                    shutil.copy2(str(src_path), str(project_dir / "build" / "assets"))
                else:
                    build.build(project_dir)

        build_handler = BuildHandler()
        build_observer = watchdog.observers.Observer()
        build_observer.schedule(build_handler, path=project_dir / "src", recursive=True)
        build_observer.start()

    # start the server
    # ----------------
    # and keep watching

    class ViewHandler(PreviewHandler):
        time = datetime.datetime.now()

        def handle_event(self, event):
            src_path = pathlib.Path(event.src_path)
            log.logger.info(
                f"[green]VIEW update <-[/] {event.event_type}: [i magenta]{src_path.relative_to(project_dir.parent)}[/]",
                extra={"markup": True},
            )

            async def send_reload_signal():
                async with websockets.connect(reload.websocket_uri) as websocket:
                    #  await asyncio.sleep(1)
                    await websocket.send(json.dumps({"command": "reload"}))

            asyncio.run(send_reload_signal())

    view_handler = ViewHandler()
    view_observer = watchdog.observers.Observer()
    view_observer.schedule(view_handler, path=project_dir / "build", recursive=True)
    view_observer.start()

    # set server
    wsserver = WebSocketServer(reload.host, reload.port)

    # Connect everything to the loop
    # ------------------------------

    webbrowser.open(str(project_dir / "build" / "index.html"))

    def close(loop):
        print()
        logger.info(f"Closing preview mode...")
        if rebuild:
            build_observer.stop()
        view_observer.stop()
        # TODO: properly shut down the server
        #  asyncio.run(wsserver.stop())
        loop.stop()

    loop.add_signal_handler(signal.SIGINT, close, loop)
    asyncio.get_event_loop().run_until_complete(wsserver.starter)
    loop.run_forever()

    loop.close()
    logger.info("Stop watching for updates.")


class WebSocketServer:
    """
    Make a generic server that broadcast the messages from the clients to all the
    other clients.
    """

    def __init__(self, host, port):
        self.USERS = set()
        self.host = host
        self.port = port

    def users_event(self):
        return json.dumps({"type": "users", "count": len(self.USERS)})

    async def notify_message(self, message):
        if self.USERS:  # asyncio.wait doesn't accept an empty list
            await asyncio.wait([user.send(message) for user in self.USERS])

    async def notify_users(self):
        if self.USERS:  # asyncio.wait doesn't accept an empty list
            message = self.users_event()
            await asyncio.wait([user.send(message) for user in self.USERS])

    async def register(self, websocket):
        self.USERS.add(websocket)
        await websocket.send("[START] Connected to the server")
        await self.notify_users()

    async def unregister(self, websocket):
        self.USERS.remove(websocket)
        await websocket.send("[EXIT] Disconnected from the server")
        await self.notify_users()

    async def connect(self, websocket, path):
        """
        This function is run any time a new client will try to connect to the
        websocket.
        """
        # register(websocket) sends user_event() to websocket
        await self.register(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                if data["command"] == "reload":
                    await self.notify_message(json.dumps(data))
                else:
                    logging.error("unsupported event: {}", data)
        finally:
            await self.unregister(websocket)

    @property
    def starter(self):
        return websockets.serve(self.connect, self.host, self.port)

    # TODO: properly shut down the server
    #  async def stop(self):
    #  for client in self.USERS:
    #  await self.unregister(client)


def test_free_connection(host, port):
    """
    Test if already connected
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))
    except OSError as e:
        if e.errno == errno.EADDRINUSE:
            print("Server running")
            return False
        else:
            # something else raised the OSError exception
            print(e)
            s.close()

    return True
