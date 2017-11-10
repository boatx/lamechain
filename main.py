import logging

from lamechain.chain import initialize_db
from lamechain.server import run_local_server
from lamechain.utils.manager import Manager

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

manager = Manager()


@manager.option('--port', type=int)
def run(port):
    """Run local chain server"""
    return run_local_server(port)


@manager.option('--file', dest='file_name', type=str)
def init(file_name):
    """Initialize db with genesis block"""
    return initialize_db(file_name)


if __name__ == "__main__":
    manager.run_command()
