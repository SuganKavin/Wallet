#!/usr/bin/env python3

from aws_cdk import core

from my_wallet.my_wallet_stack import MyWalletStack


app = core.App()
MyWalletStack(app, "my-wallet")

app.synth()
