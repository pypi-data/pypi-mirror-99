# -*- coding: utf-8 -*-

import os

from lintwork.config.config import ConfigFile
from lintwork.printer.printer import Printer
from lintwork.work.cpp.checkpatch import Checkpatch  # noqa: F401
from lintwork.work.cpp.cpplint import Cpplint  # noqa: F401
from lintwork.work.java.aosp import Aosp  # noqa: F401
from lintwork.work.java.checkstyle import Checkstyle  # noqa: F401
from lintwork.work.python.flake8 import Flake8  # noqa: F401
from lintwork.work.shell.shellcheck import Shellcheck  # noqa: F401


class WorkException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Work(object):
    def __init__(self, config):
        if config is None:
            raise WorkException("config invalid")
        self._config = config
        self._spec = config.config_file.get(ConfigFile.SPEC, None)
        if self._spec is None:
            raise WorkException("spec invalid")

    def _dump(self, data):
        printer = Printer()
        printer.run(data=data, name=self._config.output_file, append=False)

    def routine(self, project):
        if not isinstance(project, str) or not os.path.exists(project):
            raise WorkException("project invalid")
        buf = []
        for key in self._spec.keys():
            for k, v in self._spec[key].items():
                cls = globals().get(k.capitalize(), None)
                if cls is not None:
                    buf.extend(cls(v).run(project))
        if len(self._config.output_file) != 0:
            self._dump(buf)
        return buf
