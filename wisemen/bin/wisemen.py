#!/usr/bin/env python
import os
import sys
from argparse import ArgumentParser
from fileinput import FileInput
from shutil import copy2

from django.core.management import ManagementUtility
from wagtail.bin.wagtail import UpdateModulePaths

import wisemen
from wisemen import settings as wisemen_settings


class Command:
    description = None

    def create_parser(self, command_name=None):
        if command_name is None:
            prog = None
        else:
            # hack the prog name as reported to ArgumentParser to include the command
            prog = "%s %s" % (prog_name(), command_name)

        parser = ArgumentParser(
            description=getattr(self, "description", None), add_help=False, prog=prog
        )
        self.add_arguments(parser)
        return parser

    def add_arguments(self, parser):
        pass

    def print_help(self, command_name):
        parser = self.create_parser(command_name=command_name)
        parser.print_help()

    def execute(self, argv):
        parser = self.create_parser()
        options = parser.parse_args(sys.argv[2:])
        options_dict = vars(options)
        self.run(**options_dict)


class CreateProject(Command):
    description = "Creates the directory structure for a new Wisemen Wagtail/Django project."

    def add_arguments(self, parser):
        parser.add_argument("project_name", help="Name for your Wagtail project")
        parser.add_argument(
            "dest_dir",
            nargs="?",
            help="Destination directory inside which to create the project",
        )

    def run(self, project_name=None, dest_dir=None):
        # Make sure given name is not already in use by another python package/module.
        try:
            __import__(project_name)
        except ImportError:
            pass
        else:
            sys.exit(
                "'%s' conflicts with the name of an existing "
                "Python module and cannot be used as a project "
                "name. Please try another name." % project_name
            )

        print(  # noqa
            "Creating a Wagtail project called %(project_name)s"
            % {"project_name": project_name}
        )  # noqa

        # Create the project from the Wagtail template using startapp

        # First find the path to Wagtail
        import wagtail

        wagtail_path = os.path.dirname(wagtail.__file__)
        template_path = os.path.join(wagtail_path, "project_template")

        # Call django-admin startproject
        utility_args = [
            "django-admin",
            "startproject",
            "--template=" + template_path,
            "--ext=html,rst",
            "--name=Dockerfile",
            project_name,
        ]

        if dest_dir:
            utility_args.append(dest_dir)

        utility = ManagementUtility(utility_args)
        utility.execute()

        # Prepare the project specific setting file.
        settings_file = os.path.join(wisemen_settings.__path__[0], 'project_settings.py')
        with FileInput(settings_file, inplace=True) as file:
            for line in file:
                print(line.replace("{project_name}", project_name), end="")
        copy2(settings_file, os.path.join(project_name, f"{project_name}/settings", "base.py"))
        os.remove(settings_file)
        # Prepare the project specific environment file.
        environment_file = os.path.join(wisemen_settings.__path__[0], 'project_env')
        with FileInput(environment_file, inplace=True) as file:
            for line in file:
                print(line.replace("{project_name}", project_name), end="")
        copy2(environment_file, os.path.join(project_name, ".envrc"))
        os.remove(environment_file)
        # Set the urls file.
        environment_file = os.path.join(wisemen_settings.__path__[0], 'urls.py')
        copy2(environment_file, os.path.join(project_name, f"{project_name}/urls.py"))
        os.remove(environment_file)


        print(  # noqa
            "Success! %(project_name)s has been created"
            % {"project_name": project_name}
        )  # noqa

        nextsteps = """
        Next steps:
            1. Update your .envrc with the correct values and run direnv allow
            2. Set the correct languages in the base.py settings file
            3. python manage.py migrate
            4. python manage.py createsuperuser
            5. python manage.py runserver
            6. Go to http://localhost:8000/admin/ and start editing!
        """
        print(nextsteps % {"directory": project_name})

class Version(Command):
    description = "List which version of Wisemen and Wagtail you are using"

    def run(self):
        import wagtail
        import django

        wisemen_version = wisemen.__version__
        wagtail_version = wagtail.get_version(wagtail.VERSION)

        # Get the Django version
        django_version = django.get_version(django.VERSION)

        print(f"You are using Wisemen Wagtail Core {wisemen_version} (Wagtail {wagtail_version}, Django {django_version})")


COMMANDS = {
    "start": CreateProject(),
    "updatemodulepaths": UpdateModulePaths(),
    "--version": Version(),
}


def prog_name():
    return os.path.basename(sys.argv[0])


def help_index():
    print(  # noqa
        "Type '%s help <subcommand>' for help on a specific subcommand.\n" % prog_name()
    )  # NOQA
    print("Available subcommands:\n")  # NOQA
    for name, cmd in sorted(COMMANDS.items()):
        print("    %s%s" % (name.ljust(20), cmd.description))  # NOQA


def unknown_command(command):
    print("Unknown command: '%s'" % command)  # NOQA
    print("Type '%s help' for usage." % prog_name())  # NOQA
    sys.exit(1)


def main():
    try:
        command_name = sys.argv[1]
    except IndexError:
        help_index()
        return

    if command_name == "help":
        try:
            help_command_name = sys.argv[2]
        except IndexError:
            help_index()
            return

        try:
            command = COMMANDS[help_command_name]
        except KeyError:
            unknown_command(help_command_name)
            return

        command.print_help(help_command_name)
        return

    try:
        command = COMMANDS[command_name]
    except KeyError:
        unknown_command(command_name)
        return

    command.execute(sys.argv)


if __name__ == "__main__":
    main()