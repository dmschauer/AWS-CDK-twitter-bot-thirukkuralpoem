from constructs import Construct
from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    aws_events as events,
    aws_events_targets as events_targets,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    aws_logs as logs,
    custom_resources as cr,
    aws_iam as iam
)

from settings.twitter_settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, NUM_POEMS

class ThirukkuralpoemStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = ddb.Table(
            self, 'ThirukkuralPoems',
            table_name='ThirukkuralPoems',
            partition_key={'name': 'Number', 'type': ddb.AttributeType.NUMBER},
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )
        
        # create lambda function for loading json data into DynamoDB table
        lambda_load_ddb = _lambda.Function(
                            self,"LambdaLoadDDB",
                            runtime=_lambda.Runtime.PYTHON_3_9,
                            code=_lambda.Code.from_asset("lambdas/load_ddb"),
                            handler="load_ddb.handler",
                            function_name="thirukkuralpoem_load_ddb",
                            environment={
                                "DYNAMODB_TABLE_NAME":table.table_name
                            }                           
        )

        # create lambda function for sending daily Tweet
        lambda_send_tweet = _lambda.Function(
                            self,"LambdaSendTweet",
                            runtime=_lambda.Runtime.PYTHON_3_9,
                            code=_lambda.Code.from_asset("lambdas/send_tweet"),
                            handler="send_tweet.handler",
                            function_name="thirukkuralpoem_send_tweet",
                            environment={
                                "DYNAMODB_TABLE_NAME":table.table_name,
                                "CONSUMER_KEY":CONSUMER_KEY,
                                "CONSUMER_SECRET":CONSUMER_SECRET,
                                "ACCESS_TOKEN":ACCESS_TOKEN,
                                "ACCESS_TOKEN_SECRET":ACCESS_TOKEN_SECRET,
                                "NUM_POEMS":NUM_POEMS
                            }                     
        )

        # https://medium.com/geekculture/deploying-aws-lambda-layers-with-python-8b15e24bdad2
        # pip install tweepy boto3 --target ./lambda_layer/python/lib/python3.9/site-packages --no-user
        lambda_send_tweet_layer = _lambda.LayerVersion(self, 'LambdaSendTweetLayer',
                  code = _lambda.AssetCode('lambda_layer/'),
                  compatible_runtimes = [_lambda.Runtime.PYTHON_3_9],
        )   

        lambda_send_tweet.add_layers(
            _lambda.LayerVersion.from_layer_version_arn(
                self, 'SendTweet',
                layer_version_arn=lambda_send_tweet_layer.layer_version_arn)
        )

        table.grant_write_data(lambda_load_ddb)
        table.grant_read_data(lambda_send_tweet)

        # fill DynamoDB table exactly once
        # invokes Lambda after On Create event
        lambda_trigger = cr.AwsCustomResource(
            self, "LambdaTrigger",
            on_create=cr.AwsSdkCall(
                action="invoke",
                service="Lambda",
                parameters={
                    "FunctionName": lambda_load_ddb.function_name,
                    "InvocationType": 'Event'
                },
                physical_resource_id=cr.PhysicalResourceId.of(table.table_name + "_initialization"),
            ),
            policy=cr.AwsCustomResourcePolicy.from_statements([iam.PolicyStatement(
                actions=['lambda:InvokeFunction'],
                effect=iam.Effect.ALLOW,
                resources=[lambda_load_ddb.function_arn]
            )]),
            log_retention=logs.RetentionDays.ONE_DAY,
            timeout=Duration.minutes(2),
        )

        # schedule execution to once a day (at 8:00 AM)
        rule_daily = events.Rule(
            self, "DailyUTC8AM",
            # schedule=aws_events.Schedule.rate(Duration.days(1)),
            schedule=events.Schedule.cron(hour="8", minute="0")
        )
        rule_daily.add_target(events_targets.LambdaFunction(lambda_send_tweet))