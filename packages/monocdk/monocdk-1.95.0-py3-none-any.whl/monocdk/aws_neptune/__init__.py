'''
# Amazon Neptune Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

Amazon Neptune is a fast, reliable, fully managed graph database service that makes it easy to build and run applications that work with highly connected datasets. The core of Neptune is a purpose-built, high-performance graph database engine. This engine is optimized for storing billions of relationships and querying the graph with milliseconds latency. Neptune supports the popular graph query languages Apache TinkerPop Gremlin and W3C’s SPARQL, enabling you to build queries that efficiently navigate highly connected datasets.

The `@aws-cdk/aws-neptune` package contains primitives for setting up Neptune database clusters and instances.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_neptune as neptune
```

## Starting a Neptune Database

To set up a Neptune database, define a `DatabaseCluster`. You must always launch a database in a VPC.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
cluster = neptune.DatabaseCluster(self, "Database",
    vpc=vpc,
    instance_type=neptune.InstanceType.R5_LARGE
)
```

By default only writer instance is provisioned with this construct.

## Connecting

To control who can access the cluster, use the `.connections` attribute. Neptune databases have a default port, so
you don't need to specify the port:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
cluster.connections.allow_default_port_from_any_ipv4("Open to the world")
```

The endpoints to access your database cluster will be available as the `.clusterEndpoint` and `.clusterReadEndpoint`
attributes:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
write_address = cluster.cluster_endpoint.socket_address
```

## IAM Authentication

You can also authenticate to a database cluster using AWS Identity and Access Management (IAM) database authentication;
See [https://docs.aws.amazon.com/neptune/latest/userguide/iam-auth.html](https://docs.aws.amazon.com/neptune/latest/userguide/iam-auth.html) for more information and a list of supported
versions and limitations.

The following example shows enabling IAM authentication for a database cluster and granting connection access to an IAM role.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
cluster = neptune.DatabaseCluster(self, "Cluster",
    vpc=vpc,
    instance_type=neptune.InstanceType.R5_LARGE,
    iam_authentication=True
)
role = iam.Role(self, "DBRole", assumed_by=iam.AccountPrincipal(self.account))
cluster.grant_connect(role)
```

## Customizing parameters

Neptune allows configuring database behavior by supplying custom parameter groups.  For more details, refer to the
following link: [https://docs.aws.amazon.com/neptune/latest/userguide/parameters.html](https://docs.aws.amazon.com/neptune/latest/userguide/parameters.html)

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
cluster_params = neptune.ClusterParameterGroup(self, "ClusterParams",
    description="Cluster parameter group",
    parameters={
        "neptune_enable_audit_log": "1"
    }
)

db_params = neptune.ParameterGroup(self, "DbParams",
    description="Db parameter group",
    parameters={
        "neptune_query_timeout": "120000"
    }
)

cluster = neptune.DatabaseCluster(self, "Database",
    vpc=vpc,
    instance_type=neptune.InstanceType.R5_LARGE,
    cluster_parameter_group=cluster_params,
    parameter_group=db_params
)
```

## Adding replicas

`DatabaseCluster` allows launching replicas along with the writer instance. This can be specified using the `instanceCount`
attribute.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
cluster = neptune.DatabaseCluster(self, "Database",
    vpc=vpc,
    instance_type=neptune.InstanceType.R5_LARGE,
    instances=2
)
```

Additionally it is also possible to add replicas using `DatabaseInstance` for an existing cluster.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
replica1 = neptune.DatabaseInstance(self, "Instance",
    cluster=cluster,
    instance_type=neptune.InstanceType.R5_LARGE
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
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    Duration as _Duration_070aa057,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    RemovalPolicy as _RemovalPolicy_c97e7a20,
    Resource as _Resource_abff4495,
    ResourceProps as _ResourceProps_9b554c0f,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_ec2 import (
    Connections as _Connections_57ccbda9,
    IConnectable as _IConnectable_c1c0e72c,
    ISecurityGroup as _ISecurityGroup_cdbba9d3,
    IVpc as _IVpc_6d1f76c4,
    SubnetSelection as _SubnetSelection_1284e62c,
)
from ..aws_iam import (
    Grant as _Grant_bcb5eae7,
    IGrantable as _IGrantable_4c5a91d1,
    IRole as _IRole_59af6f50,
)
from ..aws_kms import IKey as _IKey_36930160


@jsii.implements(_IInspectable_82c04a63)
class CfnDBCluster(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_neptune.CfnDBCluster",
):
    '''A CloudFormation ``AWS::Neptune::DBCluster``.

    :cloudformationResource: AWS::Neptune::DBCluster
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        associated_roles: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDBCluster.DBClusterRoleProperty", _IResolvable_a771d0ef]]]] = None,
        availability_zones: typing.Optional[typing.List[builtins.str]] = None,
        backup_retention_period: typing.Optional[jsii.Number] = None,
        db_cluster_identifier: typing.Optional[builtins.str] = None,
        db_cluster_parameter_group_name: typing.Optional[builtins.str] = None,
        db_subnet_group_name: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        enable_cloudwatch_logs_exports: typing.Optional[typing.List[builtins.str]] = None,
        engine_version: typing.Optional[builtins.str] = None,
        iam_auth_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        restore_to_time: typing.Optional[builtins.str] = None,
        restore_type: typing.Optional[builtins.str] = None,
        snapshot_identifier: typing.Optional[builtins.str] = None,
        source_db_cluster_identifier: typing.Optional[builtins.str] = None,
        storage_encrypted: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
        use_latest_restorable_time: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        vpc_security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::Neptune::DBCluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param associated_roles: ``AWS::Neptune::DBCluster.AssociatedRoles``.
        :param availability_zones: ``AWS::Neptune::DBCluster.AvailabilityZones``.
        :param backup_retention_period: ``AWS::Neptune::DBCluster.BackupRetentionPeriod``.
        :param db_cluster_identifier: ``AWS::Neptune::DBCluster.DBClusterIdentifier``.
        :param db_cluster_parameter_group_name: ``AWS::Neptune::DBCluster.DBClusterParameterGroupName``.
        :param db_subnet_group_name: ``AWS::Neptune::DBCluster.DBSubnetGroupName``.
        :param deletion_protection: ``AWS::Neptune::DBCluster.DeletionProtection``.
        :param enable_cloudwatch_logs_exports: ``AWS::Neptune::DBCluster.EnableCloudwatchLogsExports``.
        :param engine_version: ``AWS::Neptune::DBCluster.EngineVersion``.
        :param iam_auth_enabled: ``AWS::Neptune::DBCluster.IamAuthEnabled``.
        :param kms_key_id: ``AWS::Neptune::DBCluster.KmsKeyId``.
        :param port: ``AWS::Neptune::DBCluster.Port``.
        :param preferred_backup_window: ``AWS::Neptune::DBCluster.PreferredBackupWindow``.
        :param preferred_maintenance_window: ``AWS::Neptune::DBCluster.PreferredMaintenanceWindow``.
        :param restore_to_time: ``AWS::Neptune::DBCluster.RestoreToTime``.
        :param restore_type: ``AWS::Neptune::DBCluster.RestoreType``.
        :param snapshot_identifier: ``AWS::Neptune::DBCluster.SnapshotIdentifier``.
        :param source_db_cluster_identifier: ``AWS::Neptune::DBCluster.SourceDBClusterIdentifier``.
        :param storage_encrypted: ``AWS::Neptune::DBCluster.StorageEncrypted``.
        :param tags: ``AWS::Neptune::DBCluster.Tags``.
        :param use_latest_restorable_time: ``AWS::Neptune::DBCluster.UseLatestRestorableTime``.
        :param vpc_security_group_ids: ``AWS::Neptune::DBCluster.VpcSecurityGroupIds``.
        '''
        props = CfnDBClusterProps(
            associated_roles=associated_roles,
            availability_zones=availability_zones,
            backup_retention_period=backup_retention_period,
            db_cluster_identifier=db_cluster_identifier,
            db_cluster_parameter_group_name=db_cluster_parameter_group_name,
            db_subnet_group_name=db_subnet_group_name,
            deletion_protection=deletion_protection,
            enable_cloudwatch_logs_exports=enable_cloudwatch_logs_exports,
            engine_version=engine_version,
            iam_auth_enabled=iam_auth_enabled,
            kms_key_id=kms_key_id,
            port=port,
            preferred_backup_window=preferred_backup_window,
            preferred_maintenance_window=preferred_maintenance_window,
            restore_to_time=restore_to_time,
            restore_type=restore_type,
            snapshot_identifier=snapshot_identifier,
            source_db_cluster_identifier=source_db_cluster_identifier,
            storage_encrypted=storage_encrypted,
            tags=tags,
            use_latest_restorable_time=use_latest_restorable_time,
            vpc_security_group_ids=vpc_security_group_ids,
        )

        jsii.create(CfnDBCluster, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrClusterResourceId")
    def attr_cluster_resource_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: ClusterResourceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrClusterResourceId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrEndpoint")
    def attr_endpoint(self) -> builtins.str:
        '''
        :cloudformationAttribute: Endpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEndpoint"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrPort")
    def attr_port(self) -> builtins.str:
        '''
        :cloudformationAttribute: Port
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPort"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrReadEndpoint")
    def attr_read_endpoint(self) -> builtins.str:
        '''
        :cloudformationAttribute: ReadEndpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrReadEndpoint"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::Neptune::DBCluster.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="associatedRoles")
    def associated_roles(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDBCluster.DBClusterRoleProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::Neptune::DBCluster.AssociatedRoles``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-associatedroles
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDBCluster.DBClusterRoleProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "associatedRoles"))

    @associated_roles.setter
    def associated_roles(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDBCluster.DBClusterRoleProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "associatedRoles", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Neptune::DBCluster.AvailabilityZones``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-availabilityzones
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "availabilityZones"))

    @availability_zones.setter
    def availability_zones(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "availabilityZones", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupRetentionPeriod")
    def backup_retention_period(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Neptune::DBCluster.BackupRetentionPeriod``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-backupretentionperiod
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backupRetentionPeriod"))

    @backup_retention_period.setter
    def backup_retention_period(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "backupRetentionPeriod", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dbClusterIdentifier")
    def db_cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.DBClusterIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-dbclusteridentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbClusterIdentifier"))

    @db_cluster_identifier.setter
    def db_cluster_identifier(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "dbClusterIdentifier", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dbClusterParameterGroupName")
    def db_cluster_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.DBClusterParameterGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-dbclusterparametergroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbClusterParameterGroupName"))

    @db_cluster_parameter_group_name.setter
    def db_cluster_parameter_group_name(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "dbClusterParameterGroupName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dbSubnetGroupName")
    def db_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.DBSubnetGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-dbsubnetgroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbSubnetGroupName"))

    @db_subnet_group_name.setter
    def db_subnet_group_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "dbSubnetGroupName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Neptune::DBCluster.DeletionProtection``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-deletionprotection
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "deletionProtection"))

    @deletion_protection.setter
    def deletion_protection(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "deletionProtection", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enableCloudwatchLogsExports")
    def enable_cloudwatch_logs_exports(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Neptune::DBCluster.EnableCloudwatchLogsExports``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-enablecloudwatchlogsexports
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "enableCloudwatchLogsExports"))

    @enable_cloudwatch_logs_exports.setter
    def enable_cloudwatch_logs_exports(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "enableCloudwatchLogsExports", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.EngineVersion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-engineversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineVersion"))

    @engine_version.setter
    def engine_version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "engineVersion", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="iamAuthEnabled")
    def iam_auth_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Neptune::DBCluster.IamAuthEnabled``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-iamauthenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "iamAuthEnabled"))

    @iam_auth_enabled.setter
    def iam_auth_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "iamAuthEnabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.KmsKeyId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "kmsKeyId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Neptune::DBCluster.Port``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-port
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "port"))

    @port.setter
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "port", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="preferredBackupWindow")
    def preferred_backup_window(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.PreferredBackupWindow``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-preferredbackupwindow
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredBackupWindow"))

    @preferred_backup_window.setter
    def preferred_backup_window(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "preferredBackupWindow", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.PreferredMaintenanceWindow``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-preferredmaintenancewindow
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredMaintenanceWindow"))

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="restoreToTime")
    def restore_to_time(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.RestoreToTime``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-restoretotime
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "restoreToTime"))

    @restore_to_time.setter
    def restore_to_time(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "restoreToTime", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="restoreType")
    def restore_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.RestoreType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-restoretype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "restoreType"))

    @restore_type.setter
    def restore_type(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "restoreType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="snapshotIdentifier")
    def snapshot_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.SnapshotIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-snapshotidentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotIdentifier"))

    @snapshot_identifier.setter
    def snapshot_identifier(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "snapshotIdentifier", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sourceDbClusterIdentifier")
    def source_db_cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.SourceDBClusterIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-sourcedbclusteridentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceDbClusterIdentifier"))

    @source_db_cluster_identifier.setter
    def source_db_cluster_identifier(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "sourceDbClusterIdentifier", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="storageEncrypted")
    def storage_encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Neptune::DBCluster.StorageEncrypted``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-storageencrypted
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "storageEncrypted"))

    @storage_encrypted.setter
    def storage_encrypted(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "storageEncrypted", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="useLatestRestorableTime")
    def use_latest_restorable_time(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Neptune::DBCluster.UseLatestRestorableTime``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-uselatestrestorabletime
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "useLatestRestorableTime"))

    @use_latest_restorable_time.setter
    def use_latest_restorable_time(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "useLatestRestorableTime", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Neptune::DBCluster.VpcSecurityGroupIds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-vpcsecuritygroupids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "vpcSecurityGroupIds"))

    @vpc_security_group_ids.setter
    def vpc_security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "vpcSecurityGroupIds", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_neptune.CfnDBCluster.DBClusterRoleProperty",
        jsii_struct_bases=[],
        name_mapping={"role_arn": "roleArn", "feature_name": "featureName"},
    )
    class DBClusterRoleProperty:
        def __init__(
            self,
            *,
            role_arn: builtins.str,
            feature_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param role_arn: ``CfnDBCluster.DBClusterRoleProperty.RoleArn``.
            :param feature_name: ``CfnDBCluster.DBClusterRoleProperty.FeatureName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-neptune-dbcluster-dbclusterrole.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "role_arn": role_arn,
            }
            if feature_name is not None:
                self._values["feature_name"] = feature_name

        @builtins.property
        def role_arn(self) -> builtins.str:
            '''``CfnDBCluster.DBClusterRoleProperty.RoleArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-neptune-dbcluster-dbclusterrole.html#cfn-neptune-dbcluster-dbclusterrole-rolearn
            '''
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def feature_name(self) -> typing.Optional[builtins.str]:
            '''``CfnDBCluster.DBClusterRoleProperty.FeatureName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-neptune-dbcluster-dbclusterrole.html#cfn-neptune-dbcluster-dbclusterrole-featurename
            '''
            result = self._values.get("feature_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DBClusterRoleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnDBClusterParameterGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_neptune.CfnDBClusterParameterGroup",
):
    '''A CloudFormation ``AWS::Neptune::DBClusterParameterGroup``.

    :cloudformationResource: AWS::Neptune::DBClusterParameterGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        description: builtins.str,
        family: builtins.str,
        parameters: typing.Any,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Create a new ``AWS::Neptune::DBClusterParameterGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::Neptune::DBClusterParameterGroup.Description``.
        :param family: ``AWS::Neptune::DBClusterParameterGroup.Family``.
        :param parameters: ``AWS::Neptune::DBClusterParameterGroup.Parameters``.
        :param name: ``AWS::Neptune::DBClusterParameterGroup.Name``.
        :param tags: ``AWS::Neptune::DBClusterParameterGroup.Tags``.
        '''
        props = CfnDBClusterParameterGroupProps(
            description=description,
            family=family,
            parameters=parameters,
            name=name,
            tags=tags,
        )

        jsii.create(CfnDBClusterParameterGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::Neptune::DBClusterParameterGroup.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html#cfn-neptune-dbclusterparametergroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''``AWS::Neptune::DBClusterParameterGroup.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html#cfn-neptune-dbclusterparametergroup-description
        '''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="family")
    def family(self) -> builtins.str:
        '''``AWS::Neptune::DBClusterParameterGroup.Family``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html#cfn-neptune-dbclusterparametergroup-family
        '''
        return typing.cast(builtins.str, jsii.get(self, "family"))

    @family.setter
    def family(self, value: builtins.str) -> None:
        jsii.set(self, "family", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Any:
        '''``AWS::Neptune::DBClusterParameterGroup.Parameters``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html#cfn-neptune-dbclusterparametergroup-parameters
        '''
        return typing.cast(typing.Any, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Any) -> None:
        jsii.set(self, "parameters", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBClusterParameterGroup.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html#cfn-neptune-dbclusterparametergroup-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="monocdk.aws_neptune.CfnDBClusterParameterGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "family": "family",
        "parameters": "parameters",
        "name": "name",
        "tags": "tags",
    },
)
class CfnDBClusterParameterGroupProps:
    def __init__(
        self,
        *,
        description: builtins.str,
        family: builtins.str,
        parameters: typing.Any,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Neptune::DBClusterParameterGroup``.

        :param description: ``AWS::Neptune::DBClusterParameterGroup.Description``.
        :param family: ``AWS::Neptune::DBClusterParameterGroup.Family``.
        :param parameters: ``AWS::Neptune::DBClusterParameterGroup.Parameters``.
        :param name: ``AWS::Neptune::DBClusterParameterGroup.Name``.
        :param tags: ``AWS::Neptune::DBClusterParameterGroup.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "description": description,
            "family": family,
            "parameters": parameters,
        }
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> builtins.str:
        '''``AWS::Neptune::DBClusterParameterGroup.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html#cfn-neptune-dbclusterparametergroup-description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def family(self) -> builtins.str:
        '''``AWS::Neptune::DBClusterParameterGroup.Family``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html#cfn-neptune-dbclusterparametergroup-family
        '''
        result = self._values.get("family")
        assert result is not None, "Required property 'family' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''``AWS::Neptune::DBClusterParameterGroup.Parameters``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html#cfn-neptune-dbclusterparametergroup-parameters
        '''
        result = self._values.get("parameters")
        assert result is not None, "Required property 'parameters' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBClusterParameterGroup.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html#cfn-neptune-dbclusterparametergroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::Neptune::DBClusterParameterGroup.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbclusterparametergroup.html#cfn-neptune-dbclusterparametergroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBClusterParameterGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_neptune.CfnDBClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "associated_roles": "associatedRoles",
        "availability_zones": "availabilityZones",
        "backup_retention_period": "backupRetentionPeriod",
        "db_cluster_identifier": "dbClusterIdentifier",
        "db_cluster_parameter_group_name": "dbClusterParameterGroupName",
        "db_subnet_group_name": "dbSubnetGroupName",
        "deletion_protection": "deletionProtection",
        "enable_cloudwatch_logs_exports": "enableCloudwatchLogsExports",
        "engine_version": "engineVersion",
        "iam_auth_enabled": "iamAuthEnabled",
        "kms_key_id": "kmsKeyId",
        "port": "port",
        "preferred_backup_window": "preferredBackupWindow",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "restore_to_time": "restoreToTime",
        "restore_type": "restoreType",
        "snapshot_identifier": "snapshotIdentifier",
        "source_db_cluster_identifier": "sourceDbClusterIdentifier",
        "storage_encrypted": "storageEncrypted",
        "tags": "tags",
        "use_latest_restorable_time": "useLatestRestorableTime",
        "vpc_security_group_ids": "vpcSecurityGroupIds",
    },
)
class CfnDBClusterProps:
    def __init__(
        self,
        *,
        associated_roles: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnDBCluster.DBClusterRoleProperty, _IResolvable_a771d0ef]]]] = None,
        availability_zones: typing.Optional[typing.List[builtins.str]] = None,
        backup_retention_period: typing.Optional[jsii.Number] = None,
        db_cluster_identifier: typing.Optional[builtins.str] = None,
        db_cluster_parameter_group_name: typing.Optional[builtins.str] = None,
        db_subnet_group_name: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        enable_cloudwatch_logs_exports: typing.Optional[typing.List[builtins.str]] = None,
        engine_version: typing.Optional[builtins.str] = None,
        iam_auth_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        restore_to_time: typing.Optional[builtins.str] = None,
        restore_type: typing.Optional[builtins.str] = None,
        snapshot_identifier: typing.Optional[builtins.str] = None,
        source_db_cluster_identifier: typing.Optional[builtins.str] = None,
        storage_encrypted: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
        use_latest_restorable_time: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        vpc_security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Neptune::DBCluster``.

        :param associated_roles: ``AWS::Neptune::DBCluster.AssociatedRoles``.
        :param availability_zones: ``AWS::Neptune::DBCluster.AvailabilityZones``.
        :param backup_retention_period: ``AWS::Neptune::DBCluster.BackupRetentionPeriod``.
        :param db_cluster_identifier: ``AWS::Neptune::DBCluster.DBClusterIdentifier``.
        :param db_cluster_parameter_group_name: ``AWS::Neptune::DBCluster.DBClusterParameterGroupName``.
        :param db_subnet_group_name: ``AWS::Neptune::DBCluster.DBSubnetGroupName``.
        :param deletion_protection: ``AWS::Neptune::DBCluster.DeletionProtection``.
        :param enable_cloudwatch_logs_exports: ``AWS::Neptune::DBCluster.EnableCloudwatchLogsExports``.
        :param engine_version: ``AWS::Neptune::DBCluster.EngineVersion``.
        :param iam_auth_enabled: ``AWS::Neptune::DBCluster.IamAuthEnabled``.
        :param kms_key_id: ``AWS::Neptune::DBCluster.KmsKeyId``.
        :param port: ``AWS::Neptune::DBCluster.Port``.
        :param preferred_backup_window: ``AWS::Neptune::DBCluster.PreferredBackupWindow``.
        :param preferred_maintenance_window: ``AWS::Neptune::DBCluster.PreferredMaintenanceWindow``.
        :param restore_to_time: ``AWS::Neptune::DBCluster.RestoreToTime``.
        :param restore_type: ``AWS::Neptune::DBCluster.RestoreType``.
        :param snapshot_identifier: ``AWS::Neptune::DBCluster.SnapshotIdentifier``.
        :param source_db_cluster_identifier: ``AWS::Neptune::DBCluster.SourceDBClusterIdentifier``.
        :param storage_encrypted: ``AWS::Neptune::DBCluster.StorageEncrypted``.
        :param tags: ``AWS::Neptune::DBCluster.Tags``.
        :param use_latest_restorable_time: ``AWS::Neptune::DBCluster.UseLatestRestorableTime``.
        :param vpc_security_group_ids: ``AWS::Neptune::DBCluster.VpcSecurityGroupIds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if associated_roles is not None:
            self._values["associated_roles"] = associated_roles
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if backup_retention_period is not None:
            self._values["backup_retention_period"] = backup_retention_period
        if db_cluster_identifier is not None:
            self._values["db_cluster_identifier"] = db_cluster_identifier
        if db_cluster_parameter_group_name is not None:
            self._values["db_cluster_parameter_group_name"] = db_cluster_parameter_group_name
        if db_subnet_group_name is not None:
            self._values["db_subnet_group_name"] = db_subnet_group_name
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if enable_cloudwatch_logs_exports is not None:
            self._values["enable_cloudwatch_logs_exports"] = enable_cloudwatch_logs_exports
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if iam_auth_enabled is not None:
            self._values["iam_auth_enabled"] = iam_auth_enabled
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if port is not None:
            self._values["port"] = port
        if preferred_backup_window is not None:
            self._values["preferred_backup_window"] = preferred_backup_window
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if restore_to_time is not None:
            self._values["restore_to_time"] = restore_to_time
        if restore_type is not None:
            self._values["restore_type"] = restore_type
        if snapshot_identifier is not None:
            self._values["snapshot_identifier"] = snapshot_identifier
        if source_db_cluster_identifier is not None:
            self._values["source_db_cluster_identifier"] = source_db_cluster_identifier
        if storage_encrypted is not None:
            self._values["storage_encrypted"] = storage_encrypted
        if tags is not None:
            self._values["tags"] = tags
        if use_latest_restorable_time is not None:
            self._values["use_latest_restorable_time"] = use_latest_restorable_time
        if vpc_security_group_ids is not None:
            self._values["vpc_security_group_ids"] = vpc_security_group_ids

    @builtins.property
    def associated_roles(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnDBCluster.DBClusterRoleProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::Neptune::DBCluster.AssociatedRoles``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-associatedroles
        '''
        result = self._values.get("associated_roles")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnDBCluster.DBClusterRoleProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Neptune::DBCluster.AvailabilityZones``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-availabilityzones
        '''
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def backup_retention_period(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Neptune::DBCluster.BackupRetentionPeriod``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-backupretentionperiod
        '''
        result = self._values.get("backup_retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def db_cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.DBClusterIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-dbclusteridentifier
        '''
        result = self._values.get("db_cluster_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_cluster_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.DBClusterParameterGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-dbclusterparametergroupname
        '''
        result = self._values.get("db_cluster_parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.DBSubnetGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-dbsubnetgroupname
        '''
        result = self._values.get("db_subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Neptune::DBCluster.DeletionProtection``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-deletionprotection
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def enable_cloudwatch_logs_exports(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Neptune::DBCluster.EnableCloudwatchLogsExports``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-enablecloudwatchlogsexports
        '''
        result = self._values.get("enable_cloudwatch_logs_exports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.EngineVersion``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iam_auth_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Neptune::DBCluster.IamAuthEnabled``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-iamauthenabled
        '''
        result = self._values.get("iam_auth_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.KmsKeyId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''``AWS::Neptune::DBCluster.Port``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preferred_backup_window(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.PreferredBackupWindow``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-preferredbackupwindow
        '''
        result = self._values.get("preferred_backup_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.PreferredMaintenanceWindow``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-preferredmaintenancewindow
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restore_to_time(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.RestoreToTime``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-restoretotime
        '''
        result = self._values.get("restore_to_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restore_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.RestoreType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-restoretype
        '''
        result = self._values.get("restore_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.SnapshotIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-snapshotidentifier
        '''
        result = self._values.get("snapshot_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_db_cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBCluster.SourceDBClusterIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-sourcedbclusteridentifier
        '''
        result = self._values.get("source_db_cluster_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Neptune::DBCluster.StorageEncrypted``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-storageencrypted
        '''
        result = self._values.get("storage_encrypted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::Neptune::DBCluster.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def use_latest_restorable_time(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Neptune::DBCluster.UseLatestRestorableTime``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-uselatestrestorabletime
        '''
        result = self._values.get("use_latest_restorable_time")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::Neptune::DBCluster.VpcSecurityGroupIds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbcluster.html#cfn-neptune-dbcluster-vpcsecuritygroupids
        '''
        result = self._values.get("vpc_security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnDBInstance(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_neptune.CfnDBInstance",
):
    '''A CloudFormation ``AWS::Neptune::DBInstance``.

    :cloudformationResource: AWS::Neptune::DBInstance
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        db_instance_class: builtins.str,
        allow_major_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        db_cluster_identifier: typing.Optional[builtins.str] = None,
        db_instance_identifier: typing.Optional[builtins.str] = None,
        db_parameter_group_name: typing.Optional[builtins.str] = None,
        db_snapshot_identifier: typing.Optional[builtins.str] = None,
        db_subnet_group_name: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Create a new ``AWS::Neptune::DBInstance``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param db_instance_class: ``AWS::Neptune::DBInstance.DBInstanceClass``.
        :param allow_major_version_upgrade: ``AWS::Neptune::DBInstance.AllowMajorVersionUpgrade``.
        :param auto_minor_version_upgrade: ``AWS::Neptune::DBInstance.AutoMinorVersionUpgrade``.
        :param availability_zone: ``AWS::Neptune::DBInstance.AvailabilityZone``.
        :param db_cluster_identifier: ``AWS::Neptune::DBInstance.DBClusterIdentifier``.
        :param db_instance_identifier: ``AWS::Neptune::DBInstance.DBInstanceIdentifier``.
        :param db_parameter_group_name: ``AWS::Neptune::DBInstance.DBParameterGroupName``.
        :param db_snapshot_identifier: ``AWS::Neptune::DBInstance.DBSnapshotIdentifier``.
        :param db_subnet_group_name: ``AWS::Neptune::DBInstance.DBSubnetGroupName``.
        :param preferred_maintenance_window: ``AWS::Neptune::DBInstance.PreferredMaintenanceWindow``.
        :param tags: ``AWS::Neptune::DBInstance.Tags``.
        '''
        props = CfnDBInstanceProps(
            db_instance_class=db_instance_class,
            allow_major_version_upgrade=allow_major_version_upgrade,
            auto_minor_version_upgrade=auto_minor_version_upgrade,
            availability_zone=availability_zone,
            db_cluster_identifier=db_cluster_identifier,
            db_instance_identifier=db_instance_identifier,
            db_parameter_group_name=db_parameter_group_name,
            db_snapshot_identifier=db_snapshot_identifier,
            db_subnet_group_name=db_subnet_group_name,
            preferred_maintenance_window=preferred_maintenance_window,
            tags=tags,
        )

        jsii.create(CfnDBInstance, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrEndpoint")
    def attr_endpoint(self) -> builtins.str:
        '''
        :cloudformationAttribute: Endpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEndpoint"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrPort")
    def attr_port(self) -> builtins.str:
        '''
        :cloudformationAttribute: Port
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPort"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::Neptune::DBInstance.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dbInstanceClass")
    def db_instance_class(self) -> builtins.str:
        '''``AWS::Neptune::DBInstance.DBInstanceClass``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbinstanceclass
        '''
        return typing.cast(builtins.str, jsii.get(self, "dbInstanceClass"))

    @db_instance_class.setter
    def db_instance_class(self, value: builtins.str) -> None:
        jsii.set(self, "dbInstanceClass", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="allowMajorVersionUpgrade")
    def allow_major_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Neptune::DBInstance.AllowMajorVersionUpgrade``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-allowmajorversionupgrade
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "allowMajorVersionUpgrade"))

    @allow_major_version_upgrade.setter
    def allow_major_version_upgrade(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "allowMajorVersionUpgrade", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="autoMinorVersionUpgrade")
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Neptune::DBInstance.AutoMinorVersionUpgrade``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-autominorversionupgrade
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "autoMinorVersionUpgrade"))

    @auto_minor_version_upgrade.setter
    def auto_minor_version_upgrade(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "autoMinorVersionUpgrade", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBInstance.AvailabilityZone``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-availabilityzone
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "availabilityZone", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dbClusterIdentifier")
    def db_cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBInstance.DBClusterIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbclusteridentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbClusterIdentifier"))

    @db_cluster_identifier.setter
    def db_cluster_identifier(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "dbClusterIdentifier", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dbInstanceIdentifier")
    def db_instance_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBInstance.DBInstanceIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbinstanceidentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbInstanceIdentifier"))

    @db_instance_identifier.setter
    def db_instance_identifier(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "dbInstanceIdentifier", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dbParameterGroupName")
    def db_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBInstance.DBParameterGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbparametergroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbParameterGroupName"))

    @db_parameter_group_name.setter
    def db_parameter_group_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "dbParameterGroupName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dbSnapshotIdentifier")
    def db_snapshot_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBInstance.DBSnapshotIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbsnapshotidentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbSnapshotIdentifier"))

    @db_snapshot_identifier.setter
    def db_snapshot_identifier(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "dbSnapshotIdentifier", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dbSubnetGroupName")
    def db_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBInstance.DBSubnetGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbsubnetgroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbSubnetGroupName"))

    @db_subnet_group_name.setter
    def db_subnet_group_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "dbSubnetGroupName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBInstance.PreferredMaintenanceWindow``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-preferredmaintenancewindow
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredMaintenanceWindow"))

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "preferredMaintenanceWindow", value)


@jsii.data_type(
    jsii_type="monocdk.aws_neptune.CfnDBInstanceProps",
    jsii_struct_bases=[],
    name_mapping={
        "db_instance_class": "dbInstanceClass",
        "allow_major_version_upgrade": "allowMajorVersionUpgrade",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "availability_zone": "availabilityZone",
        "db_cluster_identifier": "dbClusterIdentifier",
        "db_instance_identifier": "dbInstanceIdentifier",
        "db_parameter_group_name": "dbParameterGroupName",
        "db_snapshot_identifier": "dbSnapshotIdentifier",
        "db_subnet_group_name": "dbSubnetGroupName",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "tags": "tags",
    },
)
class CfnDBInstanceProps:
    def __init__(
        self,
        *,
        db_instance_class: builtins.str,
        allow_major_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        auto_minor_version_upgrade: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        db_cluster_identifier: typing.Optional[builtins.str] = None,
        db_instance_identifier: typing.Optional[builtins.str] = None,
        db_parameter_group_name: typing.Optional[builtins.str] = None,
        db_snapshot_identifier: typing.Optional[builtins.str] = None,
        db_subnet_group_name: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Neptune::DBInstance``.

        :param db_instance_class: ``AWS::Neptune::DBInstance.DBInstanceClass``.
        :param allow_major_version_upgrade: ``AWS::Neptune::DBInstance.AllowMajorVersionUpgrade``.
        :param auto_minor_version_upgrade: ``AWS::Neptune::DBInstance.AutoMinorVersionUpgrade``.
        :param availability_zone: ``AWS::Neptune::DBInstance.AvailabilityZone``.
        :param db_cluster_identifier: ``AWS::Neptune::DBInstance.DBClusterIdentifier``.
        :param db_instance_identifier: ``AWS::Neptune::DBInstance.DBInstanceIdentifier``.
        :param db_parameter_group_name: ``AWS::Neptune::DBInstance.DBParameterGroupName``.
        :param db_snapshot_identifier: ``AWS::Neptune::DBInstance.DBSnapshotIdentifier``.
        :param db_subnet_group_name: ``AWS::Neptune::DBInstance.DBSubnetGroupName``.
        :param preferred_maintenance_window: ``AWS::Neptune::DBInstance.PreferredMaintenanceWindow``.
        :param tags: ``AWS::Neptune::DBInstance.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "db_instance_class": db_instance_class,
        }
        if allow_major_version_upgrade is not None:
            self._values["allow_major_version_upgrade"] = allow_major_version_upgrade
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if db_cluster_identifier is not None:
            self._values["db_cluster_identifier"] = db_cluster_identifier
        if db_instance_identifier is not None:
            self._values["db_instance_identifier"] = db_instance_identifier
        if db_parameter_group_name is not None:
            self._values["db_parameter_group_name"] = db_parameter_group_name
        if db_snapshot_identifier is not None:
            self._values["db_snapshot_identifier"] = db_snapshot_identifier
        if db_subnet_group_name is not None:
            self._values["db_subnet_group_name"] = db_subnet_group_name
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def db_instance_class(self) -> builtins.str:
        '''``AWS::Neptune::DBInstance.DBInstanceClass``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbinstanceclass
        '''
        result = self._values.get("db_instance_class")
        assert result is not None, "Required property 'db_instance_class' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_major_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Neptune::DBInstance.AllowMajorVersionUpgrade``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-allowmajorversionupgrade
        '''
        result = self._values.get("allow_major_version_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::Neptune::DBInstance.AutoMinorVersionUpgrade``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-autominorversionupgrade
        '''
        result = self._values.get("auto_minor_version_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBInstance.AvailabilityZone``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-availabilityzone
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_cluster_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBInstance.DBClusterIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbclusteridentifier
        '''
        result = self._values.get("db_cluster_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_instance_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBInstance.DBInstanceIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbinstanceidentifier
        '''
        result = self._values.get("db_instance_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBInstance.DBParameterGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbparametergroupname
        '''
        result = self._values.get("db_parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_snapshot_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBInstance.DBSnapshotIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbsnapshotidentifier
        '''
        result = self._values.get("db_snapshot_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBInstance.DBSubnetGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-dbsubnetgroupname
        '''
        result = self._values.get("db_subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBInstance.PreferredMaintenanceWindow``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-preferredmaintenancewindow
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::Neptune::DBInstance.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbinstance.html#cfn-neptune-dbinstance-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnDBParameterGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_neptune.CfnDBParameterGroup",
):
    '''A CloudFormation ``AWS::Neptune::DBParameterGroup``.

    :cloudformationResource: AWS::Neptune::DBParameterGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        description: builtins.str,
        family: builtins.str,
        parameters: typing.Any,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Create a new ``AWS::Neptune::DBParameterGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::Neptune::DBParameterGroup.Description``.
        :param family: ``AWS::Neptune::DBParameterGroup.Family``.
        :param parameters: ``AWS::Neptune::DBParameterGroup.Parameters``.
        :param name: ``AWS::Neptune::DBParameterGroup.Name``.
        :param tags: ``AWS::Neptune::DBParameterGroup.Tags``.
        '''
        props = CfnDBParameterGroupProps(
            description=description,
            family=family,
            parameters=parameters,
            name=name,
            tags=tags,
        )

        jsii.create(CfnDBParameterGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::Neptune::DBParameterGroup.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html#cfn-neptune-dbparametergroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''``AWS::Neptune::DBParameterGroup.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html#cfn-neptune-dbparametergroup-description
        '''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="family")
    def family(self) -> builtins.str:
        '''``AWS::Neptune::DBParameterGroup.Family``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html#cfn-neptune-dbparametergroup-family
        '''
        return typing.cast(builtins.str, jsii.get(self, "family"))

    @family.setter
    def family(self, value: builtins.str) -> None:
        jsii.set(self, "family", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Any:
        '''``AWS::Neptune::DBParameterGroup.Parameters``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html#cfn-neptune-dbparametergroup-parameters
        '''
        return typing.cast(typing.Any, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Any) -> None:
        jsii.set(self, "parameters", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBParameterGroup.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html#cfn-neptune-dbparametergroup-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="monocdk.aws_neptune.CfnDBParameterGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "family": "family",
        "parameters": "parameters",
        "name": "name",
        "tags": "tags",
    },
)
class CfnDBParameterGroupProps:
    def __init__(
        self,
        *,
        description: builtins.str,
        family: builtins.str,
        parameters: typing.Any,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Neptune::DBParameterGroup``.

        :param description: ``AWS::Neptune::DBParameterGroup.Description``.
        :param family: ``AWS::Neptune::DBParameterGroup.Family``.
        :param parameters: ``AWS::Neptune::DBParameterGroup.Parameters``.
        :param name: ``AWS::Neptune::DBParameterGroup.Name``.
        :param tags: ``AWS::Neptune::DBParameterGroup.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "description": description,
            "family": family,
            "parameters": parameters,
        }
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> builtins.str:
        '''``AWS::Neptune::DBParameterGroup.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html#cfn-neptune-dbparametergroup-description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def family(self) -> builtins.str:
        '''``AWS::Neptune::DBParameterGroup.Family``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html#cfn-neptune-dbparametergroup-family
        '''
        result = self._values.get("family")
        assert result is not None, "Required property 'family' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''``AWS::Neptune::DBParameterGroup.Parameters``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html#cfn-neptune-dbparametergroup-parameters
        '''
        result = self._values.get("parameters")
        assert result is not None, "Required property 'parameters' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBParameterGroup.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html#cfn-neptune-dbparametergroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::Neptune::DBParameterGroup.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbparametergroup.html#cfn-neptune-dbparametergroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBParameterGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnDBSubnetGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_neptune.CfnDBSubnetGroup",
):
    '''A CloudFormation ``AWS::Neptune::DBSubnetGroup``.

    :cloudformationResource: AWS::Neptune::DBSubnetGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbsubnetgroup.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        db_subnet_group_description: builtins.str,
        subnet_ids: typing.List[builtins.str],
        db_subnet_group_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Create a new ``AWS::Neptune::DBSubnetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param db_subnet_group_description: ``AWS::Neptune::DBSubnetGroup.DBSubnetGroupDescription``.
        :param subnet_ids: ``AWS::Neptune::DBSubnetGroup.SubnetIds``.
        :param db_subnet_group_name: ``AWS::Neptune::DBSubnetGroup.DBSubnetGroupName``.
        :param tags: ``AWS::Neptune::DBSubnetGroup.Tags``.
        '''
        props = CfnDBSubnetGroupProps(
            db_subnet_group_description=db_subnet_group_description,
            subnet_ids=subnet_ids,
            db_subnet_group_name=db_subnet_group_name,
            tags=tags,
        )

        jsii.create(CfnDBSubnetGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::Neptune::DBSubnetGroup.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbsubnetgroup.html#cfn-neptune-dbsubnetgroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dbSubnetGroupDescription")
    def db_subnet_group_description(self) -> builtins.str:
        '''``AWS::Neptune::DBSubnetGroup.DBSubnetGroupDescription``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbsubnetgroup.html#cfn-neptune-dbsubnetgroup-dbsubnetgroupdescription
        '''
        return typing.cast(builtins.str, jsii.get(self, "dbSubnetGroupDescription"))

    @db_subnet_group_description.setter
    def db_subnet_group_description(self, value: builtins.str) -> None:
        jsii.set(self, "dbSubnetGroupDescription", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''``AWS::Neptune::DBSubnetGroup.SubnetIds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbsubnetgroup.html#cfn-neptune-dbsubnetgroup-subnetids
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "subnetIds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dbSubnetGroupName")
    def db_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBSubnetGroup.DBSubnetGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbsubnetgroup.html#cfn-neptune-dbsubnetgroup-dbsubnetgroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbSubnetGroupName"))

    @db_subnet_group_name.setter
    def db_subnet_group_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "dbSubnetGroupName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_neptune.CfnDBSubnetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "db_subnet_group_description": "dbSubnetGroupDescription",
        "subnet_ids": "subnetIds",
        "db_subnet_group_name": "dbSubnetGroupName",
        "tags": "tags",
    },
)
class CfnDBSubnetGroupProps:
    def __init__(
        self,
        *,
        db_subnet_group_description: builtins.str,
        subnet_ids: typing.List[builtins.str],
        db_subnet_group_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Neptune::DBSubnetGroup``.

        :param db_subnet_group_description: ``AWS::Neptune::DBSubnetGroup.DBSubnetGroupDescription``.
        :param subnet_ids: ``AWS::Neptune::DBSubnetGroup.SubnetIds``.
        :param db_subnet_group_name: ``AWS::Neptune::DBSubnetGroup.DBSubnetGroupName``.
        :param tags: ``AWS::Neptune::DBSubnetGroup.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbsubnetgroup.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "db_subnet_group_description": db_subnet_group_description,
            "subnet_ids": subnet_ids,
        }
        if db_subnet_group_name is not None:
            self._values["db_subnet_group_name"] = db_subnet_group_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def db_subnet_group_description(self) -> builtins.str:
        '''``AWS::Neptune::DBSubnetGroup.DBSubnetGroupDescription``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbsubnetgroup.html#cfn-neptune-dbsubnetgroup-dbsubnetgroupdescription
        '''
        result = self._values.get("db_subnet_group_description")
        assert result is not None, "Required property 'db_subnet_group_description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''``AWS::Neptune::DBSubnetGroup.SubnetIds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbsubnetgroup.html#cfn-neptune-dbsubnetgroup-subnetids
        '''
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def db_subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::Neptune::DBSubnetGroup.DBSubnetGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbsubnetgroup.html#cfn-neptune-dbsubnetgroup-dbsubnetgroupname
        '''
        result = self._values.get("db_subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::Neptune::DBSubnetGroup.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-neptune-dbsubnetgroup.html#cfn-neptune-dbsubnetgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBSubnetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_neptune.ClusterParameterGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "parameters": "parameters",
        "cluster_parameter_group_name": "clusterParameterGroupName",
        "description": "description",
    },
)
class ClusterParameterGroupProps:
    def __init__(
        self,
        *,
        parameters: typing.Mapping[builtins.str, builtins.str],
        cluster_parameter_group_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Marker class for cluster parameter group.

        :param parameters: (experimental) The parameters in this parameter group.
        :param cluster_parameter_group_name: (experimental) The name of the parameter group. Default: A CDK generated name for the parameter group
        :param description: (experimental) Description for this parameter group. Default: a CDK generated description

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "parameters": parameters,
        }
        if cluster_parameter_group_name is not None:
            self._values["cluster_parameter_group_name"] = cluster_parameter_group_name
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) The parameters in this parameter group.

        :stability: experimental
        '''
        result = self._values.get("parameters")
        assert result is not None, "Required property 'parameters' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def cluster_parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the parameter group.

        :default: A CDK generated name for the parameter group

        :stability: experimental
        '''
        result = self._values.get("cluster_parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description for this parameter group.

        :default: a CDK generated description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterParameterGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_neptune.DatabaseClusterAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_endpoint_address": "clusterEndpointAddress",
        "cluster_identifier": "clusterIdentifier",
        "cluster_resource_identifier": "clusterResourceIdentifier",
        "port": "port",
        "reader_endpoint_address": "readerEndpointAddress",
        "security_group": "securityGroup",
    },
)
class DatabaseClusterAttributes:
    def __init__(
        self,
        *,
        cluster_endpoint_address: builtins.str,
        cluster_identifier: builtins.str,
        cluster_resource_identifier: builtins.str,
        port: jsii.Number,
        reader_endpoint_address: builtins.str,
        security_group: _ISecurityGroup_cdbba9d3,
    ) -> None:
        '''(experimental) Properties that describe an existing cluster instance.

        :param cluster_endpoint_address: (experimental) Cluster endpoint address.
        :param cluster_identifier: (experimental) Identifier for the cluster.
        :param cluster_resource_identifier: (experimental) Resource Identifier for the cluster.
        :param port: (experimental) The database port.
        :param reader_endpoint_address: (experimental) Reader endpoint address.
        :param security_group: (experimental) The security group of the database cluster.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cluster_endpoint_address": cluster_endpoint_address,
            "cluster_identifier": cluster_identifier,
            "cluster_resource_identifier": cluster_resource_identifier,
            "port": port,
            "reader_endpoint_address": reader_endpoint_address,
            "security_group": security_group,
        }

    @builtins.property
    def cluster_endpoint_address(self) -> builtins.str:
        '''(experimental) Cluster endpoint address.

        :stability: experimental
        '''
        result = self._values.get("cluster_endpoint_address")
        assert result is not None, "Required property 'cluster_endpoint_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_identifier(self) -> builtins.str:
        '''(experimental) Identifier for the cluster.

        :stability: experimental
        '''
        result = self._values.get("cluster_identifier")
        assert result is not None, "Required property 'cluster_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_resource_identifier(self) -> builtins.str:
        '''(experimental) Resource Identifier for the cluster.

        :stability: experimental
        '''
        result = self._values.get("cluster_resource_identifier")
        assert result is not None, "Required property 'cluster_resource_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''(experimental) The database port.

        :stability: experimental
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def reader_endpoint_address(self) -> builtins.str:
        '''(experimental) Reader endpoint address.

        :stability: experimental
        '''
        result = self._values.get("reader_endpoint_address")
        assert result is not None, "Required property 'reader_endpoint_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group(self) -> _ISecurityGroup_cdbba9d3:
        '''(experimental) The security group of the database cluster.

        :stability: experimental
        '''
        result = self._values.get("security_group")
        assert result is not None, "Required property 'security_group' is missing"
        return typing.cast(_ISecurityGroup_cdbba9d3, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseClusterAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_neptune.DatabaseClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "vpc": "vpc",
        "associated_roles": "associatedRoles",
        "backup_retention": "backupRetention",
        "cluster_parameter_group": "clusterParameterGroup",
        "db_cluster_name": "dbClusterName",
        "deletion_protection": "deletionProtection",
        "engine_version": "engineVersion",
        "iam_authentication": "iamAuthentication",
        "instance_identifier_base": "instanceIdentifierBase",
        "instances": "instances",
        "kms_key": "kmsKey",
        "parameter_group": "parameterGroup",
        "port": "port",
        "preferred_backup_window": "preferredBackupWindow",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "removal_policy": "removalPolicy",
        "security_groups": "securityGroups",
        "storage_encrypted": "storageEncrypted",
        "subnet_group": "subnetGroup",
        "vpc_subnets": "vpcSubnets",
    },
)
class DatabaseClusterProps:
    def __init__(
        self,
        *,
        instance_type: "InstanceType",
        vpc: _IVpc_6d1f76c4,
        associated_roles: typing.Optional[typing.List[_IRole_59af6f50]] = None,
        backup_retention: typing.Optional[_Duration_070aa057] = None,
        cluster_parameter_group: typing.Optional["IClusterParameterGroup"] = None,
        db_cluster_name: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[builtins.bool] = None,
        engine_version: typing.Optional["EngineVersion"] = None,
        iam_authentication: typing.Optional[builtins.bool] = None,
        instance_identifier_base: typing.Optional[builtins.str] = None,
        instances: typing.Optional[jsii.Number] = None,
        kms_key: typing.Optional[_IKey_36930160] = None,
        parameter_group: typing.Optional["IParameterGroup"] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]] = None,
        storage_encrypted: typing.Optional[builtins.bool] = None,
        subnet_group: typing.Optional["ISubnetGroup"] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_1284e62c] = None,
    ) -> None:
        '''(experimental) Properties for a new database cluster.

        :param instance_type: (experimental) What type of instance to start for the replicas.
        :param vpc: (experimental) What subnets to run the Neptune instances in. Must be at least 2 subnets in two different AZs.
        :param associated_roles: (experimental) A list of AWS Identity and Access Management (IAM) role that can be used by the cluster to access other AWS services. Default: - No role is attached to the cluster.
        :param backup_retention: (experimental) How many days to retain the backup. Default: - cdk.Duration.days(1)
        :param cluster_parameter_group: (experimental) Additional parameters to pass to the database engine. Default: - No parameter group.
        :param db_cluster_name: (experimental) An optional identifier for the cluster. Default: - A name is automatically generated.
        :param deletion_protection: (experimental) Indicates whether the DB cluster should have deletion protection enabled. Default: - true if ``removalPolicy`` is RETAIN, false otherwise
        :param engine_version: (experimental) What version of the database to start. Default: - The default engine version.
        :param iam_authentication: (experimental) Map AWS Identity and Access Management (IAM) accounts to database accounts. Default: - ``false``
        :param instance_identifier_base: (experimental) Base identifier for instances. Every replica is named by appending the replica number to this string, 1-based. Default: - ``dbClusterName`` is used with the word "Instance" appended. If ``dbClusterName`` is not provided, the identifier is automatically generated.
        :param instances: (experimental) Number of Neptune compute instances. Default: 1
        :param kms_key: (experimental) The KMS key for storage encryption. Default: - default master key.
        :param parameter_group: (experimental) The DB parameter group to associate with the instance. Default: no parameter group
        :param port: (experimental) The port the Neptune cluster will listen on. Default: - The default engine port
        :param preferred_backup_window: (experimental) A daily time range in 24-hours UTC format in which backups preferably execute. Must be at least 30 minutes long. Example: '01:00-02:00' Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region. To see the time blocks available, see
        :param preferred_maintenance_window: (experimental) A weekly time range in which maintenance should preferably execute. Must be at least 30 minutes long. Example: 'tue:04:17-tue:04:47' Default: - 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week.
        :param removal_policy: (experimental) The removal policy to apply when the cluster and its instances are removed or replaced during a stack update, or when the stack is deleted. This removal policy also applies to the implicit security group created for the cluster if one is not supplied as a parameter. Default: - Retain cluster.
        :param security_groups: (experimental) Security group. Default: a new security group is created.
        :param storage_encrypted: (experimental) Whether to enable storage encryption. Default: true
        :param subnet_group: (experimental) Existing subnet group for the cluster. Default: - a new subnet group will be created.
        :param vpc_subnets: (experimental) Where to place the instances within the VPC. Default: private subnets

        :stability: experimental
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_1284e62c(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "instance_type": instance_type,
            "vpc": vpc,
        }
        if associated_roles is not None:
            self._values["associated_roles"] = associated_roles
        if backup_retention is not None:
            self._values["backup_retention"] = backup_retention
        if cluster_parameter_group is not None:
            self._values["cluster_parameter_group"] = cluster_parameter_group
        if db_cluster_name is not None:
            self._values["db_cluster_name"] = db_cluster_name
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if iam_authentication is not None:
            self._values["iam_authentication"] = iam_authentication
        if instance_identifier_base is not None:
            self._values["instance_identifier_base"] = instance_identifier_base
        if instances is not None:
            self._values["instances"] = instances
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if parameter_group is not None:
            self._values["parameter_group"] = parameter_group
        if port is not None:
            self._values["port"] = port
        if preferred_backup_window is not None:
            self._values["preferred_backup_window"] = preferred_backup_window
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if storage_encrypted is not None:
            self._values["storage_encrypted"] = storage_encrypted
        if subnet_group is not None:
            self._values["subnet_group"] = subnet_group
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def instance_type(self) -> "InstanceType":
        '''(experimental) What type of instance to start for the replicas.

        :stability: experimental
        '''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast("InstanceType", result)

    @builtins.property
    def vpc(self) -> _IVpc_6d1f76c4:
        '''(experimental) What subnets to run the Neptune instances in.

        Must be at least 2 subnets in two different AZs.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_IVpc_6d1f76c4, result)

    @builtins.property
    def associated_roles(self) -> typing.Optional[typing.List[_IRole_59af6f50]]:
        '''(experimental) A list of AWS Identity and Access Management (IAM) role that can be used by the cluster to access other AWS services.

        :default: - No role is attached to the cluster.

        :stability: experimental
        '''
        result = self._values.get("associated_roles")
        return typing.cast(typing.Optional[typing.List[_IRole_59af6f50]], result)

    @builtins.property
    def backup_retention(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) How many days to retain the backup.

        :default: - cdk.Duration.days(1)

        :stability: experimental
        '''
        result = self._values.get("backup_retention")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def cluster_parameter_group(self) -> typing.Optional["IClusterParameterGroup"]:
        '''(experimental) Additional parameters to pass to the database engine.

        :default: - No parameter group.

        :stability: experimental
        '''
        result = self._values.get("cluster_parameter_group")
        return typing.cast(typing.Optional["IClusterParameterGroup"], result)

    @builtins.property
    def db_cluster_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) An optional identifier for the cluster.

        :default: - A name is automatically generated.

        :stability: experimental
        '''
        result = self._values.get("db_cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deletion_protection(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the DB cluster should have deletion protection enabled.

        :default: - true if ``removalPolicy`` is RETAIN, false otherwise

        :stability: experimental
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def engine_version(self) -> typing.Optional["EngineVersion"]:
        '''(experimental) What version of the database to start.

        :default: - The default engine version.

        :stability: experimental
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional["EngineVersion"], result)

    @builtins.property
    def iam_authentication(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Map AWS Identity and Access Management (IAM) accounts to database accounts.

        :default: - ``false``

        :stability: experimental
        '''
        result = self._values.get("iam_authentication")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def instance_identifier_base(self) -> typing.Optional[builtins.str]:
        '''(experimental) Base identifier for instances.

        Every replica is named by appending the replica number to this string, 1-based.

        :default:

        - ``dbClusterName`` is used with the word "Instance" appended. If ``dbClusterName`` is not provided, the
        identifier is automatically generated.

        :stability: experimental
        '''
        result = self._values.get("instance_identifier_base")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instances(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Number of Neptune compute instances.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("instances")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) The KMS key for storage encryption.

        :default: - default master key.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def parameter_group(self) -> typing.Optional["IParameterGroup"]:
        '''(experimental) The DB parameter group to associate with the instance.

        :default: no parameter group

        :stability: experimental
        '''
        result = self._values.get("parameter_group")
        return typing.cast(typing.Optional["IParameterGroup"], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The port the Neptune cluster will listen on.

        :default: - The default engine port

        :stability: experimental
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preferred_backup_window(self) -> typing.Optional[builtins.str]:
        '''(experimental) A daily time range in 24-hours UTC format in which backups preferably execute.

        Must be at least 30 minutes long.

        Example: '01:00-02:00'

        :default:

        - a 30-minute window selected at random from an 8-hour block of
        time for each AWS Region. To see the time blocks available, see

        :stability: experimental
        '''
        result = self._values.get("preferred_backup_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''(experimental) A weekly time range in which maintenance should preferably execute.

        Must be at least 30 minutes long.

        Example: 'tue:04:17-tue:04:47'

        :default:

        - 30-minute window selected at random from an 8-hour block of time for
        each AWS Region, occurring on a random day of the week.

        :stability: experimental
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        '''(experimental) The removal policy to apply when the cluster and its instances are removed or replaced during a stack update, or when the stack is deleted.

        This
        removal policy also applies to the implicit security group created for the
        cluster if one is not supplied as a parameter.

        :default: - Retain cluster.

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_RemovalPolicy_c97e7a20], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]]:
        '''(experimental) Security group.

        :default: a new security group is created.

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]], result)

    @builtins.property
    def storage_encrypted(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable storage encryption.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("storage_encrypted")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def subnet_group(self) -> typing.Optional["ISubnetGroup"]:
        '''(experimental) Existing subnet group for the cluster.

        :default: - a new subnet group will be created.

        :stability: experimental
        '''
        result = self._values.get("subnet_group")
        return typing.cast(typing.Optional["ISubnetGroup"], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) Where to place the instances within the VPC.

        :default: private subnets

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_neptune.DatabaseInstanceAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "instance_endpoint_address": "instanceEndpointAddress",
        "instance_identifier": "instanceIdentifier",
        "port": "port",
    },
)
class DatabaseInstanceAttributes:
    def __init__(
        self,
        *,
        instance_endpoint_address: builtins.str,
        instance_identifier: builtins.str,
        port: jsii.Number,
    ) -> None:
        '''(experimental) Properties that describe an existing instance.

        :param instance_endpoint_address: (experimental) The endpoint address.
        :param instance_identifier: (experimental) The instance identifier.
        :param port: (experimental) The database port.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "instance_endpoint_address": instance_endpoint_address,
            "instance_identifier": instance_identifier,
            "port": port,
        }

    @builtins.property
    def instance_endpoint_address(self) -> builtins.str:
        '''(experimental) The endpoint address.

        :stability: experimental
        '''
        result = self._values.get("instance_endpoint_address")
        assert result is not None, "Required property 'instance_endpoint_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_identifier(self) -> builtins.str:
        '''(experimental) The instance identifier.

        :stability: experimental
        '''
        result = self._values.get("instance_identifier")
        assert result is not None, "Required property 'instance_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def port(self) -> jsii.Number:
        '''(experimental) The database port.

        :stability: experimental
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseInstanceAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_neptune.DatabaseInstanceProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "instance_type": "instanceType",
        "availability_zone": "availabilityZone",
        "db_instance_name": "dbInstanceName",
        "parameter_group": "parameterGroup",
        "removal_policy": "removalPolicy",
    },
)
class DatabaseInstanceProps:
    def __init__(
        self,
        *,
        cluster: "IDatabaseCluster",
        instance_type: "InstanceType",
        availability_zone: typing.Optional[builtins.str] = None,
        db_instance_name: typing.Optional[builtins.str] = None,
        parameter_group: typing.Optional["IParameterGroup"] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    ) -> None:
        '''(experimental) Construction properties for a DatabaseInstanceNew.

        :param cluster: (experimental) The Neptune database cluster the instance should launch into.
        :param instance_type: (experimental) What type of instance to start for the replicas.
        :param availability_zone: (experimental) The name of the Availability Zone where the DB instance will be located. Default: - no preference
        :param db_instance_name: (experimental) A name for the DB instance. If you specify a name, AWS CloudFormation converts it to lowercase. Default: - a CloudFormation generated name
        :param parameter_group: (experimental) The DB parameter group to associate with the instance. Default: no parameter group
        :param removal_policy: (experimental) The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update. Default: RemovalPolicy.Retain

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
            "instance_type": instance_type,
        }
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if db_instance_name is not None:
            self._values["db_instance_name"] = db_instance_name
        if parameter_group is not None:
            self._values["parameter_group"] = parameter_group
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def cluster(self) -> "IDatabaseCluster":
        '''(experimental) The Neptune database cluster the instance should launch into.

        :stability: experimental
        '''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast("IDatabaseCluster", result)

    @builtins.property
    def instance_type(self) -> "InstanceType":
        '''(experimental) What type of instance to start for the replicas.

        :stability: experimental
        '''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast("InstanceType", result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the Availability Zone where the DB instance will be located.

        :default: - no preference

        :stability: experimental
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def db_instance_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the DB instance.

        If you specify a name, AWS CloudFormation
        converts it to lowercase.

        :default: - a CloudFormation generated name

        :stability: experimental
        '''
        result = self._values.get("db_instance_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_group(self) -> typing.Optional["IParameterGroup"]:
        '''(experimental) The DB parameter group to associate with the instance.

        :default: no parameter group

        :stability: experimental
        '''
        result = self._values.get("parameter_group")
        return typing.cast(typing.Optional["IParameterGroup"], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        '''(experimental) The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update.

        :default: RemovalPolicy.Retain

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_RemovalPolicy_c97e7a20], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Endpoint(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_neptune.Endpoint"):
    '''(experimental) Connection endpoint of a neptune cluster or instance.

    Consists of a combination of hostname and port.

    :stability: experimental
    '''

    def __init__(self, address: builtins.str, port: jsii.Number) -> None:
        '''
        :param address: -
        :param port: -

        :stability: experimental
        '''
        jsii.create(Endpoint, self, [address, port])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        '''(experimental) The hostname of the endpoint.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        '''(experimental) The port of the endpoint.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="socketAddress")
    def socket_address(self) -> builtins.str:
        '''(experimental) The combination of "HOSTNAME:PORT" for this endpoint.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "socketAddress"))


class EngineVersion(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_neptune.EngineVersion",
):
    '''(experimental) Possible Instances Types to use in Neptune cluster used for defining {@link DatabaseClusterProps.engineVersion}.

    :stability: experimental
    '''

    def __init__(self, version: builtins.str) -> None:
        '''(experimental) Constructor for specifying a custom engine version.

        :param version: the engine version of Neptune.

        :stability: experimental
        '''
        jsii.create(EngineVersion, self, [version])

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V1_0_1_0")
    def V1_0_1_0(cls) -> "EngineVersion":
        '''(experimental) Neptune engine version 1.0.1.0.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "V1_0_1_0"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V1_0_1_1")
    def V1_0_1_1(cls) -> "EngineVersion":
        '''(experimental) Neptune engine version 1.0.1.1.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "V1_0_1_1"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V1_0_1_2")
    def V1_0_1_2(cls) -> "EngineVersion":
        '''(experimental) Neptune engine version 1.0.1.2.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "V1_0_1_2"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V1_0_2_1")
    def V1_0_2_1(cls) -> "EngineVersion":
        '''(experimental) Neptune engine version 1.0.2.1.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "V1_0_2_1"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V1_0_2_2")
    def V1_0_2_2(cls) -> "EngineVersion":
        '''(experimental) Neptune engine version 1.0.2.2.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "V1_0_2_2"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V1_0_3_0")
    def V1_0_3_0(cls) -> "EngineVersion":
        '''(experimental) Neptune engine version 1.0.3.0.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "V1_0_3_0"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V1_0_4_0")
    def V1_0_4_0(cls) -> "EngineVersion":
        '''(experimental) Neptune engine version 1.0.4.0.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "V1_0_4_0"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="V1_0_4_1")
    def V1_0_4_1(cls) -> "EngineVersion":
        '''(experimental) Neptune engine version 1.0.4.1.

        :stability: experimental
        '''
        return typing.cast("EngineVersion", jsii.sget(cls, "V1_0_4_1"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''(experimental) the engine version of Neptune.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))


@jsii.interface(jsii_type="monocdk.aws_neptune.IClusterParameterGroup")
class IClusterParameterGroup(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) A parameter group.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IClusterParameterGroupProxy"]:
        return _IClusterParameterGroupProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterParameterGroupName")
    def cluster_parameter_group_name(self) -> builtins.str:
        '''(experimental) The name of this parameter group.

        :stability: experimental
        '''
        ...


class _IClusterParameterGroupProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''(experimental) A parameter group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_neptune.IClusterParameterGroup"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterParameterGroupName")
    def cluster_parameter_group_name(self) -> builtins.str:
        '''(experimental) The name of this parameter group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterParameterGroupName"))


@jsii.interface(jsii_type="monocdk.aws_neptune.IDatabaseCluster")
class IDatabaseCluster(
    _IResource_8c1dbbbd,
    _IConnectable_c1c0e72c,
    typing_extensions.Protocol,
):
    '''(experimental) Create a clustered database with a given number of instances.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IDatabaseClusterProxy"]:
        return _IDatabaseClusterProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> Endpoint:
        '''(experimental) The endpoint to use for read/write operations.

        :stability: experimental
        :attribute: Endpoint,Port
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> builtins.str:
        '''(experimental) Identifier of the cluster.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterReadEndpoint")
    def cluster_read_endpoint(self) -> Endpoint:
        '''(experimental) Endpoint to use for load-balanced read-only operations.

        :stability: experimental
        :attribute: ReadEndpoint
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterResourceIdentifier")
    def cluster_resource_identifier(self) -> builtins.str:
        '''(experimental) Resource identifier of the cluster.

        :stability: experimental
        :attribute: ClusterResourceId
        '''
        ...

    @jsii.member(jsii_name="grantConnect")
    def grant_connect(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity connection access to the database.

        :param grantee: -

        :stability: experimental
        '''
        ...


class _IDatabaseClusterProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
    jsii.proxy_for(_IConnectable_c1c0e72c), # type: ignore[misc]
):
    '''(experimental) Create a clustered database with a given number of instances.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_neptune.IDatabaseCluster"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> Endpoint:
        '''(experimental) The endpoint to use for read/write operations.

        :stability: experimental
        :attribute: Endpoint,Port
        '''
        return typing.cast(Endpoint, jsii.get(self, "clusterEndpoint"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> builtins.str:
        '''(experimental) Identifier of the cluster.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterIdentifier"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterReadEndpoint")
    def cluster_read_endpoint(self) -> Endpoint:
        '''(experimental) Endpoint to use for load-balanced read-only operations.

        :stability: experimental
        :attribute: ReadEndpoint
        '''
        return typing.cast(Endpoint, jsii.get(self, "clusterReadEndpoint"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterResourceIdentifier")
    def cluster_resource_identifier(self) -> builtins.str:
        '''(experimental) Resource identifier of the cluster.

        :stability: experimental
        :attribute: ClusterResourceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterResourceIdentifier"))

    @jsii.member(jsii_name="grantConnect")
    def grant_connect(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity connection access to the database.

        :param grantee: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantConnect", [grantee]))


@jsii.interface(jsii_type="monocdk.aws_neptune.IDatabaseInstance")
class IDatabaseInstance(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) A database instance.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IDatabaseInstanceProxy"]:
        return _IDatabaseInstanceProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dbInstanceEndpointAddress")
    def db_instance_endpoint_address(self) -> builtins.str:
        '''(experimental) The instance endpoint address.

        :stability: experimental
        :attribute: Endpoint
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dbInstanceEndpointPort")
    def db_instance_endpoint_port(self) -> builtins.str:
        '''(experimental) The instance endpoint port.

        :stability: experimental
        :attribute: Port
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="instanceEndpoint")
    def instance_endpoint(self) -> Endpoint:
        '''(experimental) The instance endpoint.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="instanceIdentifier")
    def instance_identifier(self) -> builtins.str:
        '''(experimental) The instance identifier.

        :stability: experimental
        '''
        ...


class _IDatabaseInstanceProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''(experimental) A database instance.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_neptune.IDatabaseInstance"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dbInstanceEndpointAddress")
    def db_instance_endpoint_address(self) -> builtins.str:
        '''(experimental) The instance endpoint address.

        :stability: experimental
        :attribute: Endpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "dbInstanceEndpointAddress"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dbInstanceEndpointPort")
    def db_instance_endpoint_port(self) -> builtins.str:
        '''(experimental) The instance endpoint port.

        :stability: experimental
        :attribute: Port
        '''
        return typing.cast(builtins.str, jsii.get(self, "dbInstanceEndpointPort"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="instanceEndpoint")
    def instance_endpoint(self) -> Endpoint:
        '''(experimental) The instance endpoint.

        :stability: experimental
        '''
        return typing.cast(Endpoint, jsii.get(self, "instanceEndpoint"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="instanceIdentifier")
    def instance_identifier(self) -> builtins.str:
        '''(experimental) The instance identifier.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceIdentifier"))


@jsii.interface(jsii_type="monocdk.aws_neptune.IParameterGroup")
class IParameterGroup(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) A parameter group.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IParameterGroupProxy"]:
        return _IParameterGroupProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> builtins.str:
        '''(experimental) The name of this parameter group.

        :stability: experimental
        '''
        ...


class _IParameterGroupProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''(experimental) A parameter group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_neptune.IParameterGroup"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> builtins.str:
        '''(experimental) The name of this parameter group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "parameterGroupName"))


@jsii.interface(jsii_type="monocdk.aws_neptune.ISubnetGroup")
class ISubnetGroup(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Interface for a subnet group.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_ISubnetGroupProxy"]:
        return _ISubnetGroupProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subnetGroupName")
    def subnet_group_name(self) -> builtins.str:
        '''(experimental) The name of the subnet group.

        :stability: experimental
        :attribute: true
        '''
        ...


class _ISubnetGroupProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''(experimental) Interface for a subnet group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_neptune.ISubnetGroup"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subnetGroupName")
    def subnet_group_name(self) -> builtins.str:
        '''(experimental) The name of the subnet group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "subnetGroupName"))


@jsii.enum(jsii_type="monocdk.aws_neptune.InstanceType")
class InstanceType(enum.Enum):
    '''(experimental) Possible Instances Types to use in Neptune cluster used for defining {@link DatabaseInstanceProps.instanceType}.

    :stability: experimental
    '''

    R5_LARGE = "R5_LARGE"
    '''(experimental) db.r5.large.

    :stability: experimental
    '''
    R5_XLARGE = "R5_XLARGE"
    '''(experimental) db.r5.xlarge.

    :stability: experimental
    '''
    R5_2XLARGE = "R5_2XLARGE"
    '''(experimental) db.r5.2xlarge.

    :stability: experimental
    '''
    R5_4XLARGE = "R5_4XLARGE"
    '''(experimental) db.r5.4xlarge.

    :stability: experimental
    '''
    R5_8XLARGE = "R5_8XLARGE"
    '''(experimental) db.r5.8xlarge.

    :stability: experimental
    '''
    R5_12XLARGE = "R5_12XLARGE"
    '''(experimental) db.r5.12xlarge.

    :stability: experimental
    '''
    R5_24XLARGE = "R5_24XLARGE"
    '''(experimental) db.r5.24xlarge.

    :stability: experimental
    '''
    R4_LARGE = "R4_LARGE"
    '''(experimental) db.r4.large.

    :stability: experimental
    '''
    R4_XLARGE = "R4_XLARGE"
    '''(experimental) db.r4.xlarge.

    :stability: experimental
    '''
    R4_2XLARGE = "R4_2XLARGE"
    '''(experimental) db.r4.2xlarge.

    :stability: experimental
    '''
    R4_4XLARGE = "R4_4XLARGE"
    '''(experimental) db.r4.4xlarge.

    :stability: experimental
    '''
    R4_8XLARGE = "R4_8XLARGE"
    '''(experimental) db.r4.8xlarge.

    :stability: experimental
    '''
    T3_MEDIUM = "T3_MEDIUM"
    '''(experimental) db.t3.medium.

    :stability: experimental
    '''


@jsii.implements(IParameterGroup)
class ParameterGroup(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_neptune.ParameterGroup",
):
    '''(experimental) DB parameter group.

    :stability: experimental
    :resource: AWS::Neptune::DBParameterGroup
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        parameters: typing.Mapping[builtins.str, builtins.str],
        description: typing.Optional[builtins.str] = None,
        parameter_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param parameters: (experimental) The parameters in this parameter group.
        :param description: (experimental) Description for this parameter group. Default: a CDK generated description
        :param parameter_group_name: (experimental) The name of the parameter group. Default: A CDK generated name for the parameter group

        :stability: experimental
        '''
        props = ParameterGroupProps(
            parameters=parameters,
            description=description,
            parameter_group_name=parameter_group_name,
        )

        jsii.create(ParameterGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromParameterGroupName") # type: ignore[misc]
    @builtins.classmethod
    def from_parameter_group_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        parameter_group_name: builtins.str,
    ) -> IParameterGroup:
        '''(experimental) Imports a parameter group.

        :param scope: -
        :param id: -
        :param parameter_group_name: -

        :stability: experimental
        '''
        return typing.cast(IParameterGroup, jsii.sinvoke(cls, "fromParameterGroupName", [scope, id, parameter_group_name]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> builtins.str:
        '''(experimental) The name of the parameter group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "parameterGroupName"))


@jsii.data_type(
    jsii_type="monocdk.aws_neptune.ParameterGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "parameters": "parameters",
        "description": "description",
        "parameter_group_name": "parameterGroupName",
    },
)
class ParameterGroupProps:
    def __init__(
        self,
        *,
        parameters: typing.Mapping[builtins.str, builtins.str],
        description: typing.Optional[builtins.str] = None,
        parameter_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Marker class for cluster parameter group.

        :param parameters: (experimental) The parameters in this parameter group.
        :param description: (experimental) Description for this parameter group. Default: a CDK generated description
        :param parameter_group_name: (experimental) The name of the parameter group. Default: A CDK generated name for the parameter group

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "parameters": parameters,
        }
        if description is not None:
            self._values["description"] = description
        if parameter_group_name is not None:
            self._values["parameter_group_name"] = parameter_group_name

    @builtins.property
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) The parameters in this parameter group.

        :stability: experimental
        '''
        result = self._values.get("parameters")
        assert result is not None, "Required property 'parameters' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description for this parameter group.

        :default: a CDK generated description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the parameter group.

        :default: A CDK generated name for the parameter group

        :stability: experimental
        '''
        result = self._values.get("parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ParameterGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISubnetGroup)
class SubnetGroup(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_neptune.SubnetGroup",
):
    '''(experimental) Class for creating a RDS DB subnet group.

    :stability: experimental
    :resource: AWS::Neptune::DBSubnetGroup
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        vpc: _IVpc_6d1f76c4,
        description: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        subnet_group_name: typing.Optional[builtins.str] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_1284e62c] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc: (experimental) The VPC to place the subnet group in.
        :param description: (experimental) Description of the subnet group. Default: - a name is generated
        :param removal_policy: (experimental) The removal policy to apply when the subnet group are removed from the stack or replaced during an update. Default: RemovalPolicy.DESTROY
        :param subnet_group_name: (experimental) The name of the subnet group. Default: - a name is generated
        :param vpc_subnets: (experimental) Which subnets within the VPC to associate with this group. Default: - private subnets

        :stability: experimental
        '''
        props = SubnetGroupProps(
            vpc=vpc,
            description=description,
            removal_policy=removal_policy,
            subnet_group_name=subnet_group_name,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(SubnetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromSubnetGroupName") # type: ignore[misc]
    @builtins.classmethod
    def from_subnet_group_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        subnet_group_name: builtins.str,
    ) -> ISubnetGroup:
        '''(experimental) Imports an existing subnet group by name.

        :param scope: -
        :param id: -
        :param subnet_group_name: -

        :stability: experimental
        '''
        return typing.cast(ISubnetGroup, jsii.sinvoke(cls, "fromSubnetGroupName", [scope, id, subnet_group_name]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subnetGroupName")
    def subnet_group_name(self) -> builtins.str:
        '''(experimental) The name of the subnet group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "subnetGroupName"))


@jsii.data_type(
    jsii_type="monocdk.aws_neptune.SubnetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "description": "description",
        "removal_policy": "removalPolicy",
        "subnet_group_name": "subnetGroupName",
        "vpc_subnets": "vpcSubnets",
    },
)
class SubnetGroupProps:
    def __init__(
        self,
        *,
        vpc: _IVpc_6d1f76c4,
        description: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        subnet_group_name: typing.Optional[builtins.str] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_1284e62c] = None,
    ) -> None:
        '''(experimental) Properties for creating a SubnetGroup.

        :param vpc: (experimental) The VPC to place the subnet group in.
        :param description: (experimental) Description of the subnet group. Default: - a name is generated
        :param removal_policy: (experimental) The removal policy to apply when the subnet group are removed from the stack or replaced during an update. Default: RemovalPolicy.DESTROY
        :param subnet_group_name: (experimental) The name of the subnet group. Default: - a name is generated
        :param vpc_subnets: (experimental) Which subnets within the VPC to associate with this group. Default: - private subnets

        :stability: experimental
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_1284e62c(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }
        if description is not None:
            self._values["description"] = description
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if subnet_group_name is not None:
            self._values["subnet_group_name"] = subnet_group_name
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> _IVpc_6d1f76c4:
        '''(experimental) The VPC to place the subnet group in.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_IVpc_6d1f76c4, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of the subnet group.

        :default: - a name is generated

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        '''(experimental) The removal policy to apply when the subnet group are removed from the stack or replaced during an update.

        :default: RemovalPolicy.DESTROY

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_RemovalPolicy_c97e7a20], result)

    @builtins.property
    def subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the subnet group.

        :default: - a name is generated

        :stability: experimental
        '''
        result = self._values.get("subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) Which subnets within the VPC to associate with this group.

        :default: - private subnets

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubnetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IClusterParameterGroup)
class ClusterParameterGroup(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_neptune.ClusterParameterGroup",
):
    '''(experimental) A cluster parameter group.

    :stability: experimental
    :resource: AWS::Neptune::DBClusterParameterGroup
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        parameters: typing.Mapping[builtins.str, builtins.str],
        cluster_parameter_group_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param parameters: (experimental) The parameters in this parameter group.
        :param cluster_parameter_group_name: (experimental) The name of the parameter group. Default: A CDK generated name for the parameter group
        :param description: (experimental) Description for this parameter group. Default: a CDK generated description

        :stability: experimental
        '''
        props = ClusterParameterGroupProps(
            parameters=parameters,
            cluster_parameter_group_name=cluster_parameter_group_name,
            description=description,
        )

        jsii.create(ClusterParameterGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromClusterParameterGroupName") # type: ignore[misc]
    @builtins.classmethod
    def from_cluster_parameter_group_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        cluster_parameter_group_name: builtins.str,
    ) -> IClusterParameterGroup:
        '''(experimental) Imports a parameter group.

        :param scope: -
        :param id: -
        :param cluster_parameter_group_name: -

        :stability: experimental
        '''
        return typing.cast(IClusterParameterGroup, jsii.sinvoke(cls, "fromClusterParameterGroupName", [scope, id, cluster_parameter_group_name]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterParameterGroupName")
    def cluster_parameter_group_name(self) -> builtins.str:
        '''(experimental) The name of the parameter group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterParameterGroupName"))


@jsii.implements(IDatabaseCluster)
class DatabaseClusterBase(
    _Resource_abff4495,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_neptune.DatabaseClusterBase",
):
    '''(experimental) A new or imported database cluster.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_DatabaseClusterBaseProxy"]:
        return _DatabaseClusterBaseProxy

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: (experimental) The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param physical_name: (experimental) The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: (experimental) The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to

        :stability: experimental
        '''
        props = _ResourceProps_9b554c0f(
            account=account, physical_name=physical_name, region=region
        )

        jsii.create(DatabaseClusterBase, self, [scope, id, props])

    @jsii.member(jsii_name="fromDatabaseClusterAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_database_cluster_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster_endpoint_address: builtins.str,
        cluster_identifier: builtins.str,
        cluster_resource_identifier: builtins.str,
        port: jsii.Number,
        reader_endpoint_address: builtins.str,
        security_group: _ISecurityGroup_cdbba9d3,
    ) -> IDatabaseCluster:
        '''(experimental) Import an existing DatabaseCluster from properties.

        :param scope: -
        :param id: -
        :param cluster_endpoint_address: (experimental) Cluster endpoint address.
        :param cluster_identifier: (experimental) Identifier for the cluster.
        :param cluster_resource_identifier: (experimental) Resource Identifier for the cluster.
        :param port: (experimental) The database port.
        :param reader_endpoint_address: (experimental) Reader endpoint address.
        :param security_group: (experimental) The security group of the database cluster.

        :stability: experimental
        '''
        attrs = DatabaseClusterAttributes(
            cluster_endpoint_address=cluster_endpoint_address,
            cluster_identifier=cluster_identifier,
            cluster_resource_identifier=cluster_resource_identifier,
            port=port,
            reader_endpoint_address=reader_endpoint_address,
            security_group=security_group,
        )

        return typing.cast(IDatabaseCluster, jsii.sinvoke(cls, "fromDatabaseClusterAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="grantConnect")
    def grant_connect(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity connection access to the database.

        :param grantee: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantConnect", [grantee]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterEndpoint")
    @abc.abstractmethod
    def cluster_endpoint(self) -> Endpoint:
        '''(experimental) The endpoint to use for read/write operations.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterIdentifier")
    @abc.abstractmethod
    def cluster_identifier(self) -> builtins.str:
        '''(experimental) Identifier of the cluster.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterReadEndpoint")
    @abc.abstractmethod
    def cluster_read_endpoint(self) -> Endpoint:
        '''(experimental) Endpoint to use for load-balanced read-only operations.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterResourceIdentifier")
    @abc.abstractmethod
    def cluster_resource_identifier(self) -> builtins.str:
        '''(experimental) Resource identifier of the cluster.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="connections")
    @abc.abstractmethod
    def connections(self) -> _Connections_57ccbda9:
        '''(experimental) The connections object to implement IConnectable.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enableIamAuthentication")
    @abc.abstractmethod
    def _enable_iam_authentication(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        ...

    @_enable_iam_authentication.setter
    @abc.abstractmethod
    def _enable_iam_authentication(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _DatabaseClusterBaseProxy(
    DatabaseClusterBase, jsii.proxy_for(_Resource_abff4495) # type: ignore[misc]
):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> Endpoint:
        '''(experimental) The endpoint to use for read/write operations.

        :stability: experimental
        '''
        return typing.cast(Endpoint, jsii.get(self, "clusterEndpoint"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> builtins.str:
        '''(experimental) Identifier of the cluster.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterIdentifier"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterReadEndpoint")
    def cluster_read_endpoint(self) -> Endpoint:
        '''(experimental) Endpoint to use for load-balanced read-only operations.

        :stability: experimental
        '''
        return typing.cast(Endpoint, jsii.get(self, "clusterReadEndpoint"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterResourceIdentifier")
    def cluster_resource_identifier(self) -> builtins.str:
        '''(experimental) Resource identifier of the cluster.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterResourceIdentifier"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_57ccbda9:
        '''(experimental) The connections object to implement IConnectable.

        :stability: experimental
        '''
        return typing.cast(_Connections_57ccbda9, jsii.get(self, "connections"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enableIamAuthentication")
    def _enable_iam_authentication(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enableIamAuthentication"))

    @_enable_iam_authentication.setter
    def _enable_iam_authentication(self, value: typing.Optional[builtins.bool]) -> None:
        jsii.set(self, "enableIamAuthentication", value)


@jsii.implements(IDatabaseInstance)
class DatabaseInstance(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_neptune.DatabaseInstance",
):
    '''(experimental) A database instance.

    :stability: experimental
    :resource: AWS::Neptune::DBInstance
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster: IDatabaseCluster,
        instance_type: InstanceType,
        availability_zone: typing.Optional[builtins.str] = None,
        db_instance_name: typing.Optional[builtins.str] = None,
        parameter_group: typing.Optional[IParameterGroup] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: (experimental) The Neptune database cluster the instance should launch into.
        :param instance_type: (experimental) What type of instance to start for the replicas.
        :param availability_zone: (experimental) The name of the Availability Zone where the DB instance will be located. Default: - no preference
        :param db_instance_name: (experimental) A name for the DB instance. If you specify a name, AWS CloudFormation converts it to lowercase. Default: - a CloudFormation generated name
        :param parameter_group: (experimental) The DB parameter group to associate with the instance. Default: no parameter group
        :param removal_policy: (experimental) The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update. Default: RemovalPolicy.Retain

        :stability: experimental
        '''
        props = DatabaseInstanceProps(
            cluster=cluster,
            instance_type=instance_type,
            availability_zone=availability_zone,
            db_instance_name=db_instance_name,
            parameter_group=parameter_group,
            removal_policy=removal_policy,
        )

        jsii.create(DatabaseInstance, self, [scope, id, props])

    @jsii.member(jsii_name="fromDatabaseInstanceAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_database_instance_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        instance_endpoint_address: builtins.str,
        instance_identifier: builtins.str,
        port: jsii.Number,
    ) -> IDatabaseInstance:
        '''(experimental) Import an existing database instance.

        :param scope: -
        :param id: -
        :param instance_endpoint_address: (experimental) The endpoint address.
        :param instance_identifier: (experimental) The instance identifier.
        :param port: (experimental) The database port.

        :stability: experimental
        '''
        attrs = DatabaseInstanceAttributes(
            instance_endpoint_address=instance_endpoint_address,
            instance_identifier=instance_identifier,
            port=port,
        )

        return typing.cast(IDatabaseInstance, jsii.sinvoke(cls, "fromDatabaseInstanceAttributes", [scope, id, attrs]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> IDatabaseCluster:
        '''(experimental) The instance's database cluster.

        :stability: experimental
        '''
        return typing.cast(IDatabaseCluster, jsii.get(self, "cluster"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dbInstanceEndpointAddress")
    def db_instance_endpoint_address(self) -> builtins.str:
        '''(experimental) The instance endpoint address.

        :stability: experimental
        :inheritdoc: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "dbInstanceEndpointAddress"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="dbInstanceEndpointPort")
    def db_instance_endpoint_port(self) -> builtins.str:
        '''(experimental) The instance endpoint port.

        :stability: experimental
        :inheritdoc: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "dbInstanceEndpointPort"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="instanceEndpoint")
    def instance_endpoint(self) -> Endpoint:
        '''(experimental) The instance endpoint.

        :stability: experimental
        :inheritdoc: true
        '''
        return typing.cast(Endpoint, jsii.get(self, "instanceEndpoint"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="instanceIdentifier")
    def instance_identifier(self) -> builtins.str:
        '''(experimental) The instance identifier.

        :stability: experimental
        :inheritdoc: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceIdentifier"))


@jsii.implements(IDatabaseCluster)
class DatabaseCluster(
    DatabaseClusterBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_neptune.DatabaseCluster",
):
    '''(experimental) Create a clustered database with a given number of instances.

    :stability: experimental
    :resource: AWS::Neptune::DBCluster
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        instance_type: InstanceType,
        vpc: _IVpc_6d1f76c4,
        associated_roles: typing.Optional[typing.List[_IRole_59af6f50]] = None,
        backup_retention: typing.Optional[_Duration_070aa057] = None,
        cluster_parameter_group: typing.Optional[IClusterParameterGroup] = None,
        db_cluster_name: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[builtins.bool] = None,
        engine_version: typing.Optional[EngineVersion] = None,
        iam_authentication: typing.Optional[builtins.bool] = None,
        instance_identifier_base: typing.Optional[builtins.str] = None,
        instances: typing.Optional[jsii.Number] = None,
        kms_key: typing.Optional[_IKey_36930160] = None,
        parameter_group: typing.Optional[IParameterGroup] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]] = None,
        storage_encrypted: typing.Optional[builtins.bool] = None,
        subnet_group: typing.Optional[ISubnetGroup] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_1284e62c] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param instance_type: (experimental) What type of instance to start for the replicas.
        :param vpc: (experimental) What subnets to run the Neptune instances in. Must be at least 2 subnets in two different AZs.
        :param associated_roles: (experimental) A list of AWS Identity and Access Management (IAM) role that can be used by the cluster to access other AWS services. Default: - No role is attached to the cluster.
        :param backup_retention: (experimental) How many days to retain the backup. Default: - cdk.Duration.days(1)
        :param cluster_parameter_group: (experimental) Additional parameters to pass to the database engine. Default: - No parameter group.
        :param db_cluster_name: (experimental) An optional identifier for the cluster. Default: - A name is automatically generated.
        :param deletion_protection: (experimental) Indicates whether the DB cluster should have deletion protection enabled. Default: - true if ``removalPolicy`` is RETAIN, false otherwise
        :param engine_version: (experimental) What version of the database to start. Default: - The default engine version.
        :param iam_authentication: (experimental) Map AWS Identity and Access Management (IAM) accounts to database accounts. Default: - ``false``
        :param instance_identifier_base: (experimental) Base identifier for instances. Every replica is named by appending the replica number to this string, 1-based. Default: - ``dbClusterName`` is used with the word "Instance" appended. If ``dbClusterName`` is not provided, the identifier is automatically generated.
        :param instances: (experimental) Number of Neptune compute instances. Default: 1
        :param kms_key: (experimental) The KMS key for storage encryption. Default: - default master key.
        :param parameter_group: (experimental) The DB parameter group to associate with the instance. Default: no parameter group
        :param port: (experimental) The port the Neptune cluster will listen on. Default: - The default engine port
        :param preferred_backup_window: (experimental) A daily time range in 24-hours UTC format in which backups preferably execute. Must be at least 30 minutes long. Example: '01:00-02:00' Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region. To see the time blocks available, see
        :param preferred_maintenance_window: (experimental) A weekly time range in which maintenance should preferably execute. Must be at least 30 minutes long. Example: 'tue:04:17-tue:04:47' Default: - 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week.
        :param removal_policy: (experimental) The removal policy to apply when the cluster and its instances are removed or replaced during a stack update, or when the stack is deleted. This removal policy also applies to the implicit security group created for the cluster if one is not supplied as a parameter. Default: - Retain cluster.
        :param security_groups: (experimental) Security group. Default: a new security group is created.
        :param storage_encrypted: (experimental) Whether to enable storage encryption. Default: true
        :param subnet_group: (experimental) Existing subnet group for the cluster. Default: - a new subnet group will be created.
        :param vpc_subnets: (experimental) Where to place the instances within the VPC. Default: private subnets

        :stability: experimental
        '''
        props = DatabaseClusterProps(
            instance_type=instance_type,
            vpc=vpc,
            associated_roles=associated_roles,
            backup_retention=backup_retention,
            cluster_parameter_group=cluster_parameter_group,
            db_cluster_name=db_cluster_name,
            deletion_protection=deletion_protection,
            engine_version=engine_version,
            iam_authentication=iam_authentication,
            instance_identifier_base=instance_identifier_base,
            instances=instances,
            kms_key=kms_key,
            parameter_group=parameter_group,
            port=port,
            preferred_backup_window=preferred_backup_window,
            preferred_maintenance_window=preferred_maintenance_window,
            removal_policy=removal_policy,
            security_groups=security_groups,
            storage_encrypted=storage_encrypted,
            subnet_group=subnet_group,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(DatabaseCluster, self, [scope, id, props])

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="DEFAULT_NUM_INSTANCES")
    def DEFAULT_NUM_INSTANCES(cls) -> jsii.Number:
        '''(experimental) The default number of instances in the Neptune cluster if none are specified.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.sget(cls, "DEFAULT_NUM_INSTANCES"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> Endpoint:
        '''(experimental) The endpoint to use for read/write operations.

        :stability: experimental
        '''
        return typing.cast(Endpoint, jsii.get(self, "clusterEndpoint"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> builtins.str:
        '''(experimental) Identifier of the cluster.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterIdentifier"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterReadEndpoint")
    def cluster_read_endpoint(self) -> Endpoint:
        '''(experimental) Endpoint to use for load-balanced read-only operations.

        :stability: experimental
        '''
        return typing.cast(Endpoint, jsii.get(self, "clusterReadEndpoint"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterResourceIdentifier")
    def cluster_resource_identifier(self) -> builtins.str:
        '''(experimental) The resource id for the cluster;

        for example: cluster-ABCD1234EFGH5678IJKL90MNOP. The cluster ID uniquely
        identifies the cluster and is used in things like IAM authentication policies.

        :stability: experimental
        :attribute: ClusterResourceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterResourceIdentifier"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_57ccbda9:
        '''(experimental) The connections object to implement IConnectable.

        :stability: experimental
        '''
        return typing.cast(_Connections_57ccbda9, jsii.get(self, "connections"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="instanceEndpoints")
    def instance_endpoints(self) -> typing.List[Endpoint]:
        '''(experimental) Endpoints which address each individual instance.

        :stability: experimental
        '''
        return typing.cast(typing.List[Endpoint], jsii.get(self, "instanceEndpoints"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="instanceIdentifiers")
    def instance_identifiers(self) -> typing.List[builtins.str]:
        '''(experimental) Identifiers of the instance.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instanceIdentifiers"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subnetGroup")
    def subnet_group(self) -> ISubnetGroup:
        '''(experimental) Subnet group used by the DB.

        :stability: experimental
        '''
        return typing.cast(ISubnetGroup, jsii.get(self, "subnetGroup"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _IVpc_6d1f76c4:
        '''(experimental) The VPC where the DB subnet group is created.

        :stability: experimental
        '''
        return typing.cast(_IVpc_6d1f76c4, jsii.get(self, "vpc"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpcSubnets")
    def vpc_subnets(self) -> _SubnetSelection_1284e62c:
        '''(experimental) The subnets used by the DB subnet group.

        :stability: experimental
        '''
        return typing.cast(_SubnetSelection_1284e62c, jsii.get(self, "vpcSubnets"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enableIamAuthentication")
    def _enable_iam_authentication(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enableIamAuthentication"))

    @_enable_iam_authentication.setter
    def _enable_iam_authentication(self, value: typing.Optional[builtins.bool]) -> None:
        jsii.set(self, "enableIamAuthentication", value)


__all__ = [
    "CfnDBCluster",
    "CfnDBClusterParameterGroup",
    "CfnDBClusterParameterGroupProps",
    "CfnDBClusterProps",
    "CfnDBInstance",
    "CfnDBInstanceProps",
    "CfnDBParameterGroup",
    "CfnDBParameterGroupProps",
    "CfnDBSubnetGroup",
    "CfnDBSubnetGroupProps",
    "ClusterParameterGroup",
    "ClusterParameterGroupProps",
    "DatabaseCluster",
    "DatabaseClusterAttributes",
    "DatabaseClusterBase",
    "DatabaseClusterProps",
    "DatabaseInstance",
    "DatabaseInstanceAttributes",
    "DatabaseInstanceProps",
    "Endpoint",
    "EngineVersion",
    "IClusterParameterGroup",
    "IDatabaseCluster",
    "IDatabaseInstance",
    "IParameterGroup",
    "ISubnetGroup",
    "InstanceType",
    "ParameterGroup",
    "ParameterGroupProps",
    "SubnetGroup",
    "SubnetGroupProps",
]

publication.publish()
