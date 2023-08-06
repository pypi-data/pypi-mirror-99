"""
Clean and simple command line interfaces.

    >>> main = application("Time", "tells time")
    >>> @main.register()
    ... class Main:
    ...     def setup(self, parser):
    ...         parser.add_argument("-t", "--tz", help="timezone e.g. PST")
    ...     def run(self, args, stdin):
    ...         print(args)
    ...         return 0
    >>> main()

"""

# TODO constrain help to TTY_WIDTH
# TODO show detailed people information (update `pkg` to include `git`)
#      TODO perform enhanced Git interrogation in `pkg` using `git`
# TODO show documentation link in printed help
# TODO set WEBHELP to automatically open help in WEBAGENT
# TODO set MAILHELP to automatically open personal request for help in
#      MAILAGENT automatically signs the e-mail and pays it forward with
#      a BTC that serves as initial compenstation as well as
#      receipt confirmation

import argparse
import inspect
import logging
import os
import sys

import argcomplete
from understory.pkg import listing


class Application:
    """A command-line application framework."""

    def __init__(self, name, description):
        self.name = name
        desc, _, epilog = description.partition("\n\n")
        version, people, license = self.get_metadata()
        epilog += ("-   width may be forced by setting `TTY_WIDTH`\n"
                   "-   colors may be forced by setting `COLORS_OFF` "
                   "or `COLORS_ON`\n\n"
                   "Released under the {} by:\n".format(license))
        for person, roles in sorted(people.items()):
            epilog += "  {}: ".format(person)
            epilog += ", ".join("<{}> ({})".format(address, role)
                                for role, address in sorted(roles.items()))
        parser = argparse.ArgumentParser(prog=name, description=desc,
                                         epilog=epilog, add_help=False,
                                         formatter_class=HelpFormatter)
        add_arg = parser.add_argument
        add_arg("--help", action="store_true",
                help="print this help message and exit")
        add_arg("--version", action="version", version=version,
                help="print version number and exit")
        add_arg("--color", action="store_true",
                default=bool(os.environ.get("COLORS_ON")),
                help="force color output to a suspected non-tty")
        add_arg("--page", action="store_true",
                default=bool(os.environ.get("PAGING_ON")),
                help="force color output to a suspected non-tty")
        add_arg("-m", "--machine", action="store_true",  # TODO move to `cli`
                help="machine listing for piping to grep, cut, etc.")
        self.parser = parser

    def get_metadata(self):
        """
        return a three-tuple of app's package's version, people and license

        """
        for dist_name in listing.get_distributions(dependencies=True):
            dist = listing.get_distribution(dist_name)
            if self.name in dist.details.get("entry-points",
                                             {}).get("console_scripts", []):
                break
        dist = dist.details
        return dist["version"], dist["people"], dist["license"]

    def register(self, alias=None):
        """
        register a [sub-]command

        Register a single class named `Main` for single-parser comand
        mode. Register any other class name(s) for multi-parser,
        sub-command mode.

        """
        # TODO investigate metaclass alternative
        def handler(cls):
            """
            prepare decorated class by providing a modified

            """
            name = cls.__name__.lower()
            desc = (inspect.getdoc(cls) or "").strip()
            if name == "main":
                parser = self.parser
            else:
                try:
                    self.subparsers
                    self.handlers
                except AttributeError:
                    self.subparsers = self.parser.add_subparsers(help="cmds")
                    self.handlers = {}
                sub_add = self.subparsers.add_parser
                epilog = "see also `{} --help`".format(self.name)
                aliases = [name[:1]]  # FIXME handle names w/ same first letter
                if alias:
                    aliases.append(alias)
                parser = sub_add(name, aliases=aliases, add_help=False,
                                 formatter_class=HelpFormatter, help=desc,
                                 epilog=epilog)
                parser.add_argument("--help", action="help",
                                    help="print this help message and exit")
                parser.set_defaults(_cmd=name)
            _cls = cls()

            def add_completed_argument(*args, **kwargs):
                """
                adds `completer` kwarg to proxied `add_argument()`

                """
                completer = kwargs.pop("completer", None)
                arg = parser._add_argument(*args, **kwargs)
                if completer:
                    arg.completer = completer
                return arg

            parser._add_argument = parser.add_argument
            parser.add_argument = add_completed_argument
            try:
                setup_handler = _cls.setup
            except AttributeError:
                pass
            else:
                setup_handler(parser.add_argument)
            if name == "main":
                self.root = _cls.run
            else:
                self.handlers[name] = _cls.run
            return cls

        return handler

    def __call__(self):
        """
        provide dynamic auto-complete and run command or print help

        Use of `__call__` to keep consistent with historical practice of
        calling a function named `main`. Instead, best practice is to name
        this global instance as such and call it as usual:

            main = Application()
            ...
            if __name__ == "__main__":
                main()

        """
        argcomplete.autocomplete(self.parser)
        args = self.parser.parse_args()
        try:
            handler = self.root
        except AttributeError:
            try:
                handler = self.handlers[getattr(args, "_cmd", "")]
            except KeyError:  # multi-command, none given (better way to trap?)
                self.parser.print_help()
                self.parser.exit(0)
        for arg, value in args.__dict__.items():
            setattr(handler.__self__, arg, value)
        log = logging.getLogger(self.name)
        log.setLevel(logging.INFO)
        log.addHandler(logging.StreamHandler(sys.stdout))
        try:
            status = handler(sys.stdin, log)
        except KeyboardInterrupt:
            status = 0
        self.parser.exit(status)


class HelpFormatter(argparse.HelpFormatter):

    """
    help message formatter which adds various details to argument help

    """

    def _fill_text(self, text, width, indent):
        """
        retain formatting of description & epilog

        """
        return "".join(indent + line for line in
                       text.splitlines(keepends=True))

    def _split_lines(self, text, width):
        """
        retain formatting of help text

        """
        return text.splitlines()

    def _format_action_invocation(self, action):
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            metavar, = self._metavar_formatter(action, default)(1)
            return metavar
        else:
            output = ", ".join(action.option_strings)
            if action.nargs != 0:
                # TODO move logic to self._format_args(..) for use in `usage`
                # default = self._get_default_metavar_for_optional(action)
                # output += " " + self._format_args(action, default)
                if isinstance(action.default, list):
                    default = "{0} [..]".format(action.metavar)
                else:
                    default = action.metavar
                output += " " + str(default)
            return output

    def _get_help_string(self, action):
        """
        support repeatability (`action="count"`) & default values

        """
        help = action.help
        if isinstance(action, argparse._CountAction):
            help += " (e.g. -{})".format(3 * action.dest[0])
        if action.default is not argparse.SUPPRESS:
            default_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
            if action.default and (action.option_strings or
                                   action.nargs in default_nargs):
                help_str = "%(default)s"
                if isinstance(action.default, (tuple, list, set)):
                    help_str = ", ".join(map(str, action.default))
                help += " {{{}}}".format(help_str)
        return help
