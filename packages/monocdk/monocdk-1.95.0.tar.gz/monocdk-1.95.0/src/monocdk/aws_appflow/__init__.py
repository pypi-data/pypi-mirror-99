'''
# AWS::AppFlow Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_appflow as appflow
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
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnConnectorProfile(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appflow.CfnConnectorProfile",
):
    '''A CloudFormation ``AWS::AppFlow::ConnectorProfile``.

    :cloudformationResource: AWS::AppFlow::ConnectorProfile
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        connection_mode: builtins.str,
        connector_profile_name: builtins.str,
        connector_type: builtins.str,
        connector_profile_config: typing.Optional[typing.Union["CfnConnectorProfile.ConnectorProfileConfigProperty", _IResolvable_a771d0ef]] = None,
        kms_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::AppFlow::ConnectorProfile``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param connection_mode: ``AWS::AppFlow::ConnectorProfile.ConnectionMode``.
        :param connector_profile_name: ``AWS::AppFlow::ConnectorProfile.ConnectorProfileName``.
        :param connector_type: ``AWS::AppFlow::ConnectorProfile.ConnectorType``.
        :param connector_profile_config: ``AWS::AppFlow::ConnectorProfile.ConnectorProfileConfig``.
        :param kms_arn: ``AWS::AppFlow::ConnectorProfile.KMSArn``.
        '''
        props = CfnConnectorProfileProps(
            connection_mode=connection_mode,
            connector_profile_name=connector_profile_name,
            connector_type=connector_type,
            connector_profile_config=connector_profile_config,
            kms_arn=kms_arn,
        )

        jsii.create(CfnConnectorProfile, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrConnectorProfileArn")
    def attr_connector_profile_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: ConnectorProfileArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrConnectorProfileArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrCredentialsArn")
    def attr_credentials_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: CredentialsArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCredentialsArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="connectionMode")
    def connection_mode(self) -> builtins.str:
        '''``AWS::AppFlow::ConnectorProfile.ConnectionMode``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectionmode
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectionMode"))

    @connection_mode.setter
    def connection_mode(self, value: builtins.str) -> None:
        jsii.set(self, "connectionMode", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="connectorProfileName")
    def connector_profile_name(self) -> builtins.str:
        '''``AWS::AppFlow::ConnectorProfile.ConnectorProfileName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectorprofilename
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectorProfileName"))

    @connector_profile_name.setter
    def connector_profile_name(self, value: builtins.str) -> None:
        jsii.set(self, "connectorProfileName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="connectorType")
    def connector_type(self) -> builtins.str:
        '''``AWS::AppFlow::ConnectorProfile.ConnectorType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectortype
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectorType"))

    @connector_type.setter
    def connector_type(self, value: builtins.str) -> None:
        jsii.set(self, "connectorType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="connectorProfileConfig")
    def connector_profile_config(
        self,
    ) -> typing.Optional[typing.Union["CfnConnectorProfile.ConnectorProfileConfigProperty", _IResolvable_a771d0ef]]:
        '''``AWS::AppFlow::ConnectorProfile.ConnectorProfileConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectorprofileconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ConnectorProfileConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "connectorProfileConfig"))

    @connector_profile_config.setter
    def connector_profile_config(
        self,
        value: typing.Optional[typing.Union["CfnConnectorProfile.ConnectorProfileConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "connectorProfileConfig", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="kmsArn")
    def kms_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppFlow::ConnectorProfile.KMSArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-kmsarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsArn"))

    @kms_arn.setter
    def kms_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "kmsArn", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.AmplitudeConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"api_key": "apiKey", "secret_key": "secretKey"},
    )
    class AmplitudeConnectorProfileCredentialsProperty:
        def __init__(self, *, api_key: builtins.str, secret_key: builtins.str) -> None:
            '''
            :param api_key: ``CfnConnectorProfile.AmplitudeConnectorProfileCredentialsProperty.ApiKey``.
            :param secret_key: ``CfnConnectorProfile.AmplitudeConnectorProfileCredentialsProperty.SecretKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-amplitudeconnectorprofilecredentials.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "api_key": api_key,
                "secret_key": secret_key,
            }

        @builtins.property
        def api_key(self) -> builtins.str:
            '''``CfnConnectorProfile.AmplitudeConnectorProfileCredentialsProperty.ApiKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-amplitudeconnectorprofilecredentials.html#cfn-appflow-connectorprofile-amplitudeconnectorprofilecredentials-apikey
            '''
            result = self._values.get("api_key")
            assert result is not None, "Required property 'api_key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def secret_key(self) -> builtins.str:
            '''``CfnConnectorProfile.AmplitudeConnectorProfileCredentialsProperty.SecretKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-amplitudeconnectorprofilecredentials.html#cfn-appflow-connectorprofile-amplitudeconnectorprofilecredentials-secretkey
            '''
            result = self._values.get("secret_key")
            assert result is not None, "Required property 'secret_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AmplitudeConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.ConnectorOAuthRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"auth_code": "authCode", "redirect_uri": "redirectUri"},
    )
    class ConnectorOAuthRequestProperty:
        def __init__(
            self,
            *,
            auth_code: typing.Optional[builtins.str] = None,
            redirect_uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param auth_code: ``CfnConnectorProfile.ConnectorOAuthRequestProperty.AuthCode``.
            :param redirect_uri: ``CfnConnectorProfile.ConnectorOAuthRequestProperty.RedirectUri``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectoroauthrequest.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if auth_code is not None:
                self._values["auth_code"] = auth_code
            if redirect_uri is not None:
                self._values["redirect_uri"] = redirect_uri

        @builtins.property
        def auth_code(self) -> typing.Optional[builtins.str]:
            '''``CfnConnectorProfile.ConnectorOAuthRequestProperty.AuthCode``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectoroauthrequest.html#cfn-appflow-connectorprofile-connectoroauthrequest-authcode
            '''
            result = self._values.get("auth_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def redirect_uri(self) -> typing.Optional[builtins.str]:
            '''``CfnConnectorProfile.ConnectorOAuthRequestProperty.RedirectUri``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectoroauthrequest.html#cfn-appflow-connectorprofile-connectoroauthrequest-redirecturi
            '''
            result = self._values.get("redirect_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorOAuthRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.ConnectorProfileConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connector_profile_credentials": "connectorProfileCredentials",
            "connector_profile_properties": "connectorProfileProperties",
        },
    )
    class ConnectorProfileConfigProperty:
        def __init__(
            self,
            *,
            connector_profile_credentials: typing.Union["CfnConnectorProfile.ConnectorProfileCredentialsProperty", _IResolvable_a771d0ef],
            connector_profile_properties: typing.Optional[typing.Union["CfnConnectorProfile.ConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param connector_profile_credentials: ``CfnConnectorProfile.ConnectorProfileConfigProperty.ConnectorProfileCredentials``.
            :param connector_profile_properties: ``CfnConnectorProfile.ConnectorProfileConfigProperty.ConnectorProfileProperties``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "connector_profile_credentials": connector_profile_credentials,
            }
            if connector_profile_properties is not None:
                self._values["connector_profile_properties"] = connector_profile_properties

        @builtins.property
        def connector_profile_credentials(
            self,
        ) -> typing.Union["CfnConnectorProfile.ConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]:
            '''``CfnConnectorProfile.ConnectorProfileConfigProperty.ConnectorProfileCredentials``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileconfig.html#cfn-appflow-connectorprofile-connectorprofileconfig-connectorprofilecredentials
            '''
            result = self._values.get("connector_profile_credentials")
            assert result is not None, "Required property 'connector_profile_credentials' is missing"
            return typing.cast(typing.Union["CfnConnectorProfile.ConnectorProfileCredentialsProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def connector_profile_properties(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfileConfigProperty.ConnectorProfileProperties``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileconfig.html#cfn-appflow-connectorprofile-connectorprofileconfig-connectorprofileproperties
            '''
            result = self._values.get("connector_profile_properties")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorProfileConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.ConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "amplitude": "amplitude",
            "datadog": "datadog",
            "dynatrace": "dynatrace",
            "google_analytics": "googleAnalytics",
            "infor_nexus": "inforNexus",
            "marketo": "marketo",
            "redshift": "redshift",
            "salesforce": "salesforce",
            "service_now": "serviceNow",
            "singular": "singular",
            "slack": "slack",
            "snowflake": "snowflake",
            "trendmicro": "trendmicro",
            "veeva": "veeva",
            "zendesk": "zendesk",
        },
    )
    class ConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            amplitude: typing.Optional[typing.Union["CfnConnectorProfile.AmplitudeConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]] = None,
            datadog: typing.Optional[typing.Union["CfnConnectorProfile.DatadogConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]] = None,
            dynatrace: typing.Optional[typing.Union["CfnConnectorProfile.DynatraceConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]] = None,
            google_analytics: typing.Optional[typing.Union["CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]] = None,
            infor_nexus: typing.Optional[typing.Union["CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]] = None,
            marketo: typing.Optional[typing.Union["CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]] = None,
            redshift: typing.Optional[typing.Union["CfnConnectorProfile.RedshiftConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]] = None,
            salesforce: typing.Optional[typing.Union["CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]] = None,
            service_now: typing.Optional[typing.Union["CfnConnectorProfile.ServiceNowConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]] = None,
            singular: typing.Optional[typing.Union["CfnConnectorProfile.SingularConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]] = None,
            slack: typing.Optional[typing.Union["CfnConnectorProfile.SlackConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]] = None,
            snowflake: typing.Optional[typing.Union["CfnConnectorProfile.SnowflakeConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]] = None,
            trendmicro: typing.Optional[typing.Union["CfnConnectorProfile.TrendmicroConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]] = None,
            veeva: typing.Optional[typing.Union["CfnConnectorProfile.VeevaConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]] = None,
            zendesk: typing.Optional[typing.Union["CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param amplitude: ``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Amplitude``.
            :param datadog: ``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Datadog``.
            :param dynatrace: ``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Dynatrace``.
            :param google_analytics: ``CfnConnectorProfile.ConnectorProfileCredentialsProperty.GoogleAnalytics``.
            :param infor_nexus: ``CfnConnectorProfile.ConnectorProfileCredentialsProperty.InforNexus``.
            :param marketo: ``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Marketo``.
            :param redshift: ``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Redshift``.
            :param salesforce: ``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Salesforce``.
            :param service_now: ``CfnConnectorProfile.ConnectorProfileCredentialsProperty.ServiceNow``.
            :param singular: ``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Singular``.
            :param slack: ``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Slack``.
            :param snowflake: ``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Snowflake``.
            :param trendmicro: ``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Trendmicro``.
            :param veeva: ``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Veeva``.
            :param zendesk: ``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Zendesk``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if amplitude is not None:
                self._values["amplitude"] = amplitude
            if datadog is not None:
                self._values["datadog"] = datadog
            if dynatrace is not None:
                self._values["dynatrace"] = dynatrace
            if google_analytics is not None:
                self._values["google_analytics"] = google_analytics
            if infor_nexus is not None:
                self._values["infor_nexus"] = infor_nexus
            if marketo is not None:
                self._values["marketo"] = marketo
            if redshift is not None:
                self._values["redshift"] = redshift
            if salesforce is not None:
                self._values["salesforce"] = salesforce
            if service_now is not None:
                self._values["service_now"] = service_now
            if singular is not None:
                self._values["singular"] = singular
            if slack is not None:
                self._values["slack"] = slack
            if snowflake is not None:
                self._values["snowflake"] = snowflake
            if trendmicro is not None:
                self._values["trendmicro"] = trendmicro
            if veeva is not None:
                self._values["veeva"] = veeva
            if zendesk is not None:
                self._values["zendesk"] = zendesk

        @builtins.property
        def amplitude(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.AmplitudeConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Amplitude``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-amplitude
            '''
            result = self._values.get("amplitude")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.AmplitudeConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def datadog(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.DatadogConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Datadog``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-datadog
            '''
            result = self._values.get("datadog")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.DatadogConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def dynatrace(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.DynatraceConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Dynatrace``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-dynatrace
            '''
            result = self._values.get("dynatrace")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.DynatraceConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def google_analytics(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfileCredentialsProperty.GoogleAnalytics``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-googleanalytics
            '''
            result = self._values.get("google_analytics")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def infor_nexus(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfileCredentialsProperty.InforNexus``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-infornexus
            '''
            result = self._values.get("infor_nexus")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def marketo(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Marketo``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-marketo
            '''
            result = self._values.get("marketo")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def redshift(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.RedshiftConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Redshift``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-redshift
            '''
            result = self._values.get("redshift")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.RedshiftConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def salesforce(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Salesforce``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-salesforce
            '''
            result = self._values.get("salesforce")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def service_now(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ServiceNowConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfileCredentialsProperty.ServiceNow``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-servicenow
            '''
            result = self._values.get("service_now")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ServiceNowConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def singular(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.SingularConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Singular``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-singular
            '''
            result = self._values.get("singular")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.SingularConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def slack(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.SlackConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Slack``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-slack
            '''
            result = self._values.get("slack")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.SlackConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def snowflake(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.SnowflakeConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Snowflake``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-snowflake
            '''
            result = self._values.get("snowflake")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.SnowflakeConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def trendmicro(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.TrendmicroConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Trendmicro``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-trendmicro
            '''
            result = self._values.get("trendmicro")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.TrendmicroConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def veeva(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.VeevaConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Veeva``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-veeva
            '''
            result = self._values.get("veeva")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.VeevaConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def zendesk(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfileCredentialsProperty.Zendesk``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofilecredentials.html#cfn-appflow-connectorprofile-connectorprofilecredentials-zendesk
            '''
            result = self._values.get("zendesk")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.ConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "datadog": "datadog",
            "dynatrace": "dynatrace",
            "infor_nexus": "inforNexus",
            "marketo": "marketo",
            "redshift": "redshift",
            "salesforce": "salesforce",
            "service_now": "serviceNow",
            "slack": "slack",
            "snowflake": "snowflake",
            "veeva": "veeva",
            "zendesk": "zendesk",
        },
    )
    class ConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            datadog: typing.Optional[typing.Union["CfnConnectorProfile.DatadogConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]] = None,
            dynatrace: typing.Optional[typing.Union["CfnConnectorProfile.DynatraceConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]] = None,
            infor_nexus: typing.Optional[typing.Union["CfnConnectorProfile.InforNexusConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]] = None,
            marketo: typing.Optional[typing.Union["CfnConnectorProfile.MarketoConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]] = None,
            redshift: typing.Optional[typing.Union["CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]] = None,
            salesforce: typing.Optional[typing.Union["CfnConnectorProfile.SalesforceConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]] = None,
            service_now: typing.Optional[typing.Union["CfnConnectorProfile.ServiceNowConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]] = None,
            slack: typing.Optional[typing.Union["CfnConnectorProfile.SlackConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]] = None,
            snowflake: typing.Optional[typing.Union["CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]] = None,
            veeva: typing.Optional[typing.Union["CfnConnectorProfile.VeevaConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]] = None,
            zendesk: typing.Optional[typing.Union["CfnConnectorProfile.ZendeskConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param datadog: ``CfnConnectorProfile.ConnectorProfilePropertiesProperty.Datadog``.
            :param dynatrace: ``CfnConnectorProfile.ConnectorProfilePropertiesProperty.Dynatrace``.
            :param infor_nexus: ``CfnConnectorProfile.ConnectorProfilePropertiesProperty.InforNexus``.
            :param marketo: ``CfnConnectorProfile.ConnectorProfilePropertiesProperty.Marketo``.
            :param redshift: ``CfnConnectorProfile.ConnectorProfilePropertiesProperty.Redshift``.
            :param salesforce: ``CfnConnectorProfile.ConnectorProfilePropertiesProperty.Salesforce``.
            :param service_now: ``CfnConnectorProfile.ConnectorProfilePropertiesProperty.ServiceNow``.
            :param slack: ``CfnConnectorProfile.ConnectorProfilePropertiesProperty.Slack``.
            :param snowflake: ``CfnConnectorProfile.ConnectorProfilePropertiesProperty.Snowflake``.
            :param veeva: ``CfnConnectorProfile.ConnectorProfilePropertiesProperty.Veeva``.
            :param zendesk: ``CfnConnectorProfile.ConnectorProfilePropertiesProperty.Zendesk``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if datadog is not None:
                self._values["datadog"] = datadog
            if dynatrace is not None:
                self._values["dynatrace"] = dynatrace
            if infor_nexus is not None:
                self._values["infor_nexus"] = infor_nexus
            if marketo is not None:
                self._values["marketo"] = marketo
            if redshift is not None:
                self._values["redshift"] = redshift
            if salesforce is not None:
                self._values["salesforce"] = salesforce
            if service_now is not None:
                self._values["service_now"] = service_now
            if slack is not None:
                self._values["slack"] = slack
            if snowflake is not None:
                self._values["snowflake"] = snowflake
            if veeva is not None:
                self._values["veeva"] = veeva
            if zendesk is not None:
                self._values["zendesk"] = zendesk

        @builtins.property
        def datadog(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.DatadogConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfilePropertiesProperty.Datadog``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-datadog
            '''
            result = self._values.get("datadog")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.DatadogConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def dynatrace(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.DynatraceConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfilePropertiesProperty.Dynatrace``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-dynatrace
            '''
            result = self._values.get("dynatrace")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.DynatraceConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def infor_nexus(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.InforNexusConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfilePropertiesProperty.InforNexus``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-infornexus
            '''
            result = self._values.get("infor_nexus")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.InforNexusConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def marketo(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.MarketoConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfilePropertiesProperty.Marketo``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-marketo
            '''
            result = self._values.get("marketo")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.MarketoConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def redshift(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfilePropertiesProperty.Redshift``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-redshift
            '''
            result = self._values.get("redshift")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def salesforce(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.SalesforceConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfilePropertiesProperty.Salesforce``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-salesforce
            '''
            result = self._values.get("salesforce")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.SalesforceConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def service_now(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ServiceNowConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfilePropertiesProperty.ServiceNow``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-servicenow
            '''
            result = self._values.get("service_now")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ServiceNowConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def slack(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.SlackConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfilePropertiesProperty.Slack``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-slack
            '''
            result = self._values.get("slack")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.SlackConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def snowflake(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfilePropertiesProperty.Snowflake``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-snowflake
            '''
            result = self._values.get("snowflake")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def veeva(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.VeevaConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfilePropertiesProperty.Veeva``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-veeva
            '''
            result = self._values.get("veeva")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.VeevaConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def zendesk(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ZendeskConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ConnectorProfilePropertiesProperty.Zendesk``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-connectorprofileproperties.html#cfn-appflow-connectorprofile-connectorprofileproperties-zendesk
            '''
            result = self._values.get("zendesk")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ZendeskConnectorProfilePropertiesProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.DatadogConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"api_key": "apiKey", "application_key": "applicationKey"},
    )
    class DatadogConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            api_key: builtins.str,
            application_key: builtins.str,
        ) -> None:
            '''
            :param api_key: ``CfnConnectorProfile.DatadogConnectorProfileCredentialsProperty.ApiKey``.
            :param application_key: ``CfnConnectorProfile.DatadogConnectorProfileCredentialsProperty.ApplicationKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-datadogconnectorprofilecredentials.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "api_key": api_key,
                "application_key": application_key,
            }

        @builtins.property
        def api_key(self) -> builtins.str:
            '''``CfnConnectorProfile.DatadogConnectorProfileCredentialsProperty.ApiKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-datadogconnectorprofilecredentials.html#cfn-appflow-connectorprofile-datadogconnectorprofilecredentials-apikey
            '''
            result = self._values.get("api_key")
            assert result is not None, "Required property 'api_key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def application_key(self) -> builtins.str:
            '''``CfnConnectorProfile.DatadogConnectorProfileCredentialsProperty.ApplicationKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-datadogconnectorprofilecredentials.html#cfn-appflow-connectorprofile-datadogconnectorprofilecredentials-applicationkey
            '''
            result = self._values.get("application_key")
            assert result is not None, "Required property 'application_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatadogConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.DatadogConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class DatadogConnectorProfilePropertiesProperty:
        def __init__(self, *, instance_url: builtins.str) -> None:
            '''
            :param instance_url: ``CfnConnectorProfile.DatadogConnectorProfilePropertiesProperty.InstanceUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-datadogconnectorprofileproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "instance_url": instance_url,
            }

        @builtins.property
        def instance_url(self) -> builtins.str:
            '''``CfnConnectorProfile.DatadogConnectorProfilePropertiesProperty.InstanceUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-datadogconnectorprofileproperties.html#cfn-appflow-connectorprofile-datadogconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            assert result is not None, "Required property 'instance_url' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatadogConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.DynatraceConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"api_token": "apiToken"},
    )
    class DynatraceConnectorProfileCredentialsProperty:
        def __init__(self, *, api_token: builtins.str) -> None:
            '''
            :param api_token: ``CfnConnectorProfile.DynatraceConnectorProfileCredentialsProperty.ApiToken``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-dynatraceconnectorprofilecredentials.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "api_token": api_token,
            }

        @builtins.property
        def api_token(self) -> builtins.str:
            '''``CfnConnectorProfile.DynatraceConnectorProfileCredentialsProperty.ApiToken``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-dynatraceconnectorprofilecredentials.html#cfn-appflow-connectorprofile-dynatraceconnectorprofilecredentials-apitoken
            '''
            result = self._values.get("api_token")
            assert result is not None, "Required property 'api_token' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynatraceConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.DynatraceConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class DynatraceConnectorProfilePropertiesProperty:
        def __init__(self, *, instance_url: builtins.str) -> None:
            '''
            :param instance_url: ``CfnConnectorProfile.DynatraceConnectorProfilePropertiesProperty.InstanceUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-dynatraceconnectorprofileproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "instance_url": instance_url,
            }

        @builtins.property
        def instance_url(self) -> builtins.str:
            '''``CfnConnectorProfile.DynatraceConnectorProfilePropertiesProperty.InstanceUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-dynatraceconnectorprofileproperties.html#cfn-appflow-connectorprofile-dynatraceconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            assert result is not None, "Required property 'instance_url' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynatraceConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "access_token": "accessToken",
            "connector_o_auth_request": "connectorOAuthRequest",
            "refresh_token": "refreshToken",
        },
    )
    class GoogleAnalyticsConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            client_id: builtins.str,
            client_secret: builtins.str,
            access_token: typing.Optional[builtins.str] = None,
            connector_o_auth_request: typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]] = None,
            refresh_token: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param client_id: ``CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty.ClientId``.
            :param client_secret: ``CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty.ClientSecret``.
            :param access_token: ``CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty.AccessToken``.
            :param connector_o_auth_request: ``CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty.ConnectorOAuthRequest``.
            :param refresh_token: ``CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty.RefreshToken``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "client_id": client_id,
                "client_secret": client_secret,
            }
            if access_token is not None:
                self._values["access_token"] = access_token
            if connector_o_auth_request is not None:
                self._values["connector_o_auth_request"] = connector_o_auth_request
            if refresh_token is not None:
                self._values["refresh_token"] = refresh_token

        @builtins.property
        def client_id(self) -> builtins.str:
            '''``CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty.ClientId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials.html#cfn-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials-clientid
            '''
            result = self._values.get("client_id")
            assert result is not None, "Required property 'client_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def client_secret(self) -> builtins.str:
            '''``CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty.ClientSecret``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials.html#cfn-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials-clientsecret
            '''
            result = self._values.get("client_secret")
            assert result is not None, "Required property 'client_secret' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''``CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty.AccessToken``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials.html#cfn-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_o_auth_request(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty.ConnectorOAuthRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials.html#cfn-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials-connectoroauthrequest
            '''
            result = self._values.get("connector_o_auth_request")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def refresh_token(self) -> typing.Optional[builtins.str]:
            '''``CfnConnectorProfile.GoogleAnalyticsConnectorProfileCredentialsProperty.RefreshToken``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials.html#cfn-appflow-connectorprofile-googleanalyticsconnectorprofilecredentials-refreshtoken
            '''
            result = self._values.get("refresh_token")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GoogleAnalyticsConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_key_id": "accessKeyId",
            "datakey": "datakey",
            "secret_access_key": "secretAccessKey",
            "user_id": "userId",
        },
    )
    class InforNexusConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            access_key_id: builtins.str,
            datakey: builtins.str,
            secret_access_key: builtins.str,
            user_id: builtins.str,
        ) -> None:
            '''
            :param access_key_id: ``CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty.AccessKeyId``.
            :param datakey: ``CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty.Datakey``.
            :param secret_access_key: ``CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty.SecretAccessKey``.
            :param user_id: ``CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty.UserId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-infornexusconnectorprofilecredentials.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "access_key_id": access_key_id,
                "datakey": datakey,
                "secret_access_key": secret_access_key,
                "user_id": user_id,
            }

        @builtins.property
        def access_key_id(self) -> builtins.str:
            '''``CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty.AccessKeyId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-infornexusconnectorprofilecredentials.html#cfn-appflow-connectorprofile-infornexusconnectorprofilecredentials-accesskeyid
            '''
            result = self._values.get("access_key_id")
            assert result is not None, "Required property 'access_key_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def datakey(self) -> builtins.str:
            '''``CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty.Datakey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-infornexusconnectorprofilecredentials.html#cfn-appflow-connectorprofile-infornexusconnectorprofilecredentials-datakey
            '''
            result = self._values.get("datakey")
            assert result is not None, "Required property 'datakey' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def secret_access_key(self) -> builtins.str:
            '''``CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty.SecretAccessKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-infornexusconnectorprofilecredentials.html#cfn-appflow-connectorprofile-infornexusconnectorprofilecredentials-secretaccesskey
            '''
            result = self._values.get("secret_access_key")
            assert result is not None, "Required property 'secret_access_key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def user_id(self) -> builtins.str:
            '''``CfnConnectorProfile.InforNexusConnectorProfileCredentialsProperty.UserId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-infornexusconnectorprofilecredentials.html#cfn-appflow-connectorprofile-infornexusconnectorprofilecredentials-userid
            '''
            result = self._values.get("user_id")
            assert result is not None, "Required property 'user_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InforNexusConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.InforNexusConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class InforNexusConnectorProfilePropertiesProperty:
        def __init__(self, *, instance_url: builtins.str) -> None:
            '''
            :param instance_url: ``CfnConnectorProfile.InforNexusConnectorProfilePropertiesProperty.InstanceUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-infornexusconnectorprofileproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "instance_url": instance_url,
            }

        @builtins.property
        def instance_url(self) -> builtins.str:
            '''``CfnConnectorProfile.InforNexusConnectorProfilePropertiesProperty.InstanceUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-infornexusconnectorprofileproperties.html#cfn-appflow-connectorprofile-infornexusconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            assert result is not None, "Required property 'instance_url' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InforNexusConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "access_token": "accessToken",
            "connector_o_auth_request": "connectorOAuthRequest",
        },
    )
    class MarketoConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            client_id: builtins.str,
            client_secret: builtins.str,
            access_token: typing.Optional[builtins.str] = None,
            connector_o_auth_request: typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param client_id: ``CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty.ClientId``.
            :param client_secret: ``CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty.ClientSecret``.
            :param access_token: ``CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty.AccessToken``.
            :param connector_o_auth_request: ``CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty.ConnectorOAuthRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-marketoconnectorprofilecredentials.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "client_id": client_id,
                "client_secret": client_secret,
            }
            if access_token is not None:
                self._values["access_token"] = access_token
            if connector_o_auth_request is not None:
                self._values["connector_o_auth_request"] = connector_o_auth_request

        @builtins.property
        def client_id(self) -> builtins.str:
            '''``CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty.ClientId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-marketoconnectorprofilecredentials.html#cfn-appflow-connectorprofile-marketoconnectorprofilecredentials-clientid
            '''
            result = self._values.get("client_id")
            assert result is not None, "Required property 'client_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def client_secret(self) -> builtins.str:
            '''``CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty.ClientSecret``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-marketoconnectorprofilecredentials.html#cfn-appflow-connectorprofile-marketoconnectorprofilecredentials-clientsecret
            '''
            result = self._values.get("client_secret")
            assert result is not None, "Required property 'client_secret' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''``CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty.AccessToken``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-marketoconnectorprofilecredentials.html#cfn-appflow-connectorprofile-marketoconnectorprofilecredentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_o_auth_request(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.MarketoConnectorProfileCredentialsProperty.ConnectorOAuthRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-marketoconnectorprofilecredentials.html#cfn-appflow-connectorprofile-marketoconnectorprofilecredentials-connectoroauthrequest
            '''
            result = self._values.get("connector_o_auth_request")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MarketoConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.MarketoConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class MarketoConnectorProfilePropertiesProperty:
        def __init__(self, *, instance_url: builtins.str) -> None:
            '''
            :param instance_url: ``CfnConnectorProfile.MarketoConnectorProfilePropertiesProperty.InstanceUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-marketoconnectorprofileproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "instance_url": instance_url,
            }

        @builtins.property
        def instance_url(self) -> builtins.str:
            '''``CfnConnectorProfile.MarketoConnectorProfilePropertiesProperty.InstanceUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-marketoconnectorprofileproperties.html#cfn-appflow-connectorprofile-marketoconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            assert result is not None, "Required property 'instance_url' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MarketoConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.RedshiftConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"password": "password", "username": "username"},
    )
    class RedshiftConnectorProfileCredentialsProperty:
        def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
            '''
            :param password: ``CfnConnectorProfile.RedshiftConnectorProfileCredentialsProperty.Password``.
            :param username: ``CfnConnectorProfile.RedshiftConnectorProfileCredentialsProperty.Username``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofilecredentials.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "password": password,
                "username": username,
            }

        @builtins.property
        def password(self) -> builtins.str:
            '''``CfnConnectorProfile.RedshiftConnectorProfileCredentialsProperty.Password``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofilecredentials.html#cfn-appflow-connectorprofile-redshiftconnectorprofilecredentials-password
            '''
            result = self._values.get("password")
            assert result is not None, "Required property 'password' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def username(self) -> builtins.str:
            '''``CfnConnectorProfile.RedshiftConnectorProfileCredentialsProperty.Username``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofilecredentials.html#cfn-appflow-connectorprofile-redshiftconnectorprofilecredentials-username
            '''
            result = self._values.get("username")
            assert result is not None, "Required property 'username' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "database_url": "databaseUrl",
            "role_arn": "roleArn",
            "bucket_prefix": "bucketPrefix",
        },
    )
    class RedshiftConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            database_url: builtins.str,
            role_arn: builtins.str,
            bucket_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param bucket_name: ``CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty.BucketName``.
            :param database_url: ``CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty.DatabaseUrl``.
            :param role_arn: ``CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty.RoleArn``.
            :param bucket_prefix: ``CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty.BucketPrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bucket_name": bucket_name,
                "database_url": database_url,
                "role_arn": role_arn,
            }
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''``CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty.BucketName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def database_url(self) -> builtins.str:
            '''``CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty.DatabaseUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-databaseurl
            '''
            result = self._values.get("database_url")
            assert result is not None, "Required property 'database_url' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def role_arn(self) -> builtins.str:
            '''``CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty.RoleArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-rolearn
            '''
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnConnectorProfile.RedshiftConnectorProfilePropertiesProperty.BucketPrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-redshiftconnectorprofileproperties.html#cfn-appflow-connectorprofile-redshiftconnectorprofileproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_token": "accessToken",
            "client_credentials_arn": "clientCredentialsArn",
            "connector_o_auth_request": "connectorOAuthRequest",
            "refresh_token": "refreshToken",
        },
    )
    class SalesforceConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            access_token: typing.Optional[builtins.str] = None,
            client_credentials_arn: typing.Optional[builtins.str] = None,
            connector_o_auth_request: typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]] = None,
            refresh_token: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param access_token: ``CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty.AccessToken``.
            :param client_credentials_arn: ``CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty.ClientCredentialsArn``.
            :param connector_o_auth_request: ``CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty.ConnectorOAuthRequest``.
            :param refresh_token: ``CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty.RefreshToken``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofilecredentials.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if access_token is not None:
                self._values["access_token"] = access_token
            if client_credentials_arn is not None:
                self._values["client_credentials_arn"] = client_credentials_arn
            if connector_o_auth_request is not None:
                self._values["connector_o_auth_request"] = connector_o_auth_request
            if refresh_token is not None:
                self._values["refresh_token"] = refresh_token

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''``CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty.AccessToken``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofilecredentials.html#cfn-appflow-connectorprofile-salesforceconnectorprofilecredentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_credentials_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty.ClientCredentialsArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofilecredentials.html#cfn-appflow-connectorprofile-salesforceconnectorprofilecredentials-clientcredentialsarn
            '''
            result = self._values.get("client_credentials_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_o_auth_request(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty.ConnectorOAuthRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofilecredentials.html#cfn-appflow-connectorprofile-salesforceconnectorprofilecredentials-connectoroauthrequest
            '''
            result = self._values.get("connector_o_auth_request")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def refresh_token(self) -> typing.Optional[builtins.str]:
            '''``CfnConnectorProfile.SalesforceConnectorProfileCredentialsProperty.RefreshToken``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofilecredentials.html#cfn-appflow-connectorprofile-salesforceconnectorprofilecredentials-refreshtoken
            '''
            result = self._values.get("refresh_token")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.SalesforceConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instance_url": "instanceUrl",
            "is_sandbox_environment": "isSandboxEnvironment",
        },
    )
    class SalesforceConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            instance_url: typing.Optional[builtins.str] = None,
            is_sandbox_environment: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param instance_url: ``CfnConnectorProfile.SalesforceConnectorProfilePropertiesProperty.InstanceUrl``.
            :param is_sandbox_environment: ``CfnConnectorProfile.SalesforceConnectorProfilePropertiesProperty.isSandboxEnvironment``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofileproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if instance_url is not None:
                self._values["instance_url"] = instance_url
            if is_sandbox_environment is not None:
                self._values["is_sandbox_environment"] = is_sandbox_environment

        @builtins.property
        def instance_url(self) -> typing.Optional[builtins.str]:
            '''``CfnConnectorProfile.SalesforceConnectorProfilePropertiesProperty.InstanceUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofileproperties.html#cfn-appflow-connectorprofile-salesforceconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def is_sandbox_environment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.SalesforceConnectorProfilePropertiesProperty.isSandboxEnvironment``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-salesforceconnectorprofileproperties.html#cfn-appflow-connectorprofile-salesforceconnectorprofileproperties-issandboxenvironment
            '''
            result = self._values.get("is_sandbox_environment")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.ServiceNowConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"password": "password", "username": "username"},
    )
    class ServiceNowConnectorProfileCredentialsProperty:
        def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
            '''
            :param password: ``CfnConnectorProfile.ServiceNowConnectorProfileCredentialsProperty.Password``.
            :param username: ``CfnConnectorProfile.ServiceNowConnectorProfileCredentialsProperty.Username``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-servicenowconnectorprofilecredentials.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "password": password,
                "username": username,
            }

        @builtins.property
        def password(self) -> builtins.str:
            '''``CfnConnectorProfile.ServiceNowConnectorProfileCredentialsProperty.Password``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-servicenowconnectorprofilecredentials.html#cfn-appflow-connectorprofile-servicenowconnectorprofilecredentials-password
            '''
            result = self._values.get("password")
            assert result is not None, "Required property 'password' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def username(self) -> builtins.str:
            '''``CfnConnectorProfile.ServiceNowConnectorProfileCredentialsProperty.Username``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-servicenowconnectorprofilecredentials.html#cfn-appflow-connectorprofile-servicenowconnectorprofilecredentials-username
            '''
            result = self._values.get("username")
            assert result is not None, "Required property 'username' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceNowConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.ServiceNowConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class ServiceNowConnectorProfilePropertiesProperty:
        def __init__(self, *, instance_url: builtins.str) -> None:
            '''
            :param instance_url: ``CfnConnectorProfile.ServiceNowConnectorProfilePropertiesProperty.InstanceUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-servicenowconnectorprofileproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "instance_url": instance_url,
            }

        @builtins.property
        def instance_url(self) -> builtins.str:
            '''``CfnConnectorProfile.ServiceNowConnectorProfilePropertiesProperty.InstanceUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-servicenowconnectorprofileproperties.html#cfn-appflow-connectorprofile-servicenowconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            assert result is not None, "Required property 'instance_url' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceNowConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.SingularConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"api_key": "apiKey"},
    )
    class SingularConnectorProfileCredentialsProperty:
        def __init__(self, *, api_key: builtins.str) -> None:
            '''
            :param api_key: ``CfnConnectorProfile.SingularConnectorProfileCredentialsProperty.ApiKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-singularconnectorprofilecredentials.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "api_key": api_key,
            }

        @builtins.property
        def api_key(self) -> builtins.str:
            '''``CfnConnectorProfile.SingularConnectorProfileCredentialsProperty.ApiKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-singularconnectorprofilecredentials.html#cfn-appflow-connectorprofile-singularconnectorprofilecredentials-apikey
            '''
            result = self._values.get("api_key")
            assert result is not None, "Required property 'api_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SingularConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.SlackConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "access_token": "accessToken",
            "connector_o_auth_request": "connectorOAuthRequest",
        },
    )
    class SlackConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            client_id: builtins.str,
            client_secret: builtins.str,
            access_token: typing.Optional[builtins.str] = None,
            connector_o_auth_request: typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param client_id: ``CfnConnectorProfile.SlackConnectorProfileCredentialsProperty.ClientId``.
            :param client_secret: ``CfnConnectorProfile.SlackConnectorProfileCredentialsProperty.ClientSecret``.
            :param access_token: ``CfnConnectorProfile.SlackConnectorProfileCredentialsProperty.AccessToken``.
            :param connector_o_auth_request: ``CfnConnectorProfile.SlackConnectorProfileCredentialsProperty.ConnectorOAuthRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-slackconnectorprofilecredentials.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "client_id": client_id,
                "client_secret": client_secret,
            }
            if access_token is not None:
                self._values["access_token"] = access_token
            if connector_o_auth_request is not None:
                self._values["connector_o_auth_request"] = connector_o_auth_request

        @builtins.property
        def client_id(self) -> builtins.str:
            '''``CfnConnectorProfile.SlackConnectorProfileCredentialsProperty.ClientId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-slackconnectorprofilecredentials.html#cfn-appflow-connectorprofile-slackconnectorprofilecredentials-clientid
            '''
            result = self._values.get("client_id")
            assert result is not None, "Required property 'client_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def client_secret(self) -> builtins.str:
            '''``CfnConnectorProfile.SlackConnectorProfileCredentialsProperty.ClientSecret``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-slackconnectorprofilecredentials.html#cfn-appflow-connectorprofile-slackconnectorprofilecredentials-clientsecret
            '''
            result = self._values.get("client_secret")
            assert result is not None, "Required property 'client_secret' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''``CfnConnectorProfile.SlackConnectorProfileCredentialsProperty.AccessToken``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-slackconnectorprofilecredentials.html#cfn-appflow-connectorprofile-slackconnectorprofilecredentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_o_auth_request(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.SlackConnectorProfileCredentialsProperty.ConnectorOAuthRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-slackconnectorprofilecredentials.html#cfn-appflow-connectorprofile-slackconnectorprofilecredentials-connectoroauthrequest
            '''
            result = self._values.get("connector_o_auth_request")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlackConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.SlackConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class SlackConnectorProfilePropertiesProperty:
        def __init__(self, *, instance_url: builtins.str) -> None:
            '''
            :param instance_url: ``CfnConnectorProfile.SlackConnectorProfilePropertiesProperty.InstanceUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-slackconnectorprofileproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "instance_url": instance_url,
            }

        @builtins.property
        def instance_url(self) -> builtins.str:
            '''``CfnConnectorProfile.SlackConnectorProfilePropertiesProperty.InstanceUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-slackconnectorprofileproperties.html#cfn-appflow-connectorprofile-slackconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            assert result is not None, "Required property 'instance_url' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlackConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.SnowflakeConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"password": "password", "username": "username"},
    )
    class SnowflakeConnectorProfileCredentialsProperty:
        def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
            '''
            :param password: ``CfnConnectorProfile.SnowflakeConnectorProfileCredentialsProperty.Password``.
            :param username: ``CfnConnectorProfile.SnowflakeConnectorProfileCredentialsProperty.Username``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofilecredentials.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "password": password,
                "username": username,
            }

        @builtins.property
        def password(self) -> builtins.str:
            '''``CfnConnectorProfile.SnowflakeConnectorProfileCredentialsProperty.Password``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofilecredentials.html#cfn-appflow-connectorprofile-snowflakeconnectorprofilecredentials-password
            '''
            result = self._values.get("password")
            assert result is not None, "Required property 'password' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def username(self) -> builtins.str:
            '''``CfnConnectorProfile.SnowflakeConnectorProfileCredentialsProperty.Username``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofilecredentials.html#cfn-appflow-connectorprofile-snowflakeconnectorprofilecredentials-username
            '''
            result = self._values.get("username")
            assert result is not None, "Required property 'username' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnowflakeConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "stage": "stage",
            "warehouse": "warehouse",
            "account_name": "accountName",
            "bucket_prefix": "bucketPrefix",
            "private_link_service_name": "privateLinkServiceName",
            "region": "region",
        },
    )
    class SnowflakeConnectorProfilePropertiesProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            stage: builtins.str,
            warehouse: builtins.str,
            account_name: typing.Optional[builtins.str] = None,
            bucket_prefix: typing.Optional[builtins.str] = None,
            private_link_service_name: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param bucket_name: ``CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty.BucketName``.
            :param stage: ``CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty.Stage``.
            :param warehouse: ``CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty.Warehouse``.
            :param account_name: ``CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty.AccountName``.
            :param bucket_prefix: ``CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty.BucketPrefix``.
            :param private_link_service_name: ``CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty.PrivateLinkServiceName``.
            :param region: ``CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty.Region``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bucket_name": bucket_name,
                "stage": stage,
                "warehouse": warehouse,
            }
            if account_name is not None:
                self._values["account_name"] = account_name
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if private_link_service_name is not None:
                self._values["private_link_service_name"] = private_link_service_name
            if region is not None:
                self._values["region"] = region

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''``CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty.BucketName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html#cfn-appflow-connectorprofile-snowflakeconnectorprofileproperties-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def stage(self) -> builtins.str:
            '''``CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty.Stage``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html#cfn-appflow-connectorprofile-snowflakeconnectorprofileproperties-stage
            '''
            result = self._values.get("stage")
            assert result is not None, "Required property 'stage' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def warehouse(self) -> builtins.str:
            '''``CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty.Warehouse``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html#cfn-appflow-connectorprofile-snowflakeconnectorprofileproperties-warehouse
            '''
            result = self._values.get("warehouse")
            assert result is not None, "Required property 'warehouse' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def account_name(self) -> typing.Optional[builtins.str]:
            '''``CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty.AccountName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html#cfn-appflow-connectorprofile-snowflakeconnectorprofileproperties-accountname
            '''
            result = self._values.get("account_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty.BucketPrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html#cfn-appflow-connectorprofile-snowflakeconnectorprofileproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def private_link_service_name(self) -> typing.Optional[builtins.str]:
            '''``CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty.PrivateLinkServiceName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html#cfn-appflow-connectorprofile-snowflakeconnectorprofileproperties-privatelinkservicename
            '''
            result = self._values.get("private_link_service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''``CfnConnectorProfile.SnowflakeConnectorProfilePropertiesProperty.Region``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-snowflakeconnectorprofileproperties.html#cfn-appflow-connectorprofile-snowflakeconnectorprofileproperties-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnowflakeConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.TrendmicroConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"api_secret_key": "apiSecretKey"},
    )
    class TrendmicroConnectorProfileCredentialsProperty:
        def __init__(self, *, api_secret_key: builtins.str) -> None:
            '''
            :param api_secret_key: ``CfnConnectorProfile.TrendmicroConnectorProfileCredentialsProperty.ApiSecretKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-trendmicroconnectorprofilecredentials.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "api_secret_key": api_secret_key,
            }

        @builtins.property
        def api_secret_key(self) -> builtins.str:
            '''``CfnConnectorProfile.TrendmicroConnectorProfileCredentialsProperty.ApiSecretKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-trendmicroconnectorprofilecredentials.html#cfn-appflow-connectorprofile-trendmicroconnectorprofilecredentials-apisecretkey
            '''
            result = self._values.get("api_secret_key")
            assert result is not None, "Required property 'api_secret_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TrendmicroConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.VeevaConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={"password": "password", "username": "username"},
    )
    class VeevaConnectorProfileCredentialsProperty:
        def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
            '''
            :param password: ``CfnConnectorProfile.VeevaConnectorProfileCredentialsProperty.Password``.
            :param username: ``CfnConnectorProfile.VeevaConnectorProfileCredentialsProperty.Username``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-veevaconnectorprofilecredentials.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "password": password,
                "username": username,
            }

        @builtins.property
        def password(self) -> builtins.str:
            '''``CfnConnectorProfile.VeevaConnectorProfileCredentialsProperty.Password``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-veevaconnectorprofilecredentials.html#cfn-appflow-connectorprofile-veevaconnectorprofilecredentials-password
            '''
            result = self._values.get("password")
            assert result is not None, "Required property 'password' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def username(self) -> builtins.str:
            '''``CfnConnectorProfile.VeevaConnectorProfileCredentialsProperty.Username``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-veevaconnectorprofilecredentials.html#cfn-appflow-connectorprofile-veevaconnectorprofilecredentials-username
            '''
            result = self._values.get("username")
            assert result is not None, "Required property 'username' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VeevaConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.VeevaConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class VeevaConnectorProfilePropertiesProperty:
        def __init__(self, *, instance_url: builtins.str) -> None:
            '''
            :param instance_url: ``CfnConnectorProfile.VeevaConnectorProfilePropertiesProperty.InstanceUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-veevaconnectorprofileproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "instance_url": instance_url,
            }

        @builtins.property
        def instance_url(self) -> builtins.str:
            '''``CfnConnectorProfile.VeevaConnectorProfilePropertiesProperty.InstanceUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-veevaconnectorprofileproperties.html#cfn-appflow-connectorprofile-veevaconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            assert result is not None, "Required property 'instance_url' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VeevaConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "client_id": "clientId",
            "client_secret": "clientSecret",
            "access_token": "accessToken",
            "connector_o_auth_request": "connectorOAuthRequest",
        },
    )
    class ZendeskConnectorProfileCredentialsProperty:
        def __init__(
            self,
            *,
            client_id: builtins.str,
            client_secret: builtins.str,
            access_token: typing.Optional[builtins.str] = None,
            connector_o_auth_request: typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param client_id: ``CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty.ClientId``.
            :param client_secret: ``CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty.ClientSecret``.
            :param access_token: ``CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty.AccessToken``.
            :param connector_o_auth_request: ``CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty.ConnectorOAuthRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-zendeskconnectorprofilecredentials.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "client_id": client_id,
                "client_secret": client_secret,
            }
            if access_token is not None:
                self._values["access_token"] = access_token
            if connector_o_auth_request is not None:
                self._values["connector_o_auth_request"] = connector_o_auth_request

        @builtins.property
        def client_id(self) -> builtins.str:
            '''``CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty.ClientId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-zendeskconnectorprofilecredentials.html#cfn-appflow-connectorprofile-zendeskconnectorprofilecredentials-clientid
            '''
            result = self._values.get("client_id")
            assert result is not None, "Required property 'client_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def client_secret(self) -> builtins.str:
            '''``CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty.ClientSecret``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-zendeskconnectorprofilecredentials.html#cfn-appflow-connectorprofile-zendeskconnectorprofilecredentials-clientsecret
            '''
            result = self._values.get("client_secret")
            assert result is not None, "Required property 'client_secret' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''``CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty.AccessToken``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-zendeskconnectorprofilecredentials.html#cfn-appflow-connectorprofile-zendeskconnectorprofilecredentials-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connector_o_auth_request(
            self,
        ) -> typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]]:
            '''``CfnConnectorProfile.ZendeskConnectorProfileCredentialsProperty.ConnectorOAuthRequest``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-zendeskconnectorprofilecredentials.html#cfn-appflow-connectorprofile-zendeskconnectorprofilecredentials-connectoroauthrequest
            '''
            result = self._values.get("connector_o_auth_request")
            return typing.cast(typing.Optional[typing.Union["CfnConnectorProfile.ConnectorOAuthRequestProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZendeskConnectorProfileCredentialsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnConnectorProfile.ZendeskConnectorProfilePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_url": "instanceUrl"},
    )
    class ZendeskConnectorProfilePropertiesProperty:
        def __init__(self, *, instance_url: builtins.str) -> None:
            '''
            :param instance_url: ``CfnConnectorProfile.ZendeskConnectorProfilePropertiesProperty.InstanceUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-zendeskconnectorprofileproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "instance_url": instance_url,
            }

        @builtins.property
        def instance_url(self) -> builtins.str:
            '''``CfnConnectorProfile.ZendeskConnectorProfilePropertiesProperty.InstanceUrl``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-connectorprofile-zendeskconnectorprofileproperties.html#cfn-appflow-connectorprofile-zendeskconnectorprofileproperties-instanceurl
            '''
            result = self._values.get("instance_url")
            assert result is not None, "Required property 'instance_url' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZendeskConnectorProfilePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_appflow.CfnConnectorProfileProps",
    jsii_struct_bases=[],
    name_mapping={
        "connection_mode": "connectionMode",
        "connector_profile_name": "connectorProfileName",
        "connector_type": "connectorType",
        "connector_profile_config": "connectorProfileConfig",
        "kms_arn": "kmsArn",
    },
)
class CfnConnectorProfileProps:
    def __init__(
        self,
        *,
        connection_mode: builtins.str,
        connector_profile_name: builtins.str,
        connector_type: builtins.str,
        connector_profile_config: typing.Optional[typing.Union[CfnConnectorProfile.ConnectorProfileConfigProperty, _IResolvable_a771d0ef]] = None,
        kms_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``AWS::AppFlow::ConnectorProfile``.

        :param connection_mode: ``AWS::AppFlow::ConnectorProfile.ConnectionMode``.
        :param connector_profile_name: ``AWS::AppFlow::ConnectorProfile.ConnectorProfileName``.
        :param connector_type: ``AWS::AppFlow::ConnectorProfile.ConnectorType``.
        :param connector_profile_config: ``AWS::AppFlow::ConnectorProfile.ConnectorProfileConfig``.
        :param kms_arn: ``AWS::AppFlow::ConnectorProfile.KMSArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "connection_mode": connection_mode,
            "connector_profile_name": connector_profile_name,
            "connector_type": connector_type,
        }
        if connector_profile_config is not None:
            self._values["connector_profile_config"] = connector_profile_config
        if kms_arn is not None:
            self._values["kms_arn"] = kms_arn

    @builtins.property
    def connection_mode(self) -> builtins.str:
        '''``AWS::AppFlow::ConnectorProfile.ConnectionMode``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectionmode
        '''
        result = self._values.get("connection_mode")
        assert result is not None, "Required property 'connection_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connector_profile_name(self) -> builtins.str:
        '''``AWS::AppFlow::ConnectorProfile.ConnectorProfileName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectorprofilename
        '''
        result = self._values.get("connector_profile_name")
        assert result is not None, "Required property 'connector_profile_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connector_type(self) -> builtins.str:
        '''``AWS::AppFlow::ConnectorProfile.ConnectorType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectortype
        '''
        result = self._values.get("connector_type")
        assert result is not None, "Required property 'connector_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def connector_profile_config(
        self,
    ) -> typing.Optional[typing.Union[CfnConnectorProfile.ConnectorProfileConfigProperty, _IResolvable_a771d0ef]]:
        '''``AWS::AppFlow::ConnectorProfile.ConnectorProfileConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-connectorprofileconfig
        '''
        result = self._values.get("connector_profile_config")
        return typing.cast(typing.Optional[typing.Union[CfnConnectorProfile.ConnectorProfileConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def kms_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppFlow::ConnectorProfile.KMSArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-connectorprofile.html#cfn-appflow-connectorprofile-kmsarn
        '''
        result = self._values.get("kms_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectorProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnFlow(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appflow.CfnFlow",
):
    '''A CloudFormation ``AWS::AppFlow::Flow``.

    :cloudformationResource: AWS::AppFlow::Flow
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        destination_flow_config_list: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFlow.DestinationFlowConfigProperty", _IResolvable_a771d0ef]]],
        flow_name: builtins.str,
        source_flow_config: typing.Union["CfnFlow.SourceFlowConfigProperty", _IResolvable_a771d0ef],
        tasks: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFlow.TaskProperty", _IResolvable_a771d0ef]]],
        trigger_config: typing.Union["CfnFlow.TriggerConfigProperty", _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        kms_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Create a new ``AWS::AppFlow::Flow``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination_flow_config_list: ``AWS::AppFlow::Flow.DestinationFlowConfigList``.
        :param flow_name: ``AWS::AppFlow::Flow.FlowName``.
        :param source_flow_config: ``AWS::AppFlow::Flow.SourceFlowConfig``.
        :param tasks: ``AWS::AppFlow::Flow.Tasks``.
        :param trigger_config: ``AWS::AppFlow::Flow.TriggerConfig``.
        :param description: ``AWS::AppFlow::Flow.Description``.
        :param kms_arn: ``AWS::AppFlow::Flow.KMSArn``.
        :param tags: ``AWS::AppFlow::Flow.Tags``.
        '''
        props = CfnFlowProps(
            destination_flow_config_list=destination_flow_config_list,
            flow_name=flow_name,
            source_flow_config=source_flow_config,
            tasks=tasks,
            trigger_config=trigger_config,
            description=description,
            kms_arn=kms_arn,
            tags=tags,
        )

        jsii.create(CfnFlow, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrFlowArn")
    def attr_flow_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: FlowArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFlowArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::AppFlow::Flow.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="destinationFlowConfigList")
    def destination_flow_config_list(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFlow.DestinationFlowConfigProperty", _IResolvable_a771d0ef]]]:
        '''``AWS::AppFlow::Flow.DestinationFlowConfigList``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-destinationflowconfiglist
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFlow.DestinationFlowConfigProperty", _IResolvable_a771d0ef]]], jsii.get(self, "destinationFlowConfigList"))

    @destination_flow_config_list.setter
    def destination_flow_config_list(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFlow.DestinationFlowConfigProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        jsii.set(self, "destinationFlowConfigList", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="flowName")
    def flow_name(self) -> builtins.str:
        '''``AWS::AppFlow::Flow.FlowName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-flowname
        '''
        return typing.cast(builtins.str, jsii.get(self, "flowName"))

    @flow_name.setter
    def flow_name(self, value: builtins.str) -> None:
        jsii.set(self, "flowName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sourceFlowConfig")
    def source_flow_config(
        self,
    ) -> typing.Union["CfnFlow.SourceFlowConfigProperty", _IResolvable_a771d0ef]:
        '''``AWS::AppFlow::Flow.SourceFlowConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-sourceflowconfig
        '''
        return typing.cast(typing.Union["CfnFlow.SourceFlowConfigProperty", _IResolvable_a771d0ef], jsii.get(self, "sourceFlowConfig"))

    @source_flow_config.setter
    def source_flow_config(
        self,
        value: typing.Union["CfnFlow.SourceFlowConfigProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "sourceFlowConfig", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tasks")
    def tasks(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFlow.TaskProperty", _IResolvable_a771d0ef]]]:
        '''``AWS::AppFlow::Flow.Tasks``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-tasks
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFlow.TaskProperty", _IResolvable_a771d0ef]]], jsii.get(self, "tasks"))

    @tasks.setter
    def tasks(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFlow.TaskProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        jsii.set(self, "tasks", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="triggerConfig")
    def trigger_config(
        self,
    ) -> typing.Union["CfnFlow.TriggerConfigProperty", _IResolvable_a771d0ef]:
        '''``AWS::AppFlow::Flow.TriggerConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-triggerconfig
        '''
        return typing.cast(typing.Union["CfnFlow.TriggerConfigProperty", _IResolvable_a771d0ef], jsii.get(self, "triggerConfig"))

    @trigger_config.setter
    def trigger_config(
        self,
        value: typing.Union["CfnFlow.TriggerConfigProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "triggerConfig", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppFlow::Flow.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="kmsArn")
    def kms_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppFlow::Flow.KMSArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-kmsarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsArn"))

    @kms_arn.setter
    def kms_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "kmsArn", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.AggregationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"aggregation_type": "aggregationType"},
    )
    class AggregationConfigProperty:
        def __init__(
            self,
            *,
            aggregation_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param aggregation_type: ``CfnFlow.AggregationConfigProperty.AggregationType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-aggregationconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if aggregation_type is not None:
                self._values["aggregation_type"] = aggregation_type

        @builtins.property
        def aggregation_type(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.AggregationConfigProperty.AggregationType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-aggregationconfig.html#cfn-appflow-flow-aggregationconfig-aggregationtype
            '''
            result = self._values.get("aggregation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AggregationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.AmplitudeSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class AmplitudeSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''
            :param object: ``CfnFlow.AmplitudeSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-amplitudesourceproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''``CfnFlow.AmplitudeSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-amplitudesourceproperties.html#cfn-appflow-flow-amplitudesourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AmplitudeSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.ConnectorOperatorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "amplitude": "amplitude",
            "datadog": "datadog",
            "dynatrace": "dynatrace",
            "google_analytics": "googleAnalytics",
            "infor_nexus": "inforNexus",
            "marketo": "marketo",
            "s3": "s3",
            "salesforce": "salesforce",
            "service_now": "serviceNow",
            "singular": "singular",
            "slack": "slack",
            "trendmicro": "trendmicro",
            "veeva": "veeva",
            "zendesk": "zendesk",
        },
    )
    class ConnectorOperatorProperty:
        def __init__(
            self,
            *,
            amplitude: typing.Optional[builtins.str] = None,
            datadog: typing.Optional[builtins.str] = None,
            dynatrace: typing.Optional[builtins.str] = None,
            google_analytics: typing.Optional[builtins.str] = None,
            infor_nexus: typing.Optional[builtins.str] = None,
            marketo: typing.Optional[builtins.str] = None,
            s3: typing.Optional[builtins.str] = None,
            salesforce: typing.Optional[builtins.str] = None,
            service_now: typing.Optional[builtins.str] = None,
            singular: typing.Optional[builtins.str] = None,
            slack: typing.Optional[builtins.str] = None,
            trendmicro: typing.Optional[builtins.str] = None,
            veeva: typing.Optional[builtins.str] = None,
            zendesk: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param amplitude: ``CfnFlow.ConnectorOperatorProperty.Amplitude``.
            :param datadog: ``CfnFlow.ConnectorOperatorProperty.Datadog``.
            :param dynatrace: ``CfnFlow.ConnectorOperatorProperty.Dynatrace``.
            :param google_analytics: ``CfnFlow.ConnectorOperatorProperty.GoogleAnalytics``.
            :param infor_nexus: ``CfnFlow.ConnectorOperatorProperty.InforNexus``.
            :param marketo: ``CfnFlow.ConnectorOperatorProperty.Marketo``.
            :param s3: ``CfnFlow.ConnectorOperatorProperty.S3``.
            :param salesforce: ``CfnFlow.ConnectorOperatorProperty.Salesforce``.
            :param service_now: ``CfnFlow.ConnectorOperatorProperty.ServiceNow``.
            :param singular: ``CfnFlow.ConnectorOperatorProperty.Singular``.
            :param slack: ``CfnFlow.ConnectorOperatorProperty.Slack``.
            :param trendmicro: ``CfnFlow.ConnectorOperatorProperty.Trendmicro``.
            :param veeva: ``CfnFlow.ConnectorOperatorProperty.Veeva``.
            :param zendesk: ``CfnFlow.ConnectorOperatorProperty.Zendesk``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if amplitude is not None:
                self._values["amplitude"] = amplitude
            if datadog is not None:
                self._values["datadog"] = datadog
            if dynatrace is not None:
                self._values["dynatrace"] = dynatrace
            if google_analytics is not None:
                self._values["google_analytics"] = google_analytics
            if infor_nexus is not None:
                self._values["infor_nexus"] = infor_nexus
            if marketo is not None:
                self._values["marketo"] = marketo
            if s3 is not None:
                self._values["s3"] = s3
            if salesforce is not None:
                self._values["salesforce"] = salesforce
            if service_now is not None:
                self._values["service_now"] = service_now
            if singular is not None:
                self._values["singular"] = singular
            if slack is not None:
                self._values["slack"] = slack
            if trendmicro is not None:
                self._values["trendmicro"] = trendmicro
            if veeva is not None:
                self._values["veeva"] = veeva
            if zendesk is not None:
                self._values["zendesk"] = zendesk

        @builtins.property
        def amplitude(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.ConnectorOperatorProperty.Amplitude``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-amplitude
            '''
            result = self._values.get("amplitude")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def datadog(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.ConnectorOperatorProperty.Datadog``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-datadog
            '''
            result = self._values.get("datadog")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dynatrace(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.ConnectorOperatorProperty.Dynatrace``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-dynatrace
            '''
            result = self._values.get("dynatrace")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def google_analytics(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.ConnectorOperatorProperty.GoogleAnalytics``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-googleanalytics
            '''
            result = self._values.get("google_analytics")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def infor_nexus(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.ConnectorOperatorProperty.InforNexus``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-infornexus
            '''
            result = self._values.get("infor_nexus")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def marketo(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.ConnectorOperatorProperty.Marketo``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-marketo
            '''
            result = self._values.get("marketo")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.ConnectorOperatorProperty.S3``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def salesforce(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.ConnectorOperatorProperty.Salesforce``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-salesforce
            '''
            result = self._values.get("salesforce")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_now(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.ConnectorOperatorProperty.ServiceNow``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-servicenow
            '''
            result = self._values.get("service_now")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def singular(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.ConnectorOperatorProperty.Singular``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-singular
            '''
            result = self._values.get("singular")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def slack(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.ConnectorOperatorProperty.Slack``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-slack
            '''
            result = self._values.get("slack")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def trendmicro(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.ConnectorOperatorProperty.Trendmicro``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-trendmicro
            '''
            result = self._values.get("trendmicro")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def veeva(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.ConnectorOperatorProperty.Veeva``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-veeva
            '''
            result = self._values.get("veeva")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def zendesk(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.ConnectorOperatorProperty.Zendesk``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-connectoroperator.html#cfn-appflow-flow-connectoroperator-zendesk
            '''
            result = self._values.get("zendesk")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorOperatorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.DatadogSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class DatadogSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''
            :param object: ``CfnFlow.DatadogSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-datadogsourceproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''``CfnFlow.DatadogSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-datadogsourceproperties.html#cfn-appflow-flow-datadogsourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatadogSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.DestinationConnectorPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "event_bridge": "eventBridge",
            "redshift": "redshift",
            "s3": "s3",
            "salesforce": "salesforce",
            "snowflake": "snowflake",
            "upsolver": "upsolver",
        },
    )
    class DestinationConnectorPropertiesProperty:
        def __init__(
            self,
            *,
            event_bridge: typing.Optional[typing.Union["CfnFlow.EventBridgeDestinationPropertiesProperty", _IResolvable_a771d0ef]] = None,
            redshift: typing.Optional[typing.Union["CfnFlow.RedshiftDestinationPropertiesProperty", _IResolvable_a771d0ef]] = None,
            s3: typing.Optional[typing.Union["CfnFlow.S3DestinationPropertiesProperty", _IResolvable_a771d0ef]] = None,
            salesforce: typing.Optional[typing.Union["CfnFlow.SalesforceDestinationPropertiesProperty", _IResolvable_a771d0ef]] = None,
            snowflake: typing.Optional[typing.Union["CfnFlow.SnowflakeDestinationPropertiesProperty", _IResolvable_a771d0ef]] = None,
            upsolver: typing.Optional[typing.Union["CfnFlow.UpsolverDestinationPropertiesProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param event_bridge: ``CfnFlow.DestinationConnectorPropertiesProperty.EventBridge``.
            :param redshift: ``CfnFlow.DestinationConnectorPropertiesProperty.Redshift``.
            :param s3: ``CfnFlow.DestinationConnectorPropertiesProperty.S3``.
            :param salesforce: ``CfnFlow.DestinationConnectorPropertiesProperty.Salesforce``.
            :param snowflake: ``CfnFlow.DestinationConnectorPropertiesProperty.Snowflake``.
            :param upsolver: ``CfnFlow.DestinationConnectorPropertiesProperty.Upsolver``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if event_bridge is not None:
                self._values["event_bridge"] = event_bridge
            if redshift is not None:
                self._values["redshift"] = redshift
            if s3 is not None:
                self._values["s3"] = s3
            if salesforce is not None:
                self._values["salesforce"] = salesforce
            if snowflake is not None:
                self._values["snowflake"] = snowflake
            if upsolver is not None:
                self._values["upsolver"] = upsolver

        @builtins.property
        def event_bridge(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.EventBridgeDestinationPropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.DestinationConnectorPropertiesProperty.EventBridge``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-eventbridge
            '''
            result = self._values.get("event_bridge")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.EventBridgeDestinationPropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def redshift(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.RedshiftDestinationPropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.DestinationConnectorPropertiesProperty.Redshift``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-redshift
            '''
            result = self._values.get("redshift")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.RedshiftDestinationPropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.S3DestinationPropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.DestinationConnectorPropertiesProperty.S3``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.S3DestinationPropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def salesforce(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.SalesforceDestinationPropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.DestinationConnectorPropertiesProperty.Salesforce``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-salesforce
            '''
            result = self._values.get("salesforce")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.SalesforceDestinationPropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def snowflake(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.SnowflakeDestinationPropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.DestinationConnectorPropertiesProperty.Snowflake``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-snowflake
            '''
            result = self._values.get("snowflake")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.SnowflakeDestinationPropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def upsolver(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.UpsolverDestinationPropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.DestinationConnectorPropertiesProperty.Upsolver``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationconnectorproperties.html#cfn-appflow-flow-destinationconnectorproperties-upsolver
            '''
            result = self._values.get("upsolver")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.UpsolverDestinationPropertiesProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationConnectorPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.DestinationFlowConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connector_type": "connectorType",
            "destination_connector_properties": "destinationConnectorProperties",
            "connector_profile_name": "connectorProfileName",
        },
    )
    class DestinationFlowConfigProperty:
        def __init__(
            self,
            *,
            connector_type: builtins.str,
            destination_connector_properties: typing.Union["CfnFlow.DestinationConnectorPropertiesProperty", _IResolvable_a771d0ef],
            connector_profile_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param connector_type: ``CfnFlow.DestinationFlowConfigProperty.ConnectorType``.
            :param destination_connector_properties: ``CfnFlow.DestinationFlowConfigProperty.DestinationConnectorProperties``.
            :param connector_profile_name: ``CfnFlow.DestinationFlowConfigProperty.ConnectorProfileName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationflowconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "connector_type": connector_type,
                "destination_connector_properties": destination_connector_properties,
            }
            if connector_profile_name is not None:
                self._values["connector_profile_name"] = connector_profile_name

        @builtins.property
        def connector_type(self) -> builtins.str:
            '''``CfnFlow.DestinationFlowConfigProperty.ConnectorType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationflowconfig.html#cfn-appflow-flow-destinationflowconfig-connectortype
            '''
            result = self._values.get("connector_type")
            assert result is not None, "Required property 'connector_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def destination_connector_properties(
            self,
        ) -> typing.Union["CfnFlow.DestinationConnectorPropertiesProperty", _IResolvable_a771d0ef]:
            '''``CfnFlow.DestinationFlowConfigProperty.DestinationConnectorProperties``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationflowconfig.html#cfn-appflow-flow-destinationflowconfig-destinationconnectorproperties
            '''
            result = self._values.get("destination_connector_properties")
            assert result is not None, "Required property 'destination_connector_properties' is missing"
            return typing.cast(typing.Union["CfnFlow.DestinationConnectorPropertiesProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def connector_profile_name(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.DestinationFlowConfigProperty.ConnectorProfileName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-destinationflowconfig.html#cfn-appflow-flow-destinationflowconfig-connectorprofilename
            '''
            result = self._values.get("connector_profile_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationFlowConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.DynatraceSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class DynatraceSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''
            :param object: ``CfnFlow.DynatraceSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-dynatracesourceproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''``CfnFlow.DynatraceSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-dynatracesourceproperties.html#cfn-appflow-flow-dynatracesourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynatraceSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.ErrorHandlingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "bucket_prefix": "bucketPrefix",
            "fail_on_first_error": "failOnFirstError",
        },
    )
    class ErrorHandlingConfigProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            bucket_prefix: typing.Optional[builtins.str] = None,
            fail_on_first_error: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param bucket_name: ``CfnFlow.ErrorHandlingConfigProperty.BucketName``.
            :param bucket_prefix: ``CfnFlow.ErrorHandlingConfigProperty.BucketPrefix``.
            :param fail_on_first_error: ``CfnFlow.ErrorHandlingConfigProperty.FailOnFirstError``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-errorhandlingconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if fail_on_first_error is not None:
                self._values["fail_on_first_error"] = fail_on_first_error

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.ErrorHandlingConfigProperty.BucketName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-errorhandlingconfig.html#cfn-appflow-flow-errorhandlingconfig-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.ErrorHandlingConfigProperty.BucketPrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-errorhandlingconfig.html#cfn-appflow-flow-errorhandlingconfig-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def fail_on_first_error(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnFlow.ErrorHandlingConfigProperty.FailOnFirstError``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-errorhandlingconfig.html#cfn-appflow-flow-errorhandlingconfig-failonfirsterror
            '''
            result = self._values.get("fail_on_first_error")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ErrorHandlingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.EventBridgeDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "object": "object",
            "error_handling_config": "errorHandlingConfig",
        },
    )
    class EventBridgeDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            object: builtins.str,
            error_handling_config: typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param object: ``CfnFlow.EventBridgeDestinationPropertiesProperty.Object``.
            :param error_handling_config: ``CfnFlow.EventBridgeDestinationPropertiesProperty.ErrorHandlingConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-eventbridgedestinationproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "object": object,
            }
            if error_handling_config is not None:
                self._values["error_handling_config"] = error_handling_config

        @builtins.property
        def object(self) -> builtins.str:
            '''``CfnFlow.EventBridgeDestinationPropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-eventbridgedestinationproperties.html#cfn-appflow-flow-eventbridgedestinationproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def error_handling_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.EventBridgeDestinationPropertiesProperty.ErrorHandlingConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-eventbridgedestinationproperties.html#cfn-appflow-flow-eventbridgedestinationproperties-errorhandlingconfig
            '''
            result = self._values.get("error_handling_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventBridgeDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.GoogleAnalyticsSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class GoogleAnalyticsSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''
            :param object: ``CfnFlow.GoogleAnalyticsSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-googleanalyticssourceproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''``CfnFlow.GoogleAnalyticsSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-googleanalyticssourceproperties.html#cfn-appflow-flow-googleanalyticssourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GoogleAnalyticsSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.IdFieldNamesListProperty",
        jsii_struct_bases=[],
        name_mapping={"id_field_names_list": "idFieldNamesList"},
    )
    class IdFieldNamesListProperty:
        def __init__(
            self,
            *,
            id_field_names_list: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            '''
            :param id_field_names_list: ``CfnFlow.IdFieldNamesListProperty.IdFieldNamesList``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-idfieldnameslist.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if id_field_names_list is not None:
                self._values["id_field_names_list"] = id_field_names_list

        @builtins.property
        def id_field_names_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnFlow.IdFieldNamesListProperty.IdFieldNamesList``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-idfieldnameslist.html#cfn-appflow-flow-idfieldnameslist-idfieldnameslist
            '''
            result = self._values.get("id_field_names_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdFieldNamesListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.IncrementalPullConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"datetime_type_field_name": "datetimeTypeFieldName"},
    )
    class IncrementalPullConfigProperty:
        def __init__(
            self,
            *,
            datetime_type_field_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param datetime_type_field_name: ``CfnFlow.IncrementalPullConfigProperty.DatetimeTypeFieldName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-incrementalpullconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if datetime_type_field_name is not None:
                self._values["datetime_type_field_name"] = datetime_type_field_name

        @builtins.property
        def datetime_type_field_name(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.IncrementalPullConfigProperty.DatetimeTypeFieldName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-incrementalpullconfig.html#cfn-appflow-flow-incrementalpullconfig-datetimetypefieldname
            '''
            result = self._values.get("datetime_type_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IncrementalPullConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.InforNexusSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class InforNexusSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''
            :param object: ``CfnFlow.InforNexusSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-infornexussourceproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''``CfnFlow.InforNexusSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-infornexussourceproperties.html#cfn-appflow-flow-infornexussourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InforNexusSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.MarketoSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class MarketoSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''
            :param object: ``CfnFlow.MarketoSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-marketosourceproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''``CfnFlow.MarketoSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-marketosourceproperties.html#cfn-appflow-flow-marketosourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MarketoSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.PrefixConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"prefix_format": "prefixFormat", "prefix_type": "prefixType"},
    )
    class PrefixConfigProperty:
        def __init__(
            self,
            *,
            prefix_format: typing.Optional[builtins.str] = None,
            prefix_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param prefix_format: ``CfnFlow.PrefixConfigProperty.PrefixFormat``.
            :param prefix_type: ``CfnFlow.PrefixConfigProperty.PrefixType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-prefixconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if prefix_format is not None:
                self._values["prefix_format"] = prefix_format
            if prefix_type is not None:
                self._values["prefix_type"] = prefix_type

        @builtins.property
        def prefix_format(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.PrefixConfigProperty.PrefixFormat``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-prefixconfig.html#cfn-appflow-flow-prefixconfig-prefixformat
            '''
            result = self._values.get("prefix_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix_type(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.PrefixConfigProperty.PrefixType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-prefixconfig.html#cfn-appflow-flow-prefixconfig-prefixtype
            '''
            result = self._values.get("prefix_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrefixConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.RedshiftDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "intermediate_bucket_name": "intermediateBucketName",
            "object": "object",
            "bucket_prefix": "bucketPrefix",
            "error_handling_config": "errorHandlingConfig",
        },
    )
    class RedshiftDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            intermediate_bucket_name: builtins.str,
            object: builtins.str,
            bucket_prefix: typing.Optional[builtins.str] = None,
            error_handling_config: typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param intermediate_bucket_name: ``CfnFlow.RedshiftDestinationPropertiesProperty.IntermediateBucketName``.
            :param object: ``CfnFlow.RedshiftDestinationPropertiesProperty.Object``.
            :param bucket_prefix: ``CfnFlow.RedshiftDestinationPropertiesProperty.BucketPrefix``.
            :param error_handling_config: ``CfnFlow.RedshiftDestinationPropertiesProperty.ErrorHandlingConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-redshiftdestinationproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "intermediate_bucket_name": intermediate_bucket_name,
                "object": object,
            }
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if error_handling_config is not None:
                self._values["error_handling_config"] = error_handling_config

        @builtins.property
        def intermediate_bucket_name(self) -> builtins.str:
            '''``CfnFlow.RedshiftDestinationPropertiesProperty.IntermediateBucketName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-redshiftdestinationproperties.html#cfn-appflow-flow-redshiftdestinationproperties-intermediatebucketname
            '''
            result = self._values.get("intermediate_bucket_name")
            assert result is not None, "Required property 'intermediate_bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def object(self) -> builtins.str:
            '''``CfnFlow.RedshiftDestinationPropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-redshiftdestinationproperties.html#cfn-appflow-flow-redshiftdestinationproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.RedshiftDestinationPropertiesProperty.BucketPrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-redshiftdestinationproperties.html#cfn-appflow-flow-redshiftdestinationproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def error_handling_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.RedshiftDestinationPropertiesProperty.ErrorHandlingConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-redshiftdestinationproperties.html#cfn-appflow-flow-redshiftdestinationproperties-errorhandlingconfig
            '''
            result = self._values.get("error_handling_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedshiftDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.S3DestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "bucket_prefix": "bucketPrefix",
            "s3_output_format_config": "s3OutputFormatConfig",
        },
    )
    class S3DestinationPropertiesProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            bucket_prefix: typing.Optional[builtins.str] = None,
            s3_output_format_config: typing.Optional[typing.Union["CfnFlow.S3OutputFormatConfigProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param bucket_name: ``CfnFlow.S3DestinationPropertiesProperty.BucketName``.
            :param bucket_prefix: ``CfnFlow.S3DestinationPropertiesProperty.BucketPrefix``.
            :param s3_output_format_config: ``CfnFlow.S3DestinationPropertiesProperty.S3OutputFormatConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3destinationproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bucket_name": bucket_name,
            }
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if s3_output_format_config is not None:
                self._values["s3_output_format_config"] = s3_output_format_config

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''``CfnFlow.S3DestinationPropertiesProperty.BucketName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3destinationproperties.html#cfn-appflow-flow-s3destinationproperties-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.S3DestinationPropertiesProperty.BucketPrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3destinationproperties.html#cfn-appflow-flow-s3destinationproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_output_format_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.S3OutputFormatConfigProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.S3DestinationPropertiesProperty.S3OutputFormatConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3destinationproperties.html#cfn-appflow-flow-s3destinationproperties-s3outputformatconfig
            '''
            result = self._values.get("s3_output_format_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.S3OutputFormatConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3DestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.S3OutputFormatConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aggregation_config": "aggregationConfig",
            "file_type": "fileType",
            "prefix_config": "prefixConfig",
        },
    )
    class S3OutputFormatConfigProperty:
        def __init__(
            self,
            *,
            aggregation_config: typing.Optional[typing.Union["CfnFlow.AggregationConfigProperty", _IResolvable_a771d0ef]] = None,
            file_type: typing.Optional[builtins.str] = None,
            prefix_config: typing.Optional[typing.Union["CfnFlow.PrefixConfigProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param aggregation_config: ``CfnFlow.S3OutputFormatConfigProperty.AggregationConfig``.
            :param file_type: ``CfnFlow.S3OutputFormatConfigProperty.FileType``.
            :param prefix_config: ``CfnFlow.S3OutputFormatConfigProperty.PrefixConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3outputformatconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if aggregation_config is not None:
                self._values["aggregation_config"] = aggregation_config
            if file_type is not None:
                self._values["file_type"] = file_type
            if prefix_config is not None:
                self._values["prefix_config"] = prefix_config

        @builtins.property
        def aggregation_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.AggregationConfigProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.S3OutputFormatConfigProperty.AggregationConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3outputformatconfig.html#cfn-appflow-flow-s3outputformatconfig-aggregationconfig
            '''
            result = self._values.get("aggregation_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.AggregationConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def file_type(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.S3OutputFormatConfigProperty.FileType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3outputformatconfig.html#cfn-appflow-flow-s3outputformatconfig-filetype
            '''
            result = self._values.get("file_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.PrefixConfigProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.S3OutputFormatConfigProperty.PrefixConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3outputformatconfig.html#cfn-appflow-flow-s3outputformatconfig-prefixconfig
            '''
            result = self._values.get("prefix_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.PrefixConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3OutputFormatConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.S3SourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName", "bucket_prefix": "bucketPrefix"},
    )
    class S3SourcePropertiesProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            bucket_prefix: builtins.str,
        ) -> None:
            '''
            :param bucket_name: ``CfnFlow.S3SourcePropertiesProperty.BucketName``.
            :param bucket_prefix: ``CfnFlow.S3SourcePropertiesProperty.BucketPrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3sourceproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bucket_name": bucket_name,
                "bucket_prefix": bucket_prefix,
            }

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''``CfnFlow.S3SourcePropertiesProperty.BucketName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3sourceproperties.html#cfn-appflow-flow-s3sourceproperties-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def bucket_prefix(self) -> builtins.str:
            '''``CfnFlow.S3SourcePropertiesProperty.BucketPrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-s3sourceproperties.html#cfn-appflow-flow-s3sourceproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            assert result is not None, "Required property 'bucket_prefix' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3SourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.SalesforceDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "object": "object",
            "error_handling_config": "errorHandlingConfig",
            "id_field_names": "idFieldNames",
            "write_operation_type": "writeOperationType",
        },
    )
    class SalesforceDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            object: builtins.str,
            error_handling_config: typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]] = None,
            id_field_names: typing.Optional[typing.Union["CfnFlow.IdFieldNamesListProperty", _IResolvable_a771d0ef]] = None,
            write_operation_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param object: ``CfnFlow.SalesforceDestinationPropertiesProperty.Object``.
            :param error_handling_config: ``CfnFlow.SalesforceDestinationPropertiesProperty.ErrorHandlingConfig``.
            :param id_field_names: ``CfnFlow.SalesforceDestinationPropertiesProperty.IdFieldNames``.
            :param write_operation_type: ``CfnFlow.SalesforceDestinationPropertiesProperty.WriteOperationType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcedestinationproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "object": object,
            }
            if error_handling_config is not None:
                self._values["error_handling_config"] = error_handling_config
            if id_field_names is not None:
                self._values["id_field_names"] = id_field_names
            if write_operation_type is not None:
                self._values["write_operation_type"] = write_operation_type

        @builtins.property
        def object(self) -> builtins.str:
            '''``CfnFlow.SalesforceDestinationPropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcedestinationproperties.html#cfn-appflow-flow-salesforcedestinationproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def error_handling_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.SalesforceDestinationPropertiesProperty.ErrorHandlingConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcedestinationproperties.html#cfn-appflow-flow-salesforcedestinationproperties-errorhandlingconfig
            '''
            result = self._values.get("error_handling_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def id_field_names(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.IdFieldNamesListProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.SalesforceDestinationPropertiesProperty.IdFieldNames``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcedestinationproperties.html#cfn-appflow-flow-salesforcedestinationproperties-idfieldnames
            '''
            result = self._values.get("id_field_names")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.IdFieldNamesListProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def write_operation_type(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.SalesforceDestinationPropertiesProperty.WriteOperationType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcedestinationproperties.html#cfn-appflow-flow-salesforcedestinationproperties-writeoperationtype
            '''
            result = self._values.get("write_operation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.SalesforceSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "object": "object",
            "enable_dynamic_field_update": "enableDynamicFieldUpdate",
            "include_deleted_records": "includeDeletedRecords",
        },
    )
    class SalesforceSourcePropertiesProperty:
        def __init__(
            self,
            *,
            object: builtins.str,
            enable_dynamic_field_update: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            include_deleted_records: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param object: ``CfnFlow.SalesforceSourcePropertiesProperty.Object``.
            :param enable_dynamic_field_update: ``CfnFlow.SalesforceSourcePropertiesProperty.EnableDynamicFieldUpdate``.
            :param include_deleted_records: ``CfnFlow.SalesforceSourcePropertiesProperty.IncludeDeletedRecords``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcesourceproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "object": object,
            }
            if enable_dynamic_field_update is not None:
                self._values["enable_dynamic_field_update"] = enable_dynamic_field_update
            if include_deleted_records is not None:
                self._values["include_deleted_records"] = include_deleted_records

        @builtins.property
        def object(self) -> builtins.str:
            '''``CfnFlow.SalesforceSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcesourceproperties.html#cfn-appflow-flow-salesforcesourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def enable_dynamic_field_update(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnFlow.SalesforceSourcePropertiesProperty.EnableDynamicFieldUpdate``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcesourceproperties.html#cfn-appflow-flow-salesforcesourceproperties-enabledynamicfieldupdate
            '''
            result = self._values.get("enable_dynamic_field_update")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def include_deleted_records(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnFlow.SalesforceSourcePropertiesProperty.IncludeDeletedRecords``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-salesforcesourceproperties.html#cfn-appflow-flow-salesforcesourceproperties-includedeletedrecords
            '''
            result = self._values.get("include_deleted_records")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.ScheduledTriggerPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "schedule_expression": "scheduleExpression",
            "data_pull_mode": "dataPullMode",
            "schedule_end_time": "scheduleEndTime",
            "schedule_start_time": "scheduleStartTime",
            "time_zone": "timeZone",
        },
    )
    class ScheduledTriggerPropertiesProperty:
        def __init__(
            self,
            *,
            schedule_expression: builtins.str,
            data_pull_mode: typing.Optional[builtins.str] = None,
            schedule_end_time: typing.Optional[jsii.Number] = None,
            schedule_start_time: typing.Optional[jsii.Number] = None,
            time_zone: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param schedule_expression: ``CfnFlow.ScheduledTriggerPropertiesProperty.ScheduleExpression``.
            :param data_pull_mode: ``CfnFlow.ScheduledTriggerPropertiesProperty.DataPullMode``.
            :param schedule_end_time: ``CfnFlow.ScheduledTriggerPropertiesProperty.ScheduleEndTime``.
            :param schedule_start_time: ``CfnFlow.ScheduledTriggerPropertiesProperty.ScheduleStartTime``.
            :param time_zone: ``CfnFlow.ScheduledTriggerPropertiesProperty.TimeZone``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "schedule_expression": schedule_expression,
            }
            if data_pull_mode is not None:
                self._values["data_pull_mode"] = data_pull_mode
            if schedule_end_time is not None:
                self._values["schedule_end_time"] = schedule_end_time
            if schedule_start_time is not None:
                self._values["schedule_start_time"] = schedule_start_time
            if time_zone is not None:
                self._values["time_zone"] = time_zone

        @builtins.property
        def schedule_expression(self) -> builtins.str:
            '''``CfnFlow.ScheduledTriggerPropertiesProperty.ScheduleExpression``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html#cfn-appflow-flow-scheduledtriggerproperties-scheduleexpression
            '''
            result = self._values.get("schedule_expression")
            assert result is not None, "Required property 'schedule_expression' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def data_pull_mode(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.ScheduledTriggerPropertiesProperty.DataPullMode``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html#cfn-appflow-flow-scheduledtriggerproperties-datapullmode
            '''
            result = self._values.get("data_pull_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def schedule_end_time(self) -> typing.Optional[jsii.Number]:
            '''``CfnFlow.ScheduledTriggerPropertiesProperty.ScheduleEndTime``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html#cfn-appflow-flow-scheduledtriggerproperties-scheduleendtime
            '''
            result = self._values.get("schedule_end_time")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def schedule_start_time(self) -> typing.Optional[jsii.Number]:
            '''``CfnFlow.ScheduledTriggerPropertiesProperty.ScheduleStartTime``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html#cfn-appflow-flow-scheduledtriggerproperties-schedulestarttime
            '''
            result = self._values.get("schedule_start_time")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def time_zone(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.ScheduledTriggerPropertiesProperty.TimeZone``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-scheduledtriggerproperties.html#cfn-appflow-flow-scheduledtriggerproperties-timezone
            '''
            result = self._values.get("time_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduledTriggerPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.ServiceNowSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class ServiceNowSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''
            :param object: ``CfnFlow.ServiceNowSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-servicenowsourceproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''``CfnFlow.ServiceNowSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-servicenowsourceproperties.html#cfn-appflow-flow-servicenowsourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceNowSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.SingularSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class SingularSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''
            :param object: ``CfnFlow.SingularSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-singularsourceproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''``CfnFlow.SingularSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-singularsourceproperties.html#cfn-appflow-flow-singularsourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SingularSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.SlackSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class SlackSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''
            :param object: ``CfnFlow.SlackSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-slacksourceproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''``CfnFlow.SlackSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-slacksourceproperties.html#cfn-appflow-flow-slacksourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlackSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.SnowflakeDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "intermediate_bucket_name": "intermediateBucketName",
            "object": "object",
            "bucket_prefix": "bucketPrefix",
            "error_handling_config": "errorHandlingConfig",
        },
    )
    class SnowflakeDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            intermediate_bucket_name: builtins.str,
            object: builtins.str,
            bucket_prefix: typing.Optional[builtins.str] = None,
            error_handling_config: typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param intermediate_bucket_name: ``CfnFlow.SnowflakeDestinationPropertiesProperty.IntermediateBucketName``.
            :param object: ``CfnFlow.SnowflakeDestinationPropertiesProperty.Object``.
            :param bucket_prefix: ``CfnFlow.SnowflakeDestinationPropertiesProperty.BucketPrefix``.
            :param error_handling_config: ``CfnFlow.SnowflakeDestinationPropertiesProperty.ErrorHandlingConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-snowflakedestinationproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "intermediate_bucket_name": intermediate_bucket_name,
                "object": object,
            }
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if error_handling_config is not None:
                self._values["error_handling_config"] = error_handling_config

        @builtins.property
        def intermediate_bucket_name(self) -> builtins.str:
            '''``CfnFlow.SnowflakeDestinationPropertiesProperty.IntermediateBucketName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-snowflakedestinationproperties.html#cfn-appflow-flow-snowflakedestinationproperties-intermediatebucketname
            '''
            result = self._values.get("intermediate_bucket_name")
            assert result is not None, "Required property 'intermediate_bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def object(self) -> builtins.str:
            '''``CfnFlow.SnowflakeDestinationPropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-snowflakedestinationproperties.html#cfn-appflow-flow-snowflakedestinationproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.SnowflakeDestinationPropertiesProperty.BucketPrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-snowflakedestinationproperties.html#cfn-appflow-flow-snowflakedestinationproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def error_handling_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.SnowflakeDestinationPropertiesProperty.ErrorHandlingConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-snowflakedestinationproperties.html#cfn-appflow-flow-snowflakedestinationproperties-errorhandlingconfig
            '''
            result = self._values.get("error_handling_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.ErrorHandlingConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnowflakeDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.SourceConnectorPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "amplitude": "amplitude",
            "datadog": "datadog",
            "dynatrace": "dynatrace",
            "google_analytics": "googleAnalytics",
            "infor_nexus": "inforNexus",
            "marketo": "marketo",
            "s3": "s3",
            "salesforce": "salesforce",
            "service_now": "serviceNow",
            "singular": "singular",
            "slack": "slack",
            "trendmicro": "trendmicro",
            "veeva": "veeva",
            "zendesk": "zendesk",
        },
    )
    class SourceConnectorPropertiesProperty:
        def __init__(
            self,
            *,
            amplitude: typing.Optional[typing.Union["CfnFlow.AmplitudeSourcePropertiesProperty", _IResolvable_a771d0ef]] = None,
            datadog: typing.Optional[typing.Union["CfnFlow.DatadogSourcePropertiesProperty", _IResolvable_a771d0ef]] = None,
            dynatrace: typing.Optional[typing.Union["CfnFlow.DynatraceSourcePropertiesProperty", _IResolvable_a771d0ef]] = None,
            google_analytics: typing.Optional[typing.Union["CfnFlow.GoogleAnalyticsSourcePropertiesProperty", _IResolvable_a771d0ef]] = None,
            infor_nexus: typing.Optional[typing.Union["CfnFlow.InforNexusSourcePropertiesProperty", _IResolvable_a771d0ef]] = None,
            marketo: typing.Optional[typing.Union["CfnFlow.MarketoSourcePropertiesProperty", _IResolvable_a771d0ef]] = None,
            s3: typing.Optional[typing.Union["CfnFlow.S3SourcePropertiesProperty", _IResolvable_a771d0ef]] = None,
            salesforce: typing.Optional[typing.Union["CfnFlow.SalesforceSourcePropertiesProperty", _IResolvable_a771d0ef]] = None,
            service_now: typing.Optional[typing.Union["CfnFlow.ServiceNowSourcePropertiesProperty", _IResolvable_a771d0ef]] = None,
            singular: typing.Optional[typing.Union["CfnFlow.SingularSourcePropertiesProperty", _IResolvable_a771d0ef]] = None,
            slack: typing.Optional[typing.Union["CfnFlow.SlackSourcePropertiesProperty", _IResolvable_a771d0ef]] = None,
            trendmicro: typing.Optional[typing.Union["CfnFlow.TrendmicroSourcePropertiesProperty", _IResolvable_a771d0ef]] = None,
            veeva: typing.Optional[typing.Union["CfnFlow.VeevaSourcePropertiesProperty", _IResolvable_a771d0ef]] = None,
            zendesk: typing.Optional[typing.Union["CfnFlow.ZendeskSourcePropertiesProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param amplitude: ``CfnFlow.SourceConnectorPropertiesProperty.Amplitude``.
            :param datadog: ``CfnFlow.SourceConnectorPropertiesProperty.Datadog``.
            :param dynatrace: ``CfnFlow.SourceConnectorPropertiesProperty.Dynatrace``.
            :param google_analytics: ``CfnFlow.SourceConnectorPropertiesProperty.GoogleAnalytics``.
            :param infor_nexus: ``CfnFlow.SourceConnectorPropertiesProperty.InforNexus``.
            :param marketo: ``CfnFlow.SourceConnectorPropertiesProperty.Marketo``.
            :param s3: ``CfnFlow.SourceConnectorPropertiesProperty.S3``.
            :param salesforce: ``CfnFlow.SourceConnectorPropertiesProperty.Salesforce``.
            :param service_now: ``CfnFlow.SourceConnectorPropertiesProperty.ServiceNow``.
            :param singular: ``CfnFlow.SourceConnectorPropertiesProperty.Singular``.
            :param slack: ``CfnFlow.SourceConnectorPropertiesProperty.Slack``.
            :param trendmicro: ``CfnFlow.SourceConnectorPropertiesProperty.Trendmicro``.
            :param veeva: ``CfnFlow.SourceConnectorPropertiesProperty.Veeva``.
            :param zendesk: ``CfnFlow.SourceConnectorPropertiesProperty.Zendesk``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if amplitude is not None:
                self._values["amplitude"] = amplitude
            if datadog is not None:
                self._values["datadog"] = datadog
            if dynatrace is not None:
                self._values["dynatrace"] = dynatrace
            if google_analytics is not None:
                self._values["google_analytics"] = google_analytics
            if infor_nexus is not None:
                self._values["infor_nexus"] = infor_nexus
            if marketo is not None:
                self._values["marketo"] = marketo
            if s3 is not None:
                self._values["s3"] = s3
            if salesforce is not None:
                self._values["salesforce"] = salesforce
            if service_now is not None:
                self._values["service_now"] = service_now
            if singular is not None:
                self._values["singular"] = singular
            if slack is not None:
                self._values["slack"] = slack
            if trendmicro is not None:
                self._values["trendmicro"] = trendmicro
            if veeva is not None:
                self._values["veeva"] = veeva
            if zendesk is not None:
                self._values["zendesk"] = zendesk

        @builtins.property
        def amplitude(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.AmplitudeSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.SourceConnectorPropertiesProperty.Amplitude``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-amplitude
            '''
            result = self._values.get("amplitude")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.AmplitudeSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def datadog(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.DatadogSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.SourceConnectorPropertiesProperty.Datadog``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-datadog
            '''
            result = self._values.get("datadog")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.DatadogSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def dynatrace(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.DynatraceSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.SourceConnectorPropertiesProperty.Dynatrace``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-dynatrace
            '''
            result = self._values.get("dynatrace")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.DynatraceSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def google_analytics(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.GoogleAnalyticsSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.SourceConnectorPropertiesProperty.GoogleAnalytics``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-googleanalytics
            '''
            result = self._values.get("google_analytics")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.GoogleAnalyticsSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def infor_nexus(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.InforNexusSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.SourceConnectorPropertiesProperty.InforNexus``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-infornexus
            '''
            result = self._values.get("infor_nexus")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.InforNexusSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def marketo(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.MarketoSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.SourceConnectorPropertiesProperty.Marketo``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-marketo
            '''
            result = self._values.get("marketo")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.MarketoSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.S3SourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.SourceConnectorPropertiesProperty.S3``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.S3SourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def salesforce(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.SalesforceSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.SourceConnectorPropertiesProperty.Salesforce``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-salesforce
            '''
            result = self._values.get("salesforce")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.SalesforceSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def service_now(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.ServiceNowSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.SourceConnectorPropertiesProperty.ServiceNow``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-servicenow
            '''
            result = self._values.get("service_now")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.ServiceNowSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def singular(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.SingularSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.SourceConnectorPropertiesProperty.Singular``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-singular
            '''
            result = self._values.get("singular")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.SingularSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def slack(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.SlackSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.SourceConnectorPropertiesProperty.Slack``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-slack
            '''
            result = self._values.get("slack")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.SlackSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def trendmicro(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.TrendmicroSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.SourceConnectorPropertiesProperty.Trendmicro``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-trendmicro
            '''
            result = self._values.get("trendmicro")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.TrendmicroSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def veeva(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.VeevaSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.SourceConnectorPropertiesProperty.Veeva``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-veeva
            '''
            result = self._values.get("veeva")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.VeevaSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def zendesk(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.ZendeskSourcePropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.SourceConnectorPropertiesProperty.Zendesk``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceconnectorproperties.html#cfn-appflow-flow-sourceconnectorproperties-zendesk
            '''
            result = self._values.get("zendesk")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.ZendeskSourcePropertiesProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceConnectorPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.SourceFlowConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connector_type": "connectorType",
            "source_connector_properties": "sourceConnectorProperties",
            "connector_profile_name": "connectorProfileName",
            "incremental_pull_config": "incrementalPullConfig",
        },
    )
    class SourceFlowConfigProperty:
        def __init__(
            self,
            *,
            connector_type: builtins.str,
            source_connector_properties: typing.Union["CfnFlow.SourceConnectorPropertiesProperty", _IResolvable_a771d0ef],
            connector_profile_name: typing.Optional[builtins.str] = None,
            incremental_pull_config: typing.Optional[typing.Union["CfnFlow.IncrementalPullConfigProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param connector_type: ``CfnFlow.SourceFlowConfigProperty.ConnectorType``.
            :param source_connector_properties: ``CfnFlow.SourceFlowConfigProperty.SourceConnectorProperties``.
            :param connector_profile_name: ``CfnFlow.SourceFlowConfigProperty.ConnectorProfileName``.
            :param incremental_pull_config: ``CfnFlow.SourceFlowConfigProperty.IncrementalPullConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceflowconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "connector_type": connector_type,
                "source_connector_properties": source_connector_properties,
            }
            if connector_profile_name is not None:
                self._values["connector_profile_name"] = connector_profile_name
            if incremental_pull_config is not None:
                self._values["incremental_pull_config"] = incremental_pull_config

        @builtins.property
        def connector_type(self) -> builtins.str:
            '''``CfnFlow.SourceFlowConfigProperty.ConnectorType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceflowconfig.html#cfn-appflow-flow-sourceflowconfig-connectortype
            '''
            result = self._values.get("connector_type")
            assert result is not None, "Required property 'connector_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def source_connector_properties(
            self,
        ) -> typing.Union["CfnFlow.SourceConnectorPropertiesProperty", _IResolvable_a771d0ef]:
            '''``CfnFlow.SourceFlowConfigProperty.SourceConnectorProperties``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceflowconfig.html#cfn-appflow-flow-sourceflowconfig-sourceconnectorproperties
            '''
            result = self._values.get("source_connector_properties")
            assert result is not None, "Required property 'source_connector_properties' is missing"
            return typing.cast(typing.Union["CfnFlow.SourceConnectorPropertiesProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def connector_profile_name(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.SourceFlowConfigProperty.ConnectorProfileName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceflowconfig.html#cfn-appflow-flow-sourceflowconfig-connectorprofilename
            '''
            result = self._values.get("connector_profile_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def incremental_pull_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.IncrementalPullConfigProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.SourceFlowConfigProperty.IncrementalPullConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-sourceflowconfig.html#cfn-appflow-flow-sourceflowconfig-incrementalpullconfig
            '''
            result = self._values.get("incremental_pull_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.IncrementalPullConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceFlowConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.TaskPropertiesObjectProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TaskPropertiesObjectProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''
            :param key: ``CfnFlow.TaskPropertiesObjectProperty.Key``.
            :param value: ``CfnFlow.TaskPropertiesObjectProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-taskpropertiesobject.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnFlow.TaskPropertiesObjectProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-taskpropertiesobject.html#cfn-appflow-flow-taskpropertiesobject-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''``CfnFlow.TaskPropertiesObjectProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-taskpropertiesobject.html#cfn-appflow-flow-taskpropertiesobject-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaskPropertiesObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.TaskProperty",
        jsii_struct_bases=[],
        name_mapping={
            "source_fields": "sourceFields",
            "task_type": "taskType",
            "connector_operator": "connectorOperator",
            "destination_field": "destinationField",
            "task_properties": "taskProperties",
        },
    )
    class TaskProperty:
        def __init__(
            self,
            *,
            source_fields: typing.List[builtins.str],
            task_type: builtins.str,
            connector_operator: typing.Optional[typing.Union["CfnFlow.ConnectorOperatorProperty", _IResolvable_a771d0ef]] = None,
            destination_field: typing.Optional[builtins.str] = None,
            task_properties: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFlow.TaskPropertiesObjectProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param source_fields: ``CfnFlow.TaskProperty.SourceFields``.
            :param task_type: ``CfnFlow.TaskProperty.TaskType``.
            :param connector_operator: ``CfnFlow.TaskProperty.ConnectorOperator``.
            :param destination_field: ``CfnFlow.TaskProperty.DestinationField``.
            :param task_properties: ``CfnFlow.TaskProperty.TaskProperties``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-task.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "source_fields": source_fields,
                "task_type": task_type,
            }
            if connector_operator is not None:
                self._values["connector_operator"] = connector_operator
            if destination_field is not None:
                self._values["destination_field"] = destination_field
            if task_properties is not None:
                self._values["task_properties"] = task_properties

        @builtins.property
        def source_fields(self) -> typing.List[builtins.str]:
            '''``CfnFlow.TaskProperty.SourceFields``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-task.html#cfn-appflow-flow-task-sourcefields
            '''
            result = self._values.get("source_fields")
            assert result is not None, "Required property 'source_fields' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def task_type(self) -> builtins.str:
            '''``CfnFlow.TaskProperty.TaskType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-task.html#cfn-appflow-flow-task-tasktype
            '''
            result = self._values.get("task_type")
            assert result is not None, "Required property 'task_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def connector_operator(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.ConnectorOperatorProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.TaskProperty.ConnectorOperator``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-task.html#cfn-appflow-flow-task-connectoroperator
            '''
            result = self._values.get("connector_operator")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.ConnectorOperatorProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def destination_field(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.TaskProperty.DestinationField``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-task.html#cfn-appflow-flow-task-destinationfield
            '''
            result = self._values.get("destination_field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def task_properties(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFlow.TaskPropertiesObjectProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnFlow.TaskProperty.TaskProperties``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-task.html#cfn-appflow-flow-task-taskproperties
            '''
            result = self._values.get("task_properties")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFlow.TaskPropertiesObjectProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaskProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.TrendmicroSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class TrendmicroSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''
            :param object: ``CfnFlow.TrendmicroSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-trendmicrosourceproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''``CfnFlow.TrendmicroSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-trendmicrosourceproperties.html#cfn-appflow-flow-trendmicrosourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TrendmicroSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.TriggerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "trigger_type": "triggerType",
            "trigger_properties": "triggerProperties",
        },
    )
    class TriggerConfigProperty:
        def __init__(
            self,
            *,
            trigger_type: builtins.str,
            trigger_properties: typing.Optional[typing.Union["CfnFlow.ScheduledTriggerPropertiesProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param trigger_type: ``CfnFlow.TriggerConfigProperty.TriggerType``.
            :param trigger_properties: ``CfnFlow.TriggerConfigProperty.TriggerProperties``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-triggerconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "trigger_type": trigger_type,
            }
            if trigger_properties is not None:
                self._values["trigger_properties"] = trigger_properties

        @builtins.property
        def trigger_type(self) -> builtins.str:
            '''``CfnFlow.TriggerConfigProperty.TriggerType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-triggerconfig.html#cfn-appflow-flow-triggerconfig-triggertype
            '''
            result = self._values.get("trigger_type")
            assert result is not None, "Required property 'trigger_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def trigger_properties(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.ScheduledTriggerPropertiesProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.TriggerConfigProperty.TriggerProperties``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-triggerconfig.html#cfn-appflow-flow-triggerconfig-triggerproperties
            '''
            result = self._values.get("trigger_properties")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.ScheduledTriggerPropertiesProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TriggerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.UpsolverDestinationPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "s3_output_format_config": "s3OutputFormatConfig",
            "bucket_prefix": "bucketPrefix",
        },
    )
    class UpsolverDestinationPropertiesProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            s3_output_format_config: typing.Union["CfnFlow.UpsolverS3OutputFormatConfigProperty", _IResolvable_a771d0ef],
            bucket_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param bucket_name: ``CfnFlow.UpsolverDestinationPropertiesProperty.BucketName``.
            :param s3_output_format_config: ``CfnFlow.UpsolverDestinationPropertiesProperty.S3OutputFormatConfig``.
            :param bucket_prefix: ``CfnFlow.UpsolverDestinationPropertiesProperty.BucketPrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolverdestinationproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bucket_name": bucket_name,
                "s3_output_format_config": s3_output_format_config,
            }
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''``CfnFlow.UpsolverDestinationPropertiesProperty.BucketName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolverdestinationproperties.html#cfn-appflow-flow-upsolverdestinationproperties-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_output_format_config(
            self,
        ) -> typing.Union["CfnFlow.UpsolverS3OutputFormatConfigProperty", _IResolvable_a771d0ef]:
            '''``CfnFlow.UpsolverDestinationPropertiesProperty.S3OutputFormatConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolverdestinationproperties.html#cfn-appflow-flow-upsolverdestinationproperties-s3outputformatconfig
            '''
            result = self._values.get("s3_output_format_config")
            assert result is not None, "Required property 's3_output_format_config' is missing"
            return typing.cast(typing.Union["CfnFlow.UpsolverS3OutputFormatConfigProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.UpsolverDestinationPropertiesProperty.BucketPrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolverdestinationproperties.html#cfn-appflow-flow-upsolverdestinationproperties-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UpsolverDestinationPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.UpsolverS3OutputFormatConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "prefix_config": "prefixConfig",
            "aggregation_config": "aggregationConfig",
            "file_type": "fileType",
        },
    )
    class UpsolverS3OutputFormatConfigProperty:
        def __init__(
            self,
            *,
            prefix_config: typing.Union["CfnFlow.PrefixConfigProperty", _IResolvable_a771d0ef],
            aggregation_config: typing.Optional[typing.Union["CfnFlow.AggregationConfigProperty", _IResolvable_a771d0ef]] = None,
            file_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param prefix_config: ``CfnFlow.UpsolverS3OutputFormatConfigProperty.PrefixConfig``.
            :param aggregation_config: ``CfnFlow.UpsolverS3OutputFormatConfigProperty.AggregationConfig``.
            :param file_type: ``CfnFlow.UpsolverS3OutputFormatConfigProperty.FileType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolvers3outputformatconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "prefix_config": prefix_config,
            }
            if aggregation_config is not None:
                self._values["aggregation_config"] = aggregation_config
            if file_type is not None:
                self._values["file_type"] = file_type

        @builtins.property
        def prefix_config(
            self,
        ) -> typing.Union["CfnFlow.PrefixConfigProperty", _IResolvable_a771d0ef]:
            '''``CfnFlow.UpsolverS3OutputFormatConfigProperty.PrefixConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolvers3outputformatconfig.html#cfn-appflow-flow-upsolvers3outputformatconfig-prefixconfig
            '''
            result = self._values.get("prefix_config")
            assert result is not None, "Required property 'prefix_config' is missing"
            return typing.cast(typing.Union["CfnFlow.PrefixConfigProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def aggregation_config(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.AggregationConfigProperty", _IResolvable_a771d0ef]]:
            '''``CfnFlow.UpsolverS3OutputFormatConfigProperty.AggregationConfig``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolvers3outputformatconfig.html#cfn-appflow-flow-upsolvers3outputformatconfig-aggregationconfig
            '''
            result = self._values.get("aggregation_config")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.AggregationConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def file_type(self) -> typing.Optional[builtins.str]:
            '''``CfnFlow.UpsolverS3OutputFormatConfigProperty.FileType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-upsolvers3outputformatconfig.html#cfn-appflow-flow-upsolvers3outputformatconfig-filetype
            '''
            result = self._values.get("file_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UpsolverS3OutputFormatConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.VeevaSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class VeevaSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''
            :param object: ``CfnFlow.VeevaSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-veevasourceproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''``CfnFlow.VeevaSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-veevasourceproperties.html#cfn-appflow-flow-veevasourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VeevaSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appflow.CfnFlow.ZendeskSourcePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"object": "object"},
    )
    class ZendeskSourcePropertiesProperty:
        def __init__(self, *, object: builtins.str) -> None:
            '''
            :param object: ``CfnFlow.ZendeskSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-zendesksourceproperties.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "object": object,
            }

        @builtins.property
        def object(self) -> builtins.str:
            '''``CfnFlow.ZendeskSourcePropertiesProperty.Object``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appflow-flow-zendesksourceproperties.html#cfn-appflow-flow-zendesksourceproperties-object
            '''
            result = self._values.get("object")
            assert result is not None, "Required property 'object' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZendeskSourcePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_appflow.CfnFlowProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_flow_config_list": "destinationFlowConfigList",
        "flow_name": "flowName",
        "source_flow_config": "sourceFlowConfig",
        "tasks": "tasks",
        "trigger_config": "triggerConfig",
        "description": "description",
        "kms_arn": "kmsArn",
        "tags": "tags",
    },
)
class CfnFlowProps:
    def __init__(
        self,
        *,
        destination_flow_config_list: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFlow.DestinationFlowConfigProperty, _IResolvable_a771d0ef]]],
        flow_name: builtins.str,
        source_flow_config: typing.Union[CfnFlow.SourceFlowConfigProperty, _IResolvable_a771d0ef],
        tasks: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFlow.TaskProperty, _IResolvable_a771d0ef]]],
        trigger_config: typing.Union[CfnFlow.TriggerConfigProperty, _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        kms_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::AppFlow::Flow``.

        :param destination_flow_config_list: ``AWS::AppFlow::Flow.DestinationFlowConfigList``.
        :param flow_name: ``AWS::AppFlow::Flow.FlowName``.
        :param source_flow_config: ``AWS::AppFlow::Flow.SourceFlowConfig``.
        :param tasks: ``AWS::AppFlow::Flow.Tasks``.
        :param trigger_config: ``AWS::AppFlow::Flow.TriggerConfig``.
        :param description: ``AWS::AppFlow::Flow.Description``.
        :param kms_arn: ``AWS::AppFlow::Flow.KMSArn``.
        :param tags: ``AWS::AppFlow::Flow.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "destination_flow_config_list": destination_flow_config_list,
            "flow_name": flow_name,
            "source_flow_config": source_flow_config,
            "tasks": tasks,
            "trigger_config": trigger_config,
        }
        if description is not None:
            self._values["description"] = description
        if kms_arn is not None:
            self._values["kms_arn"] = kms_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def destination_flow_config_list(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFlow.DestinationFlowConfigProperty, _IResolvable_a771d0ef]]]:
        '''``AWS::AppFlow::Flow.DestinationFlowConfigList``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-destinationflowconfiglist
        '''
        result = self._values.get("destination_flow_config_list")
        assert result is not None, "Required property 'destination_flow_config_list' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFlow.DestinationFlowConfigProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def flow_name(self) -> builtins.str:
        '''``AWS::AppFlow::Flow.FlowName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-flowname
        '''
        result = self._values.get("flow_name")
        assert result is not None, "Required property 'flow_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_flow_config(
        self,
    ) -> typing.Union[CfnFlow.SourceFlowConfigProperty, _IResolvable_a771d0ef]:
        '''``AWS::AppFlow::Flow.SourceFlowConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-sourceflowconfig
        '''
        result = self._values.get("source_flow_config")
        assert result is not None, "Required property 'source_flow_config' is missing"
        return typing.cast(typing.Union[CfnFlow.SourceFlowConfigProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def tasks(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFlow.TaskProperty, _IResolvable_a771d0ef]]]:
        '''``AWS::AppFlow::Flow.Tasks``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-tasks
        '''
        result = self._values.get("tasks")
        assert result is not None, "Required property 'tasks' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFlow.TaskProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def trigger_config(
        self,
    ) -> typing.Union[CfnFlow.TriggerConfigProperty, _IResolvable_a771d0ef]:
        '''``AWS::AppFlow::Flow.TriggerConfig``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-triggerconfig
        '''
        result = self._values.get("trigger_config")
        assert result is not None, "Required property 'trigger_config' is missing"
        return typing.cast(typing.Union[CfnFlow.TriggerConfigProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppFlow::Flow.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::AppFlow::Flow.KMSArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-kmsarn
        '''
        result = self._values.get("kms_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::AppFlow::Flow.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appflow-flow.html#cfn-appflow-flow-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFlowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnConnectorProfile",
    "CfnConnectorProfileProps",
    "CfnFlow",
    "CfnFlowProps",
]

publication.publish()
