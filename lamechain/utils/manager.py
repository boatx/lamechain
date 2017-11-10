import argparse


class Manager:

    def __init__(self):
        self.main_parser = argparse.ArgumentParser()
        self.sub_parsers = self.main_parser.add_subparsers()
        self.parsers = {}

    def run_command(self):
        args = vars(self.parse_args())
        func = args.pop('func')
        func(**args)

    def parse_args(self):
        return self.main_parser.parse_args()

    def command(self, func):
        name = func.__name__
        sub_parser = self.sub_parsers.add_parser(
            name=name, description=func.__doc__)
        sub_parser.set_defaults(func=func)
        self.parsers[name] = sub_parser

        return func

    def option(self, *args, **kwargs):
        def option_decorator(func):
            name = func.__name__
            if name not in self.parsers:
                func = self.command(func)

            self.parsers[name].add_argument(*args, **kwargs)

            return func
        return option_decorator
