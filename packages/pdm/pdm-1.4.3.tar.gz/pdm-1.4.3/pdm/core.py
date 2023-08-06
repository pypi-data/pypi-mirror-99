from __future__ import annotations

import argparse
import importlib
import os
import pkgutil
import sys
from typing import Optional, Type

import click
from pip._vendor import pkg_resources
from resolvelib import Resolver

from pdm import termui
from pdm.cli.actions import migrate_pyproject, print_pep582_command
from pdm.cli.commands.base import BaseCommand
from pdm.cli.options import ignore_python_option, pep582_option, verbose_option
from pdm.cli.utils import PdmFormatter, PdmParser
from pdm.exceptions import PdmUsageError
from pdm.installers import Synchronizer
from pdm.models.repositories import PyPIRepository
from pdm.project import Project
from pdm.project.config import Config, ConfigItem

COMMANDS_MODULE_PATH = importlib.import_module("pdm.cli.commands").__path__


class Core:
    """A high level object that manages all classes and configurations"""

    def __init__(self):
        try:
            import importlib.metadata as importlib_metadata
        except ModuleNotFoundError:
            import importlib_metadata
        self.version = importlib_metadata.version(__name__.split(".")[0])

        self.project_class = Project
        self.repository_class = PyPIRepository
        self.resolver_class = Resolver
        self.synchronizer_class = Synchronizer

        self.ui = termui.UI()
        self.parser = None
        self.subparsers = None

    def init_parser(self):
        self.parser = PdmParser(
            prog="pdm",
            description="PDM - Python Development Master",
            formatter_class=PdmFormatter,
        )
        self.parser.is_root = True
        self.parser.add_argument(
            "-V",
            "--version",
            action="version",
            version="{}, version {}".format(
                click.style("pdm", bold=True), self.version
            ),
            help="show the version and exit",
        )
        verbose_option.add_to_parser(self.parser)
        ignore_python_option.add_to_parser(self.parser)
        pep582_option.add_to_parser(self.parser)

        self.subparsers = self.parser.add_subparsers()
        for _, name, _ in pkgutil.iter_modules(COMMANDS_MODULE_PATH):
            module = importlib.import_module(f"pdm.cli.commands.{name}", __name__)
            try:
                klass = module.Command
            except AttributeError:
                continue
            self.register_command(klass, klass.name or name)

    def __call__(self, *args, **kwargs):
        return self.main(*args, **kwargs)

    def ensure_project(
        self, options: argparse.Namespace, obj: Optional[Project]
    ) -> None:
        if obj is not None:
            options.project = obj
        if getattr(options, "project", None) is None:
            project = None
            global_project = getattr(options, "global_project", None)
            if global_project is True:
                project_factory = self.project_class.create_global
            elif global_project:
                project = global_project
            else:
                project_factory = self.project_class

            if project is None:
                project = project_factory(getattr(options, "project_path", None))
            options.project = project

        # Add reverse reference for core object
        options.project.core = self
        migrate_pyproject(options.project)

    def main(self, args=None, prog_name=None, obj=None, **extra):
        """The main entry function"""
        from pdm.models.pip_shims import global_tempdir_manager

        self.init_parser()
        self.load_plugins()

        options = self.parser.parse_args(args or None)
        self.ui.set_verbosity(options.verbose)
        if options.ignore_python:
            os.environ["PDM_IGNORE_SAVED_PYTHON"] = "1"

        if options.pep582:
            print_pep582_command(self.ui, options.pep582)
            sys.exit(0)

        self.ensure_project(options, obj)

        try:
            f = options.handler
        except AttributeError:
            self.parser.print_help()
            sys.exit(1)
        else:
            try:
                with global_tempdir_manager():
                    f(options.project, options)
            except Exception:
                etype, err, traceback = sys.exc_info()
                should_show_tb = not isinstance(err, PdmUsageError)
                if self.ui.verbosity > termui.NORMAL and should_show_tb:
                    raise err.with_traceback(traceback)
                self.ui.echo(
                    f"{termui.red('[' + etype.__name__ + ']')}: {err}", err=True
                )
                if should_show_tb:
                    self.ui.echo("Add '-v' to see the detailed traceback", fg="yellow")
                sys.exit(1)

    def register_command(
        self, command: Type[BaseCommand], name: Optional[str] = None
    ) -> None:
        """Register a subcommand to the subparsers,
        with an optional name of the subcommand.
        """
        command.project_class = self.project_class
        command.register_to(self.subparsers, name)

    @staticmethod
    def add_config(name: str, config_item: ConfigItem) -> None:
        """Add a config item to the configuration class"""
        Config.add_config(name, config_item)

    def load_plugins(self):
        """Import and load plugins under `pdm.plugin` namespace
        A plugin is a callable that accepts the core object as the only argument.

        :Example:

        def my_plugin(core: pdm.core.Core) -> None:
            ...

        """
        for plugin in pkg_resources.iter_entry_points("pdm"):
            plugin.load()(self)


def main(args=None):
    """The CLI entry function"""
    return Core().main(args)
