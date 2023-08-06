'''
# AWS CodeDeploy Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

AWS CodeDeploy is a deployment service that automates application deployments to
Amazon EC2 instances, on-premises instances, serverless Lambda functions, or
Amazon ECS services.

The CDK currently supports Amazon EC2, on-premise and AWS Lambda applications.

## EC2/on-premise Applications

To create a new CodeDeploy Application that deploys to EC2/on-premise instances:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codedeploy as codedeploy

application = codedeploy.ServerApplication(self, "CodeDeployApplication",
    application_name="MyApplication"
)
```

To import an already existing Application:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
application = codedeploy.ServerApplication.from_server_application_name(self, "ExistingCodeDeployApplication", "MyExistingApplication")
```

## EC2/on-premise Deployment Groups

To create a new CodeDeploy Deployment Group that deploys to EC2/on-premise instances:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
deployment_group = codedeploy.ServerDeploymentGroup(self, "CodeDeployDeploymentGroup",
    application=application,
    deployment_group_name="MyDeploymentGroup",
    auto_scaling_groups=[asg1, asg2],
    # adds User Data that installs the CodeDeploy agent on your auto-scaling groups hosts
    # default: true
    install_agent=True,
    # adds EC2 instances matching tags
    ec2_instance_tags=codedeploy.InstanceTagSet(
        # any instance with tags satisfying
        # key1=v1 or key1=v2 or key2 (any value) or value v3 (any key)
        # will match this group
        key1=["v1", "v2"],
        key2=[],
        =["v3"]
    ),
    # adds on-premise instances matching tags
    on_premise_instance_tags=codedeploy.InstanceTagSet({
        "key1": ["v1", "v2"]
    },
        key2=["v3"]
    ),
    # CloudWatch alarms
    alarms=[
        cloudwatch.Alarm()
    ],
    # whether to ignore failure to fetch the status of alarms from CloudWatch
    # default: false
    ignore_poll_alarms_failure=False,
    # auto-rollback configuration
    auto_rollback={
        "failed_deployment": True, # default: true
        "stopped_deployment": True, # default: false
        "deployment_in_alarm": True
    }
)
```

All properties are optional - if you don't provide an Application,
one will be automatically created.

To import an already existing Deployment Group:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
deployment_group = codedeploy.ServerDeploymentGroup.from_lambda_deployment_group_attributes(self, "ExistingCodeDeployDeploymentGroup",
    application=application,
    deployment_group_name="MyExistingDeploymentGroup"
)
```

### Load balancers

You can [specify a load balancer](https://docs.aws.amazon.com/codedeploy/latest/userguide/integrations-aws-elastic-load-balancing.html)
with the `loadBalancer` property when creating a Deployment Group.

`LoadBalancer` is an abstract class with static factory methods that allow you to create instances of it from various sources.

With Classic Elastic Load Balancer, you provide it directly:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_elasticloadbalancing as lb

elb = lb.LoadBalancer(self, "ELB")
elb.add_target()
elb.add_listener()

deployment_group = codedeploy.ServerDeploymentGroup(self, "DeploymentGroup",
    load_balancer=codedeploy.LoadBalancer.classic(elb)
)
```

With Application Load Balancer or Network Load Balancer,
you provide a Target Group as the load balancer:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_elasticloadbalancingv2 as lbv2

alb = lbv2.ApplicationLoadBalancer(self, "ALB")
listener = alb.add_listener("Listener")
target_group = listener.add_targets("Fleet")

deployment_group = codedeploy.ServerDeploymentGroup(self, "DeploymentGroup",
    load_balancer=codedeploy.LoadBalancer.application(target_group)
)
```

## Deployment Configurations

You can also pass a Deployment Configuration when creating the Deployment Group:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
deployment_group = codedeploy.ServerDeploymentGroup(self, "CodeDeployDeploymentGroup",
    deployment_config=codedeploy.ServerDeploymentConfig.ALL_AT_ONCE
)
```

The default Deployment Configuration is `ServerDeploymentConfig.ONE_AT_A_TIME`.

You can also create a custom Deployment Configuration:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
deployment_config = codedeploy.ServerDeploymentConfig(self, "DeploymentConfiguration",
    deployment_config_name="MyDeploymentConfiguration", # optional property
    # one of these is required, but both cannot be specified at the same time
    min_healthy_host_count=2,
    min_healthy_host_percentage=75
)
```

Or import an existing one:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
deployment_config = codedeploy.ServerDeploymentConfig.from_server_deployment_config_name(self, "ExistingDeploymentConfiguration", "MyExistingDeploymentConfiguration")
```

## Lambda Applications

To create a new CodeDeploy Application that deploys to a Lambda function:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codedeploy as codedeploy

application = codedeploy.LambdaApplication(self, "CodeDeployApplication",
    application_name="MyApplication"
)
```

To import an already existing Application:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
application = codedeploy.LambdaApplication.from_lambda_application_name(self, "ExistingCodeDeployApplication", "MyExistingApplication")
```

## Lambda Deployment Groups

To enable traffic shifting deployments for Lambda functions, CodeDeploy uses Lambda Aliases, which can balance incoming traffic between two different versions of your function.
Before deployment, the alias sends 100% of invokes to the version used in production.
When you publish a new version of the function to your stack, CodeDeploy will send a small percentage of traffic to the new version, monitor, and validate before shifting 100% of traffic to the new version.

To create a new CodeDeploy Deployment Group that deploys to a Lambda function:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codedeploy as codedeploy
import aws_cdk.aws_lambda as lambda_

my_application = codedeploy.LambdaApplication()
func = lambda_.Function()
version = func.add_version("1")
version1_alias = lambda_.Alias(self, "alias",
    alias_name="prod",
    version=version
)

deployment_group = codedeploy.LambdaDeploymentGroup(stack, "BlueGreenDeployment",
    application=my_application, # optional property: one will be created for you if not provided
    alias=version1_alias,
    deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10PERCENT_EVERY_1MINUTE
)
```

In order to deploy a new version of this function:

1. Increment the version, e.g. `const version = func.addVersion('2')`.
2. Re-deploy the stack (this will trigger a deployment).
3. Monitor the CodeDeploy deployment as traffic shifts between the versions.

### Create a custom Deployment Config

CodeDeploy for Lambda comes with built-in configurations for traffic shifting.
If you want to specify your own strategy,
you can do so with the CustomLambdaDeploymentConfig construct,
letting you specify precisely how fast a new function version is deployed.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
config = codedeploy.CustomLambdaDeploymentConfig(stack, "CustomConfig",
    type=codedeploy.CustomLambdaDeploymentConfigType.CANARY,
    interval=Duration.minutes(1),
    percentage=5
)
deployment_group = codedeploy.LambdaDeploymentGroup(stack, "BlueGreenDeployment",
    application=application,
    alias=alias,
    deployment_config=config
)
```

You can specify a custom name for your deployment config, but if you do you will not be able to update the interval/percentage through CDK.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
config = codedeploy.CustomLambdaDeploymentConfig(stack, "CustomConfig",
    type=codedeploy.CustomLambdaDeploymentConfigType.CANARY,
    interval=Duration.minutes(1),
    percentage=5,
    deployment_config_name="MyDeploymentConfig"
)
```

### Rollbacks and Alarms

CodeDeploy will roll back if the deployment fails. You can optionally trigger a rollback when one or more alarms are in a failed state:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
deployment_group = codedeploy.LambdaDeploymentGroup(stack, "BlueGreenDeployment",
    alias=alias,
    deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10PERCENT_EVERY_1MINUTE,
    alarms=[
        # pass some alarms when constructing the deployment group
        cloudwatch.Alarm(stack, "Errors",
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold=1,
            evaluation_periods=1,
            metric=alias.metric_errors()
        )
    ]
)

# or add alarms to an existing group
deployment_group.add_alarm(cloudwatch.Alarm(stack, "BlueGreenErrors",
    comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
    threshold=1,
    evaluation_periods=1,
    metric=blue_green_alias.metric_errors()
))
```

### Pre and Post Hooks

CodeDeploy allows you to run an arbitrary Lambda function before traffic shifting actually starts (PreTraffic Hook) and after it completes (PostTraffic Hook).
With either hook, you have the opportunity to run logic that determines whether the deployment must succeed or fail.
For example, with PreTraffic hook you could run integration tests against the newly created Lambda version (but not serving traffic). With PostTraffic hook, you could run end-to-end validation checks.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
warm_up_user_cache = lambda_.Function()
end_to_end_validation = lambda_.Function()

# pass a hook whe creating the deployment group
deployment_group = codedeploy.LambdaDeploymentGroup(stack, "BlueGreenDeployment",
    alias=alias,
    deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10PERCENT_EVERY_1MINUTE,
    pre_hook=warm_up_user_cache
)

# or configure one on an existing deployment group
deployment_group.on_post_hook(end_to_end_validation)
```

### Import an existing Deployment Group

To import an already existing Deployment Group:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
deployment_group = codedeploy.LambdaDeploymentGroup.import(self, "ExistingCodeDeployDeploymentGroup",
    application=application,
    deployment_group_name="MyExistingDeploymentGroup"
)
```
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
    CfnResource as _CfnResource_e0a482dc,
    Construct as _Construct_e78e779f,
    Duration as _Duration_070aa057,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    Resource as _Resource_abff4495,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_autoscaling import (
    AutoScalingGroup as _AutoScalingGroup_604a934f,
    IAutoScalingGroup as _IAutoScalingGroup_352723c6,
)
from ..aws_cloudwatch import IAlarm as _IAlarm_bf66c8d0
from ..aws_elasticloadbalancing import LoadBalancer as _LoadBalancer_a7de240f
from ..aws_elasticloadbalancingv2 import (
    ApplicationTargetGroup as _ApplicationTargetGroup_5b334416,
    NetworkTargetGroup as _NetworkTargetGroup_cfe3bed6,
)
from ..aws_iam import (
    Grant as _Grant_bcb5eae7,
    IGrantable as _IGrantable_4c5a91d1,
    IRole as _IRole_59af6f50,
)
from ..aws_lambda import Alias as _Alias_9e39972c, IFunction as _IFunction_6e14f09e


@jsii.data_type(
    jsii_type="monocdk.aws_codedeploy.AutoRollbackConfig",
    jsii_struct_bases=[],
    name_mapping={
        "deployment_in_alarm": "deploymentInAlarm",
        "failed_deployment": "failedDeployment",
        "stopped_deployment": "stoppedDeployment",
    },
)
class AutoRollbackConfig:
    def __init__(
        self,
        *,
        deployment_in_alarm: typing.Optional[builtins.bool] = None,
        failed_deployment: typing.Optional[builtins.bool] = None,
        stopped_deployment: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) The configuration for automatically rolling back deployments in a given Deployment Group.

        :param deployment_in_alarm: (experimental) Whether to automatically roll back a deployment during which one of the configured CloudWatch alarms for this Deployment Group went off. Default: true if you've provided any Alarms with the ``alarms`` property, false otherwise
        :param failed_deployment: (experimental) Whether to automatically roll back a deployment that fails. Default: true
        :param stopped_deployment: (experimental) Whether to automatically roll back a deployment that was manually stopped. Default: false

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if deployment_in_alarm is not None:
            self._values["deployment_in_alarm"] = deployment_in_alarm
        if failed_deployment is not None:
            self._values["failed_deployment"] = failed_deployment
        if stopped_deployment is not None:
            self._values["stopped_deployment"] = stopped_deployment

    @builtins.property
    def deployment_in_alarm(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to automatically roll back a deployment during which one of the configured CloudWatch alarms for this Deployment Group went off.

        :default: true if you've provided any Alarms with the ``alarms`` property, false otherwise

        :stability: experimental
        '''
        result = self._values.get("deployment_in_alarm")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def failed_deployment(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to automatically roll back a deployment that fails.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("failed_deployment")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stopped_deployment(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to automatically roll back a deployment that was manually stopped.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("stopped_deployment")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutoRollbackConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnApplication(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codedeploy.CfnApplication",
):
    '''A CloudFormation ``AWS::CodeDeploy::Application``.

    :cloudformationResource: AWS::CodeDeploy::Application
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_name: typing.Optional[builtins.str] = None,
        compute_platform: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::CodeDeploy::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_name: ``AWS::CodeDeploy::Application.ApplicationName``.
        :param compute_platform: ``AWS::CodeDeploy::Application.ComputePlatform``.
        '''
        props = CfnApplicationProps(
            application_name=application_name, compute_platform=compute_platform
        )

        jsii.create(CfnApplication, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::CodeDeploy::Application.ApplicationName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html#cfn-codedeploy-application-applicationname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationName"))

    @application_name.setter
    def application_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "applicationName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="computePlatform")
    def compute_platform(self) -> typing.Optional[builtins.str]:
        '''``AWS::CodeDeploy::Application.ComputePlatform``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html#cfn-codedeploy-application-computeplatform
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computePlatform"))

    @compute_platform.setter
    def compute_platform(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "computePlatform", value)


@jsii.data_type(
    jsii_type="monocdk.aws_codedeploy.CfnApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "compute_platform": "computePlatform",
    },
)
class CfnApplicationProps:
    def __init__(
        self,
        *,
        application_name: typing.Optional[builtins.str] = None,
        compute_platform: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::CodeDeploy::Application``.

        :param application_name: ``AWS::CodeDeploy::Application.ApplicationName``.
        :param compute_platform: ``AWS::CodeDeploy::Application.ComputePlatform``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if application_name is not None:
            self._values["application_name"] = application_name
        if compute_platform is not None:
            self._values["compute_platform"] = compute_platform

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::CodeDeploy::Application.ApplicationName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html#cfn-codedeploy-application-applicationname
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_platform(self) -> typing.Optional[builtins.str]:
        '''``AWS::CodeDeploy::Application.ComputePlatform``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html#cfn-codedeploy-application-computeplatform
        '''
        result = self._values.get("compute_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnDeploymentConfig(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codedeploy.CfnDeploymentConfig",
):
    '''A CloudFormation ``AWS::CodeDeploy::DeploymentConfig``.

    :cloudformationResource: AWS::CodeDeploy::DeploymentConfig
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        deployment_config_name: typing.Optional[builtins.str] = None,
        minimum_healthy_hosts: typing.Optional[typing.Union["CfnDeploymentConfig.MinimumHealthyHostsProperty", _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::CodeDeploy::DeploymentConfig``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param deployment_config_name: ``AWS::CodeDeploy::DeploymentConfig.DeploymentConfigName``.
        :param minimum_healthy_hosts: ``AWS::CodeDeploy::DeploymentConfig.MinimumHealthyHosts``.
        '''
        props = CfnDeploymentConfigProps(
            deployment_config_name=deployment_config_name,
            minimum_healthy_hosts=minimum_healthy_hosts,
        )

        jsii.create(CfnDeploymentConfig, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::CodeDeploy::DeploymentConfig.DeploymentConfigName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-deploymentconfigname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentConfigName"))

    @deployment_config_name.setter
    def deployment_config_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "deploymentConfigName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="minimumHealthyHosts")
    def minimum_healthy_hosts(
        self,
    ) -> typing.Optional[typing.Union["CfnDeploymentConfig.MinimumHealthyHostsProperty", _IResolvable_a771d0ef]]:
        '''``AWS::CodeDeploy::DeploymentConfig.MinimumHealthyHosts``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-minimumhealthyhosts
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDeploymentConfig.MinimumHealthyHostsProperty", _IResolvable_a771d0ef]], jsii.get(self, "minimumHealthyHosts"))

    @minimum_healthy_hosts.setter
    def minimum_healthy_hosts(
        self,
        value: typing.Optional[typing.Union["CfnDeploymentConfig.MinimumHealthyHostsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "minimumHealthyHosts", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_codedeploy.CfnDeploymentConfig.MinimumHealthyHostsProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class MinimumHealthyHostsProperty:
        def __init__(self, *, type: builtins.str, value: jsii.Number) -> None:
            '''
            :param type: ``CfnDeploymentConfig.MinimumHealthyHostsProperty.Type``.
            :param value: ``CfnDeploymentConfig.MinimumHealthyHostsProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-minimumhealthyhosts.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "type": type,
                "value": value,
            }

        @builtins.property
        def type(self) -> builtins.str:
            '''``CfnDeploymentConfig.MinimumHealthyHostsProperty.Type``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-minimumhealthyhosts.html#cfn-codedeploy-deploymentconfig-minimumhealthyhosts-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> jsii.Number:
            '''``CfnDeploymentConfig.MinimumHealthyHostsProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-minimumhealthyhosts.html#cfn-codedeploy-deploymentconfig-minimumhealthyhosts-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MinimumHealthyHostsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_codedeploy.CfnDeploymentConfigProps",
    jsii_struct_bases=[],
    name_mapping={
        "deployment_config_name": "deploymentConfigName",
        "minimum_healthy_hosts": "minimumHealthyHosts",
    },
)
class CfnDeploymentConfigProps:
    def __init__(
        self,
        *,
        deployment_config_name: typing.Optional[builtins.str] = None,
        minimum_healthy_hosts: typing.Optional[typing.Union[CfnDeploymentConfig.MinimumHealthyHostsProperty, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::CodeDeploy::DeploymentConfig``.

        :param deployment_config_name: ``AWS::CodeDeploy::DeploymentConfig.DeploymentConfigName``.
        :param minimum_healthy_hosts: ``AWS::CodeDeploy::DeploymentConfig.MinimumHealthyHosts``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if deployment_config_name is not None:
            self._values["deployment_config_name"] = deployment_config_name
        if minimum_healthy_hosts is not None:
            self._values["minimum_healthy_hosts"] = minimum_healthy_hosts

    @builtins.property
    def deployment_config_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::CodeDeploy::DeploymentConfig.DeploymentConfigName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-deploymentconfigname
        '''
        result = self._values.get("deployment_config_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum_healthy_hosts(
        self,
    ) -> typing.Optional[typing.Union[CfnDeploymentConfig.MinimumHealthyHostsProperty, _IResolvable_a771d0ef]]:
        '''``AWS::CodeDeploy::DeploymentConfig.MinimumHealthyHosts``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-minimumhealthyhosts
        '''
        result = self._values.get("minimum_healthy_hosts")
        return typing.cast(typing.Optional[typing.Union[CfnDeploymentConfig.MinimumHealthyHostsProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnDeploymentGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codedeploy.CfnDeploymentGroup",
):
    '''A CloudFormation ``AWS::CodeDeploy::DeploymentGroup``.

    :cloudformationResource: AWS::CodeDeploy::DeploymentGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_name: builtins.str,
        service_role_arn: builtins.str,
        alarm_configuration: typing.Optional[typing.Union["CfnDeploymentGroup.AlarmConfigurationProperty", _IResolvable_a771d0ef]] = None,
        auto_rollback_configuration: typing.Optional[typing.Union["CfnDeploymentGroup.AutoRollbackConfigurationProperty", _IResolvable_a771d0ef]] = None,
        auto_scaling_groups: typing.Optional[typing.List[builtins.str]] = None,
        deployment: typing.Optional[typing.Union["CfnDeploymentGroup.DeploymentProperty", _IResolvable_a771d0ef]] = None,
        deployment_config_name: typing.Optional[builtins.str] = None,
        deployment_group_name: typing.Optional[builtins.str] = None,
        deployment_style: typing.Optional[typing.Union["CfnDeploymentGroup.DeploymentStyleProperty", _IResolvable_a771d0ef]] = None,
        ec2_tag_filters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.EC2TagFilterProperty", _IResolvable_a771d0ef]]]] = None,
        ec2_tag_set: typing.Optional[typing.Union["CfnDeploymentGroup.EC2TagSetProperty", _IResolvable_a771d0ef]] = None,
        load_balancer_info: typing.Optional[typing.Union["CfnDeploymentGroup.LoadBalancerInfoProperty", _IResolvable_a771d0ef]] = None,
        on_premises_instance_tag_filters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.TagFilterProperty", _IResolvable_a771d0ef]]]] = None,
        on_premises_tag_set: typing.Optional[typing.Union["CfnDeploymentGroup.OnPremisesTagSetProperty", _IResolvable_a771d0ef]] = None,
        trigger_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.TriggerConfigProperty", _IResolvable_a771d0ef]]]] = None,
    ) -> None:
        '''Create a new ``AWS::CodeDeploy::DeploymentGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_name: ``AWS::CodeDeploy::DeploymentGroup.ApplicationName``.
        :param service_role_arn: ``AWS::CodeDeploy::DeploymentGroup.ServiceRoleArn``.
        :param alarm_configuration: ``AWS::CodeDeploy::DeploymentGroup.AlarmConfiguration``.
        :param auto_rollback_configuration: ``AWS::CodeDeploy::DeploymentGroup.AutoRollbackConfiguration``.
        :param auto_scaling_groups: ``AWS::CodeDeploy::DeploymentGroup.AutoScalingGroups``.
        :param deployment: ``AWS::CodeDeploy::DeploymentGroup.Deployment``.
        :param deployment_config_name: ``AWS::CodeDeploy::DeploymentGroup.DeploymentConfigName``.
        :param deployment_group_name: ``AWS::CodeDeploy::DeploymentGroup.DeploymentGroupName``.
        :param deployment_style: ``AWS::CodeDeploy::DeploymentGroup.DeploymentStyle``.
        :param ec2_tag_filters: ``AWS::CodeDeploy::DeploymentGroup.Ec2TagFilters``.
        :param ec2_tag_set: ``AWS::CodeDeploy::DeploymentGroup.Ec2TagSet``.
        :param load_balancer_info: ``AWS::CodeDeploy::DeploymentGroup.LoadBalancerInfo``.
        :param on_premises_instance_tag_filters: ``AWS::CodeDeploy::DeploymentGroup.OnPremisesInstanceTagFilters``.
        :param on_premises_tag_set: ``AWS::CodeDeploy::DeploymentGroup.OnPremisesTagSet``.
        :param trigger_configurations: ``AWS::CodeDeploy::DeploymentGroup.TriggerConfigurations``.
        '''
        props = CfnDeploymentGroupProps(
            application_name=application_name,
            service_role_arn=service_role_arn,
            alarm_configuration=alarm_configuration,
            auto_rollback_configuration=auto_rollback_configuration,
            auto_scaling_groups=auto_scaling_groups,
            deployment=deployment,
            deployment_config_name=deployment_config_name,
            deployment_group_name=deployment_group_name,
            deployment_style=deployment_style,
            ec2_tag_filters=ec2_tag_filters,
            ec2_tag_set=ec2_tag_set,
            load_balancer_info=load_balancer_info,
            on_premises_instance_tag_filters=on_premises_instance_tag_filters,
            on_premises_tag_set=on_premises_tag_set,
            trigger_configurations=trigger_configurations,
        )

        jsii.create(CfnDeploymentGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        '''``AWS::CodeDeploy::DeploymentGroup.ApplicationName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-applicationname
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))

    @application_name.setter
    def application_name(self, value: builtins.str) -> None:
        jsii.set(self, "applicationName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="serviceRoleArn")
    def service_role_arn(self) -> builtins.str:
        '''``AWS::CodeDeploy::DeploymentGroup.ServiceRoleArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-servicerolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceRoleArn"))

    @service_role_arn.setter
    def service_role_arn(self, value: builtins.str) -> None:
        jsii.set(self, "serviceRoleArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="alarmConfiguration")
    def alarm_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnDeploymentGroup.AlarmConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::CodeDeploy::DeploymentGroup.AlarmConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-alarmconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDeploymentGroup.AlarmConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "alarmConfiguration"))

    @alarm_configuration.setter
    def alarm_configuration(
        self,
        value: typing.Optional[typing.Union["CfnDeploymentGroup.AlarmConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "alarmConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="autoRollbackConfiguration")
    def auto_rollback_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnDeploymentGroup.AutoRollbackConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::CodeDeploy::DeploymentGroup.AutoRollbackConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-autorollbackconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDeploymentGroup.AutoRollbackConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "autoRollbackConfiguration"))

    @auto_rollback_configuration.setter
    def auto_rollback_configuration(
        self,
        value: typing.Optional[typing.Union["CfnDeploymentGroup.AutoRollbackConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "autoRollbackConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="autoScalingGroups")
    def auto_scaling_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::CodeDeploy::DeploymentGroup.AutoScalingGroups``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-autoscalinggroups
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "autoScalingGroups"))

    @auto_scaling_groups.setter
    def auto_scaling_groups(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "autoScalingGroups", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deployment")
    def deployment(
        self,
    ) -> typing.Optional[typing.Union["CfnDeploymentGroup.DeploymentProperty", _IResolvable_a771d0ef]]:
        '''``AWS::CodeDeploy::DeploymentGroup.Deployment``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deployment
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDeploymentGroup.DeploymentProperty", _IResolvable_a771d0ef]], jsii.get(self, "deployment"))

    @deployment.setter
    def deployment(
        self,
        value: typing.Optional[typing.Union["CfnDeploymentGroup.DeploymentProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "deployment", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::CodeDeploy::DeploymentGroup.DeploymentConfigName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentconfigname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentConfigName"))

    @deployment_config_name.setter
    def deployment_config_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "deploymentConfigName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::CodeDeploy::DeploymentGroup.DeploymentGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentgroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentGroupName"))

    @deployment_group_name.setter
    def deployment_group_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "deploymentGroupName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentStyle")
    def deployment_style(
        self,
    ) -> typing.Optional[typing.Union["CfnDeploymentGroup.DeploymentStyleProperty", _IResolvable_a771d0ef]]:
        '''``AWS::CodeDeploy::DeploymentGroup.DeploymentStyle``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentstyle
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDeploymentGroup.DeploymentStyleProperty", _IResolvable_a771d0ef]], jsii.get(self, "deploymentStyle"))

    @deployment_style.setter
    def deployment_style(
        self,
        value: typing.Optional[typing.Union["CfnDeploymentGroup.DeploymentStyleProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "deploymentStyle", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ec2TagFilters")
    def ec2_tag_filters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.EC2TagFilterProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::CodeDeploy::DeploymentGroup.Ec2TagFilters``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-ec2tagfilters
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.EC2TagFilterProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "ec2TagFilters"))

    @ec2_tag_filters.setter
    def ec2_tag_filters(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.EC2TagFilterProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "ec2TagFilters", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ec2TagSet")
    def ec2_tag_set(
        self,
    ) -> typing.Optional[typing.Union["CfnDeploymentGroup.EC2TagSetProperty", _IResolvable_a771d0ef]]:
        '''``AWS::CodeDeploy::DeploymentGroup.Ec2TagSet``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-ec2tagset
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDeploymentGroup.EC2TagSetProperty", _IResolvable_a771d0ef]], jsii.get(self, "ec2TagSet"))

    @ec2_tag_set.setter
    def ec2_tag_set(
        self,
        value: typing.Optional[typing.Union["CfnDeploymentGroup.EC2TagSetProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "ec2TagSet", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loadBalancerInfo")
    def load_balancer_info(
        self,
    ) -> typing.Optional[typing.Union["CfnDeploymentGroup.LoadBalancerInfoProperty", _IResolvable_a771d0ef]]:
        '''``AWS::CodeDeploy::DeploymentGroup.LoadBalancerInfo``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-loadbalancerinfo
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDeploymentGroup.LoadBalancerInfoProperty", _IResolvable_a771d0ef]], jsii.get(self, "loadBalancerInfo"))

    @load_balancer_info.setter
    def load_balancer_info(
        self,
        value: typing.Optional[typing.Union["CfnDeploymentGroup.LoadBalancerInfoProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "loadBalancerInfo", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="onPremisesInstanceTagFilters")
    def on_premises_instance_tag_filters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.TagFilterProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::CodeDeploy::DeploymentGroup.OnPremisesInstanceTagFilters``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-onpremisesinstancetagfilters
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.TagFilterProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "onPremisesInstanceTagFilters"))

    @on_premises_instance_tag_filters.setter
    def on_premises_instance_tag_filters(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.TagFilterProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "onPremisesInstanceTagFilters", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="onPremisesTagSet")
    def on_premises_tag_set(
        self,
    ) -> typing.Optional[typing.Union["CfnDeploymentGroup.OnPremisesTagSetProperty", _IResolvable_a771d0ef]]:
        '''``AWS::CodeDeploy::DeploymentGroup.OnPremisesTagSet``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-onpremisestagset
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDeploymentGroup.OnPremisesTagSetProperty", _IResolvable_a771d0ef]], jsii.get(self, "onPremisesTagSet"))

    @on_premises_tag_set.setter
    def on_premises_tag_set(
        self,
        value: typing.Optional[typing.Union["CfnDeploymentGroup.OnPremisesTagSetProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "onPremisesTagSet", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="triggerConfigurations")
    def trigger_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.TriggerConfigProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::CodeDeploy::DeploymentGroup.TriggerConfigurations``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-triggerconfigurations
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.TriggerConfigProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "triggerConfigurations"))

    @trigger_configurations.setter
    def trigger_configurations(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.TriggerConfigProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "triggerConfigurations", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_codedeploy.CfnDeploymentGroup.AlarmConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alarms": "alarms",
            "enabled": "enabled",
            "ignore_poll_alarm_failure": "ignorePollAlarmFailure",
        },
    )
    class AlarmConfigurationProperty:
        def __init__(
            self,
            *,
            alarms: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.AlarmProperty", _IResolvable_a771d0ef]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            ignore_poll_alarm_failure: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param alarms: ``CfnDeploymentGroup.AlarmConfigurationProperty.Alarms``.
            :param enabled: ``CfnDeploymentGroup.AlarmConfigurationProperty.Enabled``.
            :param ignore_poll_alarm_failure: ``CfnDeploymentGroup.AlarmConfigurationProperty.IgnorePollAlarmFailure``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if alarms is not None:
                self._values["alarms"] = alarms
            if enabled is not None:
                self._values["enabled"] = enabled
            if ignore_poll_alarm_failure is not None:
                self._values["ignore_poll_alarm_failure"] = ignore_poll_alarm_failure

        @builtins.property
        def alarms(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.AlarmProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnDeploymentGroup.AlarmConfigurationProperty.Alarms``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html#cfn-codedeploy-deploymentgroup-alarmconfiguration-alarms
            '''
            result = self._values.get("alarms")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.AlarmProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnDeploymentGroup.AlarmConfigurationProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html#cfn-codedeploy-deploymentgroup-alarmconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def ignore_poll_alarm_failure(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnDeploymentGroup.AlarmConfigurationProperty.IgnorePollAlarmFailure``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html#cfn-codedeploy-deploymentgroup-alarmconfiguration-ignorepollalarmfailure
            '''
            result = self._values.get("ignore_poll_alarm_failure")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_codedeploy.CfnDeploymentGroup.AlarmProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class AlarmProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''
            :param name: ``CfnDeploymentGroup.AlarmProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarm.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''``CfnDeploymentGroup.AlarmProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarm.html#cfn-codedeploy-deploymentgroup-alarm-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_codedeploy.CfnDeploymentGroup.AutoRollbackConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "events": "events"},
    )
    class AutoRollbackConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            events: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            '''
            :param enabled: ``CfnDeploymentGroup.AutoRollbackConfigurationProperty.Enabled``.
            :param events: ``CfnDeploymentGroup.AutoRollbackConfigurationProperty.Events``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-autorollbackconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if events is not None:
                self._values["events"] = events

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnDeploymentGroup.AutoRollbackConfigurationProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-autorollbackconfiguration.html#cfn-codedeploy-deploymentgroup-autorollbackconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnDeploymentGroup.AutoRollbackConfigurationProperty.Events``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-autorollbackconfiguration.html#cfn-codedeploy-deploymentgroup-autorollbackconfiguration-events
            '''
            result = self._values.get("events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoRollbackConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_codedeploy.CfnDeploymentGroup.DeploymentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "revision": "revision",
            "description": "description",
            "ignore_application_stop_failures": "ignoreApplicationStopFailures",
        },
    )
    class DeploymentProperty:
        def __init__(
            self,
            *,
            revision: typing.Union["CfnDeploymentGroup.RevisionLocationProperty", _IResolvable_a771d0ef],
            description: typing.Optional[builtins.str] = None,
            ignore_application_stop_failures: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param revision: ``CfnDeploymentGroup.DeploymentProperty.Revision``.
            :param description: ``CfnDeploymentGroup.DeploymentProperty.Description``.
            :param ignore_application_stop_failures: ``CfnDeploymentGroup.DeploymentProperty.IgnoreApplicationStopFailures``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "revision": revision,
            }
            if description is not None:
                self._values["description"] = description
            if ignore_application_stop_failures is not None:
                self._values["ignore_application_stop_failures"] = ignore_application_stop_failures

        @builtins.property
        def revision(
            self,
        ) -> typing.Union["CfnDeploymentGroup.RevisionLocationProperty", _IResolvable_a771d0ef]:
            '''``CfnDeploymentGroup.DeploymentProperty.Revision``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision
            '''
            result = self._values.get("revision")
            assert result is not None, "Required property 'revision' is missing"
            return typing.cast(typing.Union["CfnDeploymentGroup.RevisionLocationProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''``CfnDeploymentGroup.DeploymentProperty.Description``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment.html#cfn-properties-codedeploy-deploymentgroup-deployment-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ignore_application_stop_failures(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnDeploymentGroup.DeploymentProperty.IgnoreApplicationStopFailures``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment.html#cfn-properties-codedeploy-deploymentgroup-deployment-ignoreapplicationstopfailures
            '''
            result = self._values.get("ignore_application_stop_failures")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_codedeploy.CfnDeploymentGroup.DeploymentStyleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "deployment_option": "deploymentOption",
            "deployment_type": "deploymentType",
        },
    )
    class DeploymentStyleProperty:
        def __init__(
            self,
            *,
            deployment_option: typing.Optional[builtins.str] = None,
            deployment_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param deployment_option: ``CfnDeploymentGroup.DeploymentStyleProperty.DeploymentOption``.
            :param deployment_type: ``CfnDeploymentGroup.DeploymentStyleProperty.DeploymentType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deploymentstyle.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if deployment_option is not None:
                self._values["deployment_option"] = deployment_option
            if deployment_type is not None:
                self._values["deployment_type"] = deployment_type

        @builtins.property
        def deployment_option(self) -> typing.Optional[builtins.str]:
            '''``CfnDeploymentGroup.DeploymentStyleProperty.DeploymentOption``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deploymentstyle.html#cfn-codedeploy-deploymentgroup-deploymentstyle-deploymentoption
            '''
            result = self._values.get("deployment_option")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def deployment_type(self) -> typing.Optional[builtins.str]:
            '''``CfnDeploymentGroup.DeploymentStyleProperty.DeploymentType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deploymentstyle.html#cfn-codedeploy-deploymentgroup-deploymentstyle-deploymenttype
            '''
            result = self._values.get("deployment_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentStyleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_codedeploy.CfnDeploymentGroup.EC2TagFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "type": "type", "value": "value"},
    )
    class EC2TagFilterProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param key: ``CfnDeploymentGroup.EC2TagFilterProperty.Key``.
            :param type: ``CfnDeploymentGroup.EC2TagFilterProperty.Type``.
            :param value: ``CfnDeploymentGroup.EC2TagFilterProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagfilter.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''``CfnDeploymentGroup.EC2TagFilterProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagfilter.html#cfn-codedeploy-deploymentgroup-ec2tagfilter-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''``CfnDeploymentGroup.EC2TagFilterProperty.Type``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagfilter.html#cfn-codedeploy-deploymentgroup-ec2tagfilter-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''``CfnDeploymentGroup.EC2TagFilterProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagfilter.html#cfn-codedeploy-deploymentgroup-ec2tagfilter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EC2TagFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_codedeploy.CfnDeploymentGroup.EC2TagSetListObjectProperty",
        jsii_struct_bases=[],
        name_mapping={"ec2_tag_group": "ec2TagGroup"},
    )
    class EC2TagSetListObjectProperty:
        def __init__(
            self,
            *,
            ec2_tag_group: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.EC2TagFilterProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param ec2_tag_group: ``CfnDeploymentGroup.EC2TagSetListObjectProperty.Ec2TagGroup``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagsetlistobject.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if ec2_tag_group is not None:
                self._values["ec2_tag_group"] = ec2_tag_group

        @builtins.property
        def ec2_tag_group(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.EC2TagFilterProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnDeploymentGroup.EC2TagSetListObjectProperty.Ec2TagGroup``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagsetlistobject.html#cfn-codedeploy-deploymentgroup-ec2tagsetlistobject-ec2taggroup
            '''
            result = self._values.get("ec2_tag_group")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.EC2TagFilterProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EC2TagSetListObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_codedeploy.CfnDeploymentGroup.EC2TagSetProperty",
        jsii_struct_bases=[],
        name_mapping={"ec2_tag_set_list": "ec2TagSetList"},
    )
    class EC2TagSetProperty:
        def __init__(
            self,
            *,
            ec2_tag_set_list: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.EC2TagSetListObjectProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param ec2_tag_set_list: ``CfnDeploymentGroup.EC2TagSetProperty.Ec2TagSetList``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagset.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if ec2_tag_set_list is not None:
                self._values["ec2_tag_set_list"] = ec2_tag_set_list

        @builtins.property
        def ec2_tag_set_list(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.EC2TagSetListObjectProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnDeploymentGroup.EC2TagSetProperty.Ec2TagSetList``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagset.html#cfn-codedeploy-deploymentgroup-ec2tagset-ec2tagsetlist
            '''
            result = self._values.get("ec2_tag_set_list")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.EC2TagSetListObjectProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EC2TagSetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_codedeploy.CfnDeploymentGroup.ELBInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class ELBInfoProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''
            :param name: ``CfnDeploymentGroup.ELBInfoProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-elbinfo.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''``CfnDeploymentGroup.ELBInfoProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-elbinfo.html#cfn-codedeploy-deploymentgroup-elbinfo-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ELBInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_codedeploy.CfnDeploymentGroup.GitHubLocationProperty",
        jsii_struct_bases=[],
        name_mapping={"commit_id": "commitId", "repository": "repository"},
    )
    class GitHubLocationProperty:
        def __init__(
            self,
            *,
            commit_id: builtins.str,
            repository: builtins.str,
        ) -> None:
            '''
            :param commit_id: ``CfnDeploymentGroup.GitHubLocationProperty.CommitId``.
            :param repository: ``CfnDeploymentGroup.GitHubLocationProperty.Repository``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-githublocation.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "commit_id": commit_id,
                "repository": repository,
            }

        @builtins.property
        def commit_id(self) -> builtins.str:
            '''``CfnDeploymentGroup.GitHubLocationProperty.CommitId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-githublocation.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-githublocation-commitid
            '''
            result = self._values.get("commit_id")
            assert result is not None, "Required property 'commit_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def repository(self) -> builtins.str:
            '''``CfnDeploymentGroup.GitHubLocationProperty.Repository``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-githublocation.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-githublocation-repository
            '''
            result = self._values.get("repository")
            assert result is not None, "Required property 'repository' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GitHubLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_codedeploy.CfnDeploymentGroup.LoadBalancerInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "elb_info_list": "elbInfoList",
            "target_group_info_list": "targetGroupInfoList",
        },
    )
    class LoadBalancerInfoProperty:
        def __init__(
            self,
            *,
            elb_info_list: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.ELBInfoProperty", _IResolvable_a771d0ef]]]] = None,
            target_group_info_list: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.TargetGroupInfoProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param elb_info_list: ``CfnDeploymentGroup.LoadBalancerInfoProperty.ElbInfoList``.
            :param target_group_info_list: ``CfnDeploymentGroup.LoadBalancerInfoProperty.TargetGroupInfoList``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-loadbalancerinfo.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if elb_info_list is not None:
                self._values["elb_info_list"] = elb_info_list
            if target_group_info_list is not None:
                self._values["target_group_info_list"] = target_group_info_list

        @builtins.property
        def elb_info_list(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.ELBInfoProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnDeploymentGroup.LoadBalancerInfoProperty.ElbInfoList``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-loadbalancerinfo.html#cfn-codedeploy-deploymentgroup-loadbalancerinfo-elbinfolist
            '''
            result = self._values.get("elb_info_list")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.ELBInfoProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def target_group_info_list(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.TargetGroupInfoProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnDeploymentGroup.LoadBalancerInfoProperty.TargetGroupInfoList``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-loadbalancerinfo.html#cfn-codedeploy-deploymentgroup-loadbalancerinfo-targetgroupinfolist
            '''
            result = self._values.get("target_group_info_list")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.TargetGroupInfoProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoadBalancerInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_codedeploy.CfnDeploymentGroup.OnPremisesTagSetListObjectProperty",
        jsii_struct_bases=[],
        name_mapping={"on_premises_tag_group": "onPremisesTagGroup"},
    )
    class OnPremisesTagSetListObjectProperty:
        def __init__(
            self,
            *,
            on_premises_tag_group: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.TagFilterProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param on_premises_tag_group: ``CfnDeploymentGroup.OnPremisesTagSetListObjectProperty.OnPremisesTagGroup``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagsetlistobject.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if on_premises_tag_group is not None:
                self._values["on_premises_tag_group"] = on_premises_tag_group

        @builtins.property
        def on_premises_tag_group(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.TagFilterProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnDeploymentGroup.OnPremisesTagSetListObjectProperty.OnPremisesTagGroup``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagsetlistobject.html#cfn-codedeploy-deploymentgroup-onpremisestagsetlistobject-onpremisestaggroup
            '''
            result = self._values.get("on_premises_tag_group")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.TagFilterProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnPremisesTagSetListObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_codedeploy.CfnDeploymentGroup.OnPremisesTagSetProperty",
        jsii_struct_bases=[],
        name_mapping={"on_premises_tag_set_list": "onPremisesTagSetList"},
    )
    class OnPremisesTagSetProperty:
        def __init__(
            self,
            *,
            on_premises_tag_set_list: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.OnPremisesTagSetListObjectProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param on_premises_tag_set_list: ``CfnDeploymentGroup.OnPremisesTagSetProperty.OnPremisesTagSetList``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagset.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if on_premises_tag_set_list is not None:
                self._values["on_premises_tag_set_list"] = on_premises_tag_set_list

        @builtins.property
        def on_premises_tag_set_list(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.OnPremisesTagSetListObjectProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnDeploymentGroup.OnPremisesTagSetProperty.OnPremisesTagSetList``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagset.html#cfn-codedeploy-deploymentgroup-onpremisestagset-onpremisestagsetlist
            '''
            result = self._values.get("on_premises_tag_set_list")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeploymentGroup.OnPremisesTagSetListObjectProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnPremisesTagSetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_codedeploy.CfnDeploymentGroup.RevisionLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "git_hub_location": "gitHubLocation",
            "revision_type": "revisionType",
            "s3_location": "s3Location",
        },
    )
    class RevisionLocationProperty:
        def __init__(
            self,
            *,
            git_hub_location: typing.Optional[typing.Union["CfnDeploymentGroup.GitHubLocationProperty", _IResolvable_a771d0ef]] = None,
            revision_type: typing.Optional[builtins.str] = None,
            s3_location: typing.Optional[typing.Union["CfnDeploymentGroup.S3LocationProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param git_hub_location: ``CfnDeploymentGroup.RevisionLocationProperty.GitHubLocation``.
            :param revision_type: ``CfnDeploymentGroup.RevisionLocationProperty.RevisionType``.
            :param s3_location: ``CfnDeploymentGroup.RevisionLocationProperty.S3Location``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if git_hub_location is not None:
                self._values["git_hub_location"] = git_hub_location
            if revision_type is not None:
                self._values["revision_type"] = revision_type
            if s3_location is not None:
                self._values["s3_location"] = s3_location

        @builtins.property
        def git_hub_location(
            self,
        ) -> typing.Optional[typing.Union["CfnDeploymentGroup.GitHubLocationProperty", _IResolvable_a771d0ef]]:
            '''``CfnDeploymentGroup.RevisionLocationProperty.GitHubLocation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-githublocation
            '''
            result = self._values.get("git_hub_location")
            return typing.cast(typing.Optional[typing.Union["CfnDeploymentGroup.GitHubLocationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def revision_type(self) -> typing.Optional[builtins.str]:
            '''``CfnDeploymentGroup.RevisionLocationProperty.RevisionType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-revisiontype
            '''
            result = self._values.get("revision_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_location(
            self,
        ) -> typing.Optional[typing.Union["CfnDeploymentGroup.S3LocationProperty", _IResolvable_a771d0ef]]:
            '''``CfnDeploymentGroup.RevisionLocationProperty.S3Location``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location
            '''
            result = self._values.get("s3_location")
            return typing.cast(typing.Optional[typing.Union["CfnDeploymentGroup.S3LocationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RevisionLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_codedeploy.CfnDeploymentGroup.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "key": "key",
            "bundle_type": "bundleType",
            "e_tag": "eTag",
            "version": "version",
        },
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            key: builtins.str,
            bundle_type: typing.Optional[builtins.str] = None,
            e_tag: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param bucket: ``CfnDeploymentGroup.S3LocationProperty.Bucket``.
            :param key: ``CfnDeploymentGroup.S3LocationProperty.Key``.
            :param bundle_type: ``CfnDeploymentGroup.S3LocationProperty.BundleType``.
            :param e_tag: ``CfnDeploymentGroup.S3LocationProperty.ETag``.
            :param version: ``CfnDeploymentGroup.S3LocationProperty.Version``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bucket": bucket,
                "key": key,
            }
            if bundle_type is not None:
                self._values["bundle_type"] = bundle_type
            if e_tag is not None:
                self._values["e_tag"] = e_tag
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnDeploymentGroup.S3LocationProperty.Bucket``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location-bucket
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnDeploymentGroup.S3LocationProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def bundle_type(self) -> typing.Optional[builtins.str]:
            '''``CfnDeploymentGroup.S3LocationProperty.BundleType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location-bundletype
            '''
            result = self._values.get("bundle_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def e_tag(self) -> typing.Optional[builtins.str]:
            '''``CfnDeploymentGroup.S3LocationProperty.ETag``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location-etag
            '''
            result = self._values.get("e_tag")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''``CfnDeploymentGroup.S3LocationProperty.Version``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location-value
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_codedeploy.CfnDeploymentGroup.TagFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "type": "type", "value": "value"},
    )
    class TagFilterProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param key: ``CfnDeploymentGroup.TagFilterProperty.Key``.
            :param type: ``CfnDeploymentGroup.TagFilterProperty.Type``.
            :param value: ``CfnDeploymentGroup.TagFilterProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-tagfilter.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''``CfnDeploymentGroup.TagFilterProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-tagfilter.html#cfn-codedeploy-deploymentgroup-tagfilter-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''``CfnDeploymentGroup.TagFilterProperty.Type``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-tagfilter.html#cfn-codedeploy-deploymentgroup-tagfilter-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''``CfnDeploymentGroup.TagFilterProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-tagfilter.html#cfn-codedeploy-deploymentgroup-tagfilter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_codedeploy.CfnDeploymentGroup.TargetGroupInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class TargetGroupInfoProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''
            :param name: ``CfnDeploymentGroup.TargetGroupInfoProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-targetgroupinfo.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''``CfnDeploymentGroup.TargetGroupInfoProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-targetgroupinfo.html#cfn-codedeploy-deploymentgroup-targetgroupinfo-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_codedeploy.CfnDeploymentGroup.TriggerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "trigger_events": "triggerEvents",
            "trigger_name": "triggerName",
            "trigger_target_arn": "triggerTargetArn",
        },
    )
    class TriggerConfigProperty:
        def __init__(
            self,
            *,
            trigger_events: typing.Optional[typing.List[builtins.str]] = None,
            trigger_name: typing.Optional[builtins.str] = None,
            trigger_target_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param trigger_events: ``CfnDeploymentGroup.TriggerConfigProperty.TriggerEvents``.
            :param trigger_name: ``CfnDeploymentGroup.TriggerConfigProperty.TriggerName``.
            :param trigger_target_arn: ``CfnDeploymentGroup.TriggerConfigProperty.TriggerTargetArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-triggerconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if trigger_events is not None:
                self._values["trigger_events"] = trigger_events
            if trigger_name is not None:
                self._values["trigger_name"] = trigger_name
            if trigger_target_arn is not None:
                self._values["trigger_target_arn"] = trigger_target_arn

        @builtins.property
        def trigger_events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnDeploymentGroup.TriggerConfigProperty.TriggerEvents``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-triggerconfig.html#cfn-codedeploy-deploymentgroup-triggerconfig-triggerevents
            '''
            result = self._values.get("trigger_events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def trigger_name(self) -> typing.Optional[builtins.str]:
            '''``CfnDeploymentGroup.TriggerConfigProperty.TriggerName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-triggerconfig.html#cfn-codedeploy-deploymentgroup-triggerconfig-triggername
            '''
            result = self._values.get("trigger_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def trigger_target_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnDeploymentGroup.TriggerConfigProperty.TriggerTargetArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-triggerconfig.html#cfn-codedeploy-deploymentgroup-triggerconfig-triggertargetarn
            '''
            result = self._values.get("trigger_target_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TriggerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_codedeploy.CfnDeploymentGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "service_role_arn": "serviceRoleArn",
        "alarm_configuration": "alarmConfiguration",
        "auto_rollback_configuration": "autoRollbackConfiguration",
        "auto_scaling_groups": "autoScalingGroups",
        "deployment": "deployment",
        "deployment_config_name": "deploymentConfigName",
        "deployment_group_name": "deploymentGroupName",
        "deployment_style": "deploymentStyle",
        "ec2_tag_filters": "ec2TagFilters",
        "ec2_tag_set": "ec2TagSet",
        "load_balancer_info": "loadBalancerInfo",
        "on_premises_instance_tag_filters": "onPremisesInstanceTagFilters",
        "on_premises_tag_set": "onPremisesTagSet",
        "trigger_configurations": "triggerConfigurations",
    },
)
class CfnDeploymentGroupProps:
    def __init__(
        self,
        *,
        application_name: builtins.str,
        service_role_arn: builtins.str,
        alarm_configuration: typing.Optional[typing.Union[CfnDeploymentGroup.AlarmConfigurationProperty, _IResolvable_a771d0ef]] = None,
        auto_rollback_configuration: typing.Optional[typing.Union[CfnDeploymentGroup.AutoRollbackConfigurationProperty, _IResolvable_a771d0ef]] = None,
        auto_scaling_groups: typing.Optional[typing.List[builtins.str]] = None,
        deployment: typing.Optional[typing.Union[CfnDeploymentGroup.DeploymentProperty, _IResolvable_a771d0ef]] = None,
        deployment_config_name: typing.Optional[builtins.str] = None,
        deployment_group_name: typing.Optional[builtins.str] = None,
        deployment_style: typing.Optional[typing.Union[CfnDeploymentGroup.DeploymentStyleProperty, _IResolvable_a771d0ef]] = None,
        ec2_tag_filters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnDeploymentGroup.EC2TagFilterProperty, _IResolvable_a771d0ef]]]] = None,
        ec2_tag_set: typing.Optional[typing.Union[CfnDeploymentGroup.EC2TagSetProperty, _IResolvable_a771d0ef]] = None,
        load_balancer_info: typing.Optional[typing.Union[CfnDeploymentGroup.LoadBalancerInfoProperty, _IResolvable_a771d0ef]] = None,
        on_premises_instance_tag_filters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnDeploymentGroup.TagFilterProperty, _IResolvable_a771d0ef]]]] = None,
        on_premises_tag_set: typing.Optional[typing.Union[CfnDeploymentGroup.OnPremisesTagSetProperty, _IResolvable_a771d0ef]] = None,
        trigger_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnDeploymentGroup.TriggerConfigProperty, _IResolvable_a771d0ef]]]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::CodeDeploy::DeploymentGroup``.

        :param application_name: ``AWS::CodeDeploy::DeploymentGroup.ApplicationName``.
        :param service_role_arn: ``AWS::CodeDeploy::DeploymentGroup.ServiceRoleArn``.
        :param alarm_configuration: ``AWS::CodeDeploy::DeploymentGroup.AlarmConfiguration``.
        :param auto_rollback_configuration: ``AWS::CodeDeploy::DeploymentGroup.AutoRollbackConfiguration``.
        :param auto_scaling_groups: ``AWS::CodeDeploy::DeploymentGroup.AutoScalingGroups``.
        :param deployment: ``AWS::CodeDeploy::DeploymentGroup.Deployment``.
        :param deployment_config_name: ``AWS::CodeDeploy::DeploymentGroup.DeploymentConfigName``.
        :param deployment_group_name: ``AWS::CodeDeploy::DeploymentGroup.DeploymentGroupName``.
        :param deployment_style: ``AWS::CodeDeploy::DeploymentGroup.DeploymentStyle``.
        :param ec2_tag_filters: ``AWS::CodeDeploy::DeploymentGroup.Ec2TagFilters``.
        :param ec2_tag_set: ``AWS::CodeDeploy::DeploymentGroup.Ec2TagSet``.
        :param load_balancer_info: ``AWS::CodeDeploy::DeploymentGroup.LoadBalancerInfo``.
        :param on_premises_instance_tag_filters: ``AWS::CodeDeploy::DeploymentGroup.OnPremisesInstanceTagFilters``.
        :param on_premises_tag_set: ``AWS::CodeDeploy::DeploymentGroup.OnPremisesTagSet``.
        :param trigger_configurations: ``AWS::CodeDeploy::DeploymentGroup.TriggerConfigurations``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "application_name": application_name,
            "service_role_arn": service_role_arn,
        }
        if alarm_configuration is not None:
            self._values["alarm_configuration"] = alarm_configuration
        if auto_rollback_configuration is not None:
            self._values["auto_rollback_configuration"] = auto_rollback_configuration
        if auto_scaling_groups is not None:
            self._values["auto_scaling_groups"] = auto_scaling_groups
        if deployment is not None:
            self._values["deployment"] = deployment
        if deployment_config_name is not None:
            self._values["deployment_config_name"] = deployment_config_name
        if deployment_group_name is not None:
            self._values["deployment_group_name"] = deployment_group_name
        if deployment_style is not None:
            self._values["deployment_style"] = deployment_style
        if ec2_tag_filters is not None:
            self._values["ec2_tag_filters"] = ec2_tag_filters
        if ec2_tag_set is not None:
            self._values["ec2_tag_set"] = ec2_tag_set
        if load_balancer_info is not None:
            self._values["load_balancer_info"] = load_balancer_info
        if on_premises_instance_tag_filters is not None:
            self._values["on_premises_instance_tag_filters"] = on_premises_instance_tag_filters
        if on_premises_tag_set is not None:
            self._values["on_premises_tag_set"] = on_premises_tag_set
        if trigger_configurations is not None:
            self._values["trigger_configurations"] = trigger_configurations

    @builtins.property
    def application_name(self) -> builtins.str:
        '''``AWS::CodeDeploy::DeploymentGroup.ApplicationName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-applicationname
        '''
        result = self._values.get("application_name")
        assert result is not None, "Required property 'application_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_role_arn(self) -> builtins.str:
        '''``AWS::CodeDeploy::DeploymentGroup.ServiceRoleArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-servicerolearn
        '''
        result = self._values.get("service_role_arn")
        assert result is not None, "Required property 'service_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alarm_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnDeploymentGroup.AlarmConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::CodeDeploy::DeploymentGroup.AlarmConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-alarmconfiguration
        '''
        result = self._values.get("alarm_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnDeploymentGroup.AlarmConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def auto_rollback_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnDeploymentGroup.AutoRollbackConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::CodeDeploy::DeploymentGroup.AutoRollbackConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-autorollbackconfiguration
        '''
        result = self._values.get("auto_rollback_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnDeploymentGroup.AutoRollbackConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def auto_scaling_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::CodeDeploy::DeploymentGroup.AutoScalingGroups``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-autoscalinggroups
        '''
        result = self._values.get("auto_scaling_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deployment(
        self,
    ) -> typing.Optional[typing.Union[CfnDeploymentGroup.DeploymentProperty, _IResolvable_a771d0ef]]:
        '''``AWS::CodeDeploy::DeploymentGroup.Deployment``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deployment
        '''
        result = self._values.get("deployment")
        return typing.cast(typing.Optional[typing.Union[CfnDeploymentGroup.DeploymentProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def deployment_config_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::CodeDeploy::DeploymentGroup.DeploymentConfigName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentconfigname
        '''
        result = self._values.get("deployment_config_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::CodeDeploy::DeploymentGroup.DeploymentGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentgroupname
        '''
        result = self._values.get("deployment_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_style(
        self,
    ) -> typing.Optional[typing.Union[CfnDeploymentGroup.DeploymentStyleProperty, _IResolvable_a771d0ef]]:
        '''``AWS::CodeDeploy::DeploymentGroup.DeploymentStyle``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentstyle
        '''
        result = self._values.get("deployment_style")
        return typing.cast(typing.Optional[typing.Union[CfnDeploymentGroup.DeploymentStyleProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def ec2_tag_filters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnDeploymentGroup.EC2TagFilterProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::CodeDeploy::DeploymentGroup.Ec2TagFilters``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-ec2tagfilters
        '''
        result = self._values.get("ec2_tag_filters")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnDeploymentGroup.EC2TagFilterProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def ec2_tag_set(
        self,
    ) -> typing.Optional[typing.Union[CfnDeploymentGroup.EC2TagSetProperty, _IResolvable_a771d0ef]]:
        '''``AWS::CodeDeploy::DeploymentGroup.Ec2TagSet``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-ec2tagset
        '''
        result = self._values.get("ec2_tag_set")
        return typing.cast(typing.Optional[typing.Union[CfnDeploymentGroup.EC2TagSetProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def load_balancer_info(
        self,
    ) -> typing.Optional[typing.Union[CfnDeploymentGroup.LoadBalancerInfoProperty, _IResolvable_a771d0ef]]:
        '''``AWS::CodeDeploy::DeploymentGroup.LoadBalancerInfo``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-loadbalancerinfo
        '''
        result = self._values.get("load_balancer_info")
        return typing.cast(typing.Optional[typing.Union[CfnDeploymentGroup.LoadBalancerInfoProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def on_premises_instance_tag_filters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnDeploymentGroup.TagFilterProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::CodeDeploy::DeploymentGroup.OnPremisesInstanceTagFilters``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-onpremisesinstancetagfilters
        '''
        result = self._values.get("on_premises_instance_tag_filters")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnDeploymentGroup.TagFilterProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def on_premises_tag_set(
        self,
    ) -> typing.Optional[typing.Union[CfnDeploymentGroup.OnPremisesTagSetProperty, _IResolvable_a771d0ef]]:
        '''``AWS::CodeDeploy::DeploymentGroup.OnPremisesTagSet``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-onpremisestagset
        '''
        result = self._values.get("on_premises_tag_set")
        return typing.cast(typing.Optional[typing.Union[CfnDeploymentGroup.OnPremisesTagSetProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def trigger_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnDeploymentGroup.TriggerConfigProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::CodeDeploy::DeploymentGroup.TriggerConfigurations``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-triggerconfigurations
        '''
        result = self._values.get("trigger_configurations")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnDeploymentGroup.TriggerConfigProperty, _IResolvable_a771d0ef]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_codedeploy.CustomLambdaDeploymentConfigProps",
    jsii_struct_bases=[],
    name_mapping={
        "interval": "interval",
        "percentage": "percentage",
        "type": "type",
        "deployment_config_name": "deploymentConfigName",
    },
)
class CustomLambdaDeploymentConfigProps:
    def __init__(
        self,
        *,
        interval: _Duration_070aa057,
        percentage: jsii.Number,
        type: "CustomLambdaDeploymentConfigType",
        deployment_config_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties of a reference to a CodeDeploy Lambda Deployment Configuration.

        :param interval: (experimental) The interval, in number of minutes: - For LINEAR, how frequently additional traffic is shifted - For CANARY, how long to shift traffic before the full deployment.
        :param percentage: (experimental) The integer percentage of traffic to shift: - For LINEAR, the percentage to shift every interval - For CANARY, the percentage to shift until the interval passes, before the full deployment.
        :param type: (experimental) The type of deployment config, either CANARY or LINEAR.
        :param deployment_config_name: (experimental) The verbatim name of the deployment config. Must be unique per account/region. Other parameters cannot be updated if this name is provided. Default: - automatically generated name

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "interval": interval,
            "percentage": percentage,
            "type": type,
        }
        if deployment_config_name is not None:
            self._values["deployment_config_name"] = deployment_config_name

    @builtins.property
    def interval(self) -> _Duration_070aa057:
        '''(experimental) The interval, in number of minutes: - For LINEAR, how frequently additional traffic is shifted - For CANARY, how long to shift traffic before the full deployment.

        :stability: experimental
        '''
        result = self._values.get("interval")
        assert result is not None, "Required property 'interval' is missing"
        return typing.cast(_Duration_070aa057, result)

    @builtins.property
    def percentage(self) -> jsii.Number:
        '''(experimental) The integer percentage of traffic to shift: - For LINEAR, the percentage to shift every interval - For CANARY, the percentage to shift until the interval passes, before the full deployment.

        :stability: experimental
        '''
        result = self._values.get("percentage")
        assert result is not None, "Required property 'percentage' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> "CustomLambdaDeploymentConfigType":
        '''(experimental) The type of deployment config, either CANARY or LINEAR.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("CustomLambdaDeploymentConfigType", result)

    @builtins.property
    def deployment_config_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The verbatim name of the deployment config.

        Must be unique per account/region.
        Other parameters cannot be updated if this name is provided.

        :default: - automatically generated name

        :stability: experimental
        '''
        result = self._values.get("deployment_config_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomLambdaDeploymentConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_codedeploy.CustomLambdaDeploymentConfigType")
class CustomLambdaDeploymentConfigType(enum.Enum):
    '''(experimental) Lambda Deployment config type.

    :stability: experimental
    '''

    CANARY = "CANARY"
    '''(experimental) Canary deployment type.

    :stability: experimental
    '''
    LINEAR = "LINEAR"
    '''(experimental) Linear deployment type.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_codedeploy.EcsApplicationProps",
    jsii_struct_bases=[],
    name_mapping={"application_name": "applicationName"},
)
class EcsApplicationProps:
    def __init__(
        self,
        *,
        application_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Construction properties for {@link EcsApplication}.

        :param application_name: (experimental) The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if application_name is not None:
            self._values["application_name"] = application_name

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The physical, human-readable name of the CodeDeploy Application.

        :default: an auto-generated name will be used

        :stability: experimental
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsDeploymentConfig(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codedeploy.EcsDeploymentConfig",
):
    '''(experimental) A custom Deployment Configuration for an ECS Deployment Group.

    Note: This class currently stands as namespaced container of the default configurations
    until CloudFormation supports custom ECS Deployment Configs. Until then it is closed
    (private constructor) and does not extend {@link cdk.Construct}

    :stability: experimental
    :resource: AWS::CodeDeploy::DeploymentConfig
    '''

    @jsii.member(jsii_name="fromEcsDeploymentConfigName") # type: ignore[misc]
    @builtins.classmethod
    def from_ecs_deployment_config_name(
        cls,
        _scope: constructs.Construct,
        _id: builtins.str,
        ecs_deployment_config_name: builtins.str,
    ) -> "IEcsDeploymentConfig":
        '''(experimental) Import a custom Deployment Configuration for an ECS Deployment Group defined outside the CDK.

        :param _scope: the parent Construct for this new Construct.
        :param _id: the logical ID of this new Construct.
        :param ecs_deployment_config_name: the name of the referenced custom Deployment Configuration.

        :return: a Construct representing a reference to an existing custom Deployment Configuration

        :stability: experimental
        '''
        return typing.cast("IEcsDeploymentConfig", jsii.sinvoke(cls, "fromEcsDeploymentConfigName", [_scope, _id, ecs_deployment_config_name]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="ALL_AT_ONCE")
    def ALL_AT_ONCE(cls) -> "IEcsDeploymentConfig":
        '''
        :stability: experimental
        '''
        return typing.cast("IEcsDeploymentConfig", jsii.sget(cls, "ALL_AT_ONCE"))


class EcsDeploymentGroup(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codedeploy.EcsDeploymentGroup",
):
    '''(experimental) Note: This class currently stands as a namespaced container for importing an ECS Deployment Group defined outside the CDK app until CloudFormation supports provisioning ECS Deployment Groups.

    Until then it is closed (private constructor) and does not
    extend {@link cdk.Construct}.

    :stability: experimental
    :resource: AWS::CodeDeploy::DeploymentGroup
    '''

    @jsii.member(jsii_name="fromEcsDeploymentGroupAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_ecs_deployment_group_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        application: "IEcsApplication",
        deployment_group_name: builtins.str,
        deployment_config: typing.Optional["IEcsDeploymentConfig"] = None,
    ) -> "IEcsDeploymentGroup":
        '''(experimental) Import an ECS Deployment Group defined outside the CDK app.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param application: (experimental) The reference to the CodeDeploy ECS Application that this Deployment Group belongs to.
        :param deployment_group_name: (experimental) The physical, human-readable name of the CodeDeploy ECS Deployment Group that we are referencing.
        :param deployment_config: (experimental) The Deployment Configuration this Deployment Group uses. Default: EcsDeploymentConfig.ALL_AT_ONCE

        :return: a Construct representing a reference to an existing Deployment Group

        :stability: experimental
        '''
        attrs = EcsDeploymentGroupAttributes(
            application=application,
            deployment_group_name=deployment_group_name,
            deployment_config=deployment_config,
        )

        return typing.cast("IEcsDeploymentGroup", jsii.sinvoke(cls, "fromEcsDeploymentGroupAttributes", [scope, id, attrs]))


@jsii.data_type(
    jsii_type="monocdk.aws_codedeploy.EcsDeploymentGroupAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "application": "application",
        "deployment_group_name": "deploymentGroupName",
        "deployment_config": "deploymentConfig",
    },
)
class EcsDeploymentGroupAttributes:
    def __init__(
        self,
        *,
        application: "IEcsApplication",
        deployment_group_name: builtins.str,
        deployment_config: typing.Optional["IEcsDeploymentConfig"] = None,
    ) -> None:
        '''(experimental) Properties of a reference to a CodeDeploy ECS Deployment Group.

        :param application: (experimental) The reference to the CodeDeploy ECS Application that this Deployment Group belongs to.
        :param deployment_group_name: (experimental) The physical, human-readable name of the CodeDeploy ECS Deployment Group that we are referencing.
        :param deployment_config: (experimental) The Deployment Configuration this Deployment Group uses. Default: EcsDeploymentConfig.ALL_AT_ONCE

        :see: EcsDeploymentGroup#fromEcsDeploymentGroupAttributes
        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "application": application,
            "deployment_group_name": deployment_group_name,
        }
        if deployment_config is not None:
            self._values["deployment_config"] = deployment_config

    @builtins.property
    def application(self) -> "IEcsApplication":
        '''(experimental) The reference to the CodeDeploy ECS Application that this Deployment Group belongs to.

        :stability: experimental
        '''
        result = self._values.get("application")
        assert result is not None, "Required property 'application' is missing"
        return typing.cast("IEcsApplication", result)

    @builtins.property
    def deployment_group_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the CodeDeploy ECS Deployment Group that we are referencing.

        :stability: experimental
        '''
        result = self._values.get("deployment_group_name")
        assert result is not None, "Required property 'deployment_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deployment_config(self) -> typing.Optional["IEcsDeploymentConfig"]:
        '''(experimental) The Deployment Configuration this Deployment Group uses.

        :default: EcsDeploymentConfig.ALL_AT_ONCE

        :stability: experimental
        '''
        result = self._values.get("deployment_config")
        return typing.cast(typing.Optional["IEcsDeploymentConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsDeploymentGroupAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_codedeploy.IEcsApplication")
class IEcsApplication(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Represents a reference to a CodeDeploy Application deploying to Amazon ECS.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link EcsApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link EcsApplication#fromEcsApplicationName} method.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IEcsApplicationProxy"]:
        return _IEcsApplicationProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...


class _IEcsApplicationProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''(experimental) Represents a reference to a CodeDeploy Application deploying to Amazon ECS.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link EcsApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link EcsApplication#fromEcsApplicationName} method.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_codedeploy.IEcsApplication"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))


@jsii.interface(jsii_type="monocdk.aws_codedeploy.IEcsDeploymentConfig")
class IEcsDeploymentConfig(typing_extensions.Protocol):
    '''(experimental) The Deployment Configuration of an ECS Deployment Group.

    The default, pre-defined Configurations are available as constants on the {@link EcsDeploymentConfig} class
    (for example, ``EcsDeploymentConfig.AllAtOnce``).

    Note: CloudFormation does not currently support creating custom ECS configs outside
    of using a custom resource. You can import custom deployment config created outside the
    CDK or via a custom resource with {@link EcsDeploymentConfig#fromEcsDeploymentConfigName}.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IEcsDeploymentConfigProxy"]:
        return _IEcsDeploymentConfigProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...


class _IEcsDeploymentConfigProxy:
    '''(experimental) The Deployment Configuration of an ECS Deployment Group.

    The default, pre-defined Configurations are available as constants on the {@link EcsDeploymentConfig} class
    (for example, ``EcsDeploymentConfig.AllAtOnce``).

    Note: CloudFormation does not currently support creating custom ECS configs outside
    of using a custom resource. You can import custom deployment config created outside the
    CDK or via a custom resource with {@link EcsDeploymentConfig#fromEcsDeploymentConfigName}.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_codedeploy.IEcsDeploymentConfig"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigName"))


@jsii.interface(jsii_type="monocdk.aws_codedeploy.IEcsDeploymentGroup")
class IEcsDeploymentGroup(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Interface for an ECS deployment group.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IEcsDeploymentGroupProxy"]:
        return _IEcsDeploymentGroupProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="application")
    def application(self) -> IEcsApplication:
        '''(experimental) The reference to the CodeDeploy ECS Application that this Deployment Group belongs to.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> IEcsDeploymentConfig:
        '''(experimental) The Deployment Configuration this Group uses.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> builtins.str:
        '''(experimental) The ARN of this Deployment Group.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> builtins.str:
        '''(experimental) The physical name of the CodeDeploy Deployment Group.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IEcsDeploymentGroupProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''(experimental) Interface for an ECS deployment group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_codedeploy.IEcsDeploymentGroup"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="application")
    def application(self) -> IEcsApplication:
        '''(experimental) The reference to the CodeDeploy ECS Application that this Deployment Group belongs to.

        :stability: experimental
        '''
        return typing.cast(IEcsApplication, jsii.get(self, "application"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> IEcsDeploymentConfig:
        '''(experimental) The Deployment Configuration this Group uses.

        :stability: experimental
        '''
        return typing.cast(IEcsDeploymentConfig, jsii.get(self, "deploymentConfig"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> builtins.str:
        '''(experimental) The ARN of this Deployment Group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> builtins.str:
        '''(experimental) The physical name of the CodeDeploy Deployment Group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupName"))


@jsii.interface(jsii_type="monocdk.aws_codedeploy.ILambdaApplication")
class ILambdaApplication(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Represents a reference to a CodeDeploy Application deploying to AWS Lambda.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link LambdaApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link LambdaApplication#fromLambdaApplicationName} method.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_ILambdaApplicationProxy"]:
        return _ILambdaApplicationProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...


class _ILambdaApplicationProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''(experimental) Represents a reference to a CodeDeploy Application deploying to AWS Lambda.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link LambdaApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link LambdaApplication#fromLambdaApplicationName} method.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_codedeploy.ILambdaApplication"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))


@jsii.interface(jsii_type="monocdk.aws_codedeploy.ILambdaDeploymentConfig")
class ILambdaDeploymentConfig(typing_extensions.Protocol):
    '''(experimental) The Deployment Configuration of a Lambda Deployment Group.

    The default, pre-defined Configurations are available as constants on the {@link LambdaDeploymentConfig} class
    (``LambdaDeploymentConfig.AllAtOnce``, ``LambdaDeploymentConfig.Canary10Percent30Minutes``, etc.).

    Note: CloudFormation does not currently support creating custom lambda configs outside
    of using a custom resource. You can import custom deployment config created outside the
    CDK or via a custom resource with {@link LambdaDeploymentConfig#import}.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_ILambdaDeploymentConfigProxy"]:
        return _ILambdaDeploymentConfigProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...


class _ILambdaDeploymentConfigProxy:
    '''(experimental) The Deployment Configuration of a Lambda Deployment Group.

    The default, pre-defined Configurations are available as constants on the {@link LambdaDeploymentConfig} class
    (``LambdaDeploymentConfig.AllAtOnce``, ``LambdaDeploymentConfig.Canary10Percent30Minutes``, etc.).

    Note: CloudFormation does not currently support creating custom lambda configs outside
    of using a custom resource. You can import custom deployment config created outside the
    CDK or via a custom resource with {@link LambdaDeploymentConfig#import}.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_codedeploy.ILambdaDeploymentConfig"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigName"))


@jsii.interface(jsii_type="monocdk.aws_codedeploy.ILambdaDeploymentGroup")
class ILambdaDeploymentGroup(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Interface for a Lambda deployment groups.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_ILambdaDeploymentGroupProxy"]:
        return _ILambdaDeploymentGroupProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="application")
    def application(self) -> ILambdaApplication:
        '''(experimental) The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> ILambdaDeploymentConfig:
        '''(experimental) The Deployment Configuration this Group uses.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> builtins.str:
        '''(experimental) The ARN of this Deployment Group.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> builtins.str:
        '''(experimental) The physical name of the CodeDeploy Deployment Group.

        :stability: experimental
        :attribute: true
        '''
        ...


class _ILambdaDeploymentGroupProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''(experimental) Interface for a Lambda deployment groups.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_codedeploy.ILambdaDeploymentGroup"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="application")
    def application(self) -> ILambdaApplication:
        '''(experimental) The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.

        :stability: experimental
        '''
        return typing.cast(ILambdaApplication, jsii.get(self, "application"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> ILambdaDeploymentConfig:
        '''(experimental) The Deployment Configuration this Group uses.

        :stability: experimental
        '''
        return typing.cast(ILambdaDeploymentConfig, jsii.get(self, "deploymentConfig"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> builtins.str:
        '''(experimental) The ARN of this Deployment Group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> builtins.str:
        '''(experimental) The physical name of the CodeDeploy Deployment Group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupName"))


@jsii.interface(jsii_type="monocdk.aws_codedeploy.IServerApplication")
class IServerApplication(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Represents a reference to a CodeDeploy Application deploying to EC2/on-premise instances.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link ServerApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link #fromServerApplicationName} method.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IServerApplicationProxy"]:
        return _IServerApplicationProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...


class _IServerApplicationProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''(experimental) Represents a reference to a CodeDeploy Application deploying to EC2/on-premise instances.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link ServerApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link #fromServerApplicationName} method.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_codedeploy.IServerApplication"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))


@jsii.interface(jsii_type="monocdk.aws_codedeploy.IServerDeploymentConfig")
class IServerDeploymentConfig(typing_extensions.Protocol):
    '''(experimental) The Deployment Configuration of an EC2/on-premise Deployment Group.

    The default, pre-defined Configurations are available as constants on the {@link ServerDeploymentConfig} class
    (``ServerDeploymentConfig.HALF_AT_A_TIME``, ``ServerDeploymentConfig.ALL_AT_ONCE``, etc.).
    To create a custom Deployment Configuration,
    instantiate the {@link ServerDeploymentConfig} Construct.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IServerDeploymentConfigProxy"]:
        return _IServerDeploymentConfigProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...


class _IServerDeploymentConfigProxy:
    '''(experimental) The Deployment Configuration of an EC2/on-premise Deployment Group.

    The default, pre-defined Configurations are available as constants on the {@link ServerDeploymentConfig} class
    (``ServerDeploymentConfig.HALF_AT_A_TIME``, ``ServerDeploymentConfig.ALL_AT_ONCE``, etc.).
    To create a custom Deployment Configuration,
    instantiate the {@link ServerDeploymentConfig} Construct.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_codedeploy.IServerDeploymentConfig"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigName"))


@jsii.interface(jsii_type="monocdk.aws_codedeploy.IServerDeploymentGroup")
class IServerDeploymentGroup(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IServerDeploymentGroupProxy"]:
        return _IServerDeploymentGroupProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="application")
    def application(self) -> IServerApplication:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> IServerDeploymentConfig:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="autoScalingGroups")
    def auto_scaling_groups(
        self,
    ) -> typing.Optional[typing.List[_IAutoScalingGroup_352723c6]]:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''
        :stability: experimental
        '''
        ...


class _IServerDeploymentGroupProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_codedeploy.IServerDeploymentGroup"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="application")
    def application(self) -> IServerApplication:
        '''
        :stability: experimental
        '''
        return typing.cast(IServerApplication, jsii.get(self, "application"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> IServerDeploymentConfig:
        '''
        :stability: experimental
        '''
        return typing.cast(IServerDeploymentConfig, jsii.get(self, "deploymentConfig"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="autoScalingGroups")
    def auto_scaling_groups(
        self,
    ) -> typing.Optional[typing.List[_IAutoScalingGroup_352723c6]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[_IAutoScalingGroup_352723c6]], jsii.get(self, "autoScalingGroups"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IRole_59af6f50], jsii.get(self, "role"))


class InstanceTagSet(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codedeploy.InstanceTagSet",
):
    '''(experimental) Represents a set of instance tag groups.

    An instance will match a set if it matches all of the groups in the set -
    in other words, sets follow 'and' semantics.
    You can have a maximum of 3 tag groups inside a set.

    :stability: experimental
    '''

    def __init__(
        self,
        *instance_tag_groups: typing.Mapping[builtins.str, typing.List[builtins.str]],
    ) -> None:
        '''
        :param instance_tag_groups: -

        :stability: experimental
        '''
        jsii.create(InstanceTagSet, self, [*instance_tag_groups])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="instanceTagGroups")
    def instance_tag_groups(
        self,
    ) -> typing.List[typing.Mapping[builtins.str, typing.List[builtins.str]]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List[typing.Mapping[builtins.str, typing.List[builtins.str]]], jsii.get(self, "instanceTagGroups"))


@jsii.implements(ILambdaApplication)
class LambdaApplication(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codedeploy.LambdaApplication",
):
    '''(experimental) A CodeDeploy Application that deploys to an AWS Lambda function.

    :stability: experimental
    :resource: AWS::CodeDeploy::Application
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        application_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param application_name: (experimental) The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used

        :stability: experimental
        '''
        props = LambdaApplicationProps(application_name=application_name)

        jsii.create(LambdaApplication, self, [scope, id, props])

    @jsii.member(jsii_name="fromLambdaApplicationName") # type: ignore[misc]
    @builtins.classmethod
    def from_lambda_application_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        lambda_application_name: builtins.str,
    ) -> ILambdaApplication:
        '''(experimental) Import an Application defined either outside the CDK, or in a different CDK Stack.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param lambda_application_name: the name of the application to import.

        :return: a Construct representing a reference to an existing Application

        :stability: experimental
        '''
        return typing.cast(ILambdaApplication, jsii.sinvoke(cls, "fromLambdaApplicationName", [scope, id, lambda_application_name]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))


@jsii.data_type(
    jsii_type="monocdk.aws_codedeploy.LambdaApplicationProps",
    jsii_struct_bases=[],
    name_mapping={"application_name": "applicationName"},
)
class LambdaApplicationProps:
    def __init__(
        self,
        *,
        application_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Construction properties for {@link LambdaApplication}.

        :param application_name: (experimental) The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if application_name is not None:
            self._values["application_name"] = application_name

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The physical, human-readable name of the CodeDeploy Application.

        :default: an auto-generated name will be used

        :stability: experimental
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaDeploymentConfig(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codedeploy.LambdaDeploymentConfig",
):
    '''(experimental) A custom Deployment Configuration for a Lambda Deployment Group.

    Note: This class currently stands as namespaced container of the default configurations
    until CloudFormation supports custom Lambda Deployment Configs. Until then it is closed
    (private constructor) and does not extend {@link cdk.Construct}

    :stability: experimental
    :resource: AWS::CodeDeploy::DeploymentConfig
    '''

    @jsii.member(jsii_name="import") # type: ignore[misc]
    @builtins.classmethod
    def import_(
        cls,
        _scope: constructs.Construct,
        _id: builtins.str,
        *,
        deployment_config_name: builtins.str,
    ) -> ILambdaDeploymentConfig:
        '''(experimental) Import a custom Deployment Configuration for a Lambda Deployment Group defined outside the CDK.

        :param _scope: the parent Construct for this new Construct.
        :param _id: the logical ID of this new Construct.
        :param deployment_config_name: (experimental) The physical, human-readable name of the custom CodeDeploy Lambda Deployment Configuration that we are referencing.

        :return: a Construct representing a reference to an existing custom Deployment Configuration

        :stability: experimental
        '''
        props = LambdaDeploymentConfigImportProps(
            deployment_config_name=deployment_config_name
        )

        return typing.cast(ILambdaDeploymentConfig, jsii.sinvoke(cls, "import", [_scope, _id, props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="ALL_AT_ONCE")
    def ALL_AT_ONCE(cls) -> ILambdaDeploymentConfig:
        '''
        :stability: experimental
        '''
        return typing.cast(ILambdaDeploymentConfig, jsii.sget(cls, "ALL_AT_ONCE"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CANARY_10PERCENT_10MINUTES")
    def CANARY_10_PERCENT_10_MINUTES(cls) -> ILambdaDeploymentConfig:
        '''
        :stability: experimental
        '''
        return typing.cast(ILambdaDeploymentConfig, jsii.sget(cls, "CANARY_10PERCENT_10MINUTES"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CANARY_10PERCENT_15MINUTES")
    def CANARY_10_PERCENT_15_MINUTES(cls) -> ILambdaDeploymentConfig:
        '''
        :stability: experimental
        '''
        return typing.cast(ILambdaDeploymentConfig, jsii.sget(cls, "CANARY_10PERCENT_15MINUTES"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CANARY_10PERCENT_30MINUTES")
    def CANARY_10_PERCENT_30_MINUTES(cls) -> ILambdaDeploymentConfig:
        '''
        :stability: experimental
        '''
        return typing.cast(ILambdaDeploymentConfig, jsii.sget(cls, "CANARY_10PERCENT_30MINUTES"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CANARY_10PERCENT_5MINUTES")
    def CANARY_10_PERCENT_5_MINUTES(cls) -> ILambdaDeploymentConfig:
        '''
        :stability: experimental
        '''
        return typing.cast(ILambdaDeploymentConfig, jsii.sget(cls, "CANARY_10PERCENT_5MINUTES"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="LINEAR_10PERCENT_EVERY_10MINUTES")
    def LINEAR_10_PERCENT_EVERY_10_MINUTES(cls) -> ILambdaDeploymentConfig:
        '''
        :stability: experimental
        '''
        return typing.cast(ILambdaDeploymentConfig, jsii.sget(cls, "LINEAR_10PERCENT_EVERY_10MINUTES"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="LINEAR_10PERCENT_EVERY_1MINUTE")
    def LINEAR_10_PERCENT_EVERY_1_MINUTE(cls) -> ILambdaDeploymentConfig:
        '''
        :stability: experimental
        '''
        return typing.cast(ILambdaDeploymentConfig, jsii.sget(cls, "LINEAR_10PERCENT_EVERY_1MINUTE"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="LINEAR_10PERCENT_EVERY_2MINUTES")
    def LINEAR_10_PERCENT_EVERY_2_MINUTES(cls) -> ILambdaDeploymentConfig:
        '''
        :stability: experimental
        '''
        return typing.cast(ILambdaDeploymentConfig, jsii.sget(cls, "LINEAR_10PERCENT_EVERY_2MINUTES"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="LINEAR_10PERCENT_EVERY_3MINUTES")
    def LINEAR_10_PERCENT_EVERY_3_MINUTES(cls) -> ILambdaDeploymentConfig:
        '''
        :stability: experimental
        '''
        return typing.cast(ILambdaDeploymentConfig, jsii.sget(cls, "LINEAR_10PERCENT_EVERY_3MINUTES"))


@jsii.data_type(
    jsii_type="monocdk.aws_codedeploy.LambdaDeploymentConfigImportProps",
    jsii_struct_bases=[],
    name_mapping={"deployment_config_name": "deploymentConfigName"},
)
class LambdaDeploymentConfigImportProps:
    def __init__(self, *, deployment_config_name: builtins.str) -> None:
        '''(experimental) Properties of a reference to a CodeDeploy Lambda Deployment Configuration.

        :param deployment_config_name: (experimental) The physical, human-readable name of the custom CodeDeploy Lambda Deployment Configuration that we are referencing.

        :see: LambdaDeploymentConfig#import
        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "deployment_config_name": deployment_config_name,
        }

    @builtins.property
    def deployment_config_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the custom CodeDeploy Lambda Deployment Configuration that we are referencing.

        :stability: experimental
        '''
        result = self._values.get("deployment_config_name")
        assert result is not None, "Required property 'deployment_config_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaDeploymentConfigImportProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ILambdaDeploymentGroup)
class LambdaDeploymentGroup(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codedeploy.LambdaDeploymentGroup",
):
    '''
    :stability: experimental
    :resource: AWS::CodeDeploy::DeploymentGroup
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        alias: _Alias_9e39972c,
        alarms: typing.Optional[typing.List[_IAlarm_bf66c8d0]] = None,
        application: typing.Optional[ILambdaApplication] = None,
        auto_rollback: typing.Optional[AutoRollbackConfig] = None,
        deployment_config: typing.Optional[ILambdaDeploymentConfig] = None,
        deployment_group_name: typing.Optional[builtins.str] = None,
        ignore_poll_alarms_failure: typing.Optional[builtins.bool] = None,
        post_hook: typing.Optional[_IFunction_6e14f09e] = None,
        pre_hook: typing.Optional[_IFunction_6e14f09e] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param alias: (experimental) Lambda Alias to shift traffic. Updating the version of the alias will trigger a CodeDeploy deployment. [disable-awslint:ref-via-interface] since we need to modify the alias CFN resource update policy
        :param alarms: (experimental) The CloudWatch alarms associated with this Deployment Group. CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger. Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method. Default: []
        :param application: (experimental) The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to. Default: - One will be created for you.
        :param auto_rollback: (experimental) The auto-rollback configuration for this Deployment Group. Default: - default AutoRollbackConfig.
        :param deployment_config: (experimental) The Deployment Configuration this Deployment Group uses. Default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES
        :param deployment_group_name: (experimental) The physical, human-readable name of the CodeDeploy Deployment Group. Default: - An auto-generated name will be used.
        :param ignore_poll_alarms_failure: (experimental) Whether to continue a deployment even if fetching the alarm status from CloudWatch failed. Default: false
        :param post_hook: (experimental) The Lambda function to run after traffic routing starts. Default: - None.
        :param pre_hook: (experimental) The Lambda function to run before traffic routing starts. Default: - None.
        :param role: (experimental) The service Role of this Deployment Group. Default: - A new Role will be created.

        :stability: experimental
        '''
        props = LambdaDeploymentGroupProps(
            alias=alias,
            alarms=alarms,
            application=application,
            auto_rollback=auto_rollback,
            deployment_config=deployment_config,
            deployment_group_name=deployment_group_name,
            ignore_poll_alarms_failure=ignore_poll_alarms_failure,
            post_hook=post_hook,
            pre_hook=pre_hook,
            role=role,
        )

        jsii.create(LambdaDeploymentGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromLambdaDeploymentGroupAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_lambda_deployment_group_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        application: ILambdaApplication,
        deployment_group_name: builtins.str,
        deployment_config: typing.Optional[ILambdaDeploymentConfig] = None,
    ) -> ILambdaDeploymentGroup:
        '''(experimental) Import an Lambda Deployment Group defined either outside the CDK app, or in a different AWS region.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param application: (experimental) The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.
        :param deployment_group_name: (experimental) The physical, human-readable name of the CodeDeploy Lambda Deployment Group that we are referencing.
        :param deployment_config: (experimental) The Deployment Configuration this Deployment Group uses. Default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES

        :return: a Construct representing a reference to an existing Deployment Group

        :stability: experimental
        '''
        attrs = LambdaDeploymentGroupAttributes(
            application=application,
            deployment_group_name=deployment_group_name,
            deployment_config=deployment_config,
        )

        return typing.cast(ILambdaDeploymentGroup, jsii.sinvoke(cls, "fromLambdaDeploymentGroupAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addAlarm")
    def add_alarm(self, alarm: _IAlarm_bf66c8d0) -> None:
        '''(experimental) Associates an additional alarm with this Deployment Group.

        :param alarm: the alarm to associate with this Deployment Group.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addAlarm", [alarm]))

    @jsii.member(jsii_name="addPostHook")
    def add_post_hook(self, post_hook: _IFunction_6e14f09e) -> None:
        '''(experimental) Associate a function to run after deployment completes.

        :param post_hook: function to run after deployment completes.

        :stability: experimental
        :throws: an error if a post-hook function is already configured
        '''
        return typing.cast(None, jsii.invoke(self, "addPostHook", [post_hook]))

    @jsii.member(jsii_name="addPreHook")
    def add_pre_hook(self, pre_hook: _IFunction_6e14f09e) -> None:
        '''(experimental) Associate a function to run before deployment begins.

        :param pre_hook: function to run before deployment beings.

        :stability: experimental
        :throws: an error if a pre-hook function is already configured
        '''
        return typing.cast(None, jsii.invoke(self, "addPreHook", [pre_hook]))

    @jsii.member(jsii_name="grantPutLifecycleEventHookExecutionStatus")
    def grant_put_lifecycle_event_hook_execution_status(
        self,
        grantee: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant a principal permission to codedeploy:PutLifecycleEventHookExecutionStatus on this deployment group resource.

        :param grantee: to grant permission to.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPutLifecycleEventHookExecutionStatus", [grantee]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="application")
    def application(self) -> ILambdaApplication:
        '''(experimental) The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.

        :stability: experimental
        '''
        return typing.cast(ILambdaApplication, jsii.get(self, "application"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> ILambdaDeploymentConfig:
        '''(experimental) The Deployment Configuration this Group uses.

        :stability: experimental
        '''
        return typing.cast(ILambdaDeploymentConfig, jsii.get(self, "deploymentConfig"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> builtins.str:
        '''(experimental) The ARN of this Deployment Group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> builtins.str:
        '''(experimental) The physical name of the CodeDeploy Deployment Group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="role")
    def role(self) -> _IRole_59af6f50:
        '''
        :stability: experimental
        '''
        return typing.cast(_IRole_59af6f50, jsii.get(self, "role"))


@jsii.data_type(
    jsii_type="monocdk.aws_codedeploy.LambdaDeploymentGroupAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "application": "application",
        "deployment_group_name": "deploymentGroupName",
        "deployment_config": "deploymentConfig",
    },
)
class LambdaDeploymentGroupAttributes:
    def __init__(
        self,
        *,
        application: ILambdaApplication,
        deployment_group_name: builtins.str,
        deployment_config: typing.Optional[ILambdaDeploymentConfig] = None,
    ) -> None:
        '''(experimental) Properties of a reference to a CodeDeploy Lambda Deployment Group.

        :param application: (experimental) The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.
        :param deployment_group_name: (experimental) The physical, human-readable name of the CodeDeploy Lambda Deployment Group that we are referencing.
        :param deployment_config: (experimental) The Deployment Configuration this Deployment Group uses. Default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES

        :see: LambdaDeploymentGroup#fromLambdaDeploymentGroupAttributes
        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "application": application,
            "deployment_group_name": deployment_group_name,
        }
        if deployment_config is not None:
            self._values["deployment_config"] = deployment_config

    @builtins.property
    def application(self) -> ILambdaApplication:
        '''(experimental) The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.

        :stability: experimental
        '''
        result = self._values.get("application")
        assert result is not None, "Required property 'application' is missing"
        return typing.cast(ILambdaApplication, result)

    @builtins.property
    def deployment_group_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the CodeDeploy Lambda Deployment Group that we are referencing.

        :stability: experimental
        '''
        result = self._values.get("deployment_group_name")
        assert result is not None, "Required property 'deployment_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deployment_config(self) -> typing.Optional[ILambdaDeploymentConfig]:
        '''(experimental) The Deployment Configuration this Deployment Group uses.

        :default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES

        :stability: experimental
        '''
        result = self._values.get("deployment_config")
        return typing.cast(typing.Optional[ILambdaDeploymentConfig], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaDeploymentGroupAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_codedeploy.LambdaDeploymentGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "alarms": "alarms",
        "application": "application",
        "auto_rollback": "autoRollback",
        "deployment_config": "deploymentConfig",
        "deployment_group_name": "deploymentGroupName",
        "ignore_poll_alarms_failure": "ignorePollAlarmsFailure",
        "post_hook": "postHook",
        "pre_hook": "preHook",
        "role": "role",
    },
)
class LambdaDeploymentGroupProps:
    def __init__(
        self,
        *,
        alias: _Alias_9e39972c,
        alarms: typing.Optional[typing.List[_IAlarm_bf66c8d0]] = None,
        application: typing.Optional[ILambdaApplication] = None,
        auto_rollback: typing.Optional[AutoRollbackConfig] = None,
        deployment_config: typing.Optional[ILambdaDeploymentConfig] = None,
        deployment_group_name: typing.Optional[builtins.str] = None,
        ignore_poll_alarms_failure: typing.Optional[builtins.bool] = None,
        post_hook: typing.Optional[_IFunction_6e14f09e] = None,
        pre_hook: typing.Optional[_IFunction_6e14f09e] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''(experimental) Construction properties for {@link LambdaDeploymentGroup}.

        :param alias: (experimental) Lambda Alias to shift traffic. Updating the version of the alias will trigger a CodeDeploy deployment. [disable-awslint:ref-via-interface] since we need to modify the alias CFN resource update policy
        :param alarms: (experimental) The CloudWatch alarms associated with this Deployment Group. CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger. Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method. Default: []
        :param application: (experimental) The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to. Default: - One will be created for you.
        :param auto_rollback: (experimental) The auto-rollback configuration for this Deployment Group. Default: - default AutoRollbackConfig.
        :param deployment_config: (experimental) The Deployment Configuration this Deployment Group uses. Default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES
        :param deployment_group_name: (experimental) The physical, human-readable name of the CodeDeploy Deployment Group. Default: - An auto-generated name will be used.
        :param ignore_poll_alarms_failure: (experimental) Whether to continue a deployment even if fetching the alarm status from CloudWatch failed. Default: false
        :param post_hook: (experimental) The Lambda function to run after traffic routing starts. Default: - None.
        :param pre_hook: (experimental) The Lambda function to run before traffic routing starts. Default: - None.
        :param role: (experimental) The service Role of this Deployment Group. Default: - A new Role will be created.

        :stability: experimental
        '''
        if isinstance(auto_rollback, dict):
            auto_rollback = AutoRollbackConfig(**auto_rollback)
        self._values: typing.Dict[str, typing.Any] = {
            "alias": alias,
        }
        if alarms is not None:
            self._values["alarms"] = alarms
        if application is not None:
            self._values["application"] = application
        if auto_rollback is not None:
            self._values["auto_rollback"] = auto_rollback
        if deployment_config is not None:
            self._values["deployment_config"] = deployment_config
        if deployment_group_name is not None:
            self._values["deployment_group_name"] = deployment_group_name
        if ignore_poll_alarms_failure is not None:
            self._values["ignore_poll_alarms_failure"] = ignore_poll_alarms_failure
        if post_hook is not None:
            self._values["post_hook"] = post_hook
        if pre_hook is not None:
            self._values["pre_hook"] = pre_hook
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def alias(self) -> _Alias_9e39972c:
        '''(experimental) Lambda Alias to shift traffic. Updating the version of the alias will trigger a CodeDeploy deployment.

        [disable-awslint:ref-via-interface] since we need to modify the alias CFN resource update policy

        :stability: experimental
        '''
        result = self._values.get("alias")
        assert result is not None, "Required property 'alias' is missing"
        return typing.cast(_Alias_9e39972c, result)

    @builtins.property
    def alarms(self) -> typing.Optional[typing.List[_IAlarm_bf66c8d0]]:
        '''(experimental) The CloudWatch alarms associated with this Deployment Group.

        CodeDeploy will stop (and optionally roll back)
        a deployment if during it any of the alarms trigger.

        Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method.

        :default: []

        :see: https://docs.aws.amazon.com/codedeploy/latest/userguide/monitoring-create-alarms.html
        :stability: experimental
        '''
        result = self._values.get("alarms")
        return typing.cast(typing.Optional[typing.List[_IAlarm_bf66c8d0]], result)

    @builtins.property
    def application(self) -> typing.Optional[ILambdaApplication]:
        '''(experimental) The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.

        :default: - One will be created for you.

        :stability: experimental
        '''
        result = self._values.get("application")
        return typing.cast(typing.Optional[ILambdaApplication], result)

    @builtins.property
    def auto_rollback(self) -> typing.Optional[AutoRollbackConfig]:
        '''(experimental) The auto-rollback configuration for this Deployment Group.

        :default: - default AutoRollbackConfig.

        :stability: experimental
        '''
        result = self._values.get("auto_rollback")
        return typing.cast(typing.Optional[AutoRollbackConfig], result)

    @builtins.property
    def deployment_config(self) -> typing.Optional[ILambdaDeploymentConfig]:
        '''(experimental) The Deployment Configuration this Deployment Group uses.

        :default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES

        :stability: experimental
        '''
        result = self._values.get("deployment_config")
        return typing.cast(typing.Optional[ILambdaDeploymentConfig], result)

    @builtins.property
    def deployment_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The physical, human-readable name of the CodeDeploy Deployment Group.

        :default: - An auto-generated name will be used.

        :stability: experimental
        '''
        result = self._values.get("deployment_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_poll_alarms_failure(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to continue a deployment even if fetching the alarm status from CloudWatch failed.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("ignore_poll_alarms_failure")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def post_hook(self) -> typing.Optional[_IFunction_6e14f09e]:
        '''(experimental) The Lambda function to run after traffic routing starts.

        :default: - None.

        :stability: experimental
        '''
        result = self._values.get("post_hook")
        return typing.cast(typing.Optional[_IFunction_6e14f09e], result)

    @builtins.property
    def pre_hook(self) -> typing.Optional[_IFunction_6e14f09e]:
        '''(experimental) The Lambda function to run before traffic routing starts.

        :default: - None.

        :stability: experimental
        '''
        result = self._values.get("pre_hook")
        return typing.cast(typing.Optional[_IFunction_6e14f09e], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The service Role of this Deployment Group.

        :default: - A new Role will be created.

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaDeploymentGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoadBalancer(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_codedeploy.LoadBalancer",
):
    '''(experimental) An interface of an abstract load balancer, as needed by CodeDeploy.

    Create instances using the static factory methods:
    {@link #classic}, {@link #application} and {@link #network}.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_LoadBalancerProxy"]:
        return _LoadBalancerProxy

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(LoadBalancer, self, [])

    @jsii.member(jsii_name="application") # type: ignore[misc]
    @builtins.classmethod
    def application(
        cls,
        alb_target_group: _ApplicationTargetGroup_5b334416,
    ) -> "LoadBalancer":
        '''(experimental) Creates a new CodeDeploy load balancer from an Application Load Balancer Target Group.

        :param alb_target_group: an ALB Target Group.

        :stability: experimental
        '''
        return typing.cast("LoadBalancer", jsii.sinvoke(cls, "application", [alb_target_group]))

    @jsii.member(jsii_name="classic") # type: ignore[misc]
    @builtins.classmethod
    def classic(cls, load_balancer: _LoadBalancer_a7de240f) -> "LoadBalancer":
        '''(experimental) Creates a new CodeDeploy load balancer from a Classic ELB Load Balancer.

        :param load_balancer: a classic ELB Load Balancer.

        :stability: experimental
        '''
        return typing.cast("LoadBalancer", jsii.sinvoke(cls, "classic", [load_balancer]))

    @jsii.member(jsii_name="network") # type: ignore[misc]
    @builtins.classmethod
    def network(cls, nlb_target_group: _NetworkTargetGroup_cfe3bed6) -> "LoadBalancer":
        '''(experimental) Creates a new CodeDeploy load balancer from a Network Load Balancer Target Group.

        :param nlb_target_group: an NLB Target Group.

        :stability: experimental
        '''
        return typing.cast("LoadBalancer", jsii.sinvoke(cls, "network", [nlb_target_group]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="generation")
    @abc.abstractmethod
    def generation(self) -> "LoadBalancerGeneration":
        '''
        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    @abc.abstractmethod
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...


class _LoadBalancerProxy(LoadBalancer):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="generation")
    def generation(self) -> "LoadBalancerGeneration":
        '''
        :stability: experimental
        '''
        return typing.cast("LoadBalancerGeneration", jsii.get(self, "generation"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.enum(jsii_type="monocdk.aws_codedeploy.LoadBalancerGeneration")
class LoadBalancerGeneration(enum.Enum):
    '''(experimental) The generations of AWS load balancing solutions.

    :stability: experimental
    '''

    FIRST = "FIRST"
    '''(experimental) The first generation (ELB Classic).

    :stability: experimental
    '''
    SECOND = "SECOND"
    '''(experimental) The second generation (ALB and NLB).

    :stability: experimental
    '''


class MinimumHealthyHosts(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codedeploy.MinimumHealthyHosts",
):
    '''(experimental) Minimum number of healthy hosts for a server deployment.

    :stability: experimental
    '''

    @jsii.member(jsii_name="count") # type: ignore[misc]
    @builtins.classmethod
    def count(cls, value: jsii.Number) -> "MinimumHealthyHosts":
        '''(experimental) The minimum healhty hosts threshold expressed as an absolute number.

        :param value: -

        :stability: experimental
        '''
        return typing.cast("MinimumHealthyHosts", jsii.sinvoke(cls, "count", [value]))

    @jsii.member(jsii_name="percentage") # type: ignore[misc]
    @builtins.classmethod
    def percentage(cls, value: jsii.Number) -> "MinimumHealthyHosts":
        '''(experimental) The minmum healhty hosts threshold expressed as a percentage of the fleet.

        :param value: -

        :stability: experimental
        '''
        return typing.cast("MinimumHealthyHosts", jsii.sinvoke(cls, "percentage", [value]))


@jsii.implements(IServerApplication)
class ServerApplication(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codedeploy.ServerApplication",
):
    '''(experimental) A CodeDeploy Application that deploys to EC2/on-premise instances.

    :stability: experimental
    :resource: AWS::CodeDeploy::Application
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        application_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param application_name: (experimental) The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used

        :stability: experimental
        '''
        props = ServerApplicationProps(application_name=application_name)

        jsii.create(ServerApplication, self, [scope, id, props])

    @jsii.member(jsii_name="fromServerApplicationName") # type: ignore[misc]
    @builtins.classmethod
    def from_server_application_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        server_application_name: builtins.str,
    ) -> IServerApplication:
        '''(experimental) Import an Application defined either outside the CDK app, or in a different region.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param server_application_name: the name of the application to import.

        :return: a Construct representing a reference to an existing Application

        :stability: experimental
        '''
        return typing.cast(IServerApplication, jsii.sinvoke(cls, "fromServerApplicationName", [scope, id, server_application_name]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))


@jsii.data_type(
    jsii_type="monocdk.aws_codedeploy.ServerApplicationProps",
    jsii_struct_bases=[],
    name_mapping={"application_name": "applicationName"},
)
class ServerApplicationProps:
    def __init__(
        self,
        *,
        application_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Construction properties for {@link ServerApplication}.

        :param application_name: (experimental) The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if application_name is not None:
            self._values["application_name"] = application_name

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The physical, human-readable name of the CodeDeploy Application.

        :default: an auto-generated name will be used

        :stability: experimental
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IServerDeploymentConfig)
class ServerDeploymentConfig(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codedeploy.ServerDeploymentConfig",
):
    '''(experimental) A custom Deployment Configuration for an EC2/on-premise Deployment Group.

    :stability: experimental
    :resource: AWS::CodeDeploy::DeploymentConfig
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        minimum_healthy_hosts: MinimumHealthyHosts,
        deployment_config_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param minimum_healthy_hosts: (experimental) Minimum number of healthy hosts.
        :param deployment_config_name: (experimental) The physical, human-readable name of the Deployment Configuration. Default: a name will be auto-generated

        :stability: experimental
        '''
        props = ServerDeploymentConfigProps(
            minimum_healthy_hosts=minimum_healthy_hosts,
            deployment_config_name=deployment_config_name,
        )

        jsii.create(ServerDeploymentConfig, self, [scope, id, props])

    @jsii.member(jsii_name="fromServerDeploymentConfigName") # type: ignore[misc]
    @builtins.classmethod
    def from_server_deployment_config_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        server_deployment_config_name: builtins.str,
    ) -> IServerDeploymentConfig:
        '''(experimental) Import a custom Deployment Configuration for an EC2/on-premise Deployment Group defined either outside the CDK app, or in a different region.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param server_deployment_config_name: the properties of the referenced custom Deployment Configuration.

        :return: a Construct representing a reference to an existing custom Deployment Configuration

        :stability: experimental
        '''
        return typing.cast(IServerDeploymentConfig, jsii.sinvoke(cls, "fromServerDeploymentConfigName", [scope, id, server_deployment_config_name]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="ALL_AT_ONCE")
    def ALL_AT_ONCE(cls) -> IServerDeploymentConfig:
        '''
        :stability: experimental
        '''
        return typing.cast(IServerDeploymentConfig, jsii.sget(cls, "ALL_AT_ONCE"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="HALF_AT_A_TIME")
    def HALF_AT_A_TIME(cls) -> IServerDeploymentConfig:
        '''
        :stability: experimental
        '''
        return typing.cast(IServerDeploymentConfig, jsii.sget(cls, "HALF_AT_A_TIME"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="ONE_AT_A_TIME")
    def ONE_AT_A_TIME(cls) -> IServerDeploymentConfig:
        '''
        :stability: experimental
        '''
        return typing.cast(IServerDeploymentConfig, jsii.sget(cls, "ONE_AT_A_TIME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigName"))


@jsii.data_type(
    jsii_type="monocdk.aws_codedeploy.ServerDeploymentConfigProps",
    jsii_struct_bases=[],
    name_mapping={
        "minimum_healthy_hosts": "minimumHealthyHosts",
        "deployment_config_name": "deploymentConfigName",
    },
)
class ServerDeploymentConfigProps:
    def __init__(
        self,
        *,
        minimum_healthy_hosts: MinimumHealthyHosts,
        deployment_config_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Construction properties of {@link ServerDeploymentConfig}.

        :param minimum_healthy_hosts: (experimental) Minimum number of healthy hosts.
        :param deployment_config_name: (experimental) The physical, human-readable name of the Deployment Configuration. Default: a name will be auto-generated

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "minimum_healthy_hosts": minimum_healthy_hosts,
        }
        if deployment_config_name is not None:
            self._values["deployment_config_name"] = deployment_config_name

    @builtins.property
    def minimum_healthy_hosts(self) -> MinimumHealthyHosts:
        '''(experimental) Minimum number of healthy hosts.

        :stability: experimental
        '''
        result = self._values.get("minimum_healthy_hosts")
        assert result is not None, "Required property 'minimum_healthy_hosts' is missing"
        return typing.cast(MinimumHealthyHosts, result)

    @builtins.property
    def deployment_config_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The physical, human-readable name of the Deployment Configuration.

        :default: a name will be auto-generated

        :stability: experimental
        '''
        result = self._values.get("deployment_config_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerDeploymentConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IServerDeploymentGroup)
class ServerDeploymentGroup(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codedeploy.ServerDeploymentGroup",
):
    '''(experimental) A CodeDeploy Deployment Group that deploys to EC2/on-premise instances.

    :stability: experimental
    :resource: AWS::CodeDeploy::DeploymentGroup
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        alarms: typing.Optional[typing.List[_IAlarm_bf66c8d0]] = None,
        application: typing.Optional[IServerApplication] = None,
        auto_rollback: typing.Optional[AutoRollbackConfig] = None,
        auto_scaling_groups: typing.Optional[typing.List[_IAutoScalingGroup_352723c6]] = None,
        deployment_config: typing.Optional[IServerDeploymentConfig] = None,
        deployment_group_name: typing.Optional[builtins.str] = None,
        ec2_instance_tags: typing.Optional[InstanceTagSet] = None,
        ignore_poll_alarms_failure: typing.Optional[builtins.bool] = None,
        install_agent: typing.Optional[builtins.bool] = None,
        load_balancer: typing.Optional[LoadBalancer] = None,
        on_premise_instance_tags: typing.Optional[InstanceTagSet] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param alarms: (experimental) The CloudWatch alarms associated with this Deployment Group. CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger. Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method. Default: []
        :param application: (experimental) The CodeDeploy EC2/on-premise Application this Deployment Group belongs to. Default: - A new Application will be created.
        :param auto_rollback: (experimental) The auto-rollback configuration for this Deployment Group. Default: - default AutoRollbackConfig.
        :param auto_scaling_groups: (experimental) The auto-scaling groups belonging to this Deployment Group. Auto-scaling groups can also be added after the Deployment Group is created using the {@link #addAutoScalingGroup} method. [disable-awslint:ref-via-interface] is needed because we update userdata for ASGs to install the codedeploy agent. Default: []
        :param deployment_config: (experimental) The EC2/on-premise Deployment Configuration to use for this Deployment Group. Default: ServerDeploymentConfig#OneAtATime
        :param deployment_group_name: (experimental) The physical, human-readable name of the CodeDeploy Deployment Group. Default: - An auto-generated name will be used.
        :param ec2_instance_tags: (experimental) All EC2 instances matching the given set of tags when a deployment occurs will be added to this Deployment Group. Default: - No additional EC2 instances will be added to the Deployment Group.
        :param ignore_poll_alarms_failure: (experimental) Whether to continue a deployment even if fetching the alarm status from CloudWatch failed. Default: false
        :param install_agent: (experimental) If you've provided any auto-scaling groups with the {@link #autoScalingGroups} property, you can set this property to add User Data that installs the CodeDeploy agent on the instances. Default: true
        :param load_balancer: (experimental) The load balancer to place in front of this Deployment Group. Can be created from either a classic Elastic Load Balancer, or an Application Load Balancer / Network Load Balancer Target Group. Default: - Deployment Group will not have a load balancer defined.
        :param on_premise_instance_tags: (experimental) All on-premise instances matching the given set of tags when a deployment occurs will be added to this Deployment Group. Default: - No additional on-premise instances will be added to the Deployment Group.
        :param role: (experimental) The service Role of this Deployment Group. Default: - A new Role will be created.

        :stability: experimental
        '''
        props = ServerDeploymentGroupProps(
            alarms=alarms,
            application=application,
            auto_rollback=auto_rollback,
            auto_scaling_groups=auto_scaling_groups,
            deployment_config=deployment_config,
            deployment_group_name=deployment_group_name,
            ec2_instance_tags=ec2_instance_tags,
            ignore_poll_alarms_failure=ignore_poll_alarms_failure,
            install_agent=install_agent,
            load_balancer=load_balancer,
            on_premise_instance_tags=on_premise_instance_tags,
            role=role,
        )

        jsii.create(ServerDeploymentGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromServerDeploymentGroupAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_server_deployment_group_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        application: IServerApplication,
        deployment_group_name: builtins.str,
        deployment_config: typing.Optional[IServerDeploymentConfig] = None,
    ) -> IServerDeploymentGroup:
        '''(experimental) Import an EC2/on-premise Deployment Group defined either outside the CDK app, or in a different region.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param application: (experimental) The reference to the CodeDeploy EC2/on-premise Application that this Deployment Group belongs to.
        :param deployment_group_name: (experimental) The physical, human-readable name of the CodeDeploy EC2/on-premise Deployment Group that we are referencing.
        :param deployment_config: (experimental) The Deployment Configuration this Deployment Group uses. Default: ServerDeploymentConfig#OneAtATime

        :return: a Construct representing a reference to an existing Deployment Group

        :stability: experimental
        '''
        attrs = ServerDeploymentGroupAttributes(
            application=application,
            deployment_group_name=deployment_group_name,
            deployment_config=deployment_config,
        )

        return typing.cast(IServerDeploymentGroup, jsii.sinvoke(cls, "fromServerDeploymentGroupAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addAlarm")
    def add_alarm(self, alarm: _IAlarm_bf66c8d0) -> None:
        '''(experimental) Associates an additional alarm with this Deployment Group.

        :param alarm: the alarm to associate with this Deployment Group.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addAlarm", [alarm]))

    @jsii.member(jsii_name="addAutoScalingGroup")
    def add_auto_scaling_group(self, asg: _AutoScalingGroup_604a934f) -> None:
        '''(experimental) Adds an additional auto-scaling group to this Deployment Group.

        :param asg: the auto-scaling group to add to this Deployment Group. [disable-awslint:ref-via-interface] is needed in order to install the code deploy agent by updating the ASGs user data.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addAutoScalingGroup", [asg]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="application")
    def application(self) -> IServerApplication:
        '''
        :stability: experimental
        '''
        return typing.cast(IServerApplication, jsii.get(self, "application"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> IServerDeploymentConfig:
        '''
        :stability: experimental
        '''
        return typing.cast(IServerDeploymentConfig, jsii.get(self, "deploymentConfig"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="autoScalingGroups")
    def auto_scaling_groups(
        self,
    ) -> typing.Optional[typing.List[_IAutoScalingGroup_352723c6]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[_IAutoScalingGroup_352723c6]], jsii.get(self, "autoScalingGroups"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IRole_59af6f50], jsii.get(self, "role"))


@jsii.data_type(
    jsii_type="monocdk.aws_codedeploy.ServerDeploymentGroupAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "application": "application",
        "deployment_group_name": "deploymentGroupName",
        "deployment_config": "deploymentConfig",
    },
)
class ServerDeploymentGroupAttributes:
    def __init__(
        self,
        *,
        application: IServerApplication,
        deployment_group_name: builtins.str,
        deployment_config: typing.Optional[IServerDeploymentConfig] = None,
    ) -> None:
        '''(experimental) Properties of a reference to a CodeDeploy EC2/on-premise Deployment Group.

        :param application: (experimental) The reference to the CodeDeploy EC2/on-premise Application that this Deployment Group belongs to.
        :param deployment_group_name: (experimental) The physical, human-readable name of the CodeDeploy EC2/on-premise Deployment Group that we are referencing.
        :param deployment_config: (experimental) The Deployment Configuration this Deployment Group uses. Default: ServerDeploymentConfig#OneAtATime

        :see: ServerDeploymentGroup#import
        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "application": application,
            "deployment_group_name": deployment_group_name,
        }
        if deployment_config is not None:
            self._values["deployment_config"] = deployment_config

    @builtins.property
    def application(self) -> IServerApplication:
        '''(experimental) The reference to the CodeDeploy EC2/on-premise Application that this Deployment Group belongs to.

        :stability: experimental
        '''
        result = self._values.get("application")
        assert result is not None, "Required property 'application' is missing"
        return typing.cast(IServerApplication, result)

    @builtins.property
    def deployment_group_name(self) -> builtins.str:
        '''(experimental) The physical, human-readable name of the CodeDeploy EC2/on-premise Deployment Group that we are referencing.

        :stability: experimental
        '''
        result = self._values.get("deployment_group_name")
        assert result is not None, "Required property 'deployment_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deployment_config(self) -> typing.Optional[IServerDeploymentConfig]:
        '''(experimental) The Deployment Configuration this Deployment Group uses.

        :default: ServerDeploymentConfig#OneAtATime

        :stability: experimental
        '''
        result = self._values.get("deployment_config")
        return typing.cast(typing.Optional[IServerDeploymentConfig], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerDeploymentGroupAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_codedeploy.ServerDeploymentGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "alarms": "alarms",
        "application": "application",
        "auto_rollback": "autoRollback",
        "auto_scaling_groups": "autoScalingGroups",
        "deployment_config": "deploymentConfig",
        "deployment_group_name": "deploymentGroupName",
        "ec2_instance_tags": "ec2InstanceTags",
        "ignore_poll_alarms_failure": "ignorePollAlarmsFailure",
        "install_agent": "installAgent",
        "load_balancer": "loadBalancer",
        "on_premise_instance_tags": "onPremiseInstanceTags",
        "role": "role",
    },
)
class ServerDeploymentGroupProps:
    def __init__(
        self,
        *,
        alarms: typing.Optional[typing.List[_IAlarm_bf66c8d0]] = None,
        application: typing.Optional[IServerApplication] = None,
        auto_rollback: typing.Optional[AutoRollbackConfig] = None,
        auto_scaling_groups: typing.Optional[typing.List[_IAutoScalingGroup_352723c6]] = None,
        deployment_config: typing.Optional[IServerDeploymentConfig] = None,
        deployment_group_name: typing.Optional[builtins.str] = None,
        ec2_instance_tags: typing.Optional[InstanceTagSet] = None,
        ignore_poll_alarms_failure: typing.Optional[builtins.bool] = None,
        install_agent: typing.Optional[builtins.bool] = None,
        load_balancer: typing.Optional[LoadBalancer] = None,
        on_premise_instance_tags: typing.Optional[InstanceTagSet] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''(experimental) Construction properties for {@link ServerDeploymentGroup}.

        :param alarms: (experimental) The CloudWatch alarms associated with this Deployment Group. CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger. Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method. Default: []
        :param application: (experimental) The CodeDeploy EC2/on-premise Application this Deployment Group belongs to. Default: - A new Application will be created.
        :param auto_rollback: (experimental) The auto-rollback configuration for this Deployment Group. Default: - default AutoRollbackConfig.
        :param auto_scaling_groups: (experimental) The auto-scaling groups belonging to this Deployment Group. Auto-scaling groups can also be added after the Deployment Group is created using the {@link #addAutoScalingGroup} method. [disable-awslint:ref-via-interface] is needed because we update userdata for ASGs to install the codedeploy agent. Default: []
        :param deployment_config: (experimental) The EC2/on-premise Deployment Configuration to use for this Deployment Group. Default: ServerDeploymentConfig#OneAtATime
        :param deployment_group_name: (experimental) The physical, human-readable name of the CodeDeploy Deployment Group. Default: - An auto-generated name will be used.
        :param ec2_instance_tags: (experimental) All EC2 instances matching the given set of tags when a deployment occurs will be added to this Deployment Group. Default: - No additional EC2 instances will be added to the Deployment Group.
        :param ignore_poll_alarms_failure: (experimental) Whether to continue a deployment even if fetching the alarm status from CloudWatch failed. Default: false
        :param install_agent: (experimental) If you've provided any auto-scaling groups with the {@link #autoScalingGroups} property, you can set this property to add User Data that installs the CodeDeploy agent on the instances. Default: true
        :param load_balancer: (experimental) The load balancer to place in front of this Deployment Group. Can be created from either a classic Elastic Load Balancer, or an Application Load Balancer / Network Load Balancer Target Group. Default: - Deployment Group will not have a load balancer defined.
        :param on_premise_instance_tags: (experimental) All on-premise instances matching the given set of tags when a deployment occurs will be added to this Deployment Group. Default: - No additional on-premise instances will be added to the Deployment Group.
        :param role: (experimental) The service Role of this Deployment Group. Default: - A new Role will be created.

        :stability: experimental
        '''
        if isinstance(auto_rollback, dict):
            auto_rollback = AutoRollbackConfig(**auto_rollback)
        self._values: typing.Dict[str, typing.Any] = {}
        if alarms is not None:
            self._values["alarms"] = alarms
        if application is not None:
            self._values["application"] = application
        if auto_rollback is not None:
            self._values["auto_rollback"] = auto_rollback
        if auto_scaling_groups is not None:
            self._values["auto_scaling_groups"] = auto_scaling_groups
        if deployment_config is not None:
            self._values["deployment_config"] = deployment_config
        if deployment_group_name is not None:
            self._values["deployment_group_name"] = deployment_group_name
        if ec2_instance_tags is not None:
            self._values["ec2_instance_tags"] = ec2_instance_tags
        if ignore_poll_alarms_failure is not None:
            self._values["ignore_poll_alarms_failure"] = ignore_poll_alarms_failure
        if install_agent is not None:
            self._values["install_agent"] = install_agent
        if load_balancer is not None:
            self._values["load_balancer"] = load_balancer
        if on_premise_instance_tags is not None:
            self._values["on_premise_instance_tags"] = on_premise_instance_tags
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def alarms(self) -> typing.Optional[typing.List[_IAlarm_bf66c8d0]]:
        '''(experimental) The CloudWatch alarms associated with this Deployment Group.

        CodeDeploy will stop (and optionally roll back)
        a deployment if during it any of the alarms trigger.

        Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method.

        :default: []

        :see: https://docs.aws.amazon.com/codedeploy/latest/userguide/monitoring-create-alarms.html
        :stability: experimental
        '''
        result = self._values.get("alarms")
        return typing.cast(typing.Optional[typing.List[_IAlarm_bf66c8d0]], result)

    @builtins.property
    def application(self) -> typing.Optional[IServerApplication]:
        '''(experimental) The CodeDeploy EC2/on-premise Application this Deployment Group belongs to.

        :default: - A new Application will be created.

        :stability: experimental
        '''
        result = self._values.get("application")
        return typing.cast(typing.Optional[IServerApplication], result)

    @builtins.property
    def auto_rollback(self) -> typing.Optional[AutoRollbackConfig]:
        '''(experimental) The auto-rollback configuration for this Deployment Group.

        :default: - default AutoRollbackConfig.

        :stability: experimental
        '''
        result = self._values.get("auto_rollback")
        return typing.cast(typing.Optional[AutoRollbackConfig], result)

    @builtins.property
    def auto_scaling_groups(
        self,
    ) -> typing.Optional[typing.List[_IAutoScalingGroup_352723c6]]:
        '''(experimental) The auto-scaling groups belonging to this Deployment Group.

        Auto-scaling groups can also be added after the Deployment Group is created
        using the {@link #addAutoScalingGroup} method.

        [disable-awslint:ref-via-interface] is needed because we update userdata
        for ASGs to install the codedeploy agent.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("auto_scaling_groups")
        return typing.cast(typing.Optional[typing.List[_IAutoScalingGroup_352723c6]], result)

    @builtins.property
    def deployment_config(self) -> typing.Optional[IServerDeploymentConfig]:
        '''(experimental) The EC2/on-premise Deployment Configuration to use for this Deployment Group.

        :default: ServerDeploymentConfig#OneAtATime

        :stability: experimental
        '''
        result = self._values.get("deployment_config")
        return typing.cast(typing.Optional[IServerDeploymentConfig], result)

    @builtins.property
    def deployment_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The physical, human-readable name of the CodeDeploy Deployment Group.

        :default: - An auto-generated name will be used.

        :stability: experimental
        '''
        result = self._values.get("deployment_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2_instance_tags(self) -> typing.Optional[InstanceTagSet]:
        '''(experimental) All EC2 instances matching the given set of tags when a deployment occurs will be added to this Deployment Group.

        :default: - No additional EC2 instances will be added to the Deployment Group.

        :stability: experimental
        '''
        result = self._values.get("ec2_instance_tags")
        return typing.cast(typing.Optional[InstanceTagSet], result)

    @builtins.property
    def ignore_poll_alarms_failure(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to continue a deployment even if fetching the alarm status from CloudWatch failed.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("ignore_poll_alarms_failure")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def install_agent(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If you've provided any auto-scaling groups with the {@link #autoScalingGroups} property, you can set this property to add User Data that installs the CodeDeploy agent on the instances.

        :default: true

        :see: https://docs.aws.amazon.com/codedeploy/latest/userguide/codedeploy-agent-operations-install.html
        :stability: experimental
        '''
        result = self._values.get("install_agent")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def load_balancer(self) -> typing.Optional[LoadBalancer]:
        '''(experimental) The load balancer to place in front of this Deployment Group.

        Can be created from either a classic Elastic Load Balancer,
        or an Application Load Balancer / Network Load Balancer Target Group.

        :default: - Deployment Group will not have a load balancer defined.

        :stability: experimental
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional[LoadBalancer], result)

    @builtins.property
    def on_premise_instance_tags(self) -> typing.Optional[InstanceTagSet]:
        '''(experimental) All on-premise instances matching the given set of tags when a deployment occurs will be added to this Deployment Group.

        :default: - No additional on-premise instances will be added to the Deployment Group.

        :stability: experimental
        '''
        result = self._values.get("on_premise_instance_tags")
        return typing.cast(typing.Optional[InstanceTagSet], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The service Role of this Deployment Group.

        :default: - A new Role will be created.

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerDeploymentGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ILambdaDeploymentConfig)
class CustomLambdaDeploymentConfig(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codedeploy.CustomLambdaDeploymentConfig",
):
    '''(experimental) A custom Deployment Configuration for a Lambda Deployment Group.

    :stability: experimental
    :resource: AWS::CodeDeploy::DeploymentGroup
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        interval: _Duration_070aa057,
        percentage: jsii.Number,
        type: CustomLambdaDeploymentConfigType,
        deployment_config_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param interval: (experimental) The interval, in number of minutes: - For LINEAR, how frequently additional traffic is shifted - For CANARY, how long to shift traffic before the full deployment.
        :param percentage: (experimental) The integer percentage of traffic to shift: - For LINEAR, the percentage to shift every interval - For CANARY, the percentage to shift until the interval passes, before the full deployment.
        :param type: (experimental) The type of deployment config, either CANARY or LINEAR.
        :param deployment_config_name: (experimental) The verbatim name of the deployment config. Must be unique per account/region. Other parameters cannot be updated if this name is provided. Default: - automatically generated name

        :stability: experimental
        '''
        props = CustomLambdaDeploymentConfigProps(
            interval=interval,
            percentage=percentage,
            type=type,
            deployment_config_name=deployment_config_name,
        )

        jsii.create(CustomLambdaDeploymentConfig, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> builtins.str:
        '''(experimental) The arn of the deployment config.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> builtins.str:
        '''(experimental) The name of the deployment config.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentConfigName"))


@jsii.implements(IEcsApplication)
class EcsApplication(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codedeploy.EcsApplication",
):
    '''(experimental) A CodeDeploy Application that deploys to an Amazon ECS service.

    :stability: experimental
    :resource: AWS::CodeDeploy::Application
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        application_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param application_name: (experimental) The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used

        :stability: experimental
        '''
        props = EcsApplicationProps(application_name=application_name)

        jsii.create(EcsApplication, self, [scope, id, props])

    @jsii.member(jsii_name="fromEcsApplicationName") # type: ignore[misc]
    @builtins.classmethod
    def from_ecs_application_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        ecs_application_name: builtins.str,
    ) -> IEcsApplication:
        '''(experimental) Import an Application defined either outside the CDK, or in a different CDK Stack.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param ecs_application_name: the name of the application to import.

        :return: a Construct representing a reference to an existing Application

        :stability: experimental
        '''
        return typing.cast(IEcsApplication, jsii.sinvoke(cls, "fromEcsApplicationName", [scope, id, ecs_application_name]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))


__all__ = [
    "AutoRollbackConfig",
    "CfnApplication",
    "CfnApplicationProps",
    "CfnDeploymentConfig",
    "CfnDeploymentConfigProps",
    "CfnDeploymentGroup",
    "CfnDeploymentGroupProps",
    "CustomLambdaDeploymentConfig",
    "CustomLambdaDeploymentConfigProps",
    "CustomLambdaDeploymentConfigType",
    "EcsApplication",
    "EcsApplicationProps",
    "EcsDeploymentConfig",
    "EcsDeploymentGroup",
    "EcsDeploymentGroupAttributes",
    "IEcsApplication",
    "IEcsDeploymentConfig",
    "IEcsDeploymentGroup",
    "ILambdaApplication",
    "ILambdaDeploymentConfig",
    "ILambdaDeploymentGroup",
    "IServerApplication",
    "IServerDeploymentConfig",
    "IServerDeploymentGroup",
    "InstanceTagSet",
    "LambdaApplication",
    "LambdaApplicationProps",
    "LambdaDeploymentConfig",
    "LambdaDeploymentConfigImportProps",
    "LambdaDeploymentGroup",
    "LambdaDeploymentGroupAttributes",
    "LambdaDeploymentGroupProps",
    "LoadBalancer",
    "LoadBalancerGeneration",
    "MinimumHealthyHosts",
    "ServerApplication",
    "ServerApplicationProps",
    "ServerDeploymentConfig",
    "ServerDeploymentConfigProps",
    "ServerDeploymentGroup",
    "ServerDeploymentGroupAttributes",
    "ServerDeploymentGroupProps",
]

publication.publish()
