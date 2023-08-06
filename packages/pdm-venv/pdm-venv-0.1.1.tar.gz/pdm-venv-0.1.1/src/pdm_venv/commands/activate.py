import argparse
from pathlib import Path

import shellingham
from pdm import termui
from pdm.cli.commands.base import BaseCommand
from pdm.cli.options import verbose_option
from pdm.project import Project
from pdm.utils import is_venv_python

from pdm_venv.utils import BIN_DIR, iter_venvs


class ActivateCommand(BaseCommand):
    """List all virtualenvs associated with this project"""

    arguments = [verbose_option]

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("env", nargs="?", help="The key of the virtualenv")

    def handle(self, project: Project, options: argparse.Namespace) -> None:
        if options.env:
            venv = next(
                (venv for key, venv in iter_venvs(project) if key == options.env), None
            )
            if not venv:
                project.core.ui.echo(
                    termui.yellow(f"No virtualenv with key {options.env} is found"),
                    err=True,
                )
                raise SystemExit(1)
        else:
            # Use what is saved in .pdm.toml
            interpreter = project.python_executable
            if is_venv_python(interpreter):
                venv = Path(interpreter).parent.parent
            else:
                project.core.ui.echo(
                    termui.yellow(
                        f"Can't activate a non-venv Python{interpreter}, "
                        "you can specify one with pdm venv activate <env_name>"
                    )
                )
                raise SystemExit(1)
        project.core.ui.echo(self.get_activate_command(venv))

    def get_activate_command(self, venv: Path) -> str:
        shell, _ = shellingham.detect_shell()
        if shell == "fish":
            filename = "activate.fish"
        elif shell == "csh":
            filename = "activate.csh"
        elif shell == "powershell":
            filename = "Activate.ps1"
        else:
            filename = "activate"
        return str(venv / BIN_DIR / filename)
