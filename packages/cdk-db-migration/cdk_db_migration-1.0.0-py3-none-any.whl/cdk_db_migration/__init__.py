'''
# CDK DB Migration

[![Source](https://img.shields.io/badge/Source-GitHub-blue?logo=github)](https://github.com/udondan/cdk-db-migration)
[![Test](https://github.com/udondan/cdk-db-migration/workflows/Test/badge.svg)](https://github.com/udondan/cdk-db-migration/actions?query=workflow%3ATest)
[![GitHub](https://img.shields.io/github/license/udondan/cdk-db-migration)](https://github.com/udondan/cdk-db-migration/blob/master/LICENSE)
[![Docs](https://img.shields.io/badge/awscdk.io-cdk--db--migration-orange)](https://awscdk.io/packages/cdk-db-migration@1.0.0)

[![npm package](https://img.shields.io/npm/v/cdk-db-migration?color=brightgreen)](https://www.npmjs.com/package/cdk-db-migration)
[![PyPI package](https://img.shields.io/pypi/v/cdk-db-migration?color=brightgreen)](https://pypi.org/project/cdk-db-migration/)
[![NuGet package](https://img.shields.io/nuget/v/CDK.DB.Migration?color=brightgreen)](https://www.nuget.org/packages/CDK.DB.Migration/)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
[![npm](https://img.shields.io/npm/dt/cdk-db-migration?label=npm&color=blueviolet)](https://www.npmjs.com/package/cdk-db-migration)
[![PyPI](https://img.shields.io/pypi/dm/cdk-db-migration?label=pypi&color=blueviolet)](https://pypi.org/project/cdk-db-migration/)
[![NuGet](https://img.shields.io/nuget/dt/CDK.DB.Migration?label=nuget&color=blueviolet)](https://www.nuget.org/packages/CDK.DB.Migration/)

[AWS CDK](https://aws.amazon.com/cdk/) L3 construct for managing DB migrations. Currently implemented DBMS:

* Athena

I created this construct because [CloudFormations Glue Table](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-table.html) doesn't support `TBLPROPERTIES`. I needed an alternative to create a table. Since creating a table is a DB migration, I created a migration construct instead of a simple table construct, which would be hard to impossible to update.

## Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk_db_migration as Migration

m1 = Migration.Athena(self, "M1",
    up="CREATE EXTERNAL TABLE foo ...;",
    down="DROP TABLE foo;"
)

m2 = Migration.Athena(self, "M2",
    depends_on=m1,
    up="ALTER TABLE foo ...;",
    down="ALTER TABLE foo ...;"
)
```

Every migration requires a query for *up* and *down* migrations. `up` is executed when the migration is created. `down` is executed when the migration is destroyed.

A full example including creating bucket, database, workgroup and permissions can be found in the [test directory](https://github.com/udondan/cdk-db-migration/blob/master/test/lib/index.ts).

## Notes

**No modifications**: The construct will refuse to update any existing migration, because this is not how migrations work. Add another migration or first delete the migration, then add the modified statement.

**Dependencies**: Since migrations (might) depend on one another, make sure to set dependencies where required. In CDK you usually add dependencies like this:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
m1 = Migration.Athena(self, "M1", ...)
m2 = Migration.Athena(self, "M2", ...)
m2.node.add_dependency(m1)
```

Since dependencies are a very common pattern for migrations, a migration also accepts dependencies directly:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
m1 = Migration.Athena(self, "M1", ...)
m2 = Migration.Athena(self, "M2",
    depends_on=m1, ...
)
```

**Permissions**: The Lambda function which runs the migrations, is not authorized to do anything at all, because the required permissions are very custom to the use case (database, workgroup, S3 location, KMS etc). Instead of giving too wide permissions by default, none are given at all. The construct exposes the IAM role and you need to grant the required permissions.

**Best solution for your use case?**: While the construct is capable of managing the state of a database over time, have a good thought if you really want to do this with CDK/CloudFormation. CloudFormation can ony handle up to 500 resources in a stack, so this (minus all the other resources in your stack) is going to be your hard limit of migrations. Migrations are executed by a Lambda function. Since the maximum execution time of a Lambda function is 15 minutes, migrations cannot exceed this limit.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.core


class Base(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-db-migration.Base",
):
    '''Defines a new DB Migration.'''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        down: builtins.str,
        up: builtins.str,
        depends_on: typing.Optional[typing.Union[aws_cdk.core.Construct, typing.List[aws_cdk.core.Construct]]] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[aws_cdk.core.Environment] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[aws_cdk.core.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Defines a new DB Migration.

        :param scope: -
        :param id: -
        :param down: Migration to apply, when the resource is deleted.
        :param up: Migration to apply, when the resource is created.
        :param depends_on: One or more cdk constructs the migration depends on.
        :param timeout: Timeout of the lambda function, which is used to run the migrations. Default: - 30 seconds
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        '''
        props = Props(
            down=down,
            up=up,
            depends_on=depends_on,
            timeout=timeout,
            analytics_reporting=analytics_reporting,
            description=description,
            env=env,
            stack_name=stack_name,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        jsii.create(Base, self, [scope, id, props])

    @jsii.member(jsii_name="makeProperties")
    def _make_properties(
        self,
        *,
        down: builtins.str,
        up: builtins.str,
        depends_on: typing.Optional[typing.Union[aws_cdk.core.Construct, typing.List[aws_cdk.core.Construct]]] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[aws_cdk.core.Environment] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[aws_cdk.core.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> "LambdaProps":
        '''
        :param down: Migration to apply, when the resource is deleted.
        :param up: Migration to apply, when the resource is created.
        :param depends_on: One or more cdk constructs the migration depends on.
        :param timeout: Timeout of the lambda function, which is used to run the migrations. Default: - 30 seconds
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        '''
        _ = Props(
            down=down,
            up=up,
            depends_on=depends_on,
            timeout=timeout,
            analytics_reporting=analytics_reporting,
            description=description,
            env=env,
            stack_name=stack_name,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        return typing.cast("LambdaProps", jsii.invoke(self, "makeProperties", [_]))

    @jsii.member(jsii_name="makeType")
    def _make_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "makeType", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="down")
    def down(self) -> builtins.str:
        '''Migration to apply, when the resource is deleted.'''
        return typing.cast(builtins.str, jsii.get(self, "down"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> aws_cdk.aws_lambda.IFunction:
        '''The lambda function which backs the custom resource.'''
        return typing.cast(aws_cdk.aws_lambda.IFunction, jsii.get(self, "lambda"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.Role:
        '''The IAM role, used by the lambda function which backs the custom resource.'''
        return typing.cast(aws_cdk.aws_iam.Role, jsii.get(self, "role"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="up")
    def up(self) -> builtins.str:
        '''Migration to apply, when the resource is deleted.'''
        return typing.cast(builtins.str, jsii.get(self, "up"))


@jsii.data_type(
    jsii_type="cdk-db-migration.LambdaProps",
    jsii_struct_bases=[],
    name_mapping={},
)
class LambdaProps:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-db-migration.Props",
    jsii_struct_bases=[aws_cdk.core.StackProps],
    name_mapping={
        "analytics_reporting": "analyticsReporting",
        "description": "description",
        "env": "env",
        "stack_name": "stackName",
        "synthesizer": "synthesizer",
        "tags": "tags",
        "termination_protection": "terminationProtection",
        "down": "down",
        "up": "up",
        "depends_on": "dependsOn",
        "timeout": "timeout",
    },
)
class Props(aws_cdk.core.StackProps):
    def __init__(
        self,
        *,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[aws_cdk.core.Environment] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[aws_cdk.core.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
        down: builtins.str,
        up: builtins.str,
        depends_on: typing.Optional[typing.Union[aws_cdk.core.Construct, typing.List[aws_cdk.core.Construct]]] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        '''Manages Database Migration.

        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        :param down: Migration to apply, when the resource is deleted.
        :param up: Migration to apply, when the resource is created.
        :param depends_on: One or more cdk constructs the migration depends on.
        :param timeout: Timeout of the lambda function, which is used to run the migrations. Default: - 30 seconds
        '''
        if isinstance(env, dict):
            env = aws_cdk.core.Environment(**env)
        self._values: typing.Dict[str, typing.Any] = {
            "down": down,
            "up": up,
        }
        if analytics_reporting is not None:
            self._values["analytics_reporting"] = analytics_reporting
        if description is not None:
            self._values["description"] = description
        if env is not None:
            self._values["env"] = env
        if stack_name is not None:
            self._values["stack_name"] = stack_name
        if synthesizer is not None:
            self._values["synthesizer"] = synthesizer
        if tags is not None:
            self._values["tags"] = tags
        if termination_protection is not None:
            self._values["termination_protection"] = termination_protection
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def analytics_reporting(self) -> typing.Optional[builtins.bool]:
        '''Include runtime versioning information in this Stack.

        :default:

        ``analyticsReporting`` setting of containing ``App``, or value of
        'aws:cdk:version-reporting' context key
        '''
        result = self._values.get("analytics_reporting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the stack.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[aws_cdk.core.Environment]:
        '''The AWS environment (account/region) where this stack will be deployed.

        Set the ``region``/``account`` fields of ``env`` to either a concrete value to
        select the indicated environment (recommended for production stacks), or to
        the values of environment variables
        ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment
        depend on the AWS credentials/configuration that the CDK CLI is executed
        under (recommended for development stacks).

        If the ``Stack`` is instantiated inside a ``Stage``, any undefined
        ``region``/``account`` fields from ``env`` will default to the same field on the
        encompassing ``Stage``, if configured there.

        If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the
        Stack will be considered "*environment-agnostic*"". Environment-agnostic
        stacks can be deployed to any environment but may not be able to take
        advantage of all features of the CDK. For example, they will not be able to
        use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not
        automatically translate Service Principals to the right format based on the
        environment's AWS partition, and other such enhancements.

        :default:

        - The environment of the containing ``Stage`` if available,
        otherwise create the stack will be environment-agnostic.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            # Use a concrete account and region to deploy this stack to:
            # `.account` and `.region` will simply return these values.
            Stack(app, "Stack1",
                env={
                    "account": "123456789012",
                    "region": "us-east-1"
                }
            )
            
            # Use the CLI's current credentials to determine the target environment:
            # `.account` and `.region` will reflect the account+region the CLI
            # is configured to use (based on the user CLI credentials)
            Stack(app, "Stack2",
                env={
                    "account": process.env.CDK_DEFAULT_ACCOUNT,
                    "region": process.env.CDK_DEFAULT_REGION
                }
            )
            
            # Define multiple stacks stage associated with an environment
            my_stage = Stage(app, "MyStage",
                env={
                    "account": "123456789012",
                    "region": "us-east-1"
                }
            )
            
            # both of these stacks will use the stage's account/region:
            # `.account` and `.region` will resolve to the concrete values as above
            MyStack(my_stage, "Stack1")
            YourStack(my_stage, "Stack2")
            
            # Define an environment-agnostic stack:
            # `.account` and `.region` will resolve to `{ "Ref": "AWS::AccountId" }` and `{ "Ref": "AWS::Region" }` respectively.
            # which will only resolve to actual values by CloudFormation during deployment.
            MyStack(app, "Stack1")
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[aws_cdk.core.Environment], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''Name to deploy the stack with.

        :default: - Derived from construct path.
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def synthesizer(self) -> typing.Optional[aws_cdk.core.IStackSynthesizer]:
        '''Synthesis method to use while deploying this stack.

        :default:

        - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag
        is set, ``LegacyStackSynthesizer`` otherwise.
        '''
        result = self._values.get("synthesizer")
        return typing.cast(typing.Optional[aws_cdk.core.IStackSynthesizer], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Stack tags that will be applied to all the taggable resources and the stack itself.

        :default: {}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def termination_protection(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable termination protection for this stack.

        :default: false
        '''
        result = self._values.get("termination_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def down(self) -> builtins.str:
        '''Migration to apply, when the resource is deleted.'''
        result = self._values.get("down")
        assert result is not None, "Required property 'down' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def up(self) -> builtins.str:
        '''Migration to apply, when the resource is created.'''
        result = self._values.get("up")
        assert result is not None, "Required property 'up' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.Construct, typing.List[aws_cdk.core.Construct]]]:
        '''One or more cdk constructs the migration depends on.'''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.Construct, typing.List[aws_cdk.core.Construct]]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''Timeout of the lambda function, which is used to run the migrations.

        :default: - 30 seconds
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Athena(Base, metaclass=jsii.JSIIMeta, jsii_type="cdk-db-migration.Athena"):
    '''Defines a new DB Migration for Athena.'''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        work_group: typing.Optional[builtins.str] = None,
        down: builtins.str,
        up: builtins.str,
        depends_on: typing.Optional[typing.Union[aws_cdk.core.Construct, typing.List[aws_cdk.core.Construct]]] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[aws_cdk.core.Environment] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[aws_cdk.core.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Defines a new DB Migration.

        :param scope: -
        :param id: -
        :param work_group: Athena WorkGroup to run the migration in. Default: - primary
        :param down: Migration to apply, when the resource is deleted.
        :param up: Migration to apply, when the resource is created.
        :param depends_on: One or more cdk constructs the migration depends on.
        :param timeout: Timeout of the lambda function, which is used to run the migrations. Default: - 30 seconds
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        '''
        props = AthenaProps(
            work_group=work_group,
            down=down,
            up=up,
            depends_on=depends_on,
            timeout=timeout,
            analytics_reporting=analytics_reporting,
            description=description,
            env=env,
            stack_name=stack_name,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        jsii.create(Athena, self, [scope, id, props])

    @jsii.member(jsii_name="makeProperties")
    def _make_properties(
        self,
        *,
        down: builtins.str,
        up: builtins.str,
        depends_on: typing.Optional[typing.Union[aws_cdk.core.Construct, typing.List[aws_cdk.core.Construct]]] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[aws_cdk.core.Environment] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[aws_cdk.core.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> LambdaProps:
        '''
        :param down: Migration to apply, when the resource is deleted.
        :param up: Migration to apply, when the resource is created.
        :param depends_on: One or more cdk constructs the migration depends on.
        :param timeout: Timeout of the lambda function, which is used to run the migrations. Default: - 30 seconds
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        '''
        props = Props(
            down=down,
            up=up,
            depends_on=depends_on,
            timeout=timeout,
            analytics_reporting=analytics_reporting,
            description=description,
            env=env,
            stack_name=stack_name,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        return typing.cast(LambdaProps, jsii.invoke(self, "makeProperties", [props]))

    @jsii.member(jsii_name="makeType")
    def _make_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "makeType", []))


@jsii.data_type(
    jsii_type="cdk-db-migration.AthenaProps",
    jsii_struct_bases=[Props],
    name_mapping={
        "analytics_reporting": "analyticsReporting",
        "description": "description",
        "env": "env",
        "stack_name": "stackName",
        "synthesizer": "synthesizer",
        "tags": "tags",
        "termination_protection": "terminationProtection",
        "down": "down",
        "up": "up",
        "depends_on": "dependsOn",
        "timeout": "timeout",
        "work_group": "workGroup",
    },
)
class AthenaProps(Props):
    def __init__(
        self,
        *,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[aws_cdk.core.Environment] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[aws_cdk.core.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
        down: builtins.str,
        up: builtins.str,
        depends_on: typing.Optional[typing.Union[aws_cdk.core.Construct, typing.List[aws_cdk.core.Construct]]] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        work_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Props for Athena Migrations.

        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        :param down: Migration to apply, when the resource is deleted.
        :param up: Migration to apply, when the resource is created.
        :param depends_on: One or more cdk constructs the migration depends on.
        :param timeout: Timeout of the lambda function, which is used to run the migrations. Default: - 30 seconds
        :param work_group: Athena WorkGroup to run the migration in. Default: - primary
        '''
        if isinstance(env, dict):
            env = aws_cdk.core.Environment(**env)
        self._values: typing.Dict[str, typing.Any] = {
            "down": down,
            "up": up,
        }
        if analytics_reporting is not None:
            self._values["analytics_reporting"] = analytics_reporting
        if description is not None:
            self._values["description"] = description
        if env is not None:
            self._values["env"] = env
        if stack_name is not None:
            self._values["stack_name"] = stack_name
        if synthesizer is not None:
            self._values["synthesizer"] = synthesizer
        if tags is not None:
            self._values["tags"] = tags
        if termination_protection is not None:
            self._values["termination_protection"] = termination_protection
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if timeout is not None:
            self._values["timeout"] = timeout
        if work_group is not None:
            self._values["work_group"] = work_group

    @builtins.property
    def analytics_reporting(self) -> typing.Optional[builtins.bool]:
        '''Include runtime versioning information in this Stack.

        :default:

        ``analyticsReporting`` setting of containing ``App``, or value of
        'aws:cdk:version-reporting' context key
        '''
        result = self._values.get("analytics_reporting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the stack.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[aws_cdk.core.Environment]:
        '''The AWS environment (account/region) where this stack will be deployed.

        Set the ``region``/``account`` fields of ``env`` to either a concrete value to
        select the indicated environment (recommended for production stacks), or to
        the values of environment variables
        ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment
        depend on the AWS credentials/configuration that the CDK CLI is executed
        under (recommended for development stacks).

        If the ``Stack`` is instantiated inside a ``Stage``, any undefined
        ``region``/``account`` fields from ``env`` will default to the same field on the
        encompassing ``Stage``, if configured there.

        If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the
        Stack will be considered "*environment-agnostic*"". Environment-agnostic
        stacks can be deployed to any environment but may not be able to take
        advantage of all features of the CDK. For example, they will not be able to
        use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not
        automatically translate Service Principals to the right format based on the
        environment's AWS partition, and other such enhancements.

        :default:

        - The environment of the containing ``Stage`` if available,
        otherwise create the stack will be environment-agnostic.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            # Use a concrete account and region to deploy this stack to:
            # `.account` and `.region` will simply return these values.
            Stack(app, "Stack1",
                env={
                    "account": "123456789012",
                    "region": "us-east-1"
                }
            )
            
            # Use the CLI's current credentials to determine the target environment:
            # `.account` and `.region` will reflect the account+region the CLI
            # is configured to use (based on the user CLI credentials)
            Stack(app, "Stack2",
                env={
                    "account": process.env.CDK_DEFAULT_ACCOUNT,
                    "region": process.env.CDK_DEFAULT_REGION
                }
            )
            
            # Define multiple stacks stage associated with an environment
            my_stage = Stage(app, "MyStage",
                env={
                    "account": "123456789012",
                    "region": "us-east-1"
                }
            )
            
            # both of these stacks will use the stage's account/region:
            # `.account` and `.region` will resolve to the concrete values as above
            MyStack(my_stage, "Stack1")
            YourStack(my_stage, "Stack2")
            
            # Define an environment-agnostic stack:
            # `.account` and `.region` will resolve to `{ "Ref": "AWS::AccountId" }` and `{ "Ref": "AWS::Region" }` respectively.
            # which will only resolve to actual values by CloudFormation during deployment.
            MyStack(app, "Stack1")
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[aws_cdk.core.Environment], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''Name to deploy the stack with.

        :default: - Derived from construct path.
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def synthesizer(self) -> typing.Optional[aws_cdk.core.IStackSynthesizer]:
        '''Synthesis method to use while deploying this stack.

        :default:

        - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag
        is set, ``LegacyStackSynthesizer`` otherwise.
        '''
        result = self._values.get("synthesizer")
        return typing.cast(typing.Optional[aws_cdk.core.IStackSynthesizer], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Stack tags that will be applied to all the taggable resources and the stack itself.

        :default: {}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def termination_protection(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable termination protection for this stack.

        :default: false
        '''
        result = self._values.get("termination_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def down(self) -> builtins.str:
        '''Migration to apply, when the resource is deleted.'''
        result = self._values.get("down")
        assert result is not None, "Required property 'down' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def up(self) -> builtins.str:
        '''Migration to apply, when the resource is created.'''
        result = self._values.get("up")
        assert result is not None, "Required property 'up' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.Construct, typing.List[aws_cdk.core.Construct]]]:
        '''One or more cdk constructs the migration depends on.'''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.Construct, typing.List[aws_cdk.core.Construct]]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''Timeout of the lambda function, which is used to run the migrations.

        :default: - 30 seconds
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    @builtins.property
    def work_group(self) -> typing.Optional[builtins.str]:
        '''Athena WorkGroup to run the migration in.

        :default: - primary
        '''
        result = self._values.get("work_group")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AthenaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Athena",
    "AthenaProps",
    "Base",
    "LambdaProps",
    "Props",
]

publication.publish()
