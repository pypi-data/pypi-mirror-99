#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import argparse
from tccli import six
from difflib import get_close_matches
from gettext import gettext
from tccli.error_msg import USAGE


class CustomAction(argparse.Action):

    def __init__(self, option_strings, dest, command_map, **kwargs):
        self.command_map = command_map
        super(CustomAction, self).__init__(option_strings, dest, choices=self.choices, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)

    @property
    def choices(self):
        return list(self.command_map.keys())

    @choices.setter
    def choices(self, val):
        pass


class BaseArgParser(argparse.ArgumentParser):
    Formatter = argparse.RawTextHelpFormatter

    ChoicesPerLine = 2

    def _check_value(self, action, value):
        if action.choices is not None and value not in action.choices:
            msg = ['Invalid choice, valid choices are:\n']
            for i in range(len(action.choices))[::self.ChoicesPerLine]:
                current = []
                for choice in action.choices[i:i + self.ChoicesPerLine]:
                    current.append('%-40s' % choice)
                msg.append(' | '.join(current))
            possible = get_close_matches(value, action.choices, cutoff=0.8)
            if possible:
                extra = ['\n\nInvalid choice: %r, maybe you meant:\n' % value]
                for word in possible:
                    extra.append('  * %s' % word)
                msg.extend(extra)
            raise argparse.ArgumentError(action, '\n'.join(msg))

    def parse_known_args(self, args=None, namespace=None):
        parsed, remaining = super(BaseArgParser, self).parse_known_args(args, namespace)
        terminal_encoding = getattr(sys.stdin, 'encoding', 'utf-8')
        if terminal_encoding is None:
            terminal_encoding = 'utf-8'
        for arg, value in vars(parsed).items():
            if isinstance(value, six.binary_type):
                setattr(parsed, arg, value.decode(terminal_encoding))
            elif isinstance(value, list):
                encoded = []
                for v in value:
                    if isinstance(v, six.binary_type):
                        encoded.append(v.decode(terminal_encoding))
                    else:
                        encoded.append(v)
                setattr(parsed, arg, encoded)
        return parsed, remaining

    def error(self, message):
        self.print_usage(sys.stderr)
        args = {'prog': self.prog, 'message': message}
        self.exit(252, gettext('%(prog)s: error: %(message)s\n') % args)


class CLIArgParser(BaseArgParser):

    def __init__(self, command_map, version, description, argument_map, prog=None):
        super(CLIArgParser, self).__init__(
            formatter_class=self.Formatter,
            add_help=False,
            conflict_handler='resolve',
            description=description,
            usage=USAGE,
            prog=prog)
        self._build(command_map, version, argument_map)

    def _create_choice_help(self, choices):
        help_str = ''
        for choice in sorted(choices):
            help_str += '* %s\n' % choice
        return help_str

    def _build(self, command_map, version, argument_map):
        for argument_name in argument_map:
            argument = argument_map[argument_name]
            argument.add_to_parser(self)
        self.add_argument('--version',
                          action="version",
                          version=version,
                          help='Display the version of this tool')
        self.add_argument('command', action=CustomAction, command_map=command_map)


class ActionArgParser(BaseArgParser):

    def __init__(self, actions_map):
        super(ActionArgParser, self).__init__(
            formatter_class=self.Formatter,
            add_help=False,
            conflict_handler='resolve',
            usage=USAGE)
        self._build(actions_map)

    def _build(self, actions_map):
        self.add_argument('operation', action=CustomAction,
                          command_map=actions_map)


class ArgMapArgParser(BaseArgParser):

    def __init__(self, argument_map, command_map=None):
        super(ArgMapArgParser, self).__init__(
            formatter_class=self.Formatter,
            add_help=False,
            usage=USAGE,
            conflict_handler='resolve')
        self._build(argument_map, command_map)

    def _build(self, argument_map, command_map):
        for arg_name in argument_map:
            argument = argument_map[arg_name]
            argument.add_to_parser(self)
        if command_map:
            self.add_argument('subcommand', action=CustomAction, command_map=command_map, nargs='?')

    def parse_known_args(self, args=None, namespace=None):
        if len(args) == 1 and args[0] == 'help':
            namespace = argparse.Namespace()
            namespace.help = 'help'
            return namespace, []
        else:
            return super(ArgMapArgParser, self).parse_known_args(
                args, namespace)
