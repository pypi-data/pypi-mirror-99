'''
# Include CloudFormation templates in the CDK

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This module contains a set of classes whose goal is to facilitate working
with existing CloudFormation templates in the CDK.
It can be thought of as an extension of the capabilities of the
[`CfnInclude` class](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.CfnInclude.html).

## Basic usage

Assume we have a file with an existing template.
It could be in JSON format, in a file `my-template.json`:

```json
{
  "Resources": {
    "Bucket": {
      "Type": "AWS::S3::Bucket",
      "Properties": {
        "BucketName": "some-bucket-name"
      }
    }
  }
}
```

Or it could by in YAML format, in a file `my-template.yaml`:

```yaml
Resources:
  Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: some-bucket-name
```

It can be included in a CDK application with the following code:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.cloudformation_include as cfn_inc

cfn_template = cfn_inc.CfnInclude(self, "Template",
    template_file="my-template.json"
)
```

Or, if your template uses YAML:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cfn_template = cfn_inc.CfnInclude(self, "Template",
    template_file="my-template.yaml"
)
```

**Note**: different YAML parsers sometimes don't agree on what exactly constitutes valid YAML.
If you get a YAML exception when including your template,
try converting it to JSON, and including that file instead.
If you're downloading your template from the CloudFormation AWS Console,
you can easily get it in JSON format by clicking the 'View in Designer'
button on the 'Template' tab -
once in Designer, select JSON in the "Choose template language"
radio buttons on the bottom pane.

This will add all resources from `my-template.json` / `my-template.yaml` into the CDK application,
preserving their original logical IDs from the template file.

Note that this including process will *not* execute any
[CloudFormation transforms](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-macros.html) -
including the [Serverless transform](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/transform-aws-serverless.html).

Any resource from the included template can be retrieved by referring to it by its logical ID from the template.
If you know the class of the CDK object that corresponds to that resource,
you can cast the returned object to the correct type:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_s3 as s3

cfn_bucket = cfn_template.get_resource("Bucket")
```

Note that any resources not present in the latest version of the CloudFormation schema
at the time of publishing the version of this module that you depend on,
including [Custom Resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html),
will be returned as instances of the class `CfnResource`,
and so cannot be cast to a different resource type.

Any modifications made to that resource will be reflected in the resulting CDK template;
for example, the name of the bucket can be changed:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cfn_bucket.bucket_name = "my-bucket-name"
```

You can also refer to the resource when defining other constructs,
including the higher-level ones
(those whose name does not start with `Cfn`),
for example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_iam as iam

role = iam.Role(self, "Role",
    assumed_by=iam.AnyPrincipal()
)
role.add_to_policy(iam.PolicyStatement(
    actions=["s3:*"],
    resources=[cfn_bucket.attr_arn]
))
```

If you need, you can also convert the CloudFormation resource to a higher-level
resource by importing it:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = s3.Bucket.from_bucket_name(self, "L2Bucket", cfn_bucket.ref)
```

## Non-resource template elements

In addition to resources,
you can also retrieve and mutate all other template elements:

* [Parameters](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html):

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  import aws_cdk.core as core

  param = cfn_template.get_parameter("MyParameter")

  # mutating the parameter
  param.default = "MyDefault"
  ```
* [Conditions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/conditions-section-structure.html):

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  import aws_cdk.core as core

  condition = cfn_template.get_condition("MyCondition")

  # mutating the condition
  condition.expression = core.Fn.condition_equals(1, 2)
  ```
* [Mappings](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/mappings-section-structure.html):

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  import aws_cdk.core as core

  mapping = cfn_template.get_mapping("MyMapping")

  # mutating the mapping
  mapping.set_value("my-region", "AMI", "ami-04681a1dbd79675a5")
  ```
* [Service Catalog template Rules](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/reference-template_constraint_rules.html):

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  import aws_cdk.core as core

  rule = cfn_template.get_rule("MyRule")

  # mutating the rule
  rule.add_assertion(core.Fn.condition_contains(["m1.small"], my_parameter.value), "MyParameter has to be m1.small")
  ```
* [Outputs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html):

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  import aws_cdk.core as core

  output = cfn_template.get_output("MyOutput")

  # mutating the output
  output.value = cfn_bucket.attr_arn
  ```
* [Hooks for blue-green deployments](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/blue-green.html):

  ```python
  # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
  import aws_cdk.core as core

  hook = cfn_template.get_hook("MyOutput")

  # mutating the hook
  code_deploy_hook = hook
  code_deploy_hook.service_role = my_role.role_arn
  ```

## Parameter replacement

If your existing template uses CloudFormation Parameters,
you may want to remove them in favor of build-time values.
You can do that using the `parameters` property:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
inc.CfnInclude(self, "includeTemplate",
    template_file="path/to/my/template",
    parameters={
        "MyParam": "my-value"
    }
)
```

This will replace all references to `MyParam` with the string `'my-value'`,
and `MyParam` will be removed from the 'Parameters' section of the template.

## Nested Stacks

This module also supports templates that use [nested stacks](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-nested-stacks.html).

For example, if you have the following parent template:

```json
{
  "Resources": {
    "ChildStack": {
      "Type": "AWS::CloudFormation::Stack",
      "Properties": {
        "TemplateURL": "https://my-s3-template-source.s3.amazonaws.com/child-stack.json"
      }
    }
  }
}
```

where the child template pointed to by `https://my-s3-template-source.s3.amazonaws.com/child-stack.json` is:

```json
{
  "Resources": {
    "MyBucket": {
      "Type": "AWS::S3::Bucket"
    }
  }
}
```

You can include both the parent stack,
and the nested stack in your CDK application as follows:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
parent_template = inc.CfnInclude(self, "ParentStack",
    template_file="path/to/my-parent-template.json",
    load_nested_stacks={
        "ChildStack": {
            "template_file": "path/to/my-nested-template.json"
        }
    }
)
```

Here, `path/to/my-nested-template.json`
represents the path on disk to the downloaded template file from the original template URL of the nested stack
(`https://my-s3-template-source.s3.amazonaws.com/child-stack.json`).
In the CDK application,
this file will be turned into an [Asset](https://docs.aws.amazon.com/cdk/latest/guide/assets.html),
and the `TemplateURL` property of the nested stack resource
will be modified to point to that asset.

The included nested stack can be accessed with the `getNestedStack` method:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
included_child_stack = parent_template.get_nested_stack("ChildStack")
child_stack = included_child_stack.stack
child_template = included_child_stack.included_template
```

Now you can reference resources from `ChildStack`,
and modify them like any other included template:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cfn_bucket = child_template.get_resource("MyBucket")
cfn_bucket.bucket_name = "my-new-bucket-name"

role = iam.Role(child_stack, "MyRole",
    assumed_by=iam.AccountRootPrincipal()
)

role.add_to_policy(iam.PolicyStatement(
    actions=["s3:GetObject*", "s3:GetBucket*", "s3:List*"
    ],
    resources=[cfn_bucket.attr_arn]
))
```

You can also include the nested stack after the `CfnInclude` object was created,
instead of doing it on construction:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
included_child_stack = parent_template.load_nested_stack("ChildTemplate",
    template_file="path/to/my-nested-template.json"
)
```

## Vending CloudFormation templates as Constructs

In many cases, there are existing CloudFormation templates that are not entire applications,
but more like specialized fragments, implementing a particular pattern or best practice.
If you have templates like that,
you can use the `CfnInclude` class to vend them as CDK Constructs:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import path as path

class MyConstruct(Construct):
    def __init__(self, scope, id):
        super().__init__(scope, id)

        # include a template inside the Construct
        cfn_inc.CfnInclude(self, "MyConstruct",
            template_file=path.join(__dirname, "my-template.json"),
            preserve_logical_ids=False
        )
```

Notice the `preserveLogicalIds` parameter -
it makes sure the logical IDs of all the included template elements are re-named using CDK's algorithm,
guaranteeing they are unique within your application.
Without that parameter passed,
instantiating `MyConstruct` twice in the same Stack would result in duplicated logical IDs.
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
    CfnCondition as _CfnCondition_79795035,
    CfnElement as _CfnElement_3c01f138,
    CfnHook as _CfnHook_02bf9fbf,
    CfnMapping as _CfnMapping_40a28af7,
    CfnOutput as _CfnOutput_a4d857a8,
    CfnParameter as _CfnParameter_3e6f99ac,
    CfnResource as _CfnResource_e0a482dc,
    CfnRule as _CfnRule_c48d2c85,
    NestedStack as _NestedStack_9b94bddc,
)


class CfnInclude(
    _CfnElement_3c01f138,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.cloudformation_include.CfnInclude",
):
    '''(experimental) Construct to import an existing CloudFormation template file into a CDK application.

    All resources defined in the template file can be retrieved by calling the {@link getResource} method.
    Any modifications made on the returned resource objects will be reflected in the resulting CDK template.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        template_file: builtins.str,
        load_nested_stacks: typing.Optional[typing.Mapping[builtins.str, "CfnIncludeProps"]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        preserve_logical_ids: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param template_file: (experimental) Path to the template file. Both JSON and YAML template formats are supported.
        :param load_nested_stacks: (experimental) Specifies the template files that define nested stacks that should be included. If your template specifies a stack that isn't included here, it won't be created as a NestedStack resource, and it won't be accessible from the {@link CfnInclude.getNestedStack} method (but will still be accessible from the {@link CfnInclude.getResource} method). If you include a stack here with an ID that isn't in the template, or is in the template but is not a nested stack, template creation will fail and an error will be thrown. Default: - no nested stacks will be included
        :param parameters: (experimental) Specifies parameters to be replaced by the values in this mapping. Any parameters in the template that aren't specified here will be left unmodified. If you include a parameter here with an ID that isn't in the template, template creation will fail and an error will be thrown. Default: - no parameters will be replaced
        :param preserve_logical_ids: (experimental) Whether the resources should have the same logical IDs in the resulting CDK template as they did in the original CloudFormation template file. If you're vending a Construct using an existing CloudFormation template, make sure to pass this as ``false``. **Note**: regardless of whether this option is true or false, the {@link CfnInclude.getResource} and related methods always uses the original logical ID of the resource/element, as specified in the template file. Default: true

        :stability: experimental
        '''
        props = CfnIncludeProps(
            template_file=template_file,
            load_nested_stacks=load_nested_stacks,
            parameters=parameters,
            preserve_logical_ids=preserve_logical_ids,
        )

        jsii.create(CfnInclude, self, [scope, id, props])

    @jsii.member(jsii_name="getCondition")
    def get_condition(self, condition_name: builtins.str) -> _CfnCondition_79795035:
        '''(experimental) Returns the CfnCondition object from the 'Conditions' section of the CloudFormation template with the given name.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Condition with the given name is not present in the template,
        throws an exception.

        :param condition_name: the name of the Condition in the CloudFormation template file.

        :stability: experimental
        '''
        return typing.cast(_CfnCondition_79795035, jsii.invoke(self, "getCondition", [condition_name]))

    @jsii.member(jsii_name="getHook")
    def get_hook(self, hook_logical_id: builtins.str) -> _CfnHook_02bf9fbf:
        '''(experimental) Returns the CfnHook object from the 'Hooks' section of the included CloudFormation template with the given logical ID.

        Any modifications performed on the returned object will be reflected in the resulting CDK template.

        If a Hook with the given logical ID is not present in the template,
        an exception will be thrown.

        :param hook_logical_id: the logical ID of the Hook in the included CloudFormation template's 'Hooks' section.

        :stability: experimental
        '''
        return typing.cast(_CfnHook_02bf9fbf, jsii.invoke(self, "getHook", [hook_logical_id]))

    @jsii.member(jsii_name="getMapping")
    def get_mapping(self, mapping_name: builtins.str) -> _CfnMapping_40a28af7:
        '''(experimental) Returns the CfnMapping object from the 'Mappings' section of the included template.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Mapping with the given name is not present in the template,
        an exception will be thrown.

        :param mapping_name: the name of the Mapping in the template to retrieve.

        :stability: experimental
        '''
        return typing.cast(_CfnMapping_40a28af7, jsii.invoke(self, "getMapping", [mapping_name]))

    @jsii.member(jsii_name="getNestedStack")
    def get_nested_stack(self, logical_id: builtins.str) -> "IncludedNestedStack":
        '''(experimental) Returns a loaded NestedStack with name logicalId.

        For a nested stack to be returned by this method,
        it must be specified either in the {@link CfnIncludeProps.loadNestedStacks} property,
        or through the {@link loadNestedStack} method.

        :param logical_id: the ID of the stack to retrieve, as it appears in the template.

        :stability: experimental
        '''
        return typing.cast("IncludedNestedStack", jsii.invoke(self, "getNestedStack", [logical_id]))

    @jsii.member(jsii_name="getOutput")
    def get_output(self, logical_id: builtins.str) -> _CfnOutput_a4d857a8:
        '''(experimental) Returns the CfnOutput object from the 'Outputs' section of the included template.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If an Output with the given name is not present in the template,
        throws an exception.

        :param logical_id: the name of the output to retrieve.

        :stability: experimental
        '''
        return typing.cast(_CfnOutput_a4d857a8, jsii.invoke(self, "getOutput", [logical_id]))

    @jsii.member(jsii_name="getParameter")
    def get_parameter(self, parameter_name: builtins.str) -> _CfnParameter_3e6f99ac:
        '''(experimental) Returns the CfnParameter object from the 'Parameters' section of the included template.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Parameter with the given name is not present in the template,
        throws an exception.

        :param parameter_name: the name of the parameter to retrieve.

        :stability: experimental
        '''
        return typing.cast(_CfnParameter_3e6f99ac, jsii.invoke(self, "getParameter", [parameter_name]))

    @jsii.member(jsii_name="getResource")
    def get_resource(self, logical_id: builtins.str) -> _CfnResource_e0a482dc:
        '''(experimental) Returns the low-level CfnResource from the template with the given logical ID.

        Any modifications performed on that resource will be reflected in the resulting CDK template.

        The returned object will be of the proper underlying class;
        you can always cast it to the correct type in your code::

            // assume the template contains an AWS::S3::Bucket with logical ID 'Bucket'
            const cfnBucket = cfnTemplate.getResource('Bucket') as s3.CfnBucket;
            // cfnBucket is of type s3.CfnBucket

        If the template does not contain a resource with the given logical ID,
        an exception will be thrown.

        :param logical_id: the logical ID of the resource in the CloudFormation template file.

        :stability: experimental
        '''
        return typing.cast(_CfnResource_e0a482dc, jsii.invoke(self, "getResource", [logical_id]))

    @jsii.member(jsii_name="getRule")
    def get_rule(self, rule_name: builtins.str) -> _CfnRule_c48d2c85:
        '''(experimental) Returns the CfnRule object from the 'Rules' section of the CloudFormation template with the given name.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Rule with the given name is not present in the template,
        an exception will be thrown.

        :param rule_name: the name of the Rule in the CloudFormation template.

        :stability: experimental
        '''
        return typing.cast(_CfnRule_c48d2c85, jsii.invoke(self, "getRule", [rule_name]))

    @jsii.member(jsii_name="loadNestedStack")
    def load_nested_stack(
        self,
        logical_id: builtins.str,
        *,
        template_file: builtins.str,
        load_nested_stacks: typing.Optional[typing.Mapping[builtins.str, "CfnIncludeProps"]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        preserve_logical_ids: typing.Optional[builtins.bool] = None,
    ) -> "IncludedNestedStack":
        '''(experimental) Includes a template for a child stack inside of this parent template.

        A child with this logical ID must exist in the template,
        and be of type AWS::CloudFormation::Stack.
        This is equivalent to specifying the value in the {@link CfnIncludeProps.loadNestedStacks}
        property on object construction.

        :param logical_id: the ID of the stack to retrieve, as it appears in the template.
        :param template_file: (experimental) Path to the template file. Both JSON and YAML template formats are supported.
        :param load_nested_stacks: (experimental) Specifies the template files that define nested stacks that should be included. If your template specifies a stack that isn't included here, it won't be created as a NestedStack resource, and it won't be accessible from the {@link CfnInclude.getNestedStack} method (but will still be accessible from the {@link CfnInclude.getResource} method). If you include a stack here with an ID that isn't in the template, or is in the template but is not a nested stack, template creation will fail and an error will be thrown. Default: - no nested stacks will be included
        :param parameters: (experimental) Specifies parameters to be replaced by the values in this mapping. Any parameters in the template that aren't specified here will be left unmodified. If you include a parameter here with an ID that isn't in the template, template creation will fail and an error will be thrown. Default: - no parameters will be replaced
        :param preserve_logical_ids: (experimental) Whether the resources should have the same logical IDs in the resulting CDK template as they did in the original CloudFormation template file. If you're vending a Construct using an existing CloudFormation template, make sure to pass this as ``false``. **Note**: regardless of whether this option is true or false, the {@link CfnInclude.getResource} and related methods always uses the original logical ID of the resource/element, as specified in the template file. Default: true

        :return: the same {@link IncludedNestedStack} object that {@link getNestedStack} returns for this logical ID

        :stability: experimental
        '''
        nested_stack_props = CfnIncludeProps(
            template_file=template_file,
            load_nested_stacks=load_nested_stacks,
            parameters=parameters,
            preserve_logical_ids=preserve_logical_ids,
        )

        return typing.cast("IncludedNestedStack", jsii.invoke(self, "loadNestedStack", [logical_id, nested_stack_props]))


@jsii.data_type(
    jsii_type="monocdk.cloudformation_include.CfnIncludeProps",
    jsii_struct_bases=[],
    name_mapping={
        "template_file": "templateFile",
        "load_nested_stacks": "loadNestedStacks",
        "parameters": "parameters",
        "preserve_logical_ids": "preserveLogicalIds",
    },
)
class CfnIncludeProps:
    def __init__(
        self,
        *,
        template_file: builtins.str,
        load_nested_stacks: typing.Optional[typing.Mapping[builtins.str, "CfnIncludeProps"]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        preserve_logical_ids: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Construction properties of {@link CfnInclude}.

        :param template_file: (experimental) Path to the template file. Both JSON and YAML template formats are supported.
        :param load_nested_stacks: (experimental) Specifies the template files that define nested stacks that should be included. If your template specifies a stack that isn't included here, it won't be created as a NestedStack resource, and it won't be accessible from the {@link CfnInclude.getNestedStack} method (but will still be accessible from the {@link CfnInclude.getResource} method). If you include a stack here with an ID that isn't in the template, or is in the template but is not a nested stack, template creation will fail and an error will be thrown. Default: - no nested stacks will be included
        :param parameters: (experimental) Specifies parameters to be replaced by the values in this mapping. Any parameters in the template that aren't specified here will be left unmodified. If you include a parameter here with an ID that isn't in the template, template creation will fail and an error will be thrown. Default: - no parameters will be replaced
        :param preserve_logical_ids: (experimental) Whether the resources should have the same logical IDs in the resulting CDK template as they did in the original CloudFormation template file. If you're vending a Construct using an existing CloudFormation template, make sure to pass this as ``false``. **Note**: regardless of whether this option is true or false, the {@link CfnInclude.getResource} and related methods always uses the original logical ID of the resource/element, as specified in the template file. Default: true

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "template_file": template_file,
        }
        if load_nested_stacks is not None:
            self._values["load_nested_stacks"] = load_nested_stacks
        if parameters is not None:
            self._values["parameters"] = parameters
        if preserve_logical_ids is not None:
            self._values["preserve_logical_ids"] = preserve_logical_ids

    @builtins.property
    def template_file(self) -> builtins.str:
        '''(experimental) Path to the template file.

        Both JSON and YAML template formats are supported.

        :stability: experimental
        '''
        result = self._values.get("template_file")
        assert result is not None, "Required property 'template_file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def load_nested_stacks(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "CfnIncludeProps"]]:
        '''(experimental) Specifies the template files that define nested stacks that should be included.

        If your template specifies a stack that isn't included here, it won't be created as a NestedStack
        resource, and it won't be accessible from the {@link CfnInclude.getNestedStack} method
        (but will still be accessible from the {@link CfnInclude.getResource} method).

        If you include a stack here with an ID that isn't in the template,
        or is in the template but is not a nested stack,
        template creation will fail and an error will be thrown.

        :default: - no nested stacks will be included

        :stability: experimental
        '''
        result = self._values.get("load_nested_stacks")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "CfnIncludeProps"]], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Specifies parameters to be replaced by the values in this mapping.

        Any parameters in the template that aren't specified here will be left unmodified.
        If you include a parameter here with an ID that isn't in the template,
        template creation will fail and an error will be thrown.

        :default: - no parameters will be replaced

        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def preserve_logical_ids(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the resources should have the same logical IDs in the resulting CDK template as they did in the original CloudFormation template file.

        If you're vending a Construct using an existing CloudFormation template,
        make sure to pass this as ``false``.

        **Note**: regardless of whether this option is true or false,
        the {@link CfnInclude.getResource} and related methods always uses the original logical ID of the resource/element,
        as specified in the template file.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("preserve_logical_ids")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIncludeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloudformation_include.IncludedNestedStack",
    jsii_struct_bases=[],
    name_mapping={"included_template": "includedTemplate", "stack": "stack"},
)
class IncludedNestedStack:
    def __init__(
        self,
        *,
        included_template: CfnInclude,
        stack: _NestedStack_9b94bddc,
    ) -> None:
        '''(experimental) The type returned from {@link CfnInclude.getNestedStack}. Contains both the NestedStack object and CfnInclude representations of the child stack.

        :param included_template: (experimental) The CfnInclude that represents the template, which can be used to access Resources and other template elements.
        :param stack: (experimental) The NestedStack object which represents the scope of the template.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "included_template": included_template,
            "stack": stack,
        }

    @builtins.property
    def included_template(self) -> CfnInclude:
        '''(experimental) The CfnInclude that represents the template, which can be used to access Resources and other template elements.

        :stability: experimental
        '''
        result = self._values.get("included_template")
        assert result is not None, "Required property 'included_template' is missing"
        return typing.cast(CfnInclude, result)

    @builtins.property
    def stack(self) -> _NestedStack_9b94bddc:
        '''(experimental) The NestedStack object which represents the scope of the template.

        :stability: experimental
        '''
        result = self._values.get("stack")
        assert result is not None, "Required property 'stack' is missing"
        return typing.cast(_NestedStack_9b94bddc, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IncludedNestedStack(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnInclude",
    "CfnIncludeProps",
    "IncludedNestedStack",
]

publication.publish()
