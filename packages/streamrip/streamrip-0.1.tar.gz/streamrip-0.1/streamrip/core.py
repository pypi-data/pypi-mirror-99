import logging
import os
import re
from getpass import getpass
from string import Formatter
from typing import Generator, Optional, Tuple, Union

import click
from simple_term_menu import TerminalMenu

from .clients import DeezerClient, QobuzClient, TidalClient
from .config import Config
from .constants import CONFIG_PATH, DB_PATH, URL_REGEX
from .db import MusicDB
from .downloader import Album, Artist, Label, Playlist, Track
from .exceptions import AuthenticationError, ParsingError
from .utils import capitalize

logger = logging.getLogger(__name__)


MEDIA_CLASS = {
    "album": Album,
    "playlist": Playlist,
    "artist": Artist,
    "track": Track,
    "label": Label,
}
CLIENTS = {"qobuz": QobuzClient, "tidal": TidalClient, "deezer": DeezerClient}
Media = Union[Album, Playlist, Artist, Track]  # type hint


class MusicDL(list):
    def __init__(
        self,
        config: Optional[Config] = None,
    ):

        self.url_parse = re.compile(URL_REGEX)
        self.config = config
        if self.config is None:
            self.config = Config(CONFIG_PATH)

        self.clients = {
            "qobuz": QobuzClient(),
            "tidal": TidalClient(),
            "deezer": DeezerClient(),
        }

        if config.session["database"]["enabled"]:
            if config.session["database"]["path"] is not None:
                self.db = MusicDB(config.session["database"]["path"])
            else:
                self.db = MusicDB(DB_PATH)
                config.file["database"]["path"] = DB_PATH
                config.save()
        else:
            self.db = []

    def prompt_creds(self, source: str):
        """Prompt the user for credentials.

        :param source:
        :type source: str
        """
        click.secho(f"Enter {capitalize(source)} email:", fg="green")
        self.config.file[source]["email"] = input()
        click.secho(
            f"Enter {capitalize(source)} password (will not show on screen):",
            fg="green",
        )
        self.config.file[source]["password"] = getpass(
            prompt=""
        )  # does hashing work for tidal?

        self.config.save()
        click.secho(f'Credentials saved to config file at "{self.config._path}"')

    def assert_creds(self, source: str):
        assert source in ("qobuz", "tidal", "deezer"), f"Invalid source {source}"
        if source == "deezer":
            # no login for deezer
            return

        if (
            self.config.file[source]["email"] is None
            or self.config.file[source]["password"] is None
        ):
            self.prompt_creds(source)

    def handle_urls(self, url: str):
        """Download an url

        :param url:
        :type url: str
        :raises InvalidSourceError
        :raises ParsingError
        """
        source, url_type, item_id = self.parse_urls(url)[0]
        if item_id in self.db:
            logger.info(f"{url} already downloaded, use --no-db to override.")
            return

        self.handle_item(source, url_type, item_id)

    def handle_item(self, source: str, media_type: str, item_id: str):
        self.assert_creds(source)

        client = self.get_client(source)

        item = MEDIA_CLASS[media_type](client=client, id=item_id)
        self.append(item)

    def download(self):
        arguments = {
            "database": self.db,
            "parent_folder": self.config.session["downloads"]["folder"],
            "quality": self.config.session["downloads"]["quality"],
            "embed_cover": self.config.session["metadata"]["embed_cover"],
        }
        logger.debug("Arguments from config: %s", arguments)
        for item in self:
            if isinstance(item, Artist):
                filters_ = tuple(
                    k for k, v in self.config.session["filters"].items() if v
                )
                arguments["filters"] = filters_
                logger.debug("Added filter argument for artist/label: %s", filters_)

            item.load_meta()
            click.secho(f"Downloading {item!s}", fg="bright_green")
            item.download(**arguments)
            if self.config.session["conversion"]["enabled"]:
                click.secho(
                    f"Converting {item!s} to {self.config.session['conversion']['codec']}",
                    fg="cyan",
                )
                item.convert(**self.config.session["conversion"])

    def get_client(self, source: str):
        client = self.clients[source]
        if not client.logged_in:
            self.assert_creds(source)
            self.login(client)
        return client

    def convert_all(self, codec, **kwargs):
        click.secho("Converting the downloaded tracks...", fg="cyan")
        for item in self:
            item.convert(codec, **kwargs)

    def login(self, client):
        creds = self.config.creds(client.source)
        if not client.logged_in:
            while True:
                try:
                    client.login(**creds)
                    break
                except AuthenticationError:
                    click.secho("Invalid credentials, try again.")
                    self.prompt_creds(client.source)
            if (
                client.source == "qobuz"
                and not creds.get("secrets")
                and not creds.get("app_id")
            ):
                (
                    self.config.file["qobuz"]["app_id"],
                    self.config.file["qobuz"]["secrets"],
                ) = client.get_tokens()
                self.config.save()

    def parse_urls(self, url: str) -> Tuple[str, str]:
        """Returns the type of the url and the id.

        Compatible with urls of the form:
            https://www.qobuz.com/us-en/{type}/{name}/{id}
            https://open.qobuz.com/{type}/{id}
            https://play.qobuz.com/{type}/{id}
            /us-en/{type}/-/{id}

            https://www.deezer.com/us/{type}/{id}
            https://tidal.com/browse/{type}/{id}

        :raises exceptions.ParsingError
        """
        parsed = self.url_parse.findall(url)

        if parsed != []:
            return parsed

        raise ParsingError(f"Error parsing URL: `{url}`")

    def from_txt(self, filepath: Union[str, os.PathLike]):
        """
        Handle a text file containing URLs. Lines starting with `#` are ignored.

        :param filepath:
        :type filepath: Union[str, os.PathLike]
        :raises OSError
        :raises exceptions.ParsingError
        """
        with open(filepath) as txt:
            lines = " ".join(
                line for line in txt.readlines() if not line.strip().startswith("#")
            )

        return self.parse_urls(lines)

    def search(
        self, source: str, query: str, media_type: str = "album", limit: int = 200
    ) -> Generator:
        client = self.get_client(source)
        results = client.search(query, media_type)

        i = 0
        if isinstance(results, Generator):  # QobuzClient
            for page in results:
                tracklist = (
                    page[f"{media_type}s"]["items"]
                    if media_type != "featured"
                    else page["albums"]["items"]
                )
                for item in tracklist:
                    yield MEDIA_CLASS[
                        media_type if media_type != "featured" else "album"
                    ].from_api(item, client)
                    i += 1
                    if i > limit:
                        return
        else:
            for item in results.get("data") or results.get("items"):
                yield MEDIA_CLASS[media_type].from_api(item, client)
                i += 1
                if i > limit:
                    return

    def preview_media(self, media):
        if isinstance(media, Album):
            fmt = (
                "{albumartist} - {title}\n"
                "Released on {year}\n{tracktotal} tracks\n"
                "{bit_depth} bit / {sampling_rate} Hz\n"
                "Version: {version}"
            )
            fields = (fname for _, fname, _, _ in Formatter().parse(fmt) if fname)
            ret = fmt.format(**{k: media.get(k, "Unknown") for k in fields})
        else:
            raise NotImplementedError

        return ret

    def interactive_search(
        self, query: str, source: str = "qobuz", media_type: str = "album"
    ):
        results = tuple(self.search(source, query, media_type, limit=50))

        def title(res):
            return f"{res[0]+1}. {res[1].title}"

        def from_title(s):
            num = []
            for char in s:
                if char.isdigit():
                    num.append(char)
                else:
                    break
            return self.preview_media(results[int("".join(num)) - 1])

        menu = TerminalMenu(
            map(title, enumerate(results)),
            preview_command=from_title,
            preview_size=0.5,
            title=f"{capitalize(source)} {media_type} search",
            cycle_cursor=True,
            clear_screen=True,
        )
        choice = menu.show()
        if choice is None:
            return False
        else:
            self.append(results[choice])
            return True
