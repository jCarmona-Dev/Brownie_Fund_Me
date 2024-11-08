from brownie import FundMe, accounts
from scripts.config_contract import get_account
from web3 import  Web3
account = get_account() 

def fund():
    Contrato = FundMe[-2]  
    print(Contrato.getEntranceFee())
    print("Fondeando...")
    Contrato.fund({"from":account,"value":Web3.to_wei(0.02, "ether")})
def withdraw(Contrato):
    print("Retirando fondos...")
    Contrato.withdraw({'from':account})
def get_balance():
    Contrato = FundMe[-2]  
    print(Contrato.getBalance())
def main():
    for i in range(len(FundMe)):
        try:
            withdraw(FundMe[i])
        except Exception as e:
            print(e)
        