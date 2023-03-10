from ton.sync import TonlibClient
import asyncio

address = 'EQCpKU1FZRK7qTsLMNMzuLOrBc-M5-YEXfIHsQ0BsxZSXlRL'

client = TonlibClient()
TonlibClient.enable_unaudited_binaries()
client.init_tonlib()

account = client.find_account('EQCEXDQWeqjLP4BehKzzwbuRBsxQHVwEa9j4MGunBs1Vkg_w')
account.get_balance()
print(account.get_balance())
print(account.get_nft_data())
print(account.detect_type())

word_list = '///'

wallet = client.import_wallet(word_list, source='v3r2', workchain_id=0, wallet_id=0)
print(wallet.address)

# Test account 2
account_to_send = 'UQDMReg6wG5YLrtIQ1JKEBbcwEaP8M91_BLWtLVeP7AV2iJb'

# Transfer 0.1 nft

# wallet.transfer(account_to_send, client.to_nano(0.1), comment='test')


async def send_nft_async(account_to_transfer):
    print(account_to_transfer)
    await wallet.transfer(account_to_transfer, client.to_nano(0.01), comment='test')
    print('Success')
