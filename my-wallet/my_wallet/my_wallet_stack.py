from aws_cdk import core
from . import wallet_service


class MyWalletStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        wallet_service.WalletService(self, "Wallets")

