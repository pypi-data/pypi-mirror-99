"""
Estimark entrypoint
"""

import os
import sys
import logging
from json import loads
from pathlib import Path
from typing import List
from injectark import Injectark
from estimark.factories import factory_builder, strategy_builder
from estimark.presenters.shell import Shell
from estimark.core.common import config


def main(args: List[str] = None):  # pragma: no cover
    args = args or sys.argv[1:]
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                        format='%(message)s')

    strategy = strategy_builder.build(config['strategies'])
    factory = factory_builder.build(config)

    injector = Injectark(strategy, factory)

    Shell(config, injector).run(args)


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
