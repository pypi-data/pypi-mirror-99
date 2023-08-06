import os

import pytest
import requests
from eth_account.signers.local import LocalAccount
from web3 import Web3
from web3.contract import Contract

from ..contracts import get_example_erc20_contract


def just_test_if_mainnet_node() -> str:
    mainnet_node_url = os.environ.get('ETHEREUM_MAINNET_NODE')
    if not mainnet_node_url:
        pytest.skip("Mainnet node not defined, cannot test oracles", allow_module_level=True)
    elif requests.get(mainnet_node_url).status_code == 404:
        pytest.skip("Cannot connect to mainnet node", allow_module_level=True)
    return mainnet_node_url


def send_tx(w3: Web3, tx, account: LocalAccount) -> bytes:
    tx['from'] = account.address
    if 'nonce' not in tx:
        tx['nonce'] = w3.eth.get_transaction_count(account.address, block_identifier='pending')

    if 'gasPrice' not in tx:
        tx['gasPrice'] = w3.eth.gas_price

    if 'gas' not in tx:
        tx['gas'] = w3.eth.estimateGas(tx)
    else:
        tx['gas'] *= 2

    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(bytes(signed_tx.rawTransaction))
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    assert tx_receipt.status == 1, 'Error with tx %s - %s' % (tx_hash.hex(), tx)
    return tx_hash


def deploy_example_erc20(w3: Web3, amount: int, owner: str, deployer: str = None,
                         account: LocalAccount = None) -> Contract:
    return deploy_erc20(w3, 'Uxio', 'UXI', owner, amount, deployer=deployer, account=account)


def deploy_erc20(w3: Web3, name: str, symbol: str, owner: str, amount: int, decimals: int = 18, deployer: str = None,
                 account: LocalAccount = None) -> Contract:
    if account:
        erc20_contract = get_example_erc20_contract(w3)
        tx = erc20_contract.constructor(name, symbol, decimals, owner, amount).buildTransaction({
            'nonce': w3.eth.get_transaction_count(account.address, block_identifier='pending')
        })
        signed_tx = account.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    else:
        deployer = deployer or w3.eth.accounts[0]
        erc20_contract = get_example_erc20_contract(w3)
        tx_hash = erc20_contract.constructor(name, symbol, decimals, owner, amount).transact({'from': deployer})

    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    erc20_address = tx_receipt.contractAddress
    deployed_erc20 = get_example_erc20_contract(w3, erc20_address)
    assert deployed_erc20.functions.balanceOf(owner).call() == amount
    return deployed_erc20
