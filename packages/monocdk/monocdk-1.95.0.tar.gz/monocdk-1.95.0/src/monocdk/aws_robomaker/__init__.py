'''
# AWS RoboMaker Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_robomaker as robomaker
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

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnFleet(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_robomaker.CfnFleet",
):
    '''A CloudFormation ``AWS::RoboMaker::Fleet``.

    :cloudformationResource: AWS::RoboMaker::Fleet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-fleet.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::RoboMaker::Fleet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::RoboMaker::Fleet.Name``.
        :param tags: ``AWS::RoboMaker::Fleet.Tags``.
        '''
        props = CfnFleetProps(name=name, tags=tags)

        jsii.create(CfnFleet, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::RoboMaker::Fleet.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-fleet.html#cfn-robomaker-fleet-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::RoboMaker::Fleet.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-fleet.html#cfn-robomaker-fleet-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="monocdk.aws_robomaker.CfnFleetProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "tags": "tags"},
)
class CfnFleetProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``AWS::RoboMaker::Fleet``.

        :param name: ``AWS::RoboMaker::Fleet.Name``.
        :param tags: ``AWS::RoboMaker::Fleet.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-fleet.html
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::RoboMaker::Fleet.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-fleet.html#cfn-robomaker-fleet-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''``AWS::RoboMaker::Fleet.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-fleet.html#cfn-robomaker-fleet-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFleetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnRobot(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_robomaker.CfnRobot",
):
    '''A CloudFormation ``AWS::RoboMaker::Robot``.

    :cloudformationResource: AWS::RoboMaker::Robot
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        architecture: builtins.str,
        greengrass_group_id: builtins.str,
        fleet: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::RoboMaker::Robot``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param architecture: ``AWS::RoboMaker::Robot.Architecture``.
        :param greengrass_group_id: ``AWS::RoboMaker::Robot.GreengrassGroupId``.
        :param fleet: ``AWS::RoboMaker::Robot.Fleet``.
        :param name: ``AWS::RoboMaker::Robot.Name``.
        :param tags: ``AWS::RoboMaker::Robot.Tags``.
        '''
        props = CfnRobotProps(
            architecture=architecture,
            greengrass_group_id=greengrass_group_id,
            fleet=fleet,
            name=name,
            tags=tags,
        )

        jsii.create(CfnRobot, self, [scope, id, props])

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
        '''``AWS::RoboMaker::Robot.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="architecture")
    def architecture(self) -> builtins.str:
        '''``AWS::RoboMaker::Robot.Architecture``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-architecture
        '''
        return typing.cast(builtins.str, jsii.get(self, "architecture"))

    @architecture.setter
    def architecture(self, value: builtins.str) -> None:
        jsii.set(self, "architecture", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="greengrassGroupId")
    def greengrass_group_id(self) -> builtins.str:
        '''``AWS::RoboMaker::Robot.GreengrassGroupId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-greengrassgroupid
        '''
        return typing.cast(builtins.str, jsii.get(self, "greengrassGroupId"))

    @greengrass_group_id.setter
    def greengrass_group_id(self, value: builtins.str) -> None:
        jsii.set(self, "greengrassGroupId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="fleet")
    def fleet(self) -> typing.Optional[builtins.str]:
        '''``AWS::RoboMaker::Robot.Fleet``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-fleet
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fleet"))

    @fleet.setter
    def fleet(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "fleet", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::RoboMaker::Robot.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)


@jsii.implements(_IInspectable_82c04a63)
class CfnRobotApplication(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_robomaker.CfnRobotApplication",
):
    '''A CloudFormation ``AWS::RoboMaker::RobotApplication``.

    :cloudformationResource: AWS::RoboMaker::RobotApplication
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        robot_software_suite: typing.Union["CfnRobotApplication.RobotSoftwareSuiteProperty", _IResolvable_a771d0ef],
        sources: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRobotApplication.SourceConfigProperty", _IResolvable_a771d0ef]]],
        current_revision_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::RoboMaker::RobotApplication``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param robot_software_suite: ``AWS::RoboMaker::RobotApplication.RobotSoftwareSuite``.
        :param sources: ``AWS::RoboMaker::RobotApplication.Sources``.
        :param current_revision_id: ``AWS::RoboMaker::RobotApplication.CurrentRevisionId``.
        :param name: ``AWS::RoboMaker::RobotApplication.Name``.
        :param tags: ``AWS::RoboMaker::RobotApplication.Tags``.
        '''
        props = CfnRobotApplicationProps(
            robot_software_suite=robot_software_suite,
            sources=sources,
            current_revision_id=current_revision_id,
            name=name,
            tags=tags,
        )

        jsii.create(CfnRobotApplication, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrCurrentRevisionId")
    def attr_current_revision_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: CurrentRevisionId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCurrentRevisionId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::RoboMaker::RobotApplication.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="robotSoftwareSuite")
    def robot_software_suite(
        self,
    ) -> typing.Union["CfnRobotApplication.RobotSoftwareSuiteProperty", _IResolvable_a771d0ef]:
        '''``AWS::RoboMaker::RobotApplication.RobotSoftwareSuite``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-robotsoftwaresuite
        '''
        return typing.cast(typing.Union["CfnRobotApplication.RobotSoftwareSuiteProperty", _IResolvable_a771d0ef], jsii.get(self, "robotSoftwareSuite"))

    @robot_software_suite.setter
    def robot_software_suite(
        self,
        value: typing.Union["CfnRobotApplication.RobotSoftwareSuiteProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "robotSoftwareSuite", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sources")
    def sources(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRobotApplication.SourceConfigProperty", _IResolvable_a771d0ef]]]:
        '''``AWS::RoboMaker::RobotApplication.Sources``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-sources
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRobotApplication.SourceConfigProperty", _IResolvable_a771d0ef]]], jsii.get(self, "sources"))

    @sources.setter
    def sources(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRobotApplication.SourceConfigProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        jsii.set(self, "sources", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="currentRevisionId")
    def current_revision_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::RoboMaker::RobotApplication.CurrentRevisionId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-currentrevisionid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "currentRevisionId"))

    @current_revision_id.setter
    def current_revision_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "currentRevisionId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::RoboMaker::RobotApplication.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_robomaker.CfnRobotApplication.RobotSoftwareSuiteProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "version": "version"},
    )
    class RobotSoftwareSuiteProperty:
        def __init__(self, *, name: builtins.str, version: builtins.str) -> None:
            '''
            :param name: ``CfnRobotApplication.RobotSoftwareSuiteProperty.Name``.
            :param version: ``CfnRobotApplication.RobotSoftwareSuiteProperty.Version``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-robotapplication-robotsoftwaresuite.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "version": version,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnRobotApplication.RobotSoftwareSuiteProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-robotapplication-robotsoftwaresuite.html#cfn-robomaker-robotapplication-robotsoftwaresuite-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> builtins.str:
            '''``CfnRobotApplication.RobotSoftwareSuiteProperty.Version``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-robotapplication-robotsoftwaresuite.html#cfn-robomaker-robotapplication-robotsoftwaresuite-version
            '''
            result = self._values.get("version")
            assert result is not None, "Required property 'version' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RobotSoftwareSuiteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_robomaker.CfnRobotApplication.SourceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "architecture": "architecture",
            "s3_bucket": "s3Bucket",
            "s3_key": "s3Key",
        },
    )
    class SourceConfigProperty:
        def __init__(
            self,
            *,
            architecture: builtins.str,
            s3_bucket: builtins.str,
            s3_key: builtins.str,
        ) -> None:
            '''
            :param architecture: ``CfnRobotApplication.SourceConfigProperty.Architecture``.
            :param s3_bucket: ``CfnRobotApplication.SourceConfigProperty.S3Bucket``.
            :param s3_key: ``CfnRobotApplication.SourceConfigProperty.S3Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-robotapplication-sourceconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "architecture": architecture,
                "s3_bucket": s3_bucket,
                "s3_key": s3_key,
            }

        @builtins.property
        def architecture(self) -> builtins.str:
            '''``CfnRobotApplication.SourceConfigProperty.Architecture``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-robotapplication-sourceconfig.html#cfn-robomaker-robotapplication-sourceconfig-architecture
            '''
            result = self._values.get("architecture")
            assert result is not None, "Required property 'architecture' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_bucket(self) -> builtins.str:
            '''``CfnRobotApplication.SourceConfigProperty.S3Bucket``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-robotapplication-sourceconfig.html#cfn-robomaker-robotapplication-sourceconfig-s3bucket
            '''
            result = self._values.get("s3_bucket")
            assert result is not None, "Required property 's3_bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_key(self) -> builtins.str:
            '''``CfnRobotApplication.SourceConfigProperty.S3Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-robotapplication-sourceconfig.html#cfn-robomaker-robotapplication-sourceconfig-s3key
            '''
            result = self._values.get("s3_key")
            assert result is not None, "Required property 's3_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_robomaker.CfnRobotApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "robot_software_suite": "robotSoftwareSuite",
        "sources": "sources",
        "current_revision_id": "currentRevisionId",
        "name": "name",
        "tags": "tags",
    },
)
class CfnRobotApplicationProps:
    def __init__(
        self,
        *,
        robot_software_suite: typing.Union[CfnRobotApplication.RobotSoftwareSuiteProperty, _IResolvable_a771d0ef],
        sources: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnRobotApplication.SourceConfigProperty, _IResolvable_a771d0ef]]],
        current_revision_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``AWS::RoboMaker::RobotApplication``.

        :param robot_software_suite: ``AWS::RoboMaker::RobotApplication.RobotSoftwareSuite``.
        :param sources: ``AWS::RoboMaker::RobotApplication.Sources``.
        :param current_revision_id: ``AWS::RoboMaker::RobotApplication.CurrentRevisionId``.
        :param name: ``AWS::RoboMaker::RobotApplication.Name``.
        :param tags: ``AWS::RoboMaker::RobotApplication.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "robot_software_suite": robot_software_suite,
            "sources": sources,
        }
        if current_revision_id is not None:
            self._values["current_revision_id"] = current_revision_id
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def robot_software_suite(
        self,
    ) -> typing.Union[CfnRobotApplication.RobotSoftwareSuiteProperty, _IResolvable_a771d0ef]:
        '''``AWS::RoboMaker::RobotApplication.RobotSoftwareSuite``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-robotsoftwaresuite
        '''
        result = self._values.get("robot_software_suite")
        assert result is not None, "Required property 'robot_software_suite' is missing"
        return typing.cast(typing.Union[CfnRobotApplication.RobotSoftwareSuiteProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnRobotApplication.SourceConfigProperty, _IResolvable_a771d0ef]]]:
        '''``AWS::RoboMaker::RobotApplication.Sources``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-sources
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnRobotApplication.SourceConfigProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def current_revision_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::RoboMaker::RobotApplication.CurrentRevisionId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-currentrevisionid
        '''
        result = self._values.get("current_revision_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::RoboMaker::RobotApplication.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''``AWS::RoboMaker::RobotApplication.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplication.html#cfn-robomaker-robotapplication-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRobotApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnRobotApplicationVersion(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_robomaker.CfnRobotApplicationVersion",
):
    '''A CloudFormation ``AWS::RoboMaker::RobotApplicationVersion``.

    :cloudformationResource: AWS::RoboMaker::RobotApplicationVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplicationversion.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application: builtins.str,
        current_revision_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::RoboMaker::RobotApplicationVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application: ``AWS::RoboMaker::RobotApplicationVersion.Application``.
        :param current_revision_id: ``AWS::RoboMaker::RobotApplicationVersion.CurrentRevisionId``.
        '''
        props = CfnRobotApplicationVersionProps(
            application=application, current_revision_id=current_revision_id
        )

        jsii.create(CfnRobotApplicationVersion, self, [scope, id, props])

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
    @jsii.member(jsii_name="application")
    def application(self) -> builtins.str:
        '''``AWS::RoboMaker::RobotApplicationVersion.Application``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplicationversion.html#cfn-robomaker-robotapplicationversion-application
        '''
        return typing.cast(builtins.str, jsii.get(self, "application"))

    @application.setter
    def application(self, value: builtins.str) -> None:
        jsii.set(self, "application", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="currentRevisionId")
    def current_revision_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::RoboMaker::RobotApplicationVersion.CurrentRevisionId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplicationversion.html#cfn-robomaker-robotapplicationversion-currentrevisionid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "currentRevisionId"))

    @current_revision_id.setter
    def current_revision_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "currentRevisionId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_robomaker.CfnRobotApplicationVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "application": "application",
        "current_revision_id": "currentRevisionId",
    },
)
class CfnRobotApplicationVersionProps:
    def __init__(
        self,
        *,
        application: builtins.str,
        current_revision_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::RoboMaker::RobotApplicationVersion``.

        :param application: ``AWS::RoboMaker::RobotApplicationVersion.Application``.
        :param current_revision_id: ``AWS::RoboMaker::RobotApplicationVersion.CurrentRevisionId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplicationversion.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "application": application,
        }
        if current_revision_id is not None:
            self._values["current_revision_id"] = current_revision_id

    @builtins.property
    def application(self) -> builtins.str:
        '''``AWS::RoboMaker::RobotApplicationVersion.Application``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplicationversion.html#cfn-robomaker-robotapplicationversion-application
        '''
        result = self._values.get("application")
        assert result is not None, "Required property 'application' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def current_revision_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::RoboMaker::RobotApplicationVersion.CurrentRevisionId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robotapplicationversion.html#cfn-robomaker-robotapplicationversion-currentrevisionid
        '''
        result = self._values.get("current_revision_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRobotApplicationVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_robomaker.CfnRobotProps",
    jsii_struct_bases=[],
    name_mapping={
        "architecture": "architecture",
        "greengrass_group_id": "greengrassGroupId",
        "fleet": "fleet",
        "name": "name",
        "tags": "tags",
    },
)
class CfnRobotProps:
    def __init__(
        self,
        *,
        architecture: builtins.str,
        greengrass_group_id: builtins.str,
        fleet: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``AWS::RoboMaker::Robot``.

        :param architecture: ``AWS::RoboMaker::Robot.Architecture``.
        :param greengrass_group_id: ``AWS::RoboMaker::Robot.GreengrassGroupId``.
        :param fleet: ``AWS::RoboMaker::Robot.Fleet``.
        :param name: ``AWS::RoboMaker::Robot.Name``.
        :param tags: ``AWS::RoboMaker::Robot.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "architecture": architecture,
            "greengrass_group_id": greengrass_group_id,
        }
        if fleet is not None:
            self._values["fleet"] = fleet
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def architecture(self) -> builtins.str:
        '''``AWS::RoboMaker::Robot.Architecture``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-architecture
        '''
        result = self._values.get("architecture")
        assert result is not None, "Required property 'architecture' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def greengrass_group_id(self) -> builtins.str:
        '''``AWS::RoboMaker::Robot.GreengrassGroupId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-greengrassgroupid
        '''
        result = self._values.get("greengrass_group_id")
        assert result is not None, "Required property 'greengrass_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fleet(self) -> typing.Optional[builtins.str]:
        '''``AWS::RoboMaker::Robot.Fleet``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-fleet
        '''
        result = self._values.get("fleet")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::RoboMaker::Robot.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''``AWS::RoboMaker::Robot.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-robot.html#cfn-robomaker-robot-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRobotProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSimulationApplication(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_robomaker.CfnSimulationApplication",
):
    '''A CloudFormation ``AWS::RoboMaker::SimulationApplication``.

    :cloudformationResource: AWS::RoboMaker::SimulationApplication
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        rendering_engine: typing.Union["CfnSimulationApplication.RenderingEngineProperty", _IResolvable_a771d0ef],
        robot_software_suite: typing.Union["CfnSimulationApplication.RobotSoftwareSuiteProperty", _IResolvable_a771d0ef],
        simulation_software_suite: typing.Union["CfnSimulationApplication.SimulationSoftwareSuiteProperty", _IResolvable_a771d0ef],
        sources: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSimulationApplication.SourceConfigProperty", _IResolvable_a771d0ef]]],
        current_revision_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Create a new ``AWS::RoboMaker::SimulationApplication``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param rendering_engine: ``AWS::RoboMaker::SimulationApplication.RenderingEngine``.
        :param robot_software_suite: ``AWS::RoboMaker::SimulationApplication.RobotSoftwareSuite``.
        :param simulation_software_suite: ``AWS::RoboMaker::SimulationApplication.SimulationSoftwareSuite``.
        :param sources: ``AWS::RoboMaker::SimulationApplication.Sources``.
        :param current_revision_id: ``AWS::RoboMaker::SimulationApplication.CurrentRevisionId``.
        :param name: ``AWS::RoboMaker::SimulationApplication.Name``.
        :param tags: ``AWS::RoboMaker::SimulationApplication.Tags``.
        '''
        props = CfnSimulationApplicationProps(
            rendering_engine=rendering_engine,
            robot_software_suite=robot_software_suite,
            simulation_software_suite=simulation_software_suite,
            sources=sources,
            current_revision_id=current_revision_id,
            name=name,
            tags=tags,
        )

        jsii.create(CfnSimulationApplication, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrCurrentRevisionId")
    def attr_current_revision_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: CurrentRevisionId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCurrentRevisionId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::RoboMaker::SimulationApplication.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="renderingEngine")
    def rendering_engine(
        self,
    ) -> typing.Union["CfnSimulationApplication.RenderingEngineProperty", _IResolvable_a771d0ef]:
        '''``AWS::RoboMaker::SimulationApplication.RenderingEngine``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-renderingengine
        '''
        return typing.cast(typing.Union["CfnSimulationApplication.RenderingEngineProperty", _IResolvable_a771d0ef], jsii.get(self, "renderingEngine"))

    @rendering_engine.setter
    def rendering_engine(
        self,
        value: typing.Union["CfnSimulationApplication.RenderingEngineProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "renderingEngine", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="robotSoftwareSuite")
    def robot_software_suite(
        self,
    ) -> typing.Union["CfnSimulationApplication.RobotSoftwareSuiteProperty", _IResolvable_a771d0ef]:
        '''``AWS::RoboMaker::SimulationApplication.RobotSoftwareSuite``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-robotsoftwaresuite
        '''
        return typing.cast(typing.Union["CfnSimulationApplication.RobotSoftwareSuiteProperty", _IResolvable_a771d0ef], jsii.get(self, "robotSoftwareSuite"))

    @robot_software_suite.setter
    def robot_software_suite(
        self,
        value: typing.Union["CfnSimulationApplication.RobotSoftwareSuiteProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "robotSoftwareSuite", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="simulationSoftwareSuite")
    def simulation_software_suite(
        self,
    ) -> typing.Union["CfnSimulationApplication.SimulationSoftwareSuiteProperty", _IResolvable_a771d0ef]:
        '''``AWS::RoboMaker::SimulationApplication.SimulationSoftwareSuite``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-simulationsoftwaresuite
        '''
        return typing.cast(typing.Union["CfnSimulationApplication.SimulationSoftwareSuiteProperty", _IResolvable_a771d0ef], jsii.get(self, "simulationSoftwareSuite"))

    @simulation_software_suite.setter
    def simulation_software_suite(
        self,
        value: typing.Union["CfnSimulationApplication.SimulationSoftwareSuiteProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "simulationSoftwareSuite", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sources")
    def sources(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSimulationApplication.SourceConfigProperty", _IResolvable_a771d0ef]]]:
        '''``AWS::RoboMaker::SimulationApplication.Sources``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-sources
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSimulationApplication.SourceConfigProperty", _IResolvable_a771d0ef]]], jsii.get(self, "sources"))

    @sources.setter
    def sources(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnSimulationApplication.SourceConfigProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        jsii.set(self, "sources", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="currentRevisionId")
    def current_revision_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::RoboMaker::SimulationApplication.CurrentRevisionId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-currentrevisionid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "currentRevisionId"))

    @current_revision_id.setter
    def current_revision_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "currentRevisionId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::RoboMaker::SimulationApplication.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_robomaker.CfnSimulationApplication.RenderingEngineProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "version": "version"},
    )
    class RenderingEngineProperty:
        def __init__(self, *, name: builtins.str, version: builtins.str) -> None:
            '''
            :param name: ``CfnSimulationApplication.RenderingEngineProperty.Name``.
            :param version: ``CfnSimulationApplication.RenderingEngineProperty.Version``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-renderingengine.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "version": version,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnSimulationApplication.RenderingEngineProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-renderingengine.html#cfn-robomaker-simulationapplication-renderingengine-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> builtins.str:
            '''``CfnSimulationApplication.RenderingEngineProperty.Version``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-renderingengine.html#cfn-robomaker-simulationapplication-renderingengine-version
            '''
            result = self._values.get("version")
            assert result is not None, "Required property 'version' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RenderingEngineProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_robomaker.CfnSimulationApplication.RobotSoftwareSuiteProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "version": "version"},
    )
    class RobotSoftwareSuiteProperty:
        def __init__(self, *, name: builtins.str, version: builtins.str) -> None:
            '''
            :param name: ``CfnSimulationApplication.RobotSoftwareSuiteProperty.Name``.
            :param version: ``CfnSimulationApplication.RobotSoftwareSuiteProperty.Version``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-robotsoftwaresuite.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "version": version,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnSimulationApplication.RobotSoftwareSuiteProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-robotsoftwaresuite.html#cfn-robomaker-simulationapplication-robotsoftwaresuite-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> builtins.str:
            '''``CfnSimulationApplication.RobotSoftwareSuiteProperty.Version``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-robotsoftwaresuite.html#cfn-robomaker-simulationapplication-robotsoftwaresuite-version
            '''
            result = self._values.get("version")
            assert result is not None, "Required property 'version' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RobotSoftwareSuiteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_robomaker.CfnSimulationApplication.SimulationSoftwareSuiteProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "version": "version"},
    )
    class SimulationSoftwareSuiteProperty:
        def __init__(self, *, name: builtins.str, version: builtins.str) -> None:
            '''
            :param name: ``CfnSimulationApplication.SimulationSoftwareSuiteProperty.Name``.
            :param version: ``CfnSimulationApplication.SimulationSoftwareSuiteProperty.Version``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-simulationsoftwaresuite.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "version": version,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnSimulationApplication.SimulationSoftwareSuiteProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-simulationsoftwaresuite.html#cfn-robomaker-simulationapplication-simulationsoftwaresuite-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> builtins.str:
            '''``CfnSimulationApplication.SimulationSoftwareSuiteProperty.Version``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-simulationsoftwaresuite.html#cfn-robomaker-simulationapplication-simulationsoftwaresuite-version
            '''
            result = self._values.get("version")
            assert result is not None, "Required property 'version' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SimulationSoftwareSuiteProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_robomaker.CfnSimulationApplication.SourceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "architecture": "architecture",
            "s3_bucket": "s3Bucket",
            "s3_key": "s3Key",
        },
    )
    class SourceConfigProperty:
        def __init__(
            self,
            *,
            architecture: builtins.str,
            s3_bucket: builtins.str,
            s3_key: builtins.str,
        ) -> None:
            '''
            :param architecture: ``CfnSimulationApplication.SourceConfigProperty.Architecture``.
            :param s3_bucket: ``CfnSimulationApplication.SourceConfigProperty.S3Bucket``.
            :param s3_key: ``CfnSimulationApplication.SourceConfigProperty.S3Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-sourceconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "architecture": architecture,
                "s3_bucket": s3_bucket,
                "s3_key": s3_key,
            }

        @builtins.property
        def architecture(self) -> builtins.str:
            '''``CfnSimulationApplication.SourceConfigProperty.Architecture``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-sourceconfig.html#cfn-robomaker-simulationapplication-sourceconfig-architecture
            '''
            result = self._values.get("architecture")
            assert result is not None, "Required property 'architecture' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_bucket(self) -> builtins.str:
            '''``CfnSimulationApplication.SourceConfigProperty.S3Bucket``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-sourceconfig.html#cfn-robomaker-simulationapplication-sourceconfig-s3bucket
            '''
            result = self._values.get("s3_bucket")
            assert result is not None, "Required property 's3_bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_key(self) -> builtins.str:
            '''``CfnSimulationApplication.SourceConfigProperty.S3Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-robomaker-simulationapplication-sourceconfig.html#cfn-robomaker-simulationapplication-sourceconfig-s3key
            '''
            result = self._values.get("s3_key")
            assert result is not None, "Required property 's3_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_robomaker.CfnSimulationApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "rendering_engine": "renderingEngine",
        "robot_software_suite": "robotSoftwareSuite",
        "simulation_software_suite": "simulationSoftwareSuite",
        "sources": "sources",
        "current_revision_id": "currentRevisionId",
        "name": "name",
        "tags": "tags",
    },
)
class CfnSimulationApplicationProps:
    def __init__(
        self,
        *,
        rendering_engine: typing.Union[CfnSimulationApplication.RenderingEngineProperty, _IResolvable_a771d0ef],
        robot_software_suite: typing.Union[CfnSimulationApplication.RobotSoftwareSuiteProperty, _IResolvable_a771d0ef],
        simulation_software_suite: typing.Union[CfnSimulationApplication.SimulationSoftwareSuiteProperty, _IResolvable_a771d0ef],
        sources: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnSimulationApplication.SourceConfigProperty, _IResolvable_a771d0ef]]],
        current_revision_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Any = None,
    ) -> None:
        '''Properties for defining a ``AWS::RoboMaker::SimulationApplication``.

        :param rendering_engine: ``AWS::RoboMaker::SimulationApplication.RenderingEngine``.
        :param robot_software_suite: ``AWS::RoboMaker::SimulationApplication.RobotSoftwareSuite``.
        :param simulation_software_suite: ``AWS::RoboMaker::SimulationApplication.SimulationSoftwareSuite``.
        :param sources: ``AWS::RoboMaker::SimulationApplication.Sources``.
        :param current_revision_id: ``AWS::RoboMaker::SimulationApplication.CurrentRevisionId``.
        :param name: ``AWS::RoboMaker::SimulationApplication.Name``.
        :param tags: ``AWS::RoboMaker::SimulationApplication.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "rendering_engine": rendering_engine,
            "robot_software_suite": robot_software_suite,
            "simulation_software_suite": simulation_software_suite,
            "sources": sources,
        }
        if current_revision_id is not None:
            self._values["current_revision_id"] = current_revision_id
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def rendering_engine(
        self,
    ) -> typing.Union[CfnSimulationApplication.RenderingEngineProperty, _IResolvable_a771d0ef]:
        '''``AWS::RoboMaker::SimulationApplication.RenderingEngine``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-renderingengine
        '''
        result = self._values.get("rendering_engine")
        assert result is not None, "Required property 'rendering_engine' is missing"
        return typing.cast(typing.Union[CfnSimulationApplication.RenderingEngineProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def robot_software_suite(
        self,
    ) -> typing.Union[CfnSimulationApplication.RobotSoftwareSuiteProperty, _IResolvable_a771d0ef]:
        '''``AWS::RoboMaker::SimulationApplication.RobotSoftwareSuite``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-robotsoftwaresuite
        '''
        result = self._values.get("robot_software_suite")
        assert result is not None, "Required property 'robot_software_suite' is missing"
        return typing.cast(typing.Union[CfnSimulationApplication.RobotSoftwareSuiteProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def simulation_software_suite(
        self,
    ) -> typing.Union[CfnSimulationApplication.SimulationSoftwareSuiteProperty, _IResolvable_a771d0ef]:
        '''``AWS::RoboMaker::SimulationApplication.SimulationSoftwareSuite``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-simulationsoftwaresuite
        '''
        result = self._values.get("simulation_software_suite")
        assert result is not None, "Required property 'simulation_software_suite' is missing"
        return typing.cast(typing.Union[CfnSimulationApplication.SimulationSoftwareSuiteProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def sources(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnSimulationApplication.SourceConfigProperty, _IResolvable_a771d0ef]]]:
        '''``AWS::RoboMaker::SimulationApplication.Sources``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-sources
        '''
        result = self._values.get("sources")
        assert result is not None, "Required property 'sources' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnSimulationApplication.SourceConfigProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def current_revision_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::RoboMaker::SimulationApplication.CurrentRevisionId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-currentrevisionid
        '''
        result = self._values.get("current_revision_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::RoboMaker::SimulationApplication.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''``AWS::RoboMaker::SimulationApplication.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplication.html#cfn-robomaker-simulationapplication-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSimulationApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSimulationApplicationVersion(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_robomaker.CfnSimulationApplicationVersion",
):
    '''A CloudFormation ``AWS::RoboMaker::SimulationApplicationVersion``.

    :cloudformationResource: AWS::RoboMaker::SimulationApplicationVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplicationversion.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application: builtins.str,
        current_revision_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::RoboMaker::SimulationApplicationVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application: ``AWS::RoboMaker::SimulationApplicationVersion.Application``.
        :param current_revision_id: ``AWS::RoboMaker::SimulationApplicationVersion.CurrentRevisionId``.
        '''
        props = CfnSimulationApplicationVersionProps(
            application=application, current_revision_id=current_revision_id
        )

        jsii.create(CfnSimulationApplicationVersion, self, [scope, id, props])

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
    @jsii.member(jsii_name="application")
    def application(self) -> builtins.str:
        '''``AWS::RoboMaker::SimulationApplicationVersion.Application``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplicationversion.html#cfn-robomaker-simulationapplicationversion-application
        '''
        return typing.cast(builtins.str, jsii.get(self, "application"))

    @application.setter
    def application(self, value: builtins.str) -> None:
        jsii.set(self, "application", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="currentRevisionId")
    def current_revision_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::RoboMaker::SimulationApplicationVersion.CurrentRevisionId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplicationversion.html#cfn-robomaker-simulationapplicationversion-currentrevisionid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "currentRevisionId"))

    @current_revision_id.setter
    def current_revision_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "currentRevisionId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_robomaker.CfnSimulationApplicationVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "application": "application",
        "current_revision_id": "currentRevisionId",
    },
)
class CfnSimulationApplicationVersionProps:
    def __init__(
        self,
        *,
        application: builtins.str,
        current_revision_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::RoboMaker::SimulationApplicationVersion``.

        :param application: ``AWS::RoboMaker::SimulationApplicationVersion.Application``.
        :param current_revision_id: ``AWS::RoboMaker::SimulationApplicationVersion.CurrentRevisionId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplicationversion.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "application": application,
        }
        if current_revision_id is not None:
            self._values["current_revision_id"] = current_revision_id

    @builtins.property
    def application(self) -> builtins.str:
        '''``AWS::RoboMaker::SimulationApplicationVersion.Application``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplicationversion.html#cfn-robomaker-simulationapplicationversion-application
        '''
        result = self._values.get("application")
        assert result is not None, "Required property 'application' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def current_revision_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::RoboMaker::SimulationApplicationVersion.CurrentRevisionId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-robomaker-simulationapplicationversion.html#cfn-robomaker-simulationapplicationversion-currentrevisionid
        '''
        result = self._values.get("current_revision_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSimulationApplicationVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnFleet",
    "CfnFleetProps",
    "CfnRobot",
    "CfnRobotApplication",
    "CfnRobotApplicationProps",
    "CfnRobotApplicationVersion",
    "CfnRobotApplicationVersionProps",
    "CfnRobotProps",
    "CfnSimulationApplication",
    "CfnSimulationApplicationProps",
    "CfnSimulationApplicationVersion",
    "CfnSimulationApplicationVersionProps",
]

publication.publish()
