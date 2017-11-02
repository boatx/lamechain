import argparse
import logging
import sys

from lamechain.chain import initialize_db
from lamechain.server import run_local_server


log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

actions = {
    'run': run_local_server,
    'initialize': initialize_db
}


def get_arguments():
    valid_actions = list(actions.keys())
    parser = argparse.ArgumentParser()
    parser.add_argument('action', nargs=1, choices=valid_actions)
    return parser.parse_args()


def main():
    args = get_arguments()
    try:
        return actions[args.action[0]]()
    except KeyError:
        log.error('Invalid action {}'.format(args.action))
        sys.exit(1)


if __name__ == "__main__":
    main()
