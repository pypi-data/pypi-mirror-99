"""A WhiteNoiseProvider Service Provider."""

from whitenoise import WhiteNoise

from ..provider import ServiceProvider
from ..helpers import config


class WhitenoiseProvider(ServiceProvider):

    wsgi = False

    def register(self):
        pass

    def boot(self):
        """Wrap the WSGI server in a whitenoise container."""
        from config import application

        self.app.bind(
            "WSGI",
            WhiteNoise(
                self.app.make("WSGI"),
                root=config("application.static_root"),
                autorefresh=application.DEBUG,
            ),
        )

        for location, alias in self.app.make("staticfiles").items():
            self.app.make("WSGI").add_files(location, prefix=alias)
