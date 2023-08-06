# SPDX-FileCopyrightText: 2017-2021 Alliander N.V. <korte.termijn.prognoses@alliander.com> # noqa E501>
#
# SPDX-License-Identifier: MPL-2.0
import argparse
import importlib
import pkgutil

from openstf import PROJECT_ROOT


def parse_cli_arguments():
    # create the top-level parser
    parser = argparse.ArgumentParser(prog="Short term forecasting")

    subparsers = parser.add_subparsers(help="Run a task")

    # create the parser for the "task" command
    parser_task = subparsers.add_parser("task")
    parser_task.add_argument(
        "name", action="store", type=str, help="Name of the task you want to run."
    )

    args = parser.parse_args()
    return args


def validate_task_name(task_name):
    task_pkg_dir = PROJECT_ROOT / "openstf" / "tasks"
    task_modules = [m for _, m, _ in pkgutil.iter_modules([task_pkg_dir])]

    if task_name not in task_modules:
        raise RuntimeError(
            f"Unknown task: '{task_name}', valid tasks are :{', '.join(task_modules)}."
        )


def main():
    args = parse_cli_arguments()

    task_name = args.name

    validate_task_name(task_name)

    # import task
    task = importlib.import_module(f"openstf.tasks.{task_name}")
    # run task
    task.main()


if __name__ == "__main__":
    main()
