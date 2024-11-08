from brownie import FundMe, network, config
from scripts.config_contract import get_account, deploy_mock, LOCAL_BLOCKCHAIN_NETWORKS

def deploy_contract():

    account = get_account()#Obtiene una cuenta a partir del network activo 

    #Inicializar los mocks o dar address de Data Feeds
    if(network.show_active() not in LOCAL_BLOCKCHAIN_NETWORKS):
        priceFeed = config["networks"][network.show_active()]["ETH_USD_DATA_FEED"]
    else:
        priceFeed = deploy_mock()
    
    #Se despliega un nuevo contrato si es necesario
    if( network.show_active() in LOCAL_BLOCKCHAIN_NETWORKS or len(FundMe)==0):
        ContratoDeployed = FundMe.deploy(priceFeed,{"from":account},publish_source=config['networks'][network.show_active()].get("verify"))
        print(f"No había un contrato previo desplegado entonces se desplegó uno en: {ContratoDeployed.address}")
    else:
            ContratoDeployed = FundMe.deploy(priceFeed,{"from":account},publish_source=config['networks'][network.show_active()].get("verify"))
            print("Desplegado con éxito")

    return ContratoDeployed

    
def main():
    deploy_contract()