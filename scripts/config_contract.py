from brownie import network, accounts, MockV3Aggregator, config
from web3 import Web3

DECIMALS = 8

STARTING_PRICE = 2000

LOCAL_BLOCKCHAIN_NETWORKS = ["development","Ganache-local"]
FORKED_LOCAL_ENVIROMENTS = ['mainnet-fork-dev']

def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_NETWORKS or network.show_active() in FORKED_LOCAL_ENVIROMENTS:
        return  accounts[0]
    else: 
        return accounts.load("PasanteAccount") 
    
def deploy_mock():
    
        if(len(MockV3Aggregator)==0):
            print("Red de Ganache, se va a desplegar los Mocks")
            Mock_Aggregator = MockV3Aggregator.deploy(DECIMALS, Web3.to_wei(STARTING_PRICE, "ether"), {"from":get_account()})
        else:
            Mock_Aggregator = MockV3Aggregator[-1]
        return Mock_Aggregator.address