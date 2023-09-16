from sqladmin import ModelView

from src.wallets.models import Wallet, Blockchain, Asset, Transaction


class WalletAdmin(ModelView, model=Wallet):
    name = "Wallet"
    name_plural = "Wallets"
    icon = "fa-solid fa-wallet"
    column_list = [Wallet.id, Wallet.address, Wallet.user_id, Wallet.asset_id]
    column_details_exclude_list = [Wallet.private_key]
    can_export = False


class BlockchainAdmin(ModelView, model=Blockchain):
    name = 'Blockchain'
    name_plural = 'Blockchains'
    icon = 'fa fa-usd'
    column_list = [Blockchain.id, Blockchain.name, Blockchain.short_name, Blockchain.image]
    can_export = False

class AssetAdmin(ModelView, model=Asset):
    name = 'Asset'
    name_plural = 'Assets'
    icon = 'fa fa-file-text'
    column_list = [Asset.id, Asset.name, Asset.decimal_places, Asset.blockchain_id]
    column_details_exclude_list = [Asset.wallets]
    can_export = False

class TransactionAdmin(ModelView, model=Transaction):
    name = 'Transaction'
    name_plural = 'Transactions'
    icon = 'fa fa-list-alt'
    column_list = [Transaction.id, Transaction.hash, Transaction.from_send, Transaction.to_send, Transaction.value, Transaction.txn_fee, Transaction.status]
    can_export = False