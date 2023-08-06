import argparse
import errno
import io
import os
import pty
import sys
import unittest

import pytest

from pkgcore.config import central, errors
from pkgcore.test.scripts.helpers import ArgParseMixin
from pkgcore.util import commandline

# Careful: the tests should not hit a load_config() call!


def sect():
    """Just a no-op to use as configurable class."""


def mk_config(*args, **kwds):
    return central.CompatConfigManager(
        central.ConfigManager(*args, **kwds))


class _Trigger(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        """Fake a config load."""

        # HACK: force skipping the actual config loading. Might want
        # to do something more complicated here to allow testing if
        # --empty-config actually works.
        namespace.empty_config = True


class TestModifyConfig(ArgParseMixin):

    parser = commandline.ArgumentParser(domain=False, version=False)
    parser.add_argument('--trigger', nargs=0, action=_Trigger)

    def parse(self, *args, **kwargs):
        """Overridden to allow the load_config call."""
        # argparse needs a list (it does make a copy, but it uses [:]
        # to do it, which is a noop on a tuple).
        namespace = self.parser.parse_args(list(args))

        # HACK: force skipping the actual config loading. Might want
        # to do something more complicated here to allow testing if
        # --empty-config actually works.
        namespace.empty_config = True

        return namespace

    def test_empty_config(self):
        assert self.parse('--empty-config', '--trigger')

    def test_modify_config(self):
        namespace = self.parse(
            '--empty-config', '--new-config',
            'foo', 'class', 'tests.util.test_commandline.sect',
            '--trigger')
        assert namespace.config.collapse_named_section('foo')

        namespace = self.parse(
            '--empty-config', '--new-config',
            'foo', 'class', 'tests.util.test_commandline.missing',
            '--add-config', 'foo', 'class',
            'tests.util.test_commandline.sect',
            '--trigger')
        assert namespace.config.collapse_named_section('foo')

        namespace = self.parse(
            '--empty-config',
            '--add-config', 'foo', 'inherit', 'missing',
            '--trigger')
        with pytest.raises(errors.ConfigurationError):
            namespace.config.collapse_named_section('foo')
