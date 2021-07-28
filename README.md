# top-up-nft

This demo shows how to use Chainlink Keepers to automate funding an NFT contract so random collectibles can be created in a decentralized manner.

## Prerequisites

Please install or have installed the following:

- [nodejs and npm](https://nodejs.org/en/download/)
- [python](https://www.python.org/downloads/)
## Installation

1. [Install Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html), if you haven't already. Here is a simple way to install brownie.


```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
# restart your terminal
pipx install eth-brownie
```
Or, if that doesn't work, via pip
```bash
pip install eth-brownie
```

2. Download the mix and install dependancies.

```bash
brownie bake chainlink-mix
cd chainlink-mix
pip install -r requirements.txt
```

This will open up a new Chainlink project. Or, you can clone from source:

```bash
git clone https://github.com/PatrickAlphaC/top-up-nft
cd top-up-nft
```

## Testnet Development
If you want to be able to deploy to testnets, do the following.

Set your `WEB3_INFURA_PROJECT_ID`, and `PRIVATE_KEY` [environment variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html).

You can get a `WEB3_INFURA_PROJECT_ID` by getting a free trial of [Infura](https://infura.io/). At the moment, it does need to be infura with brownie. If you get lost, you can [follow this guide](https://ethereumico.io/knowledge-base/infura-api-key-guide/) to getting a project key. You can find your `PRIVATE_KEY` from your ethereum wallet like [metamask](https://metamask.io/).

You'll also need testnet ETH and LINK. You can get LINK and ETH into your wallet by using the [faucets located here](https://docs.chain.link/docs/link-token-contracts). If you're new to this, [watch this video.](https://www.youtube.com/watch?v=P7FX_1PePX0). Look at the `rinkeby` and `kovan` sections for those specific testnet faucets. 

You can add your environment variables to a `.env` file. You can use the [.env.exmple](https://github.com/smartcontractkit/chainlink-mix/blob/master/.env.example) as a template, just fill in the values and rename it to '.env'. Then, uncomment the line `# dotenv: .env` in `brownie-config.yaml`

Here is what your `.env` should look like:
```
export WEB3_INFURA_PROJECT_ID=<PROJECT_ID>
export PRIVATE_KEY=<PRIVATE_KEY>
```

AND THEN RUN `source .env` TO ACTIVATE THE ENV VARIABLES
(You'll need to do this everytime you open a new terminal, or [learn how to set them easier](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html))


![WARNING](https://via.placeholder.com/15/f03c15/000000?text=+) **WARNING** ![WARNING](https://via.placeholder.com/15/f03c15/000000?text=+)

DO NOT SEND YOUR PRIVATE KEY WITH FUNDS IN IT ONTO GITHUB

Otherwise, you can build, test, and deploy on your local environment.

### Registering with Keepers

You'll need to register your contract with the Chainlink keeper network in order for this to function correctly on the keeper network. 

Please see the [Chainlink Keeper documentation](https://docs.chain.link/docs/chainlink-keepers/introduction/) on how to do this. 

## Local Development

For local testing [install ganache-cli](https://www.npmjs.com/package/ganache-cli)
```bash
npm install -g ganache-cli
```
or
```bash
yarn add global ganache-cli
```

## Running Scripts and Deployment

```bash
brownie run scripts/collectible/deploy.py --network kovan
```
Then, after registering with the keeper network, you'll automatically add LINK token to your contract. Then you can create collectibles with:
```
brownie run scripts/collectible/create_collectible.py
```


### Local Development

For local development, you might want to deploy mocks. You can run the script to deploy mocks. Depending on your setup, it might make sense to *not* deploy mocks if you're looking to fork a mainnet. It all depends on what you're looking to do though. Right now, the scripts automatically deploy a mock so they can run.

## Testing

```
brownie test
```

For more information on effective testing with Chainlink, check out [Testing Smart Contracts](https://blog.chain.link/testing-chainlink-smart-contracts/)

Tests are really robust here! They work for local development and testnets. There are a few key differences between the testnets and the local networks. We utilize mocks so we can work with fake oracles on our testnets.


### To test development / local
```bash
brownie test
```

## Linting

```
pip install black
pip install autoflake
autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r .
black .
```

## Resources

To get started with Brownie:

* [Chainlink Documentation](https://docs.chain.link/docs)
* Check out the [Chainlink documentation](https://docs.chain.link/docs) to get started from any level of smart contract engineering.
* Check out the other [Brownie mixes](https://github.com/brownie-mix/) that can be used as a starting point for your own contracts. They also provide example code to help you get started.
* ["Getting Started with Brownie"](https://medium.com/@iamdefinitelyahuman/getting-started-with-brownie-part-1-9b2181f4cb99) is a good tutorial to help you familiarize yourself with Brownie.
* For more in-depth information, read the [Brownie documentation](https://eth-brownie.readthedocs.io/en/stable/).


Any questions? Join our [Discord](https://discord.gg/2YHSAey)

## License

This project is licensed under the [MIT license](LICENSE).
