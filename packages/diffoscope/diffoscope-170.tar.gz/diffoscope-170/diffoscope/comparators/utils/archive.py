#
# diffoscope: in-depth comparison of files, archives, and directories
#
# Copyright © 2016-2020 Chris Lamb <lamby@debian.org>
#
# diffoscope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# diffoscope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with diffoscope.  If not, see <https://www.gnu.org/licenses/>.

import os
import abc
import logging

from diffoscope.profiling import profile
from diffoscope.tempfiles import get_temporary_directory

from ..missing_file import MissingFile, AbstractMissingType

from .file import File
from .container import Container

logger = logging.getLogger(__name__)


class Archive(Container, metaclass=abc.ABCMeta):
    def __new__(cls, source, *args, **kwargs):
        if isinstance(source, MissingFile):
            return super(Container, MissingArchive).__new__(MissingArchive)
        return super(Container, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with profile("open_archive", self):
            self._archive = self.open_archive()

    def __del__(self):
        with profile("close_archive", self):
            self.close_archive()

    @property
    def archive(self):
        return self._archive

    @abc.abstractmethod
    def open_archive(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def close_archive(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_member_names(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def extract(self, member_name, dest_dir):
        raise NotImplementedError()

    def get_member(self, member_name):
        return ArchiveMember(self, member_name)

    def get_compressed_content_name(self, expected_extension):
        basename = os.path.basename(self.source.name)

        if not basename.endswith(expected_extension):
            return "%s-content" % basename

        return basename[: -len(expected_extension)]


class ArchiveMember(File):
    def __init__(self, container, member_name):
        super().__init__(container=container)
        self._name = member_name
        self._temp_dir = None
        self._path = None

    @property
    def path(self):
        if self._path is None:
            assert self._temp_dir is None
            self._temp_dir = get_temporary_directory(
                suffix=self.container.__class__.__name__
            )
            logger.debug(
                "Unpacking %s from %s to %s",
                self._name,
                self.container.source.name,
                self._temp_dir.name,
            )
            with profile("container_extract", self.container):
                self._path = self.container.extract(
                    self._name, self._temp_dir.name
                )
        return self._path

    def cleanup(self):
        if self._path is not None:
            self._path = None
        if self._temp_dir is not None:
            try:
                self._temp_dir.cleanup()
            except FileNotFoundError:
                pass
            self._temp_dir = None
        super().cleanup()

    def is_directory(self):
        return False

    def is_symlink(self):
        return False

    def is_device(self):
        return False


class MissingArchiveLikeObject(AbstractMissingType):
    def getnames(self):
        return []

    def list(self, *args, **kwargs):
        return ""

    def close(self):
        pass


class MissingArchive(Archive, AbstractMissingType):
    @property
    def source(self):
        return None

    def open_archive(self):
        return MissingArchiveLikeObject()

    def close_archive(self):
        pass

    def get_member_names(self):
        return []

    def extract(self, member_name, dest_dir):
        # should never be called
        raise NotImplementedError()

    def get_member(self, member_name):
        return MissingFile("/dev/null")

    # Be nice to gzip and the likes
    @property
    def path(self):
        return "/dev/null"
