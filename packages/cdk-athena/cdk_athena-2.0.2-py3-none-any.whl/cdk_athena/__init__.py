'''
# CDK Athena WorkGroup

[![Source](https://img.shields.io/badge/Source-GitHub-blue?logo=github)](https://github.com/udondan/cdk-athena)
[![Test](https://github.com/udondan/cdk-athena/workflows/Test/badge.svg)](https://github.com/udondan/cdk-athena/actions?query=workflow%3ATest)
[![GitHub](https://img.shields.io/github/license/udondan/cdk-athena)](https://github.com/udondan/cdk-athena/blob/master/LICENSE)
[![Docs](https://img.shields.io/badge/awscdk.io-cdk--athena-orange)](https://awscdk.io/packages/cdk-athena@2.0.0)

[![npm package](https://img.shields.io/npm/v/cdk-athena?color=brightgreen)](https://www.npmjs.com/package/cdk-athena)
[![PyPI package](https://img.shields.io/pypi/v/cdk-athena?color=brightgreen)](https://pypi.org/project/cdk-athena/)
[![NuGet package](https://img.shields.io/nuget/v/CDK.Athena?color=brightgreen)](https://www.nuget.org/packages/CDK.Athena/)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
[![npm](https://img.shields.io/npm/dt/cdk-athena?label=npm&color=blueviolet)](https://www.npmjs.com/package/cdk-athena)
[![PyPI](https://img.shields.io/pypi/dm/cdk-athena?label=pypi&color=blueviolet)](https://pypi.org/project/cdk-athena/)
[![NuGet](https://img.shields.io/nuget/dt/CDK.Athena?label=nuget&color=blueviolet)](https://www.nuget.org/packages/CDK.Athena/)

[AWS CDK](https://aws.amazon.com/cdk/) L3 construct for managing Athena [WorkGroups](https://docs.aws.amazon.com/athena/latest/ug/manage-queries-control-costs-with-workgroups.html) and named queries.

Because I couldn't get [@aws-cdk/aws-athena.CfnWorkGroup](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-athena.CfnWorkGroup.html) to work and [@aws-cdk/custom-resources.AwsCustomResource](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_custom-resources.AwsCustomResource.html) has no support for tags.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
workgroup = WorkGroup(self, "WorkGroup",
    name="TheName", # required
    desc="Some description",
    publish_cloud_watch_metrics_enabled=True,
    enforce_work_group_configuration=True,
    requester_pays_enabled=True,
    bytes_scanned_cutoff_per_query=11000000,
    result_configuration={
        "output_location": "s3://some-bucket/prefix",
        "encryption_configuration": {
            "encryption_option": EncryptionOption.SSE_S3
        }
    }
)

query = NamedQuery(self, "a-query",
    name="A Test Query",
    database="audit",
    desc="This is the description",
    query_string="""
        SELECT
          count(*) AS assumed,
          split(useridentity.principalid, ':')[2] AS user,
          resources[1].arn AS role
        FROM cloudtrail_logs
        WHERE
          eventname='AssumeRole' AND
          useridentity.principalid is NOT NULL AND
          useridentity.principalid LIKE '%@%'
        GROUP BY
          split(useridentity.principalid,':')[2],
          resources[1].arn
      """,
    work_group=workgroup
)

cdk.Tag.add(workgroup, "HelloTag", "ok")

cdk.CfnOutput(self, "WorkGroupArn",
    value=workgroup.arn
)

cdk.CfnOutput(self, "WorkGroupName",
    value=workgroup.name
)

cdk.CfnOutput(self, "QueryId",
    value=query.id
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

from ._jsii import *

import aws_cdk.aws_lambda
import aws_cdk.core


@jsii.data_type(
    jsii_type="cdk-athena.EncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"encryption_option": "encryptionOption", "kms_key": "kmsKey"},
)
class EncryptionConfiguration:
    def __init__(
        self,
        *,
        encryption_option: "EncryptionOption",
        kms_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encryption_option: Indicates whether Amazon S3 server-side encryption with Amazon S3-managed keys (``SSE-S3``), server-side encryption with KMS-managed keys (``SSE-KMS``), or client-side encryption with KMS-managed keys (``CSE-KMS``) is used. If a query runs in a workgroup and the workgroup overrides client-side settings, then the workgroup's setting for encryption is used. It specifies whether query results must be encrypted, for all queries that run in this workgroup. Possible values include: - ``SSE_S3`` - ``SSE_KMS`` - ``CSE_KMS``
        :param kms_key: For ``SSE-KMS`` and ``CSE-KMS``, this is the KMS key ARN or ID.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "encryption_option": encryption_option,
        }
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def encryption_option(self) -> "EncryptionOption":
        '''Indicates whether Amazon S3 server-side encryption with Amazon S3-managed keys (``SSE-S3``), server-side encryption with KMS-managed keys (``SSE-KMS``), or client-side encryption with KMS-managed keys (``CSE-KMS``) is used.

        If a query runs in a workgroup and the workgroup overrides client-side settings, then the workgroup's setting for encryption is used. It specifies whether query results must be encrypted, for all queries that run in this workgroup.

        Possible values include:

        - ``SSE_S3``
        - ``SSE_KMS``
        - ``CSE_KMS``
        '''
        result = self._values.get("encryption_option")
        assert result is not None, "Required property 'encryption_option' is missing"
        return typing.cast("EncryptionOption", result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''For ``SSE-KMS`` and ``CSE-KMS``, this is the KMS key ARN or ID.'''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-athena.EncryptionOption")
class EncryptionOption(enum.Enum):
    SSE_S3 = "SSE_S3"
    SSE_KMS = "SSE_KMS"
    CSE_KMS = "CSE_KMS"


class NamedQuery(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-athena.NamedQuery",
):
    '''An Athena NamedQuery.'''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        database: builtins.str,
        name: builtins.str,
        query_string: builtins.str,
        desc: typing.Optional[builtins.str] = None,
        work_group: typing.Optional[typing.Union[builtins.str, "WorkGroup"]] = None,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[aws_cdk.core.Environment] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[aws_cdk.core.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Defines a new Athena NamedQuery.

        :param scope: -
        :param id: -
        :param database: The database to which the query belongs.
        :param name: The query name.
        :param query_string: The contents of the query with all query statements.
        :param desc: The query description.
        :param work_group: The workgroup in which the named query is being created.
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        '''
        props = NamedQueryProps(
            database=database,
            name=name,
            query_string=query_string,
            desc=desc,
            work_group=work_group,
            analytics_reporting=analytics_reporting,
            description=description,
            env=env,
            stack_name=stack_name,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        jsii.create(NamedQuery, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''The unique ID of the query.'''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> aws_cdk.aws_lambda.IFunction:
        '''The lambda function that is created.'''
        return typing.cast(aws_cdk.aws_lambda.IFunction, jsii.get(self, "lambda"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''Name of the query.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="cdk-athena.NamedQueryProps",
    jsii_struct_bases=[aws_cdk.core.StackProps],
    name_mapping={
        "analytics_reporting": "analyticsReporting",
        "description": "description",
        "env": "env",
        "stack_name": "stackName",
        "synthesizer": "synthesizer",
        "tags": "tags",
        "termination_protection": "terminationProtection",
        "database": "database",
        "name": "name",
        "query_string": "queryString",
        "desc": "desc",
        "work_group": "workGroup",
    },
)
class NamedQueryProps(aws_cdk.core.StackProps):
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
        database: builtins.str,
        name: builtins.str,
        query_string: builtins.str,
        desc: typing.Optional[builtins.str] = None,
        work_group: typing.Optional[typing.Union[builtins.str, "WorkGroup"]] = None,
    ) -> None:
        '''Definition of the Athena NamedQuery.

        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        :param database: The database to which the query belongs.
        :param name: The query name.
        :param query_string: The contents of the query with all query statements.
        :param desc: The query description.
        :param work_group: The workgroup in which the named query is being created.
        '''
        if isinstance(env, dict):
            env = aws_cdk.core.Environment(**env)
        self._values: typing.Dict[str, typing.Any] = {
            "database": database,
            "name": name,
            "query_string": query_string,
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
        if desc is not None:
            self._values["desc"] = desc
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
    def database(self) -> builtins.str:
        '''The database to which the query belongs.'''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The query name.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query_string(self) -> builtins.str:
        '''The contents of the query with all query statements.'''
        result = self._values.get("query_string")
        assert result is not None, "Required property 'query_string' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def desc(self) -> typing.Optional[builtins.str]:
        '''The query description.'''
        result = self._values.get("desc")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def work_group(self) -> typing.Optional[typing.Union[builtins.str, "WorkGroup"]]:
        '''The workgroup in which the named query is being created.'''
        result = self._values.get("work_group")
        return typing.cast(typing.Optional[typing.Union[builtins.str, "WorkGroup"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NamedQueryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-athena.ResultConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_configuration": "encryptionConfiguration",
        "output_location": "outputLocation",
    },
)
class ResultConfiguration:
    def __init__(
        self,
        *,
        encryption_configuration: typing.Optional[EncryptionConfiguration] = None,
        output_location: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param encryption_configuration: If query results are encrypted in Amazon S3, indicates the encryption option used (for example, ``SSE-KMS`` or ``CSE-KMS``) and key information. This is a client-side setting. If workgroup settings override client-side settings, then the query uses the encryption configuration that is specified for the workgroup, and also uses the location for storing query results specified in the workgroup.
        :param output_location: The location in Amazon S3 where your query results are stored, such as ``s3://path/to/query/bucket/``. To run the query, you must specify the query results location using one of the ways: either for individual queries using either this setting (client-side), or in the workgroup, using WorkGroupConfiguration. If none of them is set, Athena issues an error that no output location is provided. For more information, see `Query results <https://docs.aws.amazon.com/athena/latest/ug/querying.html>`_. If workgroup settings override client-side settings, then the query uses the settings specified for the workgroup.
        '''
        if isinstance(encryption_configuration, dict):
            encryption_configuration = EncryptionConfiguration(**encryption_configuration)
        self._values: typing.Dict[str, typing.Any] = {}
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if output_location is not None:
            self._values["output_location"] = output_location

    @builtins.property
    def encryption_configuration(self) -> typing.Optional[EncryptionConfiguration]:
        '''If query results are encrypted in Amazon S3, indicates the encryption option used (for example, ``SSE-KMS`` or ``CSE-KMS``) and key information.

        This is a client-side setting. If workgroup settings override client-side settings, then the query uses the encryption configuration that is specified for the workgroup, and also uses the location for storing query results specified in the workgroup.
        '''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional[EncryptionConfiguration], result)

    @builtins.property
    def output_location(self) -> typing.Optional[builtins.str]:
        '''The location in Amazon S3 where your query results are stored, such as ``s3://path/to/query/bucket/``.

        To run the query, you must specify the query results location using one of the ways: either for individual queries using either this setting (client-side), or in the workgroup, using WorkGroupConfiguration. If none of them is set, Athena issues an error that no output location is provided. For more information, see `Query results <https://docs.aws.amazon.com/athena/latest/ug/querying.html>`_. If workgroup settings override client-side settings, then the query uses the settings specified for the workgroup.
        '''
        result = self._values.get("output_location")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResultConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.core.ITaggable)
class WorkGroup(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-athena.WorkGroup",
):
    '''An Athena WorkGroup.'''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        bytes_scanned_cutoff_per_query: typing.Optional[jsii.Number] = None,
        desc: typing.Optional[builtins.str] = None,
        enforce_work_group_configuration: typing.Optional[builtins.bool] = None,
        publish_cloud_watch_metrics_enabled: typing.Optional[builtins.bool] = None,
        requester_pays_enabled: typing.Optional[builtins.bool] = None,
        result_configuration: typing.Optional[ResultConfiguration] = None,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[aws_cdk.core.Environment] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[aws_cdk.core.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Defines a new Athena WorkGroup.

        :param scope: -
        :param id: -
        :param name: Name of the WorkGroup. **This cannot be changed! The name is the primary and only identifier of the WorkGroup. Changing the name will destroy the WorkGroup and create a new one with the new name.**
        :param bytes_scanned_cutoff_per_query: The upper data usage limit (cutoff) for the amount of bytes a single query in a workgroup is allowed to scan. Minimum value of 10000000
        :param desc: Description of the WorkGroup.
        :param enforce_work_group_configuration: If set to ``true``, the settings for the workgroup override client-side settings. If set to ``false``, client-side settings are used. For more information, see `Workgroup Settings Override Client-Side Settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_. Default: false
        :param publish_cloud_watch_metrics_enabled: Indicates that the Amazon CloudWatch metrics are enabled for the workgroup. Default: false
        :param requester_pays_enabled: If set to ``true``, allows members assigned to a workgroup to specify Amazon S3 Requester Pays buckets in queries. If set to ``false``, workgroup members cannot query data from Requester Pays buckets, and queries that retrieve data from Requester Pays buckets cause an error. The default is ``false``. For more information about Requester Pays buckets, see `Requester Pays Buckets <https://docs.aws.amazon.com/AmazonS3/latest/dev/RequesterPaysBuckets.html>`_ in the *Amazon Simple Storage Service Developer Guide*. Default: false
        :param result_configuration: The configuration for the workgroup, which includes the location in Amazon S3 where query results are stored and the encryption option, if any, used for query results. To run the query, you must specify the query results location using one of the ways: either in the workgroup using this setting, or for individual queries (client-side), using ResultConfiguration$OutputLocation. If none of them is set, Athena issues an error that no output location is provided. For more information, see `Query results <https://docs.aws.amazon.com/athena/latest/ug/querying.html>`_.
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        '''
        props = WorkGroupProps(
            name=name,
            bytes_scanned_cutoff_per_query=bytes_scanned_cutoff_per_query,
            desc=desc,
            enforce_work_group_configuration=enforce_work_group_configuration,
            publish_cloud_watch_metrics_enabled=publish_cloud_watch_metrics_enabled,
            requester_pays_enabled=requester_pays_enabled,
            result_configuration=result_configuration,
            analytics_reporting=analytics_reporting,
            description=description,
            env=env,
            stack_name=stack_name,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        jsii.create(WorkGroup, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''ARN of the WorkGroup.'''
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> aws_cdk.aws_lambda.IFunction:
        '''The lambda function that is created.'''
        return typing.cast(aws_cdk.aws_lambda.IFunction, jsii.get(self, "lambda"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''Name of the WorkGroup.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''Resource tags.'''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))


@jsii.data_type(
    jsii_type="cdk-athena.WorkGroupProps",
    jsii_struct_bases=[aws_cdk.core.StackProps],
    name_mapping={
        "analytics_reporting": "analyticsReporting",
        "description": "description",
        "env": "env",
        "stack_name": "stackName",
        "synthesizer": "synthesizer",
        "tags": "tags",
        "termination_protection": "terminationProtection",
        "name": "name",
        "bytes_scanned_cutoff_per_query": "bytesScannedCutoffPerQuery",
        "desc": "desc",
        "enforce_work_group_configuration": "enforceWorkGroupConfiguration",
        "publish_cloud_watch_metrics_enabled": "publishCloudWatchMetricsEnabled",
        "requester_pays_enabled": "requesterPaysEnabled",
        "result_configuration": "resultConfiguration",
    },
)
class WorkGroupProps(aws_cdk.core.StackProps):
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
        name: builtins.str,
        bytes_scanned_cutoff_per_query: typing.Optional[jsii.Number] = None,
        desc: typing.Optional[builtins.str] = None,
        enforce_work_group_configuration: typing.Optional[builtins.bool] = None,
        publish_cloud_watch_metrics_enabled: typing.Optional[builtins.bool] = None,
        requester_pays_enabled: typing.Optional[builtins.bool] = None,
        result_configuration: typing.Optional[ResultConfiguration] = None,
    ) -> None:
        '''Definition of the Athena WorkGroup.

        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        :param name: Name of the WorkGroup. **This cannot be changed! The name is the primary and only identifier of the WorkGroup. Changing the name will destroy the WorkGroup and create a new one with the new name.**
        :param bytes_scanned_cutoff_per_query: The upper data usage limit (cutoff) for the amount of bytes a single query in a workgroup is allowed to scan. Minimum value of 10000000
        :param desc: Description of the WorkGroup.
        :param enforce_work_group_configuration: If set to ``true``, the settings for the workgroup override client-side settings. If set to ``false``, client-side settings are used. For more information, see `Workgroup Settings Override Client-Side Settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_. Default: false
        :param publish_cloud_watch_metrics_enabled: Indicates that the Amazon CloudWatch metrics are enabled for the workgroup. Default: false
        :param requester_pays_enabled: If set to ``true``, allows members assigned to a workgroup to specify Amazon S3 Requester Pays buckets in queries. If set to ``false``, workgroup members cannot query data from Requester Pays buckets, and queries that retrieve data from Requester Pays buckets cause an error. The default is ``false``. For more information about Requester Pays buckets, see `Requester Pays Buckets <https://docs.aws.amazon.com/AmazonS3/latest/dev/RequesterPaysBuckets.html>`_ in the *Amazon Simple Storage Service Developer Guide*. Default: false
        :param result_configuration: The configuration for the workgroup, which includes the location in Amazon S3 where query results are stored and the encryption option, if any, used for query results. To run the query, you must specify the query results location using one of the ways: either in the workgroup using this setting, or for individual queries (client-side), using ResultConfiguration$OutputLocation. If none of them is set, Athena issues an error that no output location is provided. For more information, see `Query results <https://docs.aws.amazon.com/athena/latest/ug/querying.html>`_.
        '''
        if isinstance(env, dict):
            env = aws_cdk.core.Environment(**env)
        if isinstance(result_configuration, dict):
            result_configuration = ResultConfiguration(**result_configuration)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
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
        if bytes_scanned_cutoff_per_query is not None:
            self._values["bytes_scanned_cutoff_per_query"] = bytes_scanned_cutoff_per_query
        if desc is not None:
            self._values["desc"] = desc
        if enforce_work_group_configuration is not None:
            self._values["enforce_work_group_configuration"] = enforce_work_group_configuration
        if publish_cloud_watch_metrics_enabled is not None:
            self._values["publish_cloud_watch_metrics_enabled"] = publish_cloud_watch_metrics_enabled
        if requester_pays_enabled is not None:
            self._values["requester_pays_enabled"] = requester_pays_enabled
        if result_configuration is not None:
            self._values["result_configuration"] = result_configuration

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
    def name(self) -> builtins.str:
        '''Name of the WorkGroup.

        **This cannot be changed! The name is the primary  and only identifier of the WorkGroup. Changing the name will destroy the WorkGroup and create a new one with the new name.**
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bytes_scanned_cutoff_per_query(self) -> typing.Optional[jsii.Number]:
        '''The upper data usage limit (cutoff) for the amount of bytes a single query in a workgroup is allowed to scan.

        Minimum value of 10000000
        '''
        result = self._values.get("bytes_scanned_cutoff_per_query")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def desc(self) -> typing.Optional[builtins.str]:
        '''Description of the WorkGroup.'''
        result = self._values.get("desc")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce_work_group_configuration(self) -> typing.Optional[builtins.bool]:
        '''If set to ``true``, the settings for the workgroup override client-side settings.

        If set to ``false``, client-side settings are used. For more information, see `Workgroup Settings Override Client-Side Settings <https://docs.aws.amazon.com/athena/latest/ug/workgroups-settings-override.html>`_.

        :default: false
        '''
        result = self._values.get("enforce_work_group_configuration")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def publish_cloud_watch_metrics_enabled(self) -> typing.Optional[builtins.bool]:
        '''Indicates that the Amazon CloudWatch metrics are enabled for the workgroup.

        :default: false
        '''
        result = self._values.get("publish_cloud_watch_metrics_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def requester_pays_enabled(self) -> typing.Optional[builtins.bool]:
        '''If set to ``true``, allows members assigned to a workgroup to specify Amazon S3 Requester Pays buckets in queries.

        If set to ``false``, workgroup members cannot query data from Requester Pays buckets, and queries that retrieve data from Requester Pays buckets cause an error. The default is ``false``. For more information about Requester Pays buckets, see `Requester Pays Buckets <https://docs.aws.amazon.com/AmazonS3/latest/dev/RequesterPaysBuckets.html>`_ in the *Amazon Simple Storage Service Developer Guide*.

        :default: false
        '''
        result = self._values.get("requester_pays_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def result_configuration(self) -> typing.Optional[ResultConfiguration]:
        '''The configuration for the workgroup, which includes the location in Amazon S3 where query results are stored and the encryption option, if any, used for query results.

        To run the query, you must specify the query results location using one of the ways: either in the workgroup using this setting, or for individual queries (client-side), using ResultConfiguration$OutputLocation. If none of them is set, Athena issues an error that no output location is provided. For more information, see `Query results <https://docs.aws.amazon.com/athena/latest/ug/querying.html>`_.
        '''
        result = self._values.get("result_configuration")
        return typing.cast(typing.Optional[ResultConfiguration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "EncryptionConfiguration",
    "EncryptionOption",
    "NamedQuery",
    "NamedQueryProps",
    "ResultConfiguration",
    "WorkGroup",
    "WorkGroupProps",
]

publication.publish()
