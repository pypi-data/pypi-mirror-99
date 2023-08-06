# Kinesis Analytics Flink

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This package provides constructs for creating Kinesis Analytics Flink
applications. To learn more about using using managed Flink applications, see
the [AWS developer
guide](https://docs.aws.amazon.com/kinesisanalytics/latest/java/what-is.html).

## Creating Flink Applications

To create a new Flink application, use the `Application` construct:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import path as path
import aws_cdk.core as core
import ...lib as flink

app = core.App()
stack = core.Stack(app, "FlinkAppTest")

flink.Application(stack, "App",
    code=flink.ApplicationCode.from_asset(path.join(__dirname, "code-asset")),
    runtime=flink.Runtime.FLINK_1_11
)

app.synth()
```

The `code` property can use `fromAsset` as shown above to reference a local jar
file in s3 or `fromBucket` to reference a file in s3.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import path as path
import aws_cdk.aws_s3_assets as assets
import aws_cdk.core as core
import ...lib as flink

app = core.App()
stack = core.Stack(app, "FlinkAppCodeFromBucketTest")

asset = assets.Asset(stack, "CodeAsset",
    path=path.join(__dirname, "code-asset")
)
bucket = asset.bucket
file_key = asset.s3_object_key

flink.Application(stack, "App",
    code=flink.ApplicationCode.from_bucket(bucket, file_key),
    runtime=flink.Runtime.FLINK_1_11
)

app.synth()
```

The `propertyGroups` property provides a way of passing arbitrary runtime
properties to your Flink application. You can use the
aws-kinesisanalytics-runtime library to [retrieve these
properties](https://docs.aws.amazon.com/kinesisanalytics/latest/java/how-properties.html#how-properties-access).

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_kinesisanalytics_flink as flink

flink_app = flink.Application(self, "Application",
    # ...
    property_groups=PropertyGroups(
        FlinkApplicationProperties={
            "input_stream_name": "my-input-kinesis-stream",
            "output_stream_name": "my-output-kinesis-stream"
        }
    )
)
```

Flink applications also have specific configuration for passing parameters
when the Flink job starts. These include parameters for checkpointing,
snapshotting, monitoring, and parallelism.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_logs as logs

flink_app = flink.Application(self, "Application",
    code=flink.ApplicationCode.from_bucket(bucket, "my-app.jar"),
    runtime=file.Runtime.FLINK_1_11,
    checkpointing_enabled=True, # default is true
    checkpoint_interval=cdk.Duration.seconds(30), # default is 1 minute
    min_pauses_between_checkpoints=cdk.Duration.seconds(10), # default is 5 seconds
    log_level=flink.LogLevel.ERROR, # default is INFO
    metrics_level=flink.MetricsLevel.PARALLELISM, # default is APPLICATION
    auto_scaling_enabled=False, # default is true
    parallelism=32, # default is 1
    parallelism_per_kpu=2, # default is 1
    snapshots_enabled=False, # default is true
    log_group=logs.LogGroup(self, "LogGroup")
)
```
