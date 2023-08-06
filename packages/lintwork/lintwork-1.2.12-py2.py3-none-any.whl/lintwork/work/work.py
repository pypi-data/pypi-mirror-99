# -*- coding: utf-8 -*-

import os

from lintwork.config.config import ConfigFile
from lintwork.printer.printer import Printer
from lintwork.work.aosp.lint import Lint
from lintwork.work.cpp.cpplint import Cpplint
from lintwork.work.java.checkstyle import Checkstyle
from lintwork.work.linux.checkpatch import Checkpatch
from lintwork.work.python.flake8 import Flake8
from lintwork.work.shell.shellcheck import Shellcheck


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
        self._instance = self._instantiate()

    def _dump(self, data):
        printer = Printer()
        printer.run(data=data, name=self._config.output_file, append=False)

    def _instantiate(self):
        return {
            "aosp": {
                Lint.__name__.lower(): Lint(self._spec["aosp"][Lint.__name__.lower()])
            },
            "cpp": {
                Cpplint.__name__.lower(): Cpplint(
                    self._spec["cpp"][Cpplint.__name__.lower()]
                )
            },
            "java": {
                Checkstyle.__name__.lower(): Checkstyle(
                    self._spec["java"][Checkstyle.__name__.lower()]
                )
            },
            "linux": {
                Checkpatch.__name__.lower(): Checkpatch(
                    self._spec["linux"][Checkpatch.__name__.lower()]
                )
            },
            "python": {
                Flake8.__name__.lower(): Flake8(
                    self._spec["python"][Flake8.__name__.lower()]
                )
            },
            "shell": {
                Shellcheck.__name__.lower(): Shellcheck(
                    self._spec["shell"][Shellcheck.__name__.lower()]
                )
            },
        }

    def routine(self, project):
        if not isinstance(project, str) or not os.path.exists(project):
            raise WorkException("project invalid")
        buf = []
        for key in self._spec.keys():
            b = self._instance.get(key, {})
            for k in self._spec[key].keys():
                if k in b.keys():
                    buf.extend(b[k].run(project))
        if len(self._config.output_file) != 0:
            self._dump(buf)
        return buf
