from web3 import Web3

from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}")

RPC = 'https://base-rpc.publicnode.com'

CONTRACT = '0x0000000002ba96c69b95e32caab8fc38bab8b3f8'
ABI = '[{"inputs": [{"internalType": "address","name": "account","type": "address"}],"name": "allocations","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"}]'

class Checker():
    def __init__(self) -> None:
        self.web3 = Web3(Web3.HTTPProvider(RPC))
        self.contract = self.web3.eth.contract(self.web3.to_checksum_address(CONTRACT), abi=ABI)
        self.decimals = 18
        
        self.total_allocation = 0
        self.total_accounts = 0
        self.total_eligible = 0
        
    def check_allocation(self, wallets):
        self.total_accounts = len(wallets)
        
        for wallet in wallets:
            allocation = self.contract.functions.allocations(self.web3.to_checksum_address(wallet)).call()
            
            result = round(allocation / 10 ** self.decimals, 2)
            
            if result > 0:
                self.total_eligible += 1
                self.total_allocation += result
                logger.success(f'{wallet}: {result} $ZORA')
            else:
                logger.error(f'{wallet}: {result} $ZORA')

if __name__ == '__main__':
    with open('wallets.txt', 'r') as file:
        data = file.read().splitlines()
    
    checker = Checker()
    checker.check_allocation(data)
    
    logger.info(f'Total $ZORA: {round(checker.total_allocation, 2)}')
    logger.info(f'Total eligible wallets: {checker.total_eligible}/{checker.total_accounts}')