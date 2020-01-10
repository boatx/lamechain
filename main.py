import logging

from command_manager import Manager

from lamechain.chain import initialize_db
from lamechain.p2p_client import run_p2p_client
from lamechain.server import run_local_server, Server

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

manager = Manager()


@manager.option("--p2p-port", type=int, dest="p2p_port")
@manager.option("--http-port", type=int, dest="http_port")
@manager.option("-P", "--peers", type=str, nargs="*")
@manager.option("-f", "--db-file", type=str, dest="db_file")
def fullrun(db_file, peers, p2p_port, http_port):
    return Server(chain_db_file=db_file, peers_addresses=peers).run(
        p2p_port=p2p_port, http_port=http_port
    )


@manager.option("-p", "--port", type=int)
def run(port):
    """Run local chain server"""
    return run_local_server(port)


@manager.option("-P", "--peers", type=str, nargs="*")
@manager.option("-p", "--port", type=int)
@manager.option("-H", "--host", type=str)
def runp2p(host, port, peers):
    """Run p2p client"""
    return run_p2p_client(host=host, port=port, peers=peers)


@manager.option("--file", dest="file_name", type=str)
def init(file_name):
    """Initialize db with genesis block"""
    return initialize_db(file_name)


if __name__ == "__main__":
    manager.run_command()
