import pytest
from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import (
    get_account,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from scripts.collectible.deploy import BACKUP_FUND_AMOUNT


def test_can_create_advanced_collectible(
    get_keyhash, chainlink_fee,
):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    backup_wallet = get_account(index=2)
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        get_keyhash,
        chainlink_fee,
        backup_wallet.address,
        BACKUP_FUND_AMOUNT,
        {"from": account},
    )
    get_contract("link_token").transfer(
        advanced_collectible.address, chainlink_fee * 3, {"from": account}
    )
    # Act
    transaction_receipt = advanced_collectible.createCollectible(
        "None", {"from": get_account()}
    )
    requestId = transaction_receipt.events["requestedCollectible"]["requestId"]
    assert isinstance(transaction_receipt.txid, str)
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, 777, advanced_collectible.address, {"from": get_account()}
    )
    # Assert
    assert advanced_collectible.tokenCounter() > 0
    assert isinstance(advanced_collectible.tokenCounter(), int)


def test_check_upkeep_returns_true(
    get_keyhash, chainlink_fee,
):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    backup_wallet = get_account(index=2)
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        get_keyhash,
        chainlink_fee,
        account.address,
        BACKUP_FUND_AMOUNT,
        {"from": account},
    )
    # Act / Assert
    upkeepNeeded, _ = advanced_collectible.checkUpkeep.call("")
    assert upkeepNeeded is True
    return advanced_collectible, account, backup_wallet


def test_can_top_up(
    get_keyhash, chainlink_fee,
):
    # Arrange
    advanced_collectible, account, backup_wallet = test_check_upkeep_returns_true(
        get_keyhash, chainlink_fee,
    )
    keeper_node = get_account(index=1)
    tx = get_contract("link_token").approve(
        advanced_collectible.address, BACKUP_FUND_AMOUNT, {"from": account}
    )
    # Act
    starting_balance = get_contract("link_token").balanceOf(
        advanced_collectible.address
    )
    tx = advanced_collectible.performUpkeep("", {"from": keeper_node})
    tx.wait(1)
    # Assert
    assert (
        get_contract("link_token").balanceOf(advanced_collectible.address)
        == starting_balance + BACKUP_FUND_AMOUNT
    )
