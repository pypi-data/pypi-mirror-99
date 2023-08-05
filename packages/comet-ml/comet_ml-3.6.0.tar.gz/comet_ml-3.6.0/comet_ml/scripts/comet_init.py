#!/usr/bin/env python
# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2015-2021 Comet ML INC
#  This file can not be copied and/or distributed without
#  the express permission of Comet ML Inc.
# *******************************************************

"""
Creates a new project directory with a Python script and dependency file that
shows how to incorporate Comet with various ML libraries.
"""

from __future__ import print_function

import argparse
import logging
import os
import sys

from comet_ml.config import get_config

LOGGER = logging.getLogger("comet_ml")
ADDITIONAL_ARGS = True


def get_parser_arguments(parser):
    parser.add_argument(
        "-l",
        "--language",
        default="python",
        help="The language of example script to generate",
    )
    parser.add_argument(
        "-r",
        "--replay",
        action="store_const",
        const=True,
        default=False,
        help="Replay the last comet init",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_const",
        const=True,
        default=False,
        help="Force overwrite output directory if it exists",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=".",
        help="Output directory for scripts to go to",
    )


def main(args):
    # Called via `comet init ...`
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    get_parser_arguments(parser)
    parsed_args, remaining = parser.parse_known_args(args)

    init(parsed_args, remaining)


def init(parsed_args, remaining):
    try:
        from cookiecutter.main import cookiecutter
        from cookiecutter.exceptions import OutputDirExistsException
        from click.exceptions import Abort
    except ImportError:
        LOGGER.error(
            "Please install cookiecutter with `pip install cookiecutter>1.7.0`"
        )
        sys.exit(1)

    valid_languages = ["python", "r"]
    if parsed_args.language.lower() in valid_languages:
        directory = parsed_args.language.lower()
    else:
        LOGGER.error(
            "comet init currently only support these languages: %s", valid_languages
        )
        sys.exit(1)

    print("Building Comet example script from recipe...")
    print("=" * 50)
    print("After initializing, please cd into your new project and run the script.")
    print()
    if not parsed_args.replay:
        print("Please supply values for the following items:")
        print()

    template = os.environ.get(
        "COMET_INIT_RECIPE_PATH", "https://github.com/comet-ml/comet-recipes.git"
    )

    try:
        cookiecutter(
            template,
            replay=parsed_args.replay,
            overwrite_if_exists=parsed_args.force,
            output_dir=parsed_args.output,
            directory=directory,
            extra_context={"comet_api_key": get_config("comet.api_key")},
        )
    except OutputDirExistsException:
        print()
        LOGGER.error("directory already exists; use `comet init -f`")
        sys.exit(1)
    except Abort:
        print()
        LOGGER.error("comet init was aborted")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
