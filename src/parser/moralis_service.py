# import asyncio
# from datetime import datetime, timedelta
# from moralis.evm_api import evm_api
#
# from config_fastapi import settings
#
#
# class MoralisService:
#     def __init__(self, api_key: str):
#         self.api_key = api_key
#
#     async def decode_txn_moralis(self, data: dict, address: str):
#         transactions = [
#             {
#                 "txn_hash": txn.get("hash") if isinstance(txn.get("hash"), str) else txn.get("hash").hex(),
#                 "from_send": address if txn.get("from_address") == address.lower() else txn.get("from_address"),
#                 "to_send": address if txn.get("to_address") == address.lower() else txn.get("to_address"),
#                 "value": int(txn.get("value")) / (int("1" + ("0" * 18))),
#                 "date_send": txn.get("block_timestamp"),
#                 "txn_fee": int(txn.get("gas_price")) / (int("1" + ("0" * 18))) * int(txn.get("receipt_gas_used")),
#                 "status": True
#                 if txn.get("receipt_status") == "1" or txn.get("receipt_status") is None
#                 else False
#             } for txn in data.get("result")
#         ]
#         return transactions
#
#     async def get_all_transactions(self, address: str):
#         params = {
#             "address": address,
#             "chain": "sepolia",
#             "subdomain": "",
#             "from_date": datetime.now() - timedelta(days=60),
#             "to_date": datetime.now(),
#             "cursor": "",
#             "limit": 100,
#         }
#
#         result = evm_api.transaction.get_wallet_transactions(api_key=self.api_key,
#                                                                   params=params, # noqa
#                                                                   )
#         return await self.decode_txn_moralis(result, address)
#
#
