'''
# aws-events-rule-sqs module

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> All classes are under active development and subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

| **Reference Documentation**:| <span style="font-weight: normal">https://docs.aws.amazon.com/solutions/latest/constructs/</span>|
|:-------------|:-------------|

<div style="height:8px"></div>

| **Language**     | **Package**        |
|:-------------|-----------------|
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_events_rule_sqs`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-events-rule-sqs`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.eventsrulesqs`|

This AWS Solutions Construct implements an AWS Events rule and an AWS SQS Queue.

Here is a minimal deployable pattern definition in Typescript:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Duration
import aws_cdk.aws_events as events
import aws_cdk.aws_iam as iam
from aws_solutions_constructs.aws_events_rule_sqs import EventsRuleToSqsProps, EventsRuleToSqs

props = EventsRuleToSqsProps(
    event_rule_props=RuleProps(
        schedule=events.Schedule.rate(Duration.minutes(5))
    )
)

construct_stack = EventsRuleToSqs(self, "test-construct", props)

# Grant yourself permissions to use the Customer Managed KMS Key
policy_statement = iam.PolicyStatement(
    actions=["kms:Encrypt", "kms:Decrypt"],
    effect=iam.Effect.ALLOW,
    principals=[iam.AccountRootPrincipal()],
    resources=["*"]
)

construct_stack.encryption_key.add_to_resource_policy(policy_statement)
```

## Initializer

```text
new EventsRuleToSqs(scope: Construct, id: string, props: EventsRuleToSqsProps);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`EventsRuleToSqsProps`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|eventRuleProps|[`events.RuleProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-events.RuleProps.html)|User provided eventRuleProps to override the defaults. |
|existingQueueObj?|[`sqs.Queue`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sqs.Queue.html)|An optional, existing SQS queue to be used instead of the default queue. If an existing queue is provided, the `queueProps` property will be ignored.|
|queueProps?|[`sqs.QueueProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sqs.QueueProps.html)|User provided props to override the default props for the SQS Queue. |
|enableQueuePurging?|`boolean`|Whether to grant additional permissions to the Lambda function enabling it to purge the SQS queue. Defaults to `false`.|
|deployDeadLetterQueue?|`boolean`|Whether to create a secondary queue to be used as a dead letter queue. Defaults to `true`.|
|deadLetterQueueProps?|[`sqs.QueueProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sqs.QueueProps.html)|Optional user-provided props to override the default props for the dead letter queue. Only used if the `deployDeadLetterQueue` property is set to true.|
|maxReceiveCount?|`number`|The number of times a message can be unsuccessfully dequeued before being moved to the dead letter queue. Defaults to `15`.|
|enableEncryptionWithCustomerManagedKey?|`boolean`|Use a KMS Key, either managed by this CDK app, or imported. If importing an encryption key, it must be specified in the encryptionKey property for this construct.|
|encryptionKey?|[`kms.Key`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kms.Key.html)|An optional, imported encryption key to encrypt the SQS queue.|
|encryptionKeyProps?|[`kms.KeyProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kms.KeyProps.html)|An optional, user provided properties to override the default properties for the KMS encryption key.|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|eventsRule|[`events.Rule`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-events.Rule.html)|Returns an instance of events.Rule created by the construct|
|sqsQueue|[`sqs.Queue`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sqs.Queue.html)|Returns an instance of sqs.Queue created by the construct|
|encryptionKey?|[`kms.Key`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kms.Key.html)|Returns an instance of kms Key used for the SQS queue.|
|deadLetterQueue?|[`sqs.Queue`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sqs.Queue.html)|Returns an instance of the dead-letter SQS queue created by the pattern.|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### Amazon CloudWatch Events Rule

* Grant least privilege permissions to CloudWatch Events to publish to the SQS Queue.

### Amazon SQS Queue

* Deploy SQS dead-letter queue for the source SQS Queue.
* Enable server-side encryption for source SQS Queue using Customer managed KMS Key.
* Enforce encryption of data in transit.

## Architecture

![Architecture Diagram](architecture.png)

---


© Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

import aws_cdk.aws_events
import aws_cdk.aws_kms
import aws_cdk.aws_sqs
import aws_cdk.core


class EventsRuleToSqs(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-solutions-constructs/aws-events-rule-sqs.EventsRuleToSqs",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        event_rule_props: aws_cdk.aws_events.RuleProps,
        dead_letter_queue_props: typing.Optional[aws_cdk.aws_sqs.QueueProps] = None,
        deploy_dead_letter_queue: typing.Optional[builtins.bool] = None,
        enable_encryption_with_customer_managed_key: typing.Optional[builtins.bool] = None,
        enable_queue_purging: typing.Optional[builtins.bool] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.Key] = None,
        encryption_key_props: typing.Optional[aws_cdk.aws_kms.KeyProps] = None,
        existing_queue_obj: typing.Optional[aws_cdk.aws_sqs.Queue] = None,
        max_receive_count: typing.Optional[jsii.Number] = None,
        queue_props: typing.Optional[aws_cdk.aws_sqs.QueueProps] = None,
    ) -> None:
        '''
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param event_rule_props: User provided eventRuleProps to override the defaults. Default: - None
        :param dead_letter_queue_props: Optional user provided properties for the dead letter queue. Default: - Default props are used
        :param deploy_dead_letter_queue: Whether to deploy a secondary queue to be used as a dead letter queue. Default: - true.
        :param enable_encryption_with_customer_managed_key: Use a KMS Key, either managed by this CDK app, or imported. If importing an encryption key, it must be specified in the encryptionKey property for this construct. Default: - true (encryption enabled, managed by this CDK app).
        :param enable_queue_purging: Whether to grant additional permissions to the Lambda function enabling it to purge the SQS queue. Default: - "false", disabled by default.
        :param encryption_key: An optional, imported encryption key to encrypt the SQS queue, and SNS Topic. Default: - not specified.
        :param encryption_key_props: Optional user-provided props to override the default props for the encryption key. Default: - Default props are used.
        :param existing_queue_obj: Existing instance of SQS queue object, if this is set then the queueProps is ignored. Default: - None
        :param max_receive_count: The number of times a message can be unsuccessfully dequeued before being moved to the dead-letter queue. Default: - required field if deployDeadLetterQueue=true.
        :param queue_props: User provided props to override the default props for the SQS queue. Default: - Default props are used

        :access: public
        :since: 1.62.0
        :summary: Constructs a new instance of the EventsRuleToSqs class.
        '''
        props = EventsRuleToSqsProps(
            event_rule_props=event_rule_props,
            dead_letter_queue_props=dead_letter_queue_props,
            deploy_dead_letter_queue=deploy_dead_letter_queue,
            enable_encryption_with_customer_managed_key=enable_encryption_with_customer_managed_key,
            enable_queue_purging=enable_queue_purging,
            encryption_key=encryption_key,
            encryption_key_props=encryption_key_props,
            existing_queue_obj=existing_queue_obj,
            max_receive_count=max_receive_count,
            queue_props=queue_props,
        )

        jsii.create(EventsRuleToSqs, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="eventsRule")
    def events_rule(self) -> aws_cdk.aws_events.Rule:
        return typing.cast(aws_cdk.aws_events.Rule, jsii.get(self, "eventsRule"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sqsQueue")
    def sqs_queue(self) -> aws_cdk.aws_sqs.Queue:
        return typing.cast(aws_cdk.aws_sqs.Queue, jsii.get(self, "sqsQueue"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deadLetterQueue")
    def dead_letter_queue(self) -> typing.Optional[aws_cdk.aws_sqs.DeadLetterQueue]:
        return typing.cast(typing.Optional[aws_cdk.aws_sqs.DeadLetterQueue], jsii.get(self, "deadLetterQueue"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        return typing.cast(typing.Optional[aws_cdk.aws_kms.IKey], jsii.get(self, "encryptionKey"))


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/aws-events-rule-sqs.EventsRuleToSqsProps",
    jsii_struct_bases=[],
    name_mapping={
        "event_rule_props": "eventRuleProps",
        "dead_letter_queue_props": "deadLetterQueueProps",
        "deploy_dead_letter_queue": "deployDeadLetterQueue",
        "enable_encryption_with_customer_managed_key": "enableEncryptionWithCustomerManagedKey",
        "enable_queue_purging": "enableQueuePurging",
        "encryption_key": "encryptionKey",
        "encryption_key_props": "encryptionKeyProps",
        "existing_queue_obj": "existingQueueObj",
        "max_receive_count": "maxReceiveCount",
        "queue_props": "queueProps",
    },
)
class EventsRuleToSqsProps:
    def __init__(
        self,
        *,
        event_rule_props: aws_cdk.aws_events.RuleProps,
        dead_letter_queue_props: typing.Optional[aws_cdk.aws_sqs.QueueProps] = None,
        deploy_dead_letter_queue: typing.Optional[builtins.bool] = None,
        enable_encryption_with_customer_managed_key: typing.Optional[builtins.bool] = None,
        enable_queue_purging: typing.Optional[builtins.bool] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.Key] = None,
        encryption_key_props: typing.Optional[aws_cdk.aws_kms.KeyProps] = None,
        existing_queue_obj: typing.Optional[aws_cdk.aws_sqs.Queue] = None,
        max_receive_count: typing.Optional[jsii.Number] = None,
        queue_props: typing.Optional[aws_cdk.aws_sqs.QueueProps] = None,
    ) -> None:
        '''
        :param event_rule_props: User provided eventRuleProps to override the defaults. Default: - None
        :param dead_letter_queue_props: Optional user provided properties for the dead letter queue. Default: - Default props are used
        :param deploy_dead_letter_queue: Whether to deploy a secondary queue to be used as a dead letter queue. Default: - true.
        :param enable_encryption_with_customer_managed_key: Use a KMS Key, either managed by this CDK app, or imported. If importing an encryption key, it must be specified in the encryptionKey property for this construct. Default: - true (encryption enabled, managed by this CDK app).
        :param enable_queue_purging: Whether to grant additional permissions to the Lambda function enabling it to purge the SQS queue. Default: - "false", disabled by default.
        :param encryption_key: An optional, imported encryption key to encrypt the SQS queue, and SNS Topic. Default: - not specified.
        :param encryption_key_props: Optional user-provided props to override the default props for the encryption key. Default: - Default props are used.
        :param existing_queue_obj: Existing instance of SQS queue object, if this is set then the queueProps is ignored. Default: - None
        :param max_receive_count: The number of times a message can be unsuccessfully dequeued before being moved to the dead-letter queue. Default: - required field if deployDeadLetterQueue=true.
        :param queue_props: User provided props to override the default props for the SQS queue. Default: - Default props are used

        :summary: The properties for the EventsRuleToSqs Construct
        '''
        if isinstance(event_rule_props, dict):
            event_rule_props = aws_cdk.aws_events.RuleProps(**event_rule_props)
        if isinstance(dead_letter_queue_props, dict):
            dead_letter_queue_props = aws_cdk.aws_sqs.QueueProps(**dead_letter_queue_props)
        if isinstance(encryption_key_props, dict):
            encryption_key_props = aws_cdk.aws_kms.KeyProps(**encryption_key_props)
        if isinstance(queue_props, dict):
            queue_props = aws_cdk.aws_sqs.QueueProps(**queue_props)
        self._values: typing.Dict[str, typing.Any] = {
            "event_rule_props": event_rule_props,
        }
        if dead_letter_queue_props is not None:
            self._values["dead_letter_queue_props"] = dead_letter_queue_props
        if deploy_dead_letter_queue is not None:
            self._values["deploy_dead_letter_queue"] = deploy_dead_letter_queue
        if enable_encryption_with_customer_managed_key is not None:
            self._values["enable_encryption_with_customer_managed_key"] = enable_encryption_with_customer_managed_key
        if enable_queue_purging is not None:
            self._values["enable_queue_purging"] = enable_queue_purging
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if encryption_key_props is not None:
            self._values["encryption_key_props"] = encryption_key_props
        if existing_queue_obj is not None:
            self._values["existing_queue_obj"] = existing_queue_obj
        if max_receive_count is not None:
            self._values["max_receive_count"] = max_receive_count
        if queue_props is not None:
            self._values["queue_props"] = queue_props

    @builtins.property
    def event_rule_props(self) -> aws_cdk.aws_events.RuleProps:
        '''User provided eventRuleProps to override the defaults.

        :default: - None
        '''
        result = self._values.get("event_rule_props")
        assert result is not None, "Required property 'event_rule_props' is missing"
        return typing.cast(aws_cdk.aws_events.RuleProps, result)

    @builtins.property
    def dead_letter_queue_props(self) -> typing.Optional[aws_cdk.aws_sqs.QueueProps]:
        '''Optional user provided properties for the dead letter queue.

        :default: - Default props are used
        '''
        result = self._values.get("dead_letter_queue_props")
        return typing.cast(typing.Optional[aws_cdk.aws_sqs.QueueProps], result)

    @builtins.property
    def deploy_dead_letter_queue(self) -> typing.Optional[builtins.bool]:
        '''Whether to deploy a secondary queue to be used as a dead letter queue.

        :default: - true.
        '''
        result = self._values.get("deploy_dead_letter_queue")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_encryption_with_customer_managed_key(
        self,
    ) -> typing.Optional[builtins.bool]:
        '''Use a KMS Key, either managed by this CDK app, or imported.

        If importing an encryption key, it must be specified in
        the encryptionKey property for this construct.

        :default: - true (encryption enabled, managed by this CDK app).
        '''
        result = self._values.get("enable_encryption_with_customer_managed_key")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_queue_purging(self) -> typing.Optional[builtins.bool]:
        '''Whether to grant additional permissions to the Lambda function enabling it to purge the SQS queue.

        :default: - "false", disabled by default.
        '''
        result = self._values.get("enable_queue_purging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.Key]:
        '''An optional, imported encryption key to encrypt the SQS queue, and SNS Topic.

        :default: - not specified.
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[aws_cdk.aws_kms.Key], result)

    @builtins.property
    def encryption_key_props(self) -> typing.Optional[aws_cdk.aws_kms.KeyProps]:
        '''Optional user-provided props to override the default props for the encryption key.

        :default: - Default props are used.
        '''
        result = self._values.get("encryption_key_props")
        return typing.cast(typing.Optional[aws_cdk.aws_kms.KeyProps], result)

    @builtins.property
    def existing_queue_obj(self) -> typing.Optional[aws_cdk.aws_sqs.Queue]:
        '''Existing instance of SQS queue object, if this is set then the queueProps is ignored.

        :default: - None
        '''
        result = self._values.get("existing_queue_obj")
        return typing.cast(typing.Optional[aws_cdk.aws_sqs.Queue], result)

    @builtins.property
    def max_receive_count(self) -> typing.Optional[jsii.Number]:
        '''The number of times a message can be unsuccessfully dequeued before being moved to the dead-letter queue.

        :default: - required field if deployDeadLetterQueue=true.
        '''
        result = self._values.get("max_receive_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def queue_props(self) -> typing.Optional[aws_cdk.aws_sqs.QueueProps]:
        '''User provided props to override the default props for the SQS queue.

        :default: - Default props are used
        '''
        result = self._values.get("queue_props")
        return typing.cast(typing.Optional[aws_cdk.aws_sqs.QueueProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventsRuleToSqsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "EventsRuleToSqs",
    "EventsRuleToSqsProps",
]

publication.publish()
