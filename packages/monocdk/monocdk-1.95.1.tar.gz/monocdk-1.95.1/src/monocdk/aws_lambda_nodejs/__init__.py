'''
# Amazon Lambda Node.js Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This library provides constructs for Node.js Lambda functions.

To use this module, you will need to have Docker installed.

## Node.js Function

Define a `NodejsFunction`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lambda_.NodejsFunction(self, "my-handler")
```

By default, the construct will use the name of the defining file and the construct's id to look
up the entry file:

```plaintext
.
├── stack.ts # defines a 'NodejsFunction' with 'my-handler' as id
├── stack.my-handler.ts # exports a function named 'handler'
```

This file is used as "entry" for [esbuild](https://esbuild.github.io/). This means that your code is automatically transpiled and bundled whether it's written in JavaScript or TypeScript.

Alternatively, an entry file and handler can be specified:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lambda_.NodejsFunction(self, "MyFunction",
    entry="/path/to/my/file.ts", # accepts .js, .jsx, .ts and .tsx files
    handler="myExportedFunc"
)
```

All other properties of `lambda.Function` are supported, see also the [AWS Lambda construct library](https://github.com/aws/aws-cdk/tree/master/packages/%40aws-cdk/aws-lambda).

The `NodejsFunction` construct automatically [reuses existing connections](https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/node-reusing-connections.html)
when working with the AWS SDK for JavaScript. Set the `awsSdkConnectionReuse` prop to `false` to disable it.

## Lock file

The `NodejsFunction` requires a dependencies lock file (`yarn.lock` or
`package-lock.json`). When bundling in a Docker container, the path containing this
lock file is used as the source (`/asset-input`) for the volume mounted in the
container.

By default, the construct will try to automatically determine your project lock file.
Alternatively, you can specify the `depsLockFilePath` prop manually. In this
case you need to ensure that this path includes `entry` and any module/dependencies
used by your function. Otherwise bundling will fail.

## Local bundling

If `esbuild` is available it will be used to bundle your code in your environment. Otherwise,
bundling will happen in a [Lambda compatible Docker container](https://hub.docker.com/r/amazon/aws-sam-cli-build-image-nodejs12.x).

For macOS the recommendend approach is to install `esbuild` as Docker volume performance is really poor.

`esbuild` can be installed with:

```console
$ npm install --save-dev esbuild@0
```

OR

```console
$ yarn add --dev esbuild@0
```

To force bundling in a Docker container even if `esbuild` is available in your environment,
set `bundling.forceDockerBundling` to `true`. This is useful if your function relies on node
modules that should be installed (`nodeModules` prop, see [below](#install-modules)) in a Lambda
compatible environment. This is usually the case with modules using native dependencies.

## Working with modules

### Externals

By default, all node modules are bundled except for `aws-sdk`. This can be configured by specifying
`bundling.externalModules`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lambda_.NodejsFunction(self, "my-handler",
    bundling={
        "external_modules": ["aws-sdk", "cool-module"
        ]
    }
)
```

### Install modules

By default, all node modules referenced in your Lambda code will be bundled by `esbuild`.
Use the `nodeModules` prop under `bundling` to specify a list of modules that should not be
bundled but instead included in the `node_modules` folder of the Lambda package. This is useful
when working with native dependencies or when `esbuild` fails to bundle a module.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lambda_.NodejsFunction(self, "my-handler",
    bundling={
        "node_modules": ["native-module", "other-module"]
    }
)
```

The modules listed in `nodeModules` must be present in the `package.json`'s dependencies or
installed. The same version will be used for installation. The lock file (`yarn.lock` or
`package-lock.json`) will be used along with the right installer (`yarn` or `npm`).

When working with `nodeModules` using native dependencies, you might want to force bundling in a
Docker container even if `esbuild` is available in your environment. This can be done by setting
`bundling.forceDockerBundling` to `true`.

## Configuring `esbuild`

The `NodejsFunction` construct exposes some [esbuild options](https://esbuild.github.io/api/#build-api)
via properties under `bundling`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lambda_.NodejsFunction(self, "my-handler",
    bundling={
        "minify": True, # minify code, defaults to false
        "source_map": True, # include source map, defaults to false
        "target": "es2020", # target environment for the generated JavaScript code
        "loader": {# Use the 'dataurl' loader for '.png' files
            ".png": "dataurl"},
        "define": {# Replace strings during build time
            "process.env._aPI__kEY": JSON.stringify("xxx-xxxx-xxx")},
        "log_level": LogLevel.SILENT, # defaults to LogLevel.WARNING
        "keep_names": True, # defaults to false
        "tsconfig": "custom-tsconfig.json", # use custom-tsconfig.json instead of default,
        "metafile": True, # include meta file, defaults to false
        "banner": "/* comments */", # by default no comments are passed
        "footer": "/* comments */"
    }
)
```

## Command hooks

It is possible to run additional commands by specifying the `commandHooks` prop:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lambda_.NodejsFunction(self, "my-handler-with-commands",
    bundling={
        "command_hooks": {
            # Copy a file so that it will be included in the bundled asset
            def after_bundling(input_dir, output_dir): return [f"cp {inputDir}/my-binary.node {outputDir}"]
        }
    }
)
```

The following hooks are available:

* `beforeBundling`: runs before all bundling commands
* `beforeInstall`: runs before node modules installation
* `afterBundling`: runs after all bundling commands

They all receive the directory containing the lock file (`inputDir`) and the
directory where the bundled asset will be output (`outputDir`). They must return
an array of commands to run. Commands are chained with `&&`.

The commands will run in the environment in which bundling occurs: inside the
container for Docker bundling or on the host OS for local bundling.

## Customizing Docker bundling

Use `bundling.environment` to define environments variables when `esbuild` runs:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lambda_.NodejsFunction(self, "my-handler",
    bundling={
        "environment": {
            "NODE_ENV": "production"
        }
    }
)
```

Use `bundling.buildArgs` to pass build arguments when building the Docker bundling image:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lambda_.NodejsFunction(self, "my-handler",
    bundling={
        "build_args": {
            "HTTPS_PROXY": "https://127.0.0.1:3001"
        }
    }
)
```

Use `bundling.dockerImage` to use a custom Docker bundling image:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lambda_.NodejsFunction(self, "my-handler",
    bundling={
        "docker_image": cdk.DockerImage.from_build("/path/to/Dockerfile")
    }
)
```

This image should have `esbuild` installed **globally**. If you plan to use `nodeModules` it
should also have `npm` or `yarn` depending on the lock file you're using.

Use the [default image provided by `@aws-cdk/aws-lambda-nodejs`](https://github.com/aws/aws-cdk/blob/master/packages/%40aws-cdk/aws-lambda-nodejs/lib/Dockerfile)
as a source of inspiration.
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
    Construct as _Construct_e78e779f,
    DockerImage as _DockerImage_d5f0ad8e,
    Duration as _Duration_070aa057,
)
from ..aws_codeguruprofiler import IProfilingGroup as _IProfilingGroup_418eb20c
from ..aws_ec2 import (
    ISecurityGroup as _ISecurityGroup_cdbba9d3,
    IVpc as _IVpc_6d1f76c4,
    SubnetSelection as _SubnetSelection_1284e62c,
)
from ..aws_iam import (
    IRole as _IRole_59af6f50, PolicyStatement as _PolicyStatement_296fe8a3
)
from ..aws_kms import IKey as _IKey_36930160
from ..aws_lambda import (
    FileSystem as _FileSystem_17be1f4c,
    Function as _Function_40b20aa5,
    FunctionOptions as _FunctionOptions_dc75a392,
    ICodeSigningConfig as _ICodeSigningConfig_5d77bccf,
    IDestination as _IDestination_7f253ff1,
    IEventSource as _IEventSource_7914870e,
    ILayerVersion as _ILayerVersion_b2b86380,
    LogRetentionRetryOptions as _LogRetentionRetryOptions_7acc40ab,
    Runtime as _Runtime_932d369a,
    Tracing as _Tracing_b7f4a8b6,
    VersionOptions as _VersionOptions_085bb455,
)
from ..aws_logs import RetentionDays as _RetentionDays_6c560d31
from ..aws_sqs import IQueue as _IQueue_45a01ab4


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_nodejs.BundlingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "banner": "banner",
        "build_args": "buildArgs",
        "command_hooks": "commandHooks",
        "define": "define",
        "docker_image": "dockerImage",
        "environment": "environment",
        "esbuild_version": "esbuildVersion",
        "external_modules": "externalModules",
        "footer": "footer",
        "force_docker_bundling": "forceDockerBundling",
        "keep_names": "keepNames",
        "loader": "loader",
        "log_level": "logLevel",
        "metafile": "metafile",
        "minify": "minify",
        "node_modules": "nodeModules",
        "source_map": "sourceMap",
        "target": "target",
        "tsconfig": "tsconfig",
    },
)
class BundlingOptions:
    def __init__(
        self,
        *,
        banner: typing.Optional[builtins.str] = None,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        command_hooks: typing.Optional["ICommandHooks"] = None,
        define: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        docker_image: typing.Optional[_DockerImage_d5f0ad8e] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        esbuild_version: typing.Optional[builtins.str] = None,
        external_modules: typing.Optional[typing.List[builtins.str]] = None,
        footer: typing.Optional[builtins.str] = None,
        force_docker_bundling: typing.Optional[builtins.bool] = None,
        keep_names: typing.Optional[builtins.bool] = None,
        loader: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        log_level: typing.Optional["LogLevel"] = None,
        metafile: typing.Optional[builtins.bool] = None,
        minify: typing.Optional[builtins.bool] = None,
        node_modules: typing.Optional[typing.List[builtins.str]] = None,
        source_map: typing.Optional[builtins.bool] = None,
        target: typing.Optional[builtins.str] = None,
        tsconfig: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Bundling options.

        :param banner: (experimental) Use this to insert an arbitrary string at the beginning of generated JavaScript files. This is similar to footer which inserts at the end instead of the beginning. This is commonly used to insert comments: Default: - no comments are passed
        :param build_args: (experimental) Build arguments to pass when building the bundling image. Default: - no build arguments are passed
        :param command_hooks: (experimental) Command hooks. Default: - do not run additional commands
        :param define: (experimental) Replace global identifiers with constant expressions. Default: - no replacements are made
        :param docker_image: (experimental) A custom bundling Docker image. This image should have esbuild installed globally. If you plan to use ``nodeModules`` it should also have ``npm`` or ``yarn`` depending on the lock file you're using. See https://github.com/aws/aws-cdk/blob/master/packages/%40aws-cdk/aws-lambda-nodejs/lib/Dockerfile for the default image provided by @aws-cdk/aws-lambda-nodejs. Default: - use the Docker image provided by
        :param environment: (experimental) Environment variables defined when bundling runs. Default: - no environment variables are defined.
        :param esbuild_version: (experimental) The version of esbuild to use when running in a Docker container. Default: - latest v0
        :param external_modules: (experimental) A list of modules that should be considered as externals (already available in the runtime). Default: ['aws-sdk']
        :param footer: (experimental) Use this to insert an arbitrary string at the end of generated JavaScript files. This is similar to banner which inserts at the beginning instead of the end. This is commonly used to insert comments Default: - no comments are passed
        :param force_docker_bundling: (experimental) Force bundling in a Docker container even if local bundling is possible. This is useful if your function relies on node modules that should be installed (``nodeModules``) in a Lambda compatible environment. Default: false
        :param keep_names: (experimental) Whether to preserve the original ``name`` values even in minified code. In JavaScript the ``name`` property on functions and classes defaults to a nearby identifier in the source code. However, minification renames symbols to reduce code size and bundling sometimes need to rename symbols to avoid collisions. That changes value of the ``name`` property for many of these cases. This is usually fine because the ``name`` property is normally only used for debugging. However, some frameworks rely on the ``name`` property for registration and binding purposes. If this is the case, you can enable this option to preserve the original ``name`` values even in minified code. Default: false
        :param loader: (experimental) Use loaders to change how a given input file is interpreted. Configuring a loader for a given file type lets you load that file type with an ``import`` statement or a ``require`` call. Default: - use esbuild default loaders
        :param log_level: (experimental) Log level for esbuild. Default: LogLevel.WARNING
        :param metafile: (experimental) This option tells esbuild to write out a JSON file relative to output directory with metadata about the build. The metadata in this JSON file follows this schema (specified using TypeScript syntax):: { outputs: { [path: string]: { bytes: number inputs: { [path: string]: { bytesInOutput: number } } imports: { path: string }[] exports: string[] } } } } This data can then be analyzed by other tools. For example, bundle buddy can consume esbuild's metadata format and generates a treemap visualization of the modules in your bundle and how much space each one takes up. Default: - false
        :param minify: (experimental) Whether to minify files when bundling. Default: false
        :param node_modules: (experimental) A list of modules that should be installed instead of bundled. Modules are installed in a Lambda compatible environment only when bundling runs in Docker. Default: - all modules are bundled
        :param source_map: (experimental) Whether to include source maps when bundling. Default: false
        :param target: (experimental) Target environment for the generated JavaScript code. Default: - the node version of the runtime
        :param tsconfig: (experimental) Normally the esbuild automatically discovers ``tsconfig.json`` files and reads their contents during a build. However, you can also configure a custom ``tsconfig.json`` file to use instead. This is similar to entry path, you need to provide path to your custom ``tsconfig.json``. This can be useful if you need to do multiple builds of the same code with different settings. Default: - automatically discovered by ``esbuild``

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if banner is not None:
            self._values["banner"] = banner
        if build_args is not None:
            self._values["build_args"] = build_args
        if command_hooks is not None:
            self._values["command_hooks"] = command_hooks
        if define is not None:
            self._values["define"] = define
        if docker_image is not None:
            self._values["docker_image"] = docker_image
        if environment is not None:
            self._values["environment"] = environment
        if esbuild_version is not None:
            self._values["esbuild_version"] = esbuild_version
        if external_modules is not None:
            self._values["external_modules"] = external_modules
        if footer is not None:
            self._values["footer"] = footer
        if force_docker_bundling is not None:
            self._values["force_docker_bundling"] = force_docker_bundling
        if keep_names is not None:
            self._values["keep_names"] = keep_names
        if loader is not None:
            self._values["loader"] = loader
        if log_level is not None:
            self._values["log_level"] = log_level
        if metafile is not None:
            self._values["metafile"] = metafile
        if minify is not None:
            self._values["minify"] = minify
        if node_modules is not None:
            self._values["node_modules"] = node_modules
        if source_map is not None:
            self._values["source_map"] = source_map
        if target is not None:
            self._values["target"] = target
        if tsconfig is not None:
            self._values["tsconfig"] = tsconfig

    @builtins.property
    def banner(self) -> typing.Optional[builtins.str]:
        '''(experimental) Use this to insert an arbitrary string at the beginning of generated JavaScript files.

        This is similar to footer which inserts at the end instead of the beginning.

        This is commonly used to insert comments:

        :default: - no comments are passed

        :stability: experimental
        '''
        result = self._values.get("banner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Build arguments to pass when building the bundling image.

        :default: - no build arguments are passed

        :stability: experimental
        '''
        result = self._values.get("build_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def command_hooks(self) -> typing.Optional["ICommandHooks"]:
        '''(experimental) Command hooks.

        :default: - do not run additional commands

        :stability: experimental
        '''
        result = self._values.get("command_hooks")
        return typing.cast(typing.Optional["ICommandHooks"], result)

    @builtins.property
    def define(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Replace global identifiers with constant expressions.

        :default: - no replacements are made

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "process.env.API_KEY"JSON.stringify("xxx-xxxx-xxx")
        '''
        result = self._values.get("define")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def docker_image(self) -> typing.Optional[_DockerImage_d5f0ad8e]:
        '''(experimental) A custom bundling Docker image.

        This image should have esbuild installed globally. If you plan to use ``nodeModules``
        it should also have ``npm`` or ``yarn`` depending on the lock file you're using.

        See https://github.com/aws/aws-cdk/blob/master/packages/%40aws-cdk/aws-lambda-nodejs/lib/Dockerfile
        for the default image provided by @aws-cdk/aws-lambda-nodejs.

        :default: - use the Docker image provided by

        :stability: experimental
        :aws-cdk: /aws-lambda-nodejs
        '''
        result = self._values.get("docker_image")
        return typing.cast(typing.Optional[_DockerImage_d5f0ad8e], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables defined when bundling runs.

        :default: - no environment variables are defined.

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def esbuild_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of esbuild to use when running in a Docker container.

        :default: - latest v0

        :stability: experimental
        '''
        result = self._values.get("esbuild_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_modules(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of modules that should be considered as externals (already available in the runtime).

        :default: ['aws-sdk']

        :stability: experimental
        '''
        result = self._values.get("external_modules")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def footer(self) -> typing.Optional[builtins.str]:
        '''(experimental) Use this to insert an arbitrary string at the end of generated JavaScript files.

        This is similar to banner which inserts at the beginning instead of the end.

        This is commonly used to insert comments

        :default: - no comments are passed

        :stability: experimental
        '''
        result = self._values.get("footer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_docker_bundling(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Force bundling in a Docker container even if local bundling is possible.

        This is useful if your function relies on node modules
        that should be installed (``nodeModules``) in a Lambda compatible
        environment.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("force_docker_bundling")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def keep_names(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to preserve the original ``name`` values even in minified code.

        In JavaScript the ``name`` property on functions and classes defaults to a
        nearby identifier in the source code.

        However, minification renames symbols to reduce code size and bundling
        sometimes need to rename symbols to avoid collisions. That changes value of
        the ``name`` property for many of these cases. This is usually fine because
        the ``name`` property is normally only used for debugging. However, some
        frameworks rely on the ``name`` property for registration and binding purposes.
        If this is the case, you can enable this option to preserve the original
        ``name`` values even in minified code.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("keep_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def loader(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Use loaders to change how a given input file is interpreted.

        Configuring a loader for a given file type lets you load that file type with
        an ``import`` statement or a ``require`` call.

        :default: - use esbuild default loaders

        :see: https://esbuild.github.io/api/#loader
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            ".png""dataurl"
        '''
        result = self._values.get("loader")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def log_level(self) -> typing.Optional["LogLevel"]:
        '''(experimental) Log level for esbuild.

        :default: LogLevel.WARNING

        :stability: experimental
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional["LogLevel"], result)

    @builtins.property
    def metafile(self) -> typing.Optional[builtins.bool]:
        '''(experimental) This option tells esbuild to write out a JSON file relative to output directory with metadata about the build.

        The metadata in this JSON file follows this schema (specified using TypeScript syntax)::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           outputs: {
                         [path: string]: {
                           bytes: number
                           inputs: {
                             [path: string]: { bytesInOutput: number }
                           }
                           imports: { path: string }[]
                           exports: string[]
                         }
                       }

        This data can then be analyzed by other tools. For example,
        bundle buddy can consume esbuild's metadata format and generates a treemap visualization
        of the modules in your bundle and how much space each one takes up.

        :default: - false

        :see: https://esbuild.github.io/api/#metafile
        :stability: experimental
        '''
        result = self._values.get("metafile")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minify(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to minify files when bundling.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("minify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def node_modules(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of modules that should be installed instead of bundled.

        Modules are
        installed in a Lambda compatible environment only when bundling runs in
        Docker.

        :default: - all modules are bundled

        :stability: experimental
        '''
        result = self._values.get("node_modules")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source_map(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to include source maps when bundling.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("source_map")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''(experimental) Target environment for the generated JavaScript code.

        :default: - the node version of the runtime

        :see: https://esbuild.github.io/api/#target
        :stability: experimental
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tsconfig(self) -> typing.Optional[builtins.str]:
        '''(experimental) Normally the esbuild automatically discovers ``tsconfig.json`` files and reads their contents during a build.

        However, you can also configure a custom ``tsconfig.json`` file to use instead.

        This is similar to entry path, you need to provide path to your custom ``tsconfig.json``.

        This can be useful if you need to do multiple builds of the same code with different settings.

        :default: - automatically discovered by ``esbuild``

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "tsconfig""path/custom.tsconfig.json"
        '''
        result = self._values.get("tsconfig")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BundlingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_lambda_nodejs.ICommandHooks")
class ICommandHooks(typing_extensions.Protocol):
    '''(experimental) Command hooks.

    These commands will run in the environment in which bundling occurs: inside
    the container for Docker bundling or on the host OS for local bundling.

    Commands are chained with ``&&``.

    :stability: experimental

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            # Copy a file from the input directory to the output directory
            # to include it in the bundled asset
            after_bundling(input_dir, string, output_dir, string)string[]return [f"cp {inputDir}/my-binary.node {outputDir}"]
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_ICommandHooksProxy"]:
        return _ICommandHooksProxy

    @jsii.member(jsii_name="afterBundling")
    def after_bundling(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        '''(experimental) Returns commands to run after bundling.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="beforeBundling")
    def before_bundling(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        '''(experimental) Returns commands to run before bundling.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="beforeInstall")
    def before_install(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        '''(experimental) Returns commands to run before installing node modules.

        This hook only runs when node modules are installed.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -

        :stability: experimental
        '''
        ...


class _ICommandHooksProxy:
    '''(experimental) Command hooks.

    These commands will run in the environment in which bundling occurs: inside
    the container for Docker bundling or on the host OS for local bundling.

    Commands are chained with ``&&``.

    :stability: experimental

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            # Copy a file from the input directory to the output directory
            # to include it in the bundled asset
            after_bundling(input_dir, string, output_dir, string)string[]return [f"cp {inputDir}/my-binary.node {outputDir}"]
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_lambda_nodejs.ICommandHooks"

    @jsii.member(jsii_name="afterBundling")
    def after_bundling(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        '''(experimental) Returns commands to run after bundling.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "afterBundling", [input_dir, output_dir]))

    @jsii.member(jsii_name="beforeBundling")
    def before_bundling(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        '''(experimental) Returns commands to run before bundling.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "beforeBundling", [input_dir, output_dir]))

    @jsii.member(jsii_name="beforeInstall")
    def before_install(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        '''(experimental) Returns commands to run before installing node modules.

        This hook only runs when node modules are installed.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "beforeInstall", [input_dir, output_dir]))


@jsii.enum(jsii_type="monocdk.aws_lambda_nodejs.LogLevel")
class LogLevel(enum.Enum):
    '''(experimental) Log level for esbuild.

    :stability: experimental
    '''

    INFO = "INFO"
    '''(experimental) Show everything.

    :stability: experimental
    '''
    WARNING = "WARNING"
    '''(experimental) Show warnings and errors.

    :stability: experimental
    '''
    ERROR = "ERROR"
    '''(experimental) Show errors only.

    :stability: experimental
    '''
    SILENT = "SILENT"
    '''(experimental) Show nothing.

    :stability: experimental
    '''


class NodejsFunction(
    _Function_40b20aa5,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_nodejs.NodejsFunction",
):
    '''(experimental) A Node.js Lambda function bundled using esbuild.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        aws_sdk_connection_reuse: typing.Optional[builtins.bool] = None,
        bundling: typing.Optional[BundlingOptions] = None,
        deps_lock_file_path: typing.Optional[builtins.str] = None,
        entry: typing.Optional[builtins.str] = None,
        handler: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[_Runtime_932d369a] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        allow_public_subnet: typing.Optional[builtins.bool] = None,
        code_signing_config: typing.Optional[_ICodeSigningConfig_5d77bccf] = None,
        current_version_options: typing.Optional[_VersionOptions_085bb455] = None,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment_encryption: typing.Optional[_IKey_36930160] = None,
        events: typing.Optional[typing.List[_IEventSource_7914870e]] = None,
        filesystem: typing.Optional[_FileSystem_17be1f4c] = None,
        function_name: typing.Optional[builtins.str] = None,
        initial_policy: typing.Optional[typing.List[_PolicyStatement_296fe8a3]] = None,
        layers: typing.Optional[typing.List[_ILayerVersion_b2b86380]] = None,
        log_retention: typing.Optional[_RetentionDays_6c560d31] = None,
        log_retention_retry_options: typing.Optional[_LogRetentionRetryOptions_7acc40ab] = None,
        log_retention_role: typing.Optional[_IRole_59af6f50] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        profiling: typing.Optional[builtins.bool] = None,
        profiling_group: typing.Optional[_IProfilingGroup_418eb20c] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]] = None,
        timeout: typing.Optional[_Duration_070aa057] = None,
        tracing: typing.Optional[_Tracing_b7f4a8b6] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_1284e62c] = None,
        max_event_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IDestination_7f253ff1] = None,
        on_success: typing.Optional[_IDestination_7f253ff1] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param aws_sdk_connection_reuse: (experimental) Whether to automatically reuse TCP connections when working with the AWS SDK for JavaScript. This sets the ``AWS_NODEJS_CONNECTION_REUSE_ENABLED`` environment variable to ``1``. Default: true
        :param bundling: (experimental) Bundling options. Default: - use default bundling options: no minify, no sourcemap, all modules are bundled.
        :param deps_lock_file_path: (experimental) The path to the dependencies lock file (``yarn.lock`` or ``package-lock.json``). This will be used as the source for the volume mounted in the Docker container. Modules specified in ``nodeModules`` will be installed using the right installer (``npm`` or ``yarn``) along with this lock file. Default: - the path is found by walking up parent directories searching for a ``yarn.lock`` or ``package-lock.json`` file
        :param entry: (experimental) Path to the entry file (JavaScript or TypeScript). Default: - Derived from the name of the defining file and the construct's id. If the ``NodejsFunction`` is defined in ``stack.ts`` with ``my-handler`` as id (``new NodejsFunction(this, 'my-handler')``), the construct will look at ``stack.my-handler.ts`` and ``stack.my-handler.js``.
        :param handler: (experimental) The name of the exported handler in the entry file. Default: handler
        :param runtime: (experimental) The runtime environment. Only runtimes of the Node.js family are supported. Default: - ``NODEJS_14_X`` if ``process.versions.node`` >= '14.0.0', ``NODEJS_12_X`` otherwise.
        :param allow_all_outbound: (experimental) Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param allow_public_subnet: (experimental) Lambda Functions in a public subnet can NOT access the internet. Use this property to acknowledge this limitation and still place the function in a public subnet. Default: false
        :param code_signing_config: (experimental) Code signing config associated with this function. Default: - Not Sign the Code
        :param current_version_options: (experimental) Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: (experimental) The SQS queue to use if DLQ is enabled. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: (experimental) Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param description: (experimental) A description of the function. Default: - No description.
        :param environment: (experimental) Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param environment_encryption: (experimental) The AWS KMS key that's used to encrypt your function's environment variables. Default: - AWS Lambda creates and uses an AWS managed customer master key (CMK).
        :param events: (experimental) Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param filesystem: (experimental) The filesystem configuration for the lambda function. Default: - will not mount any filesystem
        :param function_name: (experimental) A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: (experimental) Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param layers: (experimental) A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by multiple functions. Default: - No layers.
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: (experimental) When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: (experimental) The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: (experimental) The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param profiling: (experimental) Enable profiling. Default: - No profiling.
        :param profiling_group: (experimental) Profiling Group. Default: - A new profiling group will be created if ``profiling`` is set.
        :param reserved_concurrent_executions: (experimental) The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: (experimental) Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param security_group: (deprecated) What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead. Only used if 'vpc' is supplied. Use securityGroups property instead. Function constructor will throw an error if both are specified. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroups prop, a dedicated security group will be created for this function.
        :param security_groups: (experimental) The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: (experimental) The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: (experimental) Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: (experimental) VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. Default: - Function is not placed within a VPC.
        :param vpc_subnets: (experimental) Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Note: internet access for Lambdas requires a NAT gateway, so picking Public subnets is not allowed. Default: - the Vpc default strategy if not specified
        :param max_event_age: (experimental) The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: (experimental) The destination for failed invocations. Default: - no destination
        :param on_success: (experimental) The destination for successful invocations. Default: - no destination
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        :stability: experimental
        '''
        props = NodejsFunctionProps(
            aws_sdk_connection_reuse=aws_sdk_connection_reuse,
            bundling=bundling,
            deps_lock_file_path=deps_lock_file_path,
            entry=entry,
            handler=handler,
            runtime=runtime,
            allow_all_outbound=allow_all_outbound,
            allow_public_subnet=allow_public_subnet,
            code_signing_config=code_signing_config,
            current_version_options=current_version_options,
            dead_letter_queue=dead_letter_queue,
            dead_letter_queue_enabled=dead_letter_queue_enabled,
            description=description,
            environment=environment,
            environment_encryption=environment_encryption,
            events=events,
            filesystem=filesystem,
            function_name=function_name,
            initial_policy=initial_policy,
            layers=layers,
            log_retention=log_retention,
            log_retention_retry_options=log_retention_retry_options,
            log_retention_role=log_retention_role,
            memory_size=memory_size,
            profiling=profiling,
            profiling_group=profiling_group,
            reserved_concurrent_executions=reserved_concurrent_executions,
            role=role,
            security_group=security_group,
            security_groups=security_groups,
            timeout=timeout,
            tracing=tracing,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
            max_event_age=max_event_age,
            on_failure=on_failure,
            on_success=on_success,
            retry_attempts=retry_attempts,
        )

        jsii.create(NodejsFunction, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_nodejs.NodejsFunctionProps",
    jsii_struct_bases=[_FunctionOptions_dc75a392],
    name_mapping={
        "max_event_age": "maxEventAge",
        "on_failure": "onFailure",
        "on_success": "onSuccess",
        "retry_attempts": "retryAttempts",
        "allow_all_outbound": "allowAllOutbound",
        "allow_public_subnet": "allowPublicSubnet",
        "code_signing_config": "codeSigningConfig",
        "current_version_options": "currentVersionOptions",
        "dead_letter_queue": "deadLetterQueue",
        "dead_letter_queue_enabled": "deadLetterQueueEnabled",
        "description": "description",
        "environment": "environment",
        "environment_encryption": "environmentEncryption",
        "events": "events",
        "filesystem": "filesystem",
        "function_name": "functionName",
        "initial_policy": "initialPolicy",
        "layers": "layers",
        "log_retention": "logRetention",
        "log_retention_retry_options": "logRetentionRetryOptions",
        "log_retention_role": "logRetentionRole",
        "memory_size": "memorySize",
        "profiling": "profiling",
        "profiling_group": "profilingGroup",
        "reserved_concurrent_executions": "reservedConcurrentExecutions",
        "role": "role",
        "security_group": "securityGroup",
        "security_groups": "securityGroups",
        "timeout": "timeout",
        "tracing": "tracing",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "aws_sdk_connection_reuse": "awsSdkConnectionReuse",
        "bundling": "bundling",
        "deps_lock_file_path": "depsLockFilePath",
        "entry": "entry",
        "handler": "handler",
        "runtime": "runtime",
    },
)
class NodejsFunctionProps(_FunctionOptions_dc75a392):
    def __init__(
        self,
        *,
        max_event_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IDestination_7f253ff1] = None,
        on_success: typing.Optional[_IDestination_7f253ff1] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        allow_public_subnet: typing.Optional[builtins.bool] = None,
        code_signing_config: typing.Optional[_ICodeSigningConfig_5d77bccf] = None,
        current_version_options: typing.Optional[_VersionOptions_085bb455] = None,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment_encryption: typing.Optional[_IKey_36930160] = None,
        events: typing.Optional[typing.List[_IEventSource_7914870e]] = None,
        filesystem: typing.Optional[_FileSystem_17be1f4c] = None,
        function_name: typing.Optional[builtins.str] = None,
        initial_policy: typing.Optional[typing.List[_PolicyStatement_296fe8a3]] = None,
        layers: typing.Optional[typing.List[_ILayerVersion_b2b86380]] = None,
        log_retention: typing.Optional[_RetentionDays_6c560d31] = None,
        log_retention_retry_options: typing.Optional[_LogRetentionRetryOptions_7acc40ab] = None,
        log_retention_role: typing.Optional[_IRole_59af6f50] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        profiling: typing.Optional[builtins.bool] = None,
        profiling_group: typing.Optional[_IProfilingGroup_418eb20c] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]] = None,
        timeout: typing.Optional[_Duration_070aa057] = None,
        tracing: typing.Optional[_Tracing_b7f4a8b6] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_1284e62c] = None,
        aws_sdk_connection_reuse: typing.Optional[builtins.bool] = None,
        bundling: typing.Optional[BundlingOptions] = None,
        deps_lock_file_path: typing.Optional[builtins.str] = None,
        entry: typing.Optional[builtins.str] = None,
        handler: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[_Runtime_932d369a] = None,
    ) -> None:
        '''(experimental) Properties for a NodejsFunction.

        :param max_event_age: (experimental) The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: (experimental) The destination for failed invocations. Default: - no destination
        :param on_success: (experimental) The destination for successful invocations. Default: - no destination
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2
        :param allow_all_outbound: (experimental) Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param allow_public_subnet: (experimental) Lambda Functions in a public subnet can NOT access the internet. Use this property to acknowledge this limitation and still place the function in a public subnet. Default: false
        :param code_signing_config: (experimental) Code signing config associated with this function. Default: - Not Sign the Code
        :param current_version_options: (experimental) Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: (experimental) The SQS queue to use if DLQ is enabled. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: (experimental) Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param description: (experimental) A description of the function. Default: - No description.
        :param environment: (experimental) Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param environment_encryption: (experimental) The AWS KMS key that's used to encrypt your function's environment variables. Default: - AWS Lambda creates and uses an AWS managed customer master key (CMK).
        :param events: (experimental) Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param filesystem: (experimental) The filesystem configuration for the lambda function. Default: - will not mount any filesystem
        :param function_name: (experimental) A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: (experimental) Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param layers: (experimental) A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by multiple functions. Default: - No layers.
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: (experimental) When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: (experimental) The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: (experimental) The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param profiling: (experimental) Enable profiling. Default: - No profiling.
        :param profiling_group: (experimental) Profiling Group. Default: - A new profiling group will be created if ``profiling`` is set.
        :param reserved_concurrent_executions: (experimental) The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: (experimental) Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param security_group: (deprecated) What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead. Only used if 'vpc' is supplied. Use securityGroups property instead. Function constructor will throw an error if both are specified. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroups prop, a dedicated security group will be created for this function.
        :param security_groups: (experimental) The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: (experimental) The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: (experimental) Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: (experimental) VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. Default: - Function is not placed within a VPC.
        :param vpc_subnets: (experimental) Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Note: internet access for Lambdas requires a NAT gateway, so picking Public subnets is not allowed. Default: - the Vpc default strategy if not specified
        :param aws_sdk_connection_reuse: (experimental) Whether to automatically reuse TCP connections when working with the AWS SDK for JavaScript. This sets the ``AWS_NODEJS_CONNECTION_REUSE_ENABLED`` environment variable to ``1``. Default: true
        :param bundling: (experimental) Bundling options. Default: - use default bundling options: no minify, no sourcemap, all modules are bundled.
        :param deps_lock_file_path: (experimental) The path to the dependencies lock file (``yarn.lock`` or ``package-lock.json``). This will be used as the source for the volume mounted in the Docker container. Modules specified in ``nodeModules`` will be installed using the right installer (``npm`` or ``yarn``) along with this lock file. Default: - the path is found by walking up parent directories searching for a ``yarn.lock`` or ``package-lock.json`` file
        :param entry: (experimental) Path to the entry file (JavaScript or TypeScript). Default: - Derived from the name of the defining file and the construct's id. If the ``NodejsFunction`` is defined in ``stack.ts`` with ``my-handler`` as id (``new NodejsFunction(this, 'my-handler')``), the construct will look at ``stack.my-handler.ts`` and ``stack.my-handler.js``.
        :param handler: (experimental) The name of the exported handler in the entry file. Default: handler
        :param runtime: (experimental) The runtime environment. Only runtimes of the Node.js family are supported. Default: - ``NODEJS_14_X`` if ``process.versions.node`` >= '14.0.0', ``NODEJS_12_X`` otherwise.

        :stability: experimental
        '''
        if isinstance(current_version_options, dict):
            current_version_options = _VersionOptions_085bb455(**current_version_options)
        if isinstance(log_retention_retry_options, dict):
            log_retention_retry_options = _LogRetentionRetryOptions_7acc40ab(**log_retention_retry_options)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_1284e62c(**vpc_subnets)
        if isinstance(bundling, dict):
            bundling = BundlingOptions(**bundling)
        self._values: typing.Dict[str, typing.Any] = {}
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if on_success is not None:
            self._values["on_success"] = on_success
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if allow_all_outbound is not None:
            self._values["allow_all_outbound"] = allow_all_outbound
        if allow_public_subnet is not None:
            self._values["allow_public_subnet"] = allow_public_subnet
        if code_signing_config is not None:
            self._values["code_signing_config"] = code_signing_config
        if current_version_options is not None:
            self._values["current_version_options"] = current_version_options
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if dead_letter_queue_enabled is not None:
            self._values["dead_letter_queue_enabled"] = dead_letter_queue_enabled
        if description is not None:
            self._values["description"] = description
        if environment is not None:
            self._values["environment"] = environment
        if environment_encryption is not None:
            self._values["environment_encryption"] = environment_encryption
        if events is not None:
            self._values["events"] = events
        if filesystem is not None:
            self._values["filesystem"] = filesystem
        if function_name is not None:
            self._values["function_name"] = function_name
        if initial_policy is not None:
            self._values["initial_policy"] = initial_policy
        if layers is not None:
            self._values["layers"] = layers
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if log_retention_retry_options is not None:
            self._values["log_retention_retry_options"] = log_retention_retry_options
        if log_retention_role is not None:
            self._values["log_retention_role"] = log_retention_role
        if memory_size is not None:
            self._values["memory_size"] = memory_size
        if profiling is not None:
            self._values["profiling"] = profiling
        if profiling_group is not None:
            self._values["profiling_group"] = profiling_group
        if reserved_concurrent_executions is not None:
            self._values["reserved_concurrent_executions"] = reserved_concurrent_executions
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if timeout is not None:
            self._values["timeout"] = timeout
        if tracing is not None:
            self._values["tracing"] = tracing
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if aws_sdk_connection_reuse is not None:
            self._values["aws_sdk_connection_reuse"] = aws_sdk_connection_reuse
        if bundling is not None:
            self._values["bundling"] = bundling
        if deps_lock_file_path is not None:
            self._values["deps_lock_file_path"] = deps_lock_file_path
        if entry is not None:
            self._values["entry"] = entry
        if handler is not None:
            self._values["handler"] = handler
        if runtime is not None:
            self._values["runtime"] = runtime

    @builtins.property
    def max_event_age(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum age of a request that Lambda sends to a function for processing.

        Minimum: 60 seconds
        Maximum: 6 hours

        :default: Duration.hours(6)

        :stability: experimental
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def on_failure(self) -> typing.Optional[_IDestination_7f253ff1]:
        '''(experimental) The destination for failed invocations.

        :default: - no destination

        :stability: experimental
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional[_IDestination_7f253ff1], result)

    @builtins.property
    def on_success(self) -> typing.Optional[_IDestination_7f253ff1]:
        '''(experimental) The destination for successful invocations.

        :default: - no destination

        :stability: experimental
        '''
        result = self._values.get("on_success")
        return typing.cast(typing.Optional[_IDestination_7f253ff1], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of times to retry when the function returns an error.

        Minimum: 0
        Maximum: 2

        :default: 2

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to allow the Lambda to send all network traffic.

        If set to false, you must individually add traffic rules to allow the
        Lambda to connect to network targets.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("allow_all_outbound")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_public_subnet(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Lambda Functions in a public subnet can NOT access the internet.

        Use this property to acknowledge this limitation and still place the function in a public subnet.

        :default: false

        :see: https://stackoverflow.com/questions/52992085/why-cant-an-aws-lambda-function-inside-a-public-subnet-in-a-vpc-connect-to-the/52994841#52994841
        :stability: experimental
        '''
        result = self._values.get("allow_public_subnet")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def code_signing_config(self) -> typing.Optional[_ICodeSigningConfig_5d77bccf]:
        '''(experimental) Code signing config associated with this function.

        :default: - Not Sign the Code

        :stability: experimental
        '''
        result = self._values.get("code_signing_config")
        return typing.cast(typing.Optional[_ICodeSigningConfig_5d77bccf], result)

    @builtins.property
    def current_version_options(self) -> typing.Optional[_VersionOptions_085bb455]:
        '''(experimental) Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method.

        :default: - default options as described in ``VersionOptions``

        :stability: experimental
        '''
        result = self._values.get("current_version_options")
        return typing.cast(typing.Optional[_VersionOptions_085bb455], result)

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_45a01ab4]:
        '''(experimental) The SQS queue to use if DLQ is enabled.

        :default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_45a01ab4], result)

    @builtins.property
    def dead_letter_queue_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enabled DLQ.

        If ``deadLetterQueue`` is undefined,
        an SQS queue with default options will be defined for your Function.

        :default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the function.

        :default: - No description.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Key-value pairs that Lambda caches and makes available for your Lambda functions.

        Use environment variables to apply configuration changes, such
        as test and production environment configurations, without changing your
        Lambda function source code.

        :default: - No environment variables.

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment_encryption(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) The AWS KMS key that's used to encrypt your function's environment variables.

        :default: - AWS Lambda creates and uses an AWS managed customer master key (CMK).

        :stability: experimental
        '''
        result = self._values.get("environment_encryption")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def events(self) -> typing.Optional[typing.List[_IEventSource_7914870e]]:
        '''(experimental) Event sources for this function.

        You can also add event sources using ``addEventSource``.

        :default: - No event sources.

        :stability: experimental
        '''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.List[_IEventSource_7914870e]], result)

    @builtins.property
    def filesystem(self) -> typing.Optional[_FileSystem_17be1f4c]:
        '''(experimental) The filesystem configuration for the lambda function.

        :default: - will not mount any filesystem

        :stability: experimental
        '''
        result = self._values.get("filesystem")
        return typing.cast(typing.Optional[_FileSystem_17be1f4c], result)

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the function.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that
        ID for the function's name. For more information, see Name Type.

        :stability: experimental
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_policy(self) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        '''(experimental) Initial policy statements to add to the created Lambda Role.

        You can call ``addToRolePolicy`` to the created lambda to add statements post creation.

        :default: - No policy statements are added to the created Lambda role.

        :stability: experimental
        '''
        result = self._values.get("initial_policy")
        return typing.cast(typing.Optional[typing.List[_PolicyStatement_296fe8a3]], result)

    @builtins.property
    def layers(self) -> typing.Optional[typing.List[_ILayerVersion_b2b86380]]:
        '''(experimental) A list of layers to add to the function's execution environment.

        You can configure your Lambda function to pull in
        additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies
        that can be used by multiple functions.

        :default: - No layers.

        :stability: experimental
        '''
        result = self._values.get("layers")
        return typing.cast(typing.Optional[typing.List[_ILayerVersion_b2b86380]], result)

    @builtins.property
    def log_retention(self) -> typing.Optional[_RetentionDays_6c560d31]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.INFINITE

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_RetentionDays_6c560d31], result)

    @builtins.property
    def log_retention_retry_options(
        self,
    ) -> typing.Optional[_LogRetentionRetryOptions_7acc40ab]:
        '''(experimental) When log retention is specified, a custom resource attempts to create the CloudWatch log group.

        These options control the retry policy when interacting with CloudWatch APIs.

        :default: - Default AWS SDK retry options.

        :stability: experimental
        '''
        result = self._values.get("log_retention_retry_options")
        return typing.cast(typing.Optional[_LogRetentionRetryOptions_7acc40ab], result)

    @builtins.property
    def log_retention_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        :default: - A new role is created.

        :stability: experimental
        '''
        result = self._values.get("log_retention_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The amount of memory, in MB, that is allocated to your Lambda function.

        Lambda uses this value to proportionally allocate the amount of CPU
        power. For more information, see Resource Model in the AWS Lambda
        Developer Guide.

        :default: 128

        :stability: experimental
        '''
        result = self._values.get("memory_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def profiling(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable profiling.

        :default: - No profiling.

        :see: https://docs.aws.amazon.com/codeguru/latest/profiler-ug/setting-up-lambda.html
        :stability: experimental
        '''
        result = self._values.get("profiling")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def profiling_group(self) -> typing.Optional[_IProfilingGroup_418eb20c]:
        '''(experimental) Profiling Group.

        :default: - A new profiling group will be created if ``profiling`` is set.

        :see: https://docs.aws.amazon.com/codeguru/latest/profiler-ug/setting-up-lambda.html
        :stability: experimental
        '''
        result = self._values.get("profiling_group")
        return typing.cast(typing.Optional[_IProfilingGroup_418eb20c], result)

    @builtins.property
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum of concurrent executions you want to reserve for the function.

        :default: - No specific limit - account limit.

        :see: https://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html
        :stability: experimental
        '''
        result = self._values.get("reserved_concurrent_executions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) Lambda execution role.

        This is the role that will be assumed by the function upon execution.
        It controls the permissions that the function will have. The Role must
        be assumable by the 'lambda.amazonaws.com' service principal.

        The default Role automatically has permissions granted for Lambda execution. If you
        provide a Role, you must add the relevant AWS managed policies yourself.

        The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and
        "service-role/AWSLambdaVPCAccessExecutionRole".

        :default:

        - A unique role will be generated for this lambda function.
        Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_cdbba9d3]:
        '''(deprecated) What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead.

        Only used if 'vpc' is supplied.

        Use securityGroups property instead.
        Function constructor will throw an error if both are specified.

        :default:

        - If the function is placed within a VPC and a security group is
        not specified, either by this or securityGroups prop, a dedicated security
        group will be created for this function.

        :deprecated: - This property is deprecated, use securityGroups instead

        :stability: deprecated
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_ISecurityGroup_cdbba9d3], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]]:
        '''(experimental) The list of security groups to associate with the Lambda's network interfaces.

        Only used if 'vpc' is supplied.

        :default:

        - If the function is placed within a VPC and a security group is
        not specified, either by this or securityGroup prop, a dedicated security
        group will be created for this function.

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The function execution time (in seconds) after which Lambda terminates the function.

        Because the execution time affects cost, set this value
        based on the function's expected execution time.

        :default: Duration.seconds(3)

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def tracing(self) -> typing.Optional[_Tracing_b7f4a8b6]:
        '''(experimental) Enable AWS X-Ray Tracing for Lambda Function.

        :default: Tracing.Disabled

        :stability: experimental
        '''
        result = self._values.get("tracing")
        return typing.cast(typing.Optional[_Tracing_b7f4a8b6], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(experimental) VPC network to place Lambda network interfaces.

        Specify this if the Lambda function needs to access resources in a VPC.

        :default: - Function is not placed within a VPC.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) Where to place the network interfaces within the VPC.

        Only used if 'vpc' is supplied. Note: internet access for Lambdas
        requires a NAT gateway, so picking Public subnets is not allowed.

        :default: - the Vpc default strategy if not specified

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    @builtins.property
    def aws_sdk_connection_reuse(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to automatically reuse TCP connections when working with the AWS SDK for JavaScript.

        This sets the ``AWS_NODEJS_CONNECTION_REUSE_ENABLED`` environment variable
        to ``1``.

        :default: true

        :see: https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/node-reusing-connections.html
        :stability: experimental
        '''
        result = self._values.get("aws_sdk_connection_reuse")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def bundling(self) -> typing.Optional[BundlingOptions]:
        '''(experimental) Bundling options.

        :default:

        - use default bundling options: no minify, no sourcemap, all
        modules are bundled.

        :stability: experimental
        '''
        result = self._values.get("bundling")
        return typing.cast(typing.Optional[BundlingOptions], result)

    @builtins.property
    def deps_lock_file_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path to the dependencies lock file (``yarn.lock`` or ``package-lock.json``).

        This will be used as the source for the volume mounted in the Docker
        container.

        Modules specified in ``nodeModules`` will be installed using the right
        installer (``npm`` or ``yarn``) along with this lock file.

        :default:

        - the path is found by walking up parent directories searching for
        a ``yarn.lock`` or ``package-lock.json`` file

        :stability: experimental
        '''
        result = self._values.get("deps_lock_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entry(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to the entry file (JavaScript or TypeScript).

        :default:

        - Derived from the name of the defining file and the construct's id.
        If the ``NodejsFunction`` is defined in ``stack.ts`` with ``my-handler`` as id
        (``new NodejsFunction(this, 'my-handler')``), the construct will look at ``stack.my-handler.ts``
        and ``stack.my-handler.js``.

        :stability: experimental
        '''
        result = self._values.get("entry")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def handler(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the exported handler in the entry file.

        :default: handler

        :stability: experimental
        '''
        result = self._values.get("handler")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime(self) -> typing.Optional[_Runtime_932d369a]:
        '''(experimental) The runtime environment.

        Only runtimes of the Node.js family are
        supported.

        :default:

        - ``NODEJS_14_X`` if ``process.versions.node`` >= '14.0.0',
        ``NODEJS_12_X`` otherwise.

        :stability: experimental
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[_Runtime_932d369a], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NodejsFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BundlingOptions",
    "ICommandHooks",
    "LogLevel",
    "NodejsFunction",
    "NodejsFunctionProps",
]

publication.publish()
