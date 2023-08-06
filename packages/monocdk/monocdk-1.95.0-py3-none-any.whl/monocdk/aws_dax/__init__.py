'''
# Amazon DynamoDB Accelerator Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.
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

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnCluster(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_dax.CfnCluster",
):
    '''A CloudFormation ``AWS::DAX::Cluster``.

    :cloudformationResource: AWS::DAX::Cluster
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        iam_role_arn: builtins.str,
        node_type: builtins.str,
        replication_factor: jsii.Number,
        availability_zones: typing.Optional[typing.List[builtins.str]] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        notification_topic_arn: typing.Optional[builtins.str] = None,
        parameter_group_name: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
        sse_specification: typing.Optional[typing.Union["CfnCluster.SSESpecificationProperty", _IResolvable_a771d0ef]] = None,
        subnet_group_name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::DAX::Cluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param iam_role_arn: ``AWS::DAX::Cluster.IAMRoleARN``.
        :param node_type: ``AWS::DAX::Cluster.NodeType``.
        :param replication_factor: ``AWS::DAX::Cluster.ReplicationFactor``.
        :param availability_zones: ``AWS::DAX::Cluster.AvailabilityZones``.
        :param cluster_name: ``AWS::DAX::Cluster.ClusterName``.
        :param description: ``AWS::DAX::Cluster.Description``.
        :param notification_topic_arn: ``AWS::DAX::Cluster.NotificationTopicARN``.
        :param parameter_group_name: ``AWS::DAX::Cluster.ParameterGroupName``.
        :param preferred_maintenance_window: ``AWS::DAX::Cluster.PreferredMaintenanceWindow``.
        :param security_group_ids: ``AWS::DAX::Cluster.SecurityGroupIds``.
        :param sse_specification: ``AWS::DAX::Cluster.SSESpecification``.
        :param subnet_group_name: ``AWS::DAX::Cluster.SubnetGroupName``.
        :param tags: ``AWS::DAX::Cluster.Tags``.
        '''
        props = CfnClusterProps(
            iam_role_arn=iam_role_arn,
            node_type=node_type,
            replication_factor=replication_factor,
            availability_zones=availability_zones,
            cluster_name=cluster_name,
            description=description,
            notification_topic_arn=notification_topic_arn,
            parameter_group_name=parameter_group_name,
            preferred_maintenance_window=preferred_maintenance_window,
            security_group_ids=security_group_ids,
            sse_specification=sse_specification,
            subnet_group_name=subnet_group_name,
            tags=tags,
        )

        jsii.create(CfnCluster, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrClusterDiscoveryEndpoint")
    def attr_cluster_discovery_endpoint(self) -> builtins.str:
        '''
        :cloudformationAttribute: ClusterDiscoveryEndpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrClusterDiscoveryEndpoint"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::DAX::Cluster.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="iamRoleArn")
    def iam_role_arn(self) -> builtins.str:
        '''``AWS::DAX::Cluster.IAMRoleARN``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-iamrolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "iamRoleArn"))

    @iam_role_arn.setter
    def iam_role_arn(self, value: builtins.str) -> None:
        jsii.set(self, "iamRoleArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> builtins.str:
        '''``AWS::DAX::Cluster.NodeType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-nodetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: builtins.str) -> None:
        jsii.set(self, "nodeType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="replicationFactor")
    def replication_factor(self) -> jsii.Number:
        '''``AWS::DAX::Cluster.ReplicationFactor``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-replicationfactor
        '''
        return typing.cast(jsii.Number, jsii.get(self, "replicationFactor"))

    @replication_factor.setter
    def replication_factor(self, value: jsii.Number) -> None:
        jsii.set(self, "replicationFactor", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::DAX::Cluster.AvailabilityZones``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-availabilityzones
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "availabilityZones"))

    @availability_zones.setter
    def availability_zones(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "availabilityZones", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::DAX::Cluster.ClusterName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-clustername
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "clusterName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::DAX::Cluster.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="notificationTopicArn")
    def notification_topic_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::DAX::Cluster.NotificationTopicARN``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-notificationtopicarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationTopicArn"))

    @notification_topic_arn.setter
    def notification_topic_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "notificationTopicArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::DAX::Cluster.ParameterGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-parametergroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterGroupName"))

    @parameter_group_name.setter
    def parameter_group_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "parameterGroupName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''``AWS::DAX::Cluster.PreferredMaintenanceWindow``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-preferredmaintenancewindow
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredMaintenanceWindow"))

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::DAX::Cluster.SecurityGroupIds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-securitygroupids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "securityGroupIds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sseSpecification")
    def sse_specification(
        self,
    ) -> typing.Optional[typing.Union["CfnCluster.SSESpecificationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::DAX::Cluster.SSESpecification``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-ssespecification
        '''
        return typing.cast(typing.Optional[typing.Union["CfnCluster.SSESpecificationProperty", _IResolvable_a771d0ef]], jsii.get(self, "sseSpecification"))

    @sse_specification.setter
    def sse_specification(
        self,
        value: typing.Optional[typing.Union["CfnCluster.SSESpecificationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "sseSpecification", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subnetGroupName")
    def subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::DAX::Cluster.SubnetGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-subnetgroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetGroupName"))

    @subnet_group_name.setter
    def subnet_group_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "subnetGroupName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_dax.CfnCluster.SSESpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"sse_enabled": "sseEnabled"},
    )
    class SSESpecificationProperty:
        def __init__(
            self,
            *,
            sse_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param sse_enabled: ``CfnCluster.SSESpecificationProperty.SSEEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dax-cluster-ssespecification.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if sse_enabled is not None:
                self._values["sse_enabled"] = sse_enabled

        @builtins.property
        def sse_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnCluster.SSESpecificationProperty.SSEEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dax-cluster-ssespecification.html#cfn-dax-cluster-ssespecification-sseenabled
            '''
            result = self._values.get("sse_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SSESpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_dax.CfnClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "iam_role_arn": "iamRoleArn",
        "node_type": "nodeType",
        "replication_factor": "replicationFactor",
        "availability_zones": "availabilityZones",
        "cluster_name": "clusterName",
        "description": "description",
        "notification_topic_arn": "notificationTopicArn",
        "parameter_group_name": "parameterGroupName",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "security_group_ids": "securityGroupIds",
        "sse_specification": "sseSpecification",
        "subnet_group_name": "subnetGroupName",
        "tags": "tags",
    },
)
class CfnClusterProps:
    def __init__(
        self,
        *,
        iam_role_arn: builtins.str,
        node_type: builtins.str,
        replication_factor: jsii.Number,
        availability_zones: typing.Optional[typing.List[builtins.str]] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        notification_topic_arn: typing.Optional[builtins.str] = None,
        parameter_group_name: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.List[builtins.str]] = None,
        sse_specification: typing.Optional[typing.Union[CfnCluster.SSESpecificationProperty, _IResolvable_a771d0ef]] = None,
        subnet_group_name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``AWS::DAX::Cluster``.

        :param iam_role_arn: ``AWS::DAX::Cluster.IAMRoleARN``.
        :param node_type: ``AWS::DAX::Cluster.NodeType``.
        :param replication_factor: ``AWS::DAX::Cluster.ReplicationFactor``.
        :param availability_zones: ``AWS::DAX::Cluster.AvailabilityZones``.
        :param cluster_name: ``AWS::DAX::Cluster.ClusterName``.
        :param description: ``AWS::DAX::Cluster.Description``.
        :param notification_topic_arn: ``AWS::DAX::Cluster.NotificationTopicARN``.
        :param parameter_group_name: ``AWS::DAX::Cluster.ParameterGroupName``.
        :param preferred_maintenance_window: ``AWS::DAX::Cluster.PreferredMaintenanceWindow``.
        :param security_group_ids: ``AWS::DAX::Cluster.SecurityGroupIds``.
        :param sse_specification: ``AWS::DAX::Cluster.SSESpecification``.
        :param subnet_group_name: ``AWS::DAX::Cluster.SubnetGroupName``.
        :param tags: ``AWS::DAX::Cluster.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "iam_role_arn": iam_role_arn,
            "node_type": node_type,
            "replication_factor": replication_factor,
        }
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if description is not None:
            self._values["description"] = description
        if notification_topic_arn is not None:
            self._values["notification_topic_arn"] = notification_topic_arn
        if parameter_group_name is not None:
            self._values["parameter_group_name"] = parameter_group_name
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if sse_specification is not None:
            self._values["sse_specification"] = sse_specification
        if subnet_group_name is not None:
            self._values["subnet_group_name"] = subnet_group_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def iam_role_arn(self) -> builtins.str:
        '''``AWS::DAX::Cluster.IAMRoleARN``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-iamrolearn
        '''
        result = self._values.get("iam_role_arn")
        assert result is not None, "Required property 'iam_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_type(self) -> builtins.str:
        '''``AWS::DAX::Cluster.NodeType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-nodetype
        '''
        result = self._values.get("node_type")
        assert result is not None, "Required property 'node_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replication_factor(self) -> jsii.Number:
        '''``AWS::DAX::Cluster.ReplicationFactor``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-replicationfactor
        '''
        result = self._values.get("replication_factor")
        assert result is not None, "Required property 'replication_factor' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::DAX::Cluster.AvailabilityZones``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-availabilityzones
        '''
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::DAX::Cluster.ClusterName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-clustername
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::DAX::Cluster.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_topic_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::DAX::Cluster.NotificationTopicARN``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-notificationtopicarn
        '''
        result = self._values.get("notification_topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::DAX::Cluster.ParameterGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-parametergroupname
        '''
        result = self._values.get("parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''``AWS::DAX::Cluster.PreferredMaintenanceWindow``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-preferredmaintenancewindow
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::DAX::Cluster.SecurityGroupIds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sse_specification(
        self,
    ) -> typing.Optional[typing.Union[CfnCluster.SSESpecificationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::DAX::Cluster.SSESpecification``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-ssespecification
        '''
        result = self._values.get("sse_specification")
        return typing.cast(typing.Optional[typing.Union[CfnCluster.SSESpecificationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::DAX::Cluster.SubnetGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-subnetgroupname
        '''
        result = self._values.get("subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''``AWS::DAX::Cluster.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnParameterGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_dax.CfnParameterGroup",
):
    '''A CloudFormation ``AWS::DAX::ParameterGroup``.

    :cloudformationResource: AWS::DAX::ParameterGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        parameter_group_name: typing.Optional[builtins.str] = None,
        parameter_name_values: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::DAX::ParameterGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::DAX::ParameterGroup.Description``.
        :param parameter_group_name: ``AWS::DAX::ParameterGroup.ParameterGroupName``.
        :param parameter_name_values: ``AWS::DAX::ParameterGroup.ParameterNameValues``.
        '''
        props = CfnParameterGroupProps(
            description=description,
            parameter_group_name=parameter_group_name,
            parameter_name_values=parameter_name_values,
        )

        jsii.create(CfnParameterGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="parameterNameValues")
    def parameter_name_values(self) -> typing.Any:
        '''``AWS::DAX::ParameterGroup.ParameterNameValues``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-parameternamevalues
        '''
        return typing.cast(typing.Any, jsii.get(self, "parameterNameValues"))

    @parameter_name_values.setter
    def parameter_name_values(self, value: typing.Any) -> None:
        jsii.set(self, "parameterNameValues", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::DAX::ParameterGroup.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::DAX::ParameterGroup.ParameterGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-parametergroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterGroupName"))

    @parameter_group_name.setter
    def parameter_group_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "parameterGroupName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_dax.CfnParameterGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "parameter_group_name": "parameterGroupName",
        "parameter_name_values": "parameterNameValues",
    },
)
class CfnParameterGroupProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        parameter_group_name: typing.Optional[builtins.str] = None,
        parameter_name_values: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``AWS::DAX::ParameterGroup``.

        :param description: ``AWS::DAX::ParameterGroup.Description``.
        :param parameter_group_name: ``AWS::DAX::ParameterGroup.ParameterGroupName``.
        :param parameter_name_values: ``AWS::DAX::ParameterGroup.ParameterNameValues``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if parameter_group_name is not None:
            self._values["parameter_group_name"] = parameter_group_name
        if parameter_name_values is not None:
            self._values["parameter_name_values"] = parameter_name_values

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::DAX::ParameterGroup.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::DAX::ParameterGroup.ParameterGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-parametergroupname
        '''
        result = self._values.get("parameter_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_name_values(self) -> typing.Any:
        '''``AWS::DAX::ParameterGroup.ParameterNameValues``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-parameternamevalues
        '''
        result = self._values.get("parameter_name_values")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnParameterGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSubnetGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_dax.CfnSubnetGroup",
):
    '''A CloudFormation ``AWS::DAX::SubnetGroup``.

    :cloudformationResource: AWS::DAX::SubnetGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        subnet_ids: typing.List[builtins.str],
        description: typing.Optional[builtins.str] = None,
        subnet_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::DAX::SubnetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param subnet_ids: ``AWS::DAX::SubnetGroup.SubnetIds``.
        :param description: ``AWS::DAX::SubnetGroup.Description``.
        :param subnet_group_name: ``AWS::DAX::SubnetGroup.SubnetGroupName``.
        '''
        props = CfnSubnetGroupProps(
            subnet_ids=subnet_ids,
            description=description,
            subnet_group_name=subnet_group_name,
        )

        jsii.create(CfnSubnetGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''``AWS::DAX::SubnetGroup.SubnetIds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-subnetids
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "subnetIds", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::DAX::SubnetGroup.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subnetGroupName")
    def subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::DAX::SubnetGroup.SubnetGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-subnetgroupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetGroupName"))

    @subnet_group_name.setter
    def subnet_group_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "subnetGroupName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_dax.CfnSubnetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "subnet_ids": "subnetIds",
        "description": "description",
        "subnet_group_name": "subnetGroupName",
    },
)
class CfnSubnetGroupProps:
    def __init__(
        self,
        *,
        subnet_ids: typing.List[builtins.str],
        description: typing.Optional[builtins.str] = None,
        subnet_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::DAX::SubnetGroup``.

        :param subnet_ids: ``AWS::DAX::SubnetGroup.SubnetIds``.
        :param description: ``AWS::DAX::SubnetGroup.Description``.
        :param subnet_group_name: ``AWS::DAX::SubnetGroup.SubnetGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "subnet_ids": subnet_ids,
        }
        if description is not None:
            self._values["description"] = description
        if subnet_group_name is not None:
            self._values["subnet_group_name"] = subnet_group_name

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''``AWS::DAX::SubnetGroup.SubnetIds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-subnetids
        '''
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::DAX::SubnetGroup.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_group_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::DAX::SubnetGroup.SubnetGroupName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-subnetgroupname
        '''
        result = self._values.get("subnet_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubnetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnCluster",
    "CfnClusterProps",
    "CfnParameterGroup",
    "CfnParameterGroupProps",
    "CfnSubnetGroup",
    "CfnSubnetGroupProps",
]

publication.publish()
