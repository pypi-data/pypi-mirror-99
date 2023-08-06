'''
# Amazon S3 Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

Define an unencrypted S3 bucket.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Bucket(self, "MyFirstBucket")
```

`Bucket` constructs expose the following deploy-time attributes:

* `bucketArn` - the ARN of the bucket (i.e. `arn:aws:s3:::bucket_name`)
* `bucketName` - the name of the bucket (i.e. `bucket_name`)
* `bucketWebsiteUrl` - the Website URL of the bucket (i.e.
  `http://bucket_name.s3-website-us-west-1.amazonaws.com`)
* `bucketDomainName` - the URL of the bucket (i.e. `bucket_name.s3.amazonaws.com`)
* `bucketDualStackDomainName` - the dual-stack URL of the bucket (i.e.
  `bucket_name.s3.dualstack.eu-west-1.amazonaws.com`)
* `bucketRegionalDomainName` - the regional URL of the bucket (i.e.
  `bucket_name.s3.eu-west-1.amazonaws.com`)
* `arnForObjects(pattern)` - the ARN of an object or objects within the bucket (i.e.
  `arn:aws:s3:::bucket_name/exampleobject.png` or
  `arn:aws:s3:::bucket_name/Development/*`)
* `urlForObject(key)` - the HTTP URL of an object within the bucket (i.e.
  `https://s3.cn-north-1.amazonaws.com.cn/china-bucket/mykey`)
* `virtualHostedUrlForObject(key)` - the virtual-hosted style HTTP URL of an object
  within the bucket (i.e. `https://china-bucket-s3.cn-north-1.amazonaws.com.cn/mykey`)
* `s3UrlForObject(key)` - the S3 URL of an object within the bucket (i.e.
  `s3://bucket/mykey`)

## Encryption

Define a KMS-encrypted bucket:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket(self, "MyEncryptedBucket",
    encryption=BucketEncryption.KMS
)

# you can access the encryption key:
assert(bucket.encryption_key instanceof kms.Key)
```

You can also supply your own key:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_kms_key = kms.Key(self, "MyKey")

bucket = Bucket(self, "MyEncryptedBucket",
    encryption=BucketEncryption.KMS,
    encryption_key=my_kms_key
)

assert(bucket.encryption_key === my_kms_key)
```

Enable KMS-SSE encryption via [S3 Bucket Keys](https://docs.aws.amazon.com/AmazonS3/latest/dev/bucket-key.html):

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket(self, "MyEncryptedBucket",
    encryption=BucketEncryption.KMS,
    bucket_key_enabled=True
)

assert(bucket.bucket_key_enabled === True)
```

Use `BucketEncryption.ManagedKms` to use the S3 master KMS key:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket(self, "Buck",
    encryption=BucketEncryption.KMS_MANAGED
)

assert(bucket.encryption_key == null)
```

## Permissions

A bucket policy will be automatically created for the bucket upon the first call to
`addToResourcePolicy(statement)`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket(self, "MyBucket")
bucket.add_to_resource_policy(iam.PolicyStatement(
    actions=["s3:GetObject"],
    resources=[bucket.arn_for_objects("file.txt")],
    principals=[iam.AccountRootPrincipal()]
))
```

The bucket policy can be directly accessed after creation to add statements or
adjust the removal policy.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket.policy.apply_removal_policy(RemovalPolicy.RETAIN)
```

Most of the time, you won't have to manipulate the bucket policy directly.
Instead, buckets have "grant" methods called to give prepackaged sets of permissions
to other resources. For example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lambda_ = lambda_.Function(self, "Lambda")

bucket = Bucket(self, "MyBucket")
bucket.grant_read_write(lambda_)
```

Will give the Lambda's execution role permissions to read and write
from the bucket.

## AWS Foundational Security Best Practices

### Enforcing SSL

To require all requests use Secure Socket Layer (SSL):

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket(self, "Bucket",
    enforce_sSL=True
)
```

## Sharing buckets between stacks

To use a bucket in a different stack in the same CDK application, pass the object to the other stack:

[sharing bucket between stacks](test/integ.bucket-sharing.lit.ts)

## Importing existing buckets

To import an existing bucket into your CDK application, use the `Bucket.fromBucketAttributes`
factory method. This method accepts `BucketAttributes` which describes the properties of an already
existing bucket:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket.from_bucket_attributes(self, "ImportedBucket",
    bucket_arn="arn:aws:s3:::my-bucket"
)

# now you can just call methods on the bucket
bucket.grant_read_write(user)
```

Alternatively, short-hand factories are available as `Bucket.fromBucketName` and
`Bucket.fromBucketArn`, which will derive all bucket attributes from the bucket
name or ARN respectively:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
by_name = Bucket.from_bucket_name(self, "BucketByName", "my-bucket")
by_arn = Bucket.from_bucket_arn(self, "BucketByArn", "arn:aws:s3:::my-bucket")
```

The bucket's region defaults to the current stack's region, but can also be explicitly set in cases where one of the bucket's
regional properties needs to contain the correct values.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_cross_region_bucket = Bucket.from_bucket_attributes(self, "CrossRegionImport",
    bucket_arn="arn:aws:s3:::my-bucket",
    region="us-east-1"
)
```

## Bucket Notifications

The Amazon S3 notification feature enables you to receive notifications when
certain events happen in your bucket as described under [S3 Bucket
Notifications] of the S3 Developer Guide.

To subscribe for bucket notifications, use the `bucket.addEventNotification` method. The
`bucket.addObjectCreatedNotification` and `bucket.addObjectRemovedNotification` can also be used for
these common use cases.

The following example will subscribe an SNS topic to be notified of all `s3:ObjectCreated:*` events:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_s3_notifications as s3n

my_topic = sns.Topic(self, "MyTopic")
bucket.add_event_notification(s3.EventType.OBJECT_CREATED, s3n.SnsDestination(topic))
```

This call will also ensure that the topic policy can accept notifications for
this specific bucket.

Supported S3 notification targets are exposed by the `@aws-cdk/aws-s3-notifications` package.

It is also possible to specify S3 object key filters when subscribing. The
following example will notify `myQueue` when objects prefixed with `foo/` and
have the `.jpg` suffix are removed from the bucket.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket.add_event_notification(s3.EventType.OBJECT_REMOVED,
    s3n.SqsDestination(my_queue), prefix="foo/", suffix=".jpg")
```

## Block Public Access

Use `blockPublicAccess` to specify [block public access settings](https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html) on the bucket.

Enable all block public access settings:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket(self, "MyBlockedBucket",
    block_public_access=BlockPublicAccess.BLOCK_ALL
)
```

Block and ignore public ACLs:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket(self, "MyBlockedBucket",
    block_public_access=BlockPublicAccess.BLOCK_ACLS
)
```

Alternatively, specify the settings manually:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket(self, "MyBlockedBucket",
    block_public_access=BlockPublicAccess(block_public_policy=True)
)
```

When `blockPublicPolicy` is set to `true`, `grantPublicRead()` throws an error.

## Logging configuration

Use `serverAccessLogsBucket` to describe where server access logs are to be stored.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
access_logs_bucket = Bucket(self, "AccessLogsBucket")

bucket = Bucket(self, "MyBucket",
    server_access_logs_bucket=access_logs_bucket
)
```

It's also possible to specify a prefix for Amazon S3 to assign to all log object keys.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket(self, "MyBucket",
    server_access_logs_bucket=access_logs_bucket,
    server_access_logs_prefix="logs"
)
```

## S3 Inventory

An [inventory](https://docs.aws.amazon.com/AmazonS3/latest/dev/storage-inventory.html) contains a list of the objects in the source bucket and metadata for each object. The inventory lists are stored in the destination bucket as a CSV file compressed with GZIP, as an Apache optimized row columnar (ORC) file compressed with ZLIB, or as an Apache Parquet (Parquet) file compressed with Snappy.

You can configure multiple inventory lists for a bucket. You can configure what object metadata to include in the inventory, whether to list all object versions or only current versions, where to store the inventory list file output, and whether to generate the inventory on a daily or weekly basis.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
inventory_bucket = s3.Bucket(self, "InventoryBucket")

data_bucket = s3.Bucket(self, "DataBucket",
    inventories=[{
        "frequency": s3.InventoryFrequency.DAILY,
        "include_object_versions": s3.InventoryObjectVersion.CURRENT,
        "destination": {
            "bucket": inventory_bucket
        }
    }, {
        "frequency": s3.InventoryFrequency.WEEKLY,
        "include_object_versions": s3.InventoryObjectVersion.ALL,
        "destination": {
            "bucket": inventory_bucket,
            "prefix": "with-all-versions"
        }
    }
    ]
)
```

If the destination bucket is created as part of the same CDK application, the necessary permissions will be automatically added to the bucket policy.
However, if you use an imported bucket (i.e `Bucket.fromXXX()`), you'll have to make sure it contains the following policy document:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "InventoryAndAnalyticsExamplePolicy",
      "Effect": "Allow",
      "Principal": { "Service": "s3.amazonaws.com" },
      "Action": "s3:PutObject",
      "Resource": ["arn:aws:s3:::destinationBucket/*"]
    }
  ]
}
```

## Website redirection

You can use the two following properties to specify the bucket [redirection policy](https://docs.aws.amazon.com/AmazonS3/latest/dev/how-to-page-redirect.html#advanced-conditional-redirects). Please note that these methods cannot both be applied to the same bucket.

### Static redirection

You can statically redirect a to a given Bucket URL or any other host name with `websiteRedirect`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket(self, "MyRedirectedBucket",
    website_redirect={"host_name": "www.example.com"}
)
```

### Routing rules

Alternatively, you can also define multiple `websiteRoutingRules`, to define complex, conditional redirections:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket(self, "MyRedirectedBucket",
    website_routing_rules=[{
        "host_name": "www.example.com",
        "http_redirect_code": "302",
        "protocol": RedirectProtocol.HTTPS,
        "replace_key": ReplaceKey.prefix_with("test/"),
        "condition": {
            "http_error_code_returned_equals": "200",
            "key_prefix_equals": "prefix"
        }
    }]
)
```

## Filling the bucket as part of deployment

To put files into a bucket as part of a deployment (for example, to host a
website), see the `@aws-cdk/aws-s3-deployment` package, which provides a
resource that can do just that.

## The URL for objects

S3 provides two types of URLs for accessing objects via HTTP(S). Path-Style and
[Virtual Hosted-Style](https://docs.aws.amazon.com/AmazonS3/latest/dev/VirtualHosting.html)
URL. Path-Style is a classic way and will be
[deprecated](https://aws.amazon.com/jp/blogs/aws/amazon-s3-path-deprecation-plan-the-rest-of-the-story).
We recommend to use Virtual Hosted-Style URL for newly made bucket.

You can generate both of them.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket.url_for_object("objectname")# Path-Style URL
bucket.virtual_hosted_url_for_object("objectname")# Virtual Hosted-Style URL
bucket.virtual_hosted_url_for_object("objectname", regional=False)
```

### Object Ownership

You can use the two following properties to specify the bucket [object Ownership](https://docs.aws.amazon.com/AmazonS3/latest/dev/about-object-ownership.html).

#### Object writer

The Uploading account will own the object.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
s3.Bucket(self, "MyBucket",
    object_ownership=s3.ObjectOwnership.OBJECT_WRITER
)
```

#### Bucket owner preferred

The bucket owner will own the object if the object is uploaded with the bucket-owner-full-control canned ACL. Without this setting and canned ACL, the object is uploaded and remains owned by the uploading account.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
s3.Bucket(self, "MyBucket",
    object_ownership=s3.ObjectOwnership.BUCKET_OWNER_PREFERRED
)
```

### Bucket deletion

When a bucket is removed from a stack (or the stack is deleted), the S3
bucket will be removed according to its removal policy (which by default will
simply orphan the bucket and leave it in your AWS account). If the removal
policy is set to `RemovalPolicy.DESTROY`, the bucket will be deleted as long
as it does not contain any objects.

To override this and force all objects to get deleted during bucket deletion,
enable the`autoDeleteObjects` option.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = Bucket(self, "MyTempFileBucket",
    removal_policy=RemovalPolicy.DESTROY,
    auto_delete_objects=True
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
    IDependable as _IDependable_1175c9f7,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    RemovalPolicy as _RemovalPolicy_c97e7a20,
    Resource as _Resource_abff4495,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_events import (
    EventPattern as _EventPattern_a23fbf37,
    IRuleTarget as _IRuleTarget_d45ec729,
    OnEventOptions as _OnEventOptions_d5081088,
    Rule as _Rule_6cfff189,
)
from ..aws_iam import (
    AddToResourcePolicyResult as _AddToResourcePolicyResult_0fd9d2a9,
    Grant as _Grant_bcb5eae7,
    IGrantable as _IGrantable_4c5a91d1,
    PolicyDocument as _PolicyDocument_b5de5177,
    PolicyStatement as _PolicyStatement_296fe8a3,
)
from ..aws_kms import IKey as _IKey_36930160


class BlockPublicAccess(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_s3.BlockPublicAccess",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        *,
        block_public_acls: typing.Optional[builtins.bool] = None,
        block_public_policy: typing.Optional[builtins.bool] = None,
        ignore_public_acls: typing.Optional[builtins.bool] = None,
        restrict_public_buckets: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param block_public_acls: (experimental) Whether to block public ACLs.
        :param block_public_policy: (experimental) Whether to block public policy.
        :param ignore_public_acls: (experimental) Whether to ignore public ACLs.
        :param restrict_public_buckets: (experimental) Whether to restrict public access.

        :stability: experimental
        '''
        options = BlockPublicAccessOptions(
            block_public_acls=block_public_acls,
            block_public_policy=block_public_policy,
            ignore_public_acls=ignore_public_acls,
            restrict_public_buckets=restrict_public_buckets,
        )

        jsii.create(BlockPublicAccess, self, [options])

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="BLOCK_ACLS")
    def BLOCK_ACLS(cls) -> "BlockPublicAccess":
        '''
        :stability: experimental
        '''
        return typing.cast("BlockPublicAccess", jsii.sget(cls, "BLOCK_ACLS"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="BLOCK_ALL")
    def BLOCK_ALL(cls) -> "BlockPublicAccess":
        '''
        :stability: experimental
        '''
        return typing.cast("BlockPublicAccess", jsii.sget(cls, "BLOCK_ALL"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="blockPublicAcls")
    def block_public_acls(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "blockPublicAcls"))

    @block_public_acls.setter
    def block_public_acls(self, value: typing.Optional[builtins.bool]) -> None:
        jsii.set(self, "blockPublicAcls", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="blockPublicPolicy")
    def block_public_policy(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "blockPublicPolicy"))

    @block_public_policy.setter
    def block_public_policy(self, value: typing.Optional[builtins.bool]) -> None:
        jsii.set(self, "blockPublicPolicy", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ignorePublicAcls")
    def ignore_public_acls(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "ignorePublicAcls"))

    @ignore_public_acls.setter
    def ignore_public_acls(self, value: typing.Optional[builtins.bool]) -> None:
        jsii.set(self, "ignorePublicAcls", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="restrictPublicBuckets")
    def restrict_public_buckets(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "restrictPublicBuckets"))

    @restrict_public_buckets.setter
    def restrict_public_buckets(self, value: typing.Optional[builtins.bool]) -> None:
        jsii.set(self, "restrictPublicBuckets", value)


@jsii.data_type(
    jsii_type="monocdk.aws_s3.BlockPublicAccessOptions",
    jsii_struct_bases=[],
    name_mapping={
        "block_public_acls": "blockPublicAcls",
        "block_public_policy": "blockPublicPolicy",
        "ignore_public_acls": "ignorePublicAcls",
        "restrict_public_buckets": "restrictPublicBuckets",
    },
)
class BlockPublicAccessOptions:
    def __init__(
        self,
        *,
        block_public_acls: typing.Optional[builtins.bool] = None,
        block_public_policy: typing.Optional[builtins.bool] = None,
        ignore_public_acls: typing.Optional[builtins.bool] = None,
        restrict_public_buckets: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param block_public_acls: (experimental) Whether to block public ACLs.
        :param block_public_policy: (experimental) Whether to block public policy.
        :param ignore_public_acls: (experimental) Whether to ignore public ACLs.
        :param restrict_public_buckets: (experimental) Whether to restrict public access.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if block_public_acls is not None:
            self._values["block_public_acls"] = block_public_acls
        if block_public_policy is not None:
            self._values["block_public_policy"] = block_public_policy
        if ignore_public_acls is not None:
            self._values["ignore_public_acls"] = ignore_public_acls
        if restrict_public_buckets is not None:
            self._values["restrict_public_buckets"] = restrict_public_buckets

    @builtins.property
    def block_public_acls(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to block public ACLs.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html#access-control-block-public-access-options
        :stability: experimental
        '''
        result = self._values.get("block_public_acls")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def block_public_policy(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to block public policy.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html#access-control-block-public-access-options
        :stability: experimental
        '''
        result = self._values.get("block_public_policy")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ignore_public_acls(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to ignore public ACLs.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html#access-control-block-public-access-options
        :stability: experimental
        '''
        result = self._values.get("ignore_public_acls")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def restrict_public_buckets(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to restrict public access.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html#access-control-block-public-access-options
        :stability: experimental
        '''
        result = self._values.get("restrict_public_buckets")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BlockPublicAccessOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_s3.BucketAccessControl")
class BucketAccessControl(enum.Enum):
    '''(experimental) Default bucket access control types.

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html
    :stability: experimental
    '''

    PRIVATE = "PRIVATE"
    '''(experimental) Owner gets FULL_CONTROL.

    No one else has access rights.

    :stability: experimental
    '''
    PUBLIC_READ = "PUBLIC_READ"
    '''(experimental) Owner gets FULL_CONTROL.

    The AllUsers group gets READ access.

    :stability: experimental
    '''
    PUBLIC_READ_WRITE = "PUBLIC_READ_WRITE"
    '''(experimental) Owner gets FULL_CONTROL.

    The AllUsers group gets READ and WRITE access.
    Granting this on a bucket is generally not recommended.

    :stability: experimental
    '''
    AUTHENTICATED_READ = "AUTHENTICATED_READ"
    '''(experimental) Owner gets FULL_CONTROL.

    The AuthenticatedUsers group gets READ access.

    :stability: experimental
    '''
    LOG_DELIVERY_WRITE = "LOG_DELIVERY_WRITE"
    '''(experimental) The LogDelivery group gets WRITE and READ_ACP permissions on the bucket.

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerLogs.html
    :stability: experimental
    '''
    BUCKET_OWNER_READ = "BUCKET_OWNER_READ"
    '''(experimental) Object owner gets FULL_CONTROL.

    Bucket owner gets READ access.
    If you specify this canned ACL when creating a bucket, Amazon S3 ignores it.

    :stability: experimental
    '''
    BUCKET_OWNER_FULL_CONTROL = "BUCKET_OWNER_FULL_CONTROL"
    '''(experimental) Both the object owner and the bucket owner get FULL_CONTROL over the object.

    If you specify this canned ACL when creating a bucket, Amazon S3 ignores it.

    :stability: experimental
    '''
    AWS_EXEC_READ = "AWS_EXEC_READ"
    '''(experimental) Owner gets FULL_CONTROL.

    Amazon EC2 gets READ access to GET an Amazon Machine Image (AMI) bundle from Amazon S3.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_s3.BucketAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "bucket_arn": "bucketArn",
        "bucket_domain_name": "bucketDomainName",
        "bucket_dual_stack_domain_name": "bucketDualStackDomainName",
        "bucket_name": "bucketName",
        "bucket_regional_domain_name": "bucketRegionalDomainName",
        "bucket_website_new_url_format": "bucketWebsiteNewUrlFormat",
        "bucket_website_url": "bucketWebsiteUrl",
        "encryption_key": "encryptionKey",
        "is_website": "isWebsite",
        "region": "region",
    },
)
class BucketAttributes:
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        bucket_arn: typing.Optional[builtins.str] = None,
        bucket_domain_name: typing.Optional[builtins.str] = None,
        bucket_dual_stack_domain_name: typing.Optional[builtins.str] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_regional_domain_name: typing.Optional[builtins.str] = None,
        bucket_website_new_url_format: typing.Optional[builtins.bool] = None,
        bucket_website_url: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        is_website: typing.Optional[builtins.bool] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) A reference to a bucket.

        The easiest way to instantiate is to call
        ``bucket.export()``. Then, the consumer can use ``Bucket.import(this, ref)`` and
        get a ``Bucket``.

        :param account: (experimental) The account this existing bucket belongs to. Default: - it's assumed the bucket belongs to the same account as the scope it's being imported into
        :param bucket_arn: (experimental) The ARN of the bucket. At least one of bucketArn or bucketName must be defined in order to initialize a bucket ref.
        :param bucket_domain_name: (experimental) The domain name of the bucket. Default: Inferred from bucket name
        :param bucket_dual_stack_domain_name: (experimental) The IPv6 DNS name of the specified bucket.
        :param bucket_name: (experimental) The name of the bucket. If the underlying value of ARN is a string, the name will be parsed from the ARN. Otherwise, the name is optional, but some features that require the bucket name such as auto-creating a bucket policy, won't work.
        :param bucket_regional_domain_name: (experimental) The regional domain name of the specified bucket.
        :param bucket_website_new_url_format: (experimental) The format of the website URL of the bucket. This should be true for regions launched since 2014. Default: false
        :param bucket_website_url: (experimental) The website URL of the bucket (if static web hosting is enabled). Default: Inferred from bucket name
        :param encryption_key: 
        :param is_website: (experimental) If this bucket has been configured for static website hosting. Default: false
        :param region: (experimental) The region this existing bucket is in. Default: - it's assumed the bucket is in the same region as the scope it's being imported into

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if bucket_arn is not None:
            self._values["bucket_arn"] = bucket_arn
        if bucket_domain_name is not None:
            self._values["bucket_domain_name"] = bucket_domain_name
        if bucket_dual_stack_domain_name is not None:
            self._values["bucket_dual_stack_domain_name"] = bucket_dual_stack_domain_name
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bucket_regional_domain_name is not None:
            self._values["bucket_regional_domain_name"] = bucket_regional_domain_name
        if bucket_website_new_url_format is not None:
            self._values["bucket_website_new_url_format"] = bucket_website_new_url_format
        if bucket_website_url is not None:
            self._values["bucket_website_url"] = bucket_website_url
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if is_website is not None:
            self._values["is_website"] = is_website
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The account this existing bucket belongs to.

        :default: - it's assumed the bucket belongs to the same account as the scope it's being imported into

        :stability: experimental
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the bucket.

        At least one of bucketArn or bucketName must be
        defined in order to initialize a bucket ref.

        :stability: experimental
        '''
        result = self._values.get("bucket_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_domain_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The domain name of the bucket.

        :default: Inferred from bucket name

        :stability: experimental
        '''
        result = self._values.get("bucket_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_dual_stack_domain_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The IPv6 DNS name of the specified bucket.

        :stability: experimental
        '''
        result = self._values.get("bucket_dual_stack_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the bucket.

        If the underlying value of ARN is a string, the
        name will be parsed from the ARN. Otherwise, the name is optional, but
        some features that require the bucket name such as auto-creating a bucket
        policy, won't work.

        :stability: experimental
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_regional_domain_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The regional domain name of the specified bucket.

        :stability: experimental
        '''
        result = self._values.get("bucket_regional_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_website_new_url_format(self) -> typing.Optional[builtins.bool]:
        '''(experimental) The format of the website URL of the bucket.

        This should be true for
        regions launched since 2014.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("bucket_website_new_url_format")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def bucket_website_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The website URL of the bucket (if static web hosting is enabled).

        :default: Inferred from bucket name

        :stability: experimental
        '''
        result = self._values.get("bucket_website_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''
        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def is_website(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If this bucket has been configured for static website hosting.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("is_website")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region this existing bucket is in.

        :default: - it's assumed the bucket is in the same region as the scope it's being imported into

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BucketAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_s3.BucketEncryption")
class BucketEncryption(enum.Enum):
    '''(experimental) What kind of server-side encryption to apply to this bucket.

    :stability: experimental
    '''

    UNENCRYPTED = "UNENCRYPTED"
    '''(experimental) Objects in the bucket are not encrypted.

    :stability: experimental
    '''
    KMS_MANAGED = "KMS_MANAGED"
    '''(experimental) Server-side KMS encryption with a master key managed by KMS.

    :stability: experimental
    '''
    S3_MANAGED = "S3_MANAGED"
    '''(experimental) Server-side encryption with a master key managed by S3.

    :stability: experimental
    '''
    KMS = "KMS"
    '''(experimental) Server-side encryption with a KMS key managed by the user.

    If ``encryptionKey`` is specified, this key will be used, otherwise, one will be defined.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_s3.BucketMetrics",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "prefix": "prefix", "tag_filters": "tagFilters"},
)
class BucketMetrics:
    def __init__(
        self,
        *,
        id: builtins.str,
        prefix: typing.Optional[builtins.str] = None,
        tag_filters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''(experimental) Specifies a metrics configuration for the CloudWatch request metrics from an Amazon S3 bucket.

        :param id: (experimental) The ID used to identify the metrics configuration.
        :param prefix: (experimental) The prefix that an object must have to be included in the metrics results.
        :param tag_filters: (experimental) Specifies a list of tag filters to use as a metrics configuration filter. The metrics configuration includes only objects that meet the filter's criteria.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "id": id,
        }
        if prefix is not None:
            self._values["prefix"] = prefix
        if tag_filters is not None:
            self._values["tag_filters"] = tag_filters

    @builtins.property
    def id(self) -> builtins.str:
        '''(experimental) The ID used to identify the metrics configuration.

        :stability: experimental
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The prefix that an object must have to be included in the metrics results.

        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_filters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Specifies a list of tag filters to use as a metrics configuration filter.

        The metrics configuration includes only objects that meet the filter's criteria.

        :stability: experimental
        '''
        result = self._values.get("tag_filters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BucketMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_s3.BucketNotificationDestinationConfig",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn", "type": "type", "dependencies": "dependencies"},
)
class BucketNotificationDestinationConfig:
    def __init__(
        self,
        *,
        arn: builtins.str,
        type: "BucketNotificationDestinationType",
        dependencies: typing.Optional[typing.List[_IDependable_1175c9f7]] = None,
    ) -> None:
        '''(experimental) Represents the properties of a notification destination.

        :param arn: (experimental) The ARN of the destination (i.e. Lambda, SNS, SQS).
        :param type: (experimental) The notification type.
        :param dependencies: (experimental) Any additional dependencies that should be resolved before the bucket notification can be configured (for example, the SNS Topic Policy resource).

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "arn": arn,
            "type": type,
        }
        if dependencies is not None:
            self._values["dependencies"] = dependencies

    @builtins.property
    def arn(self) -> builtins.str:
        '''(experimental) The ARN of the destination (i.e. Lambda, SNS, SQS).

        :stability: experimental
        '''
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> "BucketNotificationDestinationType":
        '''(experimental) The notification type.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("BucketNotificationDestinationType", result)

    @builtins.property
    def dependencies(self) -> typing.Optional[typing.List[_IDependable_1175c9f7]]:
        '''(experimental) Any additional dependencies that should be resolved before the bucket notification can be configured (for example, the SNS Topic Policy resource).

        :stability: experimental
        '''
        result = self._values.get("dependencies")
        return typing.cast(typing.Optional[typing.List[_IDependable_1175c9f7]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BucketNotificationDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_s3.BucketNotificationDestinationType")
class BucketNotificationDestinationType(enum.Enum):
    '''(experimental) Supported types of notification destinations.

    :stability: experimental
    '''

    LAMBDA = "LAMBDA"
    '''
    :stability: experimental
    '''
    QUEUE = "QUEUE"
    '''
    :stability: experimental
    '''
    TOPIC = "TOPIC"
    '''
    :stability: experimental
    '''


class BucketPolicy(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_s3.BucketPolicy",
):
    '''(experimental) Applies an Amazon S3 bucket policy to an Amazon S3 bucket.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        bucket: "IBucket",
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket: (experimental) The Amazon S3 bucket that the policy applies to.
        :param removal_policy: (experimental) Policy to apply when the policy is removed from this stack. Default: - RemovalPolicy.DESTROY.

        :stability: experimental
        '''
        props = BucketPolicyProps(bucket=bucket, removal_policy=removal_policy)

        jsii.create(BucketPolicy, self, [scope, id, props])

    @jsii.member(jsii_name="applyRemovalPolicy")
    def apply_removal_policy(self, removal_policy: _RemovalPolicy_c97e7a20) -> None:
        '''(experimental) Sets the removal policy for the BucketPolicy.

        :param removal_policy: the RemovalPolicy to set.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "applyRemovalPolicy", [removal_policy]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="document")
    def document(self) -> _PolicyDocument_b5de5177:
        '''(experimental) A policy document containing permissions to add to the specified bucket.

        For more information, see Access Policy Language Overview in the Amazon
        Simple Storage Service Developer Guide.

        :stability: experimental
        '''
        return typing.cast(_PolicyDocument_b5de5177, jsii.get(self, "document"))


@jsii.data_type(
    jsii_type="monocdk.aws_s3.BucketPolicyProps",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "removal_policy": "removalPolicy"},
)
class BucketPolicyProps:
    def __init__(
        self,
        *,
        bucket: "IBucket",
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    ) -> None:
        '''
        :param bucket: (experimental) The Amazon S3 bucket that the policy applies to.
        :param removal_policy: (experimental) Policy to apply when the policy is removed from this stack. Default: - RemovalPolicy.DESTROY.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
        }
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def bucket(self) -> "IBucket":
        '''(experimental) The Amazon S3 bucket that the policy applies to.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast("IBucket", result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        '''(experimental) Policy to apply when the policy is removed from this stack.

        :default: - RemovalPolicy.DESTROY.

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_RemovalPolicy_c97e7a20], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BucketPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_s3.BucketProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_control": "accessControl",
        "auto_delete_objects": "autoDeleteObjects",
        "block_public_access": "blockPublicAccess",
        "bucket_key_enabled": "bucketKeyEnabled",
        "bucket_name": "bucketName",
        "cors": "cors",
        "encryption": "encryption",
        "encryption_key": "encryptionKey",
        "enforce_ssl": "enforceSSL",
        "inventories": "inventories",
        "lifecycle_rules": "lifecycleRules",
        "metrics": "metrics",
        "object_ownership": "objectOwnership",
        "public_read_access": "publicReadAccess",
        "removal_policy": "removalPolicy",
        "server_access_logs_bucket": "serverAccessLogsBucket",
        "server_access_logs_prefix": "serverAccessLogsPrefix",
        "versioned": "versioned",
        "website_error_document": "websiteErrorDocument",
        "website_index_document": "websiteIndexDocument",
        "website_redirect": "websiteRedirect",
        "website_routing_rules": "websiteRoutingRules",
    },
)
class BucketProps:
    def __init__(
        self,
        *,
        access_control: typing.Optional[BucketAccessControl] = None,
        auto_delete_objects: typing.Optional[builtins.bool] = None,
        block_public_access: typing.Optional[BlockPublicAccess] = None,
        bucket_key_enabled: typing.Optional[builtins.bool] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        cors: typing.Optional[typing.List["CorsRule"]] = None,
        encryption: typing.Optional[BucketEncryption] = None,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        enforce_ssl: typing.Optional[builtins.bool] = None,
        inventories: typing.Optional[typing.List["Inventory"]] = None,
        lifecycle_rules: typing.Optional[typing.List["LifecycleRule"]] = None,
        metrics: typing.Optional[typing.List[BucketMetrics]] = None,
        object_ownership: typing.Optional["ObjectOwnership"] = None,
        public_read_access: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        server_access_logs_bucket: typing.Optional["IBucket"] = None,
        server_access_logs_prefix: typing.Optional[builtins.str] = None,
        versioned: typing.Optional[builtins.bool] = None,
        website_error_document: typing.Optional[builtins.str] = None,
        website_index_document: typing.Optional[builtins.str] = None,
        website_redirect: typing.Optional["RedirectTarget"] = None,
        website_routing_rules: typing.Optional[typing.List["RoutingRule"]] = None,
    ) -> None:
        '''
        :param access_control: (experimental) Specifies a canned ACL that grants predefined permissions to the bucket. Default: BucketAccessControl.PRIVATE
        :param auto_delete_objects: (experimental) Whether all objects should be automatically deleted when the bucket is removed from the stack or when the stack is deleted. Requires the ``removalPolicy`` to be set to ``RemovalPolicy.DESTROY``. Default: false
        :param block_public_access: (experimental) The block public access configuration of this bucket. Default: - CloudFormation defaults will apply. New buckets and objects don't allow public access, but users can modify bucket policies or object permissions to allow public access
        :param bucket_key_enabled: (experimental) Specifies whether Amazon S3 should use an S3 Bucket Key with server-side encryption using KMS (SSE-KMS) for new objects in the bucket. Only relevant, when Encryption is set to {@link BucketEncryption.KMS} Default: - false
        :param bucket_name: (experimental) Physical name of this bucket. Default: - Assigned by CloudFormation (recommended).
        :param cors: (experimental) The CORS configuration of this bucket. Default: - No CORS configuration.
        :param encryption: (experimental) The kind of server-side encryption to apply to this bucket. If you choose KMS, you can specify a KMS key via ``encryptionKey``. If encryption key is not specified, a key will automatically be created. Default: - ``Kms`` if ``encryptionKey`` is specified, or ``Unencrypted`` otherwise.
        :param encryption_key: (experimental) External KMS key to use for bucket encryption. The 'encryption' property must be either not specified or set to "Kms". An error will be emitted if encryption is set to "Unencrypted" or "Managed". Default: - If encryption is set to "Kms" and this property is undefined, a new KMS key will be created and associated with this bucket.
        :param enforce_ssl: (experimental) Enforces SSL for requests. S3.5 of the AWS Foundational Security Best Practices Regarding S3. Default: false
        :param inventories: (experimental) The inventory configuration of the bucket. Default: - No inventory configuration
        :param lifecycle_rules: (experimental) Rules that define how Amazon S3 manages objects during their lifetime. Default: - No lifecycle rules.
        :param metrics: (experimental) The metrics configuration of this bucket. Default: - No metrics configuration.
        :param object_ownership: (experimental) The objectOwnership of the bucket. Default: - No ObjectOwnership configuration, uploading account will own the object.
        :param public_read_access: (experimental) Grants public read access to all objects in the bucket. Similar to calling ``bucket.grantPublicAccess()`` Default: false
        :param removal_policy: (experimental) Policy to apply when the bucket is removed from this stack. Default: - The bucket will be orphaned.
        :param server_access_logs_bucket: (experimental) Destination bucket for the server access logs. Default: - If "serverAccessLogsPrefix" undefined - access logs disabled, otherwise - log to current bucket.
        :param server_access_logs_prefix: (experimental) Optional log file prefix to use for the bucket's access logs. If defined without "serverAccessLogsBucket", enables access logs to current bucket with this prefix. Default: - No log file prefix
        :param versioned: (experimental) Whether this bucket should have versioning turned on or not. Default: false
        :param website_error_document: (experimental) The name of the error document (e.g. "404.html") for the website. ``websiteIndexDocument`` must also be set if this is set. Default: - No error document.
        :param website_index_document: (experimental) The name of the index document (e.g. "index.html") for the website. Enables static website hosting for this bucket. Default: - No index document.
        :param website_redirect: (experimental) Specifies the redirect behavior of all requests to a website endpoint of a bucket. If you specify this property, you can't specify "websiteIndexDocument", "websiteErrorDocument" nor , "websiteRoutingRules". Default: - No redirection.
        :param website_routing_rules: (experimental) Rules that define when a redirect is applied and the redirect behavior. Default: - No redirection rules.

        :stability: experimental
        '''
        if isinstance(website_redirect, dict):
            website_redirect = RedirectTarget(**website_redirect)
        self._values: typing.Dict[str, typing.Any] = {}
        if access_control is not None:
            self._values["access_control"] = access_control
        if auto_delete_objects is not None:
            self._values["auto_delete_objects"] = auto_delete_objects
        if block_public_access is not None:
            self._values["block_public_access"] = block_public_access
        if bucket_key_enabled is not None:
            self._values["bucket_key_enabled"] = bucket_key_enabled
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if cors is not None:
            self._values["cors"] = cors
        if encryption is not None:
            self._values["encryption"] = encryption
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if enforce_ssl is not None:
            self._values["enforce_ssl"] = enforce_ssl
        if inventories is not None:
            self._values["inventories"] = inventories
        if lifecycle_rules is not None:
            self._values["lifecycle_rules"] = lifecycle_rules
        if metrics is not None:
            self._values["metrics"] = metrics
        if object_ownership is not None:
            self._values["object_ownership"] = object_ownership
        if public_read_access is not None:
            self._values["public_read_access"] = public_read_access
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if server_access_logs_bucket is not None:
            self._values["server_access_logs_bucket"] = server_access_logs_bucket
        if server_access_logs_prefix is not None:
            self._values["server_access_logs_prefix"] = server_access_logs_prefix
        if versioned is not None:
            self._values["versioned"] = versioned
        if website_error_document is not None:
            self._values["website_error_document"] = website_error_document
        if website_index_document is not None:
            self._values["website_index_document"] = website_index_document
        if website_redirect is not None:
            self._values["website_redirect"] = website_redirect
        if website_routing_rules is not None:
            self._values["website_routing_rules"] = website_routing_rules

    @builtins.property
    def access_control(self) -> typing.Optional[BucketAccessControl]:
        '''(experimental) Specifies a canned ACL that grants predefined permissions to the bucket.

        :default: BucketAccessControl.PRIVATE

        :stability: experimental
        '''
        result = self._values.get("access_control")
        return typing.cast(typing.Optional[BucketAccessControl], result)

    @builtins.property
    def auto_delete_objects(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether all objects should be automatically deleted when the bucket is removed from the stack or when the stack is deleted.

        Requires the ``removalPolicy`` to be set to ``RemovalPolicy.DESTROY``.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("auto_delete_objects")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def block_public_access(self) -> typing.Optional[BlockPublicAccess]:
        '''(experimental) The block public access configuration of this bucket.

        :default: - CloudFormation defaults will apply. New buckets and objects don't allow public access, but users can modify bucket policies or object permissions to allow public access

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html
        :stability: experimental
        '''
        result = self._values.get("block_public_access")
        return typing.cast(typing.Optional[BlockPublicAccess], result)

    @builtins.property
    def bucket_key_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether Amazon S3 should use an S3 Bucket Key with server-side encryption using KMS (SSE-KMS) for new objects in the bucket.

        Only relevant, when Encryption is set to {@link BucketEncryption.KMS}

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("bucket_key_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Physical name of this bucket.

        :default: - Assigned by CloudFormation (recommended).

        :stability: experimental
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cors(self) -> typing.Optional[typing.List["CorsRule"]]:
        '''(experimental) The CORS configuration of this bucket.

        :default: - No CORS configuration.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors.html
        :stability: experimental
        '''
        result = self._values.get("cors")
        return typing.cast(typing.Optional[typing.List["CorsRule"]], result)

    @builtins.property
    def encryption(self) -> typing.Optional[BucketEncryption]:
        '''(experimental) The kind of server-side encryption to apply to this bucket.

        If you choose KMS, you can specify a KMS key via ``encryptionKey``. If
        encryption key is not specified, a key will automatically be created.

        :default: - ``Kms`` if ``encryptionKey`` is specified, or ``Unencrypted`` otherwise.

        :stability: experimental
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[BucketEncryption], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) External KMS key to use for bucket encryption.

        The 'encryption' property must be either not specified or set to "Kms".
        An error will be emitted if encryption is set to "Unencrypted" or
        "Managed".

        :default:

        - If encryption is set to "Kms" and this property is undefined,
        a new KMS key will be created and associated with this bucket.

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def enforce_ssl(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enforces SSL for requests.

        S3.5 of the AWS Foundational Security Best Practices Regarding S3.

        :default: false

        :see: https://docs.aws.amazon.com/config/latest/developerguide/s3-bucket-ssl-requests-only.html
        :stability: experimental
        '''
        result = self._values.get("enforce_ssl")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def inventories(self) -> typing.Optional[typing.List["Inventory"]]:
        '''(experimental) The inventory configuration of the bucket.

        :default: - No inventory configuration

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/storage-inventory.html
        :stability: experimental
        '''
        result = self._values.get("inventories")
        return typing.cast(typing.Optional[typing.List["Inventory"]], result)

    @builtins.property
    def lifecycle_rules(self) -> typing.Optional[typing.List["LifecycleRule"]]:
        '''(experimental) Rules that define how Amazon S3 manages objects during their lifetime.

        :default: - No lifecycle rules.

        :stability: experimental
        '''
        result = self._values.get("lifecycle_rules")
        return typing.cast(typing.Optional[typing.List["LifecycleRule"]], result)

    @builtins.property
    def metrics(self) -> typing.Optional[typing.List[BucketMetrics]]:
        '''(experimental) The metrics configuration of this bucket.

        :default: - No metrics configuration.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metricsconfiguration.html
        :stability: experimental
        '''
        result = self._values.get("metrics")
        return typing.cast(typing.Optional[typing.List[BucketMetrics]], result)

    @builtins.property
    def object_ownership(self) -> typing.Optional["ObjectOwnership"]:
        '''(experimental) The objectOwnership of the bucket.

        :default: - No ObjectOwnership configuration, uploading account will own the object.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/about-object-ownership.html
        :stability: experimental
        '''
        result = self._values.get("object_ownership")
        return typing.cast(typing.Optional["ObjectOwnership"], result)

    @builtins.property
    def public_read_access(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Grants public read access to all objects in the bucket.

        Similar to calling ``bucket.grantPublicAccess()``

        :default: false

        :stability: experimental
        '''
        result = self._values.get("public_read_access")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        '''(experimental) Policy to apply when the bucket is removed from this stack.

        :default: - The bucket will be orphaned.

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_RemovalPolicy_c97e7a20], result)

    @builtins.property
    def server_access_logs_bucket(self) -> typing.Optional["IBucket"]:
        '''(experimental) Destination bucket for the server access logs.

        :default: - If "serverAccessLogsPrefix" undefined - access logs disabled, otherwise - log to current bucket.

        :stability: experimental
        '''
        result = self._values.get("server_access_logs_bucket")
        return typing.cast(typing.Optional["IBucket"], result)

    @builtins.property
    def server_access_logs_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Optional log file prefix to use for the bucket's access logs.

        If defined without "serverAccessLogsBucket", enables access logs to current bucket with this prefix.

        :default: - No log file prefix

        :stability: experimental
        '''
        result = self._values.get("server_access_logs_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def versioned(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether this bucket should have versioning turned on or not.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("versioned")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def website_error_document(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the error document (e.g. "404.html") for the website. ``websiteIndexDocument`` must also be set if this is set.

        :default: - No error document.

        :stability: experimental
        '''
        result = self._values.get("website_error_document")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def website_index_document(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the index document (e.g. "index.html") for the website. Enables static website hosting for this bucket.

        :default: - No index document.

        :stability: experimental
        '''
        result = self._values.get("website_index_document")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def website_redirect(self) -> typing.Optional["RedirectTarget"]:
        '''(experimental) Specifies the redirect behavior of all requests to a website endpoint of a bucket.

        If you specify this property, you can't specify "websiteIndexDocument", "websiteErrorDocument" nor , "websiteRoutingRules".

        :default: - No redirection.

        :stability: experimental
        '''
        result = self._values.get("website_redirect")
        return typing.cast(typing.Optional["RedirectTarget"], result)

    @builtins.property
    def website_routing_rules(self) -> typing.Optional[typing.List["RoutingRule"]]:
        '''(experimental) Rules that define when a redirect is applied and the redirect behavior.

        :default: - No redirection rules.

        :stability: experimental
        '''
        result = self._values.get("website_routing_rules")
        return typing.cast(typing.Optional[typing.List["RoutingRule"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnAccessPoint(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_s3.CfnAccessPoint",
):
    '''A CloudFormation ``AWS::S3::AccessPoint``.

    :cloudformationResource: AWS::S3::AccessPoint
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        bucket: builtins.str,
        name: typing.Optional[builtins.str] = None,
        policy: typing.Any = None,
        public_access_block_configuration: typing.Optional[typing.Union["CfnAccessPoint.PublicAccessBlockConfigurationProperty", _IResolvable_a771d0ef]] = None,
        vpc_configuration: typing.Optional[typing.Union["CfnAccessPoint.VpcConfigurationProperty", _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::S3::AccessPoint``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param bucket: ``AWS::S3::AccessPoint.Bucket``.
        :param name: ``AWS::S3::AccessPoint.Name``.
        :param policy: ``AWS::S3::AccessPoint.Policy``.
        :param public_access_block_configuration: ``AWS::S3::AccessPoint.PublicAccessBlockConfiguration``.
        :param vpc_configuration: ``AWS::S3::AccessPoint.VpcConfiguration``.
        '''
        props = CfnAccessPointProps(
            bucket=bucket,
            name=name,
            policy=policy,
            public_access_block_configuration=public_access_block_configuration,
            vpc_configuration=vpc_configuration,
        )

        jsii.create(CfnAccessPoint, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrNetworkOrigin")
    def attr_network_origin(self) -> builtins.str:
        '''
        :cloudformationAttribute: NetworkOrigin
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrNetworkOrigin"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        '''``AWS::S3::AccessPoint.Bucket``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-bucket
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        jsii.set(self, "bucket", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Any:
        '''``AWS::S3::AccessPoint.Policy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-policy
        '''
        return typing.cast(typing.Any, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: typing.Any) -> None:
        jsii.set(self, "policy", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::S3::AccessPoint.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="publicAccessBlockConfiguration")
    def public_access_block_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnAccessPoint.PublicAccessBlockConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::S3::AccessPoint.PublicAccessBlockConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-publicaccessblockconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAccessPoint.PublicAccessBlockConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "publicAccessBlockConfiguration"))

    @public_access_block_configuration.setter
    def public_access_block_configuration(
        self,
        value: typing.Optional[typing.Union["CfnAccessPoint.PublicAccessBlockConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "publicAccessBlockConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpcConfiguration")
    def vpc_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnAccessPoint.VpcConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::S3::AccessPoint.VpcConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-vpcconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAccessPoint.VpcConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "vpcConfiguration"))

    @vpc_configuration.setter
    def vpc_configuration(
        self,
        value: typing.Optional[typing.Union["CfnAccessPoint.VpcConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "vpcConfiguration", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnAccessPoint.PublicAccessBlockConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "block_public_acls": "blockPublicAcls",
            "block_public_policy": "blockPublicPolicy",
            "ignore_public_acls": "ignorePublicAcls",
            "restrict_public_buckets": "restrictPublicBuckets",
        },
    )
    class PublicAccessBlockConfigurationProperty:
        def __init__(
            self,
            *,
            block_public_acls: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            block_public_policy: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            ignore_public_acls: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            restrict_public_buckets: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param block_public_acls: ``CfnAccessPoint.PublicAccessBlockConfigurationProperty.BlockPublicAcls``.
            :param block_public_policy: ``CfnAccessPoint.PublicAccessBlockConfigurationProperty.BlockPublicPolicy``.
            :param ignore_public_acls: ``CfnAccessPoint.PublicAccessBlockConfigurationProperty.IgnorePublicAcls``.
            :param restrict_public_buckets: ``CfnAccessPoint.PublicAccessBlockConfigurationProperty.RestrictPublicBuckets``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accesspoint-publicaccessblockconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if block_public_acls is not None:
                self._values["block_public_acls"] = block_public_acls
            if block_public_policy is not None:
                self._values["block_public_policy"] = block_public_policy
            if ignore_public_acls is not None:
                self._values["ignore_public_acls"] = ignore_public_acls
            if restrict_public_buckets is not None:
                self._values["restrict_public_buckets"] = restrict_public_buckets

        @builtins.property
        def block_public_acls(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnAccessPoint.PublicAccessBlockConfigurationProperty.BlockPublicAcls``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accesspoint-publicaccessblockconfiguration.html#cfn-s3-accesspoint-publicaccessblockconfiguration-blockpublicacls
            '''
            result = self._values.get("block_public_acls")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def block_public_policy(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnAccessPoint.PublicAccessBlockConfigurationProperty.BlockPublicPolicy``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accesspoint-publicaccessblockconfiguration.html#cfn-s3-accesspoint-publicaccessblockconfiguration-blockpublicpolicy
            '''
            result = self._values.get("block_public_policy")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def ignore_public_acls(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnAccessPoint.PublicAccessBlockConfigurationProperty.IgnorePublicAcls``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accesspoint-publicaccessblockconfiguration.html#cfn-s3-accesspoint-publicaccessblockconfiguration-ignorepublicacls
            '''
            result = self._values.get("ignore_public_acls")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def restrict_public_buckets(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnAccessPoint.PublicAccessBlockConfigurationProperty.RestrictPublicBuckets``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accesspoint-publicaccessblockconfiguration.html#cfn-s3-accesspoint-publicaccessblockconfiguration-restrictpublicbuckets
            '''
            result = self._values.get("restrict_public_buckets")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PublicAccessBlockConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnAccessPoint.VpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"vpc_id": "vpcId"},
    )
    class VpcConfigurationProperty:
        def __init__(self, *, vpc_id: typing.Optional[builtins.str] = None) -> None:
            '''
            :param vpc_id: ``CfnAccessPoint.VpcConfigurationProperty.VpcId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accesspoint-vpcconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''``CfnAccessPoint.VpcConfigurationProperty.VpcId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-accesspoint-vpcconfiguration.html#cfn-s3-accesspoint-vpcconfiguration-vpcid
            '''
            result = self._values.get("vpc_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_s3.CfnAccessPointProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "name": "name",
        "policy": "policy",
        "public_access_block_configuration": "publicAccessBlockConfiguration",
        "vpc_configuration": "vpcConfiguration",
    },
)
class CfnAccessPointProps:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        name: typing.Optional[builtins.str] = None,
        policy: typing.Any = None,
        public_access_block_configuration: typing.Optional[typing.Union[CfnAccessPoint.PublicAccessBlockConfigurationProperty, _IResolvable_a771d0ef]] = None,
        vpc_configuration: typing.Optional[typing.Union[CfnAccessPoint.VpcConfigurationProperty, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::S3::AccessPoint``.

        :param bucket: ``AWS::S3::AccessPoint.Bucket``.
        :param name: ``AWS::S3::AccessPoint.Name``.
        :param policy: ``AWS::S3::AccessPoint.Policy``.
        :param public_access_block_configuration: ``AWS::S3::AccessPoint.PublicAccessBlockConfiguration``.
        :param vpc_configuration: ``AWS::S3::AccessPoint.VpcConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
        }
        if name is not None:
            self._values["name"] = name
        if policy is not None:
            self._values["policy"] = policy
        if public_access_block_configuration is not None:
            self._values["public_access_block_configuration"] = public_access_block_configuration
        if vpc_configuration is not None:
            self._values["vpc_configuration"] = vpc_configuration

    @builtins.property
    def bucket(self) -> builtins.str:
        '''``AWS::S3::AccessPoint.Bucket``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-bucket
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::S3::AccessPoint.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Any:
        '''``AWS::S3::AccessPoint.Policy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def public_access_block_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnAccessPoint.PublicAccessBlockConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::S3::AccessPoint.PublicAccessBlockConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-publicaccessblockconfiguration
        '''
        result = self._values.get("public_access_block_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnAccessPoint.PublicAccessBlockConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def vpc_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnAccessPoint.VpcConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::S3::AccessPoint.VpcConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-accesspoint.html#cfn-s3-accesspoint-vpcconfiguration
        '''
        result = self._values.get("vpc_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnAccessPoint.VpcConfigurationProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessPointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnBucket(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_s3.CfnBucket",
):
    '''A CloudFormation ``AWS::S3::Bucket``.

    :cloudformationResource: AWS::S3::Bucket
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        accelerate_configuration: typing.Optional[typing.Union["CfnBucket.AccelerateConfigurationProperty", _IResolvable_a771d0ef]] = None,
        access_control: typing.Optional[builtins.str] = None,
        analytics_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.AnalyticsConfigurationProperty", _IResolvable_a771d0ef]]]] = None,
        bucket_encryption: typing.Optional[typing.Union["CfnBucket.BucketEncryptionProperty", _IResolvable_a771d0ef]] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        cors_configuration: typing.Optional[typing.Union["CfnBucket.CorsConfigurationProperty", _IResolvable_a771d0ef]] = None,
        intelligent_tiering_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.IntelligentTieringConfigurationProperty", _IResolvable_a771d0ef]]]] = None,
        inventory_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.InventoryConfigurationProperty", _IResolvable_a771d0ef]]]] = None,
        lifecycle_configuration: typing.Optional[typing.Union["CfnBucket.LifecycleConfigurationProperty", _IResolvable_a771d0ef]] = None,
        logging_configuration: typing.Optional[typing.Union["CfnBucket.LoggingConfigurationProperty", _IResolvable_a771d0ef]] = None,
        metrics_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.MetricsConfigurationProperty", _IResolvable_a771d0ef]]]] = None,
        notification_configuration: typing.Optional[typing.Union["CfnBucket.NotificationConfigurationProperty", _IResolvable_a771d0ef]] = None,
        object_lock_configuration: typing.Optional[typing.Union["CfnBucket.ObjectLockConfigurationProperty", _IResolvable_a771d0ef]] = None,
        object_lock_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ownership_controls: typing.Optional[typing.Union["CfnBucket.OwnershipControlsProperty", _IResolvable_a771d0ef]] = None,
        public_access_block_configuration: typing.Optional[typing.Union["CfnBucket.PublicAccessBlockConfigurationProperty", _IResolvable_a771d0ef]] = None,
        replication_configuration: typing.Optional[typing.Union["CfnBucket.ReplicationConfigurationProperty", _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
        versioning_configuration: typing.Optional[typing.Union["CfnBucket.VersioningConfigurationProperty", _IResolvable_a771d0ef]] = None,
        website_configuration: typing.Optional[typing.Union["CfnBucket.WebsiteConfigurationProperty", _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::S3::Bucket``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param accelerate_configuration: ``AWS::S3::Bucket.AccelerateConfiguration``.
        :param access_control: ``AWS::S3::Bucket.AccessControl``.
        :param analytics_configurations: ``AWS::S3::Bucket.AnalyticsConfigurations``.
        :param bucket_encryption: ``AWS::S3::Bucket.BucketEncryption``.
        :param bucket_name: ``AWS::S3::Bucket.BucketName``.
        :param cors_configuration: ``AWS::S3::Bucket.CorsConfiguration``.
        :param intelligent_tiering_configurations: ``AWS::S3::Bucket.IntelligentTieringConfigurations``.
        :param inventory_configurations: ``AWS::S3::Bucket.InventoryConfigurations``.
        :param lifecycle_configuration: ``AWS::S3::Bucket.LifecycleConfiguration``.
        :param logging_configuration: ``AWS::S3::Bucket.LoggingConfiguration``.
        :param metrics_configurations: ``AWS::S3::Bucket.MetricsConfigurations``.
        :param notification_configuration: ``AWS::S3::Bucket.NotificationConfiguration``.
        :param object_lock_configuration: ``AWS::S3::Bucket.ObjectLockConfiguration``.
        :param object_lock_enabled: ``AWS::S3::Bucket.ObjectLockEnabled``.
        :param ownership_controls: ``AWS::S3::Bucket.OwnershipControls``.
        :param public_access_block_configuration: ``AWS::S3::Bucket.PublicAccessBlockConfiguration``.
        :param replication_configuration: ``AWS::S3::Bucket.ReplicationConfiguration``.
        :param tags: ``AWS::S3::Bucket.Tags``.
        :param versioning_configuration: ``AWS::S3::Bucket.VersioningConfiguration``.
        :param website_configuration: ``AWS::S3::Bucket.WebsiteConfiguration``.
        '''
        props = CfnBucketProps(
            accelerate_configuration=accelerate_configuration,
            access_control=access_control,
            analytics_configurations=analytics_configurations,
            bucket_encryption=bucket_encryption,
            bucket_name=bucket_name,
            cors_configuration=cors_configuration,
            intelligent_tiering_configurations=intelligent_tiering_configurations,
            inventory_configurations=inventory_configurations,
            lifecycle_configuration=lifecycle_configuration,
            logging_configuration=logging_configuration,
            metrics_configurations=metrics_configurations,
            notification_configuration=notification_configuration,
            object_lock_configuration=object_lock_configuration,
            object_lock_enabled=object_lock_enabled,
            ownership_controls=ownership_controls,
            public_access_block_configuration=public_access_block_configuration,
            replication_configuration=replication_configuration,
            tags=tags,
            versioning_configuration=versioning_configuration,
            website_configuration=website_configuration,
        )

        jsii.create(CfnBucket, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrDomainName")
    def attr_domain_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: DomainName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDomainName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrDualStackDomainName")
    def attr_dual_stack_domain_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: DualStackDomainName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDualStackDomainName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrRegionalDomainName")
    def attr_regional_domain_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: RegionalDomainName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRegionalDomainName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrWebsiteUrl")
    def attr_website_url(self) -> builtins.str:
        '''
        :cloudformationAttribute: WebsiteURL
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrWebsiteUrl"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::S3::Bucket.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accelerateConfiguration")
    def accelerate_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnBucket.AccelerateConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.AccelerateConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-accelerateconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnBucket.AccelerateConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "accelerateConfiguration"))

    @accelerate_configuration.setter
    def accelerate_configuration(
        self,
        value: typing.Optional[typing.Union["CfnBucket.AccelerateConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "accelerateConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accessControl")
    def access_control(self) -> typing.Optional[builtins.str]:
        '''``AWS::S3::Bucket.AccessControl``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-accesscontrol
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessControl"))

    @access_control.setter
    def access_control(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "accessControl", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="analyticsConfigurations")
    def analytics_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.AnalyticsConfigurationProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::S3::Bucket.AnalyticsConfigurations``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-analyticsconfigurations
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.AnalyticsConfigurationProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "analyticsConfigurations"))

    @analytics_configurations.setter
    def analytics_configurations(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.AnalyticsConfigurationProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "analyticsConfigurations", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketEncryption")
    def bucket_encryption(
        self,
    ) -> typing.Optional[typing.Union["CfnBucket.BucketEncryptionProperty", _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.BucketEncryption``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-bucketencryption
        '''
        return typing.cast(typing.Optional[typing.Union["CfnBucket.BucketEncryptionProperty", _IResolvable_a771d0ef]], jsii.get(self, "bucketEncryption"))

    @bucket_encryption.setter
    def bucket_encryption(
        self,
        value: typing.Optional[typing.Union["CfnBucket.BucketEncryptionProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "bucketEncryption", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::S3::Bucket.BucketName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "bucketName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="corsConfiguration")
    def cors_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnBucket.CorsConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.CorsConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-crossoriginconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnBucket.CorsConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "corsConfiguration"))

    @cors_configuration.setter
    def cors_configuration(
        self,
        value: typing.Optional[typing.Union["CfnBucket.CorsConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "corsConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="intelligentTieringConfigurations")
    def intelligent_tiering_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.IntelligentTieringConfigurationProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::S3::Bucket.IntelligentTieringConfigurations``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-intelligenttieringconfigurations
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.IntelligentTieringConfigurationProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "intelligentTieringConfigurations"))

    @intelligent_tiering_configurations.setter
    def intelligent_tiering_configurations(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.IntelligentTieringConfigurationProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "intelligentTieringConfigurations", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="inventoryConfigurations")
    def inventory_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.InventoryConfigurationProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::S3::Bucket.InventoryConfigurations``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-inventoryconfigurations
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.InventoryConfigurationProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "inventoryConfigurations"))

    @inventory_configurations.setter
    def inventory_configurations(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.InventoryConfigurationProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "inventoryConfigurations", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lifecycleConfiguration")
    def lifecycle_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnBucket.LifecycleConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.LifecycleConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-lifecycleconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnBucket.LifecycleConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "lifecycleConfiguration"))

    @lifecycle_configuration.setter
    def lifecycle_configuration(
        self,
        value: typing.Optional[typing.Union["CfnBucket.LifecycleConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "lifecycleConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="loggingConfiguration")
    def logging_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnBucket.LoggingConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.LoggingConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-loggingconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnBucket.LoggingConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "loggingConfiguration"))

    @logging_configuration.setter
    def logging_configuration(
        self,
        value: typing.Optional[typing.Union["CfnBucket.LoggingConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "loggingConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="metricsConfigurations")
    def metrics_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.MetricsConfigurationProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::S3::Bucket.MetricsConfigurations``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-metricsconfigurations
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.MetricsConfigurationProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "metricsConfigurations"))

    @metrics_configurations.setter
    def metrics_configurations(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.MetricsConfigurationProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        jsii.set(self, "metricsConfigurations", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="notificationConfiguration")
    def notification_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnBucket.NotificationConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.NotificationConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-notification
        '''
        return typing.cast(typing.Optional[typing.Union["CfnBucket.NotificationConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "notificationConfiguration"))

    @notification_configuration.setter
    def notification_configuration(
        self,
        value: typing.Optional[typing.Union["CfnBucket.NotificationConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "notificationConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="objectLockConfiguration")
    def object_lock_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnBucket.ObjectLockConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.ObjectLockConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-objectlockconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnBucket.ObjectLockConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "objectLockConfiguration"))

    @object_lock_configuration.setter
    def object_lock_configuration(
        self,
        value: typing.Optional[typing.Union["CfnBucket.ObjectLockConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "objectLockConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="objectLockEnabled")
    def object_lock_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.ObjectLockEnabled``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-objectlockenabled
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "objectLockEnabled"))

    @object_lock_enabled.setter
    def object_lock_enabled(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "objectLockEnabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ownershipControls")
    def ownership_controls(
        self,
    ) -> typing.Optional[typing.Union["CfnBucket.OwnershipControlsProperty", _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.OwnershipControls``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-ownershipcontrols
        '''
        return typing.cast(typing.Optional[typing.Union["CfnBucket.OwnershipControlsProperty", _IResolvable_a771d0ef]], jsii.get(self, "ownershipControls"))

    @ownership_controls.setter
    def ownership_controls(
        self,
        value: typing.Optional[typing.Union["CfnBucket.OwnershipControlsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "ownershipControls", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="publicAccessBlockConfiguration")
    def public_access_block_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnBucket.PublicAccessBlockConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.PublicAccessBlockConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-publicaccessblockconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnBucket.PublicAccessBlockConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "publicAccessBlockConfiguration"))

    @public_access_block_configuration.setter
    def public_access_block_configuration(
        self,
        value: typing.Optional[typing.Union["CfnBucket.PublicAccessBlockConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "publicAccessBlockConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="replicationConfiguration")
    def replication_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnBucket.ReplicationConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.ReplicationConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-replicationconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnBucket.ReplicationConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "replicationConfiguration"))

    @replication_configuration.setter
    def replication_configuration(
        self,
        value: typing.Optional[typing.Union["CfnBucket.ReplicationConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "replicationConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="versioningConfiguration")
    def versioning_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnBucket.VersioningConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.VersioningConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-versioning
        '''
        return typing.cast(typing.Optional[typing.Union["CfnBucket.VersioningConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "versioningConfiguration"))

    @versioning_configuration.setter
    def versioning_configuration(
        self,
        value: typing.Optional[typing.Union["CfnBucket.VersioningConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "versioningConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="websiteConfiguration")
    def website_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnBucket.WebsiteConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.WebsiteConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-websiteconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnBucket.WebsiteConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "websiteConfiguration"))

    @website_configuration.setter
    def website_configuration(
        self,
        value: typing.Optional[typing.Union["CfnBucket.WebsiteConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "websiteConfiguration", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.AbortIncompleteMultipartUploadProperty",
        jsii_struct_bases=[],
        name_mapping={"days_after_initiation": "daysAfterInitiation"},
    )
    class AbortIncompleteMultipartUploadProperty:
        def __init__(self, *, days_after_initiation: jsii.Number) -> None:
            '''
            :param days_after_initiation: ``CfnBucket.AbortIncompleteMultipartUploadProperty.DaysAfterInitiation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-abortincompletemultipartupload.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "days_after_initiation": days_after_initiation,
            }

        @builtins.property
        def days_after_initiation(self) -> jsii.Number:
            '''``CfnBucket.AbortIncompleteMultipartUploadProperty.DaysAfterInitiation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-abortincompletemultipartupload.html#cfn-s3-bucket-abortincompletemultipartupload-daysafterinitiation
            '''
            result = self._values.get("days_after_initiation")
            assert result is not None, "Required property 'days_after_initiation' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AbortIncompleteMultipartUploadProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.AccelerateConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"acceleration_status": "accelerationStatus"},
    )
    class AccelerateConfigurationProperty:
        def __init__(self, *, acceleration_status: builtins.str) -> None:
            '''
            :param acceleration_status: ``CfnBucket.AccelerateConfigurationProperty.AccelerationStatus``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-accelerateconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "acceleration_status": acceleration_status,
            }

        @builtins.property
        def acceleration_status(self) -> builtins.str:
            '''``CfnBucket.AccelerateConfigurationProperty.AccelerationStatus``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-accelerateconfiguration.html#cfn-s3-bucket-accelerateconfiguration-accelerationstatus
            '''
            result = self._values.get("acceleration_status")
            assert result is not None, "Required property 'acceleration_status' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccelerateConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.AccessControlTranslationProperty",
        jsii_struct_bases=[],
        name_mapping={"owner": "owner"},
    )
    class AccessControlTranslationProperty:
        def __init__(self, *, owner: builtins.str) -> None:
            '''
            :param owner: ``CfnBucket.AccessControlTranslationProperty.Owner``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-accesscontroltranslation.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "owner": owner,
            }

        @builtins.property
        def owner(self) -> builtins.str:
            '''``CfnBucket.AccessControlTranslationProperty.Owner``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-accesscontroltranslation.html#cfn-s3-bucket-accesscontroltranslation-owner
            '''
            result = self._values.get("owner")
            assert result is not None, "Required property 'owner' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessControlTranslationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.AnalyticsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "storage_class_analysis": "storageClassAnalysis",
            "prefix": "prefix",
            "tag_filters": "tagFilters",
        },
    )
    class AnalyticsConfigurationProperty:
        def __init__(
            self,
            *,
            id: builtins.str,
            storage_class_analysis: typing.Union["CfnBucket.StorageClassAnalysisProperty", _IResolvable_a771d0ef],
            prefix: typing.Optional[builtins.str] = None,
            tag_filters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TagFilterProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param id: ``CfnBucket.AnalyticsConfigurationProperty.Id``.
            :param storage_class_analysis: ``CfnBucket.AnalyticsConfigurationProperty.StorageClassAnalysis``.
            :param prefix: ``CfnBucket.AnalyticsConfigurationProperty.Prefix``.
            :param tag_filters: ``CfnBucket.AnalyticsConfigurationProperty.TagFilters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-analyticsconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "id": id,
                "storage_class_analysis": storage_class_analysis,
            }
            if prefix is not None:
                self._values["prefix"] = prefix
            if tag_filters is not None:
                self._values["tag_filters"] = tag_filters

        @builtins.property
        def id(self) -> builtins.str:
            '''``CfnBucket.AnalyticsConfigurationProperty.Id``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-analyticsconfiguration.html#cfn-s3-bucket-analyticsconfiguration-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def storage_class_analysis(
            self,
        ) -> typing.Union["CfnBucket.StorageClassAnalysisProperty", _IResolvable_a771d0ef]:
            '''``CfnBucket.AnalyticsConfigurationProperty.StorageClassAnalysis``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-analyticsconfiguration.html#cfn-s3-bucket-analyticsconfiguration-storageclassanalysis
            '''
            result = self._values.get("storage_class_analysis")
            assert result is not None, "Required property 'storage_class_analysis' is missing"
            return typing.cast(typing.Union["CfnBucket.StorageClassAnalysisProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.AnalyticsConfigurationProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-analyticsconfiguration.html#cfn-s3-bucket-analyticsconfiguration-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_filters(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TagFilterProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBucket.AnalyticsConfigurationProperty.TagFilters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-analyticsconfiguration.html#cfn-s3-bucket-analyticsconfiguration-tagfilters
            '''
            result = self._values.get("tag_filters")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TagFilterProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnalyticsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.BucketEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "server_side_encryption_configuration": "serverSideEncryptionConfiguration",
        },
    )
    class BucketEncryptionProperty:
        def __init__(
            self,
            *,
            server_side_encryption_configuration: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.ServerSideEncryptionRuleProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param server_side_encryption_configuration: ``CfnBucket.BucketEncryptionProperty.ServerSideEncryptionConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-bucketencryption.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "server_side_encryption_configuration": server_side_encryption_configuration,
            }

        @builtins.property
        def server_side_encryption_configuration(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.ServerSideEncryptionRuleProperty", _IResolvable_a771d0ef]]]:
            '''``CfnBucket.BucketEncryptionProperty.ServerSideEncryptionConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-bucketencryption.html#cfn-s3-bucket-bucketencryption-serversideencryptionconfiguration
            '''
            result = self._values.get("server_side_encryption_configuration")
            assert result is not None, "Required property 'server_side_encryption_configuration' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.ServerSideEncryptionRuleProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BucketEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.CorsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"cors_rules": "corsRules"},
    )
    class CorsConfigurationProperty:
        def __init__(
            self,
            *,
            cors_rules: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.CorsRuleProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param cors_rules: ``CfnBucket.CorsConfigurationProperty.CorsRules``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "cors_rules": cors_rules,
            }

        @builtins.property
        def cors_rules(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.CorsRuleProperty", _IResolvable_a771d0ef]]]:
            '''``CfnBucket.CorsConfigurationProperty.CorsRules``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors.html#cfn-s3-bucket-cors-corsrule
            '''
            result = self._values.get("cors_rules")
            assert result is not None, "Required property 'cors_rules' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.CorsRuleProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CorsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.CorsRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_methods": "allowedMethods",
            "allowed_origins": "allowedOrigins",
            "allowed_headers": "allowedHeaders",
            "exposed_headers": "exposedHeaders",
            "id": "id",
            "max_age": "maxAge",
        },
    )
    class CorsRuleProperty:
        def __init__(
            self,
            *,
            allowed_methods: typing.List[builtins.str],
            allowed_origins: typing.List[builtins.str],
            allowed_headers: typing.Optional[typing.List[builtins.str]] = None,
            exposed_headers: typing.Optional[typing.List[builtins.str]] = None,
            id: typing.Optional[builtins.str] = None,
            max_age: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param allowed_methods: ``CfnBucket.CorsRuleProperty.AllowedMethods``.
            :param allowed_origins: ``CfnBucket.CorsRuleProperty.AllowedOrigins``.
            :param allowed_headers: ``CfnBucket.CorsRuleProperty.AllowedHeaders``.
            :param exposed_headers: ``CfnBucket.CorsRuleProperty.ExposedHeaders``.
            :param id: ``CfnBucket.CorsRuleProperty.Id``.
            :param max_age: ``CfnBucket.CorsRuleProperty.MaxAge``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors-corsrule.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "allowed_methods": allowed_methods,
                "allowed_origins": allowed_origins,
            }
            if allowed_headers is not None:
                self._values["allowed_headers"] = allowed_headers
            if exposed_headers is not None:
                self._values["exposed_headers"] = exposed_headers
            if id is not None:
                self._values["id"] = id
            if max_age is not None:
                self._values["max_age"] = max_age

        @builtins.property
        def allowed_methods(self) -> typing.List[builtins.str]:
            '''``CfnBucket.CorsRuleProperty.AllowedMethods``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors-corsrule.html#cfn-s3-bucket-cors-corsrule-allowedmethods
            '''
            result = self._values.get("allowed_methods")
            assert result is not None, "Required property 'allowed_methods' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def allowed_origins(self) -> typing.List[builtins.str]:
            '''``CfnBucket.CorsRuleProperty.AllowedOrigins``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors-corsrule.html#cfn-s3-bucket-cors-corsrule-allowedorigins
            '''
            result = self._values.get("allowed_origins")
            assert result is not None, "Required property 'allowed_origins' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def allowed_headers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnBucket.CorsRuleProperty.AllowedHeaders``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors-corsrule.html#cfn-s3-bucket-cors-corsrule-allowedheaders
            '''
            result = self._values.get("allowed_headers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def exposed_headers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnBucket.CorsRuleProperty.ExposedHeaders``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors-corsrule.html#cfn-s3-bucket-cors-corsrule-exposedheaders
            '''
            result = self._values.get("exposed_headers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.CorsRuleProperty.Id``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors-corsrule.html#cfn-s3-bucket-cors-corsrule-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_age(self) -> typing.Optional[jsii.Number]:
            '''``CfnBucket.CorsRuleProperty.MaxAge``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors-corsrule.html#cfn-s3-bucket-cors-corsrule-maxage
            '''
            result = self._values.get("max_age")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CorsRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.DataExportProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination": "destination",
            "output_schema_version": "outputSchemaVersion",
        },
    )
    class DataExportProperty:
        def __init__(
            self,
            *,
            destination: typing.Union["CfnBucket.DestinationProperty", _IResolvable_a771d0ef],
            output_schema_version: builtins.str,
        ) -> None:
            '''
            :param destination: ``CfnBucket.DataExportProperty.Destination``.
            :param output_schema_version: ``CfnBucket.DataExportProperty.OutputSchemaVersion``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-dataexport.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "destination": destination,
                "output_schema_version": output_schema_version,
            }

        @builtins.property
        def destination(
            self,
        ) -> typing.Union["CfnBucket.DestinationProperty", _IResolvable_a771d0ef]:
            '''``CfnBucket.DataExportProperty.Destination``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-dataexport.html#cfn-s3-bucket-dataexport-destination
            '''
            result = self._values.get("destination")
            assert result is not None, "Required property 'destination' is missing"
            return typing.cast(typing.Union["CfnBucket.DestinationProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def output_schema_version(self) -> builtins.str:
            '''``CfnBucket.DataExportProperty.OutputSchemaVersion``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-dataexport.html#cfn-s3-bucket-dataexport-outputschemaversion
            '''
            result = self._values.get("output_schema_version")
            assert result is not None, "Required property 'output_schema_version' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataExportProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.DefaultRetentionProperty",
        jsii_struct_bases=[],
        name_mapping={"days": "days", "mode": "mode", "years": "years"},
    )
    class DefaultRetentionProperty:
        def __init__(
            self,
            *,
            days: typing.Optional[jsii.Number] = None,
            mode: typing.Optional[builtins.str] = None,
            years: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param days: ``CfnBucket.DefaultRetentionProperty.Days``.
            :param mode: ``CfnBucket.DefaultRetentionProperty.Mode``.
            :param years: ``CfnBucket.DefaultRetentionProperty.Years``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-defaultretention.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if days is not None:
                self._values["days"] = days
            if mode is not None:
                self._values["mode"] = mode
            if years is not None:
                self._values["years"] = years

        @builtins.property
        def days(self) -> typing.Optional[jsii.Number]:
            '''``CfnBucket.DefaultRetentionProperty.Days``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-defaultretention.html#cfn-s3-bucket-defaultretention-days
            '''
            result = self._values.get("days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.DefaultRetentionProperty.Mode``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-defaultretention.html#cfn-s3-bucket-defaultretention-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def years(self) -> typing.Optional[jsii.Number]:
            '''``CfnBucket.DefaultRetentionProperty.Years``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-defaultretention.html#cfn-s3-bucket-defaultretention-years
            '''
            result = self._values.get("years")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultRetentionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.DeleteMarkerReplicationProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status"},
    )
    class DeleteMarkerReplicationProperty:
        def __init__(self, *, status: typing.Optional[builtins.str] = None) -> None:
            '''
            :param status: ``CfnBucket.DeleteMarkerReplicationProperty.Status``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-deletemarkerreplication.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.DeleteMarkerReplicationProperty.Status``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-deletemarkerreplication.html#cfn-s3-bucket-deletemarkerreplication-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeleteMarkerReplicationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.DestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_arn": "bucketArn",
            "format": "format",
            "bucket_account_id": "bucketAccountId",
            "prefix": "prefix",
        },
    )
    class DestinationProperty:
        def __init__(
            self,
            *,
            bucket_arn: builtins.str,
            format: builtins.str,
            bucket_account_id: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param bucket_arn: ``CfnBucket.DestinationProperty.BucketArn``.
            :param format: ``CfnBucket.DestinationProperty.Format``.
            :param bucket_account_id: ``CfnBucket.DestinationProperty.BucketAccountId``.
            :param prefix: ``CfnBucket.DestinationProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-destination.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bucket_arn": bucket_arn,
                "format": format,
            }
            if bucket_account_id is not None:
                self._values["bucket_account_id"] = bucket_account_id
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def bucket_arn(self) -> builtins.str:
            '''``CfnBucket.DestinationProperty.BucketArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-destination.html#cfn-s3-bucket-destination-bucketarn
            '''
            result = self._values.get("bucket_arn")
            assert result is not None, "Required property 'bucket_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def format(self) -> builtins.str:
            '''``CfnBucket.DestinationProperty.Format``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-destination.html#cfn-s3-bucket-destination-format
            '''
            result = self._values.get("format")
            assert result is not None, "Required property 'format' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def bucket_account_id(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.DestinationProperty.BucketAccountId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-destination.html#cfn-s3-bucket-destination-bucketaccountid
            '''
            result = self._values.get("bucket_account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.DestinationProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-destination.html#cfn-s3-bucket-destination-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.EncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"replica_kms_key_id": "replicaKmsKeyId"},
    )
    class EncryptionConfigurationProperty:
        def __init__(self, *, replica_kms_key_id: builtins.str) -> None:
            '''
            :param replica_kms_key_id: ``CfnBucket.EncryptionConfigurationProperty.ReplicaKmsKeyID``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-encryptionconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "replica_kms_key_id": replica_kms_key_id,
            }

        @builtins.property
        def replica_kms_key_id(self) -> builtins.str:
            '''``CfnBucket.EncryptionConfigurationProperty.ReplicaKmsKeyID``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-encryptionconfiguration.html#cfn-s3-bucket-encryptionconfiguration-replicakmskeyid
            '''
            result = self._values.get("replica_kms_key_id")
            assert result is not None, "Required property 'replica_kms_key_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.FilterRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class FilterRuleProperty:
        def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
            '''
            :param name: ``CfnBucket.FilterRuleProperty.Name``.
            :param value: ``CfnBucket.FilterRuleProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter-s3key-rules.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnBucket.FilterRuleProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter-s3key-rules.html#cfn-s3-bucket-notificationconfiguraiton-config-filter-s3key-rules-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''``CfnBucket.FilterRuleProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter-s3key-rules.html#cfn-s3-bucket-notificationconfiguraiton-config-filter-s3key-rules-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.IntelligentTieringConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "status": "status",
            "tierings": "tierings",
            "prefix": "prefix",
            "tag_filters": "tagFilters",
        },
    )
    class IntelligentTieringConfigurationProperty:
        def __init__(
            self,
            *,
            id: builtins.str,
            status: builtins.str,
            tierings: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TieringProperty", _IResolvable_a771d0ef]]],
            prefix: typing.Optional[builtins.str] = None,
            tag_filters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TagFilterProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param id: ``CfnBucket.IntelligentTieringConfigurationProperty.Id``.
            :param status: ``CfnBucket.IntelligentTieringConfigurationProperty.Status``.
            :param tierings: ``CfnBucket.IntelligentTieringConfigurationProperty.Tierings``.
            :param prefix: ``CfnBucket.IntelligentTieringConfigurationProperty.Prefix``.
            :param tag_filters: ``CfnBucket.IntelligentTieringConfigurationProperty.TagFilters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-intelligenttieringconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "id": id,
                "status": status,
                "tierings": tierings,
            }
            if prefix is not None:
                self._values["prefix"] = prefix
            if tag_filters is not None:
                self._values["tag_filters"] = tag_filters

        @builtins.property
        def id(self) -> builtins.str:
            '''``CfnBucket.IntelligentTieringConfigurationProperty.Id``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-intelligenttieringconfiguration.html#cfn-s3-bucket-intelligenttieringconfiguration-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def status(self) -> builtins.str:
            '''``CfnBucket.IntelligentTieringConfigurationProperty.Status``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-intelligenttieringconfiguration.html#cfn-s3-bucket-intelligenttieringconfiguration-status
            '''
            result = self._values.get("status")
            assert result is not None, "Required property 'status' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def tierings(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TieringProperty", _IResolvable_a771d0ef]]]:
            '''``CfnBucket.IntelligentTieringConfigurationProperty.Tierings``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-intelligenttieringconfiguration.html#cfn-s3-bucket-intelligenttieringconfiguration-tierings
            '''
            result = self._values.get("tierings")
            assert result is not None, "Required property 'tierings' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TieringProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.IntelligentTieringConfigurationProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-intelligenttieringconfiguration.html#cfn-s3-bucket-intelligenttieringconfiguration-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_filters(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TagFilterProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBucket.IntelligentTieringConfigurationProperty.TagFilters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-intelligenttieringconfiguration.html#cfn-s3-bucket-intelligenttieringconfiguration-tagfilters
            '''
            result = self._values.get("tag_filters")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TagFilterProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntelligentTieringConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.InventoryConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination": "destination",
            "enabled": "enabled",
            "id": "id",
            "included_object_versions": "includedObjectVersions",
            "schedule_frequency": "scheduleFrequency",
            "optional_fields": "optionalFields",
            "prefix": "prefix",
        },
    )
    class InventoryConfigurationProperty:
        def __init__(
            self,
            *,
            destination: typing.Union["CfnBucket.DestinationProperty", _IResolvable_a771d0ef],
            enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            id: builtins.str,
            included_object_versions: builtins.str,
            schedule_frequency: builtins.str,
            optional_fields: typing.Optional[typing.List[builtins.str]] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param destination: ``CfnBucket.InventoryConfigurationProperty.Destination``.
            :param enabled: ``CfnBucket.InventoryConfigurationProperty.Enabled``.
            :param id: ``CfnBucket.InventoryConfigurationProperty.Id``.
            :param included_object_versions: ``CfnBucket.InventoryConfigurationProperty.IncludedObjectVersions``.
            :param schedule_frequency: ``CfnBucket.InventoryConfigurationProperty.ScheduleFrequency``.
            :param optional_fields: ``CfnBucket.InventoryConfigurationProperty.OptionalFields``.
            :param prefix: ``CfnBucket.InventoryConfigurationProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "destination": destination,
                "enabled": enabled,
                "id": id,
                "included_object_versions": included_object_versions,
                "schedule_frequency": schedule_frequency,
            }
            if optional_fields is not None:
                self._values["optional_fields"] = optional_fields
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def destination(
            self,
        ) -> typing.Union["CfnBucket.DestinationProperty", _IResolvable_a771d0ef]:
            '''``CfnBucket.InventoryConfigurationProperty.Destination``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html#cfn-s3-bucket-inventoryconfiguration-destination
            '''
            result = self._values.get("destination")
            assert result is not None, "Required property 'destination' is missing"
            return typing.cast(typing.Union["CfnBucket.DestinationProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def enabled(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''``CfnBucket.InventoryConfigurationProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html#cfn-s3-bucket-inventoryconfiguration-enabled
            '''
            result = self._values.get("enabled")
            assert result is not None, "Required property 'enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        @builtins.property
        def id(self) -> builtins.str:
            '''``CfnBucket.InventoryConfigurationProperty.Id``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html#cfn-s3-bucket-inventoryconfiguration-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def included_object_versions(self) -> builtins.str:
            '''``CfnBucket.InventoryConfigurationProperty.IncludedObjectVersions``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html#cfn-s3-bucket-inventoryconfiguration-includedobjectversions
            '''
            result = self._values.get("included_object_versions")
            assert result is not None, "Required property 'included_object_versions' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def schedule_frequency(self) -> builtins.str:
            '''``CfnBucket.InventoryConfigurationProperty.ScheduleFrequency``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html#cfn-s3-bucket-inventoryconfiguration-schedulefrequency
            '''
            result = self._values.get("schedule_frequency")
            assert result is not None, "Required property 'schedule_frequency' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def optional_fields(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnBucket.InventoryConfigurationProperty.OptionalFields``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html#cfn-s3-bucket-inventoryconfiguration-optionalfields
            '''
            result = self._values.get("optional_fields")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.InventoryConfigurationProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-inventoryconfiguration.html#cfn-s3-bucket-inventoryconfiguration-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InventoryConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.LambdaConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"event": "event", "function": "function", "filter": "filter"},
    )
    class LambdaConfigurationProperty:
        def __init__(
            self,
            *,
            event: builtins.str,
            function: builtins.str,
            filter: typing.Optional[typing.Union["CfnBucket.NotificationFilterProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param event: ``CfnBucket.LambdaConfigurationProperty.Event``.
            :param function: ``CfnBucket.LambdaConfigurationProperty.Function``.
            :param filter: ``CfnBucket.LambdaConfigurationProperty.Filter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-lambdaconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "event": event,
                "function": function,
            }
            if filter is not None:
                self._values["filter"] = filter

        @builtins.property
        def event(self) -> builtins.str:
            '''``CfnBucket.LambdaConfigurationProperty.Event``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-lambdaconfig.html#cfn-s3-bucket-notificationconfig-lambdaconfig-event
            '''
            result = self._values.get("event")
            assert result is not None, "Required property 'event' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def function(self) -> builtins.str:
            '''``CfnBucket.LambdaConfigurationProperty.Function``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-lambdaconfig.html#cfn-s3-bucket-notificationconfig-lambdaconfig-function
            '''
            result = self._values.get("function")
            assert result is not None, "Required property 'function' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.NotificationFilterProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.LambdaConfigurationProperty.Filter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-lambdaconfig.html#cfn-s3-bucket-notificationconfig-lambdaconfig-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.NotificationFilterProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.LifecycleConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"rules": "rules"},
    )
    class LifecycleConfigurationProperty:
        def __init__(
            self,
            *,
            rules: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.RuleProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param rules: ``CfnBucket.LifecycleConfigurationProperty.Rules``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "rules": rules,
            }

        @builtins.property
        def rules(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.RuleProperty", _IResolvable_a771d0ef]]]:
            '''``CfnBucket.LifecycleConfigurationProperty.Rules``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig.html#cfn-s3-bucket-lifecycleconfig-rules
            '''
            result = self._values.get("rules")
            assert result is not None, "Required property 'rules' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.RuleProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LifecycleConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.LoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_bucket_name": "destinationBucketName",
            "log_file_prefix": "logFilePrefix",
        },
    )
    class LoggingConfigurationProperty:
        def __init__(
            self,
            *,
            destination_bucket_name: typing.Optional[builtins.str] = None,
            log_file_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param destination_bucket_name: ``CfnBucket.LoggingConfigurationProperty.DestinationBucketName``.
            :param log_file_prefix: ``CfnBucket.LoggingConfigurationProperty.LogFilePrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-loggingconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if destination_bucket_name is not None:
                self._values["destination_bucket_name"] = destination_bucket_name
            if log_file_prefix is not None:
                self._values["log_file_prefix"] = log_file_prefix

        @builtins.property
        def destination_bucket_name(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.LoggingConfigurationProperty.DestinationBucketName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-loggingconfig.html#cfn-s3-bucket-loggingconfig-destinationbucketname
            '''
            result = self._values.get("destination_bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def log_file_prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.LoggingConfigurationProperty.LogFilePrefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-loggingconfig.html#cfn-s3-bucket-loggingconfig-logfileprefix
            '''
            result = self._values.get("log_file_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.MetricsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "prefix": "prefix", "tag_filters": "tagFilters"},
    )
    class MetricsConfigurationProperty:
        def __init__(
            self,
            *,
            id: builtins.str,
            prefix: typing.Optional[builtins.str] = None,
            tag_filters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TagFilterProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param id: ``CfnBucket.MetricsConfigurationProperty.Id``.
            :param prefix: ``CfnBucket.MetricsConfigurationProperty.Prefix``.
            :param tag_filters: ``CfnBucket.MetricsConfigurationProperty.TagFilters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metricsconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "id": id,
            }
            if prefix is not None:
                self._values["prefix"] = prefix
            if tag_filters is not None:
                self._values["tag_filters"] = tag_filters

        @builtins.property
        def id(self) -> builtins.str:
            '''``CfnBucket.MetricsConfigurationProperty.Id``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metricsconfiguration.html#cfn-s3-bucket-metricsconfiguration-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.MetricsConfigurationProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metricsconfiguration.html#cfn-s3-bucket-metricsconfiguration-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_filters(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TagFilterProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBucket.MetricsConfigurationProperty.TagFilters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metricsconfiguration.html#cfn-s3-bucket-metricsconfiguration-tagfilters
            '''
            result = self._values.get("tag_filters")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TagFilterProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.MetricsProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status", "event_threshold": "eventThreshold"},
    )
    class MetricsProperty:
        def __init__(
            self,
            *,
            status: builtins.str,
            event_threshold: typing.Optional[typing.Union["CfnBucket.ReplicationTimeValueProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param status: ``CfnBucket.MetricsProperty.Status``.
            :param event_threshold: ``CfnBucket.MetricsProperty.EventThreshold``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metrics.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "status": status,
            }
            if event_threshold is not None:
                self._values["event_threshold"] = event_threshold

        @builtins.property
        def status(self) -> builtins.str:
            '''``CfnBucket.MetricsProperty.Status``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metrics.html#cfn-s3-bucket-metrics-status
            '''
            result = self._values.get("status")
            assert result is not None, "Required property 'status' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def event_threshold(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.ReplicationTimeValueProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.MetricsProperty.EventThreshold``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metrics.html#cfn-s3-bucket-metrics-eventthreshold
            '''
            result = self._values.get("event_threshold")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.ReplicationTimeValueProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.NoncurrentVersionTransitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "storage_class": "storageClass",
            "transition_in_days": "transitionInDays",
        },
    )
    class NoncurrentVersionTransitionProperty:
        def __init__(
            self,
            *,
            storage_class: builtins.str,
            transition_in_days: jsii.Number,
        ) -> None:
            '''
            :param storage_class: ``CfnBucket.NoncurrentVersionTransitionProperty.StorageClass``.
            :param transition_in_days: ``CfnBucket.NoncurrentVersionTransitionProperty.TransitionInDays``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule-noncurrentversiontransition.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "storage_class": storage_class,
                "transition_in_days": transition_in_days,
            }

        @builtins.property
        def storage_class(self) -> builtins.str:
            '''``CfnBucket.NoncurrentVersionTransitionProperty.StorageClass``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule-noncurrentversiontransition.html#cfn-s3-bucket-lifecycleconfig-rule-noncurrentversiontransition-storageclass
            '''
            result = self._values.get("storage_class")
            assert result is not None, "Required property 'storage_class' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def transition_in_days(self) -> jsii.Number:
            '''``CfnBucket.NoncurrentVersionTransitionProperty.TransitionInDays``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule-noncurrentversiontransition.html#cfn-s3-bucket-lifecycleconfig-rule-noncurrentversiontransition-transitionindays
            '''
            result = self._values.get("transition_in_days")
            assert result is not None, "Required property 'transition_in_days' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NoncurrentVersionTransitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.NotificationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lambda_configurations": "lambdaConfigurations",
            "queue_configurations": "queueConfigurations",
            "topic_configurations": "topicConfigurations",
        },
    )
    class NotificationConfigurationProperty:
        def __init__(
            self,
            *,
            lambda_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.LambdaConfigurationProperty", _IResolvable_a771d0ef]]]] = None,
            queue_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.QueueConfigurationProperty", _IResolvable_a771d0ef]]]] = None,
            topic_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TopicConfigurationProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param lambda_configurations: ``CfnBucket.NotificationConfigurationProperty.LambdaConfigurations``.
            :param queue_configurations: ``CfnBucket.NotificationConfigurationProperty.QueueConfigurations``.
            :param topic_configurations: ``CfnBucket.NotificationConfigurationProperty.TopicConfigurations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if lambda_configurations is not None:
                self._values["lambda_configurations"] = lambda_configurations
            if queue_configurations is not None:
                self._values["queue_configurations"] = queue_configurations
            if topic_configurations is not None:
                self._values["topic_configurations"] = topic_configurations

        @builtins.property
        def lambda_configurations(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.LambdaConfigurationProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBucket.NotificationConfigurationProperty.LambdaConfigurations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig.html#cfn-s3-bucket-notificationconfig-lambdaconfig
            '''
            result = self._values.get("lambda_configurations")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.LambdaConfigurationProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def queue_configurations(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.QueueConfigurationProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBucket.NotificationConfigurationProperty.QueueConfigurations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig.html#cfn-s3-bucket-notificationconfig-queueconfig
            '''
            result = self._values.get("queue_configurations")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.QueueConfigurationProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def topic_configurations(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TopicConfigurationProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBucket.NotificationConfigurationProperty.TopicConfigurations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig.html#cfn-s3-bucket-notificationconfig-topicconfig
            '''
            result = self._values.get("topic_configurations")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TopicConfigurationProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.NotificationFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_key": "s3Key"},
    )
    class NotificationFilterProperty:
        def __init__(
            self,
            *,
            s3_key: typing.Union["CfnBucket.S3KeyFilterProperty", _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param s3_key: ``CfnBucket.NotificationFilterProperty.S3Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "s3_key": s3_key,
            }

        @builtins.property
        def s3_key(
            self,
        ) -> typing.Union["CfnBucket.S3KeyFilterProperty", _IResolvable_a771d0ef]:
            '''``CfnBucket.NotificationFilterProperty.S3Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter.html#cfn-s3-bucket-notificationconfiguraiton-config-filter-s3key
            '''
            result = self._values.get("s3_key")
            assert result is not None, "Required property 's3_key' is missing"
            return typing.cast(typing.Union["CfnBucket.S3KeyFilterProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.ObjectLockConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"object_lock_enabled": "objectLockEnabled", "rule": "rule"},
    )
    class ObjectLockConfigurationProperty:
        def __init__(
            self,
            *,
            object_lock_enabled: typing.Optional[builtins.str] = None,
            rule: typing.Optional[typing.Union["CfnBucket.ObjectLockRuleProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param object_lock_enabled: ``CfnBucket.ObjectLockConfigurationProperty.ObjectLockEnabled``.
            :param rule: ``CfnBucket.ObjectLockConfigurationProperty.Rule``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-objectlockconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if object_lock_enabled is not None:
                self._values["object_lock_enabled"] = object_lock_enabled
            if rule is not None:
                self._values["rule"] = rule

        @builtins.property
        def object_lock_enabled(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.ObjectLockConfigurationProperty.ObjectLockEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-objectlockconfiguration.html#cfn-s3-bucket-objectlockconfiguration-objectlockenabled
            '''
            result = self._values.get("object_lock_enabled")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rule(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.ObjectLockRuleProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.ObjectLockConfigurationProperty.Rule``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-objectlockconfiguration.html#cfn-s3-bucket-objectlockconfiguration-rule
            '''
            result = self._values.get("rule")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.ObjectLockRuleProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ObjectLockConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.ObjectLockRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"default_retention": "defaultRetention"},
    )
    class ObjectLockRuleProperty:
        def __init__(
            self,
            *,
            default_retention: typing.Optional[typing.Union["CfnBucket.DefaultRetentionProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param default_retention: ``CfnBucket.ObjectLockRuleProperty.DefaultRetention``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-objectlockrule.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if default_retention is not None:
                self._values["default_retention"] = default_retention

        @builtins.property
        def default_retention(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.DefaultRetentionProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.ObjectLockRuleProperty.DefaultRetention``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-objectlockrule.html#cfn-s3-bucket-objectlockrule-defaultretention
            '''
            result = self._values.get("default_retention")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.DefaultRetentionProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ObjectLockRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.OwnershipControlsProperty",
        jsii_struct_bases=[],
        name_mapping={"rules": "rules"},
    )
    class OwnershipControlsProperty:
        def __init__(
            self,
            *,
            rules: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.OwnershipControlsRuleProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param rules: ``CfnBucket.OwnershipControlsProperty.Rules``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-ownershipcontrols.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "rules": rules,
            }

        @builtins.property
        def rules(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.OwnershipControlsRuleProperty", _IResolvable_a771d0ef]]]:
            '''``CfnBucket.OwnershipControlsProperty.Rules``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-ownershipcontrols.html#cfn-s3-bucket-ownershipcontrols-rules
            '''
            result = self._values.get("rules")
            assert result is not None, "Required property 'rules' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.OwnershipControlsRuleProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OwnershipControlsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.OwnershipControlsRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"object_ownership": "objectOwnership"},
    )
    class OwnershipControlsRuleProperty:
        def __init__(
            self,
            *,
            object_ownership: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param object_ownership: ``CfnBucket.OwnershipControlsRuleProperty.ObjectOwnership``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-ownershipcontrolsrule.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if object_ownership is not None:
                self._values["object_ownership"] = object_ownership

        @builtins.property
        def object_ownership(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.OwnershipControlsRuleProperty.ObjectOwnership``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-ownershipcontrolsrule.html#cfn-s3-bucket-ownershipcontrolsrule-objectownership
            '''
            result = self._values.get("object_ownership")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OwnershipControlsRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.PublicAccessBlockConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "block_public_acls": "blockPublicAcls",
            "block_public_policy": "blockPublicPolicy",
            "ignore_public_acls": "ignorePublicAcls",
            "restrict_public_buckets": "restrictPublicBuckets",
        },
    )
    class PublicAccessBlockConfigurationProperty:
        def __init__(
            self,
            *,
            block_public_acls: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            block_public_policy: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            ignore_public_acls: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            restrict_public_buckets: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param block_public_acls: ``CfnBucket.PublicAccessBlockConfigurationProperty.BlockPublicAcls``.
            :param block_public_policy: ``CfnBucket.PublicAccessBlockConfigurationProperty.BlockPublicPolicy``.
            :param ignore_public_acls: ``CfnBucket.PublicAccessBlockConfigurationProperty.IgnorePublicAcls``.
            :param restrict_public_buckets: ``CfnBucket.PublicAccessBlockConfigurationProperty.RestrictPublicBuckets``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-publicaccessblockconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if block_public_acls is not None:
                self._values["block_public_acls"] = block_public_acls
            if block_public_policy is not None:
                self._values["block_public_policy"] = block_public_policy
            if ignore_public_acls is not None:
                self._values["ignore_public_acls"] = ignore_public_acls
            if restrict_public_buckets is not None:
                self._values["restrict_public_buckets"] = restrict_public_buckets

        @builtins.property
        def block_public_acls(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnBucket.PublicAccessBlockConfigurationProperty.BlockPublicAcls``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-publicaccessblockconfiguration.html#cfn-s3-bucket-publicaccessblockconfiguration-blockpublicacls
            '''
            result = self._values.get("block_public_acls")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def block_public_policy(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnBucket.PublicAccessBlockConfigurationProperty.BlockPublicPolicy``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-publicaccessblockconfiguration.html#cfn-s3-bucket-publicaccessblockconfiguration-blockpublicpolicy
            '''
            result = self._values.get("block_public_policy")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def ignore_public_acls(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnBucket.PublicAccessBlockConfigurationProperty.IgnorePublicAcls``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-publicaccessblockconfiguration.html#cfn-s3-bucket-publicaccessblockconfiguration-ignorepublicacls
            '''
            result = self._values.get("ignore_public_acls")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def restrict_public_buckets(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnBucket.PublicAccessBlockConfigurationProperty.RestrictPublicBuckets``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-publicaccessblockconfiguration.html#cfn-s3-bucket-publicaccessblockconfiguration-restrictpublicbuckets
            '''
            result = self._values.get("restrict_public_buckets")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PublicAccessBlockConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.QueueConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"event": "event", "queue": "queue", "filter": "filter"},
    )
    class QueueConfigurationProperty:
        def __init__(
            self,
            *,
            event: builtins.str,
            queue: builtins.str,
            filter: typing.Optional[typing.Union["CfnBucket.NotificationFilterProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param event: ``CfnBucket.QueueConfigurationProperty.Event``.
            :param queue: ``CfnBucket.QueueConfigurationProperty.Queue``.
            :param filter: ``CfnBucket.QueueConfigurationProperty.Filter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-queueconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "event": event,
                "queue": queue,
            }
            if filter is not None:
                self._values["filter"] = filter

        @builtins.property
        def event(self) -> builtins.str:
            '''``CfnBucket.QueueConfigurationProperty.Event``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-queueconfig.html#cfn-s3-bucket-notificationconfig-queueconfig-event
            '''
            result = self._values.get("event")
            assert result is not None, "Required property 'event' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def queue(self) -> builtins.str:
            '''``CfnBucket.QueueConfigurationProperty.Queue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-queueconfig.html#cfn-s3-bucket-notificationconfig-queueconfig-queue
            '''
            result = self._values.get("queue")
            assert result is not None, "Required property 'queue' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.NotificationFilterProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.QueueConfigurationProperty.Filter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-queueconfig.html#cfn-s3-bucket-notificationconfig-queueconfig-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.NotificationFilterProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueueConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.RedirectAllRequestsToProperty",
        jsii_struct_bases=[],
        name_mapping={"host_name": "hostName", "protocol": "protocol"},
    )
    class RedirectAllRequestsToProperty:
        def __init__(
            self,
            *,
            host_name: builtins.str,
            protocol: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param host_name: ``CfnBucket.RedirectAllRequestsToProperty.HostName``.
            :param protocol: ``CfnBucket.RedirectAllRequestsToProperty.Protocol``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-redirectallrequeststo.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "host_name": host_name,
            }
            if protocol is not None:
                self._values["protocol"] = protocol

        @builtins.property
        def host_name(self) -> builtins.str:
            '''``CfnBucket.RedirectAllRequestsToProperty.HostName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-redirectallrequeststo.html#cfn-s3-websiteconfiguration-redirectallrequeststo-hostname
            '''
            result = self._values.get("host_name")
            assert result is not None, "Required property 'host_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.RedirectAllRequestsToProperty.Protocol``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-redirectallrequeststo.html#cfn-s3-websiteconfiguration-redirectallrequeststo-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedirectAllRequestsToProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.RedirectRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "host_name": "hostName",
            "http_redirect_code": "httpRedirectCode",
            "protocol": "protocol",
            "replace_key_prefix_with": "replaceKeyPrefixWith",
            "replace_key_with": "replaceKeyWith",
        },
    )
    class RedirectRuleProperty:
        def __init__(
            self,
            *,
            host_name: typing.Optional[builtins.str] = None,
            http_redirect_code: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
            replace_key_prefix_with: typing.Optional[builtins.str] = None,
            replace_key_with: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param host_name: ``CfnBucket.RedirectRuleProperty.HostName``.
            :param http_redirect_code: ``CfnBucket.RedirectRuleProperty.HttpRedirectCode``.
            :param protocol: ``CfnBucket.RedirectRuleProperty.Protocol``.
            :param replace_key_prefix_with: ``CfnBucket.RedirectRuleProperty.ReplaceKeyPrefixWith``.
            :param replace_key_with: ``CfnBucket.RedirectRuleProperty.ReplaceKeyWith``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules-redirectrule.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if host_name is not None:
                self._values["host_name"] = host_name
            if http_redirect_code is not None:
                self._values["http_redirect_code"] = http_redirect_code
            if protocol is not None:
                self._values["protocol"] = protocol
            if replace_key_prefix_with is not None:
                self._values["replace_key_prefix_with"] = replace_key_prefix_with
            if replace_key_with is not None:
                self._values["replace_key_with"] = replace_key_with

        @builtins.property
        def host_name(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.RedirectRuleProperty.HostName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules-redirectrule.html#cfn-s3-websiteconfiguration-redirectrule-hostname
            '''
            result = self._values.get("host_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def http_redirect_code(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.RedirectRuleProperty.HttpRedirectCode``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules-redirectrule.html#cfn-s3-websiteconfiguration-redirectrule-httpredirectcode
            '''
            result = self._values.get("http_redirect_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.RedirectRuleProperty.Protocol``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules-redirectrule.html#cfn-s3-websiteconfiguration-redirectrule-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def replace_key_prefix_with(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.RedirectRuleProperty.ReplaceKeyPrefixWith``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules-redirectrule.html#cfn-s3-websiteconfiguration-redirectrule-replacekeyprefixwith
            '''
            result = self._values.get("replace_key_prefix_with")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def replace_key_with(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.RedirectRuleProperty.ReplaceKeyWith``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules-redirectrule.html#cfn-s3-websiteconfiguration-redirectrule-replacekeywith
            '''
            result = self._values.get("replace_key_with")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RedirectRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.ReplicaModificationsProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status"},
    )
    class ReplicaModificationsProperty:
        def __init__(self, *, status: builtins.str) -> None:
            '''
            :param status: ``CfnBucket.ReplicaModificationsProperty.Status``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicamodifications.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "status": status,
            }

        @builtins.property
        def status(self) -> builtins.str:
            '''``CfnBucket.ReplicaModificationsProperty.Status``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicamodifications.html#cfn-s3-bucket-replicamodifications-status
            '''
            result = self._values.get("status")
            assert result is not None, "Required property 'status' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicaModificationsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.ReplicationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"role": "role", "rules": "rules"},
    )
    class ReplicationConfigurationProperty:
        def __init__(
            self,
            *,
            role: builtins.str,
            rules: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.ReplicationRuleProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param role: ``CfnBucket.ReplicationConfigurationProperty.Role``.
            :param rules: ``CfnBucket.ReplicationConfigurationProperty.Rules``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "role": role,
                "rules": rules,
            }

        @builtins.property
        def role(self) -> builtins.str:
            '''``CfnBucket.ReplicationConfigurationProperty.Role``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration.html#cfn-s3-bucket-replicationconfiguration-role
            '''
            result = self._values.get("role")
            assert result is not None, "Required property 'role' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def rules(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.ReplicationRuleProperty", _IResolvable_a771d0ef]]]:
            '''``CfnBucket.ReplicationConfigurationProperty.Rules``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration.html#cfn-s3-bucket-replicationconfiguration-rules
            '''
            result = self._values.get("rules")
            assert result is not None, "Required property 'rules' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.ReplicationRuleProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.ReplicationDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket": "bucket",
            "access_control_translation": "accessControlTranslation",
            "account": "account",
            "encryption_configuration": "encryptionConfiguration",
            "metrics": "metrics",
            "replication_time": "replicationTime",
            "storage_class": "storageClass",
        },
    )
    class ReplicationDestinationProperty:
        def __init__(
            self,
            *,
            bucket: builtins.str,
            access_control_translation: typing.Optional[typing.Union["CfnBucket.AccessControlTranslationProperty", _IResolvable_a771d0ef]] = None,
            account: typing.Optional[builtins.str] = None,
            encryption_configuration: typing.Optional[typing.Union["CfnBucket.EncryptionConfigurationProperty", _IResolvable_a771d0ef]] = None,
            metrics: typing.Optional[typing.Union["CfnBucket.MetricsProperty", _IResolvable_a771d0ef]] = None,
            replication_time: typing.Optional[typing.Union["CfnBucket.ReplicationTimeProperty", _IResolvable_a771d0ef]] = None,
            storage_class: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param bucket: ``CfnBucket.ReplicationDestinationProperty.Bucket``.
            :param access_control_translation: ``CfnBucket.ReplicationDestinationProperty.AccessControlTranslation``.
            :param account: ``CfnBucket.ReplicationDestinationProperty.Account``.
            :param encryption_configuration: ``CfnBucket.ReplicationDestinationProperty.EncryptionConfiguration``.
            :param metrics: ``CfnBucket.ReplicationDestinationProperty.Metrics``.
            :param replication_time: ``CfnBucket.ReplicationDestinationProperty.ReplicationTime``.
            :param storage_class: ``CfnBucket.ReplicationDestinationProperty.StorageClass``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules-destination.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bucket": bucket,
            }
            if access_control_translation is not None:
                self._values["access_control_translation"] = access_control_translation
            if account is not None:
                self._values["account"] = account
            if encryption_configuration is not None:
                self._values["encryption_configuration"] = encryption_configuration
            if metrics is not None:
                self._values["metrics"] = metrics
            if replication_time is not None:
                self._values["replication_time"] = replication_time
            if storage_class is not None:
                self._values["storage_class"] = storage_class

        @builtins.property
        def bucket(self) -> builtins.str:
            '''``CfnBucket.ReplicationDestinationProperty.Bucket``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules-destination.html#cfn-s3-bucket-replicationconfiguration-rules-destination-bucket
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def access_control_translation(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.AccessControlTranslationProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.ReplicationDestinationProperty.AccessControlTranslation``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules-destination.html#cfn-s3-bucket-replicationdestination-accesscontroltranslation
            '''
            result = self._values.get("access_control_translation")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.AccessControlTranslationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def account(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.ReplicationDestinationProperty.Account``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules-destination.html#cfn-s3-bucket-replicationdestination-account
            '''
            result = self._values.get("account")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.EncryptionConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.ReplicationDestinationProperty.EncryptionConfiguration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules-destination.html#cfn-s3-bucket-replicationdestination-encryptionconfiguration
            '''
            result = self._values.get("encryption_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.EncryptionConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def metrics(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.MetricsProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.ReplicationDestinationProperty.Metrics``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules-destination.html#cfn-s3-bucket-replicationdestination-metrics
            '''
            result = self._values.get("metrics")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.MetricsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def replication_time(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.ReplicationTimeProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.ReplicationDestinationProperty.ReplicationTime``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules-destination.html#cfn-s3-bucket-replicationdestination-replicationtime
            '''
            result = self._values.get("replication_time")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.ReplicationTimeProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def storage_class(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.ReplicationDestinationProperty.StorageClass``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules-destination.html#cfn-s3-bucket-replicationconfiguration-rules-destination-storageclass
            '''
            result = self._values.get("storage_class")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.ReplicationRuleAndOperatorProperty",
        jsii_struct_bases=[],
        name_mapping={"prefix": "prefix", "tag_filters": "tagFilters"},
    )
    class ReplicationRuleAndOperatorProperty:
        def __init__(
            self,
            *,
            prefix: typing.Optional[builtins.str] = None,
            tag_filters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TagFilterProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param prefix: ``CfnBucket.ReplicationRuleAndOperatorProperty.Prefix``.
            :param tag_filters: ``CfnBucket.ReplicationRuleAndOperatorProperty.TagFilters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationruleandoperator.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if prefix is not None:
                self._values["prefix"] = prefix
            if tag_filters is not None:
                self._values["tag_filters"] = tag_filters

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.ReplicationRuleAndOperatorProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationruleandoperator.html#cfn-s3-bucket-replicationruleandoperator-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_filters(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TagFilterProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBucket.ReplicationRuleAndOperatorProperty.TagFilters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationruleandoperator.html#cfn-s3-bucket-replicationruleandoperator-tagfilters
            '''
            result = self._values.get("tag_filters")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TagFilterProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationRuleAndOperatorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.ReplicationRuleFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"and_": "and", "prefix": "prefix", "tag_filter": "tagFilter"},
    )
    class ReplicationRuleFilterProperty:
        def __init__(
            self,
            *,
            and_: typing.Optional[typing.Union["CfnBucket.ReplicationRuleAndOperatorProperty", _IResolvable_a771d0ef]] = None,
            prefix: typing.Optional[builtins.str] = None,
            tag_filter: typing.Optional[typing.Union["CfnBucket.TagFilterProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param and_: ``CfnBucket.ReplicationRuleFilterProperty.And``.
            :param prefix: ``CfnBucket.ReplicationRuleFilterProperty.Prefix``.
            :param tag_filter: ``CfnBucket.ReplicationRuleFilterProperty.TagFilter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationrulefilter.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if and_ is not None:
                self._values["and_"] = and_
            if prefix is not None:
                self._values["prefix"] = prefix
            if tag_filter is not None:
                self._values["tag_filter"] = tag_filter

        @builtins.property
        def and_(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.ReplicationRuleAndOperatorProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.ReplicationRuleFilterProperty.And``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationrulefilter.html#cfn-s3-bucket-replicationrulefilter-and
            '''
            result = self._values.get("and_")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.ReplicationRuleAndOperatorProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.ReplicationRuleFilterProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationrulefilter.html#cfn-s3-bucket-replicationrulefilter-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_filter(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.TagFilterProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.ReplicationRuleFilterProperty.TagFilter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationrulefilter.html#cfn-s3-bucket-replicationrulefilter-tagfilter
            '''
            result = self._values.get("tag_filter")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.TagFilterProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationRuleFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.ReplicationRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination": "destination",
            "status": "status",
            "delete_marker_replication": "deleteMarkerReplication",
            "filter": "filter",
            "id": "id",
            "prefix": "prefix",
            "priority": "priority",
            "source_selection_criteria": "sourceSelectionCriteria",
        },
    )
    class ReplicationRuleProperty:
        def __init__(
            self,
            *,
            destination: typing.Union["CfnBucket.ReplicationDestinationProperty", _IResolvable_a771d0ef],
            status: builtins.str,
            delete_marker_replication: typing.Optional[typing.Union["CfnBucket.DeleteMarkerReplicationProperty", _IResolvable_a771d0ef]] = None,
            filter: typing.Optional[typing.Union["CfnBucket.ReplicationRuleFilterProperty", _IResolvable_a771d0ef]] = None,
            id: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
            priority: typing.Optional[jsii.Number] = None,
            source_selection_criteria: typing.Optional[typing.Union["CfnBucket.SourceSelectionCriteriaProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param destination: ``CfnBucket.ReplicationRuleProperty.Destination``.
            :param status: ``CfnBucket.ReplicationRuleProperty.Status``.
            :param delete_marker_replication: ``CfnBucket.ReplicationRuleProperty.DeleteMarkerReplication``.
            :param filter: ``CfnBucket.ReplicationRuleProperty.Filter``.
            :param id: ``CfnBucket.ReplicationRuleProperty.Id``.
            :param prefix: ``CfnBucket.ReplicationRuleProperty.Prefix``.
            :param priority: ``CfnBucket.ReplicationRuleProperty.Priority``.
            :param source_selection_criteria: ``CfnBucket.ReplicationRuleProperty.SourceSelectionCriteria``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "destination": destination,
                "status": status,
            }
            if delete_marker_replication is not None:
                self._values["delete_marker_replication"] = delete_marker_replication
            if filter is not None:
                self._values["filter"] = filter
            if id is not None:
                self._values["id"] = id
            if prefix is not None:
                self._values["prefix"] = prefix
            if priority is not None:
                self._values["priority"] = priority
            if source_selection_criteria is not None:
                self._values["source_selection_criteria"] = source_selection_criteria

        @builtins.property
        def destination(
            self,
        ) -> typing.Union["CfnBucket.ReplicationDestinationProperty", _IResolvable_a771d0ef]:
            '''``CfnBucket.ReplicationRuleProperty.Destination``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules.html#cfn-s3-bucket-replicationconfiguration-rules-destination
            '''
            result = self._values.get("destination")
            assert result is not None, "Required property 'destination' is missing"
            return typing.cast(typing.Union["CfnBucket.ReplicationDestinationProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def status(self) -> builtins.str:
            '''``CfnBucket.ReplicationRuleProperty.Status``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules.html#cfn-s3-bucket-replicationconfiguration-rules-status
            '''
            result = self._values.get("status")
            assert result is not None, "Required property 'status' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def delete_marker_replication(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.DeleteMarkerReplicationProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.ReplicationRuleProperty.DeleteMarkerReplication``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules.html#cfn-s3-bucket-replicationrule-deletemarkerreplication
            '''
            result = self._values.get("delete_marker_replication")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.DeleteMarkerReplicationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.ReplicationRuleFilterProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.ReplicationRuleProperty.Filter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules.html#cfn-s3-bucket-replicationrule-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.ReplicationRuleFilterProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.ReplicationRuleProperty.Id``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules.html#cfn-s3-bucket-replicationconfiguration-rules-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.ReplicationRuleProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules.html#cfn-s3-bucket-replicationconfiguration-rules-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            '''``CfnBucket.ReplicationRuleProperty.Priority``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules.html#cfn-s3-bucket-replicationrule-priority
            '''
            result = self._values.get("priority")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def source_selection_criteria(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.SourceSelectionCriteriaProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.ReplicationRuleProperty.SourceSelectionCriteria``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationconfiguration-rules.html#cfn-s3-bucket-replicationrule-sourceselectioncriteria
            '''
            result = self._values.get("source_selection_criteria")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.SourceSelectionCriteriaProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.ReplicationTimeProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status", "time": "time"},
    )
    class ReplicationTimeProperty:
        def __init__(
            self,
            *,
            status: builtins.str,
            time: typing.Union["CfnBucket.ReplicationTimeValueProperty", _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param status: ``CfnBucket.ReplicationTimeProperty.Status``.
            :param time: ``CfnBucket.ReplicationTimeProperty.Time``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationtime.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "status": status,
                "time": time,
            }

        @builtins.property
        def status(self) -> builtins.str:
            '''``CfnBucket.ReplicationTimeProperty.Status``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationtime.html#cfn-s3-bucket-replicationtime-status
            '''
            result = self._values.get("status")
            assert result is not None, "Required property 'status' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def time(
            self,
        ) -> typing.Union["CfnBucket.ReplicationTimeValueProperty", _IResolvable_a771d0ef]:
            '''``CfnBucket.ReplicationTimeProperty.Time``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationtime.html#cfn-s3-bucket-replicationtime-time
            '''
            result = self._values.get("time")
            assert result is not None, "Required property 'time' is missing"
            return typing.cast(typing.Union["CfnBucket.ReplicationTimeValueProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationTimeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.ReplicationTimeValueProperty",
        jsii_struct_bases=[],
        name_mapping={"minutes": "minutes"},
    )
    class ReplicationTimeValueProperty:
        def __init__(self, *, minutes: jsii.Number) -> None:
            '''
            :param minutes: ``CfnBucket.ReplicationTimeValueProperty.Minutes``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationtimevalue.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "minutes": minutes,
            }

        @builtins.property
        def minutes(self) -> jsii.Number:
            '''``CfnBucket.ReplicationTimeValueProperty.Minutes``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-replicationtimevalue.html#cfn-s3-bucket-replicationtimevalue-minutes
            '''
            result = self._values.get("minutes")
            assert result is not None, "Required property 'minutes' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationTimeValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.RoutingRuleConditionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "http_error_code_returned_equals": "httpErrorCodeReturnedEquals",
            "key_prefix_equals": "keyPrefixEquals",
        },
    )
    class RoutingRuleConditionProperty:
        def __init__(
            self,
            *,
            http_error_code_returned_equals: typing.Optional[builtins.str] = None,
            key_prefix_equals: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param http_error_code_returned_equals: ``CfnBucket.RoutingRuleConditionProperty.HttpErrorCodeReturnedEquals``.
            :param key_prefix_equals: ``CfnBucket.RoutingRuleConditionProperty.KeyPrefixEquals``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules-routingrulecondition.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if http_error_code_returned_equals is not None:
                self._values["http_error_code_returned_equals"] = http_error_code_returned_equals
            if key_prefix_equals is not None:
                self._values["key_prefix_equals"] = key_prefix_equals

        @builtins.property
        def http_error_code_returned_equals(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.RoutingRuleConditionProperty.HttpErrorCodeReturnedEquals``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules-routingrulecondition.html#cfn-s3-websiteconfiguration-routingrules-routingrulecondition-httperrorcodereturnedequals
            '''
            result = self._values.get("http_error_code_returned_equals")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_prefix_equals(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.RoutingRuleConditionProperty.KeyPrefixEquals``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules-routingrulecondition.html#cfn-s3-websiteconfiguration-routingrules-routingrulecondition-keyprefixequals
            '''
            result = self._values.get("key_prefix_equals")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RoutingRuleConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.RoutingRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "redirect_rule": "redirectRule",
            "routing_rule_condition": "routingRuleCondition",
        },
    )
    class RoutingRuleProperty:
        def __init__(
            self,
            *,
            redirect_rule: typing.Union["CfnBucket.RedirectRuleProperty", _IResolvable_a771d0ef],
            routing_rule_condition: typing.Optional[typing.Union["CfnBucket.RoutingRuleConditionProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param redirect_rule: ``CfnBucket.RoutingRuleProperty.RedirectRule``.
            :param routing_rule_condition: ``CfnBucket.RoutingRuleProperty.RoutingRuleCondition``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "redirect_rule": redirect_rule,
            }
            if routing_rule_condition is not None:
                self._values["routing_rule_condition"] = routing_rule_condition

        @builtins.property
        def redirect_rule(
            self,
        ) -> typing.Union["CfnBucket.RedirectRuleProperty", _IResolvable_a771d0ef]:
            '''``CfnBucket.RoutingRuleProperty.RedirectRule``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules.html#cfn-s3-websiteconfiguration-routingrules-redirectrule
            '''
            result = self._values.get("redirect_rule")
            assert result is not None, "Required property 'redirect_rule' is missing"
            return typing.cast(typing.Union["CfnBucket.RedirectRuleProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def routing_rule_condition(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.RoutingRuleConditionProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.RoutingRuleProperty.RoutingRuleCondition``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules.html#cfn-s3-websiteconfiguration-routingrules-routingrulecondition
            '''
            result = self._values.get("routing_rule_condition")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.RoutingRuleConditionProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RoutingRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "status": "status",
            "abort_incomplete_multipart_upload": "abortIncompleteMultipartUpload",
            "expiration_date": "expirationDate",
            "expiration_in_days": "expirationInDays",
            "id": "id",
            "noncurrent_version_expiration_in_days": "noncurrentVersionExpirationInDays",
            "noncurrent_version_transition": "noncurrentVersionTransition",
            "noncurrent_version_transitions": "noncurrentVersionTransitions",
            "prefix": "prefix",
            "tag_filters": "tagFilters",
            "transition": "transition",
            "transitions": "transitions",
        },
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            status: builtins.str,
            abort_incomplete_multipart_upload: typing.Optional[typing.Union["CfnBucket.AbortIncompleteMultipartUploadProperty", _IResolvable_a771d0ef]] = None,
            expiration_date: typing.Optional[typing.Union[_IResolvable_a771d0ef, datetime.datetime]] = None,
            expiration_in_days: typing.Optional[jsii.Number] = None,
            id: typing.Optional[builtins.str] = None,
            noncurrent_version_expiration_in_days: typing.Optional[jsii.Number] = None,
            noncurrent_version_transition: typing.Optional[typing.Union["CfnBucket.NoncurrentVersionTransitionProperty", _IResolvable_a771d0ef]] = None,
            noncurrent_version_transitions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.NoncurrentVersionTransitionProperty", _IResolvable_a771d0ef]]]] = None,
            prefix: typing.Optional[builtins.str] = None,
            tag_filters: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TagFilterProperty", _IResolvable_a771d0ef]]]] = None,
            transition: typing.Optional[typing.Union["CfnBucket.TransitionProperty", _IResolvable_a771d0ef]] = None,
            transitions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TransitionProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param status: ``CfnBucket.RuleProperty.Status``.
            :param abort_incomplete_multipart_upload: ``CfnBucket.RuleProperty.AbortIncompleteMultipartUpload``.
            :param expiration_date: ``CfnBucket.RuleProperty.ExpirationDate``.
            :param expiration_in_days: ``CfnBucket.RuleProperty.ExpirationInDays``.
            :param id: ``CfnBucket.RuleProperty.Id``.
            :param noncurrent_version_expiration_in_days: ``CfnBucket.RuleProperty.NoncurrentVersionExpirationInDays``.
            :param noncurrent_version_transition: ``CfnBucket.RuleProperty.NoncurrentVersionTransition``.
            :param noncurrent_version_transitions: ``CfnBucket.RuleProperty.NoncurrentVersionTransitions``.
            :param prefix: ``CfnBucket.RuleProperty.Prefix``.
            :param tag_filters: ``CfnBucket.RuleProperty.TagFilters``.
            :param transition: ``CfnBucket.RuleProperty.Transition``.
            :param transitions: ``CfnBucket.RuleProperty.Transitions``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "status": status,
            }
            if abort_incomplete_multipart_upload is not None:
                self._values["abort_incomplete_multipart_upload"] = abort_incomplete_multipart_upload
            if expiration_date is not None:
                self._values["expiration_date"] = expiration_date
            if expiration_in_days is not None:
                self._values["expiration_in_days"] = expiration_in_days
            if id is not None:
                self._values["id"] = id
            if noncurrent_version_expiration_in_days is not None:
                self._values["noncurrent_version_expiration_in_days"] = noncurrent_version_expiration_in_days
            if noncurrent_version_transition is not None:
                self._values["noncurrent_version_transition"] = noncurrent_version_transition
            if noncurrent_version_transitions is not None:
                self._values["noncurrent_version_transitions"] = noncurrent_version_transitions
            if prefix is not None:
                self._values["prefix"] = prefix
            if tag_filters is not None:
                self._values["tag_filters"] = tag_filters
            if transition is not None:
                self._values["transition"] = transition
            if transitions is not None:
                self._values["transitions"] = transitions

        @builtins.property
        def status(self) -> builtins.str:
            '''``CfnBucket.RuleProperty.Status``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-lifecycleconfig-rule-status
            '''
            result = self._values.get("status")
            assert result is not None, "Required property 'status' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def abort_incomplete_multipart_upload(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.AbortIncompleteMultipartUploadProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.RuleProperty.AbortIncompleteMultipartUpload``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-rule-abortincompletemultipartupload
            '''
            result = self._values.get("abort_incomplete_multipart_upload")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.AbortIncompleteMultipartUploadProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def expiration_date(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, datetime.datetime]]:
            '''``CfnBucket.RuleProperty.ExpirationDate``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-lifecycleconfig-rule-expirationdate
            '''
            result = self._values.get("expiration_date")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, datetime.datetime]], result)

        @builtins.property
        def expiration_in_days(self) -> typing.Optional[jsii.Number]:
            '''``CfnBucket.RuleProperty.ExpirationInDays``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-lifecycleconfig-rule-expirationindays
            '''
            result = self._values.get("expiration_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.RuleProperty.Id``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-lifecycleconfig-rule-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def noncurrent_version_expiration_in_days(self) -> typing.Optional[jsii.Number]:
            '''``CfnBucket.RuleProperty.NoncurrentVersionExpirationInDays``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-lifecycleconfig-rule-noncurrentversionexpirationindays
            '''
            result = self._values.get("noncurrent_version_expiration_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def noncurrent_version_transition(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.NoncurrentVersionTransitionProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.RuleProperty.NoncurrentVersionTransition``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-lifecycleconfig-rule-noncurrentversiontransition
            '''
            result = self._values.get("noncurrent_version_transition")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.NoncurrentVersionTransitionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def noncurrent_version_transitions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.NoncurrentVersionTransitionProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBucket.RuleProperty.NoncurrentVersionTransitions``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-lifecycleconfig-rule-noncurrentversiontransitions
            '''
            result = self._values.get("noncurrent_version_transitions")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.NoncurrentVersionTransitionProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.RuleProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-lifecycleconfig-rule-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_filters(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TagFilterProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBucket.RuleProperty.TagFilters``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-rule-tagfilters
            '''
            result = self._values.get("tag_filters")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TagFilterProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def transition(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.TransitionProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.RuleProperty.Transition``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-lifecycleconfig-rule-transition
            '''
            result = self._values.get("transition")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.TransitionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def transitions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TransitionProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBucket.RuleProperty.Transitions``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule.html#cfn-s3-bucket-lifecycleconfig-rule-transitions
            '''
            result = self._values.get("transitions")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.TransitionProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.S3KeyFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"rules": "rules"},
    )
    class S3KeyFilterProperty:
        def __init__(
            self,
            *,
            rules: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.FilterRuleProperty", _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param rules: ``CfnBucket.S3KeyFilterProperty.Rules``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter-s3key.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "rules": rules,
            }

        @builtins.property
        def rules(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.FilterRuleProperty", _IResolvable_a771d0ef]]]:
            '''``CfnBucket.S3KeyFilterProperty.Rules``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfiguration-config-filter-s3key.html#cfn-s3-bucket-notificationconfiguraiton-config-filter-s3key-rules
            '''
            result = self._values.get("rules")
            assert result is not None, "Required property 'rules' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.FilterRuleProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3KeyFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.ServerSideEncryptionByDefaultProperty",
        jsii_struct_bases=[],
        name_mapping={
            "sse_algorithm": "sseAlgorithm",
            "kms_master_key_id": "kmsMasterKeyId",
        },
    )
    class ServerSideEncryptionByDefaultProperty:
        def __init__(
            self,
            *,
            sse_algorithm: builtins.str,
            kms_master_key_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param sse_algorithm: ``CfnBucket.ServerSideEncryptionByDefaultProperty.SSEAlgorithm``.
            :param kms_master_key_id: ``CfnBucket.ServerSideEncryptionByDefaultProperty.KMSMasterKeyID``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-serversideencryptionbydefault.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "sse_algorithm": sse_algorithm,
            }
            if kms_master_key_id is not None:
                self._values["kms_master_key_id"] = kms_master_key_id

        @builtins.property
        def sse_algorithm(self) -> builtins.str:
            '''``CfnBucket.ServerSideEncryptionByDefaultProperty.SSEAlgorithm``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-serversideencryptionbydefault.html#cfn-s3-bucket-serversideencryptionbydefault-ssealgorithm
            '''
            result = self._values.get("sse_algorithm")
            assert result is not None, "Required property 'sse_algorithm' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def kms_master_key_id(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.ServerSideEncryptionByDefaultProperty.KMSMasterKeyID``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-serversideencryptionbydefault.html#cfn-s3-bucket-serversideencryptionbydefault-kmsmasterkeyid
            '''
            result = self._values.get("kms_master_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerSideEncryptionByDefaultProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.ServerSideEncryptionRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_key_enabled": "bucketKeyEnabled",
            "server_side_encryption_by_default": "serverSideEncryptionByDefault",
        },
    )
    class ServerSideEncryptionRuleProperty:
        def __init__(
            self,
            *,
            bucket_key_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            server_side_encryption_by_default: typing.Optional[typing.Union["CfnBucket.ServerSideEncryptionByDefaultProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param bucket_key_enabled: ``CfnBucket.ServerSideEncryptionRuleProperty.BucketKeyEnabled``.
            :param server_side_encryption_by_default: ``CfnBucket.ServerSideEncryptionRuleProperty.ServerSideEncryptionByDefault``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-serversideencryptionrule.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if bucket_key_enabled is not None:
                self._values["bucket_key_enabled"] = bucket_key_enabled
            if server_side_encryption_by_default is not None:
                self._values["server_side_encryption_by_default"] = server_side_encryption_by_default

        @builtins.property
        def bucket_key_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnBucket.ServerSideEncryptionRuleProperty.BucketKeyEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-serversideencryptionrule.html#cfn-s3-bucket-serversideencryptionrule-bucketkeyenabled
            '''
            result = self._values.get("bucket_key_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def server_side_encryption_by_default(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.ServerSideEncryptionByDefaultProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.ServerSideEncryptionRuleProperty.ServerSideEncryptionByDefault``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-serversideencryptionrule.html#cfn-s3-bucket-serversideencryptionrule-serversideencryptionbydefault
            '''
            result = self._values.get("server_side_encryption_by_default")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.ServerSideEncryptionByDefaultProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerSideEncryptionRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.SourceSelectionCriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "replica_modifications": "replicaModifications",
            "sse_kms_encrypted_objects": "sseKmsEncryptedObjects",
        },
    )
    class SourceSelectionCriteriaProperty:
        def __init__(
            self,
            *,
            replica_modifications: typing.Optional[typing.Union["CfnBucket.ReplicaModificationsProperty", _IResolvable_a771d0ef]] = None,
            sse_kms_encrypted_objects: typing.Optional[typing.Union["CfnBucket.SseKmsEncryptedObjectsProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param replica_modifications: ``CfnBucket.SourceSelectionCriteriaProperty.ReplicaModifications``.
            :param sse_kms_encrypted_objects: ``CfnBucket.SourceSelectionCriteriaProperty.SseKmsEncryptedObjects``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-sourceselectioncriteria.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if replica_modifications is not None:
                self._values["replica_modifications"] = replica_modifications
            if sse_kms_encrypted_objects is not None:
                self._values["sse_kms_encrypted_objects"] = sse_kms_encrypted_objects

        @builtins.property
        def replica_modifications(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.ReplicaModificationsProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.SourceSelectionCriteriaProperty.ReplicaModifications``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-sourceselectioncriteria.html#cfn-s3-bucket-sourceselectioncriteria-replicamodifications
            '''
            result = self._values.get("replica_modifications")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.ReplicaModificationsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sse_kms_encrypted_objects(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.SseKmsEncryptedObjectsProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.SourceSelectionCriteriaProperty.SseKmsEncryptedObjects``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-sourceselectioncriteria.html#cfn-s3-bucket-sourceselectioncriteria-ssekmsencryptedobjects
            '''
            result = self._values.get("sse_kms_encrypted_objects")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.SseKmsEncryptedObjectsProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceSelectionCriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.SseKmsEncryptedObjectsProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status"},
    )
    class SseKmsEncryptedObjectsProperty:
        def __init__(self, *, status: builtins.str) -> None:
            '''
            :param status: ``CfnBucket.SseKmsEncryptedObjectsProperty.Status``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-ssekmsencryptedobjects.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "status": status,
            }

        @builtins.property
        def status(self) -> builtins.str:
            '''``CfnBucket.SseKmsEncryptedObjectsProperty.Status``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-ssekmsencryptedobjects.html#cfn-s3-bucket-ssekmsencryptedobjects-status
            '''
            result = self._values.get("status")
            assert result is not None, "Required property 'status' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SseKmsEncryptedObjectsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.StorageClassAnalysisProperty",
        jsii_struct_bases=[],
        name_mapping={"data_export": "dataExport"},
    )
    class StorageClassAnalysisProperty:
        def __init__(
            self,
            *,
            data_export: typing.Optional[typing.Union["CfnBucket.DataExportProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param data_export: ``CfnBucket.StorageClassAnalysisProperty.DataExport``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-storageclassanalysis.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if data_export is not None:
                self._values["data_export"] = data_export

        @builtins.property
        def data_export(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.DataExportProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.StorageClassAnalysisProperty.DataExport``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-storageclassanalysis.html#cfn-s3-bucket-storageclassanalysis-dataexport
            '''
            result = self._values.get("data_export")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.DataExportProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageClassAnalysisProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.TagFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagFilterProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''
            :param key: ``CfnBucket.TagFilterProperty.Key``.
            :param value: ``CfnBucket.TagFilterProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-tagfilter.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''``CfnBucket.TagFilterProperty.Key``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-tagfilter.html#cfn-s3-bucket-tagfilter-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''``CfnBucket.TagFilterProperty.Value``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-tagfilter.html#cfn-s3-bucket-tagfilter-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.TieringProperty",
        jsii_struct_bases=[],
        name_mapping={"access_tier": "accessTier", "days": "days"},
    )
    class TieringProperty:
        def __init__(self, *, access_tier: builtins.str, days: jsii.Number) -> None:
            '''
            :param access_tier: ``CfnBucket.TieringProperty.AccessTier``.
            :param days: ``CfnBucket.TieringProperty.Days``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-tiering.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "access_tier": access_tier,
                "days": days,
            }

        @builtins.property
        def access_tier(self) -> builtins.str:
            '''``CfnBucket.TieringProperty.AccessTier``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-tiering.html#cfn-s3-bucket-tiering-accesstier
            '''
            result = self._values.get("access_tier")
            assert result is not None, "Required property 'access_tier' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def days(self) -> jsii.Number:
            '''``CfnBucket.TieringProperty.Days``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-tiering.html#cfn-s3-bucket-tiering-days
            '''
            result = self._values.get("days")
            assert result is not None, "Required property 'days' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TieringProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.TopicConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"event": "event", "topic": "topic", "filter": "filter"},
    )
    class TopicConfigurationProperty:
        def __init__(
            self,
            *,
            event: builtins.str,
            topic: builtins.str,
            filter: typing.Optional[typing.Union["CfnBucket.NotificationFilterProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param event: ``CfnBucket.TopicConfigurationProperty.Event``.
            :param topic: ``CfnBucket.TopicConfigurationProperty.Topic``.
            :param filter: ``CfnBucket.TopicConfigurationProperty.Filter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-topicconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "event": event,
                "topic": topic,
            }
            if filter is not None:
                self._values["filter"] = filter

        @builtins.property
        def event(self) -> builtins.str:
            '''``CfnBucket.TopicConfigurationProperty.Event``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-topicconfig.html#cfn-s3-bucket-notificationconfig-topicconfig-event
            '''
            result = self._values.get("event")
            assert result is not None, "Required property 'event' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def topic(self) -> builtins.str:
            '''``CfnBucket.TopicConfigurationProperty.Topic``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-topicconfig.html#cfn-s3-bucket-notificationconfig-topicconfig-topic
            '''
            result = self._values.get("topic")
            assert result is not None, "Required property 'topic' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.NotificationFilterProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.TopicConfigurationProperty.Filter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-notificationconfig-topicconfig.html#cfn-s3-bucket-notificationconfig-topicconfig-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.NotificationFilterProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TopicConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.TransitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "storage_class": "storageClass",
            "transition_date": "transitionDate",
            "transition_in_days": "transitionInDays",
        },
    )
    class TransitionProperty:
        def __init__(
            self,
            *,
            storage_class: builtins.str,
            transition_date: typing.Optional[typing.Union[_IResolvable_a771d0ef, datetime.datetime]] = None,
            transition_in_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param storage_class: ``CfnBucket.TransitionProperty.StorageClass``.
            :param transition_date: ``CfnBucket.TransitionProperty.TransitionDate``.
            :param transition_in_days: ``CfnBucket.TransitionProperty.TransitionInDays``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule-transition.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "storage_class": storage_class,
            }
            if transition_date is not None:
                self._values["transition_date"] = transition_date
            if transition_in_days is not None:
                self._values["transition_in_days"] = transition_in_days

        @builtins.property
        def storage_class(self) -> builtins.str:
            '''``CfnBucket.TransitionProperty.StorageClass``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule-transition.html#cfn-s3-bucket-lifecycleconfig-rule-transition-storageclass
            '''
            result = self._values.get("storage_class")
            assert result is not None, "Required property 'storage_class' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def transition_date(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, datetime.datetime]]:
            '''``CfnBucket.TransitionProperty.TransitionDate``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule-transition.html#cfn-s3-bucket-lifecycleconfig-rule-transition-transitiondate
            '''
            result = self._values.get("transition_date")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, datetime.datetime]], result)

        @builtins.property
        def transition_in_days(self) -> typing.Optional[jsii.Number]:
            '''``CfnBucket.TransitionProperty.TransitionInDays``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-lifecycleconfig-rule-transition.html#cfn-s3-bucket-lifecycleconfig-rule-transition-transitionindays
            '''
            result = self._values.get("transition_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TransitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.VersioningConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status"},
    )
    class VersioningConfigurationProperty:
        def __init__(self, *, status: builtins.str) -> None:
            '''
            :param status: ``CfnBucket.VersioningConfigurationProperty.Status``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-versioningconfig.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "status": status,
            }

        @builtins.property
        def status(self) -> builtins.str:
            '''``CfnBucket.VersioningConfigurationProperty.Status``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-versioningconfig.html#cfn-s3-bucket-versioningconfig-status
            '''
            result = self._values.get("status")
            assert result is not None, "Required property 'status' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VersioningConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnBucket.WebsiteConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "error_document": "errorDocument",
            "index_document": "indexDocument",
            "redirect_all_requests_to": "redirectAllRequestsTo",
            "routing_rules": "routingRules",
        },
    )
    class WebsiteConfigurationProperty:
        def __init__(
            self,
            *,
            error_document: typing.Optional[builtins.str] = None,
            index_document: typing.Optional[builtins.str] = None,
            redirect_all_requests_to: typing.Optional[typing.Union["CfnBucket.RedirectAllRequestsToProperty", _IResolvable_a771d0ef]] = None,
            routing_rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.RoutingRuleProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param error_document: ``CfnBucket.WebsiteConfigurationProperty.ErrorDocument``.
            :param index_document: ``CfnBucket.WebsiteConfigurationProperty.IndexDocument``.
            :param redirect_all_requests_to: ``CfnBucket.WebsiteConfigurationProperty.RedirectAllRequestsTo``.
            :param routing_rules: ``CfnBucket.WebsiteConfigurationProperty.RoutingRules``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if error_document is not None:
                self._values["error_document"] = error_document
            if index_document is not None:
                self._values["index_document"] = index_document
            if redirect_all_requests_to is not None:
                self._values["redirect_all_requests_to"] = redirect_all_requests_to
            if routing_rules is not None:
                self._values["routing_rules"] = routing_rules

        @builtins.property
        def error_document(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.WebsiteConfigurationProperty.ErrorDocument``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration.html#cfn-s3-websiteconfiguration-errordocument
            '''
            result = self._values.get("error_document")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def index_document(self) -> typing.Optional[builtins.str]:
            '''``CfnBucket.WebsiteConfigurationProperty.IndexDocument``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration.html#cfn-s3-websiteconfiguration-indexdocument
            '''
            result = self._values.get("index_document")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def redirect_all_requests_to(
            self,
        ) -> typing.Optional[typing.Union["CfnBucket.RedirectAllRequestsToProperty", _IResolvable_a771d0ef]]:
            '''``CfnBucket.WebsiteConfigurationProperty.RedirectAllRequestsTo``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration.html#cfn-s3-websiteconfiguration-redirectallrequeststo
            '''
            result = self._values.get("redirect_all_requests_to")
            return typing.cast(typing.Optional[typing.Union["CfnBucket.RedirectAllRequestsToProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def routing_rules(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.RoutingRuleProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBucket.WebsiteConfigurationProperty.RoutingRules``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration.html#cfn-s3-websiteconfiguration-routingrules
            '''
            result = self._values.get("routing_rules")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBucket.RoutingRuleProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebsiteConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnBucketPolicy(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_s3.CfnBucketPolicy",
):
    '''A CloudFormation ``AWS::S3::BucketPolicy``.

    :cloudformationResource: AWS::S3::BucketPolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-policy.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        bucket: builtins.str,
        policy_document: typing.Any,
    ) -> None:
        '''Create a new ``AWS::S3::BucketPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param bucket: ``AWS::S3::BucketPolicy.Bucket``.
        :param policy_document: ``AWS::S3::BucketPolicy.PolicyDocument``.
        '''
        props = CfnBucketPolicyProps(bucket=bucket, policy_document=policy_document)

        jsii.create(CfnBucketPolicy, self, [scope, id, props])

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
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        '''``AWS::S3::BucketPolicy.Bucket``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-policy.html#aws-properties-s3-policy-bucket
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        jsii.set(self, "bucket", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> typing.Any:
        '''``AWS::S3::BucketPolicy.PolicyDocument``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-policy.html#aws-properties-s3-policy-policydocument
        '''
        return typing.cast(typing.Any, jsii.get(self, "policyDocument"))

    @policy_document.setter
    def policy_document(self, value: typing.Any) -> None:
        jsii.set(self, "policyDocument", value)


@jsii.data_type(
    jsii_type="monocdk.aws_s3.CfnBucketPolicyProps",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "policy_document": "policyDocument"},
)
class CfnBucketPolicyProps:
    def __init__(self, *, bucket: builtins.str, policy_document: typing.Any) -> None:
        '''Properties for defining a ``AWS::S3::BucketPolicy``.

        :param bucket: ``AWS::S3::BucketPolicy.Bucket``.
        :param policy_document: ``AWS::S3::BucketPolicy.PolicyDocument``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-policy.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
            "policy_document": policy_document,
        }

    @builtins.property
    def bucket(self) -> builtins.str:
        '''``AWS::S3::BucketPolicy.Bucket``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-policy.html#aws-properties-s3-policy-bucket
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''``AWS::S3::BucketPolicy.PolicyDocument``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-policy.html#aws-properties-s3-policy-policydocument
        '''
        result = self._values.get("policy_document")
        assert result is not None, "Required property 'policy_document' is missing"
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBucketPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_s3.CfnBucketProps",
    jsii_struct_bases=[],
    name_mapping={
        "accelerate_configuration": "accelerateConfiguration",
        "access_control": "accessControl",
        "analytics_configurations": "analyticsConfigurations",
        "bucket_encryption": "bucketEncryption",
        "bucket_name": "bucketName",
        "cors_configuration": "corsConfiguration",
        "intelligent_tiering_configurations": "intelligentTieringConfigurations",
        "inventory_configurations": "inventoryConfigurations",
        "lifecycle_configuration": "lifecycleConfiguration",
        "logging_configuration": "loggingConfiguration",
        "metrics_configurations": "metricsConfigurations",
        "notification_configuration": "notificationConfiguration",
        "object_lock_configuration": "objectLockConfiguration",
        "object_lock_enabled": "objectLockEnabled",
        "ownership_controls": "ownershipControls",
        "public_access_block_configuration": "publicAccessBlockConfiguration",
        "replication_configuration": "replicationConfiguration",
        "tags": "tags",
        "versioning_configuration": "versioningConfiguration",
        "website_configuration": "websiteConfiguration",
    },
)
class CfnBucketProps:
    def __init__(
        self,
        *,
        accelerate_configuration: typing.Optional[typing.Union[CfnBucket.AccelerateConfigurationProperty, _IResolvable_a771d0ef]] = None,
        access_control: typing.Optional[builtins.str] = None,
        analytics_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBucket.AnalyticsConfigurationProperty, _IResolvable_a771d0ef]]]] = None,
        bucket_encryption: typing.Optional[typing.Union[CfnBucket.BucketEncryptionProperty, _IResolvable_a771d0ef]] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        cors_configuration: typing.Optional[typing.Union[CfnBucket.CorsConfigurationProperty, _IResolvable_a771d0ef]] = None,
        intelligent_tiering_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBucket.IntelligentTieringConfigurationProperty, _IResolvable_a771d0ef]]]] = None,
        inventory_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBucket.InventoryConfigurationProperty, _IResolvable_a771d0ef]]]] = None,
        lifecycle_configuration: typing.Optional[typing.Union[CfnBucket.LifecycleConfigurationProperty, _IResolvable_a771d0ef]] = None,
        logging_configuration: typing.Optional[typing.Union[CfnBucket.LoggingConfigurationProperty, _IResolvable_a771d0ef]] = None,
        metrics_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBucket.MetricsConfigurationProperty, _IResolvable_a771d0ef]]]] = None,
        notification_configuration: typing.Optional[typing.Union[CfnBucket.NotificationConfigurationProperty, _IResolvable_a771d0ef]] = None,
        object_lock_configuration: typing.Optional[typing.Union[CfnBucket.ObjectLockConfigurationProperty, _IResolvable_a771d0ef]] = None,
        object_lock_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ownership_controls: typing.Optional[typing.Union[CfnBucket.OwnershipControlsProperty, _IResolvable_a771d0ef]] = None,
        public_access_block_configuration: typing.Optional[typing.Union[CfnBucket.PublicAccessBlockConfigurationProperty, _IResolvable_a771d0ef]] = None,
        replication_configuration: typing.Optional[typing.Union[CfnBucket.ReplicationConfigurationProperty, _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
        versioning_configuration: typing.Optional[typing.Union[CfnBucket.VersioningConfigurationProperty, _IResolvable_a771d0ef]] = None,
        website_configuration: typing.Optional[typing.Union[CfnBucket.WebsiteConfigurationProperty, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::S3::Bucket``.

        :param accelerate_configuration: ``AWS::S3::Bucket.AccelerateConfiguration``.
        :param access_control: ``AWS::S3::Bucket.AccessControl``.
        :param analytics_configurations: ``AWS::S3::Bucket.AnalyticsConfigurations``.
        :param bucket_encryption: ``AWS::S3::Bucket.BucketEncryption``.
        :param bucket_name: ``AWS::S3::Bucket.BucketName``.
        :param cors_configuration: ``AWS::S3::Bucket.CorsConfiguration``.
        :param intelligent_tiering_configurations: ``AWS::S3::Bucket.IntelligentTieringConfigurations``.
        :param inventory_configurations: ``AWS::S3::Bucket.InventoryConfigurations``.
        :param lifecycle_configuration: ``AWS::S3::Bucket.LifecycleConfiguration``.
        :param logging_configuration: ``AWS::S3::Bucket.LoggingConfiguration``.
        :param metrics_configurations: ``AWS::S3::Bucket.MetricsConfigurations``.
        :param notification_configuration: ``AWS::S3::Bucket.NotificationConfiguration``.
        :param object_lock_configuration: ``AWS::S3::Bucket.ObjectLockConfiguration``.
        :param object_lock_enabled: ``AWS::S3::Bucket.ObjectLockEnabled``.
        :param ownership_controls: ``AWS::S3::Bucket.OwnershipControls``.
        :param public_access_block_configuration: ``AWS::S3::Bucket.PublicAccessBlockConfiguration``.
        :param replication_configuration: ``AWS::S3::Bucket.ReplicationConfiguration``.
        :param tags: ``AWS::S3::Bucket.Tags``.
        :param versioning_configuration: ``AWS::S3::Bucket.VersioningConfiguration``.
        :param website_configuration: ``AWS::S3::Bucket.WebsiteConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if accelerate_configuration is not None:
            self._values["accelerate_configuration"] = accelerate_configuration
        if access_control is not None:
            self._values["access_control"] = access_control
        if analytics_configurations is not None:
            self._values["analytics_configurations"] = analytics_configurations
        if bucket_encryption is not None:
            self._values["bucket_encryption"] = bucket_encryption
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if cors_configuration is not None:
            self._values["cors_configuration"] = cors_configuration
        if intelligent_tiering_configurations is not None:
            self._values["intelligent_tiering_configurations"] = intelligent_tiering_configurations
        if inventory_configurations is not None:
            self._values["inventory_configurations"] = inventory_configurations
        if lifecycle_configuration is not None:
            self._values["lifecycle_configuration"] = lifecycle_configuration
        if logging_configuration is not None:
            self._values["logging_configuration"] = logging_configuration
        if metrics_configurations is not None:
            self._values["metrics_configurations"] = metrics_configurations
        if notification_configuration is not None:
            self._values["notification_configuration"] = notification_configuration
        if object_lock_configuration is not None:
            self._values["object_lock_configuration"] = object_lock_configuration
        if object_lock_enabled is not None:
            self._values["object_lock_enabled"] = object_lock_enabled
        if ownership_controls is not None:
            self._values["ownership_controls"] = ownership_controls
        if public_access_block_configuration is not None:
            self._values["public_access_block_configuration"] = public_access_block_configuration
        if replication_configuration is not None:
            self._values["replication_configuration"] = replication_configuration
        if tags is not None:
            self._values["tags"] = tags
        if versioning_configuration is not None:
            self._values["versioning_configuration"] = versioning_configuration
        if website_configuration is not None:
            self._values["website_configuration"] = website_configuration

    @builtins.property
    def accelerate_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnBucket.AccelerateConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.AccelerateConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-accelerateconfiguration
        '''
        result = self._values.get("accelerate_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnBucket.AccelerateConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def access_control(self) -> typing.Optional[builtins.str]:
        '''``AWS::S3::Bucket.AccessControl``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-accesscontrol
        '''
        result = self._values.get("access_control")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def analytics_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBucket.AnalyticsConfigurationProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::S3::Bucket.AnalyticsConfigurations``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-analyticsconfigurations
        '''
        result = self._values.get("analytics_configurations")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBucket.AnalyticsConfigurationProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def bucket_encryption(
        self,
    ) -> typing.Optional[typing.Union[CfnBucket.BucketEncryptionProperty, _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.BucketEncryption``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-bucketencryption
        '''
        result = self._values.get("bucket_encryption")
        return typing.cast(typing.Optional[typing.Union[CfnBucket.BucketEncryptionProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::S3::Bucket.BucketName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-name
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cors_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnBucket.CorsConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.CorsConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-crossoriginconfig
        '''
        result = self._values.get("cors_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnBucket.CorsConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def intelligent_tiering_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBucket.IntelligentTieringConfigurationProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::S3::Bucket.IntelligentTieringConfigurations``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-intelligenttieringconfigurations
        '''
        result = self._values.get("intelligent_tiering_configurations")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBucket.IntelligentTieringConfigurationProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def inventory_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBucket.InventoryConfigurationProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::S3::Bucket.InventoryConfigurations``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-inventoryconfigurations
        '''
        result = self._values.get("inventory_configurations")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBucket.InventoryConfigurationProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def lifecycle_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnBucket.LifecycleConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.LifecycleConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-lifecycleconfig
        '''
        result = self._values.get("lifecycle_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnBucket.LifecycleConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def logging_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnBucket.LoggingConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.LoggingConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-loggingconfig
        '''
        result = self._values.get("logging_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnBucket.LoggingConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def metrics_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBucket.MetricsConfigurationProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::S3::Bucket.MetricsConfigurations``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-metricsconfigurations
        '''
        result = self._values.get("metrics_configurations")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBucket.MetricsConfigurationProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def notification_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnBucket.NotificationConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.NotificationConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-notification
        '''
        result = self._values.get("notification_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnBucket.NotificationConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def object_lock_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnBucket.ObjectLockConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.ObjectLockConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-objectlockconfiguration
        '''
        result = self._values.get("object_lock_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnBucket.ObjectLockConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def object_lock_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.ObjectLockEnabled``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-objectlockenabled
        '''
        result = self._values.get("object_lock_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def ownership_controls(
        self,
    ) -> typing.Optional[typing.Union[CfnBucket.OwnershipControlsProperty, _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.OwnershipControls``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-ownershipcontrols
        '''
        result = self._values.get("ownership_controls")
        return typing.cast(typing.Optional[typing.Union[CfnBucket.OwnershipControlsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def public_access_block_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnBucket.PublicAccessBlockConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.PublicAccessBlockConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-publicaccessblockconfiguration
        '''
        result = self._values.get("public_access_block_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnBucket.PublicAccessBlockConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def replication_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnBucket.ReplicationConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.ReplicationConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-replicationconfiguration
        '''
        result = self._values.get("replication_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnBucket.ReplicationConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::S3::Bucket.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def versioning_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnBucket.VersioningConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.VersioningConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-versioning
        '''
        result = self._values.get("versioning_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnBucket.VersioningConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def website_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnBucket.WebsiteConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::S3::Bucket.WebsiteConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket.html#cfn-s3-bucket-websiteconfiguration
        '''
        result = self._values.get("website_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnBucket.WebsiteConfigurationProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnStorageLens(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_s3.CfnStorageLens",
):
    '''A CloudFormation ``AWS::S3::StorageLens``.

    :cloudformationResource: AWS::S3::StorageLens
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-storagelens.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        storage_lens_configuration: typing.Union["CfnStorageLens.StorageLensConfigurationProperty", _IResolvable_a771d0ef],
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Create a new ``AWS::S3::StorageLens``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param storage_lens_configuration: ``AWS::S3::StorageLens.StorageLensConfiguration``.
        :param tags: ``AWS::S3::StorageLens.Tags``.
        '''
        props = CfnStorageLensProps(
            storage_lens_configuration=storage_lens_configuration, tags=tags
        )

        jsii.create(CfnStorageLens, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrStorageLensArn")
    def attr_storage_lens_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: StorageLensArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStorageLensArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::S3::StorageLens.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-storagelens.html#cfn-s3-storagelens-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="storageLensConfiguration")
    def storage_lens_configuration(
        self,
    ) -> typing.Union["CfnStorageLens.StorageLensConfigurationProperty", _IResolvable_a771d0ef]:
        '''``AWS::S3::StorageLens.StorageLensConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-storagelens.html#cfn-s3-storagelens-storagelensconfiguration
        '''
        return typing.cast(typing.Union["CfnStorageLens.StorageLensConfigurationProperty", _IResolvable_a771d0ef], jsii.get(self, "storageLensConfiguration"))

    @storage_lens_configuration.setter
    def storage_lens_configuration(
        self,
        value: typing.Union["CfnStorageLens.StorageLensConfigurationProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "storageLensConfiguration", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnStorageLens.AccountLevelProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_level": "bucketLevel",
            "activity_metrics": "activityMetrics",
        },
    )
    class AccountLevelProperty:
        def __init__(
            self,
            *,
            bucket_level: typing.Union["CfnStorageLens.BucketLevelProperty", _IResolvable_a771d0ef],
            activity_metrics: typing.Optional[typing.Union["CfnStorageLens.ActivityMetricsProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param bucket_level: ``CfnStorageLens.AccountLevelProperty.BucketLevel``.
            :param activity_metrics: ``CfnStorageLens.AccountLevelProperty.ActivityMetrics``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-accountlevel.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "bucket_level": bucket_level,
            }
            if activity_metrics is not None:
                self._values["activity_metrics"] = activity_metrics

        @builtins.property
        def bucket_level(
            self,
        ) -> typing.Union["CfnStorageLens.BucketLevelProperty", _IResolvable_a771d0ef]:
            '''``CfnStorageLens.AccountLevelProperty.BucketLevel``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-accountlevel.html#cfn-s3-storagelens-accountlevel-bucketlevel
            '''
            result = self._values.get("bucket_level")
            assert result is not None, "Required property 'bucket_level' is missing"
            return typing.cast(typing.Union["CfnStorageLens.BucketLevelProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def activity_metrics(
            self,
        ) -> typing.Optional[typing.Union["CfnStorageLens.ActivityMetricsProperty", _IResolvable_a771d0ef]]:
            '''``CfnStorageLens.AccountLevelProperty.ActivityMetrics``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-accountlevel.html#cfn-s3-storagelens-accountlevel-activitymetrics
            '''
            result = self._values.get("activity_metrics")
            return typing.cast(typing.Optional[typing.Union["CfnStorageLens.ActivityMetricsProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccountLevelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnStorageLens.ActivityMetricsProperty",
        jsii_struct_bases=[],
        name_mapping={"is_enabled": "isEnabled"},
    )
    class ActivityMetricsProperty:
        def __init__(
            self,
            *,
            is_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param is_enabled: ``CfnStorageLens.ActivityMetricsProperty.IsEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-activitymetrics.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if is_enabled is not None:
                self._values["is_enabled"] = is_enabled

        @builtins.property
        def is_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnStorageLens.ActivityMetricsProperty.IsEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-activitymetrics.html#cfn-s3-storagelens-activitymetrics-isenabled
            '''
            result = self._values.get("is_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActivityMetricsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnStorageLens.AwsOrgProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class AwsOrgProperty:
        def __init__(self, *, arn: builtins.str) -> None:
            '''
            :param arn: ``CfnStorageLens.AwsOrgProperty.Arn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-awsorg.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "arn": arn,
            }

        @builtins.property
        def arn(self) -> builtins.str:
            '''``CfnStorageLens.AwsOrgProperty.Arn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-awsorg.html#cfn-s3-storagelens-awsorg-arn
            '''
            result = self._values.get("arn")
            assert result is not None, "Required property 'arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsOrgProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnStorageLens.BucketLevelProperty",
        jsii_struct_bases=[],
        name_mapping={
            "activity_metrics": "activityMetrics",
            "prefix_level": "prefixLevel",
        },
    )
    class BucketLevelProperty:
        def __init__(
            self,
            *,
            activity_metrics: typing.Optional[typing.Union["CfnStorageLens.ActivityMetricsProperty", _IResolvable_a771d0ef]] = None,
            prefix_level: typing.Optional[typing.Union["CfnStorageLens.PrefixLevelProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param activity_metrics: ``CfnStorageLens.BucketLevelProperty.ActivityMetrics``.
            :param prefix_level: ``CfnStorageLens.BucketLevelProperty.PrefixLevel``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-bucketlevel.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if activity_metrics is not None:
                self._values["activity_metrics"] = activity_metrics
            if prefix_level is not None:
                self._values["prefix_level"] = prefix_level

        @builtins.property
        def activity_metrics(
            self,
        ) -> typing.Optional[typing.Union["CfnStorageLens.ActivityMetricsProperty", _IResolvable_a771d0ef]]:
            '''``CfnStorageLens.BucketLevelProperty.ActivityMetrics``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-bucketlevel.html#cfn-s3-storagelens-bucketlevel-activitymetrics
            '''
            result = self._values.get("activity_metrics")
            return typing.cast(typing.Optional[typing.Union["CfnStorageLens.ActivityMetricsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def prefix_level(
            self,
        ) -> typing.Optional[typing.Union["CfnStorageLens.PrefixLevelProperty", _IResolvable_a771d0ef]]:
            '''``CfnStorageLens.BucketLevelProperty.PrefixLevel``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-bucketlevel.html#cfn-s3-storagelens-bucketlevel-prefixlevel
            '''
            result = self._values.get("prefix_level")
            return typing.cast(typing.Optional[typing.Union["CfnStorageLens.PrefixLevelProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BucketLevelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnStorageLens.BucketsAndRegionsProperty",
        jsii_struct_bases=[],
        name_mapping={"buckets": "buckets", "regions": "regions"},
    )
    class BucketsAndRegionsProperty:
        def __init__(
            self,
            *,
            buckets: typing.Optional[typing.List[builtins.str]] = None,
            regions: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            '''
            :param buckets: ``CfnStorageLens.BucketsAndRegionsProperty.Buckets``.
            :param regions: ``CfnStorageLens.BucketsAndRegionsProperty.Regions``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-bucketsandregions.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if buckets is not None:
                self._values["buckets"] = buckets
            if regions is not None:
                self._values["regions"] = regions

        @builtins.property
        def buckets(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnStorageLens.BucketsAndRegionsProperty.Buckets``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-bucketsandregions.html#cfn-s3-storagelens-bucketsandregions-buckets
            '''
            result = self._values.get("buckets")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def regions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnStorageLens.BucketsAndRegionsProperty.Regions``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-bucketsandregions.html#cfn-s3-storagelens-bucketsandregions-regions
            '''
            result = self._values.get("regions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BucketsAndRegionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnStorageLens.DataExportProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_bucket_destination": "s3BucketDestination"},
    )
    class DataExportProperty:
        def __init__(
            self,
            *,
            s3_bucket_destination: typing.Union["CfnStorageLens.S3BucketDestinationProperty", _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param s3_bucket_destination: ``CfnStorageLens.DataExportProperty.S3BucketDestination``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-dataexport.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "s3_bucket_destination": s3_bucket_destination,
            }

        @builtins.property
        def s3_bucket_destination(
            self,
        ) -> typing.Union["CfnStorageLens.S3BucketDestinationProperty", _IResolvable_a771d0ef]:
            '''``CfnStorageLens.DataExportProperty.S3BucketDestination``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-dataexport.html#cfn-s3-storagelens-dataexport-s3bucketdestination
            '''
            result = self._values.get("s3_bucket_destination")
            assert result is not None, "Required property 's3_bucket_destination' is missing"
            return typing.cast(typing.Union["CfnStorageLens.S3BucketDestinationProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataExportProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnStorageLens.EncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={},
    )
    class EncryptionProperty:
        def __init__(self) -> None:
            '''
            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-encryption.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnStorageLens.PrefixLevelProperty",
        jsii_struct_bases=[],
        name_mapping={"storage_metrics": "storageMetrics"},
    )
    class PrefixLevelProperty:
        def __init__(
            self,
            *,
            storage_metrics: typing.Union["CfnStorageLens.PrefixLevelStorageMetricsProperty", _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param storage_metrics: ``CfnStorageLens.PrefixLevelProperty.StorageMetrics``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-prefixlevel.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "storage_metrics": storage_metrics,
            }

        @builtins.property
        def storage_metrics(
            self,
        ) -> typing.Union["CfnStorageLens.PrefixLevelStorageMetricsProperty", _IResolvable_a771d0ef]:
            '''``CfnStorageLens.PrefixLevelProperty.StorageMetrics``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-prefixlevel.html#cfn-s3-storagelens-prefixlevel-storagemetrics
            '''
            result = self._values.get("storage_metrics")
            assert result is not None, "Required property 'storage_metrics' is missing"
            return typing.cast(typing.Union["CfnStorageLens.PrefixLevelStorageMetricsProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrefixLevelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnStorageLens.PrefixLevelStorageMetricsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "is_enabled": "isEnabled",
            "selection_criteria": "selectionCriteria",
        },
    )
    class PrefixLevelStorageMetricsProperty:
        def __init__(
            self,
            *,
            is_enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            selection_criteria: typing.Optional[typing.Union["CfnStorageLens.SelectionCriteriaProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param is_enabled: ``CfnStorageLens.PrefixLevelStorageMetricsProperty.IsEnabled``.
            :param selection_criteria: ``CfnStorageLens.PrefixLevelStorageMetricsProperty.SelectionCriteria``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-prefixlevelstoragemetrics.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if is_enabled is not None:
                self._values["is_enabled"] = is_enabled
            if selection_criteria is not None:
                self._values["selection_criteria"] = selection_criteria

        @builtins.property
        def is_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnStorageLens.PrefixLevelStorageMetricsProperty.IsEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-prefixlevelstoragemetrics.html#cfn-s3-storagelens-prefixlevelstoragemetrics-isenabled
            '''
            result = self._values.get("is_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def selection_criteria(
            self,
        ) -> typing.Optional[typing.Union["CfnStorageLens.SelectionCriteriaProperty", _IResolvable_a771d0ef]]:
            '''``CfnStorageLens.PrefixLevelStorageMetricsProperty.SelectionCriteria``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-prefixlevelstoragemetrics.html#cfn-s3-storagelens-prefixlevelstoragemetrics-selectioncriteria
            '''
            result = self._values.get("selection_criteria")
            return typing.cast(typing.Optional[typing.Union["CfnStorageLens.SelectionCriteriaProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrefixLevelStorageMetricsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnStorageLens.S3BucketDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_id": "accountId",
            "arn": "arn",
            "format": "format",
            "output_schema_version": "outputSchemaVersion",
            "encryption": "encryption",
            "prefix": "prefix",
        },
    )
    class S3BucketDestinationProperty:
        def __init__(
            self,
            *,
            account_id: builtins.str,
            arn: builtins.str,
            format: builtins.str,
            output_schema_version: builtins.str,
            encryption: typing.Optional[typing.Union["CfnStorageLens.EncryptionProperty", _IResolvable_a771d0ef]] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param account_id: ``CfnStorageLens.S3BucketDestinationProperty.AccountId``.
            :param arn: ``CfnStorageLens.S3BucketDestinationProperty.Arn``.
            :param format: ``CfnStorageLens.S3BucketDestinationProperty.Format``.
            :param output_schema_version: ``CfnStorageLens.S3BucketDestinationProperty.OutputSchemaVersion``.
            :param encryption: ``CfnStorageLens.S3BucketDestinationProperty.Encryption``.
            :param prefix: ``CfnStorageLens.S3BucketDestinationProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-s3bucketdestination.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "account_id": account_id,
                "arn": arn,
                "format": format,
                "output_schema_version": output_schema_version,
            }
            if encryption is not None:
                self._values["encryption"] = encryption
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def account_id(self) -> builtins.str:
            '''``CfnStorageLens.S3BucketDestinationProperty.AccountId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-s3bucketdestination.html#cfn-s3-storagelens-s3bucketdestination-accountid
            '''
            result = self._values.get("account_id")
            assert result is not None, "Required property 'account_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def arn(self) -> builtins.str:
            '''``CfnStorageLens.S3BucketDestinationProperty.Arn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-s3bucketdestination.html#cfn-s3-storagelens-s3bucketdestination-arn
            '''
            result = self._values.get("arn")
            assert result is not None, "Required property 'arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def format(self) -> builtins.str:
            '''``CfnStorageLens.S3BucketDestinationProperty.Format``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-s3bucketdestination.html#cfn-s3-storagelens-s3bucketdestination-format
            '''
            result = self._values.get("format")
            assert result is not None, "Required property 'format' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def output_schema_version(self) -> builtins.str:
            '''``CfnStorageLens.S3BucketDestinationProperty.OutputSchemaVersion``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-s3bucketdestination.html#cfn-s3-storagelens-s3bucketdestination-outputschemaversion
            '''
            result = self._values.get("output_schema_version")
            assert result is not None, "Required property 'output_schema_version' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def encryption(
            self,
        ) -> typing.Optional[typing.Union["CfnStorageLens.EncryptionProperty", _IResolvable_a771d0ef]]:
            '''``CfnStorageLens.S3BucketDestinationProperty.Encryption``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-s3bucketdestination.html#cfn-s3-storagelens-s3bucketdestination-encryption
            '''
            result = self._values.get("encryption")
            return typing.cast(typing.Optional[typing.Union["CfnStorageLens.EncryptionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnStorageLens.S3BucketDestinationProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-s3bucketdestination.html#cfn-s3-storagelens-s3bucketdestination-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3BucketDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnStorageLens.SelectionCriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delimiter": "delimiter",
            "max_depth": "maxDepth",
            "min_storage_bytes_percentage": "minStorageBytesPercentage",
        },
    )
    class SelectionCriteriaProperty:
        def __init__(
            self,
            *,
            delimiter: typing.Optional[builtins.str] = None,
            max_depth: typing.Optional[jsii.Number] = None,
            min_storage_bytes_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param delimiter: ``CfnStorageLens.SelectionCriteriaProperty.Delimiter``.
            :param max_depth: ``CfnStorageLens.SelectionCriteriaProperty.MaxDepth``.
            :param min_storage_bytes_percentage: ``CfnStorageLens.SelectionCriteriaProperty.MinStorageBytesPercentage``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-selectioncriteria.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if delimiter is not None:
                self._values["delimiter"] = delimiter
            if max_depth is not None:
                self._values["max_depth"] = max_depth
            if min_storage_bytes_percentage is not None:
                self._values["min_storage_bytes_percentage"] = min_storage_bytes_percentage

        @builtins.property
        def delimiter(self) -> typing.Optional[builtins.str]:
            '''``CfnStorageLens.SelectionCriteriaProperty.Delimiter``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-selectioncriteria.html#cfn-s3-storagelens-selectioncriteria-delimiter
            '''
            result = self._values.get("delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_depth(self) -> typing.Optional[jsii.Number]:
            '''``CfnStorageLens.SelectionCriteriaProperty.MaxDepth``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-selectioncriteria.html#cfn-s3-storagelens-selectioncriteria-maxdepth
            '''
            result = self._values.get("max_depth")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_storage_bytes_percentage(self) -> typing.Optional[jsii.Number]:
            '''``CfnStorageLens.SelectionCriteriaProperty.MinStorageBytesPercentage``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-selectioncriteria.html#cfn-s3-storagelens-selectioncriteria-minstoragebytespercentage
            '''
            result = self._values.get("min_storage_bytes_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SelectionCriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_s3.CfnStorageLens.StorageLensConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_level": "accountLevel",
            "id": "id",
            "is_enabled": "isEnabled",
            "aws_org": "awsOrg",
            "data_export": "dataExport",
            "exclude": "exclude",
            "include": "include",
            "storage_lens_arn": "storageLensArn",
        },
    )
    class StorageLensConfigurationProperty:
        def __init__(
            self,
            *,
            account_level: typing.Union["CfnStorageLens.AccountLevelProperty", _IResolvable_a771d0ef],
            id: builtins.str,
            is_enabled: typing.Union[builtins.bool, _IResolvable_a771d0ef],
            aws_org: typing.Optional[typing.Union["CfnStorageLens.AwsOrgProperty", _IResolvable_a771d0ef]] = None,
            data_export: typing.Optional[typing.Union["CfnStorageLens.DataExportProperty", _IResolvable_a771d0ef]] = None,
            exclude: typing.Optional[typing.Union["CfnStorageLens.BucketsAndRegionsProperty", _IResolvable_a771d0ef]] = None,
            include: typing.Optional[typing.Union["CfnStorageLens.BucketsAndRegionsProperty", _IResolvable_a771d0ef]] = None,
            storage_lens_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param account_level: ``CfnStorageLens.StorageLensConfigurationProperty.AccountLevel``.
            :param id: ``CfnStorageLens.StorageLensConfigurationProperty.Id``.
            :param is_enabled: ``CfnStorageLens.StorageLensConfigurationProperty.IsEnabled``.
            :param aws_org: ``CfnStorageLens.StorageLensConfigurationProperty.AwsOrg``.
            :param data_export: ``CfnStorageLens.StorageLensConfigurationProperty.DataExport``.
            :param exclude: ``CfnStorageLens.StorageLensConfigurationProperty.Exclude``.
            :param include: ``CfnStorageLens.StorageLensConfigurationProperty.Include``.
            :param storage_lens_arn: ``CfnStorageLens.StorageLensConfigurationProperty.StorageLensArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "account_level": account_level,
                "id": id,
                "is_enabled": is_enabled,
            }
            if aws_org is not None:
                self._values["aws_org"] = aws_org
            if data_export is not None:
                self._values["data_export"] = data_export
            if exclude is not None:
                self._values["exclude"] = exclude
            if include is not None:
                self._values["include"] = include
            if storage_lens_arn is not None:
                self._values["storage_lens_arn"] = storage_lens_arn

        @builtins.property
        def account_level(
            self,
        ) -> typing.Union["CfnStorageLens.AccountLevelProperty", _IResolvable_a771d0ef]:
            '''``CfnStorageLens.StorageLensConfigurationProperty.AccountLevel``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensconfiguration.html#cfn-s3-storagelens-storagelensconfiguration-accountlevel
            '''
            result = self._values.get("account_level")
            assert result is not None, "Required property 'account_level' is missing"
            return typing.cast(typing.Union["CfnStorageLens.AccountLevelProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def id(self) -> builtins.str:
            '''``CfnStorageLens.StorageLensConfigurationProperty.Id``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensconfiguration.html#cfn-s3-storagelens-storagelensconfiguration-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def is_enabled(self) -> typing.Union[builtins.bool, _IResolvable_a771d0ef]:
            '''``CfnStorageLens.StorageLensConfigurationProperty.IsEnabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensconfiguration.html#cfn-s3-storagelens-storagelensconfiguration-isenabled
            '''
            result = self._values.get("is_enabled")
            assert result is not None, "Required property 'is_enabled' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_a771d0ef], result)

        @builtins.property
        def aws_org(
            self,
        ) -> typing.Optional[typing.Union["CfnStorageLens.AwsOrgProperty", _IResolvable_a771d0ef]]:
            '''``CfnStorageLens.StorageLensConfigurationProperty.AwsOrg``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensconfiguration.html#cfn-s3-storagelens-storagelensconfiguration-awsorg
            '''
            result = self._values.get("aws_org")
            return typing.cast(typing.Optional[typing.Union["CfnStorageLens.AwsOrgProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def data_export(
            self,
        ) -> typing.Optional[typing.Union["CfnStorageLens.DataExportProperty", _IResolvable_a771d0ef]]:
            '''``CfnStorageLens.StorageLensConfigurationProperty.DataExport``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensconfiguration.html#cfn-s3-storagelens-storagelensconfiguration-dataexport
            '''
            result = self._values.get("data_export")
            return typing.cast(typing.Optional[typing.Union["CfnStorageLens.DataExportProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def exclude(
            self,
        ) -> typing.Optional[typing.Union["CfnStorageLens.BucketsAndRegionsProperty", _IResolvable_a771d0ef]]:
            '''``CfnStorageLens.StorageLensConfigurationProperty.Exclude``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensconfiguration.html#cfn-s3-storagelens-storagelensconfiguration-exclude
            '''
            result = self._values.get("exclude")
            return typing.cast(typing.Optional[typing.Union["CfnStorageLens.BucketsAndRegionsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def include(
            self,
        ) -> typing.Optional[typing.Union["CfnStorageLens.BucketsAndRegionsProperty", _IResolvable_a771d0ef]]:
            '''``CfnStorageLens.StorageLensConfigurationProperty.Include``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensconfiguration.html#cfn-s3-storagelens-storagelensconfiguration-include
            '''
            result = self._values.get("include")
            return typing.cast(typing.Optional[typing.Union["CfnStorageLens.BucketsAndRegionsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def storage_lens_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnStorageLens.StorageLensConfigurationProperty.StorageLensArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-storagelens-storagelensconfiguration.html#cfn-s3-storagelens-storagelensconfiguration-storagelensarn
            '''
            result = self._values.get("storage_lens_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageLensConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_s3.CfnStorageLensProps",
    jsii_struct_bases=[],
    name_mapping={
        "storage_lens_configuration": "storageLensConfiguration",
        "tags": "tags",
    },
)
class CfnStorageLensProps:
    def __init__(
        self,
        *,
        storage_lens_configuration: typing.Union[CfnStorageLens.StorageLensConfigurationProperty, _IResolvable_a771d0ef],
        tags: typing.Optional[typing.List[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::S3::StorageLens``.

        :param storage_lens_configuration: ``AWS::S3::StorageLens.StorageLensConfiguration``.
        :param tags: ``AWS::S3::StorageLens.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-storagelens.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "storage_lens_configuration": storage_lens_configuration,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def storage_lens_configuration(
        self,
    ) -> typing.Union[CfnStorageLens.StorageLensConfigurationProperty, _IResolvable_a771d0ef]:
        '''``AWS::S3::StorageLens.StorageLensConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-storagelens.html#cfn-s3-storagelens-storagelensconfiguration
        '''
        result = self._values.get("storage_lens_configuration")
        assert result is not None, "Required property 'storage_lens_configuration' is missing"
        return typing.cast(typing.Union[CfnStorageLens.StorageLensConfigurationProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::S3::StorageLens.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-s3-storagelens.html#cfn-s3-storagelens-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStorageLensProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_s3.CorsRule",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_methods": "allowedMethods",
        "allowed_origins": "allowedOrigins",
        "allowed_headers": "allowedHeaders",
        "exposed_headers": "exposedHeaders",
        "id": "id",
        "max_age": "maxAge",
    },
)
class CorsRule:
    def __init__(
        self,
        *,
        allowed_methods: typing.List["HttpMethods"],
        allowed_origins: typing.List[builtins.str],
        allowed_headers: typing.Optional[typing.List[builtins.str]] = None,
        exposed_headers: typing.Optional[typing.List[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        max_age: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Specifies a cross-origin access rule for an Amazon S3 bucket.

        :param allowed_methods: (experimental) An HTTP method that you allow the origin to execute.
        :param allowed_origins: (experimental) One or more origins you want customers to be able to access the bucket from.
        :param allowed_headers: (experimental) Headers that are specified in the Access-Control-Request-Headers header. Default: - No headers allowed.
        :param exposed_headers: (experimental) One or more headers in the response that you want customers to be able to access from their applications. Default: - No headers exposed.
        :param id: (experimental) A unique identifier for this rule. Default: - No id specified.
        :param max_age: (experimental) The time in seconds that your browser is to cache the preflight response for the specified resource. Default: - No caching.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "allowed_methods": allowed_methods,
            "allowed_origins": allowed_origins,
        }
        if allowed_headers is not None:
            self._values["allowed_headers"] = allowed_headers
        if exposed_headers is not None:
            self._values["exposed_headers"] = exposed_headers
        if id is not None:
            self._values["id"] = id
        if max_age is not None:
            self._values["max_age"] = max_age

    @builtins.property
    def allowed_methods(self) -> typing.List["HttpMethods"]:
        '''(experimental) An HTTP method that you allow the origin to execute.

        :stability: experimental
        '''
        result = self._values.get("allowed_methods")
        assert result is not None, "Required property 'allowed_methods' is missing"
        return typing.cast(typing.List["HttpMethods"], result)

    @builtins.property
    def allowed_origins(self) -> typing.List[builtins.str]:
        '''(experimental) One or more origins you want customers to be able to access the bucket from.

        :stability: experimental
        '''
        result = self._values.get("allowed_origins")
        assert result is not None, "Required property 'allowed_origins' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def allowed_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Headers that are specified in the Access-Control-Request-Headers header.

        :default: - No headers allowed.

        :stability: experimental
        '''
        result = self._values.get("allowed_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exposed_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) One or more headers in the response that you want customers to be able to access from their applications.

        :default: - No headers exposed.

        :stability: experimental
        '''
        result = self._values.get("exposed_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''(experimental) A unique identifier for this rule.

        :default: - No id specified.

        :stability: experimental
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_age(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The time in seconds that your browser is to cache the preflight response for the specified resource.

        :default: - No caching.

        :stability: experimental
        '''
        result = self._values.get("max_age")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CorsRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_s3.EventType")
class EventType(enum.Enum):
    '''(experimental) Notification event types.

    :stability: experimental
    '''

    OBJECT_CREATED = "OBJECT_CREATED"
    '''(experimental) Amazon S3 APIs such as PUT, POST, and COPY can create an object.

    Using
    these event types, you can enable notification when an object is created
    using a specific API, or you can use the s3:ObjectCreated:* event type to
    request notification regardless of the API that was used to create an
    object.

    :stability: experimental
    '''
    OBJECT_CREATED_PUT = "OBJECT_CREATED_PUT"
    '''(experimental) Amazon S3 APIs such as PUT, POST, and COPY can create an object.

    Using
    these event types, you can enable notification when an object is created
    using a specific API, or you can use the s3:ObjectCreated:* event type to
    request notification regardless of the API that was used to create an
    object.

    :stability: experimental
    '''
    OBJECT_CREATED_POST = "OBJECT_CREATED_POST"
    '''(experimental) Amazon S3 APIs such as PUT, POST, and COPY can create an object.

    Using
    these event types, you can enable notification when an object is created
    using a specific API, or you can use the s3:ObjectCreated:* event type to
    request notification regardless of the API that was used to create an
    object.

    :stability: experimental
    '''
    OBJECT_CREATED_COPY = "OBJECT_CREATED_COPY"
    '''(experimental) Amazon S3 APIs such as PUT, POST, and COPY can create an object.

    Using
    these event types, you can enable notification when an object is created
    using a specific API, or you can use the s3:ObjectCreated:* event type to
    request notification regardless of the API that was used to create an
    object.

    :stability: experimental
    '''
    OBJECT_CREATED_COMPLETE_MULTIPART_UPLOAD = "OBJECT_CREATED_COMPLETE_MULTIPART_UPLOAD"
    '''(experimental) Amazon S3 APIs such as PUT, POST, and COPY can create an object.

    Using
    these event types, you can enable notification when an object is created
    using a specific API, or you can use the s3:ObjectCreated:* event type to
    request notification regardless of the API that was used to create an
    object.

    :stability: experimental
    '''
    OBJECT_REMOVED = "OBJECT_REMOVED"
    '''(experimental) By using the ObjectRemoved event types, you can enable notification when an object or a batch of objects is removed from a bucket.

    You can request notification when an object is deleted or a versioned
    object is permanently deleted by using the s3:ObjectRemoved:Delete event
    type. Or you can request notification when a delete marker is created for
    a versioned object by using s3:ObjectRemoved:DeleteMarkerCreated. For
    information about deleting versioned objects, see Deleting Object
    Versions. You can also use a wildcard s3:ObjectRemoved:* to request
    notification anytime an object is deleted.

    You will not receive event notifications from automatic deletes from
    lifecycle policies or from failed operations.

    :stability: experimental
    '''
    OBJECT_REMOVED_DELETE = "OBJECT_REMOVED_DELETE"
    '''(experimental) By using the ObjectRemoved event types, you can enable notification when an object or a batch of objects is removed from a bucket.

    You can request notification when an object is deleted or a versioned
    object is permanently deleted by using the s3:ObjectRemoved:Delete event
    type. Or you can request notification when a delete marker is created for
    a versioned object by using s3:ObjectRemoved:DeleteMarkerCreated. For
    information about deleting versioned objects, see Deleting Object
    Versions. You can also use a wildcard s3:ObjectRemoved:* to request
    notification anytime an object is deleted.

    You will not receive event notifications from automatic deletes from
    lifecycle policies or from failed operations.

    :stability: experimental
    '''
    OBJECT_REMOVED_DELETE_MARKER_CREATED = "OBJECT_REMOVED_DELETE_MARKER_CREATED"
    '''(experimental) By using the ObjectRemoved event types, you can enable notification when an object or a batch of objects is removed from a bucket.

    You can request notification when an object is deleted or a versioned
    object is permanently deleted by using the s3:ObjectRemoved:Delete event
    type. Or you can request notification when a delete marker is created for
    a versioned object by using s3:ObjectRemoved:DeleteMarkerCreated. For
    information about deleting versioned objects, see Deleting Object
    Versions. You can also use a wildcard s3:ObjectRemoved:* to request
    notification anytime an object is deleted.

    You will not receive event notifications from automatic deletes from
    lifecycle policies or from failed operations.

    :stability: experimental
    '''
    OBJECT_RESTORE_POST = "OBJECT_RESTORE_POST"
    '''(experimental) Using restore object event types you can receive notifications for initiation and completion when restoring objects from the S3 Glacier storage class.

    You use s3:ObjectRestore:Post to request notification of object restoration
    initiation.

    :stability: experimental
    '''
    OBJECT_RESTORE_COMPLETED = "OBJECT_RESTORE_COMPLETED"
    '''(experimental) Using restore object event types you can receive notifications for initiation and completion when restoring objects from the S3 Glacier storage class.

    You use s3:ObjectRestore:Completed to request notification of
    restoration completion.

    :stability: experimental
    '''
    REDUCED_REDUNDANCY_LOST_OBJECT = "REDUCED_REDUNDANCY_LOST_OBJECT"
    '''(experimental) You can use this event type to request Amazon S3 to send a notification message when Amazon S3 detects that an object of the RRS storage class is lost.

    :stability: experimental
    '''
    REPLICATION_OPERATION_FAILED_REPLICATION = "REPLICATION_OPERATION_FAILED_REPLICATION"
    '''(experimental) You receive this notification event when an object that was eligible for replication using Amazon S3 Replication Time Control failed to replicate.

    :stability: experimental
    '''
    REPLICATION_OPERATION_MISSED_THRESHOLD = "REPLICATION_OPERATION_MISSED_THRESHOLD"
    '''(experimental) You receive this notification event when an object that was eligible for replication using Amazon S3 Replication Time Control exceeded the 15-minute threshold for replication.

    :stability: experimental
    '''
    REPLICATION_OPERATION_REPLICATED_AFTER_THRESHOLD = "REPLICATION_OPERATION_REPLICATED_AFTER_THRESHOLD"
    '''(experimental) You receive this notification event for an object that was eligible for replication using the Amazon S3 Replication Time Control feature replicated after the 15-minute threshold.

    :stability: experimental
    '''
    REPLICATION_OPERATION_NOT_TRACKED = "REPLICATION_OPERATION_NOT_TRACKED"
    '''(experimental) You receive this notification event for an object that was eligible for replication using Amazon S3 Replication Time Control but is no longer tracked by replication metrics.

    :stability: experimental
    '''


@jsii.enum(jsii_type="monocdk.aws_s3.HttpMethods")
class HttpMethods(enum.Enum):
    '''(experimental) All http request methods.

    :stability: experimental
    '''

    GET = "GET"
    '''(experimental) The GET method requests a representation of the specified resource.

    :stability: experimental
    '''
    PUT = "PUT"
    '''(experimental) The PUT method replaces all current representations of the target resource with the request payload.

    :stability: experimental
    '''
    HEAD = "HEAD"
    '''(experimental) The HEAD method asks for a response identical to that of a GET request, but without the response body.

    :stability: experimental
    '''
    POST = "POST"
    '''(experimental) The POST method is used to submit an entity to the specified resource, often causing a change in state or side effects on the server.

    :stability: experimental
    '''
    DELETE = "DELETE"
    '''(experimental) The DELETE method deletes the specified resource.

    :stability: experimental
    '''


@jsii.interface(jsii_type="monocdk.aws_s3.IBucket")
class IBucket(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IBucketProxy"]:
        return _IBucketProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> builtins.str:
        '''(experimental) The ARN of the bucket.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketDomainName")
    def bucket_domain_name(self) -> builtins.str:
        '''(experimental) The IPv4 DNS name of the specified bucket.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketDualStackDomainName")
    def bucket_dual_stack_domain_name(self) -> builtins.str:
        '''(experimental) The IPv6 DNS name of the specified bucket.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        '''(experimental) The name of the bucket.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketRegionalDomainName")
    def bucket_regional_domain_name(self) -> builtins.str:
        '''(experimental) The regional domain name of the specified bucket.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketWebsiteDomainName")
    def bucket_website_domain_name(self) -> builtins.str:
        '''(experimental) The Domain name of the static website.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketWebsiteUrl")
    def bucket_website_url(self) -> builtins.str:
        '''(experimental) The URL of the static website.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) Optional KMS encryption key associated with this bucket.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="isWebsite")
    def is_website(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If this bucket has been configured for static website hosting.

        :stability: experimental
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Optional[BucketPolicy]:
        '''(experimental) The resource policy associated with this bucket.

        If ``autoCreatePolicy`` is true, a ``BucketPolicy`` will be created upon the
        first call to addToResourcePolicy(s).

        :stability: experimental
        '''
        ...

    @policy.setter
    def policy(self, value: typing.Optional[BucketPolicy]) -> None:
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        permission: _PolicyStatement_296fe8a3,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        '''(experimental) Adds a statement to the resource policy for a principal (i.e. account/role/service) to perform actions on this bucket and/or it's contents. Use ``bucketArn`` and ``arnForObjects(keys)`` to obtain ARNs for this bucket or objects.

        :param permission: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="arnForObjects")
    def arn_for_objects(self, key_pattern: builtins.str) -> builtins.str:
        '''(experimental) Returns an ARN that represents all objects within the bucket that match the key pattern specified.

        To represent all keys, specify ``"*"``.

        :param key_pattern: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantDelete")
    def grant_delete(
        self,
        identity: _IGrantable_4c5a91d1,
        objects_key_pattern: typing.Any = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grants s3:DeleteObject* permission to an IAM principal for objects in this bucket.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantPublicAccess")
    def grant_public_access(
        self,
        key_prefix: typing.Optional[builtins.str] = None,
        *allowed_actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Allows unrestricted access to objects from this bucket.

        IMPORTANT: This permission allows anyone to perform actions on S3 objects
        in this bucket, which is useful for when you configure your bucket as a
        website and want everyone to be able to read objects in the bucket without
        needing to authenticate.

        Without arguments, this method will grant read ("s3:GetObject") access to
        all objects ("*") in the bucket.

        The method returns the ``iam.Grant`` object, which can then be modified
        as needed. For example, you can add a condition that will restrict access only
        to an IPv4 range like this::

            const grant = bucket.grantPublicAccess();
            grant.resourceStatement!.addCondition(‘IpAddress’, { “aws:SourceIp”: “54.240.143.0/24” });

        :param key_prefix: the prefix of S3 object keys (e.g. ``home/*``). Default is "*".
        :param allowed_actions: the set of S3 actions to allow. Default is "s3:GetObject".

        :return: The ``iam.PolicyStatement`` object, which can be used to apply e.g. conditions.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantPut")
    def grant_put(
        self,
        identity: _IGrantable_4c5a91d1,
        objects_key_pattern: typing.Any = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grants s3:PutObject* and s3:Abort* permissions for this bucket to an IAM principal.

        If encryption is used, permission to use the key to encrypt the contents
        of written files will also be granted to the same principal.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantPutAcl")
    def grant_put_acl(
        self,
        identity: _IGrantable_4c5a91d1,
        objects_key_pattern: typing.Optional[builtins.str] = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given IAM identity permissions to modify the ACLs of objects in the given Bucket.

        If your application has the '@aws-cdk/aws-s3:grantWriteWithoutAcl' feature flag set,
        calling {@link grantWrite} or {@link grantReadWrite} no longer grants permissions to modify the ACLs of the objects;
        in this case, if you need to modify object ACLs, call this method explicitly.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        identity: _IGrantable_4c5a91d1,
        objects_key_pattern: typing.Any = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for this bucket and it's contents to an IAM principal (Role/Group/User).

        If encryption is used, permission to use the key to decrypt the contents
        of the bucket will also be granted to the same principal.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        identity: _IGrantable_4c5a91d1,
        objects_key_pattern: typing.Any = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grants read/write permissions for this bucket and it's contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to use the key for
        encrypt/decrypt will also be granted.

        Before CDK version 1.85.0, this method granted the ``s3:PutObject*`` permission that included ``s3:PutObjectAcl``,
        which could be used to grant read/write object access to IAM principals in other accounts.
        If you want to get rid of that behavior, update your CDK version to 1.85.0 or later,
        and make sure the ``@aws-cdk/aws-s3:grantWriteWithoutAcl`` feature flag is set to ``true``
        in the ``context`` key of your cdk.json file.
        If you've already updated, but still need the principal to have permissions to modify the ACLs,
        use the {@link grantPutAcl} method.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        identity: _IGrantable_4c5a91d1,
        objects_key_pattern: typing.Any = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions to this bucket to an IAM principal.

        If encryption is used, permission to use the key to encrypt the contents
        of written files will also be granted to the same principal.

        Before CDK version 1.85.0, this method granted the ``s3:PutObject*`` permission that included ``s3:PutObjectAcl``,
        which could be used to grant read/write object access to IAM principals in other accounts.
        If you want to get rid of that behavior, update your CDK version to 1.85.0 or later,
        and make sure the ``@aws-cdk/aws-s3:grantWriteWithoutAcl`` feature flag is set to ``true``
        in the ``context`` key of your cdk.json file.
        If you've already updated, but still need the principal to have permissions to modify the ACLs,
        use the {@link grantPutAcl} method.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(
        self,
        id: builtins.str,
        *,
        paths: typing.Optional[typing.List[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event that triggers when something happens to this bucket.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param paths: (experimental) Only watch changes to these object paths. Default: - Watch changes to all objects
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onCloudTrailPutObject")
    def on_cloud_trail_put_object(
        self,
        id: builtins.str,
        *,
        paths: typing.Optional[typing.List[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines an AWS CloudWatch event that triggers when an object is uploaded to the specified paths (keys) in this bucket using the PutObject API call.

        Note that some tools like ``aws s3 cp`` will automatically use either
        PutObject or the multipart upload API depending on the file size,
        so using ``onCloudTrailWriteObject`` may be preferable.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param paths: (experimental) Only watch changes to these object paths. Default: - Watch changes to all objects
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onCloudTrailWriteObject")
    def on_cloud_trail_write_object(
        self,
        id: builtins.str,
        *,
        paths: typing.Optional[typing.List[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines an AWS CloudWatch event that triggers when an object at the specified paths (keys) in this bucket are written to.

        This includes
        the events PutObject, CopyObject, and CompleteMultipartUpload.

        Note that some tools like ``aws s3 cp`` will automatically use either
        PutObject or the multipart upload API depending on the file size,
        so using this method may be preferable to ``onCloudTrailPutObject``.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param paths: (experimental) Only watch changes to these object paths. Default: - Watch changes to all objects
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="s3UrlForObject")
    def s3_url_for_object(
        self,
        key: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''(experimental) The S3 URL of an S3 object.

        For example:

        :param key: The S3 key of the object. If not specified, the S3 URL of the bucket is returned.

        :return: an ObjectS3Url token

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            s3:
        '''
        ...

    @jsii.member(jsii_name="urlForObject")
    def url_for_object(self, key: typing.Optional[builtins.str] = None) -> builtins.str:
        '''(experimental) The https URL of an S3 object.

        For example:

        :param key: The S3 key of the object. If not specified, the URL of the bucket is returned.

        :return: an ObjectS3Url token

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            https:
        '''
        ...

    @jsii.member(jsii_name="virtualHostedUrlForObject")
    def virtual_hosted_url_for_object(
        self,
        key: typing.Optional[builtins.str] = None,
        *,
        regional: typing.Optional[builtins.bool] = None,
    ) -> builtins.str:
        '''(experimental) The virtual hosted-style URL of an S3 object.

        Specify ``regional: false`` at
        the options for non-regional URL. For example:

        :param key: The S3 key of the object. If not specified, the URL of the bucket is returned.
        :param regional: (experimental) Specifies the URL includes the region. Default: - true

        :return: an ObjectS3Url token

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            https:
        '''
        ...


class _IBucketProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_s3.IBucket"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> builtins.str:
        '''(experimental) The ARN of the bucket.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketDomainName")
    def bucket_domain_name(self) -> builtins.str:
        '''(experimental) The IPv4 DNS name of the specified bucket.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketDomainName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketDualStackDomainName")
    def bucket_dual_stack_domain_name(self) -> builtins.str:
        '''(experimental) The IPv6 DNS name of the specified bucket.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketDualStackDomainName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        '''(experimental) The name of the bucket.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketRegionalDomainName")
    def bucket_regional_domain_name(self) -> builtins.str:
        '''(experimental) The regional domain name of the specified bucket.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketRegionalDomainName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketWebsiteDomainName")
    def bucket_website_domain_name(self) -> builtins.str:
        '''(experimental) The Domain name of the static website.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketWebsiteDomainName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketWebsiteUrl")
    def bucket_website_url(self) -> builtins.str:
        '''(experimental) The URL of the static website.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketWebsiteUrl"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) Optional KMS encryption key associated with this bucket.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IKey_36930160], jsii.get(self, "encryptionKey"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="isWebsite")
    def is_website(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If this bucket has been configured for static website hosting.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "isWebsite"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Optional[BucketPolicy]:
        '''(experimental) The resource policy associated with this bucket.

        If ``autoCreatePolicy`` is true, a ``BucketPolicy`` will be created upon the
        first call to addToResourcePolicy(s).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[BucketPolicy], jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: typing.Optional[BucketPolicy]) -> None:
        jsii.set(self, "policy", value)

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        permission: _PolicyStatement_296fe8a3,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        '''(experimental) Adds a statement to the resource policy for a principal (i.e. account/role/service) to perform actions on this bucket and/or it's contents. Use ``bucketArn`` and ``arnForObjects(keys)`` to obtain ARNs for this bucket or objects.

        :param permission: -

        :stability: experimental
        '''
        return typing.cast(_AddToResourcePolicyResult_0fd9d2a9, jsii.invoke(self, "addToResourcePolicy", [permission]))

    @jsii.member(jsii_name="arnForObjects")
    def arn_for_objects(self, key_pattern: builtins.str) -> builtins.str:
        '''(experimental) Returns an ARN that represents all objects within the bucket that match the key pattern specified.

        To represent all keys, specify ``"*"``.

        :param key_pattern: -

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "arnForObjects", [key_pattern]))

    @jsii.member(jsii_name="grantDelete")
    def grant_delete(
        self,
        identity: _IGrantable_4c5a91d1,
        objects_key_pattern: typing.Any = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grants s3:DeleteObject* permission to an IAM principal for objects in this bucket.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantDelete", [identity, objects_key_pattern]))

    @jsii.member(jsii_name="grantPublicAccess")
    def grant_public_access(
        self,
        key_prefix: typing.Optional[builtins.str] = None,
        *allowed_actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Allows unrestricted access to objects from this bucket.

        IMPORTANT: This permission allows anyone to perform actions on S3 objects
        in this bucket, which is useful for when you configure your bucket as a
        website and want everyone to be able to read objects in the bucket without
        needing to authenticate.

        Without arguments, this method will grant read ("s3:GetObject") access to
        all objects ("*") in the bucket.

        The method returns the ``iam.Grant`` object, which can then be modified
        as needed. For example, you can add a condition that will restrict access only
        to an IPv4 range like this::

            const grant = bucket.grantPublicAccess();
            grant.resourceStatement!.addCondition(‘IpAddress’, { “aws:SourceIp”: “54.240.143.0/24” });

        :param key_prefix: the prefix of S3 object keys (e.g. ``home/*``). Default is "*".
        :param allowed_actions: the set of S3 actions to allow. Default is "s3:GetObject".

        :return: The ``iam.PolicyStatement`` object, which can be used to apply e.g. conditions.

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPublicAccess", [key_prefix, *allowed_actions]))

    @jsii.member(jsii_name="grantPut")
    def grant_put(
        self,
        identity: _IGrantable_4c5a91d1,
        objects_key_pattern: typing.Any = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grants s3:PutObject* and s3:Abort* permissions for this bucket to an IAM principal.

        If encryption is used, permission to use the key to encrypt the contents
        of written files will also be granted to the same principal.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPut", [identity, objects_key_pattern]))

    @jsii.member(jsii_name="grantPutAcl")
    def grant_put_acl(
        self,
        identity: _IGrantable_4c5a91d1,
        objects_key_pattern: typing.Optional[builtins.str] = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given IAM identity permissions to modify the ACLs of objects in the given Bucket.

        If your application has the '@aws-cdk/aws-s3:grantWriteWithoutAcl' feature flag set,
        calling {@link grantWrite} or {@link grantReadWrite} no longer grants permissions to modify the ACLs of the objects;
        in this case, if you need to modify object ACLs, call this method explicitly.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPutAcl", [identity, objects_key_pattern]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        identity: _IGrantable_4c5a91d1,
        objects_key_pattern: typing.Any = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for this bucket and it's contents to an IAM principal (Role/Group/User).

        If encryption is used, permission to use the key to decrypt the contents
        of the bucket will also be granted to the same principal.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantRead", [identity, objects_key_pattern]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        identity: _IGrantable_4c5a91d1,
        objects_key_pattern: typing.Any = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grants read/write permissions for this bucket and it's contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to use the key for
        encrypt/decrypt will also be granted.

        Before CDK version 1.85.0, this method granted the ``s3:PutObject*`` permission that included ``s3:PutObjectAcl``,
        which could be used to grant read/write object access to IAM principals in other accounts.
        If you want to get rid of that behavior, update your CDK version to 1.85.0 or later,
        and make sure the ``@aws-cdk/aws-s3:grantWriteWithoutAcl`` feature flag is set to ``true``
        in the ``context`` key of your cdk.json file.
        If you've already updated, but still need the principal to have permissions to modify the ACLs,
        use the {@link grantPutAcl} method.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantReadWrite", [identity, objects_key_pattern]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        identity: _IGrantable_4c5a91d1,
        objects_key_pattern: typing.Any = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions to this bucket to an IAM principal.

        If encryption is used, permission to use the key to encrypt the contents
        of written files will also be granted to the same principal.

        Before CDK version 1.85.0, this method granted the ``s3:PutObject*`` permission that included ``s3:PutObjectAcl``,
        which could be used to grant read/write object access to IAM principals in other accounts.
        If you want to get rid of that behavior, update your CDK version to 1.85.0 or later,
        and make sure the ``@aws-cdk/aws-s3:grantWriteWithoutAcl`` feature flag is set to ``true``
        in the ``context`` key of your cdk.json file.
        If you've already updated, but still need the principal to have permissions to modify the ACLs,
        use the {@link grantPutAcl} method.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantWrite", [identity, objects_key_pattern]))

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(
        self,
        id: builtins.str,
        *,
        paths: typing.Optional[typing.List[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines a CloudWatch event that triggers when something happens to this bucket.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param paths: (experimental) Only watch changes to these object paths. Default: - Watch changes to all objects
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        options = OnCloudTrailBucketEventOptions(
            paths=paths,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onCloudTrailEvent", [id, options]))

    @jsii.member(jsii_name="onCloudTrailPutObject")
    def on_cloud_trail_put_object(
        self,
        id: builtins.str,
        *,
        paths: typing.Optional[typing.List[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines an AWS CloudWatch event that triggers when an object is uploaded to the specified paths (keys) in this bucket using the PutObject API call.

        Note that some tools like ``aws s3 cp`` will automatically use either
        PutObject or the multipart upload API depending on the file size,
        so using ``onCloudTrailWriteObject`` may be preferable.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param paths: (experimental) Only watch changes to these object paths. Default: - Watch changes to all objects
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        options = OnCloudTrailBucketEventOptions(
            paths=paths,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onCloudTrailPutObject", [id, options]))

    @jsii.member(jsii_name="onCloudTrailWriteObject")
    def on_cloud_trail_write_object(
        self,
        id: builtins.str,
        *,
        paths: typing.Optional[typing.List[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines an AWS CloudWatch event that triggers when an object at the specified paths (keys) in this bucket are written to.

        This includes
        the events PutObject, CopyObject, and CompleteMultipartUpload.

        Note that some tools like ``aws s3 cp`` will automatically use either
        PutObject or the multipart upload API depending on the file size,
        so using this method may be preferable to ``onCloudTrailPutObject``.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param paths: (experimental) Only watch changes to these object paths. Default: - Watch changes to all objects
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        options = OnCloudTrailBucketEventOptions(
            paths=paths,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onCloudTrailWriteObject", [id, options]))

    @jsii.member(jsii_name="s3UrlForObject")
    def s3_url_for_object(
        self,
        key: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''(experimental) The S3 URL of an S3 object.

        For example:

        :param key: The S3 key of the object. If not specified, the S3 URL of the bucket is returned.

        :return: an ObjectS3Url token

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            s3:
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "s3UrlForObject", [key]))

    @jsii.member(jsii_name="urlForObject")
    def url_for_object(self, key: typing.Optional[builtins.str] = None) -> builtins.str:
        '''(experimental) The https URL of an S3 object.

        For example:

        :param key: The S3 key of the object. If not specified, the URL of the bucket is returned.

        :return: an ObjectS3Url token

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            https:
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "urlForObject", [key]))

    @jsii.member(jsii_name="virtualHostedUrlForObject")
    def virtual_hosted_url_for_object(
        self,
        key: typing.Optional[builtins.str] = None,
        *,
        regional: typing.Optional[builtins.bool] = None,
    ) -> builtins.str:
        '''(experimental) The virtual hosted-style URL of an S3 object.

        Specify ``regional: false`` at
        the options for non-regional URL. For example:

        :param key: The S3 key of the object. If not specified, the URL of the bucket is returned.
        :param regional: (experimental) Specifies the URL includes the region. Default: - true

        :return: an ObjectS3Url token

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            https:
        '''
        options = VirtualHostedStyleUrlOptions(regional=regional)

        return typing.cast(builtins.str, jsii.invoke(self, "virtualHostedUrlForObject", [key, options]))


@jsii.interface(jsii_type="monocdk.aws_s3.IBucketNotificationDestination")
class IBucketNotificationDestination(typing_extensions.Protocol):
    '''(experimental) Implemented by constructs that can be used as bucket notification destinations.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IBucketNotificationDestinationProxy"]:
        return _IBucketNotificationDestinationProxy

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_e78e779f,
        bucket: IBucket,
    ) -> BucketNotificationDestinationConfig:
        '''(experimental) Registers this resource to receive notifications for the specified bucket.

        This method will only be called once for each destination/bucket
        pair and the result will be cached, so there is no need to implement
        idempotency in each destination.

        :param scope: -
        :param bucket: The bucket object to bind to.

        :stability: experimental
        '''
        ...


class _IBucketNotificationDestinationProxy:
    '''(experimental) Implemented by constructs that can be used as bucket notification destinations.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_s3.IBucketNotificationDestination"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_e78e779f,
        bucket: IBucket,
    ) -> BucketNotificationDestinationConfig:
        '''(experimental) Registers this resource to receive notifications for the specified bucket.

        This method will only be called once for each destination/bucket
        pair and the result will be cached, so there is no need to implement
        idempotency in each destination.

        :param scope: -
        :param bucket: The bucket object to bind to.

        :stability: experimental
        '''
        return typing.cast(BucketNotificationDestinationConfig, jsii.invoke(self, "bind", [scope, bucket]))


@jsii.data_type(
    jsii_type="monocdk.aws_s3.Inventory",
    jsii_struct_bases=[],
    name_mapping={
        "destination": "destination",
        "enabled": "enabled",
        "format": "format",
        "frequency": "frequency",
        "include_object_versions": "includeObjectVersions",
        "inventory_id": "inventoryId",
        "objects_prefix": "objectsPrefix",
        "optional_fields": "optionalFields",
    },
)
class Inventory:
    def __init__(
        self,
        *,
        destination: "InventoryDestination",
        enabled: typing.Optional[builtins.bool] = None,
        format: typing.Optional["InventoryFormat"] = None,
        frequency: typing.Optional["InventoryFrequency"] = None,
        include_object_versions: typing.Optional["InventoryObjectVersion"] = None,
        inventory_id: typing.Optional[builtins.str] = None,
        objects_prefix: typing.Optional[builtins.str] = None,
        optional_fields: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        '''(experimental) Specifies the inventory configuration of an S3 Bucket.

        :param destination: (experimental) The destination of the inventory.
        :param enabled: (experimental) Whether the inventory is enabled or disabled. Default: true
        :param format: (experimental) The format of the inventory. Default: InventoryFormat.CSV
        :param frequency: (experimental) Frequency at which the inventory should be generated. Default: InventoryFrequency.WEEKLY
        :param include_object_versions: (experimental) If the inventory should contain all the object versions or only the current one. Default: InventoryObjectVersion.ALL
        :param inventory_id: (experimental) The inventory configuration ID. Default: - generated ID.
        :param objects_prefix: (experimental) The inventory will only include objects that meet the prefix filter criteria. Default: - No objects prefix
        :param optional_fields: (experimental) A list of optional fields to be included in the inventory result. Default: - No optional fields.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/storage-inventory.html
        :stability: experimental
        '''
        if isinstance(destination, dict):
            destination = InventoryDestination(**destination)
        self._values: typing.Dict[str, typing.Any] = {
            "destination": destination,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if format is not None:
            self._values["format"] = format
        if frequency is not None:
            self._values["frequency"] = frequency
        if include_object_versions is not None:
            self._values["include_object_versions"] = include_object_versions
        if inventory_id is not None:
            self._values["inventory_id"] = inventory_id
        if objects_prefix is not None:
            self._values["objects_prefix"] = objects_prefix
        if optional_fields is not None:
            self._values["optional_fields"] = optional_fields

    @builtins.property
    def destination(self) -> "InventoryDestination":
        '''(experimental) The destination of the inventory.

        :stability: experimental
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast("InventoryDestination", result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the inventory is enabled or disabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def format(self) -> typing.Optional["InventoryFormat"]:
        '''(experimental) The format of the inventory.

        :default: InventoryFormat.CSV

        :stability: experimental
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional["InventoryFormat"], result)

    @builtins.property
    def frequency(self) -> typing.Optional["InventoryFrequency"]:
        '''(experimental) Frequency at which the inventory should be generated.

        :default: InventoryFrequency.WEEKLY

        :stability: experimental
        '''
        result = self._values.get("frequency")
        return typing.cast(typing.Optional["InventoryFrequency"], result)

    @builtins.property
    def include_object_versions(self) -> typing.Optional["InventoryObjectVersion"]:
        '''(experimental) If the inventory should contain all the object versions or only the current one.

        :default: InventoryObjectVersion.ALL

        :stability: experimental
        '''
        result = self._values.get("include_object_versions")
        return typing.cast(typing.Optional["InventoryObjectVersion"], result)

    @builtins.property
    def inventory_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The inventory configuration ID.

        :default: - generated ID.

        :stability: experimental
        '''
        result = self._values.get("inventory_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def objects_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The inventory will only include objects that meet the prefix filter criteria.

        :default: - No objects prefix

        :stability: experimental
        '''
        result = self._values.get("objects_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def optional_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of optional fields to be included in the inventory result.

        :default: - No optional fields.

        :stability: experimental
        '''
        result = self._values.get("optional_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Inventory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_s3.InventoryDestination",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "bucket_owner": "bucketOwner",
        "prefix": "prefix",
    },
)
class InventoryDestination:
    def __init__(
        self,
        *,
        bucket: IBucket,
        bucket_owner: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The destination of the inventory.

        :param bucket: (experimental) Bucket where all inventories will be saved in.
        :param bucket_owner: (experimental) The account ID that owns the destination S3 bucket. If no account ID is provided, the owner is not validated before exporting data. It's recommended to set an account ID to prevent problems if the destination bucket ownership changes. Default: - No account ID.
        :param prefix: (experimental) The prefix to be used when saving the inventory. Default: - No prefix.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "bucket": bucket,
        }
        if bucket_owner is not None:
            self._values["bucket_owner"] = bucket_owner
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def bucket(self) -> IBucket:
        '''(experimental) Bucket where all inventories will be saved in.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(IBucket, result)

    @builtins.property
    def bucket_owner(self) -> typing.Optional[builtins.str]:
        '''(experimental) The account ID that owns the destination S3 bucket.

        If no account ID is provided, the owner is not validated before exporting data.
        It's recommended to set an account ID to prevent problems if the destination bucket ownership changes.

        :default: - No account ID.

        :stability: experimental
        '''
        result = self._values.get("bucket_owner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The prefix to be used when saving the inventory.

        :default: - No prefix.

        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InventoryDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_s3.InventoryFormat")
class InventoryFormat(enum.Enum):
    '''(experimental) All supported inventory list formats.

    :stability: experimental
    '''

    CSV = "CSV"
    '''(experimental) Generate the inventory list as CSV.

    :stability: experimental
    '''
    PARQUET = "PARQUET"
    '''(experimental) Generate the inventory list as Parquet.

    :stability: experimental
    '''
    ORC = "ORC"
    '''(experimental) Generate the inventory list as Parquet.

    :stability: experimental
    '''


@jsii.enum(jsii_type="monocdk.aws_s3.InventoryFrequency")
class InventoryFrequency(enum.Enum):
    '''(experimental) All supported inventory frequencies.

    :stability: experimental
    '''

    DAILY = "DAILY"
    '''(experimental) A report is generated every day.

    :stability: experimental
    '''
    WEEKLY = "WEEKLY"
    '''(experimental) A report is generated every Sunday (UTC timezone) after the initial report.

    :stability: experimental
    '''


@jsii.enum(jsii_type="monocdk.aws_s3.InventoryObjectVersion")
class InventoryObjectVersion(enum.Enum):
    '''(experimental) Inventory version support.

    :stability: experimental
    '''

    ALL = "ALL"
    '''(experimental) Includes all versions of each object in the report.

    :stability: experimental
    '''
    CURRENT = "CURRENT"
    '''(experimental) Includes only the current version of each object in the report.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_s3.LifecycleRule",
    jsii_struct_bases=[],
    name_mapping={
        "abort_incomplete_multipart_upload_after": "abortIncompleteMultipartUploadAfter",
        "enabled": "enabled",
        "expiration": "expiration",
        "expiration_date": "expirationDate",
        "id": "id",
        "noncurrent_version_expiration": "noncurrentVersionExpiration",
        "noncurrent_version_transitions": "noncurrentVersionTransitions",
        "prefix": "prefix",
        "tag_filters": "tagFilters",
        "transitions": "transitions",
    },
)
class LifecycleRule:
    def __init__(
        self,
        *,
        abort_incomplete_multipart_upload_after: typing.Optional[_Duration_070aa057] = None,
        enabled: typing.Optional[builtins.bool] = None,
        expiration: typing.Optional[_Duration_070aa057] = None,
        expiration_date: typing.Optional[datetime.datetime] = None,
        id: typing.Optional[builtins.str] = None,
        noncurrent_version_expiration: typing.Optional[_Duration_070aa057] = None,
        noncurrent_version_transitions: typing.Optional[typing.List["NoncurrentVersionTransition"]] = None,
        prefix: typing.Optional[builtins.str] = None,
        tag_filters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        transitions: typing.Optional[typing.List["Transition"]] = None,
    ) -> None:
        '''(experimental) Declaration of a Life cycle rule.

        :param abort_incomplete_multipart_upload_after: (experimental) Specifies a lifecycle rule that aborts incomplete multipart uploads to an Amazon S3 bucket. The AbortIncompleteMultipartUpload property type creates a lifecycle rule that aborts incomplete multipart uploads to an Amazon S3 bucket. When Amazon S3 aborts a multipart upload, it deletes all parts associated with the multipart upload. Default: Incomplete uploads are never aborted
        :param enabled: (experimental) Whether this rule is enabled. Default: true
        :param expiration: (experimental) Indicates the number of days after creation when objects are deleted from Amazon S3 and Amazon Glacier. If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time. Default: No expiration timeout
        :param expiration_date: (experimental) Indicates when objects are deleted from Amazon S3 and Amazon Glacier. The date value must be in ISO 8601 format. The time is always midnight UTC. If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time. Default: No expiration date
        :param id: (experimental) A unique identifier for this rule. The value cannot be more than 255 characters.
        :param noncurrent_version_expiration: (experimental) Time between when a new version of the object is uploaded to the bucket and when old versions of the object expire. For buckets with versioning enabled (or suspended), specifies the time, in days, between when a new version of the object is uploaded to the bucket and when old versions of the object expire. When object versions expire, Amazon S3 permanently deletes them. If you specify a transition and expiration time, the expiration time must be later than the transition time. Default: No noncurrent version expiration
        :param noncurrent_version_transitions: (experimental) One or more transition rules that specify when non-current objects transition to a specified storage class. Only for for buckets with versioning enabled (or suspended). If you specify a transition and expiration time, the expiration time must be later than the transition time.
        :param prefix: (experimental) Object key prefix that identifies one or more objects to which this rule applies. Default: Rule applies to all objects
        :param tag_filters: (experimental) The TagFilter property type specifies tags to use to identify a subset of objects for an Amazon S3 bucket. Default: Rule applies to all objects
        :param transitions: (experimental) One or more transition rules that specify when an object transitions to a specified storage class. If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time. Default: No transition rules

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if abort_incomplete_multipart_upload_after is not None:
            self._values["abort_incomplete_multipart_upload_after"] = abort_incomplete_multipart_upload_after
        if enabled is not None:
            self._values["enabled"] = enabled
        if expiration is not None:
            self._values["expiration"] = expiration
        if expiration_date is not None:
            self._values["expiration_date"] = expiration_date
        if id is not None:
            self._values["id"] = id
        if noncurrent_version_expiration is not None:
            self._values["noncurrent_version_expiration"] = noncurrent_version_expiration
        if noncurrent_version_transitions is not None:
            self._values["noncurrent_version_transitions"] = noncurrent_version_transitions
        if prefix is not None:
            self._values["prefix"] = prefix
        if tag_filters is not None:
            self._values["tag_filters"] = tag_filters
        if transitions is not None:
            self._values["transitions"] = transitions

    @builtins.property
    def abort_incomplete_multipart_upload_after(
        self,
    ) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Specifies a lifecycle rule that aborts incomplete multipart uploads to an Amazon S3 bucket.

        The AbortIncompleteMultipartUpload property type creates a lifecycle
        rule that aborts incomplete multipart uploads to an Amazon S3 bucket.
        When Amazon S3 aborts a multipart upload, it deletes all parts
        associated with the multipart upload.

        :default: Incomplete uploads are never aborted

        :stability: experimental
        '''
        result = self._values.get("abort_incomplete_multipart_upload_after")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether this rule is enabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def expiration(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Indicates the number of days after creation when objects are deleted from Amazon S3 and Amazon Glacier.

        If you specify an expiration and transition time, you must use the same
        time unit for both properties (either in days or by date). The
        expiration time must also be later than the transition time.

        :default: No expiration timeout

        :stability: experimental
        '''
        result = self._values.get("expiration")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def expiration_date(self) -> typing.Optional[datetime.datetime]:
        '''(experimental) Indicates when objects are deleted from Amazon S3 and Amazon Glacier.

        The date value must be in ISO 8601 format. The time is always midnight UTC.

        If you specify an expiration and transition time, you must use the same
        time unit for both properties (either in days or by date). The
        expiration time must also be later than the transition time.

        :default: No expiration date

        :stability: experimental
        '''
        result = self._values.get("expiration_date")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''(experimental) A unique identifier for this rule.

        The value cannot be more than 255 characters.

        :stability: experimental
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def noncurrent_version_expiration(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Time between when a new version of the object is uploaded to the bucket and when old versions of the object expire.

        For buckets with versioning enabled (or suspended), specifies the time,
        in days, between when a new version of the object is uploaded to the
        bucket and when old versions of the object expire. When object versions
        expire, Amazon S3 permanently deletes them. If you specify a transition
        and expiration time, the expiration time must be later than the
        transition time.

        :default: No noncurrent version expiration

        :stability: experimental
        '''
        result = self._values.get("noncurrent_version_expiration")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def noncurrent_version_transitions(
        self,
    ) -> typing.Optional[typing.List["NoncurrentVersionTransition"]]:
        '''(experimental) One or more transition rules that specify when non-current objects transition to a specified storage class.

        Only for for buckets with versioning enabled (or suspended).

        If you specify a transition and expiration time, the expiration time
        must be later than the transition time.

        :stability: experimental
        '''
        result = self._values.get("noncurrent_version_transitions")
        return typing.cast(typing.Optional[typing.List["NoncurrentVersionTransition"]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Object key prefix that identifies one or more objects to which this rule applies.

        :default: Rule applies to all objects

        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_filters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) The TagFilter property type specifies tags to use to identify a subset of objects for an Amazon S3 bucket.

        :default: Rule applies to all objects

        :stability: experimental
        '''
        result = self._values.get("tag_filters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def transitions(self) -> typing.Optional[typing.List["Transition"]]:
        '''(experimental) One or more transition rules that specify when an object transitions to a specified storage class.

        If you specify an expiration and transition time, you must use the same
        time unit for both properties (either in days or by date). The
        expiration time must also be later than the transition time.

        :default: No transition rules

        :stability: experimental
        '''
        result = self._values.get("transitions")
        return typing.cast(typing.Optional[typing.List["Transition"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LifecycleRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_s3.Location",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "object_key": "objectKey",
        "object_version": "objectVersion",
    },
)
class Location:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        object_key: builtins.str,
        object_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) An interface that represents the location of a specific object in an S3 Bucket.

        :param bucket_name: (experimental) The name of the S3 Bucket the object is in.
        :param object_key: (experimental) The path inside the Bucket where the object is located at.
        :param object_version: (experimental) The S3 object version.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "bucket_name": bucket_name,
            "object_key": object_key,
        }
        if object_version is not None:
            self._values["object_version"] = object_version

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''(experimental) The name of the S3 Bucket the object is in.

        :stability: experimental
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object_key(self) -> builtins.str:
        '''(experimental) The path inside the Bucket where the object is located at.

        :stability: experimental
        '''
        result = self._values.get("object_key")
        assert result is not None, "Required property 'object_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The S3 object version.

        :stability: experimental
        '''
        result = self._values.get("object_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Location(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_s3.NoncurrentVersionTransition",
    jsii_struct_bases=[],
    name_mapping={
        "storage_class": "storageClass",
        "transition_after": "transitionAfter",
    },
)
class NoncurrentVersionTransition:
    def __init__(
        self,
        *,
        storage_class: "StorageClass",
        transition_after: _Duration_070aa057,
    ) -> None:
        '''(experimental) Describes when noncurrent versions transition to a specified storage class.

        :param storage_class: (experimental) The storage class to which you want the object to transition.
        :param transition_after: (experimental) Indicates the number of days after creation when objects are transitioned to the specified storage class. Default: No transition count.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "storage_class": storage_class,
            "transition_after": transition_after,
        }

    @builtins.property
    def storage_class(self) -> "StorageClass":
        '''(experimental) The storage class to which you want the object to transition.

        :stability: experimental
        '''
        result = self._values.get("storage_class")
        assert result is not None, "Required property 'storage_class' is missing"
        return typing.cast("StorageClass", result)

    @builtins.property
    def transition_after(self) -> _Duration_070aa057:
        '''(experimental) Indicates the number of days after creation when objects are transitioned to the specified storage class.

        :default: No transition count.

        :stability: experimental
        '''
        result = self._values.get("transition_after")
        assert result is not None, "Required property 'transition_after' is missing"
        return typing.cast(_Duration_070aa057, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NoncurrentVersionTransition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_s3.NotificationKeyFilter",
    jsii_struct_bases=[],
    name_mapping={"prefix": "prefix", "suffix": "suffix"},
)
class NotificationKeyFilter:
    def __init__(
        self,
        *,
        prefix: typing.Optional[builtins.str] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param prefix: (experimental) S3 keys must have the specified prefix.
        :param suffix: (experimental) S3 keys must have the specified suffix.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if prefix is not None:
            self._values["prefix"] = prefix
        if suffix is not None:
            self._values["suffix"] = suffix

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) S3 keys must have the specified prefix.

        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        '''(experimental) S3 keys must have the specified suffix.

        :stability: experimental
        '''
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotificationKeyFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_s3.ObjectOwnership")
class ObjectOwnership(enum.Enum):
    '''(experimental) The ObjectOwnership of the bucket.

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/about-object-ownership.html
    :stability: experimental
    '''

    BUCKET_OWNER_PREFERRED = "BUCKET_OWNER_PREFERRED"
    '''(experimental) Objects uploaded to the bucket change ownership to the bucket owner .

    :stability: experimental
    '''
    OBJECT_WRITER = "OBJECT_WRITER"
    '''(experimental) The uploading account will own the object.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_s3.OnCloudTrailBucketEventOptions",
    jsii_struct_bases=[_OnEventOptions_d5081088],
    name_mapping={
        "description": "description",
        "event_pattern": "eventPattern",
        "rule_name": "ruleName",
        "target": "target",
        "paths": "paths",
    },
)
class OnCloudTrailBucketEventOptions(_OnEventOptions_d5081088):
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
        paths: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for the onCloudTrailPutObject method.

        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param paths: (experimental) Only watch changes to these object paths. Default: - Watch changes to all objects

        :stability: experimental
        '''
        if isinstance(event_pattern, dict):
            event_pattern = _EventPattern_a23fbf37(**event_pattern)
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if event_pattern is not None:
            self._values["event_pattern"] = event_pattern
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if target is not None:
            self._values["target"] = target
        if paths is not None:
            self._values["paths"] = paths

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the rule's purpose.

        :default: - No description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_pattern(self) -> typing.Optional[_EventPattern_a23fbf37]:
        '''(experimental) Additional restrictions for the event to route to the specified target.

        The method that generates the rule probably imposes some type of event
        filtering. The filtering implied by what you pass here is added
        on top of that filtering.

        :default: - No additional filtering based on an event pattern.

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-and-event-patterns.html
        :stability: experimental
        '''
        result = self._values.get("event_pattern")
        return typing.cast(typing.Optional[_EventPattern_a23fbf37], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the rule.

        :default: AWS CloudFormation generates a unique physical ID.

        :stability: experimental
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[_IRuleTarget_d45ec729]:
        '''(experimental) The target to register for the event.

        :default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[_IRuleTarget_d45ec729], result)

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Only watch changes to these object paths.

        :default: - Watch changes to all objects

        :stability: experimental
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnCloudTrailBucketEventOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_s3.RedirectProtocol")
class RedirectProtocol(enum.Enum):
    '''(experimental) All http request methods.

    :stability: experimental
    '''

    HTTP = "HTTP"
    '''
    :stability: experimental
    '''
    HTTPS = "HTTPS"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_s3.RedirectTarget",
    jsii_struct_bases=[],
    name_mapping={"host_name": "hostName", "protocol": "protocol"},
)
class RedirectTarget:
    def __init__(
        self,
        *,
        host_name: builtins.str,
        protocol: typing.Optional[RedirectProtocol] = None,
    ) -> None:
        '''(experimental) Specifies a redirect behavior of all requests to a website endpoint of a bucket.

        :param host_name: (experimental) Name of the host where requests are redirected.
        :param protocol: (experimental) Protocol to use when redirecting requests. Default: - The protocol used in the original request.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "host_name": host_name,
        }
        if protocol is not None:
            self._values["protocol"] = protocol

    @builtins.property
    def host_name(self) -> builtins.str:
        '''(experimental) Name of the host where requests are redirected.

        :stability: experimental
        '''
        result = self._values.get("host_name")
        assert result is not None, "Required property 'host_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> typing.Optional[RedirectProtocol]:
        '''(experimental) Protocol to use when redirecting requests.

        :default: - The protocol used in the original request.

        :stability: experimental
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[RedirectProtocol], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedirectTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReplaceKey(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_s3.ReplaceKey"):
    '''
    :stability: experimental
    '''

    @jsii.member(jsii_name="prefixWith") # type: ignore[misc]
    @builtins.classmethod
    def prefix_with(cls, key_replacement: builtins.str) -> "ReplaceKey":
        '''(experimental) The object key prefix to use in the redirect request.

        :param key_replacement: -

        :stability: experimental
        '''
        return typing.cast("ReplaceKey", jsii.sinvoke(cls, "prefixWith", [key_replacement]))

    @jsii.member(jsii_name="with") # type: ignore[misc]
    @builtins.classmethod
    def with_(cls, key_replacement: builtins.str) -> "ReplaceKey":
        '''(experimental) The specific object key to use in the redirect request.

        :param key_replacement: -

        :stability: experimental
        '''
        return typing.cast("ReplaceKey", jsii.sinvoke(cls, "with", [key_replacement]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="prefixWithKey")
    def prefix_with_key(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixWithKey"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="withKey")
    def with_key(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "withKey"))


@jsii.data_type(
    jsii_type="monocdk.aws_s3.RoutingRule",
    jsii_struct_bases=[],
    name_mapping={
        "condition": "condition",
        "host_name": "hostName",
        "http_redirect_code": "httpRedirectCode",
        "protocol": "protocol",
        "replace_key": "replaceKey",
    },
)
class RoutingRule:
    def __init__(
        self,
        *,
        condition: typing.Optional["RoutingRuleCondition"] = None,
        host_name: typing.Optional[builtins.str] = None,
        http_redirect_code: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[RedirectProtocol] = None,
        replace_key: typing.Optional[ReplaceKey] = None,
    ) -> None:
        '''(experimental) Rule that define when a redirect is applied and the redirect behavior.

        :param condition: (experimental) Specifies a condition that must be met for the specified redirect to apply. Default: - No condition
        :param host_name: (experimental) The host name to use in the redirect request. Default: - The host name used in the original request.
        :param http_redirect_code: (experimental) The HTTP redirect code to use on the response. Default: "301" - Moved Permanently
        :param protocol: (experimental) Protocol to use when redirecting requests. Default: - The protocol used in the original request.
        :param replace_key: (experimental) Specifies the object key prefix to use in the redirect request. Default: - The key will not be replaced

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/how-to-page-redirect.html
        :stability: experimental
        '''
        if isinstance(condition, dict):
            condition = RoutingRuleCondition(**condition)
        self._values: typing.Dict[str, typing.Any] = {}
        if condition is not None:
            self._values["condition"] = condition
        if host_name is not None:
            self._values["host_name"] = host_name
        if http_redirect_code is not None:
            self._values["http_redirect_code"] = http_redirect_code
        if protocol is not None:
            self._values["protocol"] = protocol
        if replace_key is not None:
            self._values["replace_key"] = replace_key

    @builtins.property
    def condition(self) -> typing.Optional["RoutingRuleCondition"]:
        '''(experimental) Specifies a condition that must be met for the specified redirect to apply.

        :default: - No condition

        :stability: experimental
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional["RoutingRuleCondition"], result)

    @builtins.property
    def host_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The host name to use in the redirect request.

        :default: - The host name used in the original request.

        :stability: experimental
        '''
        result = self._values.get("host_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http_redirect_code(self) -> typing.Optional[builtins.str]:
        '''(experimental) The HTTP redirect code to use on the response.

        :default: "301" - Moved Permanently

        :stability: experimental
        '''
        result = self._values.get("http_redirect_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[RedirectProtocol]:
        '''(experimental) Protocol to use when redirecting requests.

        :default: - The protocol used in the original request.

        :stability: experimental
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[RedirectProtocol], result)

    @builtins.property
    def replace_key(self) -> typing.Optional[ReplaceKey]:
        '''(experimental) Specifies the object key prefix to use in the redirect request.

        :default: - The key will not be replaced

        :stability: experimental
        '''
        result = self._values.get("replace_key")
        return typing.cast(typing.Optional[ReplaceKey], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoutingRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_s3.RoutingRuleCondition",
    jsii_struct_bases=[],
    name_mapping={
        "http_error_code_returned_equals": "httpErrorCodeReturnedEquals",
        "key_prefix_equals": "keyPrefixEquals",
    },
)
class RoutingRuleCondition:
    def __init__(
        self,
        *,
        http_error_code_returned_equals: typing.Optional[builtins.str] = None,
        key_prefix_equals: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param http_error_code_returned_equals: (experimental) The HTTP error code when the redirect is applied. In the event of an error, if the error code equals this value, then the specified redirect is applied. If both condition properties are specified, both must be true for the redirect to be applied. Default: - The HTTP error code will not be verified
        :param key_prefix_equals: (experimental) The object key name prefix when the redirect is applied. If both condition properties are specified, both must be true for the redirect to be applied. Default: - The object key name will not be verified

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if http_error_code_returned_equals is not None:
            self._values["http_error_code_returned_equals"] = http_error_code_returned_equals
        if key_prefix_equals is not None:
            self._values["key_prefix_equals"] = key_prefix_equals

    @builtins.property
    def http_error_code_returned_equals(self) -> typing.Optional[builtins.str]:
        '''(experimental) The HTTP error code when the redirect is applied.

        In the event of an error, if the error code equals this value, then the specified redirect is applied.

        If both condition properties are specified, both must be true for the redirect to be applied.

        :default: - The HTTP error code will not be verified

        :stability: experimental
        '''
        result = self._values.get("http_error_code_returned_equals")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_prefix_equals(self) -> typing.Optional[builtins.str]:
        '''(experimental) The object key name prefix when the redirect is applied.

        If both condition properties are specified, both must be true for the redirect to be applied.

        :default: - The object key name will not be verified

        :stability: experimental
        '''
        result = self._values.get("key_prefix_equals")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoutingRuleCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageClass(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_s3.StorageClass"):
    '''(experimental) Storage class to move an object to.

    :stability: experimental
    '''

    def __init__(self, value: builtins.str) -> None:
        '''
        :param value: -

        :stability: experimental
        '''
        jsii.create(StorageClass, self, [value])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="DEEP_ARCHIVE")
    def DEEP_ARCHIVE(cls) -> "StorageClass":
        '''(experimental) Use for archiving data that rarely needs to be accessed.

        Data stored in the
        DEEP_ARCHIVE storage class has a minimum storage duration period of 180
        days and a default retrieval time of 12 hours. If you delete an object
        before the 180-day minimum, you are charged for 180 days. For pricing
        information, see Amazon S3 Pricing.

        :stability: experimental
        '''
        return typing.cast("StorageClass", jsii.sget(cls, "DEEP_ARCHIVE"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="GLACIER")
    def GLACIER(cls) -> "StorageClass":
        '''(experimental) Storage class for long-term archival that can take between minutes and hours to access.

        Use for archives where portions of the data might need to be retrieved in
        minutes. Data stored in the GLACIER storage class has a minimum storage
        duration period of 90 days and can be accessed in as little as 1-5 minutes
        using expedited retrieval. If you delete an object before the 90-day
        minimum, you are charged for 90 days.

        :stability: experimental
        '''
        return typing.cast("StorageClass", jsii.sget(cls, "GLACIER"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="INFREQUENT_ACCESS")
    def INFREQUENT_ACCESS(cls) -> "StorageClass":
        '''(experimental) Storage class for data that is accessed less frequently, but requires rapid access when needed.

        Has lower availability than Standard storage.

        :stability: experimental
        '''
        return typing.cast("StorageClass", jsii.sget(cls, "INFREQUENT_ACCESS"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="INTELLIGENT_TIERING")
    def INTELLIGENT_TIERING(cls) -> "StorageClass":
        '''(experimental) The INTELLIGENT_TIERING storage class is designed to optimize storage costs by automatically moving data to the most cost-effective storage access tier, without performance impact or operational overhead.

        INTELLIGENT_TIERING delivers automatic cost savings by moving data on a
        granular object level between two access tiers, a frequent access tier and
        a lower-cost infrequent access tier, when access patterns change. The
        INTELLIGENT_TIERING storage class is ideal if you want to optimize storage
        costs automatically for long-lived data when access patterns are unknown or
        unpredictable.

        :stability: experimental
        '''
        return typing.cast("StorageClass", jsii.sget(cls, "INTELLIGENT_TIERING"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="ONE_ZONE_INFREQUENT_ACCESS")
    def ONE_ZONE_INFREQUENT_ACCESS(cls) -> "StorageClass":
        '''(experimental) Infrequent Access that's only stored in one availability zone.

        Has lower availability than standard InfrequentAccess.

        :stability: experimental
        '''
        return typing.cast("StorageClass", jsii.sget(cls, "ONE_ZONE_INFREQUENT_ACCESS"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "value"))


@jsii.data_type(
    jsii_type="monocdk.aws_s3.Transition",
    jsii_struct_bases=[],
    name_mapping={
        "storage_class": "storageClass",
        "transition_after": "transitionAfter",
        "transition_date": "transitionDate",
    },
)
class Transition:
    def __init__(
        self,
        *,
        storage_class: StorageClass,
        transition_after: typing.Optional[_Duration_070aa057] = None,
        transition_date: typing.Optional[datetime.datetime] = None,
    ) -> None:
        '''(experimental) Describes when an object transitions to a specified storage class.

        :param storage_class: (experimental) The storage class to which you want the object to transition.
        :param transition_after: (experimental) Indicates the number of days after creation when objects are transitioned to the specified storage class. Default: No transition count.
        :param transition_date: (experimental) Indicates when objects are transitioned to the specified storage class. The date value must be in ISO 8601 format. The time is always midnight UTC. Default: No transition date.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "storage_class": storage_class,
        }
        if transition_after is not None:
            self._values["transition_after"] = transition_after
        if transition_date is not None:
            self._values["transition_date"] = transition_date

    @builtins.property
    def storage_class(self) -> StorageClass:
        '''(experimental) The storage class to which you want the object to transition.

        :stability: experimental
        '''
        result = self._values.get("storage_class")
        assert result is not None, "Required property 'storage_class' is missing"
        return typing.cast(StorageClass, result)

    @builtins.property
    def transition_after(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Indicates the number of days after creation when objects are transitioned to the specified storage class.

        :default: No transition count.

        :stability: experimental
        '''
        result = self._values.get("transition_after")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def transition_date(self) -> typing.Optional[datetime.datetime]:
        '''(experimental) Indicates when objects are transitioned to the specified storage class.

        The date value must be in ISO 8601 format. The time is always midnight UTC.

        :default: No transition date.

        :stability: experimental
        '''
        result = self._values.get("transition_date")
        return typing.cast(typing.Optional[datetime.datetime], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Transition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_s3.VirtualHostedStyleUrlOptions",
    jsii_struct_bases=[],
    name_mapping={"regional": "regional"},
)
class VirtualHostedStyleUrlOptions:
    def __init__(self, *, regional: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Options for creating Virtual-Hosted style URL.

        :param regional: (experimental) Specifies the URL includes the region. Default: - true

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if regional is not None:
            self._values["regional"] = regional

    @builtins.property
    def regional(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies the URL includes the region.

        :default: - true

        :stability: experimental
        '''
        result = self._values.get("regional")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualHostedStyleUrlOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IBucket)
class Bucket(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_s3.Bucket",
):
    '''(experimental) An S3 bucket with associated policy objects.

    This bucket does not yet have all features that exposed by the underlying
    BucketResource.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        access_control: typing.Optional[BucketAccessControl] = None,
        auto_delete_objects: typing.Optional[builtins.bool] = None,
        block_public_access: typing.Optional[BlockPublicAccess] = None,
        bucket_key_enabled: typing.Optional[builtins.bool] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        cors: typing.Optional[typing.List[CorsRule]] = None,
        encryption: typing.Optional[BucketEncryption] = None,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        enforce_ssl: typing.Optional[builtins.bool] = None,
        inventories: typing.Optional[typing.List[Inventory]] = None,
        lifecycle_rules: typing.Optional[typing.List[LifecycleRule]] = None,
        metrics: typing.Optional[typing.List[BucketMetrics]] = None,
        object_ownership: typing.Optional[ObjectOwnership] = None,
        public_read_access: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        server_access_logs_bucket: typing.Optional[IBucket] = None,
        server_access_logs_prefix: typing.Optional[builtins.str] = None,
        versioned: typing.Optional[builtins.bool] = None,
        website_error_document: typing.Optional[builtins.str] = None,
        website_index_document: typing.Optional[builtins.str] = None,
        website_redirect: typing.Optional[RedirectTarget] = None,
        website_routing_rules: typing.Optional[typing.List[RoutingRule]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param access_control: (experimental) Specifies a canned ACL that grants predefined permissions to the bucket. Default: BucketAccessControl.PRIVATE
        :param auto_delete_objects: (experimental) Whether all objects should be automatically deleted when the bucket is removed from the stack or when the stack is deleted. Requires the ``removalPolicy`` to be set to ``RemovalPolicy.DESTROY``. Default: false
        :param block_public_access: (experimental) The block public access configuration of this bucket. Default: - CloudFormation defaults will apply. New buckets and objects don't allow public access, but users can modify bucket policies or object permissions to allow public access
        :param bucket_key_enabled: (experimental) Specifies whether Amazon S3 should use an S3 Bucket Key with server-side encryption using KMS (SSE-KMS) for new objects in the bucket. Only relevant, when Encryption is set to {@link BucketEncryption.KMS} Default: - false
        :param bucket_name: (experimental) Physical name of this bucket. Default: - Assigned by CloudFormation (recommended).
        :param cors: (experimental) The CORS configuration of this bucket. Default: - No CORS configuration.
        :param encryption: (experimental) The kind of server-side encryption to apply to this bucket. If you choose KMS, you can specify a KMS key via ``encryptionKey``. If encryption key is not specified, a key will automatically be created. Default: - ``Kms`` if ``encryptionKey`` is specified, or ``Unencrypted`` otherwise.
        :param encryption_key: (experimental) External KMS key to use for bucket encryption. The 'encryption' property must be either not specified or set to "Kms". An error will be emitted if encryption is set to "Unencrypted" or "Managed". Default: - If encryption is set to "Kms" and this property is undefined, a new KMS key will be created and associated with this bucket.
        :param enforce_ssl: (experimental) Enforces SSL for requests. S3.5 of the AWS Foundational Security Best Practices Regarding S3. Default: false
        :param inventories: (experimental) The inventory configuration of the bucket. Default: - No inventory configuration
        :param lifecycle_rules: (experimental) Rules that define how Amazon S3 manages objects during their lifetime. Default: - No lifecycle rules.
        :param metrics: (experimental) The metrics configuration of this bucket. Default: - No metrics configuration.
        :param object_ownership: (experimental) The objectOwnership of the bucket. Default: - No ObjectOwnership configuration, uploading account will own the object.
        :param public_read_access: (experimental) Grants public read access to all objects in the bucket. Similar to calling ``bucket.grantPublicAccess()`` Default: false
        :param removal_policy: (experimental) Policy to apply when the bucket is removed from this stack. Default: - The bucket will be orphaned.
        :param server_access_logs_bucket: (experimental) Destination bucket for the server access logs. Default: - If "serverAccessLogsPrefix" undefined - access logs disabled, otherwise - log to current bucket.
        :param server_access_logs_prefix: (experimental) Optional log file prefix to use for the bucket's access logs. If defined without "serverAccessLogsBucket", enables access logs to current bucket with this prefix. Default: - No log file prefix
        :param versioned: (experimental) Whether this bucket should have versioning turned on or not. Default: false
        :param website_error_document: (experimental) The name of the error document (e.g. "404.html") for the website. ``websiteIndexDocument`` must also be set if this is set. Default: - No error document.
        :param website_index_document: (experimental) The name of the index document (e.g. "index.html") for the website. Enables static website hosting for this bucket. Default: - No index document.
        :param website_redirect: (experimental) Specifies the redirect behavior of all requests to a website endpoint of a bucket. If you specify this property, you can't specify "websiteIndexDocument", "websiteErrorDocument" nor , "websiteRoutingRules". Default: - No redirection.
        :param website_routing_rules: (experimental) Rules that define when a redirect is applied and the redirect behavior. Default: - No redirection rules.

        :stability: experimental
        '''
        props = BucketProps(
            access_control=access_control,
            auto_delete_objects=auto_delete_objects,
            block_public_access=block_public_access,
            bucket_key_enabled=bucket_key_enabled,
            bucket_name=bucket_name,
            cors=cors,
            encryption=encryption,
            encryption_key=encryption_key,
            enforce_ssl=enforce_ssl,
            inventories=inventories,
            lifecycle_rules=lifecycle_rules,
            metrics=metrics,
            object_ownership=object_ownership,
            public_read_access=public_read_access,
            removal_policy=removal_policy,
            server_access_logs_bucket=server_access_logs_bucket,
            server_access_logs_prefix=server_access_logs_prefix,
            versioned=versioned,
            website_error_document=website_error_document,
            website_index_document=website_index_document,
            website_redirect=website_redirect,
            website_routing_rules=website_routing_rules,
        )

        jsii.create(Bucket, self, [scope, id, props])

    @jsii.member(jsii_name="fromBucketArn") # type: ignore[misc]
    @builtins.classmethod
    def from_bucket_arn(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        bucket_arn: builtins.str,
    ) -> IBucket:
        '''
        :param scope: -
        :param id: -
        :param bucket_arn: -

        :stability: experimental
        '''
        return typing.cast(IBucket, jsii.sinvoke(cls, "fromBucketArn", [scope, id, bucket_arn]))

    @jsii.member(jsii_name="fromBucketAttributes") # type: ignore[misc]
    @builtins.classmethod
    def from_bucket_attributes(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        bucket_arn: typing.Optional[builtins.str] = None,
        bucket_domain_name: typing.Optional[builtins.str] = None,
        bucket_dual_stack_domain_name: typing.Optional[builtins.str] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        bucket_regional_domain_name: typing.Optional[builtins.str] = None,
        bucket_website_new_url_format: typing.Optional[builtins.bool] = None,
        bucket_website_url: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        is_website: typing.Optional[builtins.bool] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> IBucket:
        '''(experimental) Creates a Bucket construct that represents an external bucket.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param account: (experimental) The account this existing bucket belongs to. Default: - it's assumed the bucket belongs to the same account as the scope it's being imported into
        :param bucket_arn: (experimental) The ARN of the bucket. At least one of bucketArn or bucketName must be defined in order to initialize a bucket ref.
        :param bucket_domain_name: (experimental) The domain name of the bucket. Default: Inferred from bucket name
        :param bucket_dual_stack_domain_name: (experimental) The IPv6 DNS name of the specified bucket.
        :param bucket_name: (experimental) The name of the bucket. If the underlying value of ARN is a string, the name will be parsed from the ARN. Otherwise, the name is optional, but some features that require the bucket name such as auto-creating a bucket policy, won't work.
        :param bucket_regional_domain_name: (experimental) The regional domain name of the specified bucket.
        :param bucket_website_new_url_format: (experimental) The format of the website URL of the bucket. This should be true for regions launched since 2014. Default: false
        :param bucket_website_url: (experimental) The website URL of the bucket (if static web hosting is enabled). Default: Inferred from bucket name
        :param encryption_key: 
        :param is_website: (experimental) If this bucket has been configured for static website hosting. Default: false
        :param region: (experimental) The region this existing bucket is in. Default: - it's assumed the bucket is in the same region as the scope it's being imported into

        :stability: experimental
        '''
        attrs = BucketAttributes(
            account=account,
            bucket_arn=bucket_arn,
            bucket_domain_name=bucket_domain_name,
            bucket_dual_stack_domain_name=bucket_dual_stack_domain_name,
            bucket_name=bucket_name,
            bucket_regional_domain_name=bucket_regional_domain_name,
            bucket_website_new_url_format=bucket_website_new_url_format,
            bucket_website_url=bucket_website_url,
            encryption_key=encryption_key,
            is_website=is_website,
            region=region,
        )

        return typing.cast(IBucket, jsii.sinvoke(cls, "fromBucketAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromBucketName") # type: ignore[misc]
    @builtins.classmethod
    def from_bucket_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        bucket_name: builtins.str,
    ) -> IBucket:
        '''
        :param scope: -
        :param id: -
        :param bucket_name: -

        :stability: experimental
        '''
        return typing.cast(IBucket, jsii.sinvoke(cls, "fromBucketName", [scope, id, bucket_name]))

    @jsii.member(jsii_name="addCorsRule")
    def add_cors_rule(
        self,
        *,
        allowed_methods: typing.List[HttpMethods],
        allowed_origins: typing.List[builtins.str],
        allowed_headers: typing.Optional[typing.List[builtins.str]] = None,
        exposed_headers: typing.Optional[typing.List[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        max_age: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Adds a cross-origin access configuration for objects in an Amazon S3 bucket.

        :param allowed_methods: (experimental) An HTTP method that you allow the origin to execute.
        :param allowed_origins: (experimental) One or more origins you want customers to be able to access the bucket from.
        :param allowed_headers: (experimental) Headers that are specified in the Access-Control-Request-Headers header. Default: - No headers allowed.
        :param exposed_headers: (experimental) One or more headers in the response that you want customers to be able to access from their applications. Default: - No headers exposed.
        :param id: (experimental) A unique identifier for this rule. Default: - No id specified.
        :param max_age: (experimental) The time in seconds that your browser is to cache the preflight response for the specified resource. Default: - No caching.

        :stability: experimental
        '''
        rule = CorsRule(
            allowed_methods=allowed_methods,
            allowed_origins=allowed_origins,
            allowed_headers=allowed_headers,
            exposed_headers=exposed_headers,
            id=id,
            max_age=max_age,
        )

        return typing.cast(None, jsii.invoke(self, "addCorsRule", [rule]))

    @jsii.member(jsii_name="addEventNotification")
    def add_event_notification(
        self,
        event: EventType,
        dest: IBucketNotificationDestination,
        *filters: NotificationKeyFilter,
    ) -> None:
        '''(experimental) Adds a bucket notification event destination.

        :param event: The event to trigger the notification.
        :param dest: The notification destination (Lambda, SNS Topic or SQS Queue).
        :param filters: S3 object key filter rules to determine which objects trigger this event. Each filter must include a ``prefix`` and/or ``suffix`` that will be matched against the s3 object key. Refer to the S3 Developer Guide for details about allowed filter rules.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            bucket.add_event_notification(EventType.OnObjectCreated, my_lambda, "home/myusername/*")
        '''
        return typing.cast(None, jsii.invoke(self, "addEventNotification", [event, dest, *filters]))

    @jsii.member(jsii_name="addInventory")
    def add_inventory(
        self,
        *,
        destination: InventoryDestination,
        enabled: typing.Optional[builtins.bool] = None,
        format: typing.Optional[InventoryFormat] = None,
        frequency: typing.Optional[InventoryFrequency] = None,
        include_object_versions: typing.Optional[InventoryObjectVersion] = None,
        inventory_id: typing.Optional[builtins.str] = None,
        objects_prefix: typing.Optional[builtins.str] = None,
        optional_fields: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        '''(experimental) Add an inventory configuration.

        :param destination: (experimental) The destination of the inventory.
        :param enabled: (experimental) Whether the inventory is enabled or disabled. Default: true
        :param format: (experimental) The format of the inventory. Default: InventoryFormat.CSV
        :param frequency: (experimental) Frequency at which the inventory should be generated. Default: InventoryFrequency.WEEKLY
        :param include_object_versions: (experimental) If the inventory should contain all the object versions or only the current one. Default: InventoryObjectVersion.ALL
        :param inventory_id: (experimental) The inventory configuration ID. Default: - generated ID.
        :param objects_prefix: (experimental) The inventory will only include objects that meet the prefix filter criteria. Default: - No objects prefix
        :param optional_fields: (experimental) A list of optional fields to be included in the inventory result. Default: - No optional fields.

        :stability: experimental
        '''
        inventory = Inventory(
            destination=destination,
            enabled=enabled,
            format=format,
            frequency=frequency,
            include_object_versions=include_object_versions,
            inventory_id=inventory_id,
            objects_prefix=objects_prefix,
            optional_fields=optional_fields,
        )

        return typing.cast(None, jsii.invoke(self, "addInventory", [inventory]))

    @jsii.member(jsii_name="addLifecycleRule")
    def add_lifecycle_rule(
        self,
        *,
        abort_incomplete_multipart_upload_after: typing.Optional[_Duration_070aa057] = None,
        enabled: typing.Optional[builtins.bool] = None,
        expiration: typing.Optional[_Duration_070aa057] = None,
        expiration_date: typing.Optional[datetime.datetime] = None,
        id: typing.Optional[builtins.str] = None,
        noncurrent_version_expiration: typing.Optional[_Duration_070aa057] = None,
        noncurrent_version_transitions: typing.Optional[typing.List[NoncurrentVersionTransition]] = None,
        prefix: typing.Optional[builtins.str] = None,
        tag_filters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        transitions: typing.Optional[typing.List[Transition]] = None,
    ) -> None:
        '''(experimental) Add a lifecycle rule to the bucket.

        :param abort_incomplete_multipart_upload_after: (experimental) Specifies a lifecycle rule that aborts incomplete multipart uploads to an Amazon S3 bucket. The AbortIncompleteMultipartUpload property type creates a lifecycle rule that aborts incomplete multipart uploads to an Amazon S3 bucket. When Amazon S3 aborts a multipart upload, it deletes all parts associated with the multipart upload. Default: Incomplete uploads are never aborted
        :param enabled: (experimental) Whether this rule is enabled. Default: true
        :param expiration: (experimental) Indicates the number of days after creation when objects are deleted from Amazon S3 and Amazon Glacier. If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time. Default: No expiration timeout
        :param expiration_date: (experimental) Indicates when objects are deleted from Amazon S3 and Amazon Glacier. The date value must be in ISO 8601 format. The time is always midnight UTC. If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time. Default: No expiration date
        :param id: (experimental) A unique identifier for this rule. The value cannot be more than 255 characters.
        :param noncurrent_version_expiration: (experimental) Time between when a new version of the object is uploaded to the bucket and when old versions of the object expire. For buckets with versioning enabled (or suspended), specifies the time, in days, between when a new version of the object is uploaded to the bucket and when old versions of the object expire. When object versions expire, Amazon S3 permanently deletes them. If you specify a transition and expiration time, the expiration time must be later than the transition time. Default: No noncurrent version expiration
        :param noncurrent_version_transitions: (experimental) One or more transition rules that specify when non-current objects transition to a specified storage class. Only for for buckets with versioning enabled (or suspended). If you specify a transition and expiration time, the expiration time must be later than the transition time.
        :param prefix: (experimental) Object key prefix that identifies one or more objects to which this rule applies. Default: Rule applies to all objects
        :param tag_filters: (experimental) The TagFilter property type specifies tags to use to identify a subset of objects for an Amazon S3 bucket. Default: Rule applies to all objects
        :param transitions: (experimental) One or more transition rules that specify when an object transitions to a specified storage class. If you specify an expiration and transition time, you must use the same time unit for both properties (either in days or by date). The expiration time must also be later than the transition time. Default: No transition rules

        :stability: experimental
        '''
        rule = LifecycleRule(
            abort_incomplete_multipart_upload_after=abort_incomplete_multipart_upload_after,
            enabled=enabled,
            expiration=expiration,
            expiration_date=expiration_date,
            id=id,
            noncurrent_version_expiration=noncurrent_version_expiration,
            noncurrent_version_transitions=noncurrent_version_transitions,
            prefix=prefix,
            tag_filters=tag_filters,
            transitions=transitions,
        )

        return typing.cast(None, jsii.invoke(self, "addLifecycleRule", [rule]))

    @jsii.member(jsii_name="addMetric")
    def add_metric(
        self,
        *,
        id: builtins.str,
        prefix: typing.Optional[builtins.str] = None,
        tag_filters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''(experimental) Adds a metrics configuration for the CloudWatch request metrics from the bucket.

        :param id: (experimental) The ID used to identify the metrics configuration.
        :param prefix: (experimental) The prefix that an object must have to be included in the metrics results.
        :param tag_filters: (experimental) Specifies a list of tag filters to use as a metrics configuration filter. The metrics configuration includes only objects that meet the filter's criteria.

        :stability: experimental
        '''
        metric = BucketMetrics(id=id, prefix=prefix, tag_filters=tag_filters)

        return typing.cast(None, jsii.invoke(self, "addMetric", [metric]))

    @jsii.member(jsii_name="addObjectCreatedNotification")
    def add_object_created_notification(
        self,
        dest: IBucketNotificationDestination,
        *filters: NotificationKeyFilter,
    ) -> None:
        '''(experimental) Subscribes a destination to receive notifications when an object is created in the bucket.

        This is identical to calling
        ``onEvent(EventType.ObjectCreated)``.

        :param dest: The notification destination (see onEvent).
        :param filters: Filters (see onEvent).

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addObjectCreatedNotification", [dest, *filters]))

    @jsii.member(jsii_name="addObjectRemovedNotification")
    def add_object_removed_notification(
        self,
        dest: IBucketNotificationDestination,
        *filters: NotificationKeyFilter,
    ) -> None:
        '''(experimental) Subscribes a destination to receive notifications when an object is removed from the bucket.

        This is identical to calling
        ``onEvent(EventType.ObjectRemoved)``.

        :param dest: The notification destination (see onEvent).
        :param filters: Filters (see onEvent).

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addObjectRemovedNotification", [dest, *filters]))

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        permission: _PolicyStatement_296fe8a3,
    ) -> _AddToResourcePolicyResult_0fd9d2a9:
        '''(experimental) Adds a statement to the resource policy for a principal (i.e. account/role/service) to perform actions on this bucket and/or it's contents. Use ``bucketArn`` and ``arnForObjects(keys)`` to obtain ARNs for this bucket or objects.

        :param permission: -

        :stability: experimental
        '''
        return typing.cast(_AddToResourcePolicyResult_0fd9d2a9, jsii.invoke(self, "addToResourcePolicy", [permission]))

    @jsii.member(jsii_name="arnForObjects")
    def arn_for_objects(self, key_pattern: builtins.str) -> builtins.str:
        '''(experimental) Returns an ARN that represents all objects within the bucket that match the key pattern specified.

        To represent all keys, specify ``"*"``.

        If you need to specify a keyPattern with multiple components, concatenate them into a single string, e.g.:

        arnForObjects(``home/${team}/${user}/*``)

        :param key_pattern: -

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "arnForObjects", [key_pattern]))

    @jsii.member(jsii_name="grantDelete")
    def grant_delete(
        self,
        identity: _IGrantable_4c5a91d1,
        objects_key_pattern: typing.Any = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grants s3:DeleteObject* permission to an IAM principal for objects in this bucket.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantDelete", [identity, objects_key_pattern]))

    @jsii.member(jsii_name="grantPublicAccess")
    def grant_public_access(
        self,
        key_prefix: typing.Optional[builtins.str] = None,
        *allowed_actions: builtins.str,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Allows unrestricted access to objects from this bucket.

        IMPORTANT: This permission allows anyone to perform actions on S3 objects
        in this bucket, which is useful for when you configure your bucket as a
        website and want everyone to be able to read objects in the bucket without
        needing to authenticate.

        Without arguments, this method will grant read ("s3:GetObject") access to
        all objects ("*") in the bucket.

        The method returns the ``iam.Grant`` object, which can then be modified
        as needed. For example, you can add a condition that will restrict access only
        to an IPv4 range like this::

            const grant = bucket.grantPublicAccess();
            grant.resourceStatement!.addCondition(‘IpAddress’, { “aws:SourceIp”: “54.240.143.0/24” });

        :param key_prefix: the prefix of S3 object keys (e.g. ``home/*``). Default is "*".
        :param allowed_actions: the set of S3 actions to allow. Default is "s3:GetObject".

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPublicAccess", [key_prefix, *allowed_actions]))

    @jsii.member(jsii_name="grantPut")
    def grant_put(
        self,
        identity: _IGrantable_4c5a91d1,
        objects_key_pattern: typing.Any = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grants s3:PutObject* and s3:Abort* permissions for this bucket to an IAM principal.

        If encryption is used, permission to use the key to encrypt the contents
        of written files will also be granted to the same principal.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPut", [identity, objects_key_pattern]))

    @jsii.member(jsii_name="grantPutAcl")
    def grant_put_acl(
        self,
        identity: _IGrantable_4c5a91d1,
        objects_key_pattern: typing.Optional[builtins.str] = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given IAM identity permissions to modify the ACLs of objects in the given Bucket.

        If your application has the '@aws-cdk/aws-s3:grantWriteWithoutAcl' feature flag set,
        calling {@link grantWrite} or {@link grantReadWrite} no longer grants permissions to modify the ACLs of the objects;
        in this case, if you need to modify object ACLs, call this method explicitly.

        :param identity: -
        :param objects_key_pattern: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPutAcl", [identity, objects_key_pattern]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        identity: _IGrantable_4c5a91d1,
        objects_key_pattern: typing.Any = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant read permissions for this bucket and it's contents to an IAM principal (Role/Group/User).

        If encryption is used, permission to use the key to decrypt the contents
        of the bucket will also be granted to the same principal.

        :param identity: The principal.
        :param objects_key_pattern: Restrict the permission to a certain key pattern (default '*').

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantRead", [identity, objects_key_pattern]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        identity: _IGrantable_4c5a91d1,
        objects_key_pattern: typing.Any = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grants read/write permissions for this bucket and it's contents to an IAM principal (Role/Group/User).

        If an encryption key is used, permission to use the key for
        encrypt/decrypt will also be granted.

        Before CDK version 1.85.0, this method granted the ``s3:PutObject*`` permission that included ``s3:PutObjectAcl``,
        which could be used to grant read/write object access to IAM principals in other accounts.
        If you want to get rid of that behavior, update your CDK version to 1.85.0 or later,
        and make sure the ``@aws-cdk/aws-s3:grantWriteWithoutAcl`` feature flag is set to ``true``
        in the ``context`` key of your cdk.json file.
        If you've already updated, but still need the principal to have permissions to modify the ACLs,
        use the {@link grantPutAcl} method.

        :param identity: -
        :param objects_key_pattern: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantReadWrite", [identity, objects_key_pattern]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        identity: _IGrantable_4c5a91d1,
        objects_key_pattern: typing.Any = None,
    ) -> _Grant_bcb5eae7:
        '''(experimental) Grant write permissions to this bucket to an IAM principal.

        If encryption is used, permission to use the key to encrypt the contents
        of written files will also be granted to the same principal.

        Before CDK version 1.85.0, this method granted the ``s3:PutObject*`` permission that included ``s3:PutObjectAcl``,
        which could be used to grant read/write object access to IAM principals in other accounts.
        If you want to get rid of that behavior, update your CDK version to 1.85.0 or later,
        and make sure the ``@aws-cdk/aws-s3:grantWriteWithoutAcl`` feature flag is set to ``true``
        in the ``context`` key of your cdk.json file.
        If you've already updated, but still need the principal to have permissions to modify the ACLs,
        use the {@link grantPutAcl} method.

        :param identity: -
        :param objects_key_pattern: -

        :stability: experimental
        '''
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantWrite", [identity, objects_key_pattern]))

    @jsii.member(jsii_name="onCloudTrailEvent")
    def on_cloud_trail_event(
        self,
        id: builtins.str,
        *,
        paths: typing.Optional[typing.List[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Define a CloudWatch event that triggers when something happens to this repository.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param paths: (experimental) Only watch changes to these object paths. Default: - Watch changes to all objects
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        options = OnCloudTrailBucketEventOptions(
            paths=paths,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onCloudTrailEvent", [id, options]))

    @jsii.member(jsii_name="onCloudTrailPutObject")
    def on_cloud_trail_put_object(
        self,
        id: builtins.str,
        *,
        paths: typing.Optional[typing.List[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines an AWS CloudWatch event that triggers when an object is uploaded to the specified paths (keys) in this bucket using the PutObject API call.

        Note that some tools like ``aws s3 cp`` will automatically use either
        PutObject or the multipart upload API depending on the file size,
        so using ``onCloudTrailWriteObject`` may be preferable.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param paths: (experimental) Only watch changes to these object paths. Default: - Watch changes to all objects
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        options = OnCloudTrailBucketEventOptions(
            paths=paths,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onCloudTrailPutObject", [id, options]))

    @jsii.member(jsii_name="onCloudTrailWriteObject")
    def on_cloud_trail_write_object(
        self,
        id: builtins.str,
        *,
        paths: typing.Optional[typing.List[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[_EventPattern_a23fbf37] = None,
        rule_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
    ) -> _Rule_6cfff189:
        '''(experimental) Defines an AWS CloudWatch event that triggers when an object at the specified paths (keys) in this bucket are written to.

        This includes
        the events PutObject, CopyObject, and CompleteMultipartUpload.

        Note that some tools like ``aws s3 cp`` will automatically use either
        PutObject or the multipart upload API depending on the file size,
        so using this method may be preferable to ``onCloudTrailPutObject``.

        Requires that there exists at least one CloudTrail Trail in your account
        that captures the event. This method will not create the Trail.

        :param id: The id of the rule.
        :param paths: (experimental) Only watch changes to these object paths. Default: - Watch changes to all objects
        :param description: (experimental) A description of the rule's purpose. Default: - No description
        :param event_pattern: (experimental) Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: (experimental) A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: (experimental) The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        :stability: experimental
        '''
        options = OnCloudTrailBucketEventOptions(
            paths=paths,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onCloudTrailWriteObject", [id, options]))

    @jsii.member(jsii_name="s3UrlForObject")
    def s3_url_for_object(
        self,
        key: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''(experimental) The S3 URL of an S3 object.

        For example:

        :param key: The S3 key of the object. If not specified, the S3 URL of the bucket is returned.

        :return: an ObjectS3Url token

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            s3:
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "s3UrlForObject", [key]))

    @jsii.member(jsii_name="urlForObject")
    def url_for_object(self, key: typing.Optional[builtins.str] = None) -> builtins.str:
        '''(experimental) The https URL of an S3 object.

        Specify ``regional: false`` at the options
        for non-regional URLs. For example:

        :param key: The S3 key of the object. If not specified, the URL of the bucket is returned.

        :return: an ObjectS3Url token

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            https:
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "urlForObject", [key]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''(experimental) Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @jsii.member(jsii_name="virtualHostedUrlForObject")
    def virtual_hosted_url_for_object(
        self,
        key: typing.Optional[builtins.str] = None,
        *,
        regional: typing.Optional[builtins.bool] = None,
    ) -> builtins.str:
        '''(experimental) The virtual hosted-style URL of an S3 object.

        Specify ``regional: false`` at
        the options for non-regional URL. For example:

        :param key: The S3 key of the object. If not specified, the URL of the bucket is returned.
        :param regional: (experimental) Specifies the URL includes the region. Default: - true

        :return: an ObjectS3Url token

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            https:
        '''
        options = VirtualHostedStyleUrlOptions(regional=regional)

        return typing.cast(builtins.str, jsii.invoke(self, "virtualHostedUrlForObject", [key, options]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> builtins.str:
        '''(experimental) The ARN of the bucket.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketDomainName")
    def bucket_domain_name(self) -> builtins.str:
        '''(experimental) The IPv4 DNS name of the specified bucket.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketDomainName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketDualStackDomainName")
    def bucket_dual_stack_domain_name(self) -> builtins.str:
        '''(experimental) The IPv6 DNS name of the specified bucket.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketDualStackDomainName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        '''(experimental) The name of the bucket.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketRegionalDomainName")
    def bucket_regional_domain_name(self) -> builtins.str:
        '''(experimental) The regional domain name of the specified bucket.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketRegionalDomainName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketWebsiteDomainName")
    def bucket_website_domain_name(self) -> builtins.str:
        '''(experimental) The Domain name of the static website.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketWebsiteDomainName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucketWebsiteUrl")
    def bucket_website_url(self) -> builtins.str:
        '''(experimental) The URL of the static website.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketWebsiteUrl"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) Optional KMS encryption key associated with this bucket.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IKey_36930160], jsii.get(self, "encryptionKey"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="isWebsite")
    def is_website(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If this bucket has been configured for static website hosting.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "isWebsite"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> builtins.bool:
        '''(experimental) Indicates if a bucket resource policy should automatically created upon the first call to ``addToResourcePolicy``.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "autoCreatePolicy"))

    @_auto_create_policy.setter
    def _auto_create_policy(self, value: builtins.bool) -> None:
        jsii.set(self, "autoCreatePolicy", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="disallowPublicAccess")
    def _disallow_public_access(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to disallow public access.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "disallowPublicAccess"))

    @_disallow_public_access.setter
    def _disallow_public_access(self, value: typing.Optional[builtins.bool]) -> None:
        jsii.set(self, "disallowPublicAccess", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Optional[BucketPolicy]:
        '''(experimental) The resource policy associated with this bucket.

        If ``autoCreatePolicy`` is true, a ``BucketPolicy`` will be created upon the
        first call to addToResourcePolicy(s).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[BucketPolicy], jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: typing.Optional[BucketPolicy]) -> None:
        jsii.set(self, "policy", value)


__all__ = [
    "BlockPublicAccess",
    "BlockPublicAccessOptions",
    "Bucket",
    "BucketAccessControl",
    "BucketAttributes",
    "BucketEncryption",
    "BucketMetrics",
    "BucketNotificationDestinationConfig",
    "BucketNotificationDestinationType",
    "BucketPolicy",
    "BucketPolicyProps",
    "BucketProps",
    "CfnAccessPoint",
    "CfnAccessPointProps",
    "CfnBucket",
    "CfnBucketPolicy",
    "CfnBucketPolicyProps",
    "CfnBucketProps",
    "CfnStorageLens",
    "CfnStorageLensProps",
    "CorsRule",
    "EventType",
    "HttpMethods",
    "IBucket",
    "IBucketNotificationDestination",
    "Inventory",
    "InventoryDestination",
    "InventoryFormat",
    "InventoryFrequency",
    "InventoryObjectVersion",
    "LifecycleRule",
    "Location",
    "NoncurrentVersionTransition",
    "NotificationKeyFilter",
    "ObjectOwnership",
    "OnCloudTrailBucketEventOptions",
    "RedirectProtocol",
    "RedirectTarget",
    "ReplaceKey",
    "RoutingRule",
    "RoutingRuleCondition",
    "StorageClass",
    "Transition",
    "VirtualHostedStyleUrlOptions",
]

publication.publish()
