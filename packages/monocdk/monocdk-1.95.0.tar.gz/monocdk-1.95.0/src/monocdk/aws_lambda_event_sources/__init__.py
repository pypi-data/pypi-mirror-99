'''
# AWS Lambda Event Sources

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

An event source mapping is an AWS Lambda resource that reads from an event source and invokes a Lambda function.
You can use event source mappings to process items from a stream or queue in services that don't invoke Lambda
functions directly. Lambda provides event source mappings for the following services. Read more about lambda
event sources [here](https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html).

This module includes classes that allow using various AWS services as event
sources for AWS Lambda via the high-level `lambda.addEventSource(source)` API.

NOTE: In most cases, it is also possible to use the resource APIs to invoke an
AWS Lambda function. This library provides a uniform API for all Lambda event
sources regardless of the underlying mechanism they use.

The following code sets up a lambda function with an SQS queue event source -

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
fn = lambda_.Function(self, "MyFunction")

queue = sqs.Queue(self, "MyQueue")
event_source = fn.add_event_source(SqsEventSource(queue))

event_source_id = event_source.event_source_id
```

The `eventSourceId` property contains the event source id. This will be a
[token](https://docs.aws.amazon.com/cdk/latest/guide/tokens.html) that will resolve to the final value at the time of
deployment.

## SQS

Amazon Simple Queue Service (Amazon SQS) allows you to build asynchronous
workflows. For more information about Amazon SQS, see Amazon Simple Queue
Service. You can configure AWS Lambda to poll for these messages as they arrive
and then pass the event to a Lambda function invocation. To view a sample event,
see [Amazon SQS Event](https://docs.aws.amazon.com/lambda/latest/dg/eventsources.html#eventsources-sqs).

To set up Amazon Simple Queue Service as an event source for AWS Lambda, you
first create or update an Amazon SQS queue and select custom values for the
queue parameters. The following parameters will impact Amazon SQS's polling
behavior:

* **visibilityTimeout**: May impact the period between retries.
* **receiveMessageWaitTime**: Will determine [long
  poll](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-long-polling.html)
  duration. The default value is 20 seconds.
* **enabled**: If the SQS event source mapping should be enabled. The default is true.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_sqs as sqs
from aws_cdk.aws_lambda_event_sources import SqsEventSource
from aws_cdk.core import Duration

queue = sqs.Queue(self, "MyQueue",
    visibility_timeout=Duration.seconds(30), # default,
    receive_message_wait_time=Duration.seconds(20)
)

lambda_.add_event_source(SqsEventSource(queue,
    batch_size=10
))
```

## S3

You can write Lambda functions to process S3 bucket events, such as the
object-created or object-deleted events. For example, when a user uploads a
photo to a bucket, you might want Amazon S3 to invoke your Lambda function so
that it reads the image and creates a thumbnail for the photo.

You can use the bucket notification configuration feature in Amazon S3 to
configure the event source mapping, identifying the bucket events that you want
Amazon S3 to publish and which Lambda function to invoke.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_s3 as s3
from aws_cdk.aws_lambda_event_sources import S3EventSource

bucket = s3.Bucket(...)

lambda_.add_event_source(S3EventSource(bucket,
    events=[s3.EventType.OBJECT_CREATED, s3.EventType.OBJECT_REMOVED],
    filters=[NotificationKeyFilter(prefix="subdir/")]
))
```

## SNS

You can write Lambda functions to process Amazon Simple Notification Service
notifications. When a message is published to an Amazon SNS topic, the service
can invoke your Lambda function by passing the message payload as a parameter.
Your Lambda function code can then process the event, for example publish the
message to other Amazon SNS topics, or send the message to other AWS services.

This also enables you to trigger a Lambda function in response to Amazon
CloudWatch alarms and other AWS services that use Amazon SNS.

For an example event, see [Appendix: Message and JSON
Formats](https://docs.aws.amazon.com/sns/latest/dg/json-formats.html) and
[Amazon SNS Sample
Event](https://docs.aws.amazon.com/lambda/latest/dg/eventsources.html#eventsources-sns).
For an example use case, see [Using AWS Lambda with Amazon SNS from Different
Accounts](https://docs.aws.amazon.com/lambda/latest/dg/with-sns.html).

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_sns as sns
from aws_cdk.aws_lambda_event_sources import SnsEventSource

topic = sns.Topic(...)
dead_letter_queue = sqs.Queue(self, "deadLetterQueue")

lambda_.add_event_source(SnsEventSource(topic,
    filter_policy={...},
    dead_letter_queue=dead_letter_queue
))
```

When a user calls the SNS Publish API on a topic that your Lambda function is
subscribed to, Amazon SNS will call Lambda to invoke your function
asynchronously. Lambda will then return a delivery status. If there was an error
calling Lambda, Amazon SNS will retry invoking the Lambda function up to three
times. After three tries, if Amazon SNS still could not successfully invoke the
Lambda function, then Amazon SNS will send a delivery status failure message to
CloudWatch.

## DynamoDB Streams

You can write Lambda functions to process change events from a DynamoDB Table. An event is emitted to a DynamoDB stream (if configured) whenever a write (Put, Delete, Update)
operation is performed against the table. See [Using AWS Lambda with Amazon DynamoDB](https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html) for more information about configuring Lambda function event sources with DynamoDB.

To process events with a Lambda function, first create or update a DynamoDB table and enable a `stream` specification. Then, create a `DynamoEventSource`
and add it to your Lambda function. The following parameters will impact Amazon DynamoDB's polling behavior:

* **batchSize**: Determines how many records are buffered before invoking your lambda function - could impact your function's memory usage (if too high) and ability to keep up with incoming data velocity (if too low).
* **bisectBatchOnError**: If a batch encounters an error, this will cause the batch to be split in two and have each new smaller batch retried, allowing the records in error to be isolated.
* **maxBatchingWindow**: The maximum amount of time to gather records before invoking the lambda. This increases the likelihood of a full batch at the cost of delayed processing.
* **maxRecordAge**: The maximum age of a record that will be sent to the function for processing. Records that exceed the max age will be treated as failures.
* **onFailure**: In the event a record fails after all retries or if the record age has exceeded the configured value, the record will be sent to SQS queue or SNS topic that is specified here
* **parallelizationFactor**: The number of batches to concurrently process on each shard.
* **retryAttempts**: The maximum number of times a record should be retried in the event of failure.
* **startingPosition**: Will determine where to being consumption, either at the most recent ('LATEST') record or the oldest record ('TRIM_HORIZON'). 'TRIM_HORIZON' will ensure you process all available data, while 'LATEST' will ignore all records that arrived prior to attaching the event source.
* **enabled**: If the DynamoDB Streams event source mapping should be enabled. The default is true.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_dynamodb as dynamodb
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_sqs as sqs
from aws_cdk.aws_lambda_event_sources import DynamoEventSource, SqsDlq

table = dynamodb.Table(...,
    partition_key=, ...,
    stream=dynamodb.StreamViewType.NEW_IMAGE
)

dead_letter_queue = sqs.Queue(self, "deadLetterQueue")def ():
    passlambda_.Function(...)
def ():
    passadd_event_source(DynamoEventSource(table,
    starting_position=lambda_.StartingPosition.TRIM_HORIZON,
    batch_size=5,
    bisect_batch_on_error=True,
    on_failure=SqsDlq(dead_letter_queue),
    retry_attempts=10
))
```

## Kinesis

You can write Lambda functions to process streaming data in Amazon Kinesis Streams. For more information about Amazon Kinesis, see [Amazon Kinesis
Service](https://aws.amazon.com/kinesis/data-streams/). To learn more about configuring Lambda function event sources with kinesis and view a sample event,
see [Amazon Kinesis Event](https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis.html).

To set up Amazon Kinesis as an event source for AWS Lambda, you
first create or update an Amazon Kinesis stream and select custom values for the
event source parameters. The following parameters will impact Amazon Kinesis's polling
behavior:

* **batchSize**: Determines how many records are buffered before invoking your lambda function - could impact your function's memory usage (if too high) and ability to keep up with incoming data velocity (if too low).
* **bisectBatchOnError**: If a batch encounters an error, this will cause the batch to be split in two and have each new smaller batch retried, allowing the records in error to be isolated.
* **maxBatchingWindow**: The maximum amount of time to gather records before invoking the lambda. This increases the likelihood of a full batch at the cost of possibly delaying processing.
* **maxRecordAge**: The maximum age of a record that will be sent to the function for processing. Records that exceed the max age will be treated as failures.
* **onFailure**: In the event a record fails and consumes all retries, the record will be sent to SQS queue or SNS topic that is specified here
* **parallelizationFactor**: The number of batches to concurrently process on each shard.
* **retryAttempts**: The maximum number of times a record should be retried in the event of failure.
* **startingPosition**: Will determine where to being consumption, either at the most recent ('LATEST') record or the oldest record ('TRIM_HORIZON'). 'TRIM_HORIZON' will ensure you process all available data, while 'LATEST' will ignore all records that arrived prior to attaching the event source.
* **enabled**: If the DynamoDB Streams event source mapping should be enabled. The default is true.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_kinesis as kinesis
from aws_cdk.aws_lambda_event_sources import KinesisEventSource

stream = kinesis.Stream(self, "MyStream")

my_function.add_event_source(KinesisEventSource(stream,
    batch_size=100, # default
    starting_position=lambda_.StartingPosition.TRIM_HORIZON
))
```

## Kafka

You can write Lambda functions to process data either from [Amazon MSK](https://docs.aws.amazon.com/lambda/latest/dg/with-msk.html) or a [self managed Kafka](https://docs.aws.amazon.com/lambda/latest/dg/kafka-smaa.html) cluster.

The following code sets up Amazon MSK as an event source for a lambda function. Credentials will need to be configured to access the
MSK cluster, as described in [Username/Password authentication](https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html).

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_lambda as msk
from aws_cdk.aws_secretmanager import Secret
from aws_cdk.aws_lambda_event_sources import ManagedKafkaEventSource

# Your MSK cluster
cluster = msk.Cluster.from_cluster_arn(self, "Cluster", "arn:aws:kafka:us-east-1:0123456789019:cluster/SalesCluster/abcd1234-abcd-cafe-abab-9876543210ab-4")

# The Kafka topic you want to subscribe to
topic = "some-cool-topic"

# The secret that allows access to your MSK cluster
# You still have to make sure that it is associated with your cluster as described in the documentation
secret = Secret(self, "Secret", secret_name="AmazonMSK_KafkaSecret")

my_function.add_event_source(ManagedKafkaEventSource(
    cluster=cluster,
    topic=topic,
    secret=secret,
    batch_size=100, # default
    starting_position=lambda_.StartingPosition.TRIM_HORIZON
))
```

The following code sets up a self managed Kafka cluster as an event source. Username and password based authentication
will need to be set up as described in [Managing access and permissions](https://docs.aws.amazon.com/lambda/latest/dg/smaa-permissions.html#smaa-permissions-add-secret).

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_lambda as lambda_
from aws_cdk.aws_secretmanager import Secret
from aws_cdk.aws_lambda_event_sources import SelfManagedKafkaEventSource

# The list of Kafka brokers
bootstrap_servers = ["kafka-broker:9092"]

# The Kafka topic you want to subscribe to
topic = "some-cool-topic"

# The secret that allows access to your self hosted Kafka cluster
secret = Secret(self, "Secret", ...)

my_function.add_event_source(SelfManagedKafkaEventSource(
    bootstrap_servers=bootstrap_servers,
    topic=topic,
    secret=secret,
    batch_size=100, # default
    starting_position=lambda_.StartingPosition.TRIM_HORIZON
))
```

If your self managed Kafka cluster is only reachable via VPC also configure `vpc` `vpcSubnets` and `securityGroup`.

## Roadmap

Eventually, this module will support all the event sources described under
[Supported Event
Sources](https://docs.aws.amazon.com/lambda/latest/dg/invoking-lambda-function.html)
in the AWS Lambda Developer Guide.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

from .. import Duration as _Duration_070aa057
from ..aws_apigateway import (
    AuthorizationType as _AuthorizationType_0ef85b12,
    IAuthorizer as _IAuthorizer_6ddd4da0,
    IModel as _IModel_f4167163,
    IRequestValidator as _IRequestValidator_8d44748f,
    MethodOptions as _MethodOptions_285920d7,
    MethodResponse as _MethodResponse_bb921d07,
    RequestValidatorOptions as _RequestValidatorOptions_b89e3f10,
)
from ..aws_dynamodb import ITable as _ITable_24826f7e
from ..aws_ec2 import (
    ISecurityGroup as _ISecurityGroup_cdbba9d3,
    IVpc as _IVpc_6d1f76c4,
    SubnetSelection as _SubnetSelection_1284e62c,
)
from ..aws_kinesis import IStream as _IStream_14c6ec7f
from ..aws_lambda import (
    DlqDestinationConfig as _DlqDestinationConfig_563cae69,
    EventSourceMappingOptions as _EventSourceMappingOptions_36519f99,
    IEventSource as _IEventSource_7914870e,
    IEventSourceDlq as _IEventSourceDlq_f5ae73e7,
    IEventSourceMapping as _IEventSourceMapping_b4960cf6,
    IFunction as _IFunction_6e14f09e,
    SourceAccessConfiguration as _SourceAccessConfiguration_afc347bf,
    StartingPosition as _StartingPosition_9192859a,
)
from ..aws_msk import ICluster as _ICluster_6fd159f2
from ..aws_s3 import (
    Bucket as _Bucket_aa378085,
    EventType as _EventType_5af33d27,
    NotificationKeyFilter as _NotificationKeyFilter_7f4bf31a,
)
from ..aws_secretsmanager import ISecret as _ISecret_22fb8757
from ..aws_sns import (
    ITopic as _ITopic_465e36b9, SubscriptionFilter as _SubscriptionFilter_1f5c48ae
)
from ..aws_sns_subscriptions import (
    LambdaSubscriptionProps as _LambdaSubscriptionProps_d5f9085e
)
from ..aws_sqs import IQueue as _IQueue_45a01ab4


@jsii.implements(_IEventSource_7914870e)
class ApiEventSource(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_event_sources.ApiEventSource",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        method: builtins.str,
        path: builtins.str,
        *,
        api_key_required: typing.Optional[builtins.bool] = None,
        authorization_scopes: typing.Optional[typing.List[builtins.str]] = None,
        authorization_type: typing.Optional[_AuthorizationType_0ef85b12] = None,
        authorizer: typing.Optional[_IAuthorizer_6ddd4da0] = None,
        method_responses: typing.Optional[typing.List[_MethodResponse_bb921d07]] = None,
        operation_name: typing.Optional[builtins.str] = None,
        request_models: typing.Optional[typing.Mapping[builtins.str, _IModel_f4167163]] = None,
        request_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.bool]] = None,
        request_validator: typing.Optional[_IRequestValidator_8d44748f] = None,
        request_validator_options: typing.Optional[_RequestValidatorOptions_b89e3f10] = None,
    ) -> None:
        '''
        :param method: -
        :param path: -
        :param api_key_required: (experimental) Indicates whether the method requires clients to submit a valid API key. Default: false
        :param authorization_scopes: (experimental) A list of authorization scopes configured on the method. The scopes are used with a COGNITO_USER_POOLS authorizer to authorize the method invocation. Default: - no authorization scopes
        :param authorization_type: (experimental) Method authorization. If the value is set of ``Custom``, an ``authorizer`` must also be specified. If you're using one of the authorizers that are available via the {@link Authorizer} class, such as {@link Authorizer#token()}, it is recommended that this option not be specified. The authorizer will take care of setting the correct authorization type. However, specifying an authorization type using this property that conflicts with what is expected by the {@link Authorizer} will result in an error. Default: - open access unless ``authorizer`` is specified
        :param authorizer: (experimental) If ``authorizationType`` is ``Custom``, this specifies the ID of the method authorizer resource. If specified, the value of ``authorizationType`` must be set to ``Custom``
        :param method_responses: (experimental) The responses that can be sent to the client who calls the method. Default: None This property is not required, but if these are not supplied for a Lambda proxy integration, the Lambda function must return a value of the correct format, for the integration response to be correctly mapped to a response to the client.
        :param operation_name: (experimental) A friendly operation name for the method. For example, you can assign the OperationName of ListPets for the GET /pets method.
        :param request_models: (experimental) The models which describe data structure of request payload. When combined with ``requestValidator`` or ``requestValidatorOptions``, the service will validate the API request payload before it reaches the API's Integration (including proxies). Specify ``requestModels`` as key-value pairs, with a content type (e.g. ``'application/json'``) as the key and an API Gateway Model as the value.
        :param request_parameters: (experimental) The request parameters that API Gateway accepts. Specify request parameters as key-value pairs (string-to-Boolean mapping), with a source as the key and a Boolean as the value. The Boolean specifies whether a parameter is required. A source must match the format method.request.location.name, where the location is querystring, path, or header, and name is a valid, unique parameter name. Default: None
        :param request_validator: (experimental) The ID of the associated request validator. Only one of ``requestValidator`` or ``requestValidatorOptions`` must be specified. Works together with ``requestModels`` or ``requestParameters`` to validate the request before it reaches integration like Lambda Proxy Integration. Default: - No default validator
        :param request_validator_options: (experimental) Request validator options to create new validator Only one of ``requestValidator`` or ``requestValidatorOptions`` must be specified. Works together with ``requestModels`` or ``requestParameters`` to validate the request before it reaches integration like Lambda Proxy Integration. Default: - No default validator

        :stability: experimental
        '''
        options = _MethodOptions_285920d7(
            api_key_required=api_key_required,
            authorization_scopes=authorization_scopes,
            authorization_type=authorization_type,
            authorizer=authorizer,
            method_responses=method_responses,
            operation_name=operation_name,
            request_models=request_models,
            request_parameters=request_parameters,
            request_validator=request_validator,
            request_validator_options=request_validator_options,
        )

        jsii.create(ApiEventSource, self, [method, path, options])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _IFunction_6e14f09e) -> None:
        '''(experimental) Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "bind", [target]))


@jsii.enum(jsii_type="monocdk.aws_lambda_event_sources.AuthenticationMethod")
class AuthenticationMethod(enum.Enum):
    '''(experimental) The authentication method to use with SelfManagedKafkaEventSource.

    :stability: experimental
    '''

    SASL_SCRAM_512_AUTH = "SASL_SCRAM_512_AUTH"
    '''(experimental) SASL_SCRAM_512_AUTH authentication method for your Kafka cluster.

    :stability: experimental
    '''
    SASL_SCRAM_256_AUTH = "SASL_SCRAM_256_AUTH"
    '''(experimental) SASL_SCRAM_256_AUTH authentication method for your Kafka cluster.

    :stability: experimental
    '''


@jsii.implements(_IEventSource_7914870e)
class S3EventSource(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_event_sources.S3EventSource",
):
    '''(experimental) Use S3 bucket notifications as an event source for AWS Lambda.

    :stability: experimental
    '''

    def __init__(
        self,
        bucket: _Bucket_aa378085,
        *,
        events: typing.List[_EventType_5af33d27],
        filters: typing.Optional[typing.List[_NotificationKeyFilter_7f4bf31a]] = None,
    ) -> None:
        '''
        :param bucket: -
        :param events: (experimental) The s3 event types that will trigger the notification.
        :param filters: (experimental) S3 object key filter rules to determine which objects trigger this event. Each filter must include a ``prefix`` and/or ``suffix`` that will be matched against the s3 object key. Refer to the S3 Developer Guide for details about allowed filter rules.

        :stability: experimental
        '''
        props = S3EventSourceProps(events=events, filters=filters)

        jsii.create(S3EventSource, self, [bucket, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _IFunction_6e14f09e) -> None:
        '''(experimental) Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "bind", [target]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> _Bucket_aa378085:
        '''
        :stability: experimental
        '''
        return typing.cast(_Bucket_aa378085, jsii.get(self, "bucket"))


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_event_sources.S3EventSourceProps",
    jsii_struct_bases=[],
    name_mapping={"events": "events", "filters": "filters"},
)
class S3EventSourceProps:
    def __init__(
        self,
        *,
        events: typing.List[_EventType_5af33d27],
        filters: typing.Optional[typing.List[_NotificationKeyFilter_7f4bf31a]] = None,
    ) -> None:
        '''
        :param events: (experimental) The s3 event types that will trigger the notification.
        :param filters: (experimental) S3 object key filter rules to determine which objects trigger this event. Each filter must include a ``prefix`` and/or ``suffix`` that will be matched against the s3 object key. Refer to the S3 Developer Guide for details about allowed filter rules.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "events": events,
        }
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def events(self) -> typing.List[_EventType_5af33d27]:
        '''(experimental) The s3 event types that will trigger the notification.

        :stability: experimental
        '''
        result = self._values.get("events")
        assert result is not None, "Required property 'events' is missing"
        return typing.cast(typing.List[_EventType_5af33d27], result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[_NotificationKeyFilter_7f4bf31a]]:
        '''(experimental) S3 object key filter rules to determine which objects trigger this event.

        Each filter must include a ``prefix`` and/or ``suffix`` that will be matched
        against the s3 object key. Refer to the S3 Developer Guide for details
        about allowed filter rules.

        :stability: experimental
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[_NotificationKeyFilter_7f4bf31a]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3EventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IEventSourceDlq_f5ae73e7)
class SnsDlq(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_event_sources.SnsDlq",
):
    '''(experimental) An SNS dead letter queue destination configuration for a Lambda event source.

    :stability: experimental
    '''

    def __init__(self, topic: _ITopic_465e36b9) -> None:
        '''
        :param topic: -

        :stability: experimental
        '''
        jsii.create(SnsDlq, self, [topic])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _target: _IEventSourceMapping_b4960cf6,
        target_handler: _IFunction_6e14f09e,
    ) -> _DlqDestinationConfig_563cae69:
        '''(experimental) Returns a destination configuration for the DLQ.

        :param _target: -
        :param target_handler: -

        :stability: experimental
        '''
        return typing.cast(_DlqDestinationConfig_563cae69, jsii.invoke(self, "bind", [_target, target_handler]))


@jsii.implements(_IEventSource_7914870e)
class SnsEventSource(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_event_sources.SnsEventSource",
):
    '''(experimental) Use an Amazon SNS topic as an event source for AWS Lambda.

    :stability: experimental
    '''

    def __init__(
        self,
        topic: _ITopic_465e36b9,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    ) -> None:
        '''
        :param topic: -
        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered

        :stability: experimental
        '''
        props = SnsEventSourceProps(
            dead_letter_queue=dead_letter_queue, filter_policy=filter_policy
        )

        jsii.create(SnsEventSource, self, [topic, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _IFunction_6e14f09e) -> None:
        '''(experimental) Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "bind", [target]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="topic")
    def topic(self) -> _ITopic_465e36b9:
        '''
        :stability: experimental
        '''
        return typing.cast(_ITopic_465e36b9, jsii.get(self, "topic"))


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_event_sources.SnsEventSourceProps",
    jsii_struct_bases=[_LambdaSubscriptionProps_d5f9085e],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "filter_policy": "filterPolicy",
    },
)
class SnsEventSourceProps(_LambdaSubscriptionProps_d5f9085e):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        filter_policy: typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]] = None,
    ) -> None:
        '''(experimental) Properties forwarded to the Lambda Subscription.

        :param dead_letter_queue: (experimental) Queue to be used as dead letter queue. If not passed no dead letter queue is enabled. Default: - No dead letter queue enabled.
        :param filter_policy: (experimental) The filter policy. Default: - all messages are delivered

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_45a01ab4]:
        '''(experimental) Queue to be used as dead letter queue.

        If not passed no dead letter queue is enabled.

        :default: - No dead letter queue enabled.

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_45a01ab4], result)

    @builtins.property
    def filter_policy(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]]:
        '''(experimental) The filter policy.

        :default: - all messages are delivered

        :stability: experimental
        '''
        result = self._values.get("filter_policy")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _SubscriptionFilter_1f5c48ae]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IEventSourceDlq_f5ae73e7)
class SqsDlq(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_event_sources.SqsDlq",
):
    '''(experimental) An SQS dead letter queue destination configuration for a Lambda event source.

    :stability: experimental
    '''

    def __init__(self, queue: _IQueue_45a01ab4) -> None:
        '''
        :param queue: -

        :stability: experimental
        '''
        jsii.create(SqsDlq, self, [queue])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _target: _IEventSourceMapping_b4960cf6,
        target_handler: _IFunction_6e14f09e,
    ) -> _DlqDestinationConfig_563cae69:
        '''(experimental) Returns a destination configuration for the DLQ.

        :param _target: -
        :param target_handler: -

        :stability: experimental
        '''
        return typing.cast(_DlqDestinationConfig_563cae69, jsii.invoke(self, "bind", [_target, target_handler]))


@jsii.implements(_IEventSource_7914870e)
class SqsEventSource(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_event_sources.SqsEventSource",
):
    '''(experimental) Use an Amazon SQS queue as an event source for AWS Lambda.

    :stability: experimental
    '''

    def __init__(
        self,
        queue: _IQueue_45a01ab4,
        *,
        batch_size: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param queue: -
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10. Default: 10
        :param enabled: (experimental) If the SQS event source mapping should be enabled. Default: true

        :stability: experimental
        '''
        props = SqsEventSourceProps(batch_size=batch_size, enabled=enabled)

        jsii.create(SqsEventSource, self, [queue, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _IFunction_6e14f09e) -> None:
        '''(experimental) Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "bind", [target]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="eventSourceMappingId")
    def event_source_mapping_id(self) -> builtins.str:
        '''(experimental) The identifier for this EventSourceMapping.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "eventSourceMappingId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="queue")
    def queue(self) -> _IQueue_45a01ab4:
        '''
        :stability: experimental
        '''
        return typing.cast(_IQueue_45a01ab4, jsii.get(self, "queue"))


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_event_sources.SqsEventSourceProps",
    jsii_struct_bases=[],
    name_mapping={"batch_size": "batchSize", "enabled": "enabled"},
)
class SqsEventSourceProps:
    def __init__(
        self,
        *,
        batch_size: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10. Default: 10
        :param enabled: (experimental) If the SQS event source mapping should be enabled. Default: true

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range: Minimum value of 1. Maximum value of 10.

        :default: 10

        :stability: experimental
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the SQS event source mapping should be enabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IEventSource_7914870e)
class StreamEventSource(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_lambda_event_sources.StreamEventSource",
):
    '''(experimental) Use an stream as an event source for AWS Lambda.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_StreamEventSourceProxy"]:
        return _StreamEventSourceProxy

    def __init__(
        self,
        *,
        starting_position: _StartingPosition_9192859a,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_Duration_070aa057] = None,
        max_record_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IEventSourceDlq_f5ae73e7] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param starting_position: (experimental) Where to begin consuming the stream.
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: (experimental) If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: (experimental) If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: (experimental) The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: (experimental) The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: (experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: (experimental) The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: (experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000

        :stability: experimental
        '''
        props = StreamEventSourceProps(
            starting_position=starting_position,
            batch_size=batch_size,
            bisect_batch_on_error=bisect_batch_on_error,
            enabled=enabled,
            max_batching_window=max_batching_window,
            max_record_age=max_record_age,
            on_failure=on_failure,
            parallelization_factor=parallelization_factor,
            retry_attempts=retry_attempts,
        )

        jsii.create(StreamEventSource, self, [props])

    @jsii.member(jsii_name="bind") # type: ignore[misc]
    @abc.abstractmethod
    def bind(self, _target: _IFunction_6e14f09e) -> None:
        '''(experimental) Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param _target: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="enrichMappingOptions")
    def _enrich_mapping_options(
        self,
        *,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_source_arn: typing.Optional[builtins.str] = None,
        kafka_bootstrap_servers: typing.Optional[typing.List[builtins.str]] = None,
        kafka_topic: typing.Optional[builtins.str] = None,
        max_batching_window: typing.Optional[_Duration_070aa057] = None,
        max_record_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IEventSourceDlq_f5ae73e7] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        source_access_configurations: typing.Optional[typing.List[_SourceAccessConfiguration_afc347bf]] = None,
        starting_position: typing.Optional[_StartingPosition_9192859a] = None,
    ) -> _EventSourceMappingOptions_36519f99:
        '''
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10000. Default: - Amazon Kinesis, Amazon DynamoDB, and Amazon MSK is 100 records. Both the default and maximum for Amazon SQS are 10 messages.
        :param bisect_batch_on_error: (experimental) If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: (experimental) Set to false to disable the event source upon creation. Default: true
        :param event_source_arn: (experimental) The Amazon Resource Name (ARN) of the event source. Any record added to this stream can invoke the Lambda function. Default: - not set if using a self managed Kafka cluster, throws an error otherwise
        :param kafka_bootstrap_servers: (experimental) A list of host and port pairs that are the addresses of the Kafka brokers in a self managed "bootstrap" Kafka cluster that a Kafka client connects to initially to bootstrap itself. They are in the format ``abc.example.com:9096``. Default: - none
        :param kafka_topic: (experimental) The name of the Kafka topic. Default: - no topic
        :param max_batching_window: (experimental) The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: (experimental) The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: - infinite or until the record expires.
        :param on_failure: (experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: (experimental) The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Set to ``undefined`` if you want lambda to keep retrying infinitely or until the record expires. Valid Range: - Minimum value of 0 - Maximum value of 10000 Default: - infinite or until the record expires.
        :param source_access_configurations: (experimental) Specific settings like the authentication protocol or the VPC components to secure access to your event source. Default: - none
        :param starting_position: (experimental) The position in the DynamoDB, Kinesis or MSK stream where AWS Lambda should start reading. Default: - Required for Amazon Kinesis, Amazon DynamoDB, and Amazon MSK Streams sources.

        :stability: experimental
        '''
        options = _EventSourceMappingOptions_36519f99(
            batch_size=batch_size,
            bisect_batch_on_error=bisect_batch_on_error,
            enabled=enabled,
            event_source_arn=event_source_arn,
            kafka_bootstrap_servers=kafka_bootstrap_servers,
            kafka_topic=kafka_topic,
            max_batching_window=max_batching_window,
            max_record_age=max_record_age,
            on_failure=on_failure,
            parallelization_factor=parallelization_factor,
            retry_attempts=retry_attempts,
            source_access_configurations=source_access_configurations,
            starting_position=starting_position,
        )

        return typing.cast(_EventSourceMappingOptions_36519f99, jsii.invoke(self, "enrichMappingOptions", [options]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="props")
    def _props(self) -> "StreamEventSourceProps":
        '''
        :stability: experimental
        '''
        return typing.cast("StreamEventSourceProps", jsii.get(self, "props"))


class _StreamEventSourceProxy(StreamEventSource):
    @jsii.member(jsii_name="bind")
    def bind(self, _target: _IFunction_6e14f09e) -> None:
        '''(experimental) Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param _target: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "bind", [_target]))


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_event_sources.StreamEventSourceProps",
    jsii_struct_bases=[],
    name_mapping={
        "starting_position": "startingPosition",
        "batch_size": "batchSize",
        "bisect_batch_on_error": "bisectBatchOnError",
        "enabled": "enabled",
        "max_batching_window": "maxBatchingWindow",
        "max_record_age": "maxRecordAge",
        "on_failure": "onFailure",
        "parallelization_factor": "parallelizationFactor",
        "retry_attempts": "retryAttempts",
    },
)
class StreamEventSourceProps:
    def __init__(
        self,
        *,
        starting_position: _StartingPosition_9192859a,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_Duration_070aa057] = None,
        max_record_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IEventSourceDlq_f5ae73e7] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) The set of properties for event sources that follow the streaming model, such as, Dynamo, Kinesis and Kafka.

        :param starting_position: (experimental) Where to begin consuming the stream.
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: (experimental) If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: (experimental) If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: (experimental) The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: (experimental) The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: (experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: (experimental) The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: (experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "starting_position": starting_position,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if bisect_batch_on_error is not None:
            self._values["bisect_batch_on_error"] = bisect_batch_on_error
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_batching_window is not None:
            self._values["max_batching_window"] = max_batching_window
        if max_record_age is not None:
            self._values["max_record_age"] = max_record_age
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts

    @builtins.property
    def starting_position(self) -> _StartingPosition_9192859a:
        '''(experimental) Where to begin consuming the stream.

        :stability: experimental
        '''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(_StartingPosition_9192859a, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}

        :default: 100

        :stability: experimental
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bisect_batch_on_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the function returns an error, split the batch in two and retry.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("bisect_batch_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the stream event source mapping should be enabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum amount of time to gather records before invoking the function.

        Maximum of Duration.minutes(5)

        :default: Duration.seconds(0)

        :stability: experimental
        '''
        result = self._values.get("max_batching_window")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def max_record_age(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum age of a record that Lambda sends to a function for processing.

        Valid Range:

        - Minimum value of 60 seconds
        - Maximum value of 7 days

        :default: Duration.days(7)

        :stability: experimental
        '''
        result = self._values.get("max_record_age")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def on_failure(self) -> typing.Optional[_IEventSourceDlq_f5ae73e7]:
        '''(experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records.

        :default: discarded records are ignored

        :stability: experimental
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional[_IEventSourceDlq_f5ae73e7], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of batches to process from each shard concurrently.

        Valid Range:

        - Minimum value of 1
        - Maximum value of 10

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000.

        :default: 10000

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DynamoEventSource(
    StreamEventSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_event_sources.DynamoEventSource",
):
    '''(experimental) Use an Amazon DynamoDB stream as an event source for AWS Lambda.

    :stability: experimental
    '''

    def __init__(
        self,
        table: _ITable_24826f7e,
        *,
        starting_position: _StartingPosition_9192859a,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_Duration_070aa057] = None,
        max_record_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IEventSourceDlq_f5ae73e7] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param table: -
        :param starting_position: (experimental) Where to begin consuming the stream.
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: (experimental) If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: (experimental) If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: (experimental) The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: (experimental) The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: (experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: (experimental) The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: (experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000

        :stability: experimental
        '''
        props = DynamoEventSourceProps(
            starting_position=starting_position,
            batch_size=batch_size,
            bisect_batch_on_error=bisect_batch_on_error,
            enabled=enabled,
            max_batching_window=max_batching_window,
            max_record_age=max_record_age,
            on_failure=on_failure,
            parallelization_factor=parallelization_factor,
            retry_attempts=retry_attempts,
        )

        jsii.create(DynamoEventSource, self, [table, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _IFunction_6e14f09e) -> None:
        '''(experimental) Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "bind", [target]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="eventSourceMappingId")
    def event_source_mapping_id(self) -> builtins.str:
        '''(experimental) The identifier for this EventSourceMapping.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "eventSourceMappingId"))


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_event_sources.DynamoEventSourceProps",
    jsii_struct_bases=[StreamEventSourceProps],
    name_mapping={
        "starting_position": "startingPosition",
        "batch_size": "batchSize",
        "bisect_batch_on_error": "bisectBatchOnError",
        "enabled": "enabled",
        "max_batching_window": "maxBatchingWindow",
        "max_record_age": "maxRecordAge",
        "on_failure": "onFailure",
        "parallelization_factor": "parallelizationFactor",
        "retry_attempts": "retryAttempts",
    },
)
class DynamoEventSourceProps(StreamEventSourceProps):
    def __init__(
        self,
        *,
        starting_position: _StartingPosition_9192859a,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_Duration_070aa057] = None,
        max_record_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IEventSourceDlq_f5ae73e7] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param starting_position: (experimental) Where to begin consuming the stream.
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: (experimental) If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: (experimental) If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: (experimental) The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: (experimental) The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: (experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: (experimental) The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: (experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "starting_position": starting_position,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if bisect_batch_on_error is not None:
            self._values["bisect_batch_on_error"] = bisect_batch_on_error
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_batching_window is not None:
            self._values["max_batching_window"] = max_batching_window
        if max_record_age is not None:
            self._values["max_record_age"] = max_record_age
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts

    @builtins.property
    def starting_position(self) -> _StartingPosition_9192859a:
        '''(experimental) Where to begin consuming the stream.

        :stability: experimental
        '''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(_StartingPosition_9192859a, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}

        :default: 100

        :stability: experimental
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bisect_batch_on_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the function returns an error, split the batch in two and retry.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("bisect_batch_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the stream event source mapping should be enabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum amount of time to gather records before invoking the function.

        Maximum of Duration.minutes(5)

        :default: Duration.seconds(0)

        :stability: experimental
        '''
        result = self._values.get("max_batching_window")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def max_record_age(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum age of a record that Lambda sends to a function for processing.

        Valid Range:

        - Minimum value of 60 seconds
        - Maximum value of 7 days

        :default: Duration.days(7)

        :stability: experimental
        '''
        result = self._values.get("max_record_age")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def on_failure(self) -> typing.Optional[_IEventSourceDlq_f5ae73e7]:
        '''(experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records.

        :default: discarded records are ignored

        :stability: experimental
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional[_IEventSourceDlq_f5ae73e7], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of batches to process from each shard concurrently.

        Valid Range:

        - Minimum value of 1
        - Maximum value of 10

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000.

        :default: 10000

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DynamoEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_event_sources.KafkaEventSourceProps",
    jsii_struct_bases=[StreamEventSourceProps],
    name_mapping={
        "starting_position": "startingPosition",
        "batch_size": "batchSize",
        "bisect_batch_on_error": "bisectBatchOnError",
        "enabled": "enabled",
        "max_batching_window": "maxBatchingWindow",
        "max_record_age": "maxRecordAge",
        "on_failure": "onFailure",
        "parallelization_factor": "parallelizationFactor",
        "retry_attempts": "retryAttempts",
        "secret": "secret",
        "topic": "topic",
    },
)
class KafkaEventSourceProps(StreamEventSourceProps):
    def __init__(
        self,
        *,
        starting_position: _StartingPosition_9192859a,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_Duration_070aa057] = None,
        max_record_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IEventSourceDlq_f5ae73e7] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        secret: _ISecret_22fb8757,
        topic: builtins.str,
    ) -> None:
        '''(experimental) Properties for a Kafka event source.

        :param starting_position: (experimental) Where to begin consuming the stream.
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: (experimental) If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: (experimental) If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: (experimental) The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: (experimental) The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: (experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: (experimental) The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: (experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000
        :param secret: (experimental) the secret with the Kafka credentials, see https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html for details.
        :param topic: (experimental) the Kafka topic to subscribe to.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "starting_position": starting_position,
            "secret": secret,
            "topic": topic,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if bisect_batch_on_error is not None:
            self._values["bisect_batch_on_error"] = bisect_batch_on_error
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_batching_window is not None:
            self._values["max_batching_window"] = max_batching_window
        if max_record_age is not None:
            self._values["max_record_age"] = max_record_age
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts

    @builtins.property
    def starting_position(self) -> _StartingPosition_9192859a:
        '''(experimental) Where to begin consuming the stream.

        :stability: experimental
        '''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(_StartingPosition_9192859a, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}

        :default: 100

        :stability: experimental
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bisect_batch_on_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the function returns an error, split the batch in two and retry.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("bisect_batch_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the stream event source mapping should be enabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum amount of time to gather records before invoking the function.

        Maximum of Duration.minutes(5)

        :default: Duration.seconds(0)

        :stability: experimental
        '''
        result = self._values.get("max_batching_window")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def max_record_age(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum age of a record that Lambda sends to a function for processing.

        Valid Range:

        - Minimum value of 60 seconds
        - Maximum value of 7 days

        :default: Duration.days(7)

        :stability: experimental
        '''
        result = self._values.get("max_record_age")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def on_failure(self) -> typing.Optional[_IEventSourceDlq_f5ae73e7]:
        '''(experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records.

        :default: discarded records are ignored

        :stability: experimental
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional[_IEventSourceDlq_f5ae73e7], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of batches to process from each shard concurrently.

        Valid Range:

        - Minimum value of 1
        - Maximum value of 10

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000.

        :default: 10000

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret(self) -> _ISecret_22fb8757:
        '''(experimental) the secret with the Kafka credentials, see https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html for details.

        :stability: experimental
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(_ISecret_22fb8757, result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''(experimental) the Kafka topic to subscribe to.

        :stability: experimental
        '''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KafkaEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KinesisEventSource(
    StreamEventSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_event_sources.KinesisEventSource",
):
    '''(experimental) Use an Amazon Kinesis stream as an event source for AWS Lambda.

    :stability: experimental
    '''

    def __init__(
        self,
        stream: _IStream_14c6ec7f,
        *,
        starting_position: _StartingPosition_9192859a,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_Duration_070aa057] = None,
        max_record_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IEventSourceDlq_f5ae73e7] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param stream: -
        :param starting_position: (experimental) Where to begin consuming the stream.
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: (experimental) If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: (experimental) If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: (experimental) The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: (experimental) The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: (experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: (experimental) The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: (experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000

        :stability: experimental
        '''
        props = KinesisEventSourceProps(
            starting_position=starting_position,
            batch_size=batch_size,
            bisect_batch_on_error=bisect_batch_on_error,
            enabled=enabled,
            max_batching_window=max_batching_window,
            max_record_age=max_record_age,
            on_failure=on_failure,
            parallelization_factor=parallelization_factor,
            retry_attempts=retry_attempts,
        )

        jsii.create(KinesisEventSource, self, [stream, props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _IFunction_6e14f09e) -> None:
        '''(experimental) Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "bind", [target]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="eventSourceMappingId")
    def event_source_mapping_id(self) -> builtins.str:
        '''(experimental) The identifier for this EventSourceMapping.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "eventSourceMappingId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stream")
    def stream(self) -> _IStream_14c6ec7f:
        '''
        :stability: experimental
        '''
        return typing.cast(_IStream_14c6ec7f, jsii.get(self, "stream"))


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_event_sources.KinesisEventSourceProps",
    jsii_struct_bases=[StreamEventSourceProps],
    name_mapping={
        "starting_position": "startingPosition",
        "batch_size": "batchSize",
        "bisect_batch_on_error": "bisectBatchOnError",
        "enabled": "enabled",
        "max_batching_window": "maxBatchingWindow",
        "max_record_age": "maxRecordAge",
        "on_failure": "onFailure",
        "parallelization_factor": "parallelizationFactor",
        "retry_attempts": "retryAttempts",
    },
)
class KinesisEventSourceProps(StreamEventSourceProps):
    def __init__(
        self,
        *,
        starting_position: _StartingPosition_9192859a,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_Duration_070aa057] = None,
        max_record_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IEventSourceDlq_f5ae73e7] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param starting_position: (experimental) Where to begin consuming the stream.
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: (experimental) If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: (experimental) If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: (experimental) The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: (experimental) The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: (experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: (experimental) The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: (experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "starting_position": starting_position,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if bisect_batch_on_error is not None:
            self._values["bisect_batch_on_error"] = bisect_batch_on_error
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_batching_window is not None:
            self._values["max_batching_window"] = max_batching_window
        if max_record_age is not None:
            self._values["max_record_age"] = max_record_age
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts

    @builtins.property
    def starting_position(self) -> _StartingPosition_9192859a:
        '''(experimental) Where to begin consuming the stream.

        :stability: experimental
        '''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(_StartingPosition_9192859a, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}

        :default: 100

        :stability: experimental
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bisect_batch_on_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the function returns an error, split the batch in two and retry.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("bisect_batch_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the stream event source mapping should be enabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum amount of time to gather records before invoking the function.

        Maximum of Duration.minutes(5)

        :default: Duration.seconds(0)

        :stability: experimental
        '''
        result = self._values.get("max_batching_window")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def max_record_age(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum age of a record that Lambda sends to a function for processing.

        Valid Range:

        - Minimum value of 60 seconds
        - Maximum value of 7 days

        :default: Duration.days(7)

        :stability: experimental
        '''
        result = self._values.get("max_record_age")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def on_failure(self) -> typing.Optional[_IEventSourceDlq_f5ae73e7]:
        '''(experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records.

        :default: discarded records are ignored

        :stability: experimental
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional[_IEventSourceDlq_f5ae73e7], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of batches to process from each shard concurrently.

        Valid Range:

        - Minimum value of 1
        - Maximum value of 10

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000.

        :default: 10000

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ManagedKafkaEventSource(
    StreamEventSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_event_sources.ManagedKafkaEventSource",
):
    '''(experimental) Use a MSK cluster as a streaming source for AWS Lambda.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        cluster: _ICluster_6fd159f2,
        secret: _ISecret_22fb8757,
        topic: builtins.str,
        starting_position: _StartingPosition_9192859a,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_Duration_070aa057] = None,
        max_record_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IEventSourceDlq_f5ae73e7] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cluster: (experimental) an MSK cluster construct.
        :param secret: (experimental) the secret with the Kafka credentials, see https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html for details.
        :param topic: (experimental) the Kafka topic to subscribe to.
        :param starting_position: (experimental) Where to begin consuming the stream.
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: (experimental) If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: (experimental) If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: (experimental) The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: (experimental) The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: (experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: (experimental) The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: (experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000

        :stability: experimental
        '''
        props = ManagedKafkaEventSourceProps(
            cluster=cluster,
            secret=secret,
            topic=topic,
            starting_position=starting_position,
            batch_size=batch_size,
            bisect_batch_on_error=bisect_batch_on_error,
            enabled=enabled,
            max_batching_window=max_batching_window,
            max_record_age=max_record_age,
            on_failure=on_failure,
            parallelization_factor=parallelization_factor,
            retry_attempts=retry_attempts,
        )

        jsii.create(ManagedKafkaEventSource, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _IFunction_6e14f09e) -> None:
        '''(experimental) Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "bind", [target]))


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_event_sources.ManagedKafkaEventSourceProps",
    jsii_struct_bases=[KafkaEventSourceProps],
    name_mapping={
        "starting_position": "startingPosition",
        "batch_size": "batchSize",
        "bisect_batch_on_error": "bisectBatchOnError",
        "enabled": "enabled",
        "max_batching_window": "maxBatchingWindow",
        "max_record_age": "maxRecordAge",
        "on_failure": "onFailure",
        "parallelization_factor": "parallelizationFactor",
        "retry_attempts": "retryAttempts",
        "secret": "secret",
        "topic": "topic",
        "cluster": "cluster",
    },
)
class ManagedKafkaEventSourceProps(KafkaEventSourceProps):
    def __init__(
        self,
        *,
        starting_position: _StartingPosition_9192859a,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_Duration_070aa057] = None,
        max_record_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IEventSourceDlq_f5ae73e7] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        secret: _ISecret_22fb8757,
        topic: builtins.str,
        cluster: _ICluster_6fd159f2,
    ) -> None:
        '''(experimental) Properties for a MSK event source.

        :param starting_position: (experimental) Where to begin consuming the stream.
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: (experimental) If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: (experimental) If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: (experimental) The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: (experimental) The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: (experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: (experimental) The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: (experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000
        :param secret: (experimental) the secret with the Kafka credentials, see https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html for details.
        :param topic: (experimental) the Kafka topic to subscribe to.
        :param cluster: (experimental) an MSK cluster construct.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "starting_position": starting_position,
            "secret": secret,
            "topic": topic,
            "cluster": cluster,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if bisect_batch_on_error is not None:
            self._values["bisect_batch_on_error"] = bisect_batch_on_error
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_batching_window is not None:
            self._values["max_batching_window"] = max_batching_window
        if max_record_age is not None:
            self._values["max_record_age"] = max_record_age
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts

    @builtins.property
    def starting_position(self) -> _StartingPosition_9192859a:
        '''(experimental) Where to begin consuming the stream.

        :stability: experimental
        '''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(_StartingPosition_9192859a, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}

        :default: 100

        :stability: experimental
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bisect_batch_on_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the function returns an error, split the batch in two and retry.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("bisect_batch_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the stream event source mapping should be enabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum amount of time to gather records before invoking the function.

        Maximum of Duration.minutes(5)

        :default: Duration.seconds(0)

        :stability: experimental
        '''
        result = self._values.get("max_batching_window")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def max_record_age(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum age of a record that Lambda sends to a function for processing.

        Valid Range:

        - Minimum value of 60 seconds
        - Maximum value of 7 days

        :default: Duration.days(7)

        :stability: experimental
        '''
        result = self._values.get("max_record_age")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def on_failure(self) -> typing.Optional[_IEventSourceDlq_f5ae73e7]:
        '''(experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records.

        :default: discarded records are ignored

        :stability: experimental
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional[_IEventSourceDlq_f5ae73e7], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of batches to process from each shard concurrently.

        Valid Range:

        - Minimum value of 1
        - Maximum value of 10

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000.

        :default: 10000

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret(self) -> _ISecret_22fb8757:
        '''(experimental) the secret with the Kafka credentials, see https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html for details.

        :stability: experimental
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(_ISecret_22fb8757, result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''(experimental) the Kafka topic to subscribe to.

        :stability: experimental
        '''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster(self) -> _ICluster_6fd159f2:
        '''(experimental) an MSK cluster construct.

        :stability: experimental
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(_ICluster_6fd159f2, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedKafkaEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SelfManagedKafkaEventSource(
    StreamEventSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_event_sources.SelfManagedKafkaEventSource",
):
    '''(experimental) Use a self hosted Kafka installation as a streaming source for AWS Lambda.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        bootstrap_servers: typing.List[builtins.str],
        authentication_method: typing.Optional[AuthenticationMethod] = None,
        security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_1284e62c] = None,
        secret: _ISecret_22fb8757,
        topic: builtins.str,
        starting_position: _StartingPosition_9192859a,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_Duration_070aa057] = None,
        max_record_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IEventSourceDlq_f5ae73e7] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bootstrap_servers: (experimental) The list of host and port pairs that are the addresses of the Kafka brokers in a "bootstrap" Kafka cluster that a Kafka client connects to initially to bootstrap itself. They are in the format ``abc.xyz.com:xxxx``.
        :param authentication_method: (experimental) The authentication method for your Kafka cluster. Default: AuthenticationMethod.SASL_SCRAM_512_AUTH
        :param security_group: (experimental) If your Kafka brokers are only reachable via VPC, provide the security group here. Default: - none, required if setting vpc
        :param vpc: (experimental) If your Kafka brokers are only reachable via VPC provide the VPC here. Default: none
        :param vpc_subnets: (experimental) If your Kafka brokers are only reachable via VPC, provide the subnets selection here. Default: - none, required if setting vpc
        :param secret: (experimental) the secret with the Kafka credentials, see https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html for details.
        :param topic: (experimental) the Kafka topic to subscribe to.
        :param starting_position: (experimental) Where to begin consuming the stream.
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: (experimental) If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: (experimental) If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: (experimental) The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: (experimental) The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: (experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: (experimental) The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: (experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000

        :stability: experimental
        '''
        props = SelfManagedKafkaEventSourceProps(
            bootstrap_servers=bootstrap_servers,
            authentication_method=authentication_method,
            security_group=security_group,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
            secret=secret,
            topic=topic,
            starting_position=starting_position,
            batch_size=batch_size,
            bisect_batch_on_error=bisect_batch_on_error,
            enabled=enabled,
            max_batching_window=max_batching_window,
            max_record_age=max_record_age,
            on_failure=on_failure,
            parallelization_factor=parallelization_factor,
            retry_attempts=retry_attempts,
        )

        jsii.create(SelfManagedKafkaEventSource, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, target: _IFunction_6e14f09e) -> None:
        '''(experimental) Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "bind", [target]))


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_event_sources.SelfManagedKafkaEventSourceProps",
    jsii_struct_bases=[KafkaEventSourceProps],
    name_mapping={
        "starting_position": "startingPosition",
        "batch_size": "batchSize",
        "bisect_batch_on_error": "bisectBatchOnError",
        "enabled": "enabled",
        "max_batching_window": "maxBatchingWindow",
        "max_record_age": "maxRecordAge",
        "on_failure": "onFailure",
        "parallelization_factor": "parallelizationFactor",
        "retry_attempts": "retryAttempts",
        "secret": "secret",
        "topic": "topic",
        "bootstrap_servers": "bootstrapServers",
        "authentication_method": "authenticationMethod",
        "security_group": "securityGroup",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
    },
)
class SelfManagedKafkaEventSourceProps(KafkaEventSourceProps):
    def __init__(
        self,
        *,
        starting_position: _StartingPosition_9192859a,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        max_batching_window: typing.Optional[_Duration_070aa057] = None,
        max_record_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IEventSourceDlq_f5ae73e7] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        secret: _ISecret_22fb8757,
        topic: builtins.str,
        bootstrap_servers: typing.List[builtins.str],
        authentication_method: typing.Optional[AuthenticationMethod] = None,
        security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_1284e62c] = None,
    ) -> None:
        '''(experimental) Properties for a self managed Kafka cluster event source.

        If your Kafka cluster is only reachable via VPC make sure to configure it.

        :param starting_position: (experimental) Where to begin consuming the stream.
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: - Minimum value of 1 - Maximum value of: - 1000 for {@link DynamoEventSource} - 10000 for {@link KinesisEventSource} Default: 100
        :param bisect_batch_on_error: (experimental) If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: (experimental) If the stream event source mapping should be enabled. Default: true
        :param max_batching_window: (experimental) The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: (experimental) The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: (experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: (experimental) The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: (experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000. Default: 10000
        :param secret: (experimental) the secret with the Kafka credentials, see https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html for details.
        :param topic: (experimental) the Kafka topic to subscribe to.
        :param bootstrap_servers: (experimental) The list of host and port pairs that are the addresses of the Kafka brokers in a "bootstrap" Kafka cluster that a Kafka client connects to initially to bootstrap itself. They are in the format ``abc.xyz.com:xxxx``.
        :param authentication_method: (experimental) The authentication method for your Kafka cluster. Default: AuthenticationMethod.SASL_SCRAM_512_AUTH
        :param security_group: (experimental) If your Kafka brokers are only reachable via VPC, provide the security group here. Default: - none, required if setting vpc
        :param vpc: (experimental) If your Kafka brokers are only reachable via VPC provide the VPC here. Default: none
        :param vpc_subnets: (experimental) If your Kafka brokers are only reachable via VPC, provide the subnets selection here. Default: - none, required if setting vpc

        :stability: experimental
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_1284e62c(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "starting_position": starting_position,
            "secret": secret,
            "topic": topic,
            "bootstrap_servers": bootstrap_servers,
        }
        if batch_size is not None:
            self._values["batch_size"] = batch_size
        if bisect_batch_on_error is not None:
            self._values["bisect_batch_on_error"] = bisect_batch_on_error
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_batching_window is not None:
            self._values["max_batching_window"] = max_batching_window
        if max_record_age is not None:
            self._values["max_record_age"] = max_record_age
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if parallelization_factor is not None:
            self._values["parallelization_factor"] = parallelization_factor
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if authentication_method is not None:
            self._values["authentication_method"] = authentication_method
        if security_group is not None:
            self._values["security_group"] = security_group
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def starting_position(self) -> _StartingPosition_9192859a:
        '''(experimental) Where to begin consuming the stream.

        :stability: experimental
        '''
        result = self._values.get("starting_position")
        assert result is not None, "Required property 'starting_position' is missing"
        return typing.cast(_StartingPosition_9192859a, result)

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range:

        - Minimum value of 1
        - Maximum value of:

          - 1000 for {@link DynamoEventSource}
          - 10000 for {@link KinesisEventSource}

        :default: 100

        :stability: experimental
        '''
        result = self._values.get("batch_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bisect_batch_on_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the function returns an error, split the batch in two and retry.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("bisect_batch_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the stream event source mapping should be enabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum amount of time to gather records before invoking the function.

        Maximum of Duration.minutes(5)

        :default: Duration.seconds(0)

        :stability: experimental
        '''
        result = self._values.get("max_batching_window")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def max_record_age(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum age of a record that Lambda sends to a function for processing.

        Valid Range:

        - Minimum value of 60 seconds
        - Maximum value of 7 days

        :default: Duration.days(7)

        :stability: experimental
        '''
        result = self._values.get("max_record_age")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def on_failure(self) -> typing.Optional[_IEventSourceDlq_f5ae73e7]:
        '''(experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records.

        :default: discarded records are ignored

        :stability: experimental
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional[_IEventSourceDlq_f5ae73e7], result)

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of batches to process from each shard concurrently.

        Valid Range:

        - Minimum value of 1
        - Maximum value of 10

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("parallelization_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Maximum number of retry attempts Valid Range: * Minimum value of 0 * Maximum value of 10000.

        :default: 10000

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def secret(self) -> _ISecret_22fb8757:
        '''(experimental) the secret with the Kafka credentials, see https://docs.aws.amazon.com/msk/latest/developerguide/msk-password.html for details.

        :stability: experimental
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(_ISecret_22fb8757, result)

    @builtins.property
    def topic(self) -> builtins.str:
        '''(experimental) the Kafka topic to subscribe to.

        :stability: experimental
        '''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bootstrap_servers(self) -> typing.List[builtins.str]:
        '''(experimental) The list of host and port pairs that are the addresses of the Kafka brokers in a "bootstrap" Kafka cluster that a Kafka client connects to initially to bootstrap itself.

        They are in the format ``abc.xyz.com:xxxx``.

        :stability: experimental
        '''
        result = self._values.get("bootstrap_servers")
        assert result is not None, "Required property 'bootstrap_servers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def authentication_method(self) -> typing.Optional[AuthenticationMethod]:
        '''(experimental) The authentication method for your Kafka cluster.

        :default: AuthenticationMethod.SASL_SCRAM_512_AUTH

        :stability: experimental
        '''
        result = self._values.get("authentication_method")
        return typing.cast(typing.Optional[AuthenticationMethod], result)

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_cdbba9d3]:
        '''(experimental) If your Kafka brokers are only reachable via VPC, provide the security group here.

        :default: - none, required if setting vpc

        :stability: experimental
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_ISecurityGroup_cdbba9d3], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(experimental) If your Kafka brokers are only reachable via VPC provide the VPC here.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) If your Kafka brokers are only reachable via VPC, provide the subnets selection here.

        :default: - none, required if setting vpc

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SelfManagedKafkaEventSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ApiEventSource",
    "AuthenticationMethod",
    "DynamoEventSource",
    "DynamoEventSourceProps",
    "KafkaEventSourceProps",
    "KinesisEventSource",
    "KinesisEventSourceProps",
    "ManagedKafkaEventSource",
    "ManagedKafkaEventSourceProps",
    "S3EventSource",
    "S3EventSourceProps",
    "SelfManagedKafkaEventSource",
    "SelfManagedKafkaEventSourceProps",
    "SnsDlq",
    "SnsEventSource",
    "SnsEventSourceProps",
    "SqsDlq",
    "SqsEventSource",
    "SqsEventSourceProps",
    "StreamEventSource",
    "StreamEventSourceProps",
]

publication.publish()
