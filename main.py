import logging

from command_manager import Manager

from lamechain.chain import initialize_db
from lamechain.p2p_client import run_p2p_client
from lamechain.server import run_local_server

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

manager = Manager()


@manager.option('-p', '--port', type=int)
def run(port):
    """Run local chain server"""
    return run_local_server(port)


@manager.option('-P', '--peers', type=str, nargs='*')
@manager.option('-p', '--port', type=int)
@manager.option('-H', '--host', type=str)
def runp2p(host, port, peers):
    """Run p2p client"""
    return run_p2p_client(host=host, port=port, peers=peers)


@manager.option('--file', dest='file_name', type=str)
def init(file_name):
    """Initialize db with genesis block"""
    return initialize_db(file_name)


if __name__ == "__main__":
    manager.run_command()
