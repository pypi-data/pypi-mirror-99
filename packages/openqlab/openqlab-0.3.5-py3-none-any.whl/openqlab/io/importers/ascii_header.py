import logging
import re
from pathlib import Path
from typing import List

import pandas as pd

from openqlab.io.base_importer import StreamImporter
from openqlab.io.data_container import DataContainer
from openqlab.io.importers.utils import UnknownFileType

log = logging.getLogger(__name__)

# logger.setLevel(logging.DEBUG)


class ASCII_Header(StreamImporter):
    PRIORITY = -5
    NAME = "ASCII_Header"
    AUTOIMPORTER = True
    STARTING_LINES: List[str] = []
    HEADER_ESCAPE: str = r"[#$%]"
    LINE_SPLIT: str = r"[,:;\s\t]"

    def __init__(self, stream):
        super().__init__(stream)
        self._comment = ""
        self.prefix = None
        self.header_line = None

    def read(self):
        self._read_header()
        if self.header_line is None:
            self.prefix = f"{Path(self._stream.name).stem}_"
        try:
            return DataContainer(
                pd.read_csv(
                    self._stream,
                    sep=None,
                    engine="python",
                    prefix=self.prefix,
                    index_col=0,
                    comment="#",
                    header=self.header_line,
                ),
                header=self._header,
            )
        except Exception as e:
            raise UnknownFileType from e

    def _read_header(self):

        line = True
        while line:
            line = self._stream.readline()
            log.debug(rf"line:{repr(line)}")
            match = re.match(rf"^{self.HEADER_ESCAPE}{{2}}\s*", line)
            if match:
                self._comment += line[match.end() :]
                continue
            match = re.match(rf"^{self.HEADER_ESCAPE}\s*", line)
            if match:
                keyword, value = re.split(
                    self.LINE_SPLIT, line[match.end() :], maxsplit=1
                )
                self._header[keyword] = value.strip()
                continue
            if not re.match(r"[-+]*\d+", line):
                self.header_line = 0
            break
        if not self._comment or not self._header:
            pass
            # raise UnknownFileType
        self._header["comment"] = self._comment.strip()

        log.debug(f"position:{self._stream.tell()}")
        log.debug(f"len(line):{len(line)}")

        self._stream.seek(self._stream.tell() - len(line))
