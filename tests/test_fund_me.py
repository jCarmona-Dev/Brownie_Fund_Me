from web3 import Web3
from scripts.config_contract import get_account, LOCAL_BLOCKCHAIN_NETWORKS
from scripts.deploy import deploy_contract
from  brownie import network, accounts, exceptions
import pytest
def test_can_fund_and_withdraw():
    account = get_account()
    ContratoDeployed = deploy_contract()
    tx = ContratoDeployed.fund({'from':account,'value': Web3.to_wei(0.05,"ether")})
    tx.wait(1)
    assert ContratoDeployed.addressToAmountFunded(account.address) == Web3.to_wei(0.05,"ether")
    tx2 = ContratoDeployed.withdraw({"from":account}) 
    tx2.wait(1)
    assert ContratoDeployed.addressToAmountFunded(account.address) == 0
def test_only_owner_Can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_NETWORKS:
        pytest.skip("Solo pruebas locales")
    ContratoDeployed = deploy_contract()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        ContratoDeployed.withdraw({"from":bad_actor})