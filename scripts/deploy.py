# brownie run scripts/deploy.py --network kovan
# brownie run scripts/deploy.py --network ganache-local

# FORK MAINNET =
# brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork='https://infura.io/v3/$WEB3_INFURA_PROJECT_ID' accounts=10 mnemonic=brownie port=8545
# but : not work well with infura => use alchemy
# brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork='https://eth-mainnet.alchemyapi.io/v2/k7miQWvsZw4mUHuLoZ0dL9mSLFL1hW6c' accounts=10 mnemonic=brownie port=8545
#

from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    # if network.show_active() != "development":
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to : {fund_me.address}")
    return fund_me
    # pass


def main():
    deploy_fund_me()
