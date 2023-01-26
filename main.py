from ton.sync import TonlibClient
from ton.account import Account

address = 'EQCpKU1FZRK7qTsLMNMzuLOrBc-M5-YEXfIHsQ0BsxZSXlRL'

client = TonlibClient()
TonlibClient.enable_unaudited_binaries()
client.init_tonlib()

key = None

account = client.find_account('EQCEXDQWeqjLP4BehKzzwbuRBsxQHVwEa9j4MGunBs1Vkg_w')
account.get_balance()
print(account.get_balance())
print(account.get_nft_data())
print(account.detect_type())

word_list = '...'

wallet = client.import_wallet(word_list, source='v3r2', workchain_id=0, wallet_id=0)
print(wallet.address)

account_to_send = 'UQDMReg6wG5YLrtIQ1JKEBbcwEaP8M91_BLWtLVeP7AV2iJb'

# Transfer 0.1 nft
wallet.transfer(account_to_send, client.to_nano(0.1), comment='test')

# word_list = 'drift release sudden crew swear together garden verify amount ' \
#             'master smoke daughter field faint kingdom arrange refuse ' \
#             'slender require chalk rocket number often wedding'
#
# wallet = client.import_wallet(word_list, source='v3r2', workchain_id=0, wallet_id=0, local_password=None)
# print('Wallet address:', wallet.address)
# print('Seed:', wallet.export())
#
#
# async def fetch_text():
#     account = await client.find_account('EQCEXDQWeqjLP4BehKzzwbuRBsxQHVwEa9j4MGunBs1Vkg_w')
#     body = account.create_transfer_nft_body('EQCl1Ug9ZT9ZfGyFH9l4q-bqaUy6kyOzVPmrk7bivmVKJRRZ')
#     wallet.transfer(account.address, client.to_nano(0.05), data=body.serialize_boc())
