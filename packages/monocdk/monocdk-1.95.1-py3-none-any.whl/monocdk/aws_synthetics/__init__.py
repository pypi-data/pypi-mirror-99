'''
# Amazon CloudWatch Synthetics Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Developer Preview](https://img.shields.io/badge/cdk--constructs-developer--preview-informational.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are in **developer preview** before they
> become stable. We will only make breaking changes to address unforeseen API issues. Therefore,
> these APIs are not subject to [Semantic Versioning](https://semver.org/), and breaking changes
> will be announced in release notes. This means that while you may use them, you may need to
> update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

Amazon CloudWatch Synthetics allow you to monitor your application by generating **synthetic** traffic. The traffic is produced by a **canary**: a configurable script that runs on a schedule. You configure the canary script to follow the same routes and perform the same actions as a user, which allows you to continually verify your user experience even when you don't have any traffic on your applications.

## Canary

To illustrate how to use a canary, assume your application defines the following endpoint:

```console
% curl "https://api.example.com/user/books/topbook/"
The Hitchhikers Guide to the Galaxy

```

The below code defines a canary that will hit the `books/topbook` endpoint every 5 minutes:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_synthetics as synthetics

canary = synthetics.Canary(self, "MyCanary",
    schedule=synthetics.Schedule.rate(Duration.minutes(5)),
    test=Test.custom(
        code=synthetics.Code.from_asset(path.join(__dirname, "canary")),
        handler="index.handler"
    ),
    runtime=synthetics.Runtime.SYNTHETICS_NODEJS_PUPPETEER_3_0
)
```

The following is an example of an `index.js` file which exports the `handler` function:

```js
var synthetics = require('Synthetics');
const log = require('SyntheticsLogger');

const pageLoadBlueprint = async function () {

    // INSERT URL here
    const URL = "https://api.example.com/user/books/topbook/";

    let page = await synthetics.getPage();
    const response = await page.goto(URL, {waitUntil: 'domcontentloaded', timeout: 30000});
    //Wait for page to render.
    //Increase or decrease wait time based on endpoint being monitored.
    await page.waitFor(15000);
    // This will take a screenshot that will be included in test output artifacts
    await synthetics.takeScreenshot('loaded', 'loaded');
    let pageTitle = await page.title();
    log.info('Page title: ' + pageTitle);
    if (response.status() !== 200) {
        throw "Failed to load page!";
    }
};

exports.handler = async () => {
    return await pageLoadBlueprint();
};
```

> **Note:** The function **must** be called `handler`.

The canary will automatically produce a CloudWatch Dashboard:

![UI Screenshot](images/ui-screenshot.png)

The Canary code will be executed in a lambda function created by Synthetics on your behalf. The Lambda function includes a custom [runtime](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_Library.html) provided by Synthetics. The provided runtime includes a variety of handy tools such as [Puppeteer](https://www.npmjs.com/package/puppeteer-core) (for nodejs based one) and Chromium.

To learn more about Synthetics capabilities, check out the [docs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries.html).

### Configuring the Canary Script

To configure the script the canary executes, use the `test` property. The `test` property accepts a `Test` instance that can be initialized by the `Test` class static methods. Currently, the only implemented method is `Test.custom()`, which allows you to bring your own code. In the future, other methods will be added. `Test.custom()` accepts `code` and `handler` properties -- both are required by Synthetics to create a lambda function on your behalf.

The `synthetics.Code` class exposes static methods to bundle your code artifacts:

* `code.fromInline(code)` - specify an inline script.
* `code.fromAsset(path)` - specify a .zip file or a directory in the local filesystem which will be zipped and uploaded to S3 on deployment. See the above Note for directory structure.
* `code.fromBucket(bucket, key[, objectVersion])` - specify an S3 object that contains the .zip file of your runtime code. See the above Note for directory structure.

Using the `Code` class static initializers:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# To supply the code inline:
canary = Canary(self, "MyCanary",
    test=Test.custom(
        code=synthetics.Code.from_inline("/* Synthetics handler code */"),
        handler="index.handler"
    ),
    runtime=synthetics.Runtime.SYNTHETICS_NODEJS_PUPPETEER_3_0
)

# To supply the code from your local filesystem:
canary = Canary(self, "MyCanary",
    test=Test.custom(
        code=synthetics.Code.from_asset(path.join(__dirname, "canary")),
        handler="index.handler"
    ),
    runtime=synthetics.Runtime.SYNTHETICS_NODEJS_PUPPETEER_3_0
)

# To supply the code from a S3 bucket:
canary = Canary(self, "MyCanary",
    test=Test.custom(
        code=synthetics.Code.from_bucket(bucket, "canary.zip"),
        handler="index.handler"
    ),
    runtime=synthetics.Runtime.SYNTHETICS_NODEJS_PUPPETEER_3_0
)
```

> **Note:** For `code.fromAsset()` and `code.fromBucket()`, the canary resource requires the following folder structure:
>
> ```plaintext
> canary/
> ├── nodejs/
>    ├── node_modules/
>         ├── <filename>.js
> ```
>
> See Synthetics [docs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_WritingCanary.html).

### Alarms

You can configure a CloudWatch Alarm on a canary metric. Metrics are emitted by CloudWatch automatically and can be accessed by the following APIs:

* `canary.metricSuccessPercent()` - percentage of successful canary runs over a given time
* `canary.metricDuration()` - how much time each canary run takes, in seconds.
* `canary.metricFailed()` - number of failed canary runs over a given time

Create an alarm that tracks the canary metric:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cloudwatch.Alarm(self, "CanaryAlarm",
    metric=canary.metric_success_percent(),
    evaluation_periods=2,
    threshold=90,
    comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD
)
```

### Future Work

* Add blueprints to the Test class [#9613](https://github.com/aws/aws-cdk/issues/9613#issue-677134857).
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

import constructs
from .. import (
    AssetHashType as _AssetHashType_49193809,
    BundlingOptions as _BundlingOptions_ab115a99,
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    Duration as _Duration_070aa057,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IgnoreMode as _IgnoreMode_31d8bf46,
    Resource as _Resource_abff4495,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..assets import FollowMode as _FollowMode_98b05cc5
from ..aws_cloudwatch import (
    Metric as _Metric_5b2b8e58,
    MetricOptions as _MetricOptions_1c185ae8,
    Unit as _Unit_113c79f9,
)
from ..aws_iam import IGrantable as _IGrantable_4c5a91d1, IRole as _IRole_59af6f50
from ..aws_s3 import IBucket as _IBucket_73486e29, Location as _Location_cce991ca
from ..aws_s3_assets import AssetOptions as _AssetOptions_bd2996da


@jsii.data_type(
    jsii_type="monocdk.aws_synthetics.ArtifactsBucketLocation",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "prefix": "prefix"},
)
class ArtifactsBucketLocation:
    def __init__(
        self,
        *,
        bucket: _IBucket_73486e29,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for specifying the s3 location that stores the data of each canary run.

        The artifacts bucket location **cannot**
        be updated once the canary is created.

        :param bucket: (experimental) The s3 location that stores the data of each run.
        :param prefix: (experimental) The S3 bucket prefix. Specify this if you want a more specific path within the artifacts bucket. Default: - no prefix

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
        }
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def bucket(self) -> _IBucket_73486e29:
        '''(experimental) The s3 location that stores the data of each run.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_IBucket_73486e29, result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The S3 bucket prefix.

        Specify this if you want a more specific path within the artifacts bucket.

        :default: - no prefix

        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactsBucketLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Canary(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_synthetics.Canary",
):
    '''(experimental) Define a new Canary.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        runtime: "Runtime",
        test: "Test",
        artifacts_bucket_location: typing.Optional[ArtifactsBucketLocation] = None,
        canary_name: typing.Optional[builtins.str] = None,
        failure_retention_period: typing.Optional[_Duration_070aa057] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        schedule: typing.Optional["Schedule"] = None,
        start_after_creation: typing.Optional[builtins.bool] = None,
        success_retention_period: typing.Optional[_Duration_070aa057] = None,
        time_to_live: typing.Optional[_Duration_070aa057] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param runtime: (experimental) Specify the runtime version to use for the canary.
        :param test: (experimental) The type of test that you want your canary to run. Use ``Test.custom()`` to specify the test to run.
        :param artifacts_bucket_location: (experimental) The s3 location that stores the data of the canary runs. Default: - A new s3 bucket will be created without a prefix.
        :param canary_name: (experimental) The name of the canary. Be sure to give it a descriptive name that distinguishes it from other canaries in your account. Do not include secrets or proprietary information in your canary name. The canary name makes up part of the canary ARN, which is included in outbound calls over the internet. Default: - A unique name will be generated from the construct ID
        :param failure_retention_period: (experimental) How many days should failed runs be retained. Default: Duration.days(31)
        :param role: (experimental) Canary execution role. This is the role that will be assumed by the canary upon execution. It controls the permissions that the canary will have. The role must be assumable by the AWS Lambda service principal. If not supplied, a role will be created with all the required permissions. If you provide a Role, you must add the required permissions. Default: - A unique role will be generated for this canary. You can add permissions to roles by calling 'addToRolePolicy'.
        :param schedule: (experimental) Specify the schedule for how often the canary runs. For example, if you set ``schedule`` to ``rate(10 minutes)``, then the canary will run every 10 minutes. You can set the schedule with ``Schedule.rate(Duration)`` (recommended) or you can specify an expression using ``Schedule.expression()``. Default: 'rate(5 minutes)'
        :param start_after_creation: (experimental) Whether or not the canary should start after creation. Default: true
        :param success_retention_period: (experimental) How many days should successful runs be retained. Default: Duration.days(31)
        :param time_to_live: (experimental) How long the canary will be in a 'RUNNING' state. For example, if you set ``timeToLive`` to be 1 hour and ``schedule`` to be ``rate(10 minutes)``, your canary will run at 10 minute intervals for an hour, for a total of 6 times. Default: - no limit

        :stability: experimental
        '''
        props = CanaryProps(
            runtime=runtime,
            test=test,
            artifacts_bucket_location=artifacts_bucket_location,
            canary_name=canary_name,
            failure_retention_period=failure_retention_period,
            role=role,
            schedule=schedule,
            start_after_creation=start_after_creation,
            success_retention_period=success_retention_period,
            time_to_live=time_to_live,
        )

        jsii.create(Canary, self, [scope, id, props])

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Measure the Duration of a single canary run, in seconds.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: avg over 5 minutes

        :stability: experimental
        '''
        options = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricDuration", [options]))

    @jsii.member(jsii_name="metricFailed")
    def metric_failed(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Measure the number of failed canary runs over a given time period.

        Default: sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        options = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricFailed", [options]))

    @jsii.member(jsii_name="metricSuccessPercent")
    def metric_success_percent(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Measure the percentage of successful canary runs.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: avg over 5 minutes

        :stability: experimental
        '''
        options = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSuccessPercent", [options]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="artifactsBucket")
    def artifacts_bucket(self) -> _IBucket_73486e29:
        '''(experimental) Bucket where data from each canary run is stored.

        :stability: experimental
        '''
        return typing.cast(_IBucket_73486e29, jsii.get(self, "artifactsBucket"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="canaryId")
    def canary_id(self) -> builtins.str:
        '''(experimental) The canary ID.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "canaryId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="canaryName")
    def canary_name(self) -> builtins.str:
        '''(experimental) The canary Name.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "canaryName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="canaryState")
    def canary_state(self) -> builtins.str:
        '''(experimental) The state of the canary.

        For example, 'RUNNING', 'STOPPED', 'NOT STARTED', or 'ERROR'.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "canaryState"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="role")
    def role(self) -> _IRole_59af6f50:
        '''(experimental) Execution role associated with this Canary.

        :stability: experimental
        '''
        return typing.cast(_IRole_59af6f50, jsii.get(self, "role"))


@jsii.data_type(
    jsii_type="monocdk.aws_synthetics.CanaryProps",
    jsii_struct_bases=[],
    name_mapping={
        "runtime": "runtime",
        "test": "test",
        "artifacts_bucket_location": "artifactsBucketLocation",
        "canary_name": "canaryName",
        "failure_retention_period": "failureRetentionPeriod",
        "role": "role",
        "schedule": "schedule",
        "start_after_creation": "startAfterCreation",
        "success_retention_period": "successRetentionPeriod",
        "time_to_live": "timeToLive",
    },
)
class CanaryProps:
    def __init__(
        self,
        *,
        runtime: "Runtime",
        test: "Test",
        artifacts_bucket_location: typing.Optional[ArtifactsBucketLocation] = None,
        canary_name: typing.Optional[builtins.str] = None,
        failure_retention_period: typing.Optional[_Duration_070aa057] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        schedule: typing.Optional["Schedule"] = None,
        start_after_creation: typing.Optional[builtins.bool] = None,
        success_retention_period: typing.Optional[_Duration_070aa057] = None,
        time_to_live: typing.Optional[_Duration_070aa057] = None,
    ) -> None:
        '''(experimental) Properties for a canary.

        :param runtime: (experimental) Specify the runtime version to use for the canary.
        :param test: (experimental) The type of test that you want your canary to run. Use ``Test.custom()`` to specify the test to run.
        :param artifacts_bucket_location: (experimental) The s3 location that stores the data of the canary runs. Default: - A new s3 bucket will be created without a prefix.
        :param canary_name: (experimental) The name of the canary. Be sure to give it a descriptive name that distinguishes it from other canaries in your account. Do not include secrets or proprietary information in your canary name. The canary name makes up part of the canary ARN, which is included in outbound calls over the internet. Default: - A unique name will be generated from the construct ID
        :param failure_retention_period: (experimental) How many days should failed runs be retained. Default: Duration.days(31)
        :param role: (experimental) Canary execution role. This is the role that will be assumed by the canary upon execution. It controls the permissions that the canary will have. The role must be assumable by the AWS Lambda service principal. If not supplied, a role will be created with all the required permissions. If you provide a Role, you must add the required permissions. Default: - A unique role will be generated for this canary. You can add permissions to roles by calling 'addToRolePolicy'.
        :param schedule: (experimental) Specify the schedule for how often the canary runs. For example, if you set ``schedule`` to ``rate(10 minutes)``, then the canary will run every 10 minutes. You can set the schedule with ``Schedule.rate(Duration)`` (recommended) or you can specify an expression using ``Schedule.expression()``. Default: 'rate(5 minutes)'
        :param start_after_creation: (experimental) Whether or not the canary should start after creation. Default: true
        :param success_retention_period: (experimental) How many days should successful runs be retained. Default: Duration.days(31)
        :param time_to_live: (experimental) How long the canary will be in a 'RUNNING' state. For example, if you set ``timeToLive`` to be 1 hour and ``schedule`` to be ``rate(10 minutes)``, your canary will run at 10 minute intervals for an hour, for a total of 6 times. Default: - no limit

        :stability: experimental
        '''
        if isinstance(artifacts_bucket_location, dict):
            artifacts_bucket_location = ArtifactsBucketLocation(**artifacts_bucket_location)
        self._values: typing.Dict[str, typing.Any] = {
            "runtime": runtime,
            "test": test,
        }
        if artifacts_bucket_location is not None:
            self._values["artifacts_bucket_location"] = artifacts_bucket_location
        if canary_name is not None:
            self._values["canary_name"] = canary_name
        if failure_retention_period is not None:
            self._values["failure_retention_period"] = failure_retention_period
        if role is not None:
            self._values["role"] = role
        if schedule is not None:
            self._values["schedule"] = schedule
        if start_after_creation is not None:
            self._values["start_after_creation"] = start_after_creation
        if success_retention_period is not None:
            self._values["success_retention_period"] = success_retention_period
        if time_to_live is not None:
            self._values["time_to_live"] = time_to_live

    @builtins.property
    def runtime(self) -> "Runtime":
        '''(experimental) Specify the runtime version to use for the canary.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_Library.html
        :stability: experimental
        '''
        result = self._values.get("runtime")
        assert result is not None, "Required property 'runtime' is missing"
        return typing.cast("Runtime", result)

    @builtins.property
    def test(self) -> "Test":
        '''(experimental) The type of test that you want your canary to run.

        Use ``Test.custom()`` to specify the test to run.

        :stability: experimental
        '''
        result = self._values.get("test")
        assert result is not None, "Required property 'test' is missing"
        return typing.cast("Test", result)

    @builtins.property
    def artifacts_bucket_location(self) -> typing.Optional[ArtifactsBucketLocation]:
        '''(experimental) The s3 location that stores the data of the canary runs.

        :default: - A new s3 bucket will be created without a prefix.

        :stability: experimental
        '''
        result = self._values.get("artifacts_bucket_location")
        return typing.cast(typing.Optional[ArtifactsBucketLocation], result)

    @builtins.property
    def canary_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the canary.

        Be sure to give it a descriptive name that distinguishes it from
        other canaries in your account.

        Do not include secrets or proprietary information in your canary name. The canary name
        makes up part of the canary ARN, which is included in outbound calls over the internet.

        :default: - A unique name will be generated from the construct ID

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/servicelens_canaries_security.html
        :stability: experimental
        '''
        result = self._values.get("canary_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failure_retention_period(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) How many days should failed runs be retained.

        :default: Duration.days(31)

        :stability: experimental
        '''
        result = self._values.get("failure_retention_period")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) Canary execution role.

        This is the role that will be assumed by the canary upon execution.
        It controls the permissions that the canary will have. The role must
        be assumable by the AWS Lambda service principal.

        If not supplied, a role will be created with all the required permissions.
        If you provide a Role, you must add the required permissions.

        :default:

        - A unique role will be generated for this canary.
        You can add permissions to roles by calling 'addToRolePolicy'.

        :see: required permissions: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-executionrolearn
        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def schedule(self) -> typing.Optional["Schedule"]:
        '''(experimental) Specify the schedule for how often the canary runs.

        For example, if you set ``schedule`` to ``rate(10 minutes)``, then the canary will run every 10 minutes.
        You can set the schedule with ``Schedule.rate(Duration)`` (recommended) or you can specify an expression using ``Schedule.expression()``.

        :default: 'rate(5 minutes)'

        :stability: experimental
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["Schedule"], result)

    @builtins.property
    def start_after_creation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not the canary should start after creation.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("start_after_creation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def success_retention_period(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) How many days should successful runs be retained.

        :default: Duration.days(31)

        :stability: experimental
        '''
        result = self._values.get("success_retention_period")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def time_to_live(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) How long the canary will be in a 'RUNNING' state.

        For example, if you set ``timeToLive`` to be 1 hour and ``schedule`` to be ``rate(10 minutes)``,
        your canary will run at 10 minute intervals for an hour, for a total of 6 times.

        :default: - no limit

        :stability: experimental
        '''
        result = self._values.get("time_to_live")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CanaryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnCanary(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_synthetics.CfnCanary",
):
    '''A CloudFormation ``AWS::Synthetics::Canary``.

    :cloudformationResource: AWS::Synthetics::Canary
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        artifact_s3_location: builtins.str,
        code: typing.Union["CfnCanary.CodeProperty", _IResolvable_a771d0ef],
        execution_role_arn: builtins.str,
        name: builtins.str,
        runtime_version: builtins.str,
        schedule: typing.Union["CfnCanary.ScheduleProperty", _IResolvable_a771d0ef],
        start_canary_after_creation: typing.Union[builtins.bool, _IResolvable_a771d0ef],
        failure_retention_period: typing.Optional[jsii.Number] = None,
        run_config: typing.Optional[typing.Union["CfnCanary.RunConfigProperty", _IResolvable_a771d0ef]] = None,
        success_retention_period: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
        vpc_config: typing.Optional[typing.Union["CfnCanary.VPCConfigProperty", _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::Synthetics::Canary``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param artifact_s3_location: ``AWS::Synthetics::Canary.ArtifactS3Location``.
        :param code: ``AWS::Synthetics::Canary.Code``.
        :param execution_role_arn: ``AWS::Synthetics::Canary.ExecutionRoleArn``.
        :param name: ``AWS::Synthetics::Canary.Name``.
        :param runtime_version: ``AWS::Synthetics::Canary.RuntimeVersion``.
        :param schedule: ``AWS::Synthetics::Canary.Schedule``.
        :param start_canary_after_creation: ``AWS::Synthetics::Canary.StartCanaryAfterCreation``.
        :param failure_retention_period: ``AWS::Synthetics::Canary.FailureRetentionPeriod``.
        :param run_config: ``AWS::Synthetics::Canary.RunConfig``.
        :param success_retention_period: ``AWS::Synthetics::Canary.SuccessRetentionPeriod``.
        :param tags: ``AWS::Synthetics::Canary.Tags``.
        :param vpc_config: ``AWS::Synthetics::Canary.VPCConfig``.
        '''
        props = CfnCanaryProps(
            artifact_s3_location=artifact_s3_location,
            code=code,
            execution_role_arn=execution_role_arn,
            name=name,
            runtime_version=runtime_version,
            schedule=schedule,
            start_canary_after_creation=start_canary_after_creation,
            failure_retention_period=failure_retention_period,
            run_config=run_config,
            success_retention_period=success_retention_period,
            tags=tags,
            vpc_config=vpc_config,
        )

        jsii.create(CfnCanary, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''
        :cloudformationAttribute: State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::Synthetics::Canary.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="artifactS3Location")
    def artifact_s3_location(self) -> builtins.str:
        '''``AWS::Synthetics::Canary.ArtifactS3Location``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-artifacts3location
        '''
        return typing.cast(builtins.str, jsii.get(self, "artifactS3Location"))

    @artifact_s3_location.setter
    def artifact_s3_location(self, value: builtins.str) -> None:
        jsii.set(self, "artifactS3Location", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="code")
    def code(self) -> typing.Union["CfnCanary.CodeProperty", _IResolvable_a771d0ef]:
        '''``AWS::Synthetics::Canary.Code``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-code
        '''
        return typing.cast(typing.Union["CfnCanary.CodeProperty", _IResolvable_a771d0ef], jsii.get(self, "code"))

    @code.setter
    def code(
        self,
        value: typing.Union["CfnCanary.CodeProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "code", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> builtins.str:
        '''``AWS::Synthetics::Canary.ExecutionRoleArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-executionrolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "executionRoleArn"))

    @execution_role_arn.setter
    def execution_role_arn(self, value: builtins.str) -> None:
        jsii.set(self, "executionRoleArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''``AWS::Synthetics::Canary.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        '''``AWS::Synthetics::Canary.RuntimeVersion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-runtimeversion
        '''
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @runtime_version.setter
    def runtime_version(self, value: builtins.str) -> None:
        jsii.set(self, "runtimeVersion", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="schedule")
    def schedule(
        self,
    ) -> typing.Union["CfnCanary.ScheduleProperty", _IResolvable_a771d0ef]:
        '''``AWS::Synthetics::Canary.Schedule``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-schedule
        '''
        return typing.cast(typing.Union["CfnCanary.ScheduleProperty", _IResolvable_a771d0ef], jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(
        self,
        value: typing.Union["CfnCanary.ScheduleProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "schedule", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="startCanaryAfterCreation")
    def start_canary_after_creation(
        self,
    ) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
        '''``AWS::Synthetics::Canary.StartCanaryAfterCreation``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-startcanaryaftercreation
        '''
        return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], jsii.get(self, "startCanaryAfterCreation"))

    @start_canary_after_creation.setter
    def start_canary_after_creation(
        self,
        value: typing.Union[builtins.bool, _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "startCanaryAfterCreation", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="failureRetentionPeriod")
    def failure_retention_period(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Synthetics::Canary.FailureRetentionPeriod``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-failureretentionperiod
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureRetentionPeriod"))

    @failure_retention_period.setter
    def failure_retention_period(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "failureRetentionPeriod", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="runConfig")
    def run_config(
        self,
    ) -> typing.Optional[typing.Union["CfnCanary.RunConfigProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Synthetics::Canary.RunConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-runconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnCanary.RunConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "runConfig"))

    @run_config.setter
    def run_config(
        self,
        value: typing.Optional[typing.Union["CfnCanary.RunConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "runConfig", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="successRetentionPeriod")
    def success_retention_period(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Synthetics::Canary.SuccessRetentionPeriod``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-successretentionperiod
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "successRetentionPeriod"))

    @success_retention_period.setter
    def success_retention_period(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "successRetentionPeriod", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union["CfnCanary.VPCConfigProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Synthetics::Canary.VPCConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-vpcconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnCanary.VPCConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "vpcConfig"))

    @vpc_config.setter
    def vpc_config(
        self,
        value: typing.Optional[typing.Union["CfnCanary.VPCConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "vpcConfig", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_synthetics.CfnCanary.CodeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "handler": "handler",
            "s3_bucket": "s3Bucket",
            "s3_key": "s3Key",
            "s3_object_version": "s3ObjectVersion",
            "script": "script",
        },
    )
    class CodeProperty:
        def __init__(
            self,
            *,
            handler: builtins.str,
            s3_bucket: typing.Optional[builtins.str] = None,
            s3_key: typing.Optional[builtins.str] = None,
            s3_object_version: typing.Optional[builtins.str] = None,
            script: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param handler: ``CfnCanary.CodeProperty.Handler``.
            :param s3_bucket: ``CfnCanary.CodeProperty.S3Bucket``.
            :param s3_key: ``CfnCanary.CodeProperty.S3Key``.
            :param s3_object_version: ``CfnCanary.CodeProperty.S3ObjectVersion``.
            :param script: ``CfnCanary.CodeProperty.Script``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "handler": handler,
            }
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket
            if s3_key is not None:
                self._values["s3_key"] = s3_key
            if s3_object_version is not None:
                self._values["s3_object_version"] = s3_object_version
            if script is not None:
                self._values["script"] = script

        @builtins.property
        def handler(self) -> builtins.str:
            '''``CfnCanary.CodeProperty.Handler``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-handler
            '''
            result = self._values.get("handler")
            assert result is not None, "Required property 'handler' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_bucket(self) -> typing.Optional[builtins.str]:
            '''``CfnCanary.CodeProperty.S3Bucket``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_key(self) -> typing.Optional[builtins.str]:
            '''``CfnCanary.CodeProperty.S3Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-s3key
            '''
            result = self._values.get("s3_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_object_version(self) -> typing.Optional[builtins.str]:
            '''``CfnCanary.CodeProperty.S3ObjectVersion``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-s3objectversion
            '''
            result = self._values.get("s3_object_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def script(self) -> typing.Optional[builtins.str]:
            '''``CfnCanary.CodeProperty.Script``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-script
            '''
            result = self._values.get("script")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_synthetics.CfnCanary.RunConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "active_tracing": "activeTracing",
            "environment_variables": "environmentVariables",
            "memory_in_mb": "memoryInMb",
            "timeout_in_seconds": "timeoutInSeconds",
        },
    )
    class RunConfigProperty:
        def __init__(
            self,
            *,
            active_tracing: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            environment_variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
            memory_in_mb: typing.Optional[jsii.Number] = None,
            timeout_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param active_tracing: ``CfnCanary.RunConfigProperty.ActiveTracing``.
            :param environment_variables: ``CfnCanary.RunConfigProperty.EnvironmentVariables``.
            :param memory_in_mb: ``CfnCanary.RunConfigProperty.MemoryInMB``.
            :param timeout_in_seconds: ``CfnCanary.RunConfigProperty.TimeoutInSeconds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-runconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if active_tracing is not None:
                self._values["active_tracing"] = active_tracing
            if environment_variables is not None:
                self._values["environment_variables"] = environment_variables
            if memory_in_mb is not None:
                self._values["memory_in_mb"] = memory_in_mb
            if timeout_in_seconds is not None:
                self._values["timeout_in_seconds"] = timeout_in_seconds

        @builtins.property
        def active_tracing(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnCanary.RunConfigProperty.ActiveTracing``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-runconfig.html#cfn-synthetics-canary-runconfig-activetracing
            '''
            result = self._values.get("active_tracing")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def environment_variables(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
            '''``CfnCanary.RunConfigProperty.EnvironmentVariables``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-runconfig.html#cfn-synthetics-canary-runconfig-environmentvariables
            '''
            result = self._values.get("environment_variables")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def memory_in_mb(self) -> typing.Optional[jsii.Number]:
            '''``CfnCanary.RunConfigProperty.MemoryInMB``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-runconfig.html#cfn-synthetics-canary-runconfig-memoryinmb
            '''
            result = self._values.get("memory_in_mb")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''``CfnCanary.RunConfigProperty.TimeoutInSeconds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-runconfig.html#cfn-synthetics-canary-runconfig-timeoutinseconds
            '''
            result = self._values.get("timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RunConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_synthetics.CfnCanary.ScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "expression": "expression",
            "duration_in_seconds": "durationInSeconds",
        },
    )
    class ScheduleProperty:
        def __init__(
            self,
            *,
            expression: builtins.str,
            duration_in_seconds: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param expression: ``CfnCanary.ScheduleProperty.Expression``.
            :param duration_in_seconds: ``CfnCanary.ScheduleProperty.DurationInSeconds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-schedule.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "expression": expression,
            }
            if duration_in_seconds is not None:
                self._values["duration_in_seconds"] = duration_in_seconds

        @builtins.property
        def expression(self) -> builtins.str:
            '''``CfnCanary.ScheduleProperty.Expression``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-schedule.html#cfn-synthetics-canary-schedule-expression
            '''
            result = self._values.get("expression")
            assert result is not None, "Required property 'expression' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def duration_in_seconds(self) -> typing.Optional[builtins.str]:
            '''``CfnCanary.ScheduleProperty.DurationInSeconds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-schedule.html#cfn-synthetics-canary-schedule-durationinseconds
            '''
            result = self._values.get("duration_in_seconds")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_synthetics.CfnCanary.VPCConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
            "vpc_id": "vpcId",
        },
    )
    class VPCConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.List[builtins.str],
            subnet_ids: typing.List[builtins.str],
            vpc_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param security_group_ids: ``CfnCanary.VPCConfigProperty.SecurityGroupIds``.
            :param subnet_ids: ``CfnCanary.VPCConfigProperty.SubnetIds``.
            :param vpc_id: ``CfnCanary.VPCConfigProperty.VpcId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-vpcconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "security_group_ids": security_group_ids,
                "subnet_ids": subnet_ids,
            }
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def security_group_ids(self) -> typing.List[builtins.str]:
            '''``CfnCanary.VPCConfigProperty.SecurityGroupIds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-vpcconfig.html#cfn-synthetics-canary-vpcconfig-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            assert result is not None, "Required property 'security_group_ids' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def subnet_ids(self) -> typing.List[builtins.str]:
            '''``CfnCanary.VPCConfigProperty.SubnetIds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-vpcconfig.html#cfn-synthetics-canary-vpcconfig-subnetids
            '''
            result = self._values.get("subnet_ids")
            assert result is not None, "Required property 'subnet_ids' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''``CfnCanary.VPCConfigProperty.VpcId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-vpcconfig.html#cfn-synthetics-canary-vpcconfig-vpcid
            '''
            result = self._values.get("vpc_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VPCConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_synthetics.CfnCanaryProps",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_s3_location": "artifactS3Location",
        "code": "code",
        "execution_role_arn": "executionRoleArn",
        "name": "name",
        "runtime_version": "runtimeVersion",
        "schedule": "schedule",
        "start_canary_after_creation": "startCanaryAfterCreation",
        "failure_retention_period": "failureRetentionPeriod",
        "run_config": "runConfig",
        "success_retention_period": "successRetentionPeriod",
        "tags": "tags",
        "vpc_config": "vpcConfig",
    },
)
class CfnCanaryProps:
    def __init__(
        self,
        *,
        artifact_s3_location: builtins.str,
        code: typing.Union[CfnCanary.CodeProperty, _IResolvable_a771d0ef],
        execution_role_arn: builtins.str,
        name: builtins.str,
        runtime_version: builtins.str,
        schedule: typing.Union[CfnCanary.ScheduleProperty, _IResolvable_a771d0ef],
        start_canary_after_creation: typing.Union[builtins.bool, _IResolvable_a771d0ef],
        failure_retention_period: typing.Optional[jsii.Number] = None,
        run_config: typing.Optional[typing.Union[CfnCanary.RunConfigProperty, _IResolvable_a771d0ef]] = None,
        success_retention_period: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
        vpc_config: typing.Optional[typing.Union[CfnCanary.VPCConfigProperty, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Synthetics::Canary``.

        :param artifact_s3_location: ``AWS::Synthetics::Canary.ArtifactS3Location``.
        :param code: ``AWS::Synthetics::Canary.Code``.
        :param execution_role_arn: ``AWS::Synthetics::Canary.ExecutionRoleArn``.
        :param name: ``AWS::Synthetics::Canary.Name``.
        :param runtime_version: ``AWS::Synthetics::Canary.RuntimeVersion``.
        :param schedule: ``AWS::Synthetics::Canary.Schedule``.
        :param start_canary_after_creation: ``AWS::Synthetics::Canary.StartCanaryAfterCreation``.
        :param failure_retention_period: ``AWS::Synthetics::Canary.FailureRetentionPeriod``.
        :param run_config: ``AWS::Synthetics::Canary.RunConfig``.
        :param success_retention_period: ``AWS::Synthetics::Canary.SuccessRetentionPeriod``.
        :param tags: ``AWS::Synthetics::Canary.Tags``.
        :param vpc_config: ``AWS::Synthetics::Canary.VPCConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "artifact_s3_location": artifact_s3_location,
            "code": code,
            "execution_role_arn": execution_role_arn,
            "name": name,
            "runtime_version": runtime_version,
            "schedule": schedule,
            "start_canary_after_creation": start_canary_after_creation,
        }
        if failure_retention_period is not None:
            self._values["failure_retention_period"] = failure_retention_period
        if run_config is not None:
            self._values["run_config"] = run_config
        if success_retention_period is not None:
            self._values["success_retention_period"] = success_retention_period
        if tags is not None:
            self._values["tags"] = tags
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def artifact_s3_location(self) -> builtins.str:
        '''``AWS::Synthetics::Canary.ArtifactS3Location``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-artifacts3location
        '''
        result = self._values.get("artifact_s3_location")
        assert result is not None, "Required property 'artifact_s3_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def code(self) -> typing.Union[CfnCanary.CodeProperty, _IResolvable_a771d0ef]:
        '''``AWS::Synthetics::Canary.Code``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-code
        '''
        result = self._values.get("code")
        assert result is not None, "Required property 'code' is missing"
        return typing.cast(typing.Union[CfnCanary.CodeProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def execution_role_arn(self) -> builtins.str:
        '''``AWS::Synthetics::Canary.ExecutionRoleArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-executionrolearn
        '''
        result = self._values.get("execution_role_arn")
        assert result is not None, "Required property 'execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''``AWS::Synthetics::Canary.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runtime_version(self) -> builtins.str:
        '''``AWS::Synthetics::Canary.RuntimeVersion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-runtimeversion
        '''
        result = self._values.get("runtime_version")
        assert result is not None, "Required property 'runtime_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Union[CfnCanary.ScheduleProperty, _IResolvable_a771d0ef]:
        '''``AWS::Synthetics::Canary.Schedule``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-schedule
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(typing.Union[CfnCanary.ScheduleProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def start_canary_after_creation(
        self,
    ) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
        '''``AWS::Synthetics::Canary.StartCanaryAfterCreation``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-startcanaryaftercreation
        '''
        result = self._values.get("start_canary_after_creation")
        assert result is not None, "Required property 'start_canary_after_creation' is missing"
        return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

    @builtins.property
    def failure_retention_period(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Synthetics::Canary.FailureRetentionPeriod``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-failureretentionperiod
        '''
        result = self._values.get("failure_retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def run_config(
        self,
    ) -> typing.Optional[typing.Union[CfnCanary.RunConfigProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Synthetics::Canary.RunConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-runconfig
        '''
        result = self._values.get("run_config")
        return typing.cast(typing.Optional[typing.Union[CfnCanary.RunConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def success_retention_period(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Synthetics::Canary.SuccessRetentionPeriod``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-successretentionperiod
        '''
        result = self._values.get("success_retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::Synthetics::Canary.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union[CfnCanary.VPCConfigProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Synthetics::Canary.VPCConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-vpcconfig
        '''
        result = self._values.get("vpc_config")
        return typing.cast(typing.Optional[typing.Union[CfnCanary.VPCConfigProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCanaryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Code(metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk.aws_synthetics.Code"):
    '''(experimental) The code the canary should execute.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_CodeProxy"]:
        return _CodeProxy

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(Code, self, [])

    @jsii.member(jsii_name="fromAsset") # type: ignore[misc]
    @builtins.classmethod
    def from_asset(
        cls,
        asset_path: builtins.str,
        *,
        readers: typing.Optional[typing.List[_IGrantable_4c5a91d1]] = None,
        source_hash: typing.Optional[builtins.str] = None,
        exclude: typing.Optional[typing.List[builtins.str]] = None,
        follow: typing.Optional[_FollowMode_98b05cc5] = None,
        ignore_mode: typing.Optional[_IgnoreMode_31d8bf46] = None,
        asset_hash: typing.Optional[builtins.str] = None,
        asset_hash_type: typing.Optional[_AssetHashType_49193809] = None,
        bundling: typing.Optional[_BundlingOptions_ab115a99] = None,
    ) -> "AssetCode":
        '''(experimental) Specify code from a local path.

        Path must include the folder structure ``nodejs/node_modules/myCanaryFilename.js``.

        :param asset_path: Either a directory or a .zip file.
        :param readers: (experimental) A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_hash: (deprecated) Custom hash to use when identifying the specific version of the asset. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the source hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the source hash, you will need to make sure it is updated every time the source changes, or otherwise it is possible that some deployments will not be invalidated. Default: - automatically calculate source hash based on the contents of the source file or directory.
        :param exclude: (deprecated) Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: (deprecated) The ignore behavior to use for exclude patterns. Default: - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the '
        :param asset_hash: (experimental) Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: (experimental) Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: (experimental) Bundle the asset by executing a command in a Docker container. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise

        :return: ``AssetCode`` associated with the specified path.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_WritingCanary.html#CloudWatch_Synthetics_Canaries_write_from_scratch
        :stability: experimental
        '''
        options = _AssetOptions_bd2996da(
            readers=readers,
            source_hash=source_hash,
            exclude=exclude,
            follow=follow,
            ignore_mode=ignore_mode,
            asset_hash=asset_hash,
            asset_hash_type=asset_hash_type,
            bundling=bundling,
        )

        return typing.cast("AssetCode", jsii.sinvoke(cls, "fromAsset", [asset_path, options]))

    @jsii.member(jsii_name="fromBucket") # type: ignore[misc]
    @builtins.classmethod
    def from_bucket(
        cls,
        bucket: _IBucket_73486e29,
        key: builtins.str,
        object_version: typing.Optional[builtins.str] = None,
    ) -> "S3Code":
        '''(experimental) Specify code from an s3 bucket.

        The object in the s3 bucket must be a .zip file that contains
        the structure ``nodejs/node_modules/myCanaryFilename.js``.

        :param bucket: The S3 bucket.
        :param key: The object key.
        :param object_version: Optional S3 object version.

        :return: ``S3Code`` associated with the specified S3 object.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_WritingCanary.html#CloudWatch_Synthetics_Canaries_write_from_scratch
        :stability: experimental
        '''
        return typing.cast("S3Code", jsii.sinvoke(cls, "fromBucket", [bucket, key, object_version]))

    @jsii.member(jsii_name="fromInline") # type: ignore[misc]
    @builtins.classmethod
    def from_inline(cls, code: builtins.str) -> "InlineCode":
        '''(experimental) Specify code inline.

        :param code: The actual handler code (limited to 4KiB).

        :return: ``InlineCode`` with inline code.

        :stability: experimental
        '''
        return typing.cast("InlineCode", jsii.sinvoke(cls, "fromInline", [code]))

    @jsii.member(jsii_name="bind") # type: ignore[misc]
    @abc.abstractmethod
    def bind(self, scope: _Construct_e78e779f, handler: builtins.str) -> "CodeConfig":
        '''(experimental) Called when the canary is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: The binding scope. Don't be smart about trying to down-cast or assume it's initialized. You may just use it as a construct scope.
        :param handler: -

        :return: a bound ``CodeConfig``.

        :stability: experimental
        '''
        ...


class _CodeProxy(Code):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_e78e779f, handler: builtins.str) -> "CodeConfig":
        '''(experimental) Called when the canary is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: The binding scope. Don't be smart about trying to down-cast or assume it's initialized. You may just use it as a construct scope.
        :param handler: -

        :return: a bound ``CodeConfig``.

        :stability: experimental
        '''
        return typing.cast("CodeConfig", jsii.invoke(self, "bind", [scope, handler]))


@jsii.data_type(
    jsii_type="monocdk.aws_synthetics.CodeConfig",
    jsii_struct_bases=[],
    name_mapping={"inline_code": "inlineCode", "s3_location": "s3Location"},
)
class CodeConfig:
    def __init__(
        self,
        *,
        inline_code: typing.Optional[builtins.str] = None,
        s3_location: typing.Optional[_Location_cce991ca] = None,
    ) -> None:
        '''(experimental) Configuration of the code class.

        :param inline_code: (experimental) Inline code (mutually exclusive with ``s3Location``). Default: - none
        :param s3_location: (experimental) The location of the code in S3 (mutually exclusive with ``inlineCode``). Default: - none

        :stability: experimental
        '''
        if isinstance(s3_location, dict):
            s3_location = _Location_cce991ca(**s3_location)
        self._values: typing.Dict[str, typing.Any] = {}
        if inline_code is not None:
            self._values["inline_code"] = inline_code
        if s3_location is not None:
            self._values["s3_location"] = s3_location

    @builtins.property
    def inline_code(self) -> typing.Optional[builtins.str]:
        '''(experimental) Inline code (mutually exclusive with ``s3Location``).

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("inline_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_location(self) -> typing.Optional[_Location_cce991ca]:
        '''(experimental) The location of the code in S3 (mutually exclusive with ``inlineCode``).

        :default: - none

        :stability: experimental
        '''
        result = self._values.get("s3_location")
        return typing.cast(typing.Optional[_Location_cce991ca], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_synthetics.CustomTestOptions",
    jsii_struct_bases=[],
    name_mapping={"code": "code", "handler": "handler"},
)
class CustomTestOptions:
    def __init__(self, *, code: Code, handler: builtins.str) -> None:
        '''(experimental) Properties for specifying a test.

        :param code: (experimental) The code of the canary script.
        :param handler: (experimental) The handler for the code. Must end with ``.handler``.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "code": code,
            "handler": handler,
        }

    @builtins.property
    def code(self) -> Code:
        '''(experimental) The code of the canary script.

        :stability: experimental
        '''
        result = self._values.get("code")
        assert result is not None, "Required property 'code' is missing"
        return typing.cast(Code, result)

    @builtins.property
    def handler(self) -> builtins.str:
        '''(experimental) The handler for the code.

        Must end with ``.handler``.

        :stability: experimental
        '''
        result = self._values.get("handler")
        assert result is not None, "Required property 'handler' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomTestOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class InlineCode(
    Code,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_synthetics.InlineCode",
):
    '''(experimental) Canary code from an inline string.

    :stability: experimental
    '''

    def __init__(self, code: builtins.str) -> None:
        '''
        :param code: -

        :stability: experimental
        '''
        jsii.create(InlineCode, self, [code])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_e78e779f, handler: builtins.str) -> CodeConfig:
        '''(experimental) Called when the canary is initialized to allow this object to bind to the stack, add resources and have fun.

        :param _scope: -
        :param handler: -

        :stability: experimental
        '''
        return typing.cast(CodeConfig, jsii.invoke(self, "bind", [_scope, handler]))


class Runtime(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_synthetics.Runtime"):
    '''(experimental) Runtime options for a canary.

    :stability: experimental
    '''

    def __init__(self, name: builtins.str) -> None:
        '''
        :param name: The name of the runtime version.

        :stability: experimental
        '''
        jsii.create(Runtime, self, [name])

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="SYNTHETICS_1_0")
    def SYNTHETICS_1_0(cls) -> "Runtime":
        '''(experimental) ``syn-1.0`` includes the following:.

        - Synthetics library 1.0
        - Synthetics handler code 1.0
        - Lambda runtime Node.js 10.x
        - Puppeteer-core version 1.14.0
        - The Chromium version that matches Puppeteer-core 1.14.0

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Library_nodejs_puppeteer.html#CloudWatch_Synthetics_runtimeversion-1.0
        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "SYNTHETICS_1_0"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="SYNTHETICS_NODEJS_2_0")
    def SYNTHETICS_NODEJS_2_0(cls) -> "Runtime":
        '''(experimental) ``syn-nodejs-2.0`` includes the following: - Lambda runtime Node.js 10.x - Puppeteer-core version 3.3.0 - Chromium version 83.0.4103.0.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Library_nodejs_puppeteer.html#CloudWatch_Synthetics_runtimeversion-2.0
        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "SYNTHETICS_NODEJS_2_0"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="SYNTHETICS_NODEJS_2_1")
    def SYNTHETICS_NODEJS_2_1(cls) -> "Runtime":
        '''(experimental) ``syn-nodejs-2.1`` includes the following: - Lambda runtime Node.js 10.x - Puppeteer-core version 3.3.0 - Chromium version 83.0.4103.0.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Library_nodejs_puppeteer.html#CloudWatch_Synthetics_runtimeversion-2.1
        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "SYNTHETICS_NODEJS_2_1"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="SYNTHETICS_NODEJS_2_2")
    def SYNTHETICS_NODEJS_2_2(cls) -> "Runtime":
        '''(experimental) ``syn-nodejs-2.2`` includes the following: - Lambda runtime Node.js 10.x - Puppeteer-core version 3.3.0 - Chromium version 83.0.4103.0.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Library_nodejs_puppeteer.html#CloudWatch_Synthetics_runtimeversion-2.2
        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "SYNTHETICS_NODEJS_2_2"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="SYNTHETICS_NODEJS_PUPPETEER_3_0")
    def SYNTHETICS_NODEJS_PUPPETEER_3_0(cls) -> "Runtime":
        '''(experimental) ``syn-nodejs-puppeteer-3.0`` includes the following: - Lambda runtime Node.js 12.x - Puppeteer-core version 5.5.0 - Chromium version 88.0.4298.0.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Library_nodejs_puppeteer.html#CloudWatch_Synthetics_runtimeversion-nodejs-puppeteer-3.0
        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "SYNTHETICS_NODEJS_PUPPETEER_3_0"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of the runtime version.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


class S3Code(Code, metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_synthetics.S3Code"):
    '''(experimental) S3 bucket path to the code zip file.

    :stability: experimental
    '''

    def __init__(
        self,
        bucket: _IBucket_73486e29,
        key: builtins.str,
        object_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: -
        :param key: -
        :param object_version: -

        :stability: experimental
        '''
        jsii.create(S3Code, self, [bucket, key, object_version])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_e78e779f, _handler: builtins.str) -> CodeConfig:
        '''(experimental) Called when the canary is initialized to allow this object to bind to the stack, add resources and have fun.

        :param _scope: -
        :param _handler: -

        :stability: experimental
        '''
        return typing.cast(CodeConfig, jsii.invoke(self, "bind", [_scope, _handler]))


class Schedule(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_synthetics.Schedule"):
    '''(experimental) Schedule for canary runs.

    :stability: experimental
    '''

    @jsii.member(jsii_name="expression") # type: ignore[misc]
    @builtins.classmethod
    def expression(cls, expression: builtins.str) -> "Schedule":
        '''(experimental) Construct a schedule from a literal schedule expression.

        The expression must be in a ``rate(number units)`` format.
        For example, ``Schedule.expression('rate(10 minutes)')``

        :param expression: The expression to use.

        :stability: experimental
        '''
        return typing.cast("Schedule", jsii.sinvoke(cls, "expression", [expression]))

    @jsii.member(jsii_name="once") # type: ignore[misc]
    @builtins.classmethod
    def once(cls) -> "Schedule":
        '''(experimental) The canary will be executed once.

        :stability: experimental
        '''
        return typing.cast("Schedule", jsii.sinvoke(cls, "once", []))

    @jsii.member(jsii_name="rate") # type: ignore[misc]
    @builtins.classmethod
    def rate(cls, interval: _Duration_070aa057) -> "Schedule":
        '''(experimental) Construct a schedule from an interval.

        Allowed values: 0 (for a single run) or between 1 and 60 minutes.
        To specify a single run, you can use ``Schedule.once()``.

        :param interval: The interval at which to run the canary.

        :stability: experimental
        '''
        return typing.cast("Schedule", jsii.sinvoke(cls, "rate", [interval]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="expressionString")
    def expression_string(self) -> builtins.str:
        '''(experimental) The Schedule expression.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "expressionString"))


class Test(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_synthetics.Test"):
    '''(experimental) Specify a test that the canary should run.

    :stability: experimental
    '''

    @jsii.member(jsii_name="custom") # type: ignore[misc]
    @builtins.classmethod
    def custom(cls, *, code: Code, handler: builtins.str) -> "Test":
        '''(experimental) Specify a custom test with your own code.

        :param code: (experimental) The code of the canary script.
        :param handler: (experimental) The handler for the code. Must end with ``.handler``.

        :return: ``Test`` associated with the specified Code object

        :stability: experimental
        '''
        options = CustomTestOptions(code=code, handler=handler)

        return typing.cast("Test", jsii.sinvoke(cls, "custom", [options]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="code")
    def code(self) -> Code:
        '''(experimental) The code that the canary should run.

        :stability: experimental
        '''
        return typing.cast(Code, jsii.get(self, "code"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="handler")
    def handler(self) -> builtins.str:
        '''(experimental) The handler of the canary.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "handler"))


class AssetCode(
    Code,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_synthetics.AssetCode",
):
    '''(experimental) Canary code from an Asset.

    :stability: experimental
    '''

    def __init__(
        self,
        asset_path: builtins.str,
        *,
        readers: typing.Optional[typing.List[_IGrantable_4c5a91d1]] = None,
        source_hash: typing.Optional[builtins.str] = None,
        exclude: typing.Optional[typing.List[builtins.str]] = None,
        follow: typing.Optional[_FollowMode_98b05cc5] = None,
        ignore_mode: typing.Optional[_IgnoreMode_31d8bf46] = None,
        asset_hash: typing.Optional[builtins.str] = None,
        asset_hash_type: typing.Optional[_AssetHashType_49193809] = None,
        bundling: typing.Optional[_BundlingOptions_ab115a99] = None,
    ) -> None:
        '''
        :param asset_path: The path to the asset file or directory.
        :param readers: (experimental) A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_hash: (deprecated) Custom hash to use when identifying the specific version of the asset. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the source hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the source hash, you will need to make sure it is updated every time the source changes, or otherwise it is possible that some deployments will not be invalidated. Default: - automatically calculate source hash based on the contents of the source file or directory.
        :param exclude: (deprecated) Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: (deprecated) The ignore behavior to use for exclude patterns. Default: - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the '
        :param asset_hash: (experimental) Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: (experimental) Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: (experimental) Bundle the asset by executing a command in a Docker container. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise

        :stability: experimental
        '''
        options = _AssetOptions_bd2996da(
            readers=readers,
            source_hash=source_hash,
            exclude=exclude,
            follow=follow,
            ignore_mode=ignore_mode,
            asset_hash=asset_hash,
            asset_hash_type=asset_hash_type,
            bundling=bundling,
        )

        jsii.create(AssetCode, self, [asset_path, options])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_e78e779f, handler: builtins.str) -> CodeConfig:
        '''(experimental) Called when the canary is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: -
        :param handler: -

        :stability: experimental
        '''
        return typing.cast(CodeConfig, jsii.invoke(self, "bind", [scope, handler]))


__all__ = [
    "ArtifactsBucketLocation",
    "AssetCode",
    "Canary",
    "CanaryProps",
    "CfnCanary",
    "CfnCanaryProps",
    "Code",
    "CodeConfig",
    "CustomTestOptions",
    "InlineCode",
    "Runtime",
    "S3Code",
    "Schedule",
    "Test",
]

publication.publish()
