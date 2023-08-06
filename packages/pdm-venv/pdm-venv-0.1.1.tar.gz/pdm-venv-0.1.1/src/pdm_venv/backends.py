import abc
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Mapping, Optional, Tuple, Type

from pdm import Project, termui
from pdm.exceptions import ProjectError
from pdm.models.in_process import get_python_version
from pdm.utils import cached_property, get_python_version_string
from pythonfinder import Finder

from pdm_venv.utils import get_venv_prefix


class VirtualenvCreateError(ProjectError):
    pass


class Backend(abc.ABC):
    """The base class for virtualenv backends"""

    def __init__(self, project: Project, python: Optional[str]) -> None:
        self.project = project
        self.python = python

    @cached_property
    def _resolved_interpreter(self) -> str:
        if not self.python:
            return self.project.python_executable
        if os.path.isabs(self.python):
            return self.python
        finder = Finder()
        result = finder.find_python_version(self.python)
        if not result:
            raise VirtualenvCreateError(f"Can't find python interpreter {self.python}")
        return result.path.as_posix()

    @property
    def ident(self) -> str:
        """Get the identifier of this virtualenv.
        self.python can be one of:
            3.8
            /usr/bin/python
            3.9.0a4
            python3.8
        """
        python_version, is_64bit = get_python_version(self._resolved_interpreter, True)
        return get_python_version_string(python_version, is_64bit)

    def subprocess_call(self, cmd: List[str], **kwargs) -> None:
        self.project.core.ui.echo(f"Run command: {cmd}", verbosity=termui.DETAIL)
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            raise VirtualenvCreateError(e) from None

    def _ensure_clean(self, location: Path, force: bool = False) -> None:
        if not location.exists():
            return
        if not force:
            raise VirtualenvCreateError(f"The location {location} is not empty")
        self.project.core.ui.echo(
            f"Cleaning existing target directory {location}", err=True
        )
        shutil.rmtree(location)

    def get_location(self, name: Optional[str]) -> Path:
        venv_parent = Path(self.project.config["venv.location"])
        if not venv_parent.is_dir():
            venv_parent.mkdir(exist_ok=True, parents=True)
        return venv_parent / f"{get_venv_prefix(self.project)}{name or self.ident}"

    def create(
        self, name: Optional[str] = None, args: Tuple[str] = (), force: bool = False
    ) -> Path:
        location = self.get_location(name)
        self._ensure_clean(location, force)
        self.perform_create(location, args)
        return location

    @abc.abstractmethod
    def perform_create(self, location: Path, args: Tuple[str] = ()) -> Path:
        pass


class VirtualenvBackend(Backend):
    def perform_create(self, location: Path, args: Tuple[str] = ()) -> Path:
        cmd = [sys.executable, "-m", "virtualenv", location]
        cmd.extend(["-p", self._resolved_interpreter])
        cmd.extend(args)
        self.subprocess_call(cmd)


class VenvBackend(VirtualenvBackend):
    def perform_create(self, location: Path, args: Tuple[str]) -> Path:
        cmd = [self._resolved_interpreter, "-m", "venv", location] + list(args)
        self.subprocess_call(cmd)


class CondaBackend(Backend):
    def perform_create(self, location: Path, args: Tuple[str]) -> Path:
        cmd = [
            "conda",
            "create",
            "--yes",
            "--prefix",
            location,
            # Ensure the pip package is installed.
            "pip",
        ]

        cmd.extend(args)

        if self.python:
            python_dep = "python={}".format(self.python)
        else:
            python_dep = "python"
        cmd.append(python_dep)
        self.subprocess_call(cmd)


BACKENDS: Mapping[str, Type[Backend]] = {
    "virtualenv": VirtualenvBackend,
    "venv": VenvBackend,
    "conda": CondaBackend,
}
