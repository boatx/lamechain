import logging
import shelve

from lamechain.block import Block, create_genesis_block

log = logging.getLogger(__name__)

DB_FILENAME = "chain.db"


class Chain:
    def __init__(self, chain_db=DB_FILENAME):
        self._node_blocks = []
        self.chain_db = chain_db

    @property
    def last_block(self):
        if not self._node_blocks:
            self.sync()
        return self.node_blocks[-1]

    @property
    def node_blocks(self):
        if not self._node_blocks:
            return self.sync()
        return self._node_blocks

    def sync(self):
        """Sync block chain
        :returns: list of blocks

        """
        with shelve.open(self.chain_db) as db:
            self._node_blocks = [Block(block) for block in db["blocks"]]
        return self._node_blocks

    def dump(self):
        return [dict(block) for block in self._node_blocks]

    def add_block(self, block):
        self._node_blocks.append(block)
        with shelve.open(self.chain_db) as db:
            db["blocks"] = self.dump()

    def mine_block(self, data):
        unmined_block = self.last_block.get_unmined_block(data)
        return unmined_block.mine()

    def validate_block(new_block, previous_block):
        return new_block.validate_block(previous_block)


def initialize_db(file_name=DB_FILENAME):
    genesis_block = create_genesis_block()
    with shelve.open(file_name) as db:
        db["blocks"] = [dict(genesis_block)]
    log.info("Database file: {} has been created".format(file_name))
