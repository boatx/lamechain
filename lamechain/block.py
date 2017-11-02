import hashlib
import time
from collections import UserDict


class _BaseBlock(UserDict):
    def __getattr__(self, item):
        try:
            return super().__getattr__(item)
        except AttributeError:
            try:
                return self.data[item]
            except KeyError:
                raise AttributeError()

    def __dir__(self):
        return super().__dir__() + [item for item in self.data.keys()]


class BaseBlock(_BaseBlock):

    NUM_ZEROS = 4
    HASH_START = NUM_ZEROS * '0'

    @property
    def header(self):
        return str(self.index) + str(self.prev_hash) + str(self.block_data) + \
            str(self.timestamp) + str(self.nonce)

    def validate_hash(self):
        return str(self.hash[0:self.NUM_ZEROS]) == self.HASH_START

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(self.header.encode())
        return sha.hexdigest()


class Block(BaseBlock):

    def validate_block(self, previous_block):
        if previous_block.index != self.index - 1:
            return False
        if previous_block.hash != self.previous_hash:
            return False

        return self.validate_hash() and self.calculate_hash() == self.hash

    def get_unmined_block(self, block_data):
        index = int(self.index) + 1
        return UnminedBlock(
            index=index, timestamp=time.time(), prev_hash=self.hash,
            block_data=block_data, hash=None, nonce=0)

    def __str__(self):
        return 'Block<prev_hash: {}, hash: {}>'.format(
            self.prev_hash, self.hash)


class UnminedBlock(BaseBlock):

    def mine(self):
        self['hash'] = self.calculate_hash()
        while not self.validate_hash():
            self['nonce'] += 1
            self['hash'] = self.calculate_hash()
        return Block(**self)

    def __str__(self):
        return 'UnminedBlock<prev_hash: {}>'.format(self.prev_hash)


def create_genesis_block():
    pre_block = Block(index=-1, hash='')
    return pre_block.get_unmined_block(block_data='genesis block').mine_block()
