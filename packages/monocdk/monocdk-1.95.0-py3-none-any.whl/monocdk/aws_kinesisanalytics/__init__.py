'''
# Amazon Kinesis Data Analytics Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## Kinesis Analytics Flink

The `aws-kinesisanalytics-flink` package provides constructs for building Flink applications.

* [Github](https://github.com/aws/aws-cdk/tree/master/packages/%40aws-cdk/aws-kinesisanalytics-flink)
* [CDK Docs](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-kinesisanalytics-flink.html)
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
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnApplication(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_kinesisanalytics.CfnApplication",
):
    '''A CloudFormation ``AWS::KinesisAnalytics::Application``.

    :cloudformationResource: AWS::KinesisAnalytics::Application
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        inputs: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplication.InputProperty", _IResolvable_a771d0ef]]],
        application_code: typing.Optional[builtins.str] = None,
        application_description: typing.Optional[builtins.str] = None,
        application_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::KinesisAnalytics::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param inputs: ``AWS::KinesisAnalytics::Application.Inputs``.
        :param application_code: ``AWS::KinesisAnalytics::Application.ApplicationCode``.
        :param application_description: ``AWS::KinesisAnalytics::Application.ApplicationDescription``.
        :param application_name: ``AWS::KinesisAnalytics::Application.ApplicationName``.
        '''
        props = CfnApplicationProps(
            inputs=inputs,
            application_code=application_code,
            application_description=application_description,
            application_name=application_name,
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
    @jsii.member(jsii_name="inputs")
    def inputs(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplication.InputProperty", _IResolvable_a771d0ef]]]:
        '''``AWS::KinesisAnalytics::Application.Inputs``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html#cfn-kinesisanalytics-application-inputs
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplication.InputProperty", _IResolvable_a771d0ef]]], jsii.get(self, "inputs"))

    @inputs.setter
    def inputs(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplication.InputProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        jsii.set(self, "inputs", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationCode")
    def application_code(self) -> typing.Optional[builtins.str]:
        '''``AWS::KinesisAnalytics::Application.ApplicationCode``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html#cfn-kinesisanalytics-application-applicationcode
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationCode"))

    @application_code.setter
    def application_code(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "applicationCode", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationDescription")
    def application_description(self) -> typing.Optional[builtins.str]:
        '''``AWS::KinesisAnalytics::Application.ApplicationDescription``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html#cfn-kinesisanalytics-application-applicationdescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationDescription"))

    @application_description.setter
    def application_description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "applicationDescription", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::KinesisAnalytics::Application.ApplicationName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html#cfn-kinesisanalytics-application-applicationname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationName"))

    @application_name.setter
    def application_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "applicationName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplication.CSVMappingParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "record_column_delimiter": "recordColumnDelimiter",
            "record_row_delimiter": "recordRowDelimiter",
        },
    )
    class CSVMappingParametersProperty:
        def __init__(
            self,
            *,
            record_column_delimiter: builtins.str,
            record_row_delimiter: builtins.str,
        ) -> None:
            '''
            :param record_column_delimiter: ``CfnApplication.CSVMappingParametersProperty.RecordColumnDelimiter``.
            :param record_row_delimiter: ``CfnApplication.CSVMappingParametersProperty.RecordRowDelimiter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-csvmappingparameters.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "record_column_delimiter": record_column_delimiter,
                "record_row_delimiter": record_row_delimiter,
            }

        @builtins.property
        def record_column_delimiter(self) -> builtins.str:
            '''``CfnApplication.CSVMappingParametersProperty.RecordColumnDelimiter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-csvmappingparameters.html#cfn-kinesisanalytics-application-csvmappingparameters-recordcolumndelimiter
            '''
            result = self._values.get("record_column_delimiter")
            assert result is not None, "Required property 'record_column_delimiter' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def record_row_delimiter(self) -> builtins.str:
            '''``CfnApplication.CSVMappingParametersProperty.RecordRowDelimiter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-csvmappingparameters.html#cfn-kinesisanalytics-application-csvmappingparameters-recordrowdelimiter
            '''
            result = self._values.get("record_row_delimiter")
            assert result is not None, "Required property 'record_row_delimiter' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CSVMappingParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplication.InputLambdaProcessorProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
    )
    class InputLambdaProcessorProperty:
        def __init__(
            self,
            *,
            resource_arn: builtins.str,
            role_arn: builtins.str,
        ) -> None:
            '''
            :param resource_arn: ``CfnApplication.InputLambdaProcessorProperty.ResourceARN``.
            :param role_arn: ``CfnApplication.InputLambdaProcessorProperty.RoleARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputlambdaprocessor.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "resource_arn": resource_arn,
                "role_arn": role_arn,
            }

        @builtins.property
        def resource_arn(self) -> builtins.str:
            '''``CfnApplication.InputLambdaProcessorProperty.ResourceARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputlambdaprocessor.html#cfn-kinesisanalytics-application-inputlambdaprocessor-resourcearn
            '''
            result = self._values.get("resource_arn")
            assert result is not None, "Required property 'resource_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def role_arn(self) -> builtins.str:
            '''``CfnApplication.InputLambdaProcessorProperty.RoleARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputlambdaprocessor.html#cfn-kinesisanalytics-application-inputlambdaprocessor-rolearn
            '''
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputLambdaProcessorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplication.InputParallelismProperty",
        jsii_struct_bases=[],
        name_mapping={"count": "count"},
    )
    class InputParallelismProperty:
        def __init__(self, *, count: typing.Optional[jsii.Number] = None) -> None:
            '''
            :param count: ``CfnApplication.InputParallelismProperty.Count``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputparallelism.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if count is not None:
                self._values["count"] = count

        @builtins.property
        def count(self) -> typing.Optional[jsii.Number]:
            '''``CfnApplication.InputParallelismProperty.Count``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputparallelism.html#cfn-kinesisanalytics-application-inputparallelism-count
            '''
            result = self._values.get("count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputParallelismProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplication.InputProcessingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"input_lambda_processor": "inputLambdaProcessor"},
    )
    class InputProcessingConfigurationProperty:
        def __init__(
            self,
            *,
            input_lambda_processor: typing.Optional[typing.Union["CfnApplication.InputLambdaProcessorProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param input_lambda_processor: ``CfnApplication.InputProcessingConfigurationProperty.InputLambdaProcessor``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputprocessingconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if input_lambda_processor is not None:
                self._values["input_lambda_processor"] = input_lambda_processor

        @builtins.property
        def input_lambda_processor(
            self,
        ) -> typing.Optional[typing.Union["CfnApplication.InputLambdaProcessorProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplication.InputProcessingConfigurationProperty.InputLambdaProcessor``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputprocessingconfiguration.html#cfn-kinesisanalytics-application-inputprocessingconfiguration-inputlambdaprocessor
            '''
            result = self._values.get("input_lambda_processor")
            return typing.cast(typing.Optional[typing.Union["CfnApplication.InputLambdaProcessorProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputProcessingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplication.InputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "input_schema": "inputSchema",
            "name_prefix": "namePrefix",
            "input_parallelism": "inputParallelism",
            "input_processing_configuration": "inputProcessingConfiguration",
            "kinesis_firehose_input": "kinesisFirehoseInput",
            "kinesis_streams_input": "kinesisStreamsInput",
        },
    )
    class InputProperty:
        def __init__(
            self,
            *,
            input_schema: typing.Union["CfnApplication.InputSchemaProperty", _IResolvable_a771d0ef],
            name_prefix: builtins.str,
            input_parallelism: typing.Optional[typing.Union["CfnApplication.InputParallelismProperty", _IResolvable_a771d0ef]] = None,
            input_processing_configuration: typing.Optional[typing.Union["CfnApplication.InputProcessingConfigurationProperty", _IResolvable_a771d0ef]] = None,
            kinesis_firehose_input: typing.Optional[typing.Union["CfnApplication.KinesisFirehoseInputProperty", _IResolvable_a771d0ef]] = None,
            kinesis_streams_input: typing.Optional[typing.Union["CfnApplication.KinesisStreamsInputProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param input_schema: ``CfnApplication.InputProperty.InputSchema``.
            :param name_prefix: ``CfnApplication.InputProperty.NamePrefix``.
            :param input_parallelism: ``CfnApplication.InputProperty.InputParallelism``.
            :param input_processing_configuration: ``CfnApplication.InputProperty.InputProcessingConfiguration``.
            :param kinesis_firehose_input: ``CfnApplication.InputProperty.KinesisFirehoseInput``.
            :param kinesis_streams_input: ``CfnApplication.InputProperty.KinesisStreamsInput``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-input.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "input_schema": input_schema,
                "name_prefix": name_prefix,
            }
            if input_parallelism is not None:
                self._values["input_parallelism"] = input_parallelism
            if input_processing_configuration is not None:
                self._values["input_processing_configuration"] = input_processing_configuration
            if kinesis_firehose_input is not None:
                self._values["kinesis_firehose_input"] = kinesis_firehose_input
            if kinesis_streams_input is not None:
                self._values["kinesis_streams_input"] = kinesis_streams_input

        @builtins.property
        def input_schema(
            self,
        ) -> typing.Union["CfnApplication.InputSchemaProperty", _IResolvable_a771d0ef]:
            '''``CfnApplication.InputProperty.InputSchema``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-input.html#cfn-kinesisanalytics-application-input-inputschema
            '''
            result = self._values.get("input_schema")
            assert result is not None, "Required property 'input_schema' is missing"
            return typing.cast(typing.Union["CfnApplication.InputSchemaProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def name_prefix(self) -> builtins.str:
            '''``CfnApplication.InputProperty.NamePrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-input.html#cfn-kinesisanalytics-application-input-nameprefix
            '''
            result = self._values.get("name_prefix")
            assert result is not None, "Required property 'name_prefix' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def input_parallelism(
            self,
        ) -> typing.Optional[typing.Union["CfnApplication.InputParallelismProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplication.InputProperty.InputParallelism``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-input.html#cfn-kinesisanalytics-application-input-inputparallelism
            '''
            result = self._values.get("input_parallelism")
            return typing.cast(typing.Optional[typing.Union["CfnApplication.InputParallelismProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def input_processing_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnApplication.InputProcessingConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplication.InputProperty.InputProcessingConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-input.html#cfn-kinesisanalytics-application-input-inputprocessingconfiguration
            '''
            result = self._values.get("input_processing_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnApplication.InputProcessingConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def kinesis_firehose_input(
            self,
        ) -> typing.Optional[typing.Union["CfnApplication.KinesisFirehoseInputProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplication.InputProperty.KinesisFirehoseInput``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-input.html#cfn-kinesisanalytics-application-input-kinesisfirehoseinput
            '''
            result = self._values.get("kinesis_firehose_input")
            return typing.cast(typing.Optional[typing.Union["CfnApplication.KinesisFirehoseInputProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def kinesis_streams_input(
            self,
        ) -> typing.Optional[typing.Union["CfnApplication.KinesisStreamsInputProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplication.InputProperty.KinesisStreamsInput``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-input.html#cfn-kinesisanalytics-application-input-kinesisstreamsinput
            '''
            result = self._values.get("kinesis_streams_input")
            return typing.cast(typing.Optional[typing.Union["CfnApplication.KinesisStreamsInputProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplication.InputSchemaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "record_columns": "recordColumns",
            "record_format": "recordFormat",
            "record_encoding": "recordEncoding",
        },
    )
    class InputSchemaProperty:
        def __init__(
            self,
            *,
            record_columns: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplication.RecordColumnProperty", _IResolvable_a771d0ef]]],
            record_format: typing.Union["CfnApplication.RecordFormatProperty", _IResolvable_a771d0ef],
            record_encoding: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param record_columns: ``CfnApplication.InputSchemaProperty.RecordColumns``.
            :param record_format: ``CfnApplication.InputSchemaProperty.RecordFormat``.
            :param record_encoding: ``CfnApplication.InputSchemaProperty.RecordEncoding``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputschema.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "record_columns": record_columns,
                "record_format": record_format,
            }
            if record_encoding is not None:
                self._values["record_encoding"] = record_encoding

        @builtins.property
        def record_columns(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplication.RecordColumnProperty", _IResolvable_a771d0ef]]]:
            '''``CfnApplication.InputSchemaProperty.RecordColumns``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputschema.html#cfn-kinesisanalytics-application-inputschema-recordcolumns
            '''
            result = self._values.get("record_columns")
            assert result is not None, "Required property 'record_columns' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplication.RecordColumnProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def record_format(
            self,
        ) -> typing.Union["CfnApplication.RecordFormatProperty", _IResolvable_a771d0ef]:
            '''``CfnApplication.InputSchemaProperty.RecordFormat``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputschema.html#cfn-kinesisanalytics-application-inputschema-recordformat
            '''
            result = self._values.get("record_format")
            assert result is not None, "Required property 'record_format' is missing"
            return typing.cast(typing.Union["CfnApplication.RecordFormatProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def record_encoding(self) -> typing.Optional[builtins.str]:
            '''``CfnApplication.InputSchemaProperty.RecordEncoding``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputschema.html#cfn-kinesisanalytics-application-inputschema-recordencoding
            '''
            result = self._values.get("record_encoding")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputSchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplication.JSONMappingParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"record_row_path": "recordRowPath"},
    )
    class JSONMappingParametersProperty:
        def __init__(self, *, record_row_path: builtins.str) -> None:
            '''
            :param record_row_path: ``CfnApplication.JSONMappingParametersProperty.RecordRowPath``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-jsonmappingparameters.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "record_row_path": record_row_path,
            }

        @builtins.property
        def record_row_path(self) -> builtins.str:
            '''``CfnApplication.JSONMappingParametersProperty.RecordRowPath``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-jsonmappingparameters.html#cfn-kinesisanalytics-application-jsonmappingparameters-recordrowpath
            '''
            result = self._values.get("record_row_path")
            assert result is not None, "Required property 'record_row_path' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JSONMappingParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplication.KinesisFirehoseInputProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
    )
    class KinesisFirehoseInputProperty:
        def __init__(
            self,
            *,
            resource_arn: builtins.str,
            role_arn: builtins.str,
        ) -> None:
            '''
            :param resource_arn: ``CfnApplication.KinesisFirehoseInputProperty.ResourceARN``.
            :param role_arn: ``CfnApplication.KinesisFirehoseInputProperty.RoleARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-kinesisfirehoseinput.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "resource_arn": resource_arn,
                "role_arn": role_arn,
            }

        @builtins.property
        def resource_arn(self) -> builtins.str:
            '''``CfnApplication.KinesisFirehoseInputProperty.ResourceARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-kinesisfirehoseinput.html#cfn-kinesisanalytics-application-kinesisfirehoseinput-resourcearn
            '''
            result = self._values.get("resource_arn")
            assert result is not None, "Required property 'resource_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def role_arn(self) -> builtins.str:
            '''``CfnApplication.KinesisFirehoseInputProperty.RoleARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-kinesisfirehoseinput.html#cfn-kinesisanalytics-application-kinesisfirehoseinput-rolearn
            '''
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisFirehoseInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplication.KinesisStreamsInputProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
    )
    class KinesisStreamsInputProperty:
        def __init__(
            self,
            *,
            resource_arn: builtins.str,
            role_arn: builtins.str,
        ) -> None:
            '''
            :param resource_arn: ``CfnApplication.KinesisStreamsInputProperty.ResourceARN``.
            :param role_arn: ``CfnApplication.KinesisStreamsInputProperty.RoleARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-kinesisstreamsinput.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "resource_arn": resource_arn,
                "role_arn": role_arn,
            }

        @builtins.property
        def resource_arn(self) -> builtins.str:
            '''``CfnApplication.KinesisStreamsInputProperty.ResourceARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-kinesisstreamsinput.html#cfn-kinesisanalytics-application-kinesisstreamsinput-resourcearn
            '''
            result = self._values.get("resource_arn")
            assert result is not None, "Required property 'resource_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def role_arn(self) -> builtins.str:
            '''``CfnApplication.KinesisStreamsInputProperty.RoleARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-kinesisstreamsinput.html#cfn-kinesisanalytics-application-kinesisstreamsinput-rolearn
            '''
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisStreamsInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplication.MappingParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "csv_mapping_parameters": "csvMappingParameters",
            "json_mapping_parameters": "jsonMappingParameters",
        },
    )
    class MappingParametersProperty:
        def __init__(
            self,
            *,
            csv_mapping_parameters: typing.Optional[typing.Union["CfnApplication.CSVMappingParametersProperty", _IResolvable_a771d0ef]] = None,
            json_mapping_parameters: typing.Optional[typing.Union["CfnApplication.JSONMappingParametersProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param csv_mapping_parameters: ``CfnApplication.MappingParametersProperty.CSVMappingParameters``.
            :param json_mapping_parameters: ``CfnApplication.MappingParametersProperty.JSONMappingParameters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-mappingparameters.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if csv_mapping_parameters is not None:
                self._values["csv_mapping_parameters"] = csv_mapping_parameters
            if json_mapping_parameters is not None:
                self._values["json_mapping_parameters"] = json_mapping_parameters

        @builtins.property
        def csv_mapping_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnApplication.CSVMappingParametersProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplication.MappingParametersProperty.CSVMappingParameters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-mappingparameters.html#cfn-kinesisanalytics-application-mappingparameters-csvmappingparameters
            '''
            result = self._values.get("csv_mapping_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnApplication.CSVMappingParametersProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def json_mapping_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnApplication.JSONMappingParametersProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplication.MappingParametersProperty.JSONMappingParameters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-mappingparameters.html#cfn-kinesisanalytics-application-mappingparameters-jsonmappingparameters
            '''
            result = self._values.get("json_mapping_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnApplication.JSONMappingParametersProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MappingParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplication.RecordColumnProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "sql_type": "sqlType", "mapping": "mapping"},
    )
    class RecordColumnProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            sql_type: builtins.str,
            mapping: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param name: ``CfnApplication.RecordColumnProperty.Name``.
            :param sql_type: ``CfnApplication.RecordColumnProperty.SqlType``.
            :param mapping: ``CfnApplication.RecordColumnProperty.Mapping``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-recordcolumn.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "sql_type": sql_type,
            }
            if mapping is not None:
                self._values["mapping"] = mapping

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnApplication.RecordColumnProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-recordcolumn.html#cfn-kinesisanalytics-application-recordcolumn-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def sql_type(self) -> builtins.str:
            '''``CfnApplication.RecordColumnProperty.SqlType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-recordcolumn.html#cfn-kinesisanalytics-application-recordcolumn-sqltype
            '''
            result = self._values.get("sql_type")
            assert result is not None, "Required property 'sql_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def mapping(self) -> typing.Optional[builtins.str]:
            '''``CfnApplication.RecordColumnProperty.Mapping``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-recordcolumn.html#cfn-kinesisanalytics-application-recordcolumn-mapping
            '''
            result = self._values.get("mapping")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecordColumnProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplication.RecordFormatProperty",
        jsii_struct_bases=[],
        name_mapping={
            "record_format_type": "recordFormatType",
            "mapping_parameters": "mappingParameters",
        },
    )
    class RecordFormatProperty:
        def __init__(
            self,
            *,
            record_format_type: builtins.str,
            mapping_parameters: typing.Optional[typing.Union["CfnApplication.MappingParametersProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param record_format_type: ``CfnApplication.RecordFormatProperty.RecordFormatType``.
            :param mapping_parameters: ``CfnApplication.RecordFormatProperty.MappingParameters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-recordformat.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "record_format_type": record_format_type,
            }
            if mapping_parameters is not None:
                self._values["mapping_parameters"] = mapping_parameters

        @builtins.property
        def record_format_type(self) -> builtins.str:
            '''``CfnApplication.RecordFormatProperty.RecordFormatType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-recordformat.html#cfn-kinesisanalytics-application-recordformat-recordformattype
            '''
            result = self._values.get("record_format_type")
            assert result is not None, "Required property 'record_format_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def mapping_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnApplication.MappingParametersProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplication.RecordFormatProperty.MappingParameters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-recordformat.html#cfn-kinesisanalytics-application-recordformat-mappingparameters
            '''
            result = self._values.get("mapping_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnApplication.MappingParametersProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecordFormatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnApplicationCloudWatchLoggingOptionV2(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationCloudWatchLoggingOptionV2",
):
    '''A CloudFormation ``AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption``.

    :cloudformationResource: AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationcloudwatchloggingoption.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_name: builtins.str,
        cloud_watch_logging_option: typing.Union["CfnApplicationCloudWatchLoggingOptionV2.CloudWatchLoggingOptionProperty", _IResolvable_a771d0ef],
    ) -> None:
        '''Create a new ``AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_name: ``AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption.ApplicationName``.
        :param cloud_watch_logging_option: ``AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption.CloudWatchLoggingOption``.
        '''
        props = CfnApplicationCloudWatchLoggingOptionV2Props(
            application_name=application_name,
            cloud_watch_logging_option=cloud_watch_logging_option,
        )

        jsii.create(CfnApplicationCloudWatchLoggingOptionV2, self, [scope, id, props])

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
        '''``AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption.ApplicationName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationcloudwatchloggingoption.html#cfn-kinesisanalyticsv2-applicationcloudwatchloggingoption-applicationname
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))

    @application_name.setter
    def application_name(self, value: builtins.str) -> None:
        jsii.set(self, "applicationName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cloudWatchLoggingOption")
    def cloud_watch_logging_option(
        self,
    ) -> typing.Union["CfnApplicationCloudWatchLoggingOptionV2.CloudWatchLoggingOptionProperty", _IResolvable_a771d0ef]:
        '''``AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption.CloudWatchLoggingOption``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationcloudwatchloggingoption.html#cfn-kinesisanalyticsv2-applicationcloudwatchloggingoption-cloudwatchloggingoption
        '''
        return typing.cast(typing.Union["CfnApplicationCloudWatchLoggingOptionV2.CloudWatchLoggingOptionProperty", _IResolvable_a771d0ef], jsii.get(self, "cloudWatchLoggingOption"))

    @cloud_watch_logging_option.setter
    def cloud_watch_logging_option(
        self,
        value: typing.Union["CfnApplicationCloudWatchLoggingOptionV2.CloudWatchLoggingOptionProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "cloudWatchLoggingOption", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationCloudWatchLoggingOptionV2.CloudWatchLoggingOptionProperty",
        jsii_struct_bases=[],
        name_mapping={"log_stream_arn": "logStreamArn"},
    )
    class CloudWatchLoggingOptionProperty:
        def __init__(self, *, log_stream_arn: builtins.str) -> None:
            '''
            :param log_stream_arn: ``CfnApplicationCloudWatchLoggingOptionV2.CloudWatchLoggingOptionProperty.LogStreamARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationcloudwatchloggingoption-cloudwatchloggingoption.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "log_stream_arn": log_stream_arn,
            }

        @builtins.property
        def log_stream_arn(self) -> builtins.str:
            '''``CfnApplicationCloudWatchLoggingOptionV2.CloudWatchLoggingOptionProperty.LogStreamARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationcloudwatchloggingoption-cloudwatchloggingoption.html#cfn-kinesisanalyticsv2-applicationcloudwatchloggingoption-cloudwatchloggingoption-logstreamarn
            '''
            result = self._values.get("log_stream_arn")
            assert result is not None, "Required property 'log_stream_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLoggingOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationCloudWatchLoggingOptionV2Props",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "cloud_watch_logging_option": "cloudWatchLoggingOption",
    },
)
class CfnApplicationCloudWatchLoggingOptionV2Props:
    def __init__(
        self,
        *,
        application_name: builtins.str,
        cloud_watch_logging_option: typing.Union[CfnApplicationCloudWatchLoggingOptionV2.CloudWatchLoggingOptionProperty, _IResolvable_a771d0ef],
    ) -> None:
        '''Properties for defining a ``AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption``.

        :param application_name: ``AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption.ApplicationName``.
        :param cloud_watch_logging_option: ``AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption.CloudWatchLoggingOption``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationcloudwatchloggingoption.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "application_name": application_name,
            "cloud_watch_logging_option": cloud_watch_logging_option,
        }

    @builtins.property
    def application_name(self) -> builtins.str:
        '''``AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption.ApplicationName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationcloudwatchloggingoption.html#cfn-kinesisanalyticsv2-applicationcloudwatchloggingoption-applicationname
        '''
        result = self._values.get("application_name")
        assert result is not None, "Required property 'application_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_watch_logging_option(
        self,
    ) -> typing.Union[CfnApplicationCloudWatchLoggingOptionV2.CloudWatchLoggingOptionProperty, _IResolvable_a771d0ef]:
        '''``AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption.CloudWatchLoggingOption``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationcloudwatchloggingoption.html#cfn-kinesisanalyticsv2-applicationcloudwatchloggingoption-cloudwatchloggingoption
        '''
        result = self._values.get("cloud_watch_logging_option")
        assert result is not None, "Required property 'cloud_watch_logging_option' is missing"
        return typing.cast(typing.Union[CfnApplicationCloudWatchLoggingOptionV2.CloudWatchLoggingOptionProperty, _IResolvable_a771d0ef], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationCloudWatchLoggingOptionV2Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnApplicationOutput(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationOutput",
):
    '''A CloudFormation ``AWS::KinesisAnalytics::ApplicationOutput``.

    :cloudformationResource: AWS::KinesisAnalytics::ApplicationOutput
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationoutput.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_name: builtins.str,
        output: typing.Union["CfnApplicationOutput.OutputProperty", _IResolvable_a771d0ef],
    ) -> None:
        '''Create a new ``AWS::KinesisAnalytics::ApplicationOutput``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_name: ``AWS::KinesisAnalytics::ApplicationOutput.ApplicationName``.
        :param output: ``AWS::KinesisAnalytics::ApplicationOutput.Output``.
        '''
        props = CfnApplicationOutputProps(
            application_name=application_name, output=output
        )

        jsii.create(CfnApplicationOutput, self, [scope, id, props])

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
        '''``AWS::KinesisAnalytics::ApplicationOutput.ApplicationName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationoutput.html#cfn-kinesisanalytics-applicationoutput-applicationname
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))

    @application_name.setter
    def application_name(self, value: builtins.str) -> None:
        jsii.set(self, "applicationName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="output")
    def output(
        self,
    ) -> typing.Union["CfnApplicationOutput.OutputProperty", _IResolvable_a771d0ef]:
        '''``AWS::KinesisAnalytics::ApplicationOutput.Output``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationoutput.html#cfn-kinesisanalytics-applicationoutput-output
        '''
        return typing.cast(typing.Union["CfnApplicationOutput.OutputProperty", _IResolvable_a771d0ef], jsii.get(self, "output"))

    @output.setter
    def output(
        self,
        value: typing.Union["CfnApplicationOutput.OutputProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "output", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationOutput.DestinationSchemaProperty",
        jsii_struct_bases=[],
        name_mapping={"record_format_type": "recordFormatType"},
    )
    class DestinationSchemaProperty:
        def __init__(
            self,
            *,
            record_format_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param record_format_type: ``CfnApplicationOutput.DestinationSchemaProperty.RecordFormatType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-destinationschema.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if record_format_type is not None:
                self._values["record_format_type"] = record_format_type

        @builtins.property
        def record_format_type(self) -> typing.Optional[builtins.str]:
            '''``CfnApplicationOutput.DestinationSchemaProperty.RecordFormatType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-destinationschema.html#cfn-kinesisanalytics-applicationoutput-destinationschema-recordformattype
            '''
            result = self._values.get("record_format_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationSchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationOutput.KinesisFirehoseOutputProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
    )
    class KinesisFirehoseOutputProperty:
        def __init__(
            self,
            *,
            resource_arn: builtins.str,
            role_arn: builtins.str,
        ) -> None:
            '''
            :param resource_arn: ``CfnApplicationOutput.KinesisFirehoseOutputProperty.ResourceARN``.
            :param role_arn: ``CfnApplicationOutput.KinesisFirehoseOutputProperty.RoleARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-kinesisfirehoseoutput.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "resource_arn": resource_arn,
                "role_arn": role_arn,
            }

        @builtins.property
        def resource_arn(self) -> builtins.str:
            '''``CfnApplicationOutput.KinesisFirehoseOutputProperty.ResourceARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-kinesisfirehoseoutput.html#cfn-kinesisanalytics-applicationoutput-kinesisfirehoseoutput-resourcearn
            '''
            result = self._values.get("resource_arn")
            assert result is not None, "Required property 'resource_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def role_arn(self) -> builtins.str:
            '''``CfnApplicationOutput.KinesisFirehoseOutputProperty.RoleARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-kinesisfirehoseoutput.html#cfn-kinesisanalytics-applicationoutput-kinesisfirehoseoutput-rolearn
            '''
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisFirehoseOutputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationOutput.KinesisStreamsOutputProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
    )
    class KinesisStreamsOutputProperty:
        def __init__(
            self,
            *,
            resource_arn: builtins.str,
            role_arn: builtins.str,
        ) -> None:
            '''
            :param resource_arn: ``CfnApplicationOutput.KinesisStreamsOutputProperty.ResourceARN``.
            :param role_arn: ``CfnApplicationOutput.KinesisStreamsOutputProperty.RoleARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-kinesisstreamsoutput.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "resource_arn": resource_arn,
                "role_arn": role_arn,
            }

        @builtins.property
        def resource_arn(self) -> builtins.str:
            '''``CfnApplicationOutput.KinesisStreamsOutputProperty.ResourceARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-kinesisstreamsoutput.html#cfn-kinesisanalytics-applicationoutput-kinesisstreamsoutput-resourcearn
            '''
            result = self._values.get("resource_arn")
            assert result is not None, "Required property 'resource_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def role_arn(self) -> builtins.str:
            '''``CfnApplicationOutput.KinesisStreamsOutputProperty.RoleARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-kinesisstreamsoutput.html#cfn-kinesisanalytics-applicationoutput-kinesisstreamsoutput-rolearn
            '''
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisStreamsOutputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationOutput.LambdaOutputProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
    )
    class LambdaOutputProperty:
        def __init__(
            self,
            *,
            resource_arn: builtins.str,
            role_arn: builtins.str,
        ) -> None:
            '''
            :param resource_arn: ``CfnApplicationOutput.LambdaOutputProperty.ResourceARN``.
            :param role_arn: ``CfnApplicationOutput.LambdaOutputProperty.RoleARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-lambdaoutput.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "resource_arn": resource_arn,
                "role_arn": role_arn,
            }

        @builtins.property
        def resource_arn(self) -> builtins.str:
            '''``CfnApplicationOutput.LambdaOutputProperty.ResourceARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-lambdaoutput.html#cfn-kinesisanalytics-applicationoutput-lambdaoutput-resourcearn
            '''
            result = self._values.get("resource_arn")
            assert result is not None, "Required property 'resource_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def role_arn(self) -> builtins.str:
            '''``CfnApplicationOutput.LambdaOutputProperty.RoleARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-lambdaoutput.html#cfn-kinesisanalytics-applicationoutput-lambdaoutput-rolearn
            '''
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaOutputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationOutput.OutputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_schema": "destinationSchema",
            "kinesis_firehose_output": "kinesisFirehoseOutput",
            "kinesis_streams_output": "kinesisStreamsOutput",
            "lambda_output": "lambdaOutput",
            "name": "name",
        },
    )
    class OutputProperty:
        def __init__(
            self,
            *,
            destination_schema: typing.Union["CfnApplicationOutput.DestinationSchemaProperty", _IResolvable_a771d0ef],
            kinesis_firehose_output: typing.Optional[typing.Union["CfnApplicationOutput.KinesisFirehoseOutputProperty", _IResolvable_a771d0ef]] = None,
            kinesis_streams_output: typing.Optional[typing.Union["CfnApplicationOutput.KinesisStreamsOutputProperty", _IResolvable_a771d0ef]] = None,
            lambda_output: typing.Optional[typing.Union["CfnApplicationOutput.LambdaOutputProperty", _IResolvable_a771d0ef]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param destination_schema: ``CfnApplicationOutput.OutputProperty.DestinationSchema``.
            :param kinesis_firehose_output: ``CfnApplicationOutput.OutputProperty.KinesisFirehoseOutput``.
            :param kinesis_streams_output: ``CfnApplicationOutput.OutputProperty.KinesisStreamsOutput``.
            :param lambda_output: ``CfnApplicationOutput.OutputProperty.LambdaOutput``.
            :param name: ``CfnApplicationOutput.OutputProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-output.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "destination_schema": destination_schema,
            }
            if kinesis_firehose_output is not None:
                self._values["kinesis_firehose_output"] = kinesis_firehose_output
            if kinesis_streams_output is not None:
                self._values["kinesis_streams_output"] = kinesis_streams_output
            if lambda_output is not None:
                self._values["lambda_output"] = lambda_output
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def destination_schema(
            self,
        ) -> typing.Union["CfnApplicationOutput.DestinationSchemaProperty", _IResolvable_a771d0ef]:
            '''``CfnApplicationOutput.OutputProperty.DestinationSchema``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-output.html#cfn-kinesisanalytics-applicationoutput-output-destinationschema
            '''
            result = self._values.get("destination_schema")
            assert result is not None, "Required property 'destination_schema' is missing"
            return typing.cast(typing.Union["CfnApplicationOutput.DestinationSchemaProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def kinesis_firehose_output(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationOutput.KinesisFirehoseOutputProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationOutput.OutputProperty.KinesisFirehoseOutput``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-output.html#cfn-kinesisanalytics-applicationoutput-output-kinesisfirehoseoutput
            '''
            result = self._values.get("kinesis_firehose_output")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationOutput.KinesisFirehoseOutputProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def kinesis_streams_output(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationOutput.KinesisStreamsOutputProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationOutput.OutputProperty.KinesisStreamsOutput``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-output.html#cfn-kinesisanalytics-applicationoutput-output-kinesisstreamsoutput
            '''
            result = self._values.get("kinesis_streams_output")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationOutput.KinesisStreamsOutputProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def lambda_output(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationOutput.LambdaOutputProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationOutput.OutputProperty.LambdaOutput``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-output.html#cfn-kinesisanalytics-applicationoutput-output-lambdaoutput
            '''
            result = self._values.get("lambda_output")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationOutput.LambdaOutputProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''``CfnApplicationOutput.OutputProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-output.html#cfn-kinesisanalytics-applicationoutput-output-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationOutputProps",
    jsii_struct_bases=[],
    name_mapping={"application_name": "applicationName", "output": "output"},
)
class CfnApplicationOutputProps:
    def __init__(
        self,
        *,
        application_name: builtins.str,
        output: typing.Union[CfnApplicationOutput.OutputProperty, _IResolvable_a771d0ef],
    ) -> None:
        '''Properties for defining a ``AWS::KinesisAnalytics::ApplicationOutput``.

        :param application_name: ``AWS::KinesisAnalytics::ApplicationOutput.ApplicationName``.
        :param output: ``AWS::KinesisAnalytics::ApplicationOutput.Output``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationoutput.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "application_name": application_name,
            "output": output,
        }

    @builtins.property
    def application_name(self) -> builtins.str:
        '''``AWS::KinesisAnalytics::ApplicationOutput.ApplicationName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationoutput.html#cfn-kinesisanalytics-applicationoutput-applicationname
        '''
        result = self._values.get("application_name")
        assert result is not None, "Required property 'application_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def output(
        self,
    ) -> typing.Union[CfnApplicationOutput.OutputProperty, _IResolvable_a771d0ef]:
        '''``AWS::KinesisAnalytics::ApplicationOutput.Output``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationoutput.html#cfn-kinesisanalytics-applicationoutput-output
        '''
        result = self._values.get("output")
        assert result is not None, "Required property 'output' is missing"
        return typing.cast(typing.Union[CfnApplicationOutput.OutputProperty, _IResolvable_a771d0ef], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationOutputProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnApplicationOutputV2(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationOutputV2",
):
    '''A CloudFormation ``AWS::KinesisAnalyticsV2::ApplicationOutput``.

    :cloudformationResource: AWS::KinesisAnalyticsV2::ApplicationOutput
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationoutput.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_name: builtins.str,
        output: typing.Union["CfnApplicationOutputV2.OutputProperty", _IResolvable_a771d0ef],
    ) -> None:
        '''Create a new ``AWS::KinesisAnalyticsV2::ApplicationOutput``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_name: ``AWS::KinesisAnalyticsV2::ApplicationOutput.ApplicationName``.
        :param output: ``AWS::KinesisAnalyticsV2::ApplicationOutput.Output``.
        '''
        props = CfnApplicationOutputV2Props(
            application_name=application_name, output=output
        )

        jsii.create(CfnApplicationOutputV2, self, [scope, id, props])

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
        '''``AWS::KinesisAnalyticsV2::ApplicationOutput.ApplicationName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationoutput.html#cfn-kinesisanalyticsv2-applicationoutput-applicationname
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))

    @application_name.setter
    def application_name(self, value: builtins.str) -> None:
        jsii.set(self, "applicationName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="output")
    def output(
        self,
    ) -> typing.Union["CfnApplicationOutputV2.OutputProperty", _IResolvable_a771d0ef]:
        '''``AWS::KinesisAnalyticsV2::ApplicationOutput.Output``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationoutput.html#cfn-kinesisanalyticsv2-applicationoutput-output
        '''
        return typing.cast(typing.Union["CfnApplicationOutputV2.OutputProperty", _IResolvable_a771d0ef], jsii.get(self, "output"))

    @output.setter
    def output(
        self,
        value: typing.Union["CfnApplicationOutputV2.OutputProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "output", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationOutputV2.DestinationSchemaProperty",
        jsii_struct_bases=[],
        name_mapping={"record_format_type": "recordFormatType"},
    )
    class DestinationSchemaProperty:
        def __init__(
            self,
            *,
            record_format_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param record_format_type: ``CfnApplicationOutputV2.DestinationSchemaProperty.RecordFormatType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-destinationschema.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if record_format_type is not None:
                self._values["record_format_type"] = record_format_type

        @builtins.property
        def record_format_type(self) -> typing.Optional[builtins.str]:
            '''``CfnApplicationOutputV2.DestinationSchemaProperty.RecordFormatType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-destinationschema.html#cfn-kinesisanalyticsv2-applicationoutput-destinationschema-recordformattype
            '''
            result = self._values.get("record_format_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationSchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationOutputV2.KinesisFirehoseOutputProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn"},
    )
    class KinesisFirehoseOutputProperty:
        def __init__(self, *, resource_arn: builtins.str) -> None:
            '''
            :param resource_arn: ``CfnApplicationOutputV2.KinesisFirehoseOutputProperty.ResourceARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-kinesisfirehoseoutput.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "resource_arn": resource_arn,
            }

        @builtins.property
        def resource_arn(self) -> builtins.str:
            '''``CfnApplicationOutputV2.KinesisFirehoseOutputProperty.ResourceARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-kinesisfirehoseoutput.html#cfn-kinesisanalyticsv2-applicationoutput-kinesisfirehoseoutput-resourcearn
            '''
            result = self._values.get("resource_arn")
            assert result is not None, "Required property 'resource_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisFirehoseOutputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationOutputV2.KinesisStreamsOutputProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn"},
    )
    class KinesisStreamsOutputProperty:
        def __init__(self, *, resource_arn: builtins.str) -> None:
            '''
            :param resource_arn: ``CfnApplicationOutputV2.KinesisStreamsOutputProperty.ResourceARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-kinesisstreamsoutput.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "resource_arn": resource_arn,
            }

        @builtins.property
        def resource_arn(self) -> builtins.str:
            '''``CfnApplicationOutputV2.KinesisStreamsOutputProperty.ResourceARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-kinesisstreamsoutput.html#cfn-kinesisanalyticsv2-applicationoutput-kinesisstreamsoutput-resourcearn
            '''
            result = self._values.get("resource_arn")
            assert result is not None, "Required property 'resource_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisStreamsOutputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationOutputV2.LambdaOutputProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn"},
    )
    class LambdaOutputProperty:
        def __init__(self, *, resource_arn: builtins.str) -> None:
            '''
            :param resource_arn: ``CfnApplicationOutputV2.LambdaOutputProperty.ResourceARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-lambdaoutput.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "resource_arn": resource_arn,
            }

        @builtins.property
        def resource_arn(self) -> builtins.str:
            '''``CfnApplicationOutputV2.LambdaOutputProperty.ResourceARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-lambdaoutput.html#cfn-kinesisanalyticsv2-applicationoutput-lambdaoutput-resourcearn
            '''
            result = self._values.get("resource_arn")
            assert result is not None, "Required property 'resource_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaOutputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationOutputV2.OutputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_schema": "destinationSchema",
            "kinesis_firehose_output": "kinesisFirehoseOutput",
            "kinesis_streams_output": "kinesisStreamsOutput",
            "lambda_output": "lambdaOutput",
            "name": "name",
        },
    )
    class OutputProperty:
        def __init__(
            self,
            *,
            destination_schema: typing.Union["CfnApplicationOutputV2.DestinationSchemaProperty", _IResolvable_a771d0ef],
            kinesis_firehose_output: typing.Optional[typing.Union["CfnApplicationOutputV2.KinesisFirehoseOutputProperty", _IResolvable_a771d0ef]] = None,
            kinesis_streams_output: typing.Optional[typing.Union["CfnApplicationOutputV2.KinesisStreamsOutputProperty", _IResolvable_a771d0ef]] = None,
            lambda_output: typing.Optional[typing.Union["CfnApplicationOutputV2.LambdaOutputProperty", _IResolvable_a771d0ef]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param destination_schema: ``CfnApplicationOutputV2.OutputProperty.DestinationSchema``.
            :param kinesis_firehose_output: ``CfnApplicationOutputV2.OutputProperty.KinesisFirehoseOutput``.
            :param kinesis_streams_output: ``CfnApplicationOutputV2.OutputProperty.KinesisStreamsOutput``.
            :param lambda_output: ``CfnApplicationOutputV2.OutputProperty.LambdaOutput``.
            :param name: ``CfnApplicationOutputV2.OutputProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-output.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "destination_schema": destination_schema,
            }
            if kinesis_firehose_output is not None:
                self._values["kinesis_firehose_output"] = kinesis_firehose_output
            if kinesis_streams_output is not None:
                self._values["kinesis_streams_output"] = kinesis_streams_output
            if lambda_output is not None:
                self._values["lambda_output"] = lambda_output
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def destination_schema(
            self,
        ) -> typing.Union["CfnApplicationOutputV2.DestinationSchemaProperty", _IResolvable_a771d0ef]:
            '''``CfnApplicationOutputV2.OutputProperty.DestinationSchema``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-output.html#cfn-kinesisanalyticsv2-applicationoutput-output-destinationschema
            '''
            result = self._values.get("destination_schema")
            assert result is not None, "Required property 'destination_schema' is missing"
            return typing.cast(typing.Union["CfnApplicationOutputV2.DestinationSchemaProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def kinesis_firehose_output(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationOutputV2.KinesisFirehoseOutputProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationOutputV2.OutputProperty.KinesisFirehoseOutput``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-output.html#cfn-kinesisanalyticsv2-applicationoutput-output-kinesisfirehoseoutput
            '''
            result = self._values.get("kinesis_firehose_output")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationOutputV2.KinesisFirehoseOutputProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def kinesis_streams_output(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationOutputV2.KinesisStreamsOutputProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationOutputV2.OutputProperty.KinesisStreamsOutput``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-output.html#cfn-kinesisanalyticsv2-applicationoutput-output-kinesisstreamsoutput
            '''
            result = self._values.get("kinesis_streams_output")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationOutputV2.KinesisStreamsOutputProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def lambda_output(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationOutputV2.LambdaOutputProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationOutputV2.OutputProperty.LambdaOutput``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-output.html#cfn-kinesisanalyticsv2-applicationoutput-output-lambdaoutput
            '''
            result = self._values.get("lambda_output")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationOutputV2.LambdaOutputProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''``CfnApplicationOutputV2.OutputProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-output.html#cfn-kinesisanalyticsv2-applicationoutput-output-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationOutputV2Props",
    jsii_struct_bases=[],
    name_mapping={"application_name": "applicationName", "output": "output"},
)
class CfnApplicationOutputV2Props:
    def __init__(
        self,
        *,
        application_name: builtins.str,
        output: typing.Union[CfnApplicationOutputV2.OutputProperty, _IResolvable_a771d0ef],
    ) -> None:
        '''Properties for defining a ``AWS::KinesisAnalyticsV2::ApplicationOutput``.

        :param application_name: ``AWS::KinesisAnalyticsV2::ApplicationOutput.ApplicationName``.
        :param output: ``AWS::KinesisAnalyticsV2::ApplicationOutput.Output``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationoutput.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "application_name": application_name,
            "output": output,
        }

    @builtins.property
    def application_name(self) -> builtins.str:
        '''``AWS::KinesisAnalyticsV2::ApplicationOutput.ApplicationName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationoutput.html#cfn-kinesisanalyticsv2-applicationoutput-applicationname
        '''
        result = self._values.get("application_name")
        assert result is not None, "Required property 'application_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def output(
        self,
    ) -> typing.Union[CfnApplicationOutputV2.OutputProperty, _IResolvable_a771d0ef]:
        '''``AWS::KinesisAnalyticsV2::ApplicationOutput.Output``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationoutput.html#cfn-kinesisanalyticsv2-applicationoutput-output
        '''
        result = self._values.get("output")
        assert result is not None, "Required property 'output' is missing"
        return typing.cast(typing.Union[CfnApplicationOutputV2.OutputProperty, _IResolvable_a771d0ef], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationOutputV2Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "inputs": "inputs",
        "application_code": "applicationCode",
        "application_description": "applicationDescription",
        "application_name": "applicationName",
    },
)
class CfnApplicationProps:
    def __init__(
        self,
        *,
        inputs: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnApplication.InputProperty, _IResolvable_a771d0ef]]],
        application_code: typing.Optional[builtins.str] = None,
        application_description: typing.Optional[builtins.str] = None,
        application_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::KinesisAnalytics::Application``.

        :param inputs: ``AWS::KinesisAnalytics::Application.Inputs``.
        :param application_code: ``AWS::KinesisAnalytics::Application.ApplicationCode``.
        :param application_description: ``AWS::KinesisAnalytics::Application.ApplicationDescription``.
        :param application_name: ``AWS::KinesisAnalytics::Application.ApplicationName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "inputs": inputs,
        }
        if application_code is not None:
            self._values["application_code"] = application_code
        if application_description is not None:
            self._values["application_description"] = application_description
        if application_name is not None:
            self._values["application_name"] = application_name

    @builtins.property
    def inputs(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnApplication.InputProperty, _IResolvable_a771d0ef]]]:
        '''``AWS::KinesisAnalytics::Application.Inputs``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html#cfn-kinesisanalytics-application-inputs
        '''
        result = self._values.get("inputs")
        assert result is not None, "Required property 'inputs' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnApplication.InputProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def application_code(self) -> typing.Optional[builtins.str]:
        '''``AWS::KinesisAnalytics::Application.ApplicationCode``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html#cfn-kinesisanalytics-application-applicationcode
        '''
        result = self._values.get("application_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_description(self) -> typing.Optional[builtins.str]:
        '''``AWS::KinesisAnalytics::Application.ApplicationDescription``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html#cfn-kinesisanalytics-application-applicationdescription
        '''
        result = self._values.get("application_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::KinesisAnalytics::Application.ApplicationName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html#cfn-kinesisanalytics-application-applicationname
        '''
        result = self._values.get("application_name")
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
class CfnApplicationReferenceDataSource(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationReferenceDataSource",
):
    '''A CloudFormation ``AWS::KinesisAnalytics::ApplicationReferenceDataSource``.

    :cloudformationResource: AWS::KinesisAnalytics::ApplicationReferenceDataSource
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationreferencedatasource.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_name: builtins.str,
        reference_data_source: typing.Union["CfnApplicationReferenceDataSource.ReferenceDataSourceProperty", _IResolvable_a771d0ef],
    ) -> None:
        '''Create a new ``AWS::KinesisAnalytics::ApplicationReferenceDataSource``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_name: ``AWS::KinesisAnalytics::ApplicationReferenceDataSource.ApplicationName``.
        :param reference_data_source: ``AWS::KinesisAnalytics::ApplicationReferenceDataSource.ReferenceDataSource``.
        '''
        props = CfnApplicationReferenceDataSourceProps(
            application_name=application_name,
            reference_data_source=reference_data_source,
        )

        jsii.create(CfnApplicationReferenceDataSource, self, [scope, id, props])

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
        '''``AWS::KinesisAnalytics::ApplicationReferenceDataSource.ApplicationName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationreferencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-applicationname
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))

    @application_name.setter
    def application_name(self, value: builtins.str) -> None:
        jsii.set(self, "applicationName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="referenceDataSource")
    def reference_data_source(
        self,
    ) -> typing.Union["CfnApplicationReferenceDataSource.ReferenceDataSourceProperty", _IResolvable_a771d0ef]:
        '''``AWS::KinesisAnalytics::ApplicationReferenceDataSource.ReferenceDataSource``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationreferencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-referencedatasource
        '''
        return typing.cast(typing.Union["CfnApplicationReferenceDataSource.ReferenceDataSourceProperty", _IResolvable_a771d0ef], jsii.get(self, "referenceDataSource"))

    @reference_data_source.setter
    def reference_data_source(
        self,
        value: typing.Union["CfnApplicationReferenceDataSource.ReferenceDataSourceProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "referenceDataSource", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationReferenceDataSource.CSVMappingParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "record_column_delimiter": "recordColumnDelimiter",
            "record_row_delimiter": "recordRowDelimiter",
        },
    )
    class CSVMappingParametersProperty:
        def __init__(
            self,
            *,
            record_column_delimiter: builtins.str,
            record_row_delimiter: builtins.str,
        ) -> None:
            '''
            :param record_column_delimiter: ``CfnApplicationReferenceDataSource.CSVMappingParametersProperty.RecordColumnDelimiter``.
            :param record_row_delimiter: ``CfnApplicationReferenceDataSource.CSVMappingParametersProperty.RecordRowDelimiter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-csvmappingparameters.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "record_column_delimiter": record_column_delimiter,
                "record_row_delimiter": record_row_delimiter,
            }

        @builtins.property
        def record_column_delimiter(self) -> builtins.str:
            '''``CfnApplicationReferenceDataSource.CSVMappingParametersProperty.RecordColumnDelimiter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-csvmappingparameters.html#cfn-kinesisanalytics-applicationreferencedatasource-csvmappingparameters-recordcolumndelimiter
            '''
            result = self._values.get("record_column_delimiter")
            assert result is not None, "Required property 'record_column_delimiter' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def record_row_delimiter(self) -> builtins.str:
            '''``CfnApplicationReferenceDataSource.CSVMappingParametersProperty.RecordRowDelimiter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-csvmappingparameters.html#cfn-kinesisanalytics-applicationreferencedatasource-csvmappingparameters-recordrowdelimiter
            '''
            result = self._values.get("record_row_delimiter")
            assert result is not None, "Required property 'record_row_delimiter' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CSVMappingParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationReferenceDataSource.JSONMappingParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"record_row_path": "recordRowPath"},
    )
    class JSONMappingParametersProperty:
        def __init__(self, *, record_row_path: builtins.str) -> None:
            '''
            :param record_row_path: ``CfnApplicationReferenceDataSource.JSONMappingParametersProperty.RecordRowPath``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-jsonmappingparameters.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "record_row_path": record_row_path,
            }

        @builtins.property
        def record_row_path(self) -> builtins.str:
            '''``CfnApplicationReferenceDataSource.JSONMappingParametersProperty.RecordRowPath``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-jsonmappingparameters.html#cfn-kinesisanalytics-applicationreferencedatasource-jsonmappingparameters-recordrowpath
            '''
            result = self._values.get("record_row_path")
            assert result is not None, "Required property 'record_row_path' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JSONMappingParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationReferenceDataSource.MappingParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "csv_mapping_parameters": "csvMappingParameters",
            "json_mapping_parameters": "jsonMappingParameters",
        },
    )
    class MappingParametersProperty:
        def __init__(
            self,
            *,
            csv_mapping_parameters: typing.Optional[typing.Union["CfnApplicationReferenceDataSource.CSVMappingParametersProperty", _IResolvable_a771d0ef]] = None,
            json_mapping_parameters: typing.Optional[typing.Union["CfnApplicationReferenceDataSource.JSONMappingParametersProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param csv_mapping_parameters: ``CfnApplicationReferenceDataSource.MappingParametersProperty.CSVMappingParameters``.
            :param json_mapping_parameters: ``CfnApplicationReferenceDataSource.MappingParametersProperty.JSONMappingParameters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-mappingparameters.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if csv_mapping_parameters is not None:
                self._values["csv_mapping_parameters"] = csv_mapping_parameters
            if json_mapping_parameters is not None:
                self._values["json_mapping_parameters"] = json_mapping_parameters

        @builtins.property
        def csv_mapping_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationReferenceDataSource.CSVMappingParametersProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationReferenceDataSource.MappingParametersProperty.CSVMappingParameters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-mappingparameters.html#cfn-kinesisanalytics-applicationreferencedatasource-mappingparameters-csvmappingparameters
            '''
            result = self._values.get("csv_mapping_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationReferenceDataSource.CSVMappingParametersProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def json_mapping_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationReferenceDataSource.JSONMappingParametersProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationReferenceDataSource.MappingParametersProperty.JSONMappingParameters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-mappingparameters.html#cfn-kinesisanalytics-applicationreferencedatasource-mappingparameters-jsonmappingparameters
            '''
            result = self._values.get("json_mapping_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationReferenceDataSource.JSONMappingParametersProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MappingParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationReferenceDataSource.RecordColumnProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "sql_type": "sqlType", "mapping": "mapping"},
    )
    class RecordColumnProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            sql_type: builtins.str,
            mapping: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param name: ``CfnApplicationReferenceDataSource.RecordColumnProperty.Name``.
            :param sql_type: ``CfnApplicationReferenceDataSource.RecordColumnProperty.SqlType``.
            :param mapping: ``CfnApplicationReferenceDataSource.RecordColumnProperty.Mapping``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-recordcolumn.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "sql_type": sql_type,
            }
            if mapping is not None:
                self._values["mapping"] = mapping

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnApplicationReferenceDataSource.RecordColumnProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-recordcolumn.html#cfn-kinesisanalytics-applicationreferencedatasource-recordcolumn-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def sql_type(self) -> builtins.str:
            '''``CfnApplicationReferenceDataSource.RecordColumnProperty.SqlType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-recordcolumn.html#cfn-kinesisanalytics-applicationreferencedatasource-recordcolumn-sqltype
            '''
            result = self._values.get("sql_type")
            assert result is not None, "Required property 'sql_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def mapping(self) -> typing.Optional[builtins.str]:
            '''``CfnApplicationReferenceDataSource.RecordColumnProperty.Mapping``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-recordcolumn.html#cfn-kinesisanalytics-applicationreferencedatasource-recordcolumn-mapping
            '''
            result = self._values.get("mapping")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecordColumnProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationReferenceDataSource.RecordFormatProperty",
        jsii_struct_bases=[],
        name_mapping={
            "record_format_type": "recordFormatType",
            "mapping_parameters": "mappingParameters",
        },
    )
    class RecordFormatProperty:
        def __init__(
            self,
            *,
            record_format_type: builtins.str,
            mapping_parameters: typing.Optional[typing.Union["CfnApplicationReferenceDataSource.MappingParametersProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param record_format_type: ``CfnApplicationReferenceDataSource.RecordFormatProperty.RecordFormatType``.
            :param mapping_parameters: ``CfnApplicationReferenceDataSource.RecordFormatProperty.MappingParameters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-recordformat.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "record_format_type": record_format_type,
            }
            if mapping_parameters is not None:
                self._values["mapping_parameters"] = mapping_parameters

        @builtins.property
        def record_format_type(self) -> builtins.str:
            '''``CfnApplicationReferenceDataSource.RecordFormatProperty.RecordFormatType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-recordformat.html#cfn-kinesisanalytics-applicationreferencedatasource-recordformat-recordformattype
            '''
            result = self._values.get("record_format_type")
            assert result is not None, "Required property 'record_format_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def mapping_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationReferenceDataSource.MappingParametersProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationReferenceDataSource.RecordFormatProperty.MappingParameters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-recordformat.html#cfn-kinesisanalytics-applicationreferencedatasource-recordformat-mappingparameters
            '''
            result = self._values.get("mapping_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationReferenceDataSource.MappingParametersProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecordFormatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationReferenceDataSource.ReferenceDataSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "reference_schema": "referenceSchema",
            "s3_reference_data_source": "s3ReferenceDataSource",
            "table_name": "tableName",
        },
    )
    class ReferenceDataSourceProperty:
        def __init__(
            self,
            *,
            reference_schema: typing.Union["CfnApplicationReferenceDataSource.ReferenceSchemaProperty", _IResolvable_a771d0ef],
            s3_reference_data_source: typing.Optional[typing.Union["CfnApplicationReferenceDataSource.S3ReferenceDataSourceProperty", _IResolvable_a771d0ef]] = None,
            table_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param reference_schema: ``CfnApplicationReferenceDataSource.ReferenceDataSourceProperty.ReferenceSchema``.
            :param s3_reference_data_source: ``CfnApplicationReferenceDataSource.ReferenceDataSourceProperty.S3ReferenceDataSource``.
            :param table_name: ``CfnApplicationReferenceDataSource.ReferenceDataSourceProperty.TableName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referencedatasource.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "reference_schema": reference_schema,
            }
            if s3_reference_data_source is not None:
                self._values["s3_reference_data_source"] = s3_reference_data_source
            if table_name is not None:
                self._values["table_name"] = table_name

        @builtins.property
        def reference_schema(
            self,
        ) -> typing.Union["CfnApplicationReferenceDataSource.ReferenceSchemaProperty", _IResolvable_a771d0ef]:
            '''``CfnApplicationReferenceDataSource.ReferenceDataSourceProperty.ReferenceSchema``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-referencedatasource-referenceschema
            '''
            result = self._values.get("reference_schema")
            assert result is not None, "Required property 'reference_schema' is missing"
            return typing.cast(typing.Union["CfnApplicationReferenceDataSource.ReferenceSchemaProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def s3_reference_data_source(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationReferenceDataSource.S3ReferenceDataSourceProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationReferenceDataSource.ReferenceDataSourceProperty.S3ReferenceDataSource``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-referencedatasource-s3referencedatasource
            '''
            result = self._values.get("s3_reference_data_source")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationReferenceDataSource.S3ReferenceDataSourceProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''``CfnApplicationReferenceDataSource.ReferenceDataSourceProperty.TableName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-referencedatasource-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReferenceDataSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationReferenceDataSource.ReferenceSchemaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "record_columns": "recordColumns",
            "record_format": "recordFormat",
            "record_encoding": "recordEncoding",
        },
    )
    class ReferenceSchemaProperty:
        def __init__(
            self,
            *,
            record_columns: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplicationReferenceDataSource.RecordColumnProperty", _IResolvable_a771d0ef]]],
            record_format: typing.Union["CfnApplicationReferenceDataSource.RecordFormatProperty", _IResolvable_a771d0ef],
            record_encoding: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param record_columns: ``CfnApplicationReferenceDataSource.ReferenceSchemaProperty.RecordColumns``.
            :param record_format: ``CfnApplicationReferenceDataSource.ReferenceSchemaProperty.RecordFormat``.
            :param record_encoding: ``CfnApplicationReferenceDataSource.ReferenceSchemaProperty.RecordEncoding``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referenceschema.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "record_columns": record_columns,
                "record_format": record_format,
            }
            if record_encoding is not None:
                self._values["record_encoding"] = record_encoding

        @builtins.property
        def record_columns(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplicationReferenceDataSource.RecordColumnProperty", _IResolvable_a771d0ef]]]:
            '''``CfnApplicationReferenceDataSource.ReferenceSchemaProperty.RecordColumns``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referenceschema.html#cfn-kinesisanalytics-applicationreferencedatasource-referenceschema-recordcolumns
            '''
            result = self._values.get("record_columns")
            assert result is not None, "Required property 'record_columns' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplicationReferenceDataSource.RecordColumnProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def record_format(
            self,
        ) -> typing.Union["CfnApplicationReferenceDataSource.RecordFormatProperty", _IResolvable_a771d0ef]:
            '''``CfnApplicationReferenceDataSource.ReferenceSchemaProperty.RecordFormat``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referenceschema.html#cfn-kinesisanalytics-applicationreferencedatasource-referenceschema-recordformat
            '''
            result = self._values.get("record_format")
            assert result is not None, "Required property 'record_format' is missing"
            return typing.cast(typing.Union["CfnApplicationReferenceDataSource.RecordFormatProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def record_encoding(self) -> typing.Optional[builtins.str]:
            '''``CfnApplicationReferenceDataSource.ReferenceSchemaProperty.RecordEncoding``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referenceschema.html#cfn-kinesisanalytics-applicationreferencedatasource-referenceschema-recordencoding
            '''
            result = self._values.get("record_encoding")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReferenceSchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationReferenceDataSource.S3ReferenceDataSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_arn": "bucketArn",
            "file_key": "fileKey",
            "reference_role_arn": "referenceRoleArn",
        },
    )
    class S3ReferenceDataSourceProperty:
        def __init__(
            self,
            *,
            bucket_arn: builtins.str,
            file_key: builtins.str,
            reference_role_arn: builtins.str,
        ) -> None:
            '''
            :param bucket_arn: ``CfnApplicationReferenceDataSource.S3ReferenceDataSourceProperty.BucketARN``.
            :param file_key: ``CfnApplicationReferenceDataSource.S3ReferenceDataSourceProperty.FileKey``.
            :param reference_role_arn: ``CfnApplicationReferenceDataSource.S3ReferenceDataSourceProperty.ReferenceRoleARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-s3referencedatasource.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bucket_arn": bucket_arn,
                "file_key": file_key,
                "reference_role_arn": reference_role_arn,
            }

        @builtins.property
        def bucket_arn(self) -> builtins.str:
            '''``CfnApplicationReferenceDataSource.S3ReferenceDataSourceProperty.BucketARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-s3referencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-s3referencedatasource-bucketarn
            '''
            result = self._values.get("bucket_arn")
            assert result is not None, "Required property 'bucket_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def file_key(self) -> builtins.str:
            '''``CfnApplicationReferenceDataSource.S3ReferenceDataSourceProperty.FileKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-s3referencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-s3referencedatasource-filekey
            '''
            result = self._values.get("file_key")
            assert result is not None, "Required property 'file_key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def reference_role_arn(self) -> builtins.str:
            '''``CfnApplicationReferenceDataSource.S3ReferenceDataSourceProperty.ReferenceRoleARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-s3referencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-s3referencedatasource-referencerolearn
            '''
            result = self._values.get("reference_role_arn")
            assert result is not None, "Required property 'reference_role_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ReferenceDataSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationReferenceDataSourceProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "reference_data_source": "referenceDataSource",
    },
)
class CfnApplicationReferenceDataSourceProps:
    def __init__(
        self,
        *,
        application_name: builtins.str,
        reference_data_source: typing.Union[CfnApplicationReferenceDataSource.ReferenceDataSourceProperty, _IResolvable_a771d0ef],
    ) -> None:
        '''Properties for defining a ``AWS::KinesisAnalytics::ApplicationReferenceDataSource``.

        :param application_name: ``AWS::KinesisAnalytics::ApplicationReferenceDataSource.ApplicationName``.
        :param reference_data_source: ``AWS::KinesisAnalytics::ApplicationReferenceDataSource.ReferenceDataSource``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationreferencedatasource.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "application_name": application_name,
            "reference_data_source": reference_data_source,
        }

    @builtins.property
    def application_name(self) -> builtins.str:
        '''``AWS::KinesisAnalytics::ApplicationReferenceDataSource.ApplicationName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationreferencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-applicationname
        '''
        result = self._values.get("application_name")
        assert result is not None, "Required property 'application_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def reference_data_source(
        self,
    ) -> typing.Union[CfnApplicationReferenceDataSource.ReferenceDataSourceProperty, _IResolvable_a771d0ef]:
        '''``AWS::KinesisAnalytics::ApplicationReferenceDataSource.ReferenceDataSource``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationreferencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-referencedatasource
        '''
        result = self._values.get("reference_data_source")
        assert result is not None, "Required property 'reference_data_source' is missing"
        return typing.cast(typing.Union[CfnApplicationReferenceDataSource.ReferenceDataSourceProperty, _IResolvable_a771d0ef], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationReferenceDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnApplicationReferenceDataSourceV2(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationReferenceDataSourceV2",
):
    '''A CloudFormation ``AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource``.

    :cloudformationResource: AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationreferencedatasource.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_name: builtins.str,
        reference_data_source: typing.Union["CfnApplicationReferenceDataSourceV2.ReferenceDataSourceProperty", _IResolvable_a771d0ef],
    ) -> None:
        '''Create a new ``AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_name: ``AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource.ApplicationName``.
        :param reference_data_source: ``AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource.ReferenceDataSource``.
        '''
        props = CfnApplicationReferenceDataSourceV2Props(
            application_name=application_name,
            reference_data_source=reference_data_source,
        )

        jsii.create(CfnApplicationReferenceDataSourceV2, self, [scope, id, props])

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
        '''``AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource.ApplicationName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationreferencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-applicationname
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))

    @application_name.setter
    def application_name(self, value: builtins.str) -> None:
        jsii.set(self, "applicationName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="referenceDataSource")
    def reference_data_source(
        self,
    ) -> typing.Union["CfnApplicationReferenceDataSourceV2.ReferenceDataSourceProperty", _IResolvable_a771d0ef]:
        '''``AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource.ReferenceDataSource``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationreferencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource
        '''
        return typing.cast(typing.Union["CfnApplicationReferenceDataSourceV2.ReferenceDataSourceProperty", _IResolvable_a771d0ef], jsii.get(self, "referenceDataSource"))

    @reference_data_source.setter
    def reference_data_source(
        self,
        value: typing.Union["CfnApplicationReferenceDataSourceV2.ReferenceDataSourceProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "referenceDataSource", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationReferenceDataSourceV2.CSVMappingParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "record_column_delimiter": "recordColumnDelimiter",
            "record_row_delimiter": "recordRowDelimiter",
        },
    )
    class CSVMappingParametersProperty:
        def __init__(
            self,
            *,
            record_column_delimiter: builtins.str,
            record_row_delimiter: builtins.str,
        ) -> None:
            '''
            :param record_column_delimiter: ``CfnApplicationReferenceDataSourceV2.CSVMappingParametersProperty.RecordColumnDelimiter``.
            :param record_row_delimiter: ``CfnApplicationReferenceDataSourceV2.CSVMappingParametersProperty.RecordRowDelimiter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-csvmappingparameters.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "record_column_delimiter": record_column_delimiter,
                "record_row_delimiter": record_row_delimiter,
            }

        @builtins.property
        def record_column_delimiter(self) -> builtins.str:
            '''``CfnApplicationReferenceDataSourceV2.CSVMappingParametersProperty.RecordColumnDelimiter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-csvmappingparameters.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-csvmappingparameters-recordcolumndelimiter
            '''
            result = self._values.get("record_column_delimiter")
            assert result is not None, "Required property 'record_column_delimiter' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def record_row_delimiter(self) -> builtins.str:
            '''``CfnApplicationReferenceDataSourceV2.CSVMappingParametersProperty.RecordRowDelimiter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-csvmappingparameters.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-csvmappingparameters-recordrowdelimiter
            '''
            result = self._values.get("record_row_delimiter")
            assert result is not None, "Required property 'record_row_delimiter' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CSVMappingParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationReferenceDataSourceV2.JSONMappingParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"record_row_path": "recordRowPath"},
    )
    class JSONMappingParametersProperty:
        def __init__(self, *, record_row_path: builtins.str) -> None:
            '''
            :param record_row_path: ``CfnApplicationReferenceDataSourceV2.JSONMappingParametersProperty.RecordRowPath``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-jsonmappingparameters.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "record_row_path": record_row_path,
            }

        @builtins.property
        def record_row_path(self) -> builtins.str:
            '''``CfnApplicationReferenceDataSourceV2.JSONMappingParametersProperty.RecordRowPath``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-jsonmappingparameters.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-jsonmappingparameters-recordrowpath
            '''
            result = self._values.get("record_row_path")
            assert result is not None, "Required property 'record_row_path' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JSONMappingParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationReferenceDataSourceV2.MappingParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "csv_mapping_parameters": "csvMappingParameters",
            "json_mapping_parameters": "jsonMappingParameters",
        },
    )
    class MappingParametersProperty:
        def __init__(
            self,
            *,
            csv_mapping_parameters: typing.Optional[typing.Union["CfnApplicationReferenceDataSourceV2.CSVMappingParametersProperty", _IResolvable_a771d0ef]] = None,
            json_mapping_parameters: typing.Optional[typing.Union["CfnApplicationReferenceDataSourceV2.JSONMappingParametersProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param csv_mapping_parameters: ``CfnApplicationReferenceDataSourceV2.MappingParametersProperty.CSVMappingParameters``.
            :param json_mapping_parameters: ``CfnApplicationReferenceDataSourceV2.MappingParametersProperty.JSONMappingParameters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-mappingparameters.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if csv_mapping_parameters is not None:
                self._values["csv_mapping_parameters"] = csv_mapping_parameters
            if json_mapping_parameters is not None:
                self._values["json_mapping_parameters"] = json_mapping_parameters

        @builtins.property
        def csv_mapping_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationReferenceDataSourceV2.CSVMappingParametersProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationReferenceDataSourceV2.MappingParametersProperty.CSVMappingParameters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-mappingparameters.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-mappingparameters-csvmappingparameters
            '''
            result = self._values.get("csv_mapping_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationReferenceDataSourceV2.CSVMappingParametersProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def json_mapping_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationReferenceDataSourceV2.JSONMappingParametersProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationReferenceDataSourceV2.MappingParametersProperty.JSONMappingParameters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-mappingparameters.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-mappingparameters-jsonmappingparameters
            '''
            result = self._values.get("json_mapping_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationReferenceDataSourceV2.JSONMappingParametersProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MappingParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationReferenceDataSourceV2.RecordColumnProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "sql_type": "sqlType", "mapping": "mapping"},
    )
    class RecordColumnProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            sql_type: builtins.str,
            mapping: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param name: ``CfnApplicationReferenceDataSourceV2.RecordColumnProperty.Name``.
            :param sql_type: ``CfnApplicationReferenceDataSourceV2.RecordColumnProperty.SqlType``.
            :param mapping: ``CfnApplicationReferenceDataSourceV2.RecordColumnProperty.Mapping``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-recordcolumn.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "sql_type": sql_type,
            }
            if mapping is not None:
                self._values["mapping"] = mapping

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnApplicationReferenceDataSourceV2.RecordColumnProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-recordcolumn.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-recordcolumn-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def sql_type(self) -> builtins.str:
            '''``CfnApplicationReferenceDataSourceV2.RecordColumnProperty.SqlType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-recordcolumn.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-recordcolumn-sqltype
            '''
            result = self._values.get("sql_type")
            assert result is not None, "Required property 'sql_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def mapping(self) -> typing.Optional[builtins.str]:
            '''``CfnApplicationReferenceDataSourceV2.RecordColumnProperty.Mapping``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-recordcolumn.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-recordcolumn-mapping
            '''
            result = self._values.get("mapping")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecordColumnProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationReferenceDataSourceV2.RecordFormatProperty",
        jsii_struct_bases=[],
        name_mapping={
            "record_format_type": "recordFormatType",
            "mapping_parameters": "mappingParameters",
        },
    )
    class RecordFormatProperty:
        def __init__(
            self,
            *,
            record_format_type: builtins.str,
            mapping_parameters: typing.Optional[typing.Union["CfnApplicationReferenceDataSourceV2.MappingParametersProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param record_format_type: ``CfnApplicationReferenceDataSourceV2.RecordFormatProperty.RecordFormatType``.
            :param mapping_parameters: ``CfnApplicationReferenceDataSourceV2.RecordFormatProperty.MappingParameters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-recordformat.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "record_format_type": record_format_type,
            }
            if mapping_parameters is not None:
                self._values["mapping_parameters"] = mapping_parameters

        @builtins.property
        def record_format_type(self) -> builtins.str:
            '''``CfnApplicationReferenceDataSourceV2.RecordFormatProperty.RecordFormatType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-recordformat.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-recordformat-recordformattype
            '''
            result = self._values.get("record_format_type")
            assert result is not None, "Required property 'record_format_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def mapping_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationReferenceDataSourceV2.MappingParametersProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationReferenceDataSourceV2.RecordFormatProperty.MappingParameters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-recordformat.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-recordformat-mappingparameters
            '''
            result = self._values.get("mapping_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationReferenceDataSourceV2.MappingParametersProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecordFormatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationReferenceDataSourceV2.ReferenceDataSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "reference_schema": "referenceSchema",
            "s3_reference_data_source": "s3ReferenceDataSource",
            "table_name": "tableName",
        },
    )
    class ReferenceDataSourceProperty:
        def __init__(
            self,
            *,
            reference_schema: typing.Union["CfnApplicationReferenceDataSourceV2.ReferenceSchemaProperty", _IResolvable_a771d0ef],
            s3_reference_data_source: typing.Optional[typing.Union["CfnApplicationReferenceDataSourceV2.S3ReferenceDataSourceProperty", _IResolvable_a771d0ef]] = None,
            table_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param reference_schema: ``CfnApplicationReferenceDataSourceV2.ReferenceDataSourceProperty.ReferenceSchema``.
            :param s3_reference_data_source: ``CfnApplicationReferenceDataSourceV2.ReferenceDataSourceProperty.S3ReferenceDataSource``.
            :param table_name: ``CfnApplicationReferenceDataSourceV2.ReferenceDataSourceProperty.TableName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "reference_schema": reference_schema,
            }
            if s3_reference_data_source is not None:
                self._values["s3_reference_data_source"] = s3_reference_data_source
            if table_name is not None:
                self._values["table_name"] = table_name

        @builtins.property
        def reference_schema(
            self,
        ) -> typing.Union["CfnApplicationReferenceDataSourceV2.ReferenceSchemaProperty", _IResolvable_a771d0ef]:
            '''``CfnApplicationReferenceDataSourceV2.ReferenceDataSourceProperty.ReferenceSchema``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource-referenceschema
            '''
            result = self._values.get("reference_schema")
            assert result is not None, "Required property 'reference_schema' is missing"
            return typing.cast(typing.Union["CfnApplicationReferenceDataSourceV2.ReferenceSchemaProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def s3_reference_data_source(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationReferenceDataSourceV2.S3ReferenceDataSourceProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationReferenceDataSourceV2.ReferenceDataSourceProperty.S3ReferenceDataSource``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource-s3referencedatasource
            '''
            result = self._values.get("s3_reference_data_source")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationReferenceDataSourceV2.S3ReferenceDataSourceProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''``CfnApplicationReferenceDataSourceV2.ReferenceDataSourceProperty.TableName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReferenceDataSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationReferenceDataSourceV2.ReferenceSchemaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "record_columns": "recordColumns",
            "record_format": "recordFormat",
            "record_encoding": "recordEncoding",
        },
    )
    class ReferenceSchemaProperty:
        def __init__(
            self,
            *,
            record_columns: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplicationReferenceDataSourceV2.RecordColumnProperty", _IResolvable_a771d0ef]]],
            record_format: typing.Union["CfnApplicationReferenceDataSourceV2.RecordFormatProperty", _IResolvable_a771d0ef],
            record_encoding: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param record_columns: ``CfnApplicationReferenceDataSourceV2.ReferenceSchemaProperty.RecordColumns``.
            :param record_format: ``CfnApplicationReferenceDataSourceV2.ReferenceSchemaProperty.RecordFormat``.
            :param record_encoding: ``CfnApplicationReferenceDataSourceV2.ReferenceSchemaProperty.RecordEncoding``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referenceschema.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "record_columns": record_columns,
                "record_format": record_format,
            }
            if record_encoding is not None:
                self._values["record_encoding"] = record_encoding

        @builtins.property
        def record_columns(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplicationReferenceDataSourceV2.RecordColumnProperty", _IResolvable_a771d0ef]]]:
            '''``CfnApplicationReferenceDataSourceV2.ReferenceSchemaProperty.RecordColumns``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referenceschema.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referenceschema-recordcolumns
            '''
            result = self._values.get("record_columns")
            assert result is not None, "Required property 'record_columns' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplicationReferenceDataSourceV2.RecordColumnProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def record_format(
            self,
        ) -> typing.Union["CfnApplicationReferenceDataSourceV2.RecordFormatProperty", _IResolvable_a771d0ef]:
            '''``CfnApplicationReferenceDataSourceV2.ReferenceSchemaProperty.RecordFormat``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referenceschema.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referenceschema-recordformat
            '''
            result = self._values.get("record_format")
            assert result is not None, "Required property 'record_format' is missing"
            return typing.cast(typing.Union["CfnApplicationReferenceDataSourceV2.RecordFormatProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def record_encoding(self) -> typing.Optional[builtins.str]:
            '''``CfnApplicationReferenceDataSourceV2.ReferenceSchemaProperty.RecordEncoding``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referenceschema.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referenceschema-recordencoding
            '''
            result = self._values.get("record_encoding")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReferenceSchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationReferenceDataSourceV2.S3ReferenceDataSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_arn": "bucketArn", "file_key": "fileKey"},
    )
    class S3ReferenceDataSourceProperty:
        def __init__(self, *, bucket_arn: builtins.str, file_key: builtins.str) -> None:
            '''
            :param bucket_arn: ``CfnApplicationReferenceDataSourceV2.S3ReferenceDataSourceProperty.BucketARN``.
            :param file_key: ``CfnApplicationReferenceDataSourceV2.S3ReferenceDataSourceProperty.FileKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-s3referencedatasource.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bucket_arn": bucket_arn,
                "file_key": file_key,
            }

        @builtins.property
        def bucket_arn(self) -> builtins.str:
            '''``CfnApplicationReferenceDataSourceV2.S3ReferenceDataSourceProperty.BucketARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-s3referencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-s3referencedatasource-bucketarn
            '''
            result = self._values.get("bucket_arn")
            assert result is not None, "Required property 'bucket_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def file_key(self) -> builtins.str:
            '''``CfnApplicationReferenceDataSourceV2.S3ReferenceDataSourceProperty.FileKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-s3referencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-s3referencedatasource-filekey
            '''
            result = self._values.get("file_key")
            assert result is not None, "Required property 'file_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ReferenceDataSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationReferenceDataSourceV2Props",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "reference_data_source": "referenceDataSource",
    },
)
class CfnApplicationReferenceDataSourceV2Props:
    def __init__(
        self,
        *,
        application_name: builtins.str,
        reference_data_source: typing.Union[CfnApplicationReferenceDataSourceV2.ReferenceDataSourceProperty, _IResolvable_a771d0ef],
    ) -> None:
        '''Properties for defining a ``AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource``.

        :param application_name: ``AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource.ApplicationName``.
        :param reference_data_source: ``AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource.ReferenceDataSource``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationreferencedatasource.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "application_name": application_name,
            "reference_data_source": reference_data_source,
        }

    @builtins.property
    def application_name(self) -> builtins.str:
        '''``AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource.ApplicationName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationreferencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-applicationname
        '''
        result = self._values.get("application_name")
        assert result is not None, "Required property 'application_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def reference_data_source(
        self,
    ) -> typing.Union[CfnApplicationReferenceDataSourceV2.ReferenceDataSourceProperty, _IResolvable_a771d0ef]:
        '''``AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource.ReferenceDataSource``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationreferencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource
        '''
        result = self._values.get("reference_data_source")
        assert result is not None, "Required property 'reference_data_source' is missing"
        return typing.cast(typing.Union[CfnApplicationReferenceDataSourceV2.ReferenceDataSourceProperty, _IResolvable_a771d0ef], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationReferenceDataSourceV2Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnApplicationV2(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2",
):
    '''A CloudFormation ``AWS::KinesisAnalyticsV2::Application``.

    :cloudformationResource: AWS::KinesisAnalyticsV2::Application
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        runtime_environment: builtins.str,
        service_execution_role: builtins.str,
        application_configuration: typing.Optional[typing.Union["CfnApplicationV2.ApplicationConfigurationProperty", _IResolvable_a771d0ef]] = None,
        application_description: typing.Optional[builtins.str] = None,
        application_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Create a new ``AWS::KinesisAnalyticsV2::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param runtime_environment: ``AWS::KinesisAnalyticsV2::Application.RuntimeEnvironment``.
        :param service_execution_role: ``AWS::KinesisAnalyticsV2::Application.ServiceExecutionRole``.
        :param application_configuration: ``AWS::KinesisAnalyticsV2::Application.ApplicationConfiguration``.
        :param application_description: ``AWS::KinesisAnalyticsV2::Application.ApplicationDescription``.
        :param application_name: ``AWS::KinesisAnalyticsV2::Application.ApplicationName``.
        :param tags: ``AWS::KinesisAnalyticsV2::Application.Tags``.
        '''
        props = CfnApplicationV2Props(
            runtime_environment=runtime_environment,
            service_execution_role=service_execution_role,
            application_configuration=application_configuration,
            application_description=application_description,
            application_name=application_name,
            tags=tags,
        )

        jsii.create(CfnApplicationV2, self, [scope, id, props])

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
        '''``AWS::KinesisAnalyticsV2::Application.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="runtimeEnvironment")
    def runtime_environment(self) -> builtins.str:
        '''``AWS::KinesisAnalyticsV2::Application.RuntimeEnvironment``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-runtimeenvironment
        '''
        return typing.cast(builtins.str, jsii.get(self, "runtimeEnvironment"))

    @runtime_environment.setter
    def runtime_environment(self, value: builtins.str) -> None:
        jsii.set(self, "runtimeEnvironment", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="serviceExecutionRole")
    def service_execution_role(self) -> builtins.str:
        '''``AWS::KinesisAnalyticsV2::Application.ServiceExecutionRole``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-serviceexecutionrole
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceExecutionRole"))

    @service_execution_role.setter
    def service_execution_role(self, value: builtins.str) -> None:
        jsii.set(self, "serviceExecutionRole", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationConfiguration")
    def application_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnApplicationV2.ApplicationConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::KinesisAnalyticsV2::Application.ApplicationConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-applicationconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnApplicationV2.ApplicationConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "applicationConfiguration"))

    @application_configuration.setter
    def application_configuration(
        self,
        value: typing.Optional[typing.Union["CfnApplicationV2.ApplicationConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "applicationConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationDescription")
    def application_description(self) -> typing.Optional[builtins.str]:
        '''``AWS::KinesisAnalyticsV2::Application.ApplicationDescription``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-applicationdescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationDescription"))

    @application_description.setter
    def application_description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "applicationDescription", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::KinesisAnalyticsV2::Application.ApplicationName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-applicationname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationName"))

    @application_name.setter
    def application_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "applicationName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.ApplicationCodeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "code_content": "codeContent",
            "code_content_type": "codeContentType",
        },
    )
    class ApplicationCodeConfigurationProperty:
        def __init__(
            self,
            *,
            code_content: typing.Union["CfnApplicationV2.CodeContentProperty", _IResolvable_a771d0ef],
            code_content_type: builtins.str,
        ) -> None:
            '''
            :param code_content: ``CfnApplicationV2.ApplicationCodeConfigurationProperty.CodeContent``.
            :param code_content_type: ``CfnApplicationV2.ApplicationCodeConfigurationProperty.CodeContentType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationcodeconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "code_content": code_content,
                "code_content_type": code_content_type,
            }

        @builtins.property
        def code_content(
            self,
        ) -> typing.Union["CfnApplicationV2.CodeContentProperty", _IResolvable_a771d0ef]:
            '''``CfnApplicationV2.ApplicationCodeConfigurationProperty.CodeContent``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationcodeconfiguration.html#cfn-kinesisanalyticsv2-application-applicationcodeconfiguration-codecontent
            '''
            result = self._values.get("code_content")
            assert result is not None, "Required property 'code_content' is missing"
            return typing.cast(typing.Union["CfnApplicationV2.CodeContentProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def code_content_type(self) -> builtins.str:
            '''``CfnApplicationV2.ApplicationCodeConfigurationProperty.CodeContentType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationcodeconfiguration.html#cfn-kinesisanalyticsv2-application-applicationcodeconfiguration-codecontenttype
            '''
            result = self._values.get("code_content_type")
            assert result is not None, "Required property 'code_content_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationCodeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.ApplicationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_code_configuration": "applicationCodeConfiguration",
            "application_snapshot_configuration": "applicationSnapshotConfiguration",
            "environment_properties": "environmentProperties",
            "flink_application_configuration": "flinkApplicationConfiguration",
            "sql_application_configuration": "sqlApplicationConfiguration",
        },
    )
    class ApplicationConfigurationProperty:
        def __init__(
            self,
            *,
            application_code_configuration: typing.Optional[typing.Union["CfnApplicationV2.ApplicationCodeConfigurationProperty", _IResolvable_a771d0ef]] = None,
            application_snapshot_configuration: typing.Optional[typing.Union["CfnApplicationV2.ApplicationSnapshotConfigurationProperty", _IResolvable_a771d0ef]] = None,
            environment_properties: typing.Optional[typing.Union["CfnApplicationV2.EnvironmentPropertiesProperty", _IResolvable_a771d0ef]] = None,
            flink_application_configuration: typing.Optional[typing.Union["CfnApplicationV2.FlinkApplicationConfigurationProperty", _IResolvable_a771d0ef]] = None,
            sql_application_configuration: typing.Optional[typing.Union["CfnApplicationV2.SqlApplicationConfigurationProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param application_code_configuration: ``CfnApplicationV2.ApplicationConfigurationProperty.ApplicationCodeConfiguration``.
            :param application_snapshot_configuration: ``CfnApplicationV2.ApplicationConfigurationProperty.ApplicationSnapshotConfiguration``.
            :param environment_properties: ``CfnApplicationV2.ApplicationConfigurationProperty.EnvironmentProperties``.
            :param flink_application_configuration: ``CfnApplicationV2.ApplicationConfigurationProperty.FlinkApplicationConfiguration``.
            :param sql_application_configuration: ``CfnApplicationV2.ApplicationConfigurationProperty.SqlApplicationConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if application_code_configuration is not None:
                self._values["application_code_configuration"] = application_code_configuration
            if application_snapshot_configuration is not None:
                self._values["application_snapshot_configuration"] = application_snapshot_configuration
            if environment_properties is not None:
                self._values["environment_properties"] = environment_properties
            if flink_application_configuration is not None:
                self._values["flink_application_configuration"] = flink_application_configuration
            if sql_application_configuration is not None:
                self._values["sql_application_configuration"] = sql_application_configuration

        @builtins.property
        def application_code_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationV2.ApplicationCodeConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationV2.ApplicationConfigurationProperty.ApplicationCodeConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html#cfn-kinesisanalyticsv2-application-applicationconfiguration-applicationcodeconfiguration
            '''
            result = self._values.get("application_code_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationV2.ApplicationCodeConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def application_snapshot_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationV2.ApplicationSnapshotConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationV2.ApplicationConfigurationProperty.ApplicationSnapshotConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html#cfn-kinesisanalyticsv2-application-applicationconfiguration-applicationsnapshotconfiguration
            '''
            result = self._values.get("application_snapshot_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationV2.ApplicationSnapshotConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def environment_properties(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationV2.EnvironmentPropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationV2.ApplicationConfigurationProperty.EnvironmentProperties``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html#cfn-kinesisanalyticsv2-application-applicationconfiguration-environmentproperties
            '''
            result = self._values.get("environment_properties")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationV2.EnvironmentPropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def flink_application_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationV2.FlinkApplicationConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationV2.ApplicationConfigurationProperty.FlinkApplicationConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html#cfn-kinesisanalyticsv2-application-applicationconfiguration-flinkapplicationconfiguration
            '''
            result = self._values.get("flink_application_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationV2.FlinkApplicationConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sql_application_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationV2.SqlApplicationConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationV2.ApplicationConfigurationProperty.SqlApplicationConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html#cfn-kinesisanalyticsv2-application-applicationconfiguration-sqlapplicationconfiguration
            '''
            result = self._values.get("sql_application_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationV2.SqlApplicationConfigurationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.ApplicationSnapshotConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"snapshots_enabled": "snapshotsEnabled"},
    )
    class ApplicationSnapshotConfigurationProperty:
        def __init__(
            self,
            *,
            snapshots_enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param snapshots_enabled: ``CfnApplicationV2.ApplicationSnapshotConfigurationProperty.SnapshotsEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationsnapshotconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "snapshots_enabled": snapshots_enabled,
            }

        @builtins.property
        def snapshots_enabled(
            self,
        ) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''``CfnApplicationV2.ApplicationSnapshotConfigurationProperty.SnapshotsEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationsnapshotconfiguration.html#cfn-kinesisanalyticsv2-application-applicationsnapshotconfiguration-snapshotsenabled
            '''
            result = self._values.get("snapshots_enabled")
            assert result is not None, "Required property 'snapshots_enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationSnapshotConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.CSVMappingParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "record_column_delimiter": "recordColumnDelimiter",
            "record_row_delimiter": "recordRowDelimiter",
        },
    )
    class CSVMappingParametersProperty:
        def __init__(
            self,
            *,
            record_column_delimiter: builtins.str,
            record_row_delimiter: builtins.str,
        ) -> None:
            '''
            :param record_column_delimiter: ``CfnApplicationV2.CSVMappingParametersProperty.RecordColumnDelimiter``.
            :param record_row_delimiter: ``CfnApplicationV2.CSVMappingParametersProperty.RecordRowDelimiter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-csvmappingparameters.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "record_column_delimiter": record_column_delimiter,
                "record_row_delimiter": record_row_delimiter,
            }

        @builtins.property
        def record_column_delimiter(self) -> builtins.str:
            '''``CfnApplicationV2.CSVMappingParametersProperty.RecordColumnDelimiter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-csvmappingparameters.html#cfn-kinesisanalyticsv2-application-csvmappingparameters-recordcolumndelimiter
            '''
            result = self._values.get("record_column_delimiter")
            assert result is not None, "Required property 'record_column_delimiter' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def record_row_delimiter(self) -> builtins.str:
            '''``CfnApplicationV2.CSVMappingParametersProperty.RecordRowDelimiter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-csvmappingparameters.html#cfn-kinesisanalyticsv2-application-csvmappingparameters-recordrowdelimiter
            '''
            result = self._values.get("record_row_delimiter")
            assert result is not None, "Required property 'record_row_delimiter' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CSVMappingParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.CheckpointConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configuration_type": "configurationType",
            "checkpointing_enabled": "checkpointingEnabled",
            "checkpoint_interval": "checkpointInterval",
            "min_pause_between_checkpoints": "minPauseBetweenCheckpoints",
        },
    )
    class CheckpointConfigurationProperty:
        def __init__(
            self,
            *,
            configuration_type: builtins.str,
            checkpointing_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            checkpoint_interval: typing.Optional[jsii.Number] = None,
            min_pause_between_checkpoints: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param configuration_type: ``CfnApplicationV2.CheckpointConfigurationProperty.ConfigurationType``.
            :param checkpointing_enabled: ``CfnApplicationV2.CheckpointConfigurationProperty.CheckpointingEnabled``.
            :param checkpoint_interval: ``CfnApplicationV2.CheckpointConfigurationProperty.CheckpointInterval``.
            :param min_pause_between_checkpoints: ``CfnApplicationV2.CheckpointConfigurationProperty.MinPauseBetweenCheckpoints``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-checkpointconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "configuration_type": configuration_type,
            }
            if checkpointing_enabled is not None:
                self._values["checkpointing_enabled"] = checkpointing_enabled
            if checkpoint_interval is not None:
                self._values["checkpoint_interval"] = checkpoint_interval
            if min_pause_between_checkpoints is not None:
                self._values["min_pause_between_checkpoints"] = min_pause_between_checkpoints

        @builtins.property
        def configuration_type(self) -> builtins.str:
            '''``CfnApplicationV2.CheckpointConfigurationProperty.ConfigurationType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-checkpointconfiguration.html#cfn-kinesisanalyticsv2-application-checkpointconfiguration-configurationtype
            '''
            result = self._values.get("configuration_type")
            assert result is not None, "Required property 'configuration_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def checkpointing_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnApplicationV2.CheckpointConfigurationProperty.CheckpointingEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-checkpointconfiguration.html#cfn-kinesisanalyticsv2-application-checkpointconfiguration-checkpointingenabled
            '''
            result = self._values.get("checkpointing_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def checkpoint_interval(self) -> typing.Optional[jsii.Number]:
            '''``CfnApplicationV2.CheckpointConfigurationProperty.CheckpointInterval``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-checkpointconfiguration.html#cfn-kinesisanalyticsv2-application-checkpointconfiguration-checkpointinterval
            '''
            result = self._values.get("checkpoint_interval")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_pause_between_checkpoints(self) -> typing.Optional[jsii.Number]:
            '''``CfnApplicationV2.CheckpointConfigurationProperty.MinPauseBetweenCheckpoints``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-checkpointconfiguration.html#cfn-kinesisanalyticsv2-application-checkpointconfiguration-minpausebetweencheckpoints
            '''
            result = self._values.get("min_pause_between_checkpoints")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CheckpointConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.CodeContentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "s3_content_location": "s3ContentLocation",
            "text_content": "textContent",
            "zip_file_content": "zipFileContent",
        },
    )
    class CodeContentProperty:
        def __init__(
            self,
            *,
            s3_content_location: typing.Optional[typing.Union["CfnApplicationV2.S3ContentLocationProperty", _IResolvable_a771d0ef]] = None,
            text_content: typing.Optional[builtins.str] = None,
            zip_file_content: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param s3_content_location: ``CfnApplicationV2.CodeContentProperty.S3ContentLocation``.
            :param text_content: ``CfnApplicationV2.CodeContentProperty.TextContent``.
            :param zip_file_content: ``CfnApplicationV2.CodeContentProperty.ZipFileContent``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-codecontent.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if s3_content_location is not None:
                self._values["s3_content_location"] = s3_content_location
            if text_content is not None:
                self._values["text_content"] = text_content
            if zip_file_content is not None:
                self._values["zip_file_content"] = zip_file_content

        @builtins.property
        def s3_content_location(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationV2.S3ContentLocationProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationV2.CodeContentProperty.S3ContentLocation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-codecontent.html#cfn-kinesisanalyticsv2-application-codecontent-s3contentlocation
            '''
            result = self._values.get("s3_content_location")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationV2.S3ContentLocationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def text_content(self) -> typing.Optional[builtins.str]:
            '''``CfnApplicationV2.CodeContentProperty.TextContent``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-codecontent.html#cfn-kinesisanalyticsv2-application-codecontent-textcontent
            '''
            result = self._values.get("text_content")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def zip_file_content(self) -> typing.Optional[builtins.str]:
            '''``CfnApplicationV2.CodeContentProperty.ZipFileContent``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-codecontent.html#cfn-kinesisanalyticsv2-application-codecontent-zipfilecontent
            '''
            result = self._values.get("zip_file_content")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeContentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.EnvironmentPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"property_groups": "propertyGroups"},
    )
    class EnvironmentPropertiesProperty:
        def __init__(
            self,
            *,
            property_groups: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplicationV2.PropertyGroupProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param property_groups: ``CfnApplicationV2.EnvironmentPropertiesProperty.PropertyGroups``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-environmentproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if property_groups is not None:
                self._values["property_groups"] = property_groups

        @builtins.property
        def property_groups(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplicationV2.PropertyGroupProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnApplicationV2.EnvironmentPropertiesProperty.PropertyGroups``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-environmentproperties.html#cfn-kinesisanalyticsv2-application-environmentproperties-propertygroups
            '''
            result = self._values.get("property_groups")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplicationV2.PropertyGroupProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.FlinkApplicationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "checkpoint_configuration": "checkpointConfiguration",
            "monitoring_configuration": "monitoringConfiguration",
            "parallelism_configuration": "parallelismConfiguration",
        },
    )
    class FlinkApplicationConfigurationProperty:
        def __init__(
            self,
            *,
            checkpoint_configuration: typing.Optional[typing.Union["CfnApplicationV2.CheckpointConfigurationProperty", _IResolvable_a771d0ef]] = None,
            monitoring_configuration: typing.Optional[typing.Union["CfnApplicationV2.MonitoringConfigurationProperty", _IResolvable_a771d0ef]] = None,
            parallelism_configuration: typing.Optional[typing.Union["CfnApplicationV2.ParallelismConfigurationProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param checkpoint_configuration: ``CfnApplicationV2.FlinkApplicationConfigurationProperty.CheckpointConfiguration``.
            :param monitoring_configuration: ``CfnApplicationV2.FlinkApplicationConfigurationProperty.MonitoringConfiguration``.
            :param parallelism_configuration: ``CfnApplicationV2.FlinkApplicationConfigurationProperty.ParallelismConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-flinkapplicationconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if checkpoint_configuration is not None:
                self._values["checkpoint_configuration"] = checkpoint_configuration
            if monitoring_configuration is not None:
                self._values["monitoring_configuration"] = monitoring_configuration
            if parallelism_configuration is not None:
                self._values["parallelism_configuration"] = parallelism_configuration

        @builtins.property
        def checkpoint_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationV2.CheckpointConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationV2.FlinkApplicationConfigurationProperty.CheckpointConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-flinkapplicationconfiguration.html#cfn-kinesisanalyticsv2-application-flinkapplicationconfiguration-checkpointconfiguration
            '''
            result = self._values.get("checkpoint_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationV2.CheckpointConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def monitoring_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationV2.MonitoringConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationV2.FlinkApplicationConfigurationProperty.MonitoringConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-flinkapplicationconfiguration.html#cfn-kinesisanalyticsv2-application-flinkapplicationconfiguration-monitoringconfiguration
            '''
            result = self._values.get("monitoring_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationV2.MonitoringConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def parallelism_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationV2.ParallelismConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationV2.FlinkApplicationConfigurationProperty.ParallelismConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-flinkapplicationconfiguration.html#cfn-kinesisanalyticsv2-application-flinkapplicationconfiguration-parallelismconfiguration
            '''
            result = self._values.get("parallelism_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationV2.ParallelismConfigurationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FlinkApplicationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.InputLambdaProcessorProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn"},
    )
    class InputLambdaProcessorProperty:
        def __init__(self, *, resource_arn: builtins.str) -> None:
            '''
            :param resource_arn: ``CfnApplicationV2.InputLambdaProcessorProperty.ResourceARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputlambdaprocessor.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "resource_arn": resource_arn,
            }

        @builtins.property
        def resource_arn(self) -> builtins.str:
            '''``CfnApplicationV2.InputLambdaProcessorProperty.ResourceARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputlambdaprocessor.html#cfn-kinesisanalyticsv2-application-inputlambdaprocessor-resourcearn
            '''
            result = self._values.get("resource_arn")
            assert result is not None, "Required property 'resource_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputLambdaProcessorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.InputParallelismProperty",
        jsii_struct_bases=[],
        name_mapping={"count": "count"},
    )
    class InputParallelismProperty:
        def __init__(self, *, count: typing.Optional[jsii.Number] = None) -> None:
            '''
            :param count: ``CfnApplicationV2.InputParallelismProperty.Count``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputparallelism.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if count is not None:
                self._values["count"] = count

        @builtins.property
        def count(self) -> typing.Optional[jsii.Number]:
            '''``CfnApplicationV2.InputParallelismProperty.Count``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputparallelism.html#cfn-kinesisanalyticsv2-application-inputparallelism-count
            '''
            result = self._values.get("count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputParallelismProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.InputProcessingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"input_lambda_processor": "inputLambdaProcessor"},
    )
    class InputProcessingConfigurationProperty:
        def __init__(
            self,
            *,
            input_lambda_processor: typing.Optional[typing.Union["CfnApplicationV2.InputLambdaProcessorProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param input_lambda_processor: ``CfnApplicationV2.InputProcessingConfigurationProperty.InputLambdaProcessor``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputprocessingconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if input_lambda_processor is not None:
                self._values["input_lambda_processor"] = input_lambda_processor

        @builtins.property
        def input_lambda_processor(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationV2.InputLambdaProcessorProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationV2.InputProcessingConfigurationProperty.InputLambdaProcessor``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputprocessingconfiguration.html#cfn-kinesisanalyticsv2-application-inputprocessingconfiguration-inputlambdaprocessor
            '''
            result = self._values.get("input_lambda_processor")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationV2.InputLambdaProcessorProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputProcessingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.InputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "input_schema": "inputSchema",
            "name_prefix": "namePrefix",
            "input_parallelism": "inputParallelism",
            "input_processing_configuration": "inputProcessingConfiguration",
            "kinesis_firehose_input": "kinesisFirehoseInput",
            "kinesis_streams_input": "kinesisStreamsInput",
        },
    )
    class InputProperty:
        def __init__(
            self,
            *,
            input_schema: typing.Union["CfnApplicationV2.InputSchemaProperty", _IResolvable_a771d0ef],
            name_prefix: builtins.str,
            input_parallelism: typing.Optional[typing.Union["CfnApplicationV2.InputParallelismProperty", _IResolvable_a771d0ef]] = None,
            input_processing_configuration: typing.Optional[typing.Union["CfnApplicationV2.InputProcessingConfigurationProperty", _IResolvable_a771d0ef]] = None,
            kinesis_firehose_input: typing.Optional[typing.Union["CfnApplicationV2.KinesisFirehoseInputProperty", _IResolvable_a771d0ef]] = None,
            kinesis_streams_input: typing.Optional[typing.Union["CfnApplicationV2.KinesisStreamsInputProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param input_schema: ``CfnApplicationV2.InputProperty.InputSchema``.
            :param name_prefix: ``CfnApplicationV2.InputProperty.NamePrefix``.
            :param input_parallelism: ``CfnApplicationV2.InputProperty.InputParallelism``.
            :param input_processing_configuration: ``CfnApplicationV2.InputProperty.InputProcessingConfiguration``.
            :param kinesis_firehose_input: ``CfnApplicationV2.InputProperty.KinesisFirehoseInput``.
            :param kinesis_streams_input: ``CfnApplicationV2.InputProperty.KinesisStreamsInput``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-input.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "input_schema": input_schema,
                "name_prefix": name_prefix,
            }
            if input_parallelism is not None:
                self._values["input_parallelism"] = input_parallelism
            if input_processing_configuration is not None:
                self._values["input_processing_configuration"] = input_processing_configuration
            if kinesis_firehose_input is not None:
                self._values["kinesis_firehose_input"] = kinesis_firehose_input
            if kinesis_streams_input is not None:
                self._values["kinesis_streams_input"] = kinesis_streams_input

        @builtins.property
        def input_schema(
            self,
        ) -> typing.Union["CfnApplicationV2.InputSchemaProperty", _IResolvable_a771d0ef]:
            '''``CfnApplicationV2.InputProperty.InputSchema``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-input.html#cfn-kinesisanalyticsv2-application-input-inputschema
            '''
            result = self._values.get("input_schema")
            assert result is not None, "Required property 'input_schema' is missing"
            return typing.cast(typing.Union["CfnApplicationV2.InputSchemaProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def name_prefix(self) -> builtins.str:
            '''``CfnApplicationV2.InputProperty.NamePrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-input.html#cfn-kinesisanalyticsv2-application-input-nameprefix
            '''
            result = self._values.get("name_prefix")
            assert result is not None, "Required property 'name_prefix' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def input_parallelism(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationV2.InputParallelismProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationV2.InputProperty.InputParallelism``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-input.html#cfn-kinesisanalyticsv2-application-input-inputparallelism
            '''
            result = self._values.get("input_parallelism")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationV2.InputParallelismProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def input_processing_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationV2.InputProcessingConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationV2.InputProperty.InputProcessingConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-input.html#cfn-kinesisanalyticsv2-application-input-inputprocessingconfiguration
            '''
            result = self._values.get("input_processing_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationV2.InputProcessingConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def kinesis_firehose_input(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationV2.KinesisFirehoseInputProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationV2.InputProperty.KinesisFirehoseInput``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-input.html#cfn-kinesisanalyticsv2-application-input-kinesisfirehoseinput
            '''
            result = self._values.get("kinesis_firehose_input")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationV2.KinesisFirehoseInputProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def kinesis_streams_input(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationV2.KinesisStreamsInputProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationV2.InputProperty.KinesisStreamsInput``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-input.html#cfn-kinesisanalyticsv2-application-input-kinesisstreamsinput
            '''
            result = self._values.get("kinesis_streams_input")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationV2.KinesisStreamsInputProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.InputSchemaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "record_columns": "recordColumns",
            "record_format": "recordFormat",
            "record_encoding": "recordEncoding",
        },
    )
    class InputSchemaProperty:
        def __init__(
            self,
            *,
            record_columns: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplicationV2.RecordColumnProperty", _IResolvable_a771d0ef]]],
            record_format: typing.Union["CfnApplicationV2.RecordFormatProperty", _IResolvable_a771d0ef],
            record_encoding: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param record_columns: ``CfnApplicationV2.InputSchemaProperty.RecordColumns``.
            :param record_format: ``CfnApplicationV2.InputSchemaProperty.RecordFormat``.
            :param record_encoding: ``CfnApplicationV2.InputSchemaProperty.RecordEncoding``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputschema.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "record_columns": record_columns,
                "record_format": record_format,
            }
            if record_encoding is not None:
                self._values["record_encoding"] = record_encoding

        @builtins.property
        def record_columns(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplicationV2.RecordColumnProperty", _IResolvable_a771d0ef]]]:
            '''``CfnApplicationV2.InputSchemaProperty.RecordColumns``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputschema.html#cfn-kinesisanalyticsv2-application-inputschema-recordcolumns
            '''
            result = self._values.get("record_columns")
            assert result is not None, "Required property 'record_columns' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplicationV2.RecordColumnProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def record_format(
            self,
        ) -> typing.Union["CfnApplicationV2.RecordFormatProperty", _IResolvable_a771d0ef]:
            '''``CfnApplicationV2.InputSchemaProperty.RecordFormat``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputschema.html#cfn-kinesisanalyticsv2-application-inputschema-recordformat
            '''
            result = self._values.get("record_format")
            assert result is not None, "Required property 'record_format' is missing"
            return typing.cast(typing.Union["CfnApplicationV2.RecordFormatProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def record_encoding(self) -> typing.Optional[builtins.str]:
            '''``CfnApplicationV2.InputSchemaProperty.RecordEncoding``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputschema.html#cfn-kinesisanalyticsv2-application-inputschema-recordencoding
            '''
            result = self._values.get("record_encoding")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputSchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.JSONMappingParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"record_row_path": "recordRowPath"},
    )
    class JSONMappingParametersProperty:
        def __init__(self, *, record_row_path: builtins.str) -> None:
            '''
            :param record_row_path: ``CfnApplicationV2.JSONMappingParametersProperty.RecordRowPath``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-jsonmappingparameters.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "record_row_path": record_row_path,
            }

        @builtins.property
        def record_row_path(self) -> builtins.str:
            '''``CfnApplicationV2.JSONMappingParametersProperty.RecordRowPath``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-jsonmappingparameters.html#cfn-kinesisanalyticsv2-application-jsonmappingparameters-recordrowpath
            '''
            result = self._values.get("record_row_path")
            assert result is not None, "Required property 'record_row_path' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JSONMappingParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.KinesisFirehoseInputProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn"},
    )
    class KinesisFirehoseInputProperty:
        def __init__(self, *, resource_arn: builtins.str) -> None:
            '''
            :param resource_arn: ``CfnApplicationV2.KinesisFirehoseInputProperty.ResourceARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-kinesisfirehoseinput.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "resource_arn": resource_arn,
            }

        @builtins.property
        def resource_arn(self) -> builtins.str:
            '''``CfnApplicationV2.KinesisFirehoseInputProperty.ResourceARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-kinesisfirehoseinput.html#cfn-kinesisanalyticsv2-application-kinesisfirehoseinput-resourcearn
            '''
            result = self._values.get("resource_arn")
            assert result is not None, "Required property 'resource_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisFirehoseInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.KinesisStreamsInputProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn"},
    )
    class KinesisStreamsInputProperty:
        def __init__(self, *, resource_arn: builtins.str) -> None:
            '''
            :param resource_arn: ``CfnApplicationV2.KinesisStreamsInputProperty.ResourceARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-kinesisstreamsinput.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "resource_arn": resource_arn,
            }

        @builtins.property
        def resource_arn(self) -> builtins.str:
            '''``CfnApplicationV2.KinesisStreamsInputProperty.ResourceARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-kinesisstreamsinput.html#cfn-kinesisanalyticsv2-application-kinesisstreamsinput-resourcearn
            '''
            result = self._values.get("resource_arn")
            assert result is not None, "Required property 'resource_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisStreamsInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.MappingParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "csv_mapping_parameters": "csvMappingParameters",
            "json_mapping_parameters": "jsonMappingParameters",
        },
    )
    class MappingParametersProperty:
        def __init__(
            self,
            *,
            csv_mapping_parameters: typing.Optional[typing.Union["CfnApplicationV2.CSVMappingParametersProperty", _IResolvable_a771d0ef]] = None,
            json_mapping_parameters: typing.Optional[typing.Union["CfnApplicationV2.JSONMappingParametersProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param csv_mapping_parameters: ``CfnApplicationV2.MappingParametersProperty.CSVMappingParameters``.
            :param json_mapping_parameters: ``CfnApplicationV2.MappingParametersProperty.JSONMappingParameters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-mappingparameters.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if csv_mapping_parameters is not None:
                self._values["csv_mapping_parameters"] = csv_mapping_parameters
            if json_mapping_parameters is not None:
                self._values["json_mapping_parameters"] = json_mapping_parameters

        @builtins.property
        def csv_mapping_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationV2.CSVMappingParametersProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationV2.MappingParametersProperty.CSVMappingParameters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-mappingparameters.html#cfn-kinesisanalyticsv2-application-mappingparameters-csvmappingparameters
            '''
            result = self._values.get("csv_mapping_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationV2.CSVMappingParametersProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def json_mapping_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationV2.JSONMappingParametersProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationV2.MappingParametersProperty.JSONMappingParameters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-mappingparameters.html#cfn-kinesisanalyticsv2-application-mappingparameters-jsonmappingparameters
            '''
            result = self._values.get("json_mapping_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationV2.JSONMappingParametersProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MappingParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.MonitoringConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configuration_type": "configurationType",
            "log_level": "logLevel",
            "metrics_level": "metricsLevel",
        },
    )
    class MonitoringConfigurationProperty:
        def __init__(
            self,
            *,
            configuration_type: builtins.str,
            log_level: typing.Optional[builtins.str] = None,
            metrics_level: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param configuration_type: ``CfnApplicationV2.MonitoringConfigurationProperty.ConfigurationType``.
            :param log_level: ``CfnApplicationV2.MonitoringConfigurationProperty.LogLevel``.
            :param metrics_level: ``CfnApplicationV2.MonitoringConfigurationProperty.MetricsLevel``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-monitoringconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "configuration_type": configuration_type,
            }
            if log_level is not None:
                self._values["log_level"] = log_level
            if metrics_level is not None:
                self._values["metrics_level"] = metrics_level

        @builtins.property
        def configuration_type(self) -> builtins.str:
            '''``CfnApplicationV2.MonitoringConfigurationProperty.ConfigurationType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-monitoringconfiguration.html#cfn-kinesisanalyticsv2-application-monitoringconfiguration-configurationtype
            '''
            result = self._values.get("configuration_type")
            assert result is not None, "Required property 'configuration_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def log_level(self) -> typing.Optional[builtins.str]:
            '''``CfnApplicationV2.MonitoringConfigurationProperty.LogLevel``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-monitoringconfiguration.html#cfn-kinesisanalyticsv2-application-monitoringconfiguration-loglevel
            '''
            result = self._values.get("log_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metrics_level(self) -> typing.Optional[builtins.str]:
            '''``CfnApplicationV2.MonitoringConfigurationProperty.MetricsLevel``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-monitoringconfiguration.html#cfn-kinesisanalyticsv2-application-monitoringconfiguration-metricslevel
            '''
            result = self._values.get("metrics_level")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MonitoringConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.ParallelismConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configuration_type": "configurationType",
            "auto_scaling_enabled": "autoScalingEnabled",
            "parallelism": "parallelism",
            "parallelism_per_kpu": "parallelismPerKpu",
        },
    )
    class ParallelismConfigurationProperty:
        def __init__(
            self,
            *,
            configuration_type: builtins.str,
            auto_scaling_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            parallelism: typing.Optional[jsii.Number] = None,
            parallelism_per_kpu: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param configuration_type: ``CfnApplicationV2.ParallelismConfigurationProperty.ConfigurationType``.
            :param auto_scaling_enabled: ``CfnApplicationV2.ParallelismConfigurationProperty.AutoScalingEnabled``.
            :param parallelism: ``CfnApplicationV2.ParallelismConfigurationProperty.Parallelism``.
            :param parallelism_per_kpu: ``CfnApplicationV2.ParallelismConfigurationProperty.ParallelismPerKPU``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-parallelismconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "configuration_type": configuration_type,
            }
            if auto_scaling_enabled is not None:
                self._values["auto_scaling_enabled"] = auto_scaling_enabled
            if parallelism is not None:
                self._values["parallelism"] = parallelism
            if parallelism_per_kpu is not None:
                self._values["parallelism_per_kpu"] = parallelism_per_kpu

        @builtins.property
        def configuration_type(self) -> builtins.str:
            '''``CfnApplicationV2.ParallelismConfigurationProperty.ConfigurationType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-parallelismconfiguration.html#cfn-kinesisanalyticsv2-application-parallelismconfiguration-configurationtype
            '''
            result = self._values.get("configuration_type")
            assert result is not None, "Required property 'configuration_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def auto_scaling_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnApplicationV2.ParallelismConfigurationProperty.AutoScalingEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-parallelismconfiguration.html#cfn-kinesisanalyticsv2-application-parallelismconfiguration-autoscalingenabled
            '''
            result = self._values.get("auto_scaling_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def parallelism(self) -> typing.Optional[jsii.Number]:
            '''``CfnApplicationV2.ParallelismConfigurationProperty.Parallelism``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-parallelismconfiguration.html#cfn-kinesisanalyticsv2-application-parallelismconfiguration-parallelism
            '''
            result = self._values.get("parallelism")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def parallelism_per_kpu(self) -> typing.Optional[jsii.Number]:
            '''``CfnApplicationV2.ParallelismConfigurationProperty.ParallelismPerKPU``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-parallelismconfiguration.html#cfn-kinesisanalyticsv2-application-parallelismconfiguration-parallelismperkpu
            '''
            result = self._values.get("parallelism_per_kpu")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParallelismConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.PropertyGroupProperty",
        jsii_struct_bases=[],
        name_mapping={
            "property_group_id": "propertyGroupId",
            "property_map": "propertyMap",
        },
    )
    class PropertyGroupProperty:
        def __init__(
            self,
            *,
            property_group_id: typing.Optional[builtins.str] = None,
            property_map: typing.Any = None,
        ) -> None:
            '''
            :param property_group_id: ``CfnApplicationV2.PropertyGroupProperty.PropertyGroupId``.
            :param property_map: ``CfnApplicationV2.PropertyGroupProperty.PropertyMap``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-propertygroup.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if property_group_id is not None:
                self._values["property_group_id"] = property_group_id
            if property_map is not None:
                self._values["property_map"] = property_map

        @builtins.property
        def property_group_id(self) -> typing.Optional[builtins.str]:
            '''``CfnApplicationV2.PropertyGroupProperty.PropertyGroupId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-propertygroup.html#cfn-kinesisanalyticsv2-application-propertygroup-propertygroupid
            '''
            result = self._values.get("property_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_map(self) -> typing.Any:
            '''``CfnApplicationV2.PropertyGroupProperty.PropertyMap``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-propertygroup.html#cfn-kinesisanalyticsv2-application-propertygroup-propertymap
            '''
            result = self._values.get("property_map")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertyGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.RecordColumnProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "sql_type": "sqlType", "mapping": "mapping"},
    )
    class RecordColumnProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            sql_type: builtins.str,
            mapping: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param name: ``CfnApplicationV2.RecordColumnProperty.Name``.
            :param sql_type: ``CfnApplicationV2.RecordColumnProperty.SqlType``.
            :param mapping: ``CfnApplicationV2.RecordColumnProperty.Mapping``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-recordcolumn.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "sql_type": sql_type,
            }
            if mapping is not None:
                self._values["mapping"] = mapping

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnApplicationV2.RecordColumnProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-recordcolumn.html#cfn-kinesisanalyticsv2-application-recordcolumn-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def sql_type(self) -> builtins.str:
            '''``CfnApplicationV2.RecordColumnProperty.SqlType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-recordcolumn.html#cfn-kinesisanalyticsv2-application-recordcolumn-sqltype
            '''
            result = self._values.get("sql_type")
            assert result is not None, "Required property 'sql_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def mapping(self) -> typing.Optional[builtins.str]:
            '''``CfnApplicationV2.RecordColumnProperty.Mapping``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-recordcolumn.html#cfn-kinesisanalyticsv2-application-recordcolumn-mapping
            '''
            result = self._values.get("mapping")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecordColumnProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.RecordFormatProperty",
        jsii_struct_bases=[],
        name_mapping={
            "record_format_type": "recordFormatType",
            "mapping_parameters": "mappingParameters",
        },
    )
    class RecordFormatProperty:
        def __init__(
            self,
            *,
            record_format_type: builtins.str,
            mapping_parameters: typing.Optional[typing.Union["CfnApplicationV2.MappingParametersProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param record_format_type: ``CfnApplicationV2.RecordFormatProperty.RecordFormatType``.
            :param mapping_parameters: ``CfnApplicationV2.RecordFormatProperty.MappingParameters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-recordformat.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "record_format_type": record_format_type,
            }
            if mapping_parameters is not None:
                self._values["mapping_parameters"] = mapping_parameters

        @builtins.property
        def record_format_type(self) -> builtins.str:
            '''``CfnApplicationV2.RecordFormatProperty.RecordFormatType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-recordformat.html#cfn-kinesisanalyticsv2-application-recordformat-recordformattype
            '''
            result = self._values.get("record_format_type")
            assert result is not None, "Required property 'record_format_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def mapping_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnApplicationV2.MappingParametersProperty", _IResolvable_a771d0ef]]:
            '''``CfnApplicationV2.RecordFormatProperty.MappingParameters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-recordformat.html#cfn-kinesisanalyticsv2-application-recordformat-mappingparameters
            '''
            result = self._values.get("mapping_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnApplicationV2.MappingParametersProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecordFormatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.S3ContentLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_arn": "bucketArn",
            "file_key": "fileKey",
            "object_version": "objectVersion",
        },
    )
    class S3ContentLocationProperty:
        def __init__(
            self,
            *,
            bucket_arn: typing.Optional[builtins.str] = None,
            file_key: typing.Optional[builtins.str] = None,
            object_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param bucket_arn: ``CfnApplicationV2.S3ContentLocationProperty.BucketARN``.
            :param file_key: ``CfnApplicationV2.S3ContentLocationProperty.FileKey``.
            :param object_version: ``CfnApplicationV2.S3ContentLocationProperty.ObjectVersion``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-s3contentlocation.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if bucket_arn is not None:
                self._values["bucket_arn"] = bucket_arn
            if file_key is not None:
                self._values["file_key"] = file_key
            if object_version is not None:
                self._values["object_version"] = object_version

        @builtins.property
        def bucket_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnApplicationV2.S3ContentLocationProperty.BucketARN``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-s3contentlocation.html#cfn-kinesisanalyticsv2-application-s3contentlocation-bucketarn
            '''
            result = self._values.get("bucket_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def file_key(self) -> typing.Optional[builtins.str]:
            '''``CfnApplicationV2.S3ContentLocationProperty.FileKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-s3contentlocation.html#cfn-kinesisanalyticsv2-application-s3contentlocation-filekey
            '''
            result = self._values.get("file_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_version(self) -> typing.Optional[builtins.str]:
            '''``CfnApplicationV2.S3ContentLocationProperty.ObjectVersion``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-s3contentlocation.html#cfn-kinesisanalyticsv2-application-s3contentlocation-objectversion
            '''
            result = self._values.get("object_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ContentLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2.SqlApplicationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"inputs": "inputs"},
    )
    class SqlApplicationConfigurationProperty:
        def __init__(
            self,
            *,
            inputs: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplicationV2.InputProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param inputs: ``CfnApplicationV2.SqlApplicationConfigurationProperty.Inputs``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-sqlapplicationconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if inputs is not None:
                self._values["inputs"] = inputs

        @builtins.property
        def inputs(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplicationV2.InputProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnApplicationV2.SqlApplicationConfigurationProperty.Inputs``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-sqlapplicationconfiguration.html#cfn-kinesisanalyticsv2-application-sqlapplicationconfiguration-inputs
            '''
            result = self._values.get("inputs")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplicationV2.InputProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SqlApplicationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_kinesisanalytics.CfnApplicationV2Props",
    jsii_struct_bases=[],
    name_mapping={
        "runtime_environment": "runtimeEnvironment",
        "service_execution_role": "serviceExecutionRole",
        "application_configuration": "applicationConfiguration",
        "application_description": "applicationDescription",
        "application_name": "applicationName",
        "tags": "tags",
    },
)
class CfnApplicationV2Props:
    def __init__(
        self,
        *,
        runtime_environment: builtins.str,
        service_execution_role: builtins.str,
        application_configuration: typing.Optional[typing.Union[CfnApplicationV2.ApplicationConfigurationProperty, _IResolvable_a771d0ef]] = None,
        application_description: typing.Optional[builtins.str] = None,
        application_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::KinesisAnalyticsV2::Application``.

        :param runtime_environment: ``AWS::KinesisAnalyticsV2::Application.RuntimeEnvironment``.
        :param service_execution_role: ``AWS::KinesisAnalyticsV2::Application.ServiceExecutionRole``.
        :param application_configuration: ``AWS::KinesisAnalyticsV2::Application.ApplicationConfiguration``.
        :param application_description: ``AWS::KinesisAnalyticsV2::Application.ApplicationDescription``.
        :param application_name: ``AWS::KinesisAnalyticsV2::Application.ApplicationName``.
        :param tags: ``AWS::KinesisAnalyticsV2::Application.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "runtime_environment": runtime_environment,
            "service_execution_role": service_execution_role,
        }
        if application_configuration is not None:
            self._values["application_configuration"] = application_configuration
        if application_description is not None:
            self._values["application_description"] = application_description
        if application_name is not None:
            self._values["application_name"] = application_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def runtime_environment(self) -> builtins.str:
        '''``AWS::KinesisAnalyticsV2::Application.RuntimeEnvironment``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-runtimeenvironment
        '''
        result = self._values.get("runtime_environment")
        assert result is not None, "Required property 'runtime_environment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_execution_role(self) -> builtins.str:
        '''``AWS::KinesisAnalyticsV2::Application.ServiceExecutionRole``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-serviceexecutionrole
        '''
        result = self._values.get("service_execution_role")
        assert result is not None, "Required property 'service_execution_role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnApplicationV2.ApplicationConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::KinesisAnalyticsV2::Application.ApplicationConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-applicationconfiguration
        '''
        result = self._values.get("application_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnApplicationV2.ApplicationConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def application_description(self) -> typing.Optional[builtins.str]:
        '''``AWS::KinesisAnalyticsV2::Application.ApplicationDescription``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-applicationdescription
        '''
        result = self._values.get("application_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::KinesisAnalyticsV2::Application.ApplicationName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-applicationname
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::KinesisAnalyticsV2::Application.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationV2Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnApplication",
    "CfnApplicationCloudWatchLoggingOptionV2",
    "CfnApplicationCloudWatchLoggingOptionV2Props",
    "CfnApplicationOutput",
    "CfnApplicationOutputProps",
    "CfnApplicationOutputV2",
    "CfnApplicationOutputV2Props",
    "CfnApplicationProps",
    "CfnApplicationReferenceDataSource",
    "CfnApplicationReferenceDataSourceProps",
    "CfnApplicationReferenceDataSourceV2",
    "CfnApplicationReferenceDataSourceV2Props",
    "CfnApplicationV2",
    "CfnApplicationV2Props",
]

publication.publish()
