from aws_cdk import (core,
                     aws_apigateway as apigateway,
                     aws_dynamodb as dynamodb,
                     aws_lambda as lambda_)


class WalletService(core.Construct):
    def __init__(self, scope: core.Construct, id: str):
        super().__init__(scope, id)


            # create dynamo table
        wallet_table = dynamodb.Table(self,"WalletDetail",  table_name="WalletDetail", partition_key=dynamodb.Attribute(
            name="id",
            type=dynamodb.AttributeType.STRING
        ))

        transaction_table = dynamodb.Table(self,"TransactionDetail",table_name="TransactionDetail", partition_key=dynamodb.Attribute(
            name="id",
            type=dynamodb.AttributeType.STRING
        ))

        create_wallet_handler = lambda_.Function(self, "WalletCreateHandler",
                                              function_name="WalletCreate",
                                              runtime=lambda_.Runtime.PYTHON_3_7,
                                              code=lambda_.Code.asset("resources"),
                                              handler="createWallet.handler",
                                              environment=dict(
                                                  WALLET_TABLE=wallet_table.table_name)
                                              )

        wallet_table.grant_read_write_data(create_wallet_handler)

        create_trx_handler = lambda_.Function(self, "TrxCreateHandler",
                                                 function_name="TransactionCreate",
                                                 runtime=lambda_.Runtime.PYTHON_3_7,
                                                 code=lambda_.Code.asset("resources"),
                                                 handler="create.handler",
                                                 environment=dict(
                                                     WALLET_TABLE=wallet_table.table_name,
                                                     TRANSACTION_TABLE= transaction_table.table_name)
                                                 )

        transaction_table.grant_read_write_data(create_trx_handler)
        wallet_table.grant_read_write_data(create_trx_handler)

        get_handler = lambda_.Function(self, "WalletGetHandler",
                                           function_name="WalletGet",
                                           runtime=lambda_.Runtime.PYTHON_3_7,
                                           code=lambda_.Code.asset("resources"),
                                           handler="get.handler",
                                           environment=dict(
                                               WALLET_TABLE=wallet_table.table_name)
                                           )

        wallet_table.grant_read_data(get_handler)

        put_handler = lambda_.Function(self, "WalletUpdateHandler",
                                           function_name="WalletUpdate",
                                           runtime=lambda_.Runtime.PYTHON_3_7,
                                           code=lambda_.Code.asset("resources"),
                                           handler="update.handler",
                                           environment=dict(
                                               WALLET_TABLE=wallet_table.table_name)
                                           )

        wallet_table.grant_write_data(put_handler)

        delete_handler = lambda_.Function(self, "WalletDeleteHandler",
                                              function_name="WalletDelete",
                                              runtime=lambda_.Runtime.PYTHON_3_7,
                                              code=lambda_.Code.asset("resources"),
                                              handler="delete.handler",
                                              environment=dict(
                                                  WALLET_TABLE=wallet_table.table_name)
                                              )

        wallet_table.grant_write_data(delete_handler)


        api = apigateway.RestApi(self, "Wallet-api",
                                     rest_api_name="Wallet Service",
                                     description="This service serves Wallets.")

        '''post_integration = apigateway.LambdaIntegration(create_wallet_handler,
                                                                   request_templates={
                                                                       "application/json": '{ "statusCode": "200" }'})'''
        post_integration = apigateway.LambdaIntegration(create_trx_handler,
                                                        request_templates={
                                                            "application/json": '{ "statusCode": "200" }'})

        get_integration = apigateway.LambdaIntegration(get_handler,
                                                                  request_templates={
                                                                      "application/json": '{ "statusCode": "200" }'})

        put_integration = apigateway.LambdaIntegration(put_handler,
                                                                  request_templates={
                                                                      "application/json": '{ "statusCode": "200" }'})

        delete_integration = apigateway.LambdaIntegration(delete_handler,
                                                                     request_templates={
                                                                         "application/json": '{ "statusCode": "200" }'})


        api.root.add_method("POST", post_integration)  # POST /

        resource = api.root.add_resource("{id}")

        resource.add_method("PUT", put_integration)  # PUT /{id}

        resource.add_method("GET", get_integration)  # GET /{id}

        resource.add_method("DELETE", delete_integration)  # DELETE /{id}