'''
# Amazon Elasticsearch Service Construct Library

<!--BEGIN STABILITY BANNER-->---


Features                           | Stability
-----------------------------------|----------------------------------------------------------------
CFN Resources                      | ![Stable](https://img.shields.io/badge/stable-success.svg?style=for-the-badge)
Higher level constructs for Domain | ![Experimental](https://img.shields.io/badge/experimental-important.svg?style=for-the-badge)

> **CFN Resources:** All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always
> stable and safe to use.

<!-- -->

> **Experimental:** Higher level constructs in this module that are marked as experimental are
> under active development. They are subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and
> breaking changes will be announced in the release notes. This means that while you may use them,
> you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## Quick start

Create a development cluster by simply specifying the version:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_elasticsearch as es

dev_domain = es.Domain(self, "Domain",
    version=es.ElasticsearchVersion.V7_1
)
```

To perform version upgrades without replacing the entire domain, specify the `enableVersionUpgrade` property.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_elasticsearch as es

dev_domain = es.Domain(self, "Domain",
    version=es.ElasticsearchVersion.V7_9,
    enable_version_upgrade=True
)
```

Create a production grade cluster by also specifying things like capacity and az distribution

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
prod_domain = es.Domain(self, "Domain",
    version=es.ElasticsearchVersion.V7_1,
    capacity={
        "master_nodes": 5,
        "data_nodes": 20
    },
    ebs={
        "volume_size": 20
    },
    zone_awareness={
        "availability_zone_count": 3
    },
    logging={
        "slow_search_log_enabled": True,
        "app_log_enabled": True,
        "slow_index_log_enabled": True
    }
)
```

This creates an Elasticsearch cluster and automatically sets up log groups for
logging the domain logs and slow search logs.

## A note about SLR

Some cluster configurations (e.g VPC access) require the existence of the [`AWSServiceRoleForAmazonElasticsearchService`](https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/slr-es.html) Service-Linked Role.

When performing such operations via the AWS Console, this SLR is created automatically when needed. However, this is not the behavior when using CloudFormation. If an SLR is needed, but doesn't exist, you will encounter a failure message simlar to:

```console
Before you can proceed, you must enable a service-linked role to give Amazon ES...
```

To resolve this, you need to [create](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html#create-service-linked-role) the SLR. We recommend using the AWS CLI:

```console
aws iam create-service-linked-role --aws-service-name es.amazonaws.com
```

You can also create it using the CDK, **but note that only the first application deploying this will succeed**:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
slr = iam.CfnServiceLinkedRole(self, "ElasticSLR",
    aws_service_name="es.amazonaws.com"
)
```

## Importing existing domains

To import an existing domain into your CDK application, use the `Domain.fromDomainEndpoint` factory method.
This method accepts a domain endpoint of an already existing domain:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
domain_endpoint = "https://my-domain-jcjotrt6f7otem4sqcwbch3c4u.us-east-1.es.amazonaws.com"
domain = Domain.from_domain_endpoint(self, "ImportedDomain", domain_endpoint)
```

## Permissions

### IAM

Helper methods also exist for managing access to the domain.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lambda_ = lambda_.Function(self, "Lambda")

# Grant write access to the app-search index
domain.grant_index_write("app-search", lambda_)

# Grant read access to the 'app-search/_search' path
domain.grant_path_read("app-search/_search", lambda_)
```

## Encryption

The domain can also be created with encryption enabled:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
domain = es.Domain(self, "Domain",
    version=es.ElasticsearchVersion.V7_4,
    ebs={
        "volume_size": 100,
        "volume_type": EbsDeviceVolumeType.GENERAL_PURPOSE_SSD
    },
    node_to_node_encryption=True,
    encryption_at_rest={
        "enabled": True
    }
)
```

This sets up the domain with node to node encryption and encryption at
rest. You can also choose to supply your own KMS key to use for encryption at
rest.

## Metrics

Helper methods exist to access common domain metrics for example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
free_storage_space = domain.metric_free_storage_space()
master_sys_memory_utilization = domain.metric("MasterSysMemoryUtilization")
```

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## Fine grained access control

The domain can also be created with a master user configured. The password can
be supplied or dynamically created if not supplied.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
domain = es.Domain(self, "Domain",
    version=es.ElasticsearchVersion.V7_1,
    enforce_https=True,
    node_to_node_encryption=True,
    encryption_at_rest={
        "enabled": True
    },
    fine_grained_access_control={
        "master_user_name": "master-user"
    }
)

master_user_password = domain.master_user_password
```

## Using unsigned basic auth

For convenience, the domain can be configured to allow unsigned HTTP requests
that use basic auth. Unless the domain is configured to be part of a VPC this
means anyone can access the domain using the configured master username and
password.

To enable unsigned basic auth access the domain is configured with an access
policy that allows anyonmous requests, HTTPS required, node to node encryption,
encryption at rest and fine grained access control.

If the above settings are not set they will be configured as part of enabling
unsigned basic auth. If they are set with conflicting values, an error will be
thrown.

If no master user is configured a default master user is created with the
username `admin`.

If no password is configured a default master user password is created and
stored in the AWS Secrets Manager as secret. The secret has the prefix
`<domain id>MasterUser`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
domain = es.Domain(self, "Domain",
    version=es.ElasticsearchVersion.V7_1,
    use_unsigned_basic_auth=True
)

master_user_password = domain.master_user_password
```

## Audit logs

Audit logs can be enabled for a domain, but only when fine grained access control is enabled.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
domain = es.Domain(self, "Domain",
    version=es.ElasticsearchVersion.V7_1,
    enforce_https=True,
    node_to_node_encryption=True,
    encryption_at_rest={
        "enabled": True
    },
    fine_grained_access_control={
        "master_user_name": "master-user"
    },
    logging={
        "audit_log_enabled": True,
        "slow_search_log_enabled": True,
        "app_log_enabled": True,
        "slow_index_log_enabled": True
    }
)
```

## UltraWarm

UltraWarm nodes can be enabled to provide a cost-effective way to store large amounts of read-only data.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
domain = es.Domain(self, "Domain",
    version=es.ElasticsearchVersion.V7_9,
    capacity={
        "master_nodes": 2,
        "warm_nodes": 2,
        "warm_instance_type": "ultrawarm1.medium.elasticsearch"
    }
)
```

## Custom endpoint

Custom endpoints can be configured to reach the ES domain under a custom domain name.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Domain(stack, "Domain",
    version=ElasticsearchVersion.V7_7,
    custom_endpoint={
        "domain_name": "search.example.com"
    }
)
```

It is also possible to specify a custom certificate instead of the auto-generated one.

Additionally, an automatic CNAME-Record is created if a hosted zone is provided for the custom endpoint
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
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    Duration as _Duration_070aa057,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    RemovalPolicy as _RemovalPolicy_c97e7a20,
    Resource as _Resource_abff4495,
    SecretValue as _SecretValue_c18506ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_certificatemanager import ICertificate as _ICertificate_c7bbdc16
from ..aws_cloudwatch import (
    Metric as _Metric_5b2b8e58,
    MetricOptions as _MetricOptions_1c185ae8,
    Unit as _Unit_113c79f9,
)
from ..aws_ec2 import (
    EbsDeviceVolumeType as _EbsDeviceVolumeType_3b8e2d6d,
    ISecurityGroup as _ISecurityGroup_cdbba9d3,
    ISubnet as _ISubnet_0a12f914,
)
from ..aws_iam import (
    Grant as _Grant_bcb5eae7,
    IGrantable as _IGrantable_4c5a91d1,
    IRole as _IRole_59af6f50,
    PolicyStatement as _PolicyStatement_296fe8a3,
)
from ..aws_kms import IKey as _IKey_36930160
from ..aws_logs import ILogGroup as _ILogGroup_846e17a0
from ..aws_route53 import IHostedZone as _IHostedZone_78d5a9c9


@jsii.data_type(
    jsii_type="monocdk.aws_elasticsearch.AdvancedSecurityOptions",
    jsii_struct_bases=[],
    name_mapping={
        "master_user_arn": "masterUserArn",
        "master_user_name": "masterUserName",
        "master_user_password": "masterUserPassword",
    },
)
class AdvancedSecurityOptions:
    def __init__(
        self,
        *,
        master_user_arn: typing.Optional[builtins.str] = None,
        master_user_name: typing.Optional[builtins.str] = None,
        master_user_password: typing.Optional[_SecretValue_c18506ef] = None,
    ) -> None:
        '''(experimental) Specifies options for fine-grained access control.

        :param master_user_arn: (experimental) ARN for the master user. Only specify this or masterUserName, but not both. Default: - fine-grained access control is disabled
        :param master_user_name: (experimental) Username for the master user. Only specify this or masterUserArn, but not both. Default: - fine-grained access control is disabled
        :param master_user_password: (experimental) Password for the master user. You can use ``SecretValue.plainText`` to specify a password in plain text or use ``secretsmanager.Secret.fromSecretAttributes`` to reference a secret in Secrets Manager. Default: - A Secrets Manager generated password

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if master_user_arn is not None:
            self._values["master_user_arn"] = master_user_arn
        if master_user_name is not None:
            self._values["master_user_name"] = master_user_name
        if master_user_password is not None:
            self._values["master_user_password"] = master_user_password

    @builtins.property
    def master_user_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) ARN for the master user.

        Only specify this or masterUserName, but not both.

        :default: - fine-grained access control is disabled

        :stability: experimental
        '''
        result = self._values.get("master_user_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_user_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Username for the master user.

        Only specify this or masterUserArn, but not both.

        :default: - fine-grained access control is disabled

        :stability: experimental
        '''
        result = self._values.get("master_user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_user_password(self) -> typing.Optional[_SecretValue_c18506ef]:
        '''(experimental) Password for the master user.

        You can use ``SecretValue.plainText`` to specify a password in plain text or
        use ``secretsmanager.Secret.fromSecretAttributes`` to reference a secret in
        Secrets Manager.

        :default: - A Secrets Manager generated password

        :stability: experimental
        '''
        result = self._values.get("master_user_password")
        return typing.cast(typing.Optional[_SecretValue_c18506ef], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedSecurityOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_elasticsearch.CapacityConfig",
    jsii_struct_bases=[],
    name_mapping={
        "data_node_instance_type": "dataNodeInstanceType",
        "data_nodes": "dataNodes",
        "master_node_instance_type": "masterNodeInstanceType",
        "master_nodes": "masterNodes",
        "warm_instance_type": "warmInstanceType",
        "warm_nodes": "warmNodes",
    },
)
class CapacityConfig:
    def __init__(
        self,
        *,
        data_node_instance_type: typing.Optional[builtins.str] = None,
        data_nodes: typing.Optional[jsii.Number] = None,
        master_node_instance_type: typing.Optional[builtins.str] = None,
        master_nodes: typing.Optional[jsii.Number] = None,
        warm_instance_type: typing.Optional[builtins.str] = None,
        warm_nodes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Configures the capacity of the cluster such as the instance type and the number of instances.

        :param data_node_instance_type: (experimental) The instance type for your data nodes, such as ``m3.medium.elasticsearch``. For valid values, see `Supported Instance Types <https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/aes-supported-instance-types.html>`_ in the Amazon Elasticsearch Service Developer Guide. Default: - r5.large.elasticsearch
        :param data_nodes: (experimental) The number of data nodes (instances) to use in the Amazon ES domain. Default: - 1
        :param master_node_instance_type: (experimental) The hardware configuration of the computer that hosts the dedicated master node, such as ``m3.medium.elasticsearch``. For valid values, see [Supported Instance Types] (https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/aes-supported-instance-types.html) in the Amazon Elasticsearch Service Developer Guide. Default: - r5.large.elasticsearch
        :param master_nodes: (experimental) The number of instances to use for the master node. Default: - no dedicated master nodes
        :param warm_instance_type: (experimental) The instance type for your UltraWarm node, such as ``ultrawarm1.medium.elasticsearch``. For valid values, see [UltraWarm Storage Limits] (https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/aes-limits.html#limits-ultrawarm) in the Amazon Elasticsearch Service Developer Guide. Default: - ultrawarm1.medium.elasticsearch
        :param warm_nodes: (experimental) The number of UltraWarm nodes (instances) to use in the Amazon ES domain. Default: - no UltraWarm nodes

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if data_node_instance_type is not None:
            self._values["data_node_instance_type"] = data_node_instance_type
        if data_nodes is not None:
            self._values["data_nodes"] = data_nodes
        if master_node_instance_type is not None:
            self._values["master_node_instance_type"] = master_node_instance_type
        if master_nodes is not None:
            self._values["master_nodes"] = master_nodes
        if warm_instance_type is not None:
            self._values["warm_instance_type"] = warm_instance_type
        if warm_nodes is not None:
            self._values["warm_nodes"] = warm_nodes

    @builtins.property
    def data_node_instance_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) The instance type for your data nodes, such as ``m3.medium.elasticsearch``. For valid values, see `Supported Instance Types <https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/aes-supported-instance-types.html>`_ in the Amazon Elasticsearch Service Developer Guide.

        :default: - r5.large.elasticsearch

        :stability: experimental
        '''
        result = self._values.get("data_node_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_nodes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of data nodes (instances) to use in the Amazon ES domain.

        :default: - 1

        :stability: experimental
        '''
        result = self._values.get("data_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def master_node_instance_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) The hardware configuration of the computer that hosts the dedicated master node, such as ``m3.medium.elasticsearch``. For valid values, see [Supported Instance Types] (https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/aes-supported-instance-types.html) in the Amazon Elasticsearch Service Developer Guide.

        :default: - r5.large.elasticsearch

        :stability: experimental
        '''
        result = self._values.get("master_node_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_nodes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of instances to use for the master node.

        :default: - no dedicated master nodes

        :stability: experimental
        '''
        result = self._values.get("master_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def warm_instance_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) The instance type for your UltraWarm node, such as ``ultrawarm1.medium.elasticsearch``. For valid values, see [UltraWarm Storage Limits] (https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/aes-limits.html#limits-ultrawarm) in the Amazon Elasticsearch Service Developer Guide.

        :default: - ultrawarm1.medium.elasticsearch

        :stability: experimental
        '''
        result = self._values.get("warm_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def warm_nodes(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of UltraWarm nodes (instances) to use in the Amazon ES domain.

        :default: - no UltraWarm nodes

        :stability: experimental
        '''
        result = self._values.get("warm_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CapacityConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnDomain(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticsearch.CfnDomain",
):
    '''A CloudFormation ``AWS::Elasticsearch::Domain``.

    :cloudformationResource: AWS::Elasticsearch::Domain
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        access_policies: typing.Any = None,
        advanced_options: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        advanced_security_options: typing.Optional[typing.Union["CfnDomain.AdvancedSecurityOptionsInputProperty", _IResolvable_a771d0ef]] = None,
        cognito_options: typing.Optional[typing.Union["CfnDomain.CognitoOptionsProperty", _IResolvable_a771d0ef]] = None,
        domain_endpoint_options: typing.Optional[typing.Union["CfnDomain.DomainEndpointOptionsProperty", _IResolvable_a771d0ef]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        ebs_options: typing.Optional[typing.Union["CfnDomain.EBSOptionsProperty", _IResolvable_a771d0ef]] = None,
        elasticsearch_cluster_config: typing.Optional[typing.Union["CfnDomain.ElasticsearchClusterConfigProperty", _IResolvable_a771d0ef]] = None,
        elasticsearch_version: typing.Optional[builtins.str] = None,
        encryption_at_rest_options: typing.Optional[typing.Union["CfnDomain.EncryptionAtRestOptionsProperty", _IResolvable_a771d0ef]] = None,
        log_publishing_options: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnDomain.LogPublishingOptionProperty", _IResolvable_a771d0ef]]]] = None,
        node_to_node_encryption_options: typing.Optional[typing.Union["CfnDomain.NodeToNodeEncryptionOptionsProperty", _IResolvable_a771d0ef]] = None,
        snapshot_options: typing.Optional[typing.Union["CfnDomain.SnapshotOptionsProperty", _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
        vpc_options: typing.Optional[typing.Union["CfnDomain.VPCOptionsProperty", _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::Elasticsearch::Domain``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param access_policies: ``AWS::Elasticsearch::Domain.AccessPolicies``.
        :param advanced_options: ``AWS::Elasticsearch::Domain.AdvancedOptions``.
        :param advanced_security_options: ``AWS::Elasticsearch::Domain.AdvancedSecurityOptions``.
        :param cognito_options: ``AWS::Elasticsearch::Domain.CognitoOptions``.
        :param domain_endpoint_options: ``AWS::Elasticsearch::Domain.DomainEndpointOptions``.
        :param domain_name: ``AWS::Elasticsearch::Domain.DomainName``.
        :param ebs_options: ``AWS::Elasticsearch::Domain.EBSOptions``.
        :param elasticsearch_cluster_config: ``AWS::Elasticsearch::Domain.ElasticsearchClusterConfig``.
        :param elasticsearch_version: ``AWS::Elasticsearch::Domain.ElasticsearchVersion``.
        :param encryption_at_rest_options: ``AWS::Elasticsearch::Domain.EncryptionAtRestOptions``.
        :param log_publishing_options: ``AWS::Elasticsearch::Domain.LogPublishingOptions``.
        :param node_to_node_encryption_options: ``AWS::Elasticsearch::Domain.NodeToNodeEncryptionOptions``.
        :param snapshot_options: ``AWS::Elasticsearch::Domain.SnapshotOptions``.
        :param tags: ``AWS::Elasticsearch::Domain.Tags``.
        :param vpc_options: ``AWS::Elasticsearch::Domain.VPCOptions``.
        '''
        props = CfnDomainProps(
            access_policies=access_policies,
            advanced_options=advanced_options,
            advanced_security_options=advanced_security_options,
            cognito_options=cognito_options,
            domain_endpoint_options=domain_endpoint_options,
            domain_name=domain_name,
            ebs_options=ebs_options,
            elasticsearch_cluster_config=elasticsearch_cluster_config,
            elasticsearch_version=elasticsearch_version,
            encryption_at_rest_options=encryption_at_rest_options,
            log_publishing_options=log_publishing_options,
            node_to_node_encryption_options=node_to_node_encryption_options,
            snapshot_options=snapshot_options,
            tags=tags,
            vpc_options=vpc_options,
        )

        jsii.create(CfnDomain, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrDomainEndpoint")
    def attr_domain_endpoint(self) -> builtins.str:
        '''
        :cloudformationAttribute: DomainEndpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDomainEndpoint"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::Elasticsearch::Domain.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accessPolicies")
    def access_policies(self) -> typing.Any:
        '''``AWS::Elasticsearch::Domain.AccessPolicies``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-accesspolicies
        '''
        return typing.cast(typing.Any, jsii.get(self, "accessPolicies"))

    @access_policies.setter
    def access_policies(self, value: typing.Any) -> None:
        jsii.set(self, "accessPolicies", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="advancedOptions")
    def advanced_options(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Elasticsearch::Domain.AdvancedOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-advancedoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "advancedOptions"))

    @advanced_options.setter
    def advanced_options(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        jsii.set(self, "advancedOptions", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="advancedSecurityOptions")
    def advanced_security_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.AdvancedSecurityOptionsInputProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Elasticsearch::Domain.AdvancedSecurityOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-advancedsecurityoptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDomain.AdvancedSecurityOptionsInputProperty", _IResolvable_a771d0ef]], jsii.get(self, "advancedSecurityOptions"))

    @advanced_security_options.setter
    def advanced_security_options(
        self,
        value: typing.Optional[typing.Union["CfnDomain.AdvancedSecurityOptionsInputProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "advancedSecurityOptions", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cognitoOptions")
    def cognito_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.CognitoOptionsProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Elasticsearch::Domain.CognitoOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-cognitooptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDomain.CognitoOptionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "cognitoOptions"))

    @cognito_options.setter
    def cognito_options(
        self,
        value: typing.Optional[typing.Union["CfnDomain.CognitoOptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "cognitoOptions", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainEndpointOptions")
    def domain_endpoint_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.DomainEndpointOptionsProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Elasticsearch::Domain.DomainEndpointOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-domainendpointoptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDomain.DomainEndpointOptionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "domainEndpointOptions"))

    @domain_endpoint_options.setter
    def domain_endpoint_options(
        self,
        value: typing.Optional[typing.Union["CfnDomain.DomainEndpointOptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "domainEndpointOptions", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Elasticsearch::Domain.DomainName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-domainname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "domainName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ebsOptions")
    def ebs_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.EBSOptionsProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Elasticsearch::Domain.EBSOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-ebsoptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDomain.EBSOptionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "ebsOptions"))

    @ebs_options.setter
    def ebs_options(
        self,
        value: typing.Optional[typing.Union["CfnDomain.EBSOptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "ebsOptions", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="elasticsearchClusterConfig")
    def elasticsearch_cluster_config(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.ElasticsearchClusterConfigProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Elasticsearch::Domain.ElasticsearchClusterConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-elasticsearchclusterconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDomain.ElasticsearchClusterConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "elasticsearchClusterConfig"))

    @elasticsearch_cluster_config.setter
    def elasticsearch_cluster_config(
        self,
        value: typing.Optional[typing.Union["CfnDomain.ElasticsearchClusterConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "elasticsearchClusterConfig", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="elasticsearchVersion")
    def elasticsearch_version(self) -> typing.Optional[builtins.str]:
        '''``AWS::Elasticsearch::Domain.ElasticsearchVersion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-elasticsearchversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "elasticsearchVersion"))

    @elasticsearch_version.setter
    def elasticsearch_version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "elasticsearchVersion", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="encryptionAtRestOptions")
    def encryption_at_rest_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.EncryptionAtRestOptionsProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Elasticsearch::Domain.EncryptionAtRestOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-encryptionatrestoptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDomain.EncryptionAtRestOptionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "encryptionAtRestOptions"))

    @encryption_at_rest_options.setter
    def encryption_at_rest_options(
        self,
        value: typing.Optional[typing.Union["CfnDomain.EncryptionAtRestOptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "encryptionAtRestOptions", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logPublishingOptions")
    def log_publishing_options(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnDomain.LogPublishingOptionProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::Elasticsearch::Domain.LogPublishingOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-logpublishingoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnDomain.LogPublishingOptionProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "logPublishingOptions"))

    @log_publishing_options.setter
    def log_publishing_options(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnDomain.LogPublishingOptionProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "logPublishingOptions", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nodeToNodeEncryptionOptions")
    def node_to_node_encryption_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.NodeToNodeEncryptionOptionsProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Elasticsearch::Domain.NodeToNodeEncryptionOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-nodetonodeencryptionoptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDomain.NodeToNodeEncryptionOptionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "nodeToNodeEncryptionOptions"))

    @node_to_node_encryption_options.setter
    def node_to_node_encryption_options(
        self,
        value: typing.Optional[typing.Union["CfnDomain.NodeToNodeEncryptionOptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "nodeToNodeEncryptionOptions", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="snapshotOptions")
    def snapshot_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.SnapshotOptionsProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Elasticsearch::Domain.SnapshotOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-snapshotoptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDomain.SnapshotOptionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "snapshotOptions"))

    @snapshot_options.setter
    def snapshot_options(
        self,
        value: typing.Optional[typing.Union["CfnDomain.SnapshotOptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "snapshotOptions", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpcOptions")
    def vpc_options(
        self,
    ) -> typing.Optional[typing.Union["CfnDomain.VPCOptionsProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Elasticsearch::Domain.VPCOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-vpcoptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDomain.VPCOptionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "vpcOptions"))

    @vpc_options.setter
    def vpc_options(
        self,
        value: typing.Optional[typing.Union["CfnDomain.VPCOptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "vpcOptions", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticsearch.CfnDomain.AdvancedSecurityOptionsInputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "internal_user_database_enabled": "internalUserDatabaseEnabled",
            "master_user_options": "masterUserOptions",
        },
    )
    class AdvancedSecurityOptionsInputProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            internal_user_database_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            master_user_options: typing.Optional[typing.Union["CfnDomain.MasterUserOptionsProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param enabled: ``CfnDomain.AdvancedSecurityOptionsInputProperty.Enabled``.
            :param internal_user_database_enabled: ``CfnDomain.AdvancedSecurityOptionsInputProperty.InternalUserDatabaseEnabled``.
            :param master_user_options: ``CfnDomain.AdvancedSecurityOptionsInputProperty.MasterUserOptions``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-advancedsecurityoptionsinput.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if internal_user_database_enabled is not None:
                self._values["internal_user_database_enabled"] = internal_user_database_enabled
            if master_user_options is not None:
                self._values["master_user_options"] = master_user_options

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnDomain.AdvancedSecurityOptionsInputProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-advancedsecurityoptionsinput.html#cfn-elasticsearch-domain-advancedsecurityoptionsinput-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def internal_user_database_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnDomain.AdvancedSecurityOptionsInputProperty.InternalUserDatabaseEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-advancedsecurityoptionsinput.html#cfn-elasticsearch-domain-advancedsecurityoptionsinput-internaluserdatabaseenabled
            '''
            result = self._values.get("internal_user_database_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def master_user_options(
            self,
        ) -> typing.Optional[typing.Union["CfnDomain.MasterUserOptionsProperty", _IResolvable_a771d0ef]]:
            '''``CfnDomain.AdvancedSecurityOptionsInputProperty.MasterUserOptions``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-advancedsecurityoptionsinput.html#cfn-elasticsearch-domain-advancedsecurityoptionsinput-masteruseroptions
            '''
            result = self._values.get("master_user_options")
            return typing.cast(typing.Optional[typing.Union["CfnDomain.MasterUserOptionsProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdvancedSecurityOptionsInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticsearch.CfnDomain.CognitoOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "identity_pool_id": "identityPoolId",
            "role_arn": "roleArn",
            "user_pool_id": "userPoolId",
        },
    )
    class CognitoOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            identity_pool_id: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
            user_pool_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param enabled: ``CfnDomain.CognitoOptionsProperty.Enabled``.
            :param identity_pool_id: ``CfnDomain.CognitoOptionsProperty.IdentityPoolId``.
            :param role_arn: ``CfnDomain.CognitoOptionsProperty.RoleArn``.
            :param user_pool_id: ``CfnDomain.CognitoOptionsProperty.UserPoolId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-cognitooptions.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if identity_pool_id is not None:
                self._values["identity_pool_id"] = identity_pool_id
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if user_pool_id is not None:
                self._values["user_pool_id"] = user_pool_id

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnDomain.CognitoOptionsProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-cognitooptions.html#cfn-elasticsearch-domain-cognitooptions-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def identity_pool_id(self) -> typing.Optional[builtins.str]:
            '''``CfnDomain.CognitoOptionsProperty.IdentityPoolId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-cognitooptions.html#cfn-elasticsearch-domain-cognitooptions-identitypoolid
            '''
            result = self._values.get("identity_pool_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnDomain.CognitoOptionsProperty.RoleArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-cognitooptions.html#cfn-elasticsearch-domain-cognitooptions-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_pool_id(self) -> typing.Optional[builtins.str]:
            '''``CfnDomain.CognitoOptionsProperty.UserPoolId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-cognitooptions.html#cfn-elasticsearch-domain-cognitooptions-userpoolid
            '''
            result = self._values.get("user_pool_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CognitoOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticsearch.CfnDomain.DomainEndpointOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "custom_endpoint": "customEndpoint",
            "custom_endpoint_certificate_arn": "customEndpointCertificateArn",
            "custom_endpoint_enabled": "customEndpointEnabled",
            "enforce_https": "enforceHttps",
            "tls_security_policy": "tlsSecurityPolicy",
        },
    )
    class DomainEndpointOptionsProperty:
        def __init__(
            self,
            *,
            custom_endpoint: typing.Optional[builtins.str] = None,
            custom_endpoint_certificate_arn: typing.Optional[builtins.str] = None,
            custom_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            enforce_https: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            tls_security_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param custom_endpoint: ``CfnDomain.DomainEndpointOptionsProperty.CustomEndpoint``.
            :param custom_endpoint_certificate_arn: ``CfnDomain.DomainEndpointOptionsProperty.CustomEndpointCertificateArn``.
            :param custom_endpoint_enabled: ``CfnDomain.DomainEndpointOptionsProperty.CustomEndpointEnabled``.
            :param enforce_https: ``CfnDomain.DomainEndpointOptionsProperty.EnforceHTTPS``.
            :param tls_security_policy: ``CfnDomain.DomainEndpointOptionsProperty.TLSSecurityPolicy``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-domainendpointoptions.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if custom_endpoint is not None:
                self._values["custom_endpoint"] = custom_endpoint
            if custom_endpoint_certificate_arn is not None:
                self._values["custom_endpoint_certificate_arn"] = custom_endpoint_certificate_arn
            if custom_endpoint_enabled is not None:
                self._values["custom_endpoint_enabled"] = custom_endpoint_enabled
            if enforce_https is not None:
                self._values["enforce_https"] = enforce_https
            if tls_security_policy is not None:
                self._values["tls_security_policy"] = tls_security_policy

        @builtins.property
        def custom_endpoint(self) -> typing.Optional[builtins.str]:
            '''``CfnDomain.DomainEndpointOptionsProperty.CustomEndpoint``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-domainendpointoptions.html#cfn-elasticsearch-domain-domainendpointoptions-customendpoint
            '''
            result = self._values.get("custom_endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_endpoint_certificate_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnDomain.DomainEndpointOptionsProperty.CustomEndpointCertificateArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-domainendpointoptions.html#cfn-elasticsearch-domain-domainendpointoptions-customendpointcertificatearn
            '''
            result = self._values.get("custom_endpoint_certificate_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_endpoint_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnDomain.DomainEndpointOptionsProperty.CustomEndpointEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-domainendpointoptions.html#cfn-elasticsearch-domain-domainendpointoptions-customendpointenabled
            '''
            result = self._values.get("custom_endpoint_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def enforce_https(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnDomain.DomainEndpointOptionsProperty.EnforceHTTPS``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-domainendpointoptions.html#cfn-elasticsearch-domain-domainendpointoptions-enforcehttps
            '''
            result = self._values.get("enforce_https")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def tls_security_policy(self) -> typing.Optional[builtins.str]:
            '''``CfnDomain.DomainEndpointOptionsProperty.TLSSecurityPolicy``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-domainendpointoptions.html#cfn-elasticsearch-domain-domainendpointoptions-tlssecuritypolicy
            '''
            result = self._values.get("tls_security_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainEndpointOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticsearch.CfnDomain.EBSOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ebs_enabled": "ebsEnabled",
            "iops": "iops",
            "volume_size": "volumeSize",
            "volume_type": "volumeType",
        },
    )
    class EBSOptionsProperty:
        def __init__(
            self,
            *,
            ebs_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            iops: typing.Optional[jsii.Number] = None,
            volume_size: typing.Optional[jsii.Number] = None,
            volume_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param ebs_enabled: ``CfnDomain.EBSOptionsProperty.EBSEnabled``.
            :param iops: ``CfnDomain.EBSOptionsProperty.Iops``.
            :param volume_size: ``CfnDomain.EBSOptionsProperty.VolumeSize``.
            :param volume_type: ``CfnDomain.EBSOptionsProperty.VolumeType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-ebsoptions.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if ebs_enabled is not None:
                self._values["ebs_enabled"] = ebs_enabled
            if iops is not None:
                self._values["iops"] = iops
            if volume_size is not None:
                self._values["volume_size"] = volume_size
            if volume_type is not None:
                self._values["volume_type"] = volume_type

        @builtins.property
        def ebs_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnDomain.EBSOptionsProperty.EBSEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-ebsoptions.html#cfn-elasticsearch-domain-ebsoptions-ebsenabled
            '''
            result = self._values.get("ebs_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            '''``CfnDomain.EBSOptionsProperty.Iops``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-ebsoptions.html#cfn-elasticsearch-domain-ebsoptions-iops
            '''
            result = self._values.get("iops")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_size(self) -> typing.Optional[jsii.Number]:
            '''``CfnDomain.EBSOptionsProperty.VolumeSize``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-ebsoptions.html#cfn-elasticsearch-domain-ebsoptions-volumesize
            '''
            result = self._values.get("volume_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volume_type(self) -> typing.Optional[builtins.str]:
            '''``CfnDomain.EBSOptionsProperty.VolumeType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-ebsoptions.html#cfn-elasticsearch-domain-ebsoptions-volumetype
            '''
            result = self._values.get("volume_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EBSOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticsearch.CfnDomain.ElasticsearchClusterConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dedicated_master_count": "dedicatedMasterCount",
            "dedicated_master_enabled": "dedicatedMasterEnabled",
            "dedicated_master_type": "dedicatedMasterType",
            "instance_count": "instanceCount",
            "instance_type": "instanceType",
            "warm_count": "warmCount",
            "warm_enabled": "warmEnabled",
            "warm_type": "warmType",
            "zone_awareness_config": "zoneAwarenessConfig",
            "zone_awareness_enabled": "zoneAwarenessEnabled",
        },
    )
    class ElasticsearchClusterConfigProperty:
        def __init__(
            self,
            *,
            dedicated_master_count: typing.Optional[jsii.Number] = None,
            dedicated_master_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            dedicated_master_type: typing.Optional[builtins.str] = None,
            instance_count: typing.Optional[jsii.Number] = None,
            instance_type: typing.Optional[builtins.str] = None,
            warm_count: typing.Optional[jsii.Number] = None,
            warm_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            warm_type: typing.Optional[builtins.str] = None,
            zone_awareness_config: typing.Optional[typing.Union["CfnDomain.ZoneAwarenessConfigProperty", _IResolvable_a771d0ef]] = None,
            zone_awareness_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param dedicated_master_count: ``CfnDomain.ElasticsearchClusterConfigProperty.DedicatedMasterCount``.
            :param dedicated_master_enabled: ``CfnDomain.ElasticsearchClusterConfigProperty.DedicatedMasterEnabled``.
            :param dedicated_master_type: ``CfnDomain.ElasticsearchClusterConfigProperty.DedicatedMasterType``.
            :param instance_count: ``CfnDomain.ElasticsearchClusterConfigProperty.InstanceCount``.
            :param instance_type: ``CfnDomain.ElasticsearchClusterConfigProperty.InstanceType``.
            :param warm_count: ``CfnDomain.ElasticsearchClusterConfigProperty.WarmCount``.
            :param warm_enabled: ``CfnDomain.ElasticsearchClusterConfigProperty.WarmEnabled``.
            :param warm_type: ``CfnDomain.ElasticsearchClusterConfigProperty.WarmType``.
            :param zone_awareness_config: ``CfnDomain.ElasticsearchClusterConfigProperty.ZoneAwarenessConfig``.
            :param zone_awareness_enabled: ``CfnDomain.ElasticsearchClusterConfigProperty.ZoneAwarenessEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if dedicated_master_count is not None:
                self._values["dedicated_master_count"] = dedicated_master_count
            if dedicated_master_enabled is not None:
                self._values["dedicated_master_enabled"] = dedicated_master_enabled
            if dedicated_master_type is not None:
                self._values["dedicated_master_type"] = dedicated_master_type
            if instance_count is not None:
                self._values["instance_count"] = instance_count
            if instance_type is not None:
                self._values["instance_type"] = instance_type
            if warm_count is not None:
                self._values["warm_count"] = warm_count
            if warm_enabled is not None:
                self._values["warm_enabled"] = warm_enabled
            if warm_type is not None:
                self._values["warm_type"] = warm_type
            if zone_awareness_config is not None:
                self._values["zone_awareness_config"] = zone_awareness_config
            if zone_awareness_enabled is not None:
                self._values["zone_awareness_enabled"] = zone_awareness_enabled

        @builtins.property
        def dedicated_master_count(self) -> typing.Optional[jsii.Number]:
            '''``CfnDomain.ElasticsearchClusterConfigProperty.DedicatedMasterCount``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-dedicatedmastercount
            '''
            result = self._values.get("dedicated_master_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def dedicated_master_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnDomain.ElasticsearchClusterConfigProperty.DedicatedMasterEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-dedicatedmasterenabled
            '''
            result = self._values.get("dedicated_master_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def dedicated_master_type(self) -> typing.Optional[builtins.str]:
            '''``CfnDomain.ElasticsearchClusterConfigProperty.DedicatedMasterType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-dedicatedmastertype
            '''
            result = self._values.get("dedicated_master_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_count(self) -> typing.Optional[jsii.Number]:
            '''``CfnDomain.ElasticsearchClusterConfigProperty.InstanceCount``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-instancecount
            '''
            result = self._values.get("instance_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def instance_type(self) -> typing.Optional[builtins.str]:
            '''``CfnDomain.ElasticsearchClusterConfigProperty.InstanceType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-instnacetype
            '''
            result = self._values.get("instance_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def warm_count(self) -> typing.Optional[jsii.Number]:
            '''``CfnDomain.ElasticsearchClusterConfigProperty.WarmCount``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticsearchclusterconfig-warmcount
            '''
            result = self._values.get("warm_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def warm_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnDomain.ElasticsearchClusterConfigProperty.WarmEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticsearchclusterconfig-warmenabled
            '''
            result = self._values.get("warm_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def warm_type(self) -> typing.Optional[builtins.str]:
            '''``CfnDomain.ElasticsearchClusterConfigProperty.WarmType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticsearchclusterconfig-warmtype
            '''
            result = self._values.get("warm_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def zone_awareness_config(
            self,
        ) -> typing.Optional[typing.Union["CfnDomain.ZoneAwarenessConfigProperty", _IResolvable_a771d0ef]]:
            '''``CfnDomain.ElasticsearchClusterConfigProperty.ZoneAwarenessConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticsearchclusterconfig-zoneawarenessconfig
            '''
            result = self._values.get("zone_awareness_config")
            return typing.cast(typing.Optional[typing.Union["CfnDomain.ZoneAwarenessConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def zone_awareness_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnDomain.ElasticsearchClusterConfigProperty.ZoneAwarenessEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-zoneawarenessenabled
            '''
            result = self._values.get("zone_awareness_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ElasticsearchClusterConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticsearch.CfnDomain.EncryptionAtRestOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "kms_key_id": "kmsKeyId"},
    )
    class EncryptionAtRestOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            kms_key_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param enabled: ``CfnDomain.EncryptionAtRestOptionsProperty.Enabled``.
            :param kms_key_id: ``CfnDomain.EncryptionAtRestOptionsProperty.KmsKeyId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-encryptionatrestoptions.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnDomain.EncryptionAtRestOptionsProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-encryptionatrestoptions.html#cfn-elasticsearch-domain-encryptionatrestoptions-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''``CfnDomain.EncryptionAtRestOptionsProperty.KmsKeyId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-encryptionatrestoptions.html#cfn-elasticsearch-domain-encryptionatrestoptions-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionAtRestOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticsearch.CfnDomain.LogPublishingOptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logs_log_group_arn": "cloudWatchLogsLogGroupArn",
            "enabled": "enabled",
        },
    )
    class LogPublishingOptionProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs_log_group_arn: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param cloud_watch_logs_log_group_arn: ``CfnDomain.LogPublishingOptionProperty.CloudWatchLogsLogGroupArn``.
            :param enabled: ``CfnDomain.LogPublishingOptionProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-logpublishingoption.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if cloud_watch_logs_log_group_arn is not None:
                self._values["cloud_watch_logs_log_group_arn"] = cloud_watch_logs_log_group_arn
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def cloud_watch_logs_log_group_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnDomain.LogPublishingOptionProperty.CloudWatchLogsLogGroupArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-logpublishingoption.html#cfn-elasticsearch-domain-logpublishingoption-cloudwatchlogsloggrouparn
            '''
            result = self._values.get("cloud_watch_logs_log_group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnDomain.LogPublishingOptionProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-logpublishingoption.html#cfn-elasticsearch-domain-logpublishingoption-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogPublishingOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticsearch.CfnDomain.MasterUserOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "master_user_arn": "masterUserArn",
            "master_user_name": "masterUserName",
            "master_user_password": "masterUserPassword",
        },
    )
    class MasterUserOptionsProperty:
        def __init__(
            self,
            *,
            master_user_arn: typing.Optional[builtins.str] = None,
            master_user_name: typing.Optional[builtins.str] = None,
            master_user_password: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param master_user_arn: ``CfnDomain.MasterUserOptionsProperty.MasterUserARN``.
            :param master_user_name: ``CfnDomain.MasterUserOptionsProperty.MasterUserName``.
            :param master_user_password: ``CfnDomain.MasterUserOptionsProperty.MasterUserPassword``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-masteruseroptions.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if master_user_arn is not None:
                self._values["master_user_arn"] = master_user_arn
            if master_user_name is not None:
                self._values["master_user_name"] = master_user_name
            if master_user_password is not None:
                self._values["master_user_password"] = master_user_password

        @builtins.property
        def master_user_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnDomain.MasterUserOptionsProperty.MasterUserARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-masteruseroptions.html#cfn-elasticsearch-domain-masteruseroptions-masteruserarn
            '''
            result = self._values.get("master_user_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def master_user_name(self) -> typing.Optional[builtins.str]:
            '''``CfnDomain.MasterUserOptionsProperty.MasterUserName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-masteruseroptions.html#cfn-elasticsearch-domain-masteruseroptions-masterusername
            '''
            result = self._values.get("master_user_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def master_user_password(self) -> typing.Optional[builtins.str]:
            '''``CfnDomain.MasterUserOptionsProperty.MasterUserPassword``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-masteruseroptions.html#cfn-elasticsearch-domain-masteruseroptions-masteruserpassword
            '''
            result = self._values.get("master_user_password")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MasterUserOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticsearch.CfnDomain.NodeToNodeEncryptionOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class NodeToNodeEncryptionOptionsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param enabled: ``CfnDomain.NodeToNodeEncryptionOptionsProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-nodetonodeencryptionoptions.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnDomain.NodeToNodeEncryptionOptionsProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-nodetonodeencryptionoptions.html#cfn-elasticsearch-domain-nodetonodeencryptionoptions-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeToNodeEncryptionOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticsearch.CfnDomain.SnapshotOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"automated_snapshot_start_hour": "automatedSnapshotStartHour"},
    )
    class SnapshotOptionsProperty:
        def __init__(
            self,
            *,
            automated_snapshot_start_hour: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param automated_snapshot_start_hour: ``CfnDomain.SnapshotOptionsProperty.AutomatedSnapshotStartHour``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-snapshotoptions.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if automated_snapshot_start_hour is not None:
                self._values["automated_snapshot_start_hour"] = automated_snapshot_start_hour

        @builtins.property
        def automated_snapshot_start_hour(self) -> typing.Optional[jsii.Number]:
            '''``CfnDomain.SnapshotOptionsProperty.AutomatedSnapshotStartHour``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-snapshotoptions.html#cfn-elasticsearch-domain-snapshotoptions-automatedsnapshotstarthour
            '''
            result = self._values.get("automated_snapshot_start_hour")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnapshotOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticsearch.CfnDomain.VPCOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class VPCOptionsProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            '''
            :param security_group_ids: ``CfnDomain.VPCOptionsProperty.SecurityGroupIds``.
            :param subnet_ids: ``CfnDomain.VPCOptionsProperty.SubnetIds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-vpcoptions.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnDomain.VPCOptionsProperty.SecurityGroupIds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-vpcoptions.html#cfn-elasticsearch-domain-vpcoptions-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnDomain.VPCOptionsProperty.SubnetIds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-vpcoptions.html#cfn-elasticsearch-domain-vpcoptions-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VPCOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_elasticsearch.CfnDomain.ZoneAwarenessConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"availability_zone_count": "availabilityZoneCount"},
    )
    class ZoneAwarenessConfigProperty:
        def __init__(
            self,
            *,
            availability_zone_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param availability_zone_count: ``CfnDomain.ZoneAwarenessConfigProperty.AvailabilityZoneCount``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-zoneawarenessconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if availability_zone_count is not None:
                self._values["availability_zone_count"] = availability_zone_count

        @builtins.property
        def availability_zone_count(self) -> typing.Optional[jsii.Number]:
            '''``CfnDomain.ZoneAwarenessConfigProperty.AvailabilityZoneCount``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-zoneawarenessconfig.html#cfn-elasticsearch-domain-zoneawarenessconfig-availabilityzonecount
            '''
            result = self._values.get("availability_zone_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZoneAwarenessConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_elasticsearch.CfnDomainProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_policies": "accessPolicies",
        "advanced_options": "advancedOptions",
        "advanced_security_options": "advancedSecurityOptions",
        "cognito_options": "cognitoOptions",
        "domain_endpoint_options": "domainEndpointOptions",
        "domain_name": "domainName",
        "ebs_options": "ebsOptions",
        "elasticsearch_cluster_config": "elasticsearchClusterConfig",
        "elasticsearch_version": "elasticsearchVersion",
        "encryption_at_rest_options": "encryptionAtRestOptions",
        "log_publishing_options": "logPublishingOptions",
        "node_to_node_encryption_options": "nodeToNodeEncryptionOptions",
        "snapshot_options": "snapshotOptions",
        "tags": "tags",
        "vpc_options": "vpcOptions",
    },
)
class CfnDomainProps:
    def __init__(
        self,
        *,
        access_policies: typing.Any = None,
        advanced_options: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        advanced_security_options: typing.Optional[typing.Union[CfnDomain.AdvancedSecurityOptionsInputProperty, _IResolvable_a771d0ef]] = None,
        cognito_options: typing.Optional[typing.Union[CfnDomain.CognitoOptionsProperty, _IResolvable_a771d0ef]] = None,
        domain_endpoint_options: typing.Optional[typing.Union[CfnDomain.DomainEndpointOptionsProperty, _IResolvable_a771d0ef]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        ebs_options: typing.Optional[typing.Union[CfnDomain.EBSOptionsProperty, _IResolvable_a771d0ef]] = None,
        elasticsearch_cluster_config: typing.Optional[typing.Union[CfnDomain.ElasticsearchClusterConfigProperty, _IResolvable_a771d0ef]] = None,
        elasticsearch_version: typing.Optional[builtins.str] = None,
        encryption_at_rest_options: typing.Optional[typing.Union[CfnDomain.EncryptionAtRestOptionsProperty, _IResolvable_a771d0ef]] = None,
        log_publishing_options: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnDomain.LogPublishingOptionProperty, _IResolvable_a771d0ef]]]] = None,
        node_to_node_encryption_options: typing.Optional[typing.Union[CfnDomain.NodeToNodeEncryptionOptionsProperty, _IResolvable_a771d0ef]] = None,
        snapshot_options: typing.Optional[typing.Union[CfnDomain.SnapshotOptionsProperty, _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
        vpc_options: typing.Optional[typing.Union[CfnDomain.VPCOptionsProperty, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Elasticsearch::Domain``.

        :param access_policies: ``AWS::Elasticsearch::Domain.AccessPolicies``.
        :param advanced_options: ``AWS::Elasticsearch::Domain.AdvancedOptions``.
        :param advanced_security_options: ``AWS::Elasticsearch::Domain.AdvancedSecurityOptions``.
        :param cognito_options: ``AWS::Elasticsearch::Domain.CognitoOptions``.
        :param domain_endpoint_options: ``AWS::Elasticsearch::Domain.DomainEndpointOptions``.
        :param domain_name: ``AWS::Elasticsearch::Domain.DomainName``.
        :param ebs_options: ``AWS::Elasticsearch::Domain.EBSOptions``.
        :param elasticsearch_cluster_config: ``AWS::Elasticsearch::Domain.ElasticsearchClusterConfig``.
        :param elasticsearch_version: ``AWS::Elasticsearch::Domain.ElasticsearchVersion``.
        :param encryption_at_rest_options: ``AWS::Elasticsearch::Domain.EncryptionAtRestOptions``.
        :param log_publishing_options: ``AWS::Elasticsearch::Domain.LogPublishingOptions``.
        :param node_to_node_encryption_options: ``AWS::Elasticsearch::Domain.NodeToNodeEncryptionOptions``.
        :param snapshot_options: ``AWS::Elasticsearch::Domain.SnapshotOptions``.
        :param tags: ``AWS::Elasticsearch::Domain.Tags``.
        :param vpc_options: ``AWS::Elasticsearch::Domain.VPCOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if access_policies is not None:
            self._values["access_policies"] = access_policies
        if advanced_options is not None:
            self._values["advanced_options"] = advanced_options
        if advanced_security_options is not None:
            self._values["advanced_security_options"] = advanced_security_options
        if cognito_options is not None:
            self._values["cognito_options"] = cognito_options
        if domain_endpoint_options is not None:
            self._values["domain_endpoint_options"] = domain_endpoint_options
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if ebs_options is not None:
            self._values["ebs_options"] = ebs_options
        if elasticsearch_cluster_config is not None:
            self._values["elasticsearch_cluster_config"] = elasticsearch_cluster_config
        if elasticsearch_version is not None:
            self._values["elasticsearch_version"] = elasticsearch_version
        if encryption_at_rest_options is not None:
            self._values["encryption_at_rest_options"] = encryption_at_rest_options
        if log_publishing_options is not None:
            self._values["log_publishing_options"] = log_publishing_options
        if node_to_node_encryption_options is not None:
            self._values["node_to_node_encryption_options"] = node_to_node_encryption_options
        if snapshot_options is not None:
            self._values["snapshot_options"] = snapshot_options
        if tags is not None:
            self._values["tags"] = tags
        if vpc_options is not None:
            self._values["vpc_options"] = vpc_options

    @builtins.property
    def access_policies(self) -> typing.Any:
        '''``AWS::Elasticsearch::Domain.AccessPolicies``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-accesspolicies
        '''
        result = self._values.get("access_policies")
        return typing.cast(typing.Any, result)

    @builtins.property
    def advanced_options(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Elasticsearch::Domain.AdvancedOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-advancedoptions
        '''
        result = self._values.get("advanced_options")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def advanced_security_options(
        self,
    ) -> typing.Optional[typing.Union[CfnDomain.AdvancedSecurityOptionsInputProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Elasticsearch::Domain.AdvancedSecurityOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-advancedsecurityoptions
        '''
        result = self._values.get("advanced_security_options")
        return typing.cast(typing.Optional[typing.Union[CfnDomain.AdvancedSecurityOptionsInputProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def cognito_options(
        self,
    ) -> typing.Optional[typing.Union[CfnDomain.CognitoOptionsProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Elasticsearch::Domain.CognitoOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-cognitooptions
        '''
        result = self._values.get("cognito_options")
        return typing.cast(typing.Optional[typing.Union[CfnDomain.CognitoOptionsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def domain_endpoint_options(
        self,
    ) -> typing.Optional[typing.Union[CfnDomain.DomainEndpointOptionsProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Elasticsearch::Domain.DomainEndpointOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-domainendpointoptions
        '''
        result = self._values.get("domain_endpoint_options")
        return typing.cast(typing.Optional[typing.Union[CfnDomain.DomainEndpointOptionsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Elasticsearch::Domain.DomainName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ebs_options(
        self,
    ) -> typing.Optional[typing.Union[CfnDomain.EBSOptionsProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Elasticsearch::Domain.EBSOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-ebsoptions
        '''
        result = self._values.get("ebs_options")
        return typing.cast(typing.Optional[typing.Union[CfnDomain.EBSOptionsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def elasticsearch_cluster_config(
        self,
    ) -> typing.Optional[typing.Union[CfnDomain.ElasticsearchClusterConfigProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Elasticsearch::Domain.ElasticsearchClusterConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-elasticsearchclusterconfig
        '''
        result = self._values.get("elasticsearch_cluster_config")
        return typing.cast(typing.Optional[typing.Union[CfnDomain.ElasticsearchClusterConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def elasticsearch_version(self) -> typing.Optional[builtins.str]:
        '''``AWS::Elasticsearch::Domain.ElasticsearchVersion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-elasticsearchversion
        '''
        result = self._values.get("elasticsearch_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_at_rest_options(
        self,
    ) -> typing.Optional[typing.Union[CfnDomain.EncryptionAtRestOptionsProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Elasticsearch::Domain.EncryptionAtRestOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-encryptionatrestoptions
        '''
        result = self._values.get("encryption_at_rest_options")
        return typing.cast(typing.Optional[typing.Union[CfnDomain.EncryptionAtRestOptionsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def log_publishing_options(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnDomain.LogPublishingOptionProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::Elasticsearch::Domain.LogPublishingOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-logpublishingoptions
        '''
        result = self._values.get("log_publishing_options")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnDomain.LogPublishingOptionProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def node_to_node_encryption_options(
        self,
    ) -> typing.Optional[typing.Union[CfnDomain.NodeToNodeEncryptionOptionsProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Elasticsearch::Domain.NodeToNodeEncryptionOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-nodetonodeencryptionoptions
        '''
        result = self._values.get("node_to_node_encryption_options")
        return typing.cast(typing.Optional[typing.Union[CfnDomain.NodeToNodeEncryptionOptionsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def snapshot_options(
        self,
    ) -> typing.Optional[typing.Union[CfnDomain.SnapshotOptionsProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Elasticsearch::Domain.SnapshotOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-snapshotoptions
        '''
        result = self._values.get("snapshot_options")
        return typing.cast(typing.Optional[typing.Union[CfnDomain.SnapshotOptionsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::Elasticsearch::Domain.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def vpc_options(
        self,
    ) -> typing.Optional[typing.Union[CfnDomain.VPCOptionsProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Elasticsearch::Domain.VPCOptions``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-vpcoptions
        '''
        result = self._values.get("vpc_options")
        return typing.cast(typing.Optional[typing.Union[CfnDomain.VPCOptionsProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_elasticsearch.CognitoOptions",
    jsii_struct_bases=[],
    name_mapping={
        "identity_pool_id": "identityPoolId",
        "role": "role",
        "user_pool_id": "userPoolId",
    },
)
class CognitoOptions:
    def __init__(
        self,
        *,
        identity_pool_id: builtins.str,
        role: _IRole_59af6f50,
        user_pool_id: builtins.str,
    ) -> None:
        '''(experimental) Configures Amazon ES to use Amazon Cognito authentication for Kibana.

        :param identity_pool_id: (experimental) The Amazon Cognito identity pool ID that you want Amazon ES to use for Kibana authentication.
        :param role: (experimental) A role that allows Amazon ES to configure your user pool and identity pool. It must have the ``AmazonESCognitoAccess`` policy attached to it.
        :param user_pool_id: (experimental) The Amazon Cognito user pool ID that you want Amazon ES to use for Kibana authentication.

        :see: https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-cognito-auth.html
        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "identity_pool_id": identity_pool_id,
            "role": role,
            "user_pool_id": user_pool_id,
        }

    @builtins.property
    def identity_pool_id(self) -> builtins.str:
        '''(experimental) The Amazon Cognito identity pool ID that you want Amazon ES to use for Kibana authentication.

        :stability: experimental
        '''
        result = self._values.get("identity_pool_id")
        assert result is not None, "Required property 'identity_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> _IRole_59af6f50:
        '''(experimental) A role that allows Amazon ES to configure your user pool and identity pool.

        It must have the ``AmazonESCognitoAccess`` policy attached to it.

        :see: https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-cognito-auth.html#es-cognito-auth-prereq
        :stability: experimental
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(_IRole_59af6f50, result)

    @builtins.property
    def user_pool_id(self) -> builtins.str:
        '''(experimental) The Amazon Cognito user pool ID that you want Amazon ES to use for Kibana authentication.

        :stability: experimental
        '''
        result = self._values.get("user_pool_id")
        assert result is not None, "Required property 'user_pool_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CognitoOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_elasticsearch.CustomEndpointOptions",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "certificate": "certificate",
        "hosted_zone": "hostedZone",
    },
)
class CustomEndpointOptions:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        certificate: typing.Optional[_ICertificate_c7bbdc16] = None,
        hosted_zone: typing.Optional[_IHostedZone_78d5a9c9] = None,
    ) -> None:
        '''(experimental) Configures a custom domain endpoint for the ES domain.

        :param domain_name: (experimental) The custom domain name to assign.
        :param certificate: (experimental) The certificate to use. Default: - create a new one
        :param hosted_zone: (experimental) The hosted zone in Route53 to create the CNAME record in. Default: - do not create a CNAME

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "domain_name": domain_name,
        }
        if certificate is not None:
            self._values["certificate"] = certificate
        if hosted_zone is not None:
            self._values["hosted_zone"] = hosted_zone

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''(experimental) The custom domain name to assign.

        :stability: experimental
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def certificate(self) -> typing.Optional[_ICertificate_c7bbdc16]:
        '''(experimental) The certificate to use.

        :default: - create a new one

        :stability: experimental
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[_ICertificate_c7bbdc16], result)

    @builtins.property
    def hosted_zone(self) -> typing.Optional[_IHostedZone_78d5a9c9]:
        '''(experimental) The hosted zone in Route53 to create the CNAME record in.

        :default: - do not create a CNAME

        :stability: experimental
        '''
        result = self._values.get("hosted_zone")
        return typing.cast(typing.Optional[_IHostedZone_78d5a9c9], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomEndpointOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_elasticsearch.DomainAttributes",
    jsii_struct_bases=[],
    name_mapping={"domain_arn": "domainArn", "domain_endpoint": "domainEndpoint"},
)
class DomainAttributes:
    def __init__(
        self,
        *,
        domain_arn: builtins.str,
        domain_endpoint: builtins.str,
    ) -> None:
        '''(experimental) Reference to an Elasticsearch domain.

        :param domain_arn: (experimental) The ARN of the Elasticsearch domain.
        :param domain_endpoint: (experimental) The domain endpoint of the Elasticsearch domain.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "domain_arn": domain_arn,
            "domain_endpoint": domain_endpoint,
        }

    @builtins.property
    def domain_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Elasticsearch domain.

        :stability: experimental
        '''
        result = self._values.get("domain_arn")
        assert result is not None, "Required property 'domain_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_endpoint(self) -> builtins.str:
        '''(experimental) The domain endpoint of the Elasticsearch domain.

        :stability: experimental
        '''
        result = self._values.get("domain_endpoint")
        assert result is not None, "Required property 'domain_endpoint' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_elasticsearch.DomainProps",
    jsii_struct_bases=[],
    name_mapping={
        "version": "version",
        "access_policies": "accessPolicies",
        "advanced_options": "advancedOptions",
        "automated_snapshot_start_hour": "automatedSnapshotStartHour",
        "capacity": "capacity",
        "cognito_kibana_auth": "cognitoKibanaAuth",
        "custom_endpoint": "customEndpoint",
        "domain_name": "domainName",
        "ebs": "ebs",
        "enable_version_upgrade": "enableVersionUpgrade",
        "encryption_at_rest": "encryptionAtRest",
        "enforce_https": "enforceHttps",
        "fine_grained_access_control": "fineGrainedAccessControl",
        "logging": "logging",
        "node_to_node_encryption": "nodeToNodeEncryption",
        "removal_policy": "removalPolicy",
        "tls_security_policy": "tlsSecurityPolicy",
        "use_unsigned_basic_auth": "useUnsignedBasicAuth",
        "vpc_options": "vpcOptions",
        "zone_awareness": "zoneAwareness",
    },
)
class DomainProps:
    def __init__(
        self,
        *,
        version: "ElasticsearchVersion",
        access_policies: typing.Optional[typing.List[_PolicyStatement_296fe8a3]] = None,
        advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        automated_snapshot_start_hour: typing.Optional[jsii.Number] = None,
        capacity: typing.Optional[CapacityConfig] = None,
        cognito_kibana_auth: typing.Optional[CognitoOptions] = None,
        custom_endpoint: typing.Optional[CustomEndpointOptions] = None,
        domain_name: typing.Optional[builtins.str] = None,
        ebs: typing.Optional["EbsOptions"] = None,
        enable_version_upgrade: typing.Optional[builtins.bool] = None,
        encryption_at_rest: typing.Optional["EncryptionAtRestOptions"] = None,
        enforce_https: typing.Optional[builtins.bool] = None,
        fine_grained_access_control: typing.Optional[AdvancedSecurityOptions] = None,
        logging: typing.Optional["LoggingOptions"] = None,
        node_to_node_encryption: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        tls_security_policy: typing.Optional["TLSSecurityPolicy"] = None,
        use_unsigned_basic_auth: typing.Optional[builtins.bool] = None,
        vpc_options: typing.Optional["VpcOptions"] = None,
        zone_awareness: typing.Optional["ZoneAwarenessConfig"] = None,
    ) -> None:
        '''(experimental) Properties for an AWS Elasticsearch Domain.

        :param version: (experimental) The Elasticsearch version that your domain will leverage.
        :param access_policies: (experimental) Domain Access policies. Default: - No access policies.
        :param advanced_options: (experimental) Additional options to specify for the Amazon ES domain. Default: - no advanced options are specified
        :param automated_snapshot_start_hour: (experimental) The hour in UTC during which the service takes an automated daily snapshot of the indices in the Amazon ES domain. Only applies for Elasticsearch versions below 5.3. Default: - Hourly automated snapshots not used
        :param capacity: (experimental) The cluster capacity configuration for the Amazon ES domain. Default: - 1 r5.large.elasticsearch data node; no dedicated master nodes.
        :param cognito_kibana_auth: (experimental) Configures Amazon ES to use Amazon Cognito authentication for Kibana. Default: - Cognito not used for authentication to Kibana.
        :param custom_endpoint: (experimental) To configure a custom domain configure these options. If you specify a Route53 hosted zone it will create a CNAME record and use DNS validation for the certificate Default: - no custom domain endpoint will be configured
        :param domain_name: (experimental) Enforces a particular physical domain name. Default: - A name will be auto-generated.
        :param ebs: (experimental) The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the Amazon ES domain. For more information, see [Configuring EBS-based Storage] (https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-createupdatedomains.html#es-createdomain-configure-ebs) in the Amazon Elasticsearch Service Developer Guide. Default: - 10 GiB General Purpose (SSD) volumes per node.
        :param enable_version_upgrade: (experimental) To upgrade an Amazon ES domain to a new version of Elasticsearch rather than replacing the entire domain resource, use the EnableVersionUpgrade update policy. Default: - false
        :param encryption_at_rest: (experimental) Encryption at rest options for the cluster. Default: - No encryption at rest
        :param enforce_https: (experimental) True to require that all traffic to the domain arrive over HTTPS. Default: - false
        :param fine_grained_access_control: (experimental) Specifies options for fine-grained access control. Requires Elasticsearch version 6.7 or later. Enabling fine-grained access control also requires encryption of data at rest and node-to-node encryption, along with enforced HTTPS. Default: - fine-grained access control is disabled
        :param logging: (experimental) Configuration log publishing configuration options. Default: - No logs are published
        :param node_to_node_encryption: (experimental) Specify true to enable node to node encryption. Requires Elasticsearch version 6.0 or later. Default: - Node to node encryption is not enabled.
        :param removal_policy: (experimental) Policy to apply when the domain is removed from the stack. Default: RemovalPolicy.RETAIN
        :param tls_security_policy: (experimental) The minimum TLS version required for traffic to the domain. Default: - TLSSecurityPolicy.TLS_1_0
        :param use_unsigned_basic_auth: (experimental) Configures the domain so that unsigned basic auth is enabled. If no master user is provided a default master user with username ``admin`` and a dynamically generated password stored in KMS is created. The password can be retrieved by getting ``masterUserPassword`` from the domain instance. Setting this to true will also add an access policy that allows unsigned access, enable node to node encryption, encryption at rest. If conflicting settings are encountered (like disabling encryption at rest) enabling this setting will cause a failure. Default: - false
        :param vpc_options: (experimental) The virtual private cloud (VPC) configuration for the Amazon ES domain. For more information, see `VPC Support for Amazon Elasticsearch Service Domains <https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-vpc.html>`_ in the Amazon Elasticsearch Service Developer Guide. Default: - VPC not used
        :param zone_awareness: (experimental) The cluster zone awareness configuration for the Amazon ES domain. Default: - no zone awareness (1 AZ)

        :stability: experimental
        '''
        if isinstance(capacity, dict):
            capacity = CapacityConfig(**capacity)
        if isinstance(cognito_kibana_auth, dict):
            cognito_kibana_auth = CognitoOptions(**cognito_kibana_auth)
        if isinstance(custom_endpoint, dict):
            custom_endpoint = CustomEndpointOptions(**custom_endpoint)
        if isinstance(ebs, dict):
            ebs = EbsOptions(**ebs)
        if isinstance(encryption_at_rest, dict):
            encryption_at_rest = EncryptionAtRestOptions(**encryption_at_rest)
        if isinstance(fine_grained_access_control, dict):
            fine_grained_access_control = AdvancedSecurityOptions(**fine_grained_access_control)
        if isinstance(logging, dict):
            logging = LoggingOptions(**logging)
        if isinstance(vpc_options, dict):
            vpc_options = VpcOptions(**vpc_options)
        if isinstance(zone_awareness, dict):
            zone_awareness = ZoneAwarenessConfig(**zone_awareness)
        self._values: typing.Dict[str, typing.Any] = {
            "version": version,
        }
        if access_policies is not None:
            self._values["access_policies"] = access_policies
        if advanced_options is not None:
            self._values["advanced_options"] = advanced_options
        if automated_snapshot_start_hour is not None:
            self._values["automated_snapshot_start_hour"] = automated_snapshot_start_hour
        if capacity is not None:
            self._values["capacity"] = capacity
        if cognito_kibana_auth is not None:
            self._values["cognito_kibana_auth"] = cognito_kibana_auth
        if custom_endpoint is not None:
            self._values["custom_endpoint"] = custom_endpoint
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if ebs is not None:
            self._values["ebs"] = ebs
        if enable_version_upgrade is not None:
            self._values["enable_version_upgrade"] = enable_version_upgrade
        if encryption_at_rest is not None:
            self._values["encryption_at_rest"] = encryption_at_rest
        if enforce_https is not None:
            self._values["enforce_https"] = enforce_https
        if fine_grained_access_control is not None:
            self._values["fine_grained_access_control"] = fine_grained_access_control
        if logging is not None:
            self._values["logging"] = logging
        if node_to_node_encryption is not None:
            self._values["node_to_node_encryption"] = node_to_node_encryption
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if tls_security_policy is not None:
            self._values["tls_security_policy"] = tls_security_policy
        if use_unsigned_basic_auth is not None:
            self._values["use_unsigned_basic_auth"] = use_unsigned_basic_auth
        if vpc_options is not None:
            self._values["vpc_options"] = vpc_options
        if zone_awareness is not None:
            self._values["zone_awareness"] = zone_awareness

    @builtins.property
    def version(self) -> "ElasticsearchVersion":
        '''(experimental) The Elasticsearch version that your domain will leverage.

        :stability: experimental
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast("ElasticsearchVersion", result)

    @builtins.property
    def access_policies(
        self,
    ) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        '''(experimental) Domain Access policies.

        :default: - No access policies.

        :stability: experimental
        '''
        result = self._values.get("access_policies")
        return typing.cast(typing.Optional[typing.List[_PolicyStatement_296fe8a3]], result)

    @builtins.property
    def advanced_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Additional options to specify for the Amazon ES domain.

        :default: - no advanced options are specified

        :stability: experimental
        '''
        result = self._values.get("advanced_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def automated_snapshot_start_hour(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The hour in UTC during which the service takes an automated daily snapshot of the indices in the Amazon ES domain.

        Only applies for Elasticsearch
        versions below 5.3.

        :default: - Hourly automated snapshots not used

        :stability: experimental
        '''
        result = self._values.get("automated_snapshot_start_hour")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def capacity(self) -> typing.Optional[CapacityConfig]:
        '''(experimental) The cluster capacity configuration for the Amazon ES domain.

        :default: - 1 r5.large.elasticsearch data node; no dedicated master nodes.

        :stability: experimental
        '''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional[CapacityConfig], result)

    @builtins.property
    def cognito_kibana_auth(self) -> typing.Optional[CognitoOptions]:
        '''(experimental) Configures Amazon ES to use Amazon Cognito authentication for Kibana.

        :default: - Cognito not used for authentication to Kibana.

        :stability: experimental
        '''
        result = self._values.get("cognito_kibana_auth")
        return typing.cast(typing.Optional[CognitoOptions], result)

    @builtins.property
    def custom_endpoint(self) -> typing.Optional[CustomEndpointOptions]:
        '''(experimental) To configure a custom domain configure these options.

        If you specify a Route53 hosted zone it will create a CNAME record and use DNS validation for the certificate

        :default: - no custom domain endpoint will be configured

        :stability: experimental
        '''
        result = self._values.get("custom_endpoint")
        return typing.cast(typing.Optional[CustomEndpointOptions], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Enforces a particular physical domain name.

        :default: - A name will be auto-generated.

        :stability: experimental
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ebs(self) -> typing.Optional["EbsOptions"]:
        '''(experimental) The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the Amazon ES domain.

        For more information, see
        [Configuring EBS-based Storage]
        (https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-createupdatedomains.html#es-createdomain-configure-ebs)
        in the Amazon Elasticsearch Service Developer Guide.

        :default: - 10 GiB General Purpose (SSD) volumes per node.

        :stability: experimental
        '''
        result = self._values.get("ebs")
        return typing.cast(typing.Optional["EbsOptions"], result)

    @builtins.property
    def enable_version_upgrade(self) -> typing.Optional[builtins.bool]:
        '''(experimental) To upgrade an Amazon ES domain to a new version of Elasticsearch rather than replacing the entire domain resource, use the EnableVersionUpgrade update policy.

        :default: - false

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-upgradeelasticsearchdomain
        :stability: experimental
        '''
        result = self._values.get("enable_version_upgrade")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def encryption_at_rest(self) -> typing.Optional["EncryptionAtRestOptions"]:
        '''(experimental) Encryption at rest options for the cluster.

        :default: - No encryption at rest

        :stability: experimental
        '''
        result = self._values.get("encryption_at_rest")
        return typing.cast(typing.Optional["EncryptionAtRestOptions"], result)

    @builtins.property
    def enforce_https(self) -> typing.Optional[builtins.bool]:
        '''(experimental) True to require that all traffic to the domain arrive over HTTPS.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("enforce_https")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def fine_grained_access_control(self) -> typing.Optional[AdvancedSecurityOptions]:
        '''(experimental) Specifies options for fine-grained access control.

        Requires Elasticsearch version 6.7 or later. Enabling fine-grained access control
        also requires encryption of data at rest and node-to-node encryption, along with
        enforced HTTPS.

        :default: - fine-grained access control is disabled

        :stability: experimental
        '''
        result = self._values.get("fine_grained_access_control")
        return typing.cast(typing.Optional[AdvancedSecurityOptions], result)

    @builtins.property
    def logging(self) -> typing.Optional["LoggingOptions"]:
        '''(experimental) Configuration log publishing configuration options.

        :default: - No logs are published

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional["LoggingOptions"], result)

    @builtins.property
    def node_to_node_encryption(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specify true to enable node to node encryption.

        Requires Elasticsearch version 6.0 or later.

        :default: - Node to node encryption is not enabled.

        :stability: experimental
        '''
        result = self._values.get("node_to_node_encryption")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        '''(experimental) Policy to apply when the domain is removed from the stack.

        :default: RemovalPolicy.RETAIN

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_RemovalPolicy_c97e7a20], result)

    @builtins.property
    def tls_security_policy(self) -> typing.Optional["TLSSecurityPolicy"]:
        '''(experimental) The minimum TLS version required for traffic to the domain.

        :default: - TLSSecurityPolicy.TLS_1_0

        :stability: experimental
        '''
        result = self._values.get("tls_security_policy")
        return typing.cast(typing.Optional["TLSSecurityPolicy"], result)

    @builtins.property
    def use_unsigned_basic_auth(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Configures the domain so that unsigned basic auth is enabled.

        If no master user is provided a default master user
        with username ``admin`` and a dynamically generated password stored in KMS is created. The password can be retrieved
        by getting ``masterUserPassword`` from the domain instance.

        Setting this to true will also add an access policy that allows unsigned
        access, enable node to node encryption, encryption at rest. If conflicting
        settings are encountered (like disabling encryption at rest) enabling this
        setting will cause a failure.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("use_unsigned_basic_auth")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc_options(self) -> typing.Optional["VpcOptions"]:
        '''(experimental) The virtual private cloud (VPC) configuration for the Amazon ES domain.

        For
        more information, see `VPC Support for Amazon Elasticsearch Service
        Domains <https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-vpc.html>`_
        in the Amazon Elasticsearch Service Developer Guide.

        :default: - VPC not used

        :stability: experimental
        '''
        result = self._values.get("vpc_options")
        return typing.cast(typing.Optional["VpcOptions"], result)

    @builtins.property
    def zone_awareness(self) -> typing.Optional["ZoneAwarenessConfig"]:
        '''(experimental) The cluster zone awareness configuration for the Amazon ES domain.

        :default: - no zone awareness (1 AZ)

        :stability: experimental
        '''
        result = self._values.get("zone_awareness")
        return typing.cast(typing.Optional["ZoneAwarenessConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_elasticsearch.EbsOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "iops": "iops",
        "volume_size": "volumeSize",
        "volume_type": "volumeType",
    },
)
class EbsOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        iops: typing.Optional[jsii.Number] = None,
        volume_size: typing.Optional[jsii.Number] = None,
        volume_type: typing.Optional[_EbsDeviceVolumeType_3b8e2d6d] = None,
    ) -> None:
        '''(experimental) The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the Amazon ES domain.

        For more information, see
        [Configuring EBS-based Storage]
        (https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-createupdatedomains.html#es-createdomain-configure-ebs)
        in the Amazon Elasticsearch Service Developer Guide.

        :param enabled: (experimental) Specifies whether Amazon EBS volumes are attached to data nodes in the Amazon ES domain. Default: - true
        :param iops: (experimental) The number of I/O operations per second (IOPS) that the volume supports. This property applies only to the Provisioned IOPS (SSD) EBS volume type. Default: - iops are not set.
        :param volume_size: (experimental) The size (in GiB) of the EBS volume for each data node. The minimum and maximum size of an EBS volume depends on the EBS volume type and the instance type to which it is attached. For more information, see [Configuring EBS-based Storage] (https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-createupdatedomains.html#es-createdomain-configure-ebs) in the Amazon Elasticsearch Service Developer Guide. Default: 10
        :param volume_type: (experimental) The EBS volume type to use with the Amazon ES domain, such as standard, gp2, io1. For more information, see[Configuring EBS-based Storage] (https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-createupdatedomains.html#es-createdomain-configure-ebs) in the Amazon Elasticsearch Service Developer Guide. Default: gp2

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if iops is not None:
            self._values["iops"] = iops
        if volume_size is not None:
            self._values["volume_size"] = volume_size
        if volume_type is not None:
            self._values["volume_type"] = volume_type

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether Amazon EBS volumes are attached to data nodes in the Amazon ES domain.

        :default: - true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of I/O operations per second (IOPS) that the volume supports.

        This property applies only to the Provisioned IOPS (SSD) EBS
        volume type.

        :default: - iops are not set.

        :stability: experimental
        '''
        result = self._values.get("iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size (in GiB) of the EBS volume for each data node.

        The minimum and
        maximum size of an EBS volume depends on the EBS volume type and the
        instance type to which it is attached.  For more information, see
        [Configuring EBS-based Storage]
        (https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-createupdatedomains.html#es-createdomain-configure-ebs)
        in the Amazon Elasticsearch Service Developer Guide.

        :default: 10

        :stability: experimental
        '''
        result = self._values.get("volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volume_type(self) -> typing.Optional[_EbsDeviceVolumeType_3b8e2d6d]:
        '''(experimental) The EBS volume type to use with the Amazon ES domain, such as standard, gp2, io1.

        For more information, see[Configuring EBS-based Storage]
        (https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-createupdatedomains.html#es-createdomain-configure-ebs)
        in the Amazon Elasticsearch Service Developer Guide.

        :default: gp2

        :stability: experimental
        '''
        result = self._values.get("volume_type")
        return typing.cast(typing.Optional[_EbsDeviceVolumeType_3b8e2d6d], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EbsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ElasticsearchVersion(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticsearch.ElasticsearchVersion",
):
    '''(experimental) Elasticsearch version.

    :stability: experimental
    '''

    @jsii.member(jsii_name="of") # type: ignore[misc]
    @builtins.classmethod
    def of(cls, version: builtins.str) -> "ElasticsearchVersion":
        '''(experimental) Custom Elasticsearch version.

        :param version: custom version number.

        :stability: experimental
        '''
        return typing.cast("ElasticsearchVersion", jsii.sinvoke(cls, "of", [version]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V1_5")
    def V1_5(cls) -> "ElasticsearchVersion":
        '''(experimental) AWS Elasticsearch 1.5.

        :stability: experimental
        '''
        return typing.cast("ElasticsearchVersion", jsii.sget(cls, "V1_5"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V2_3")
    def V2_3(cls) -> "ElasticsearchVersion":
        '''(experimental) AWS Elasticsearch 2.3.

        :stability: experimental
        '''
        return typing.cast("ElasticsearchVersion", jsii.sget(cls, "V2_3"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V5_1")
    def V5_1(cls) -> "ElasticsearchVersion":
        '''(experimental) AWS Elasticsearch 5.1.

        :stability: experimental
        '''
        return typing.cast("ElasticsearchVersion", jsii.sget(cls, "V5_1"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V5_3")
    def V5_3(cls) -> "ElasticsearchVersion":
        '''(experimental) AWS Elasticsearch 5.3.

        :stability: experimental
        '''
        return typing.cast("ElasticsearchVersion", jsii.sget(cls, "V5_3"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V5_5")
    def V5_5(cls) -> "ElasticsearchVersion":
        '''(experimental) AWS Elasticsearch 5.5.

        :stability: experimental
        '''
        return typing.cast("ElasticsearchVersion", jsii.sget(cls, "V5_5"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V5_6")
    def V5_6(cls) -> "ElasticsearchVersion":
        '''(experimental) AWS Elasticsearch 5.6.

        :stability: experimental
        '''
        return typing.cast("ElasticsearchVersion", jsii.sget(cls, "V5_6"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V6_0")
    def V6_0(cls) -> "ElasticsearchVersion":
        '''(experimental) AWS Elasticsearch 6.0.

        :stability: experimental
        '''
        return typing.cast("ElasticsearchVersion", jsii.sget(cls, "V6_0"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V6_2")
    def V6_2(cls) -> "ElasticsearchVersion":
        '''(experimental) AWS Elasticsearch 6.2.

        :stability: experimental
        '''
        return typing.cast("ElasticsearchVersion", jsii.sget(cls, "V6_2"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V6_3")
    def V6_3(cls) -> "ElasticsearchVersion":
        '''(experimental) AWS Elasticsearch 6.3.

        :stability: experimental
        '''
        return typing.cast("ElasticsearchVersion", jsii.sget(cls, "V6_3"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V6_4")
    def V6_4(cls) -> "ElasticsearchVersion":
        '''(experimental) AWS Elasticsearch 6.4.

        :stability: experimental
        '''
        return typing.cast("ElasticsearchVersion", jsii.sget(cls, "V6_4"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V6_5")
    def V6_5(cls) -> "ElasticsearchVersion":
        '''(experimental) AWS Elasticsearch 6.5.

        :stability: experimental
        '''
        return typing.cast("ElasticsearchVersion", jsii.sget(cls, "V6_5"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V6_7")
    def V6_7(cls) -> "ElasticsearchVersion":
        '''(experimental) AWS Elasticsearch 6.7.

        :stability: experimental
        '''
        return typing.cast("ElasticsearchVersion", jsii.sget(cls, "V6_7"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V6_8")
    def V6_8(cls) -> "ElasticsearchVersion":
        '''(experimental) AWS Elasticsearch 6.8.

        :stability: experimental
        '''
        return typing.cast("ElasticsearchVersion", jsii.sget(cls, "V6_8"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V7_1")
    def V7_1(cls) -> "ElasticsearchVersion":
        '''(experimental) AWS Elasticsearch 7.1.

        :stability: experimental
        '''
        return typing.cast("ElasticsearchVersion", jsii.sget(cls, "V7_1"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V7_4")
    def V7_4(cls) -> "ElasticsearchVersion":
        '''(experimental) AWS Elasticsearch 7.4.

        :stability: experimental
        '''
        return typing.cast("ElasticsearchVersion", jsii.sget(cls, "V7_4"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V7_7")
    def V7_7(cls) -> "ElasticsearchVersion":
        '''(experimental) AWS Elasticsearch 7.7.

        :stability: experimental
        '''
        return typing.cast("ElasticsearchVersion", jsii.sget(cls, "V7_7"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V7_8")
    def V7_8(cls) -> "ElasticsearchVersion":
        '''(experimental) AWS Elasticsearch 7.8.

        :stability: experimental
        '''
        return typing.cast("ElasticsearchVersion", jsii.sget(cls, "V7_8"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V7_9")
    def V7_9(cls) -> "ElasticsearchVersion":
        '''(experimental) AWS Elasticsearch 7.9.

        :stability: experimental
        '''
        return typing.cast("ElasticsearchVersion", jsii.sget(cls, "V7_9"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''(experimental) Elasticsearch version number.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))


@jsii.data_type(
    jsii_type="monocdk.aws_elasticsearch.EncryptionAtRestOptions",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "kms_key": "kmsKey"},
)
class EncryptionAtRestOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        kms_key: typing.Optional[_IKey_36930160] = None,
    ) -> None:
        '''(experimental) Whether the domain should encrypt data at rest, and if so, the AWS Key Management Service (KMS) key to use.

        Can only be used to create a new domain,
        not update an existing one. Requires Elasticsearch version 5.1 or later.

        :param enabled: (experimental) Specify true to enable encryption at rest. Default: - encryption at rest is disabled.
        :param kms_key: (experimental) Supply if using KMS key for encryption at rest. Default: - uses default aws/es KMS key.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specify true to enable encryption at rest.

        :default: - encryption at rest is disabled.

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) Supply if using KMS key for encryption at rest.

        :default: - uses default aws/es KMS key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EncryptionAtRestOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_elasticsearch.IDomain")
class IDomain(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) An interface that represents an Elasticsearch domain - either created with the CDK, or an existing one.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IDomainProxy"]:
        return _IDomainProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainArn")
    def domain_arn(self) -> builtins.str:
        '''(experimental) Arn of the Elasticsearch domain.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainEndpoint")
    def domain_endpoint(self) -> builtins.str:
        '''(experimental) Endpoint of the Elasticsearch domain.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''(experimental) Domain name of the Elasticsearch domain.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grantIndexRead")
    def grant_index_read(
        self,
        index: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantIndexReadWrite")
    def grant_index_read_write(
        self,
        index: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read/write permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantIndexWrite")
    def grant_index_write(
        self,
        index: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantPathRead")
    def grant_path_read(
        self,
        path: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantPathReadWrite")
    def grant_path_read_write(
        self,
        path: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read/write permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantPathWrite")
    def grant_path_write(
        self,
        path: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant read/write permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
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
        '''(experimental) Return the given named metric for this Domain.

        :param metric_name: -
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
        ...

    @jsii.member(jsii_name="metricAutomatedSnapshotFailure")
    def metric_automated_snapshot_failure(
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
        '''(experimental) Metric for automated snapshot failures.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricClusterIndexWriteBlocked")
    def metric_cluster_index_write_blocked(
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
        '''(experimental) Metric for the cluster blocking index writes.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 1 minute

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricClusterStatusRed")
    def metric_cluster_status_red(
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
        '''(experimental) Metric for the time the cluster status is red.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricClusterStatusYellow")
    def metric_cluster_status_yellow(
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
        '''(experimental) Metric for the time the cluster status is yellow.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricCPUUtilization")
    def metric_cpu_utilization(
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
        '''(experimental) Metric for CPU utilization.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricFreeStorageSpace")
    def metric_free_storage_space(
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
        '''(experimental) Metric for the storage space of nodes in the cluster.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: minimum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricIndexingLatency")
    def metric_indexing_latency(
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
        '''(experimental) Metric for indexing latency.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: p99 over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricJVMMemoryPressure")
    def metric_jvm_memory_pressure(
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
        '''(experimental) Metric for JVM memory pressure.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricKMSKeyError")
    def metric_kms_key_error(
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
        '''(experimental) Metric for KMS key errors.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricKMSKeyInaccessible")
    def metric_kms_key_inaccessible(
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
        '''(experimental) Metric for KMS key being inaccessible.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricMasterCPUUtilization")
    def metric_master_cpu_utilization(
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
        '''(experimental) Metric for master CPU utilization.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricMasterJVMMemoryPressure")
    def metric_master_jvm_memory_pressure(
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
        '''(experimental) Metric for master JVM memory pressure.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricNodes")
    def metric_nodes(
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
        '''(experimental) Metric for the number of nodes.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: minimum over 1 hour

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricSearchableDocuments")
    def metric_searchable_documents(
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
        '''(experimental) Metric for number of searchable documents.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricSearchLatency")
    def metric_search_latency(
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
        '''(experimental) Metric for search latency.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: p99 over 5 minutes

        :stability: experimental
        '''
        ...


class _IDomainProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''(experimental) An interface that represents an Elasticsearch domain - either created with the CDK, or an existing one.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_elasticsearch.IDomain"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainArn")
    def domain_arn(self) -> builtins.str:
        '''(experimental) Arn of the Elasticsearch domain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainEndpoint")
    def domain_endpoint(self) -> builtins.str:
        '''(experimental) Endpoint of the Elasticsearch domain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainEndpoint"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''(experimental) Domain name of the Elasticsearch domain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @jsii.member(jsii_name="grantIndexRead")
    def grant_index_read(
        self,
        index: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantIndexRead", [index, identity]))

    @jsii.member(jsii_name="grantIndexReadWrite")
    def grant_index_read_write(
        self,
        index: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read/write permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantIndexReadWrite", [index, identity]))

    @jsii.member(jsii_name="grantIndexWrite")
    def grant_index_write(
        self,
        index: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantIndexWrite", [index, identity]))

    @jsii.member(jsii_name="grantPathRead")
    def grant_path_read(
        self,
        path: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPathRead", [path, identity]))

    @jsii.member(jsii_name="grantPathReadWrite")
    def grant_path_read_write(
        self,
        path: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read/write permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPathReadWrite", [path, identity]))

    @jsii.member(jsii_name="grantPathWrite")
    def grant_path_write(
        self,
        path: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPathWrite", [path, identity]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantRead", [identity]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant read/write permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantReadWrite", [identity]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantWrite", [identity]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
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
        '''(experimental) Return the given named metric for this Domain.

        :param metric_name: -
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
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricAutomatedSnapshotFailure")
    def metric_automated_snapshot_failure(
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
        '''(experimental) Metric for automated snapshot failures.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricAutomatedSnapshotFailure", [props]))

    @jsii.member(jsii_name="metricClusterIndexWriteBlocked")
    def metric_cluster_index_write_blocked(
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
        '''(experimental) Metric for the cluster blocking index writes.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 1 minute

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricClusterIndexWriteBlocked", [props]))

    @jsii.member(jsii_name="metricClusterStatusRed")
    def metric_cluster_status_red(
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
        '''(experimental) Metric for the time the cluster status is red.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricClusterStatusRed", [props]))

    @jsii.member(jsii_name="metricClusterStatusYellow")
    def metric_cluster_status_yellow(
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
        '''(experimental) Metric for the time the cluster status is yellow.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricClusterStatusYellow", [props]))

    @jsii.member(jsii_name="metricCPUUtilization")
    def metric_cpu_utilization(
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
        '''(experimental) Metric for CPU utilization.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricCPUUtilization", [props]))

    @jsii.member(jsii_name="metricFreeStorageSpace")
    def metric_free_storage_space(
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
        '''(experimental) Metric for the storage space of nodes in the cluster.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: minimum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricFreeStorageSpace", [props]))

    @jsii.member(jsii_name="metricIndexingLatency")
    def metric_indexing_latency(
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
        '''(experimental) Metric for indexing latency.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: p99 over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricIndexingLatency", [props]))

    @jsii.member(jsii_name="metricJVMMemoryPressure")
    def metric_jvm_memory_pressure(
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
        '''(experimental) Metric for JVM memory pressure.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricJVMMemoryPressure", [props]))

    @jsii.member(jsii_name="metricKMSKeyError")
    def metric_kms_key_error(
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
        '''(experimental) Metric for KMS key errors.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricKMSKeyError", [props]))

    @jsii.member(jsii_name="metricKMSKeyInaccessible")
    def metric_kms_key_inaccessible(
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
        '''(experimental) Metric for KMS key being inaccessible.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricKMSKeyInaccessible", [props]))

    @jsii.member(jsii_name="metricMasterCPUUtilization")
    def metric_master_cpu_utilization(
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
        '''(experimental) Metric for master CPU utilization.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricMasterCPUUtilization", [props]))

    @jsii.member(jsii_name="metricMasterJVMMemoryPressure")
    def metric_master_jvm_memory_pressure(
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
        '''(experimental) Metric for master JVM memory pressure.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricMasterJVMMemoryPressure", [props]))

    @jsii.member(jsii_name="metricNodes")
    def metric_nodes(
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
        '''(experimental) Metric for the number of nodes.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: minimum over 1 hour

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNodes", [props]))

    @jsii.member(jsii_name="metricSearchableDocuments")
    def metric_searchable_documents(
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
        '''(experimental) Metric for number of searchable documents.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSearchableDocuments", [props]))

    @jsii.member(jsii_name="metricSearchLatency")
    def metric_search_latency(
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
        '''(experimental) Metric for search latency.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: p99 over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSearchLatency", [props]))


@jsii.data_type(
    jsii_type="monocdk.aws_elasticsearch.LoggingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "app_log_enabled": "appLogEnabled",
        "app_log_group": "appLogGroup",
        "audit_log_enabled": "auditLogEnabled",
        "audit_log_group": "auditLogGroup",
        "slow_index_log_enabled": "slowIndexLogEnabled",
        "slow_index_log_group": "slowIndexLogGroup",
        "slow_search_log_enabled": "slowSearchLogEnabled",
        "slow_search_log_group": "slowSearchLogGroup",
    },
)
class LoggingOptions:
    def __init__(
        self,
        *,
        app_log_enabled: typing.Optional[builtins.bool] = None,
        app_log_group: typing.Optional[_ILogGroup_846e17a0] = None,
        audit_log_enabled: typing.Optional[builtins.bool] = None,
        audit_log_group: typing.Optional[_ILogGroup_846e17a0] = None,
        slow_index_log_enabled: typing.Optional[builtins.bool] = None,
        slow_index_log_group: typing.Optional[_ILogGroup_846e17a0] = None,
        slow_search_log_enabled: typing.Optional[builtins.bool] = None,
        slow_search_log_group: typing.Optional[_ILogGroup_846e17a0] = None,
    ) -> None:
        '''(experimental) Configures log settings for the domain.

        :param app_log_enabled: (experimental) Specify if Elasticsearch application logging should be set up. Requires Elasticsearch version 5.1 or later. Default: - false
        :param app_log_group: (experimental) Log Elasticsearch application logs to this log group. Default: - a new log group is created if app logging is enabled
        :param audit_log_enabled: (experimental) Specify if Elasticsearch audit logging should be set up. Requires Elasticsearch version 6.7 or later and fine grained access control to be enabled. Default: - false
        :param audit_log_group: (experimental) Log Elasticsearch audit logs to this log group. Default: - a new log group is created if audit logging is enabled
        :param slow_index_log_enabled: (experimental) Specify if slow index logging should be set up. Requires Elasticsearch version 5.1 or later. Default: - false
        :param slow_index_log_group: (experimental) Log slow indices to this log group. Default: - a new log group is created if slow index logging is enabled
        :param slow_search_log_enabled: (experimental) Specify if slow search logging should be set up. Requires Elasticsearch version 5.1 or later. Default: - false
        :param slow_search_log_group: (experimental) Log slow searches to this log group. Default: - a new log group is created if slow search logging is enabled

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if app_log_enabled is not None:
            self._values["app_log_enabled"] = app_log_enabled
        if app_log_group is not None:
            self._values["app_log_group"] = app_log_group
        if audit_log_enabled is not None:
            self._values["audit_log_enabled"] = audit_log_enabled
        if audit_log_group is not None:
            self._values["audit_log_group"] = audit_log_group
        if slow_index_log_enabled is not None:
            self._values["slow_index_log_enabled"] = slow_index_log_enabled
        if slow_index_log_group is not None:
            self._values["slow_index_log_group"] = slow_index_log_group
        if slow_search_log_enabled is not None:
            self._values["slow_search_log_enabled"] = slow_search_log_enabled
        if slow_search_log_group is not None:
            self._values["slow_search_log_group"] = slow_search_log_group

    @builtins.property
    def app_log_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specify if Elasticsearch application logging should be set up.

        Requires Elasticsearch version 5.1 or later.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("app_log_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def app_log_group(self) -> typing.Optional[_ILogGroup_846e17a0]:
        '''(experimental) Log Elasticsearch application logs to this log group.

        :default: - a new log group is created if app logging is enabled

        :stability: experimental
        '''
        result = self._values.get("app_log_group")
        return typing.cast(typing.Optional[_ILogGroup_846e17a0], result)

    @builtins.property
    def audit_log_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specify if Elasticsearch audit logging should be set up.

        Requires Elasticsearch version 6.7 or later and fine grained access control to be enabled.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("audit_log_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def audit_log_group(self) -> typing.Optional[_ILogGroup_846e17a0]:
        '''(experimental) Log Elasticsearch audit logs to this log group.

        :default: - a new log group is created if audit logging is enabled

        :stability: experimental
        '''
        result = self._values.get("audit_log_group")
        return typing.cast(typing.Optional[_ILogGroup_846e17a0], result)

    @builtins.property
    def slow_index_log_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specify if slow index logging should be set up.

        Requires Elasticsearch version 5.1 or later.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("slow_index_log_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def slow_index_log_group(self) -> typing.Optional[_ILogGroup_846e17a0]:
        '''(experimental) Log slow indices to this log group.

        :default: - a new log group is created if slow index logging is enabled

        :stability: experimental
        '''
        result = self._values.get("slow_index_log_group")
        return typing.cast(typing.Optional[_ILogGroup_846e17a0], result)

    @builtins.property
    def slow_search_log_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specify if slow search logging should be set up.

        Requires Elasticsearch version 5.1 or later.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("slow_search_log_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def slow_search_log_group(self) -> typing.Optional[_ILogGroup_846e17a0]:
        '''(experimental) Log slow searches to this log group.

        :default: - a new log group is created if slow search logging is enabled

        :stability: experimental
        '''
        result = self._values.get("slow_search_log_group")
        return typing.cast(typing.Optional[_ILogGroup_846e17a0], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoggingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_elasticsearch.TLSSecurityPolicy")
class TLSSecurityPolicy(enum.Enum):
    '''(experimental) The minimum TLS version required for traffic to the domain.

    :stability: experimental
    '''

    TLS_1_0 = "TLS_1_0"
    '''(experimental) Cipher suite TLS 1.0.

    :stability: experimental
    '''
    TLS_1_2 = "TLS_1_2"
    '''(experimental) Cipher suite TLS 1.2.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_elasticsearch.VpcOptions",
    jsii_struct_bases=[],
    name_mapping={"security_groups": "securityGroups", "subnets": "subnets"},
)
class VpcOptions:
    def __init__(
        self,
        *,
        security_groups: typing.List[_ISecurityGroup_cdbba9d3],
        subnets: typing.List[_ISubnet_0a12f914],
    ) -> None:
        '''(experimental) The virtual private cloud (VPC) configuration for the Amazon ES domain.

        For
        more information, see `VPC Support for Amazon Elasticsearch Service
        Domains <https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-vpc.html>`_
        in the Amazon Elasticsearch Service Developer Guide.

        :param security_groups: (experimental) The list of security groups that are associated with the VPC endpoints for the domain. If you don't provide a security group ID, Amazon ES uses the default security group for the VPC. To learn more, see [Security Groups for your VPC] (https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) in the Amazon VPC User Guide.
        :param subnets: (experimental) Provide one subnet for each Availability Zone that your domain uses. For example, you must specify three subnet IDs for a three Availability Zone domain. To learn more, see [VPCs and Subnets] (https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html) in the Amazon VPC User Guide.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "security_groups": security_groups,
            "subnets": subnets,
        }

    @builtins.property
    def security_groups(self) -> typing.List[_ISecurityGroup_cdbba9d3]:
        '''(experimental) The list of security groups that are associated with the VPC endpoints for the domain.

        If you don't provide a security group ID, Amazon ES uses
        the default security group for the VPC. To learn more, see [Security Groups for your VPC]
        (https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) in the Amazon VPC
        User Guide.

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        assert result is not None, "Required property 'security_groups' is missing"
        return typing.cast(typing.List[_ISecurityGroup_cdbba9d3], result)

    @builtins.property
    def subnets(self) -> typing.List[_ISubnet_0a12f914]:
        '''(experimental) Provide one subnet for each Availability Zone that your domain uses.

        For
        example, you must specify three subnet IDs for a three Availability Zone
        domain. To learn more, see [VPCs and Subnets]
        (https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html) in the
        Amazon VPC User Guide.

        :stability: experimental
        '''
        result = self._values.get("subnets")
        assert result is not None, "Required property 'subnets' is missing"
        return typing.cast(typing.List[_ISubnet_0a12f914], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_elasticsearch.ZoneAwarenessConfig",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zone_count": "availabilityZoneCount",
        "enabled": "enabled",
    },
)
class ZoneAwarenessConfig:
    def __init__(
        self,
        *,
        availability_zone_count: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Specifies zone awareness configuration options.

        :param availability_zone_count: (experimental) If you enabled multiple Availability Zones (AZs), the number of AZs that you want the domain to use. Valid values are 2 and 3. Default: - 2 if zone awareness is enabled.
        :param enabled: (experimental) Indicates whether to enable zone awareness for the Amazon ES domain. When you enable zone awareness, Amazon ES allocates the nodes and replica index shards that belong to a cluster across two Availability Zones (AZs) in the same region to prevent data loss and minimize downtime in the event of node or data center failure. Don't enable zone awareness if your cluster has no replica index shards or is a single-node cluster. For more information, see [Configuring a Multi-AZ Domain] (https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-createupdatedomains.html#es-managedomains-multiaz) in the Amazon Elasticsearch Service Developer Guide. Default: - false

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if availability_zone_count is not None:
            self._values["availability_zone_count"] = availability_zone_count
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def availability_zone_count(self) -> typing.Optional[jsii.Number]:
        '''(experimental) If you enabled multiple Availability Zones (AZs), the number of AZs that you want the domain to use.

        Valid values are 2 and 3.

        :default: - 2 if zone awareness is enabled.

        :stability: experimental
        '''
        result = self._values.get("availability_zone_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether to enable zone awareness for the Amazon ES domain.

        When you enable zone awareness, Amazon ES allocates the nodes and replica
        index shards that belong to a cluster across two Availability Zones (AZs)
        in the same region to prevent data loss and minimize downtime in the event
        of node or data center failure. Don't enable zone awareness if your cluster
        has no replica index shards or is a single-node cluster. For more information,
        see [Configuring a Multi-AZ Domain]
        (https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-createupdatedomains.html#es-managedomains-multiaz)
        in the Amazon Elasticsearch Service Developer Guide.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZoneAwarenessConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IDomain)
class Domain(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_elasticsearch.Domain",
):
    '''(experimental) Provides an Elasticsearch domain.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        version: ElasticsearchVersion,
        access_policies: typing.Optional[typing.List[_PolicyStatement_296fe8a3]] = None,
        advanced_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        automated_snapshot_start_hour: typing.Optional[jsii.Number] = None,
        capacity: typing.Optional[CapacityConfig] = None,
        cognito_kibana_auth: typing.Optional[CognitoOptions] = None,
        custom_endpoint: typing.Optional[CustomEndpointOptions] = None,
        domain_name: typing.Optional[builtins.str] = None,
        ebs: typing.Optional[EbsOptions] = None,
        enable_version_upgrade: typing.Optional[builtins.bool] = None,
        encryption_at_rest: typing.Optional[EncryptionAtRestOptions] = None,
        enforce_https: typing.Optional[builtins.bool] = None,
        fine_grained_access_control: typing.Optional[AdvancedSecurityOptions] = None,
        logging: typing.Optional[LoggingOptions] = None,
        node_to_node_encryption: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        tls_security_policy: typing.Optional[TLSSecurityPolicy] = None,
        use_unsigned_basic_auth: typing.Optional[builtins.bool] = None,
        vpc_options: typing.Optional[VpcOptions] = None,
        zone_awareness: typing.Optional[ZoneAwarenessConfig] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param version: (experimental) The Elasticsearch version that your domain will leverage.
        :param access_policies: (experimental) Domain Access policies. Default: - No access policies.
        :param advanced_options: (experimental) Additional options to specify for the Amazon ES domain. Default: - no advanced options are specified
        :param automated_snapshot_start_hour: (experimental) The hour in UTC during which the service takes an automated daily snapshot of the indices in the Amazon ES domain. Only applies for Elasticsearch versions below 5.3. Default: - Hourly automated snapshots not used
        :param capacity: (experimental) The cluster capacity configuration for the Amazon ES domain. Default: - 1 r5.large.elasticsearch data node; no dedicated master nodes.
        :param cognito_kibana_auth: (experimental) Configures Amazon ES to use Amazon Cognito authentication for Kibana. Default: - Cognito not used for authentication to Kibana.
        :param custom_endpoint: (experimental) To configure a custom domain configure these options. If you specify a Route53 hosted zone it will create a CNAME record and use DNS validation for the certificate Default: - no custom domain endpoint will be configured
        :param domain_name: (experimental) Enforces a particular physical domain name. Default: - A name will be auto-generated.
        :param ebs: (experimental) The configurations of Amazon Elastic Block Store (Amazon EBS) volumes that are attached to data nodes in the Amazon ES domain. For more information, see [Configuring EBS-based Storage] (https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-createupdatedomains.html#es-createdomain-configure-ebs) in the Amazon Elasticsearch Service Developer Guide. Default: - 10 GiB General Purpose (SSD) volumes per node.
        :param enable_version_upgrade: (experimental) To upgrade an Amazon ES domain to a new version of Elasticsearch rather than replacing the entire domain resource, use the EnableVersionUpgrade update policy. Default: - false
        :param encryption_at_rest: (experimental) Encryption at rest options for the cluster. Default: - No encryption at rest
        :param enforce_https: (experimental) True to require that all traffic to the domain arrive over HTTPS. Default: - false
        :param fine_grained_access_control: (experimental) Specifies options for fine-grained access control. Requires Elasticsearch version 6.7 or later. Enabling fine-grained access control also requires encryption of data at rest and node-to-node encryption, along with enforced HTTPS. Default: - fine-grained access control is disabled
        :param logging: (experimental) Configuration log publishing configuration options. Default: - No logs are published
        :param node_to_node_encryption: (experimental) Specify true to enable node to node encryption. Requires Elasticsearch version 6.0 or later. Default: - Node to node encryption is not enabled.
        :param removal_policy: (experimental) Policy to apply when the domain is removed from the stack. Default: RemovalPolicy.RETAIN
        :param tls_security_policy: (experimental) The minimum TLS version required for traffic to the domain. Default: - TLSSecurityPolicy.TLS_1_0
        :param use_unsigned_basic_auth: (experimental) Configures the domain so that unsigned basic auth is enabled. If no master user is provided a default master user with username ``admin`` and a dynamically generated password stored in KMS is created. The password can be retrieved by getting ``masterUserPassword`` from the domain instance. Setting this to true will also add an access policy that allows unsigned access, enable node to node encryption, encryption at rest. If conflicting settings are encountered (like disabling encryption at rest) enabling this setting will cause a failure. Default: - false
        :param vpc_options: (experimental) The virtual private cloud (VPC) configuration for the Amazon ES domain. For more information, see `VPC Support for Amazon Elasticsearch Service Domains <https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-vpc.html>`_ in the Amazon Elasticsearch Service Developer Guide. Default: - VPC not used
        :param zone_awareness: (experimental) The cluster zone awareness configuration for the Amazon ES domain. Default: - no zone awareness (1 AZ)

        :stability: experimental
        '''
        props = DomainProps(
            version=version,
            access_policies=access_policies,
            advanced_options=advanced_options,
            automated_snapshot_start_hour=automated_snapshot_start_hour,
            capacity=capacity,
            cognito_kibana_auth=cognito_kibana_auth,
            custom_endpoint=custom_endpoint,
            domain_name=domain_name,
            ebs=ebs,
            enable_version_upgrade=enable_version_upgrade,
            encryption_at_rest=encryption_at_rest,
            enforce_https=enforce_https,
            fine_grained_access_control=fine_grained_access_control,
            logging=logging,
            node_to_node_encryption=node_to_node_encryption,
            removal_policy=removal_policy,
            tls_security_policy=tls_security_policy,
            use_unsigned_basic_auth=use_unsigned_basic_auth,
            vpc_options=vpc_options,
            zone_awareness=zone_awareness,
        )

        jsii.create(Domain, self, [scope, id, props])

    @jsii.member(jsii_name="fromDomainAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_domain_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        domain_arn: builtins.str,
        domain_endpoint: builtins.str,
    ) -> IDomain:
        '''(experimental) Creates a Domain construct that represents an external domain.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param domain_arn: (experimental) The ARN of the Elasticsearch domain.
        :param domain_endpoint: (experimental) The domain endpoint of the Elasticsearch domain.

        :stability: experimental
        '''
        attrs = DomainAttributes(
            domain_arn=domain_arn, domain_endpoint=domain_endpoint
        )

        return typing.cast(IDomain, jsii.sinvoke(cls, "fromDomainAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromDomainEndpoint") # type: ignore[misc]
    @builtins.classmethod
    def from_domain_endpoint(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        domain_endpoint: builtins.str,
    ) -> IDomain:
        '''(experimental) Creates a Domain construct that represents an external domain via domain endpoint.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param domain_endpoint: The domain's endpoint.

        :stability: experimental
        '''
        return typing.cast(IDomain, jsii.sinvoke(cls, "fromDomainEndpoint", [scope, id, domain_endpoint]))

    @jsii.member(jsii_name="grantIndexRead")
    def grant_index_read(
        self,
        index: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantIndexRead", [index, identity]))

    @jsii.member(jsii_name="grantIndexReadWrite")
    def grant_index_read_write(
        self,
        index: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read/write permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantIndexReadWrite", [index, identity]))

    @jsii.member(jsii_name="grantIndexWrite")
    def grant_index_write(
        self,
        index: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions for an index in this domain to an IAM principal (Role/Group/User).

        :param index: The index to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantIndexWrite", [index, identity]))

    @jsii.member(jsii_name="grantPathRead")
    def grant_path_read(
        self,
        path: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPathRead", [path, identity]))

    @jsii.member(jsii_name="grantPathReadWrite")
    def grant_path_read_write(
        self,
        path: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read/write permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPathReadWrite", [path, identity]))

    @jsii.member(jsii_name="grantPathWrite")
    def grant_path_write(
        self,
        path: builtins.str,
        identity: _IGrantable_4c5a91d1,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions for a specific path in this domain to an IAM principal (Role/Group/User).

        :param path: The path to grant permissions for.
        :param identity: The principal.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPathWrite", [path, identity]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantRead", [identity]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant read/write permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantReadWrite", [identity]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions for this domain and its contents to an IAM principal (Role/Group/User).

        :param identity: The principal.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantWrite", [identity]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
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
        '''(experimental) Return the given named metric for this Domain.

        :param metric_name: -
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
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricAutomatedSnapshotFailure")
    def metric_automated_snapshot_failure(
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
        '''(experimental) Metric for automated snapshot failures.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricAutomatedSnapshotFailure", [props]))

    @jsii.member(jsii_name="metricClusterIndexWriteBlocked")
    def metric_cluster_index_write_blocked(
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
        '''(experimental) Metric for the cluster blocking index writes.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 1 minute

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricClusterIndexWriteBlocked", [props]))

    @jsii.member(jsii_name="metricClusterStatusRed")
    def metric_cluster_status_red(
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
        '''(experimental) Metric for the time the cluster status is red.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricClusterStatusRed", [props]))

    @jsii.member(jsii_name="metricClusterStatusYellow")
    def metric_cluster_status_yellow(
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
        '''(experimental) Metric for the time the cluster status is yellow.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricClusterStatusYellow", [props]))

    @jsii.member(jsii_name="metricCPUUtilization")
    def metric_cpu_utilization(
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
        '''(experimental) Metric for CPU utilization.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricCPUUtilization", [props]))

    @jsii.member(jsii_name="metricFreeStorageSpace")
    def metric_free_storage_space(
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
        '''(experimental) Metric for the storage space of nodes in the cluster.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: minimum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricFreeStorageSpace", [props]))

    @jsii.member(jsii_name="metricIndexingLatency")
    def metric_indexing_latency(
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
        '''(experimental) Metric for indexing latency.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: p99 over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricIndexingLatency", [props]))

    @jsii.member(jsii_name="metricJVMMemoryPressure")
    def metric_jvm_memory_pressure(
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
        '''(experimental) Metric for JVM memory pressure.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricJVMMemoryPressure", [props]))

    @jsii.member(jsii_name="metricKMSKeyError")
    def metric_kms_key_error(
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
        '''(experimental) Metric for KMS key errors.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricKMSKeyError", [props]))

    @jsii.member(jsii_name="metricKMSKeyInaccessible")
    def metric_kms_key_inaccessible(
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
        '''(experimental) Metric for KMS key being inaccessible.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricKMSKeyInaccessible", [props]))

    @jsii.member(jsii_name="metricMasterCPUUtilization")
    def metric_master_cpu_utilization(
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
        '''(experimental) Metric for master CPU utilization.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricMasterCPUUtilization", [props]))

    @jsii.member(jsii_name="metricMasterJVMMemoryPressure")
    def metric_master_jvm_memory_pressure(
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
        '''(experimental) Metric for master JVM memory pressure.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricMasterJVMMemoryPressure", [props]))

    @jsii.member(jsii_name="metricNodes")
    def metric_nodes(
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
        '''(experimental) Metric for the number of nodes.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: minimum over 1 hour

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricNodes", [props]))

    @jsii.member(jsii_name="metricSearchableDocuments")
    def metric_searchable_documents(
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
        '''(experimental) Metric for number of searchable documents.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: maximum over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSearchableDocuments", [props]))

    @jsii.member(jsii_name="metricSearchLatency")
    def metric_search_latency(
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
        '''(experimental) Metric for search latency.

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: p99 over 5 minutes

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricSearchLatency", [props]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainArn")
    def domain_arn(self) -> builtins.str:
        '''(experimental) Arn of the Elasticsearch domain.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainEndpoint")
    def domain_endpoint(self) -> builtins.str:
        '''(experimental) Endpoint of the Elasticsearch domain.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainEndpoint"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''(experimental) Domain name of the Elasticsearch domain.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="appLogGroup")
    def app_log_group(self) -> typing.Optional[_ILogGroup_846e17a0]:
        '''(experimental) Log group that application logs are logged to.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.Optional[_ILogGroup_846e17a0], jsii.get(self, "appLogGroup"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="auditLogGroup")
    def audit_log_group(self) -> typing.Optional[_ILogGroup_846e17a0]:
        '''(experimental) Log group that audit logs are logged to.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.Optional[_ILogGroup_846e17a0], jsii.get(self, "auditLogGroup"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="masterUserPassword")
    def master_user_password(self) -> typing.Optional[_SecretValue_c18506ef]:
        '''(experimental) Master user password if fine grained access control is configured.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_SecretValue_c18506ef], jsii.get(self, "masterUserPassword"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="slowIndexLogGroup")
    def slow_index_log_group(self) -> typing.Optional[_ILogGroup_846e17a0]:
        '''(experimental) Log group that slow indices are logged to.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.Optional[_ILogGroup_846e17a0], jsii.get(self, "slowIndexLogGroup"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="slowSearchLogGroup")
    def slow_search_log_group(self) -> typing.Optional[_ILogGroup_846e17a0]:
        '''(experimental) Log group that slow searches are logged to.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.Optional[_ILogGroup_846e17a0], jsii.get(self, "slowSearchLogGroup"))


__all__ = [
    "AdvancedSecurityOptions",
    "CapacityConfig",
    "CfnDomain",
    "CfnDomainProps",
    "CognitoOptions",
    "CustomEndpointOptions",
    "Domain",
    "DomainAttributes",
    "DomainProps",
    "EbsOptions",
    "ElasticsearchVersion",
    "EncryptionAtRestOptions",
    "IDomain",
    "LoggingOptions",
    "TLSSecurityPolicy",
    "VpcOptions",
    "ZoneAwarenessConfig",
]

publication.publish()
