import argparse


class Manager:
    """Helper class to simplify creating parsers for sub commands"""

    def __init__(self):
        self.main_parser = argparse.ArgumentParser()
        self.sub_parsers = self.main_parser.add_subparsers()
        self.parsers = {}

    def run_command(self):
        """Parse arguments and run registered command"""
        args = vars(self.parse_args())
        func = args.pop('func')
        func(**args)

    def parse_args(self):
        """Parser arguments"""
        return self.main_parser.parse_args()

    def command(self, func):
        """Register function as sub command"""

        """
        Use function name as name of command and docstring as description.
        Create sub parser for new command.

        :param func: python function
        :returns: Input function.
        """
        name = func.__name__
        sub_parser = self.sub_parsers.add_parser(
            name=name, description=func.__doc__)
        sub_parser.set_defaults(func=func)
        self.parsers[name] = sub_parser

        return func

    def option(self, *args, **kwargs):
        """Register function as sub command with input arguments"""

        """
        If parser with function name don't exisits in parsers dict
        new sub parser will be created.

        :param func: python function
        :returns: Input function.
        """
        def option_decorator(func):
            name = func.__name__
            if name not in self.parsers:
                func = self.command(func)

            self.parsers[name].add_argument(*args, **kwargs)

            return func
        return option_decorator
