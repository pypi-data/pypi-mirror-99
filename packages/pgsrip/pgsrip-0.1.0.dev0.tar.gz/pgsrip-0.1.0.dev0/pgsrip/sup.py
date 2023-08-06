# -*- coding: utf-8 -*-
import logging
from typing import Iterable

from .media import Media, Pgs, MediaPath
from .options import Options

logger = logging.getLogger(__name__)


class Sup(Media):

    def __init__(self, path: str):
        media_path = MediaPath(path)
        super().__init__(media_path, languages={media_path.language})

    def get_pgs_medias(self, options: Options) -> Iterable[Pgs]:
        yield Pgs(self.media_path, data_reader=self.media_path.get_data)
