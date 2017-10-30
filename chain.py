import shelve

from block import Block


class Chain:

    DB_FILENAME = 'chain.db'

    def __init__(self):
        self._node_blocks = []

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
        with shelve.open(self.DB_FILENAME) as db:
            self._node_blocks = [Block(block) for block in db['blocks']]
        return self._node_blocks

    def add_block(self, block):
        self._node_blocks.append(block)
        with shelve.open(self.DB_FILENAME) as db:
            db['blocks'].append(dict(block))

    def mine_block(self):
        unmined_block = self.last_block.get_unmined_block()
        return unmined_block.mine()

    def validate_block(new_block, previous_block):
        return new_block.validate_block(previous_block)
