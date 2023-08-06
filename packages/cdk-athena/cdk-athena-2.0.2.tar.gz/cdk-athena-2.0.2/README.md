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
