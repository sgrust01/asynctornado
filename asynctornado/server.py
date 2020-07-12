import tornado.ioloop
from tornado.web import RequestHandler
import click
import asyncio
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop
from colorama import init
from termcolor import colored
import datetime
from uuid import uuid4

init()
DELAY = 10


async def aws_fetch():
    """Actual worker function"""
    click.echo(
        colored("AWS Download: ", "yellow") + colored("In-progress...", "green", attrs=['blink'])
    )
    await asyncio.sleep(DELAY)
    click.echo(
        colored("AWS Download: ", "yellow") + colored("Complete", "green")
    )


async def wait_for_sync():
    """Wait for some more sync to complete"""
    return True


async def reload(store):
    """Demo reload composing other async functions"""
    click.echo(
        colored("Status: ", "yellow") + colored("Reloading...", "green")
    )
    await aws_fetch()
    assert await wait_for_sync()
    store.update({datetime.datetime.now().isoformat(): str(uuid4())})
    colored("Status: ", "yellow") + colored("Reloading...", "green", attrs=['blink'])


class Cache:
    """Cache emulator"""
    store = {}

    def update(self):
        """Run the co-routine"""
        IOLoop.current().spawn_callback(reload, self.store)

    def get(self):
        """Get the state of the store"""
        return str(self.store)


cache = Cache()


class EchoWebSocket(WebSocketHandler):
    """Web-Socket handler"""

    def open(self):
        """During web-socket connection"""
        pass

    def on_message(self, message):
        """During client message"""
        click.echo(
            colored("Serving /ws: ", "yellow") + colored(message, "blue", attrs=['bold'])
        )
        self.write_message("You said: " + message)

    def on_close(self):
        """During client disconnect"""
        pass

    def check_origin(self, origin):
        """Needs to be true"""
        return True


class CacheGetHandler(RequestHandler):
    """Handles /get"""

    def get(self):
        msg = cache.get()
        click.echo(
            colored("Serving /get: ", "yellow") + colored(msg, "blue", attrs=['bold'])
        )
        self.write(msg)


class CacheUpdateHandler(RequestHandler):
    """Handles /update"""

    def get(self):
        msg = "Updating"
        cache.update()
        click.echo(
            colored("Serving /update: ", "yellow") + colored(msg, "blue", attrs=['bold'])
        )
        self.write(msg)


class MainHandler(RequestHandler):
    def get(self):
        msg = "Hello, world"
        click.echo(
            colored("Serving /: ", "yellow") + colored(msg, "blue", attrs=['bold'])
        )
        self.write(msg)


def make_app():
    """ Make tornado app
    :return: app
    """
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/get", CacheGetHandler),
        (r"/update", CacheUpdateHandler),
        (r'/ws', EchoWebSocket, {}),

    ])


def bootup(port, delay):
    """Main entry point
    :param port: Running port
    """
    click.echo(
        colored(f"Port: ", "yellow") + colored(f"{port}", "red", attrs=['underline'])
    )
    click.echo(
        colored(f"Delay: ", "yellow") + colored(f"{delay}s", "red", attrs=['underline'])
    )
    global DELAY
    DELAY = delay
    app = make_app()

    app.listen(port)
    IOLoop.current().start()


def main():
    bootup(8000)


if __name__ == '__main__':
    main()
