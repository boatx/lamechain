# lamechain

Naive block chain implementation in Python.

## Inspired by
* [naivechain](https://github.com/lhartikk/naivechain)
* [Big-Ish Data blog post](https://bigishdata.com/2017/10/17/write-your-own-blockchain-part-1-creating-storing-syncing-displaying-mining-and-proving-work/)

## Usage

To create initial database in file `chain.db` with [genesesis block](https://en.bitcoin.it/wiki/Genesis_block) call:

```bash

python main.py init --file chain.db

```

To call operations on chain start local http server. To start server on address
`http://localhost:8888` call:

```bash

python main.py run --port 8888

```

To create new block:

```bash

curl --data 'data=Test' http://localhost:8888/blocks

```

## Endpoints

| Name      | Method | Parameters                        | Description                   |
|-----------|--------|-----------------------------------|-------------------------------|
| `/blocks` | `GET`  |                                   | List blocks in chain          |
| `/blocks` | `POST` | data -- data to use in blockchain | Mine new block with test data |

## Requirements
* python => 3.6

