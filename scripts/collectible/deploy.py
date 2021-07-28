#!/usr/bin/python3
from brownie import AdvancedCollectible, config, interface, network
from scripts.helpful_scripts import get_account, get_contract
from web3 import Web3

BACKUP_FUND_AMOUNT = Web3.toWei(1, "ether")


def main():
    account = get_account()
    print(network.show_active())
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        account.address,
        BACKUP_FUND_AMOUNT,
        {"from": account},
        publish_source=False,
    )
    # tx = fund_with_link(advanced_collectible.address)
    # tx.wait(1)
    tx = interface.LinkTokenInterface(get_contract("link_token").address).approve(
        advanced_collectible.address, BACKUP_FUND_AMOUNT * 1000, {"from": account}
    )
    tx.wait(1)
    return advanced_collectible
