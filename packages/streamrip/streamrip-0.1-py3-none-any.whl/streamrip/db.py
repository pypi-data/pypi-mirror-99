import logging
import os
import sqlite3
from typing import Union

logger = logging.getLogger(__name__)


class MusicDB:
    """Simple interface for the downloaded track database."""

    def __init__(self, db_path: Union[str, os.PathLike]):
        """Create a MusicDB object

        :param db_path: filepath of the database
        :type db_path: Union[str, os.PathLike]
        """
        self.path = db_path
        if not os.path.exists(self.path):
            self.create()

    def create(self):
        """Create a database at `self.path`"""
        with sqlite3.connect(self.path) as conn:
            try:
                conn.execute("CREATE TABLE downloads (id TEXT UNIQUE NOT NULL);")
                logger.debug("Download-IDs database created: %s", self.path)
            except sqlite3.OperationalError:
                pass

            return self.path

    def __contains__(self, item_id: Union[str, int]) -> bool:
        """Checks whether the database contains an id.

        :param item_id: the id to check
        :type item_id: str
        :rtype: bool
        """
        with sqlite3.connect(self.path) as conn:
            return (
                conn.execute(
                    "SELECT id FROM downloads where id=?", (item_id,)
                ).fetchone()
                is not None
            )

    def add(self, item_id: str):
        """Adds an id to the database.

        :param item_id:
        :type item_id: str
        """
        with sqlite3.connect(self.path) as conn:
            try:
                conn.execute(
                    "INSERT INTO downloads (id) VALUES (?)",
                    (item_id,),
                )
                conn.commit()
            except sqlite3.Error as error:
                logger.error("Unexpected DB error: %s", error)
