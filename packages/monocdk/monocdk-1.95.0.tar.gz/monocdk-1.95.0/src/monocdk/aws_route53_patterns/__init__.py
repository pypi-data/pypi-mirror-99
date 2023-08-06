'''
# CDK Construct library for higher-level Route 53 Constructs

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This library provides higher-level Amazon Route 53 constructs which follow common
architectural patterns.

## HTTPS Redirect

If you want to speed up delivery of your web content, you can use Amazon CloudFront,
the AWS content delivery network (CDN). CloudFront can deliver your entire website
—including dynamic, static, streaming, and interactive content—by using a global
network of edge locations. Requests for your content are automatically routed to the
edge location that gives your users the lowest latency.

This construct allows creating a redirect from domainA to domainB using Amazon
CloudFront and Amazon S3. You can specify multiple domains to be redirected.
[Learn more](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-cloudfront-distribution.html) about routing traffic to a CloudFront web distribution.

The `HttpsRedirect` constructs creates:

* Amazon CloudFront distribution - makes website available from data centres
  around the world
* Amazon S3 bucket - empty bucket used for website hosting redirect (`websiteRedirect`) capabilities.
* Amazon Route 53 A/AAAA Alias records - routes traffic to the CloudFront distribution
* AWS Certificate Manager certificate - SSL/TLS certificate used by
  CloudFront for your domain

⚠️ The stack/construct can be used in any region for configuring an HTTPS redirect.
The certificate created in Amazon Certificate Manager (ACM) will be in US East (N. Virginia)
region. If you use an existing certificate, the AWS region of the certificate
must be in US East (N. Virginia).

The following example creates an HTTPS redirect from `foo.example.com` to `bar.example.com`
As an existing certificate is not provided, one will be created in `us-east-1` by the CDK.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
HttpsRedirect(stack, "Redirect",
    record_names=["foo.example.com"],
    target_domain="bar.example.com",
    zone=HostedZone.from_hosted_zone_attributes(stack, "HostedZone",
        hosted_zone_id="ID",
        zone_name="example.com"
    )
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
from .. import Construct as _Construct_e78e779f
from ..aws_certificatemanager import ICertificate as _ICertificate_c7bbdc16
from ..aws_route53 import IHostedZone as _IHostedZone_78d5a9c9


class HttpsRedirect(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53_patterns.HttpsRedirect",
):
    '''(experimental) Allows creating a domainA -> domainB redirect using CloudFront and S3.

    You can specify multiple domains to be redirected.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        target_domain: builtins.str,
        zone: _IHostedZone_78d5a9c9,
        certificate: typing.Optional[_ICertificate_c7bbdc16] = None,
        record_names: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param target_domain: (experimental) The redirect target fully qualified domain name (FQDN). An alias record will be created that points to your CloudFront distribution. Root domain or sub-domain can be supplied.
        :param zone: (experimental) Hosted zone of the domain which will be used to create alias record(s) from domain names in the hosted zone to the target domain. The hosted zone must contain entries for the domain name(s) supplied through ``recordNames`` that will redirect to the target domain. Domain names in the hosted zone can include a specific domain (example.com) and its subdomains (acme.example.com, zenith.example.com).
        :param certificate: (experimental) The AWS Certificate Manager (ACM) certificate that will be associated with the CloudFront distribution that will be created. If provided, the certificate must be stored in us-east-1 (N. Virginia) Default: - A new certificate is created in us-east-1 (N. Virginia)
        :param record_names: (experimental) The domain names that will redirect to ``targetDomain``. Default: - the domain name of the hosted zone

        :stability: experimental
        '''
        props = HttpsRedirectProps(
            target_domain=target_domain,
            zone=zone,
            certificate=certificate,
            record_names=record_names,
        )

        jsii.create(HttpsRedirect, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk.aws_route53_patterns.HttpsRedirectProps",
    jsii_struct_bases=[],
    name_mapping={
        "target_domain": "targetDomain",
        "zone": "zone",
        "certificate": "certificate",
        "record_names": "recordNames",
    },
)
class HttpsRedirectProps:
    def __init__(
        self,
        *,
        target_domain: builtins.str,
        zone: _IHostedZone_78d5a9c9,
        certificate: typing.Optional[_ICertificate_c7bbdc16] = None,
        record_names: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        '''(experimental) Properties to configure an HTTPS Redirect.

        :param target_domain: (experimental) The redirect target fully qualified domain name (FQDN). An alias record will be created that points to your CloudFront distribution. Root domain or sub-domain can be supplied.
        :param zone: (experimental) Hosted zone of the domain which will be used to create alias record(s) from domain names in the hosted zone to the target domain. The hosted zone must contain entries for the domain name(s) supplied through ``recordNames`` that will redirect to the target domain. Domain names in the hosted zone can include a specific domain (example.com) and its subdomains (acme.example.com, zenith.example.com).
        :param certificate: (experimental) The AWS Certificate Manager (ACM) certificate that will be associated with the CloudFront distribution that will be created. If provided, the certificate must be stored in us-east-1 (N. Virginia) Default: - A new certificate is created in us-east-1 (N. Virginia)
        :param record_names: (experimental) The domain names that will redirect to ``targetDomain``. Default: - the domain name of the hosted zone

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "target_domain": target_domain,
            "zone": zone,
        }
        if certificate is not None:
            self._values["certificate"] = certificate
        if record_names is not None:
            self._values["record_names"] = record_names

    @builtins.property
    def target_domain(self) -> builtins.str:
        '''(experimental) The redirect target fully qualified domain name (FQDN).

        An alias record
        will be created that points to your CloudFront distribution. Root domain
        or sub-domain can be supplied.

        :stability: experimental
        '''
        result = self._values.get("target_domain")
        assert result is not None, "Required property 'target_domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def zone(self) -> _IHostedZone_78d5a9c9:
        '''(experimental) Hosted zone of the domain which will be used to create alias record(s) from domain names in the hosted zone to the target domain.

        The hosted zone must
        contain entries for the domain name(s) supplied through ``recordNames`` that
        will redirect to the target domain.

        Domain names in the hosted zone can include a specific domain (example.com)
        and its subdomains (acme.example.com, zenith.example.com).

        :stability: experimental
        '''
        result = self._values.get("zone")
        assert result is not None, "Required property 'zone' is missing"
        return typing.cast(_IHostedZone_78d5a9c9, result)

    @builtins.property
    def certificate(self) -> typing.Optional[_ICertificate_c7bbdc16]:
        '''(experimental) The AWS Certificate Manager (ACM) certificate that will be associated with the CloudFront distribution that will be created.

        If provided, the certificate must be
        stored in us-east-1 (N. Virginia)

        :default: - A new certificate is created in us-east-1 (N. Virginia)

        :stability: experimental
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[_ICertificate_c7bbdc16], result)

    @builtins.property
    def record_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The domain names that will redirect to ``targetDomain``.

        :default: - the domain name of the hosted zone

        :stability: experimental
        '''
        result = self._values.get("record_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpsRedirectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "HttpsRedirect",
    "HttpsRedirectProps",
]

publication.publish()
