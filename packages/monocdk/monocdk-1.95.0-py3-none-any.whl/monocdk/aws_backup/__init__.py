'''
# AWS Backup Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

AWS Backup is a fully managed backup service that makes it easy to centralize and automate the backup of data across AWS services in the cloud and on premises. Using AWS Backup, you can configure backup policies and monitor backup activity for your AWS resources in one place.

## Backup plan and selection

In AWS Backup, a *backup plan* is a policy expression that defines when and how you want to back up your AWS resources, such as Amazon DynamoDB tables or Amazon Elastic File System (Amazon EFS) file systems. You can assign resources to backup plans, and AWS Backup automatically backs up and retains backups for those resources according to the backup plan. You can create multiple backup plans if you have workloads with different backup requirements.

This module provides ready-made backup plans (similar to the console experience):

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_backup as backup

# Daily, weekly and monthly with 5 year retention
plan = backup.BackupPlan.daily_weekly_monthly5_year_retention(self, "Plan")
```

Assigning resources to a plan can be done with `addSelection()`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
plan.add_selection("Selection",
    resources=[
        backup.BackupResource.from_dynamo_db_table(my_table), # A DynamoDB table
        backup.BackupResource.from_tag("stage", "prod"), # All resources that are tagged stage=prod in the region/account
        backup.BackupResource.from_construct(my_cool_construct)
    ]
)
```

If not specified, a new IAM role with a managed policy for backup will be
created for the selection. The `BackupSelection` implements `IGrantable`.

To add rules to a plan, use `addRule()`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
plan.add_rule(BackupPlanRule(
    completion_window=Duration.hours(2),
    start_window=Duration.hours(1),
    schedule_expression=events.Schedule.cron(# Only cron expressions are supported
        day="15",
        hour="3",
        minute="30"),
    move_to_cold_storage_after=Duration.days(30)
))
```

Ready-made rules are also available:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
plan.add_rule(BackupPlanRule.daily())
plan.add_rule(BackupPlanRule.weekly())
```

By default a new [vault](#Backup-vault) is created when creating a plan.
It is also possible to specify a vault either at the plan level or at the
rule level.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
plan = backup.BackupPlan.daily35_day_retention(self, "Plan", my_vault)# Use `myVault` for all plan rules
plan.add_rule(BackupPlanRule.monthly1_year(other_vault))
```

## Backup vault

In AWS Backup, a *backup vault* is a container that you organize your backups in. You can use backup vaults to set the AWS Key Management Service (AWS KMS) encryption key that is used to encrypt backups in the backup vault and to control access to the backups in the backup vault. If you require different encryption keys or access policies for different groups of backups, you can optionally create multiple backup vaults.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
vault = BackupVault(stack, "Vault",
    encryption_key=my_key, # Custom encryption key
    notification_topic=my_topic
)
```

A vault has a default `RemovalPolicy` set to `RETAIN`. Note that removing a vault
that contains recovery points will fail.
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
    Construct as _Construct_e78e779f,
    Duration as _Duration_070aa057,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    RemovalPolicy as _RemovalPolicy_c97e7a20,
    Resource as _Resource_abff4495,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_dynamodb import ITable as _ITable_24826f7e
from ..aws_ec2 import IInstance as _IInstance_3a12995c
from ..aws_efs import IFileSystem as _IFileSystem_f9c61b15
from ..aws_events import Schedule as _Schedule_297d3fad
from ..aws_iam import (
    IGrantable as _IGrantable_4c5a91d1,
    IPrincipal as _IPrincipal_93b48231,
    IRole as _IRole_59af6f50,
    PolicyDocument as _PolicyDocument_b5de5177,
)
from ..aws_kms import IKey as _IKey_36930160
from ..aws_rds import IDatabaseInstance as _IDatabaseInstance_2f266f28
from ..aws_sns import ITopic as _ITopic_465e36b9


@jsii.data_type(
    jsii_type="monocdk.aws_backup.BackupPlanProps",
    jsii_struct_bases=[],
    name_mapping={
        "backup_plan_name": "backupPlanName",
        "backup_plan_rules": "backupPlanRules",
        "backup_vault": "backupVault",
    },
)
class BackupPlanProps:
    def __init__(
        self,
        *,
        backup_plan_name: typing.Optional[builtins.str] = None,
        backup_plan_rules: typing.Optional[typing.List["BackupPlanRule"]] = None,
        backup_vault: typing.Optional["IBackupVault"] = None,
    ) -> None:
        '''(experimental) Properties for a BackupPlan.

        :param backup_plan_name: (experimental) The display name of the backup plan. Default: - A CDK generated name
        :param backup_plan_rules: (experimental) Rules for the backup plan. Use ``addRule()`` to add rules after instantiation. Default: - use ``addRule()`` to add rules
        :param backup_vault: (experimental) The backup vault where backups are stored. Default: - use the vault defined at the rule level. If not defined a new common vault for the plan will be created

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if backup_plan_name is not None:
            self._values["backup_plan_name"] = backup_plan_name
        if backup_plan_rules is not None:
            self._values["backup_plan_rules"] = backup_plan_rules
        if backup_vault is not None:
            self._values["backup_vault"] = backup_vault

    @builtins.property
    def backup_plan_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The display name of the backup plan.

        :default: - A CDK generated name

        :stability: experimental
        '''
        result = self._values.get("backup_plan_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_plan_rules(self) -> typing.Optional[typing.List["BackupPlanRule"]]:
        '''(experimental) Rules for the backup plan.

        Use ``addRule()`` to add rules after
        instantiation.

        :default: - use ``addRule()`` to add rules

        :stability: experimental
        '''
        result = self._values.get("backup_plan_rules")
        return typing.cast(typing.Optional[typing.List["BackupPlanRule"]], result)

    @builtins.property
    def backup_vault(self) -> typing.Optional["IBackupVault"]:
        '''(experimental) The backup vault where backups are stored.

        :default:

        - use the vault defined at the rule level. If not defined a new
        common vault for the plan will be created

        :stability: experimental
        '''
        result = self._values.get("backup_vault")
        return typing.cast(typing.Optional["IBackupVault"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPlanProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupPlanRule(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_backup.BackupPlanRule",
):
    '''(experimental) A backup plan rule.

    :stability: experimental
    '''

    def __init__(
        self,
        *,
        backup_vault: typing.Optional["IBackupVault"] = None,
        completion_window: typing.Optional[_Duration_070aa057] = None,
        delete_after: typing.Optional[_Duration_070aa057] = None,
        move_to_cold_storage_after: typing.Optional[_Duration_070aa057] = None,
        rule_name: typing.Optional[builtins.str] = None,
        schedule_expression: typing.Optional[_Schedule_297d3fad] = None,
        start_window: typing.Optional[_Duration_070aa057] = None,
    ) -> None:
        '''
        :param backup_vault: (experimental) The backup vault where backups are. Default: - use the vault defined at the plan level. If not defined a new common vault for the plan will be created
        :param completion_window: (experimental) The duration after a backup job is successfully started before it must be completed or it is canceled by AWS Backup. Default: - 8 hours
        :param delete_after: (experimental) Specifies the duration after creation that a recovery point is deleted. Must be greater than ``moveToColdStorageAfter``. Default: - recovery point is never deleted
        :param move_to_cold_storage_after: (experimental) Specifies the duration after creation that a recovery point is moved to cold storage. Default: - recovery point is never moved to cold storage
        :param rule_name: (experimental) A display name for the backup rule. Default: - a CDK generated name
        :param schedule_expression: (experimental) A CRON expression specifying when AWS Backup initiates a backup job. Default: - no schedule
        :param start_window: (experimental) The duration after a backup is scheduled before a job is canceled if it doesn't start successfully. Default: - 8 hours

        :stability: experimental
        '''
        props = BackupPlanRuleProps(
            backup_vault=backup_vault,
            completion_window=completion_window,
            delete_after=delete_after,
            move_to_cold_storage_after=move_to_cold_storage_after,
            rule_name=rule_name,
            schedule_expression=schedule_expression,
            start_window=start_window,
        )

        jsii.create(BackupPlanRule, self, [props])

    @jsii.member(jsii_name="daily") # type: ignore[misc]
    @builtins.classmethod
    def daily(
        cls,
        backup_vault: typing.Optional["IBackupVault"] = None,
    ) -> "BackupPlanRule":
        '''(experimental) Daily with 35 days retention.

        :param backup_vault: -

        :stability: experimental
        '''
        return typing.cast("BackupPlanRule", jsii.sinvoke(cls, "daily", [backup_vault]))

    @jsii.member(jsii_name="monthly1Year") # type: ignore[misc]
    @builtins.classmethod
    def monthly1_year(
        cls,
        backup_vault: typing.Optional["IBackupVault"] = None,
    ) -> "BackupPlanRule":
        '''(experimental) Monthly 1 year retention, move to cold storage after 1 month.

        :param backup_vault: -

        :stability: experimental
        '''
        return typing.cast("BackupPlanRule", jsii.sinvoke(cls, "monthly1Year", [backup_vault]))

    @jsii.member(jsii_name="monthly5Year") # type: ignore[misc]
    @builtins.classmethod
    def monthly5_year(
        cls,
        backup_vault: typing.Optional["IBackupVault"] = None,
    ) -> "BackupPlanRule":
        '''(experimental) Monthly 5 year retention, move to cold storage after 3 months.

        :param backup_vault: -

        :stability: experimental
        '''
        return typing.cast("BackupPlanRule", jsii.sinvoke(cls, "monthly5Year", [backup_vault]))

    @jsii.member(jsii_name="monthly7Year") # type: ignore[misc]
    @builtins.classmethod
    def monthly7_year(
        cls,
        backup_vault: typing.Optional["IBackupVault"] = None,
    ) -> "BackupPlanRule":
        '''(experimental) Monthly 7 year retention, move to cold storage after 3 months.

        :param backup_vault: -

        :stability: experimental
        '''
        return typing.cast("BackupPlanRule", jsii.sinvoke(cls, "monthly7Year", [backup_vault]))

    @jsii.member(jsii_name="weekly") # type: ignore[misc]
    @builtins.classmethod
    def weekly(
        cls,
        backup_vault: typing.Optional["IBackupVault"] = None,
    ) -> "BackupPlanRule":
        '''(experimental) Weekly with 3 months retention.

        :param backup_vault: -

        :stability: experimental
        '''
        return typing.cast("BackupPlanRule", jsii.sinvoke(cls, "weekly", [backup_vault]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="props")
    def props(self) -> "BackupPlanRuleProps":
        '''(experimental) Rule properties.

        :stability: experimental
        '''
        return typing.cast("BackupPlanRuleProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="monocdk.aws_backup.BackupPlanRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "backup_vault": "backupVault",
        "completion_window": "completionWindow",
        "delete_after": "deleteAfter",
        "move_to_cold_storage_after": "moveToColdStorageAfter",
        "rule_name": "ruleName",
        "schedule_expression": "scheduleExpression",
        "start_window": "startWindow",
    },
)
class BackupPlanRuleProps:
    def __init__(
        self,
        *,
        backup_vault: typing.Optional["IBackupVault"] = None,
        completion_window: typing.Optional[_Duration_070aa057] = None,
        delete_after: typing.Optional[_Duration_070aa057] = None,
        move_to_cold_storage_after: typing.Optional[_Duration_070aa057] = None,
        rule_name: typing.Optional[builtins.str] = None,
        schedule_expression: typing.Optional[_Schedule_297d3fad] = None,
        start_window: typing.Optional[_Duration_070aa057] = None,
    ) -> None:
        '''(experimental) Properties for a BackupPlanRule.

        :param backup_vault: (experimental) The backup vault where backups are. Default: - use the vault defined at the plan level. If not defined a new common vault for the plan will be created
        :param completion_window: (experimental) The duration after a backup job is successfully started before it must be completed or it is canceled by AWS Backup. Default: - 8 hours
        :param delete_after: (experimental) Specifies the duration after creation that a recovery point is deleted. Must be greater than ``moveToColdStorageAfter``. Default: - recovery point is never deleted
        :param move_to_cold_storage_after: (experimental) Specifies the duration after creation that a recovery point is moved to cold storage. Default: - recovery point is never moved to cold storage
        :param rule_name: (experimental) A display name for the backup rule. Default: - a CDK generated name
        :param schedule_expression: (experimental) A CRON expression specifying when AWS Backup initiates a backup job. Default: - no schedule
        :param start_window: (experimental) The duration after a backup is scheduled before a job is canceled if it doesn't start successfully. Default: - 8 hours

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if backup_vault is not None:
            self._values["backup_vault"] = backup_vault
        if completion_window is not None:
            self._values["completion_window"] = completion_window
        if delete_after is not None:
            self._values["delete_after"] = delete_after
        if move_to_cold_storage_after is not None:
            self._values["move_to_cold_storage_after"] = move_to_cold_storage_after
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if schedule_expression is not None:
            self._values["schedule_expression"] = schedule_expression
        if start_window is not None:
            self._values["start_window"] = start_window

    @builtins.property
    def backup_vault(self) -> typing.Optional["IBackupVault"]:
        '''(experimental) The backup vault where backups are.

        :default:

        - use the vault defined at the plan level. If not defined a new
        common vault for the plan will be created

        :stability: experimental
        '''
        result = self._values.get("backup_vault")
        return typing.cast(typing.Optional["IBackupVault"], result)

    @builtins.property
    def completion_window(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The duration after a backup job is successfully started before it must be completed or it is canceled by AWS Backup.

        :default: - 8 hours

        :stability: experimental
        '''
        result = self._values.get("completion_window")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def delete_after(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Specifies the duration after creation that a recovery point is deleted.

        Must be greater than ``moveToColdStorageAfter``.

        :default: - recovery point is never deleted

        :stability: experimental
        '''
        result = self._values.get("delete_after")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def move_to_cold_storage_after(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) Specifies the duration after creation that a recovery point is moved to cold storage.

        :default: - recovery point is never moved to cold storage

        :stability: experimental
        '''
        result = self._values.get("move_to_cold_storage_after")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A display name for the backup rule.

        :default: - a CDK generated name

        :stability: experimental
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_expression(self) -> typing.Optional[_Schedule_297d3fad]:
        '''(experimental) A CRON expression specifying when AWS Backup initiates a backup job.

        :default: - no schedule

        :stability: experimental
        '''
        result = self._values.get("schedule_expression")
        return typing.cast(typing.Optional[_Schedule_297d3fad], result)

    @builtins.property
    def start_window(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The duration after a backup is scheduled before a job is canceled if it doesn't start successfully.

        :default: - 8 hours

        :stability: experimental
        '''
        result = self._values.get("start_window")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupPlanRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BackupResource(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_backup.BackupResource",
):
    '''(experimental) A resource to backup.

    :stability: experimental
    '''

    def __init__(
        self,
        resource: typing.Optional[builtins.str] = None,
        tag_condition: typing.Optional["TagCondition"] = None,
        construct: typing.Optional[constructs.Construct] = None,
    ) -> None:
        '''
        :param resource: -
        :param tag_condition: -
        :param construct: -

        :stability: experimental
        '''
        jsii.create(BackupResource, self, [resource, tag_condition, construct])

    @jsii.member(jsii_name="fromArn") # type: ignore[misc]
    @builtins.classmethod
    def from_arn(cls, arn: builtins.str) -> "BackupResource":
        '''(experimental) A list of ARNs or match patterns such as ``arn:aws:ec2:us-east-1:123456789012:volume/*``.

        :param arn: -

        :stability: experimental
        '''
        return typing.cast("BackupResource", jsii.sinvoke(cls, "fromArn", [arn]))

    @jsii.member(jsii_name="fromConstruct") # type: ignore[misc]
    @builtins.classmethod
    def from_construct(cls, construct: constructs.Construct) -> "BackupResource":
        '''(experimental) Adds all supported resources in a construct.

        :param construct: The construct containing resources to backup.

        :stability: experimental
        '''
        return typing.cast("BackupResource", jsii.sinvoke(cls, "fromConstruct", [construct]))

    @jsii.member(jsii_name="fromDynamoDbTable") # type: ignore[misc]
    @builtins.classmethod
    def from_dynamo_db_table(cls, table: _ITable_24826f7e) -> "BackupResource":
        '''(experimental) A DynamoDB table.

        :param table: -

        :stability: experimental
        '''
        return typing.cast("BackupResource", jsii.sinvoke(cls, "fromDynamoDbTable", [table]))

    @jsii.member(jsii_name="fromEc2Instance") # type: ignore[misc]
    @builtins.classmethod
    def from_ec2_instance(cls, instance: _IInstance_3a12995c) -> "BackupResource":
        '''(experimental) An EC2 instance.

        :param instance: -

        :stability: experimental
        '''
        return typing.cast("BackupResource", jsii.sinvoke(cls, "fromEc2Instance", [instance]))

    @jsii.member(jsii_name="fromEfsFileSystem") # type: ignore[misc]
    @builtins.classmethod
    def from_efs_file_system(
        cls,
        file_system: _IFileSystem_f9c61b15,
    ) -> "BackupResource":
        '''(experimental) An EFS file system.

        :param file_system: -

        :stability: experimental
        '''
        return typing.cast("BackupResource", jsii.sinvoke(cls, "fromEfsFileSystem", [file_system]))

    @jsii.member(jsii_name="fromRdsDatabaseInstance") # type: ignore[misc]
    @builtins.classmethod
    def from_rds_database_instance(
        cls,
        instance: _IDatabaseInstance_2f266f28,
    ) -> "BackupResource":
        '''(experimental) A RDS database instance.

        :param instance: -

        :stability: experimental
        '''
        return typing.cast("BackupResource", jsii.sinvoke(cls, "fromRdsDatabaseInstance", [instance]))

    @jsii.member(jsii_name="fromTag") # type: ignore[misc]
    @builtins.classmethod
    def from_tag(
        cls,
        key: builtins.str,
        value: builtins.str,
        operation: typing.Optional["TagOperation"] = None,
    ) -> "BackupResource":
        '''(experimental) A tag condition.

        :param key: -
        :param value: -
        :param operation: -

        :stability: experimental
        '''
        return typing.cast("BackupResource", jsii.sinvoke(cls, "fromTag", [key, value, operation]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="construct")
    def construct(self) -> typing.Optional[_Construct_e78e779f]:
        '''(experimental) A construct.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_Construct_e78e779f], jsii.get(self, "construct"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="resource")
    def resource(self) -> typing.Optional[builtins.str]:
        '''(experimental) A resource.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resource"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tagCondition")
    def tag_condition(self) -> typing.Optional["TagCondition"]:
        '''(experimental) A condition on a tag.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["TagCondition"], jsii.get(self, "tagCondition"))


@jsii.implements(_IGrantable_4c5a91d1)
class BackupSelection(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_backup.BackupSelection",
):
    '''(experimental) A backup selection.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        backup_plan: "IBackupPlan",
        resources: typing.List[BackupResource],
        allow_restores: typing.Optional[builtins.bool] = None,
        backup_selection_name: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param backup_plan: (experimental) The backup plan for this selection.
        :param resources: (experimental) The resources to backup. Use the helper static methods defined on ``BackupResource``.
        :param allow_restores: (experimental) Whether to automatically give restores permissions to the role that AWS Backup uses. If ``true``, the ``AWSBackupServiceRolePolicyForRestores`` managed policy will be attached to the role. Default: false
        :param backup_selection_name: (experimental) The name for this selection. Default: - a CDK generated name
        :param role: (experimental) The role that AWS Backup uses to authenticate when backuping or restoring the resources. The ``AWSBackupServiceRolePolicyForBackup`` managed policy will be attached to this role. Default: - a new role will be created

        :stability: experimental
        '''
        props = BackupSelectionProps(
            backup_plan=backup_plan,
            resources=resources,
            allow_restores=allow_restores,
            backup_selection_name=backup_selection_name,
            role=role,
        )

        jsii.create(BackupSelection, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupPlanId")
    def backup_plan_id(self) -> builtins.str:
        '''(experimental) The identifier of the backup plan.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "backupPlanId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_93b48231:
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        return typing.cast(_IPrincipal_93b48231, jsii.get(self, "grantPrincipal"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="selectionId")
    def selection_id(self) -> builtins.str:
        '''(experimental) The identifier of the backup selection.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "selectionId"))


@jsii.data_type(
    jsii_type="monocdk.aws_backup.BackupSelectionOptions",
    jsii_struct_bases=[],
    name_mapping={
        "resources": "resources",
        "allow_restores": "allowRestores",
        "backup_selection_name": "backupSelectionName",
        "role": "role",
    },
)
class BackupSelectionOptions:
    def __init__(
        self,
        *,
        resources: typing.List[BackupResource],
        allow_restores: typing.Optional[builtins.bool] = None,
        backup_selection_name: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''(experimental) Options for a BackupSelection.

        :param resources: (experimental) The resources to backup. Use the helper static methods defined on ``BackupResource``.
        :param allow_restores: (experimental) Whether to automatically give restores permissions to the role that AWS Backup uses. If ``true``, the ``AWSBackupServiceRolePolicyForRestores`` managed policy will be attached to the role. Default: false
        :param backup_selection_name: (experimental) The name for this selection. Default: - a CDK generated name
        :param role: (experimental) The role that AWS Backup uses to authenticate when backuping or restoring the resources. The ``AWSBackupServiceRolePolicyForBackup`` managed policy will be attached to this role. Default: - a new role will be created

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "resources": resources,
        }
        if allow_restores is not None:
            self._values["allow_restores"] = allow_restores
        if backup_selection_name is not None:
            self._values["backup_selection_name"] = backup_selection_name
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def resources(self) -> typing.List[BackupResource]:
        '''(experimental) The resources to backup.

        Use the helper static methods defined on ``BackupResource``.

        :stability: experimental
        '''
        result = self._values.get("resources")
        assert result is not None, "Required property 'resources' is missing"
        return typing.cast(typing.List[BackupResource], result)

    @builtins.property
    def allow_restores(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to automatically give restores permissions to the role that AWS Backup uses.

        If ``true``, the ``AWSBackupServiceRolePolicyForRestores`` managed
        policy will be attached to the role.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("allow_restores")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def backup_selection_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name for this selection.

        :default: - a CDK generated name

        :stability: experimental
        '''
        result = self._values.get("backup_selection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The role that AWS Backup uses to authenticate when backuping or restoring the resources.

        The ``AWSBackupServiceRolePolicyForBackup`` managed policy
        will be attached to this role.

        :default: - a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupSelectionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_backup.BackupSelectionProps",
    jsii_struct_bases=[BackupSelectionOptions],
    name_mapping={
        "resources": "resources",
        "allow_restores": "allowRestores",
        "backup_selection_name": "backupSelectionName",
        "role": "role",
        "backup_plan": "backupPlan",
    },
)
class BackupSelectionProps(BackupSelectionOptions):
    def __init__(
        self,
        *,
        resources: typing.List[BackupResource],
        allow_restores: typing.Optional[builtins.bool] = None,
        backup_selection_name: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        backup_plan: "IBackupPlan",
    ) -> None:
        '''(experimental) Properties for a BackupSelection.

        :param resources: (experimental) The resources to backup. Use the helper static methods defined on ``BackupResource``.
        :param allow_restores: (experimental) Whether to automatically give restores permissions to the role that AWS Backup uses. If ``true``, the ``AWSBackupServiceRolePolicyForRestores`` managed policy will be attached to the role. Default: false
        :param backup_selection_name: (experimental) The name for this selection. Default: - a CDK generated name
        :param role: (experimental) The role that AWS Backup uses to authenticate when backuping or restoring the resources. The ``AWSBackupServiceRolePolicyForBackup`` managed policy will be attached to this role. Default: - a new role will be created
        :param backup_plan: (experimental) The backup plan for this selection.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "resources": resources,
            "backup_plan": backup_plan,
        }
        if allow_restores is not None:
            self._values["allow_restores"] = allow_restores
        if backup_selection_name is not None:
            self._values["backup_selection_name"] = backup_selection_name
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def resources(self) -> typing.List[BackupResource]:
        '''(experimental) The resources to backup.

        Use the helper static methods defined on ``BackupResource``.

        :stability: experimental
        '''
        result = self._values.get("resources")
        assert result is not None, "Required property 'resources' is missing"
        return typing.cast(typing.List[BackupResource], result)

    @builtins.property
    def allow_restores(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to automatically give restores permissions to the role that AWS Backup uses.

        If ``true``, the ``AWSBackupServiceRolePolicyForRestores`` managed
        policy will be attached to the role.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("allow_restores")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def backup_selection_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name for this selection.

        :default: - a CDK generated name

        :stability: experimental
        '''
        result = self._values.get("backup_selection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The role that AWS Backup uses to authenticate when backuping or restoring the resources.

        The ``AWSBackupServiceRolePolicyForBackup`` managed policy
        will be attached to this role.

        :default: - a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def backup_plan(self) -> "IBackupPlan":
        '''(experimental) The backup plan for this selection.

        :stability: experimental
        '''
        result = self._values.get("backup_plan")
        assert result is not None, "Required property 'backup_plan' is missing"
        return typing.cast("IBackupPlan", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupSelectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_backup.BackupVaultEvents")
class BackupVaultEvents(enum.Enum):
    '''(experimental) Backup vault events.

    :stability: experimental
    '''

    BACKUP_JOB_STARTED = "BACKUP_JOB_STARTED"
    '''(experimental) BACKUP_JOB_STARTED.

    :stability: experimental
    '''
    BACKUP_JOB_COMPLETED = "BACKUP_JOB_COMPLETED"
    '''(experimental) BACKUP_JOB_COMPLETED.

    :stability: experimental
    '''
    BACKUP_JOB_SUCCESSFUL = "BACKUP_JOB_SUCCESSFUL"
    '''(experimental) BACKUP_JOB_SUCCESSFUL.

    :stability: experimental
    '''
    BACKUP_JOB_FAILED = "BACKUP_JOB_FAILED"
    '''(experimental) BACKUP_JOB_FAILED.

    :stability: experimental
    '''
    BACKUP_JOB_EXPIRED = "BACKUP_JOB_EXPIRED"
    '''(experimental) BACKUP_JOB_EXPIRED.

    :stability: experimental
    '''
    RESTORE_JOB_STARTED = "RESTORE_JOB_STARTED"
    '''(experimental) RESTORE_JOB_STARTED.

    :stability: experimental
    '''
    RESTORE_JOB_COMPLETED = "RESTORE_JOB_COMPLETED"
    '''(experimental) RESTORE_JOB_COMPLETED.

    :stability: experimental
    '''
    RESTORE_JOB_SUCCESSFUL = "RESTORE_JOB_SUCCESSFUL"
    '''(experimental) RESTORE_JOB_SUCCESSFUL.

    :stability: experimental
    '''
    RESTORE_JOB_FAILED = "RESTORE_JOB_FAILED"
    '''(experimental) RESTORE_JOB_FAILED.

    :stability: experimental
    '''
    COPY_JOB_STARTED = "COPY_JOB_STARTED"
    '''(experimental) COPY_JOB_STARTED.

    :stability: experimental
    '''
    COPY_JOB_SUCCESSFUL = "COPY_JOB_SUCCESSFUL"
    '''(experimental) COPY_JOB_SUCCESSFUL.

    :stability: experimental
    '''
    COPY_JOB_FAILED = "COPY_JOB_FAILED"
    '''(experimental) COPY_JOB_FAILED.

    :stability: experimental
    '''
    RECOVERY_POINT_MODIFIED = "RECOVERY_POINT_MODIFIED"
    '''(experimental) RECOVERY_POINT_MODIFIED.

    :stability: experimental
    '''
    BACKUP_PLAN_CREATED = "BACKUP_PLAN_CREATED"
    '''(experimental) BACKUP_PLAN_CREATED.

    :stability: experimental
    '''
    BACKUP_PLAN_MODIFIED = "BACKUP_PLAN_MODIFIED"
    '''(experimental) BACKUP_PLAN_MODIFIED.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_backup.BackupVaultProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_policy": "accessPolicy",
        "backup_vault_name": "backupVaultName",
        "encryption_key": "encryptionKey",
        "notification_events": "notificationEvents",
        "notification_topic": "notificationTopic",
        "removal_policy": "removalPolicy",
    },
)
class BackupVaultProps:
    def __init__(
        self,
        *,
        access_policy: typing.Optional[_PolicyDocument_b5de5177] = None,
        backup_vault_name: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        notification_events: typing.Optional[typing.List[BackupVaultEvents]] = None,
        notification_topic: typing.Optional[_ITopic_465e36b9] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    ) -> None:
        '''(experimental) Properties for a BackupVault.

        :param access_policy: (experimental) A resource-based policy that is used to manage access permissions on the backup vault. Default: - access is not restricted
        :param backup_vault_name: (experimental) The name of a logical container where backups are stored. Backup vaults are identified by names that are unique to the account used to create them and the AWS Region where they are created. Default: - A CDK generated name
        :param encryption_key: (experimental) The server-side encryption key to use to protect your backups. Default: - an Amazon managed KMS key
        :param notification_events: (experimental) The vault events to send. Default: - all vault events if ``notificationTopic`` is defined
        :param notification_topic: (experimental) A SNS topic to send vault events to. Default: - no notifications
        :param removal_policy: (experimental) The removal policy to apply to the vault. Note that removing a vault that contains recovery points will fail. Default: RemovalPolicy.RETAIN

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if access_policy is not None:
            self._values["access_policy"] = access_policy
        if backup_vault_name is not None:
            self._values["backup_vault_name"] = backup_vault_name
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if notification_events is not None:
            self._values["notification_events"] = notification_events
        if notification_topic is not None:
            self._values["notification_topic"] = notification_topic
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def access_policy(self) -> typing.Optional[_PolicyDocument_b5de5177]:
        '''(experimental) A resource-based policy that is used to manage access permissions on the backup vault.

        :default: - access is not restricted

        :stability: experimental
        '''
        result = self._values.get("access_policy")
        return typing.cast(typing.Optional[_PolicyDocument_b5de5177], result)

    @builtins.property
    def backup_vault_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of a logical container where backups are stored.

        Backup vaults
        are identified by names that are unique to the account used to create
        them and the AWS Region where they are created.

        :default: - A CDK generated name

        :stability: experimental
        '''
        result = self._values.get("backup_vault_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) The server-side encryption key to use to protect your backups.

        :default: - an Amazon managed KMS key

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def notification_events(self) -> typing.Optional[typing.List[BackupVaultEvents]]:
        '''(experimental) The vault events to send.

        :default: - all vault events if ``notificationTopic`` is defined

        :see: https://docs.aws.amazon.com/aws-backup/latest/devguide/sns-notifications.html
        :stability: experimental
        '''
        result = self._values.get("notification_events")
        return typing.cast(typing.Optional[typing.List[BackupVaultEvents]], result)

    @builtins.property
    def notification_topic(self) -> typing.Optional[_ITopic_465e36b9]:
        '''(experimental) A SNS topic to send vault events to.

        :default: - no notifications

        :see: https://docs.aws.amazon.com/aws-backup/latest/devguide/sns-notifications.html
        :stability: experimental
        '''
        result = self._values.get("notification_topic")
        return typing.cast(typing.Optional[_ITopic_465e36b9], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        '''(experimental) The removal policy to apply to the vault.

        Note that removing a vault
        that contains recovery points will fail.

        :default: RemovalPolicy.RETAIN

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_RemovalPolicy_c97e7a20], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupVaultProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnBackupPlan(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_backup.CfnBackupPlan",
):
    '''A CloudFormation ``AWS::Backup::BackupPlan``.

    :cloudformationResource: AWS::Backup::BackupPlan
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupplan.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        backup_plan: typing.Union["CfnBackupPlan.BackupPlanResourceTypeProperty", _IResolvable_a771d0ef],
        backup_plan_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> None:
        '''Create a new ``AWS::Backup::BackupPlan``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param backup_plan: ``AWS::Backup::BackupPlan.BackupPlan``.
        :param backup_plan_tags: ``AWS::Backup::BackupPlan.BackupPlanTags``.
        '''
        props = CfnBackupPlanProps(
            backup_plan=backup_plan, backup_plan_tags=backup_plan_tags
        )

        jsii.create(CfnBackupPlan, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrBackupPlanArn")
    def attr_backup_plan_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: BackupPlanArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrBackupPlanArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrBackupPlanId")
    def attr_backup_plan_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: BackupPlanId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrBackupPlanId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrVersionId")
    def attr_version_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: VersionId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVersionId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupPlan")
    def backup_plan(
        self,
    ) -> typing.Union["CfnBackupPlan.BackupPlanResourceTypeProperty", _IResolvable_a771d0ef]:
        '''``AWS::Backup::BackupPlan.BackupPlan``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupplan.html#cfn-backup-backupplan-backupplan
        '''
        return typing.cast(typing.Union["CfnBackupPlan.BackupPlanResourceTypeProperty", _IResolvable_a771d0ef], jsii.get(self, "backupPlan"))

    @backup_plan.setter
    def backup_plan(
        self,
        value: typing.Union["CfnBackupPlan.BackupPlanResourceTypeProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "backupPlan", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupPlanTags")
    def backup_plan_tags(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Backup::BackupPlan.BackupPlanTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupplan.html#cfn-backup-backupplan-backupplantags
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "backupPlanTags"))

    @backup_plan_tags.setter
    def backup_plan_tags(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        jsii.set(self, "backupPlanTags", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_backup.CfnBackupPlan.AdvancedBackupSettingResourceTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "backup_options": "backupOptions",
            "resource_type": "resourceType",
        },
    )
    class AdvancedBackupSettingResourceTypeProperty:
        def __init__(
            self,
            *,
            backup_options: typing.Any,
            resource_type: builtins.str,
        ) -> None:
            '''
            :param backup_options: ``CfnBackupPlan.AdvancedBackupSettingResourceTypeProperty.BackupOptions``.
            :param resource_type: ``CfnBackupPlan.AdvancedBackupSettingResourceTypeProperty.ResourceType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-advancedbackupsettingresourcetype.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "backup_options": backup_options,
                "resource_type": resource_type,
            }

        @builtins.property
        def backup_options(self) -> typing.Any:
            '''``CfnBackupPlan.AdvancedBackupSettingResourceTypeProperty.BackupOptions``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-advancedbackupsettingresourcetype.html#cfn-backup-backupplan-advancedbackupsettingresourcetype-backupoptions
            '''
            result = self._values.get("backup_options")
            assert result is not None, "Required property 'backup_options' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def resource_type(self) -> builtins.str:
            '''``CfnBackupPlan.AdvancedBackupSettingResourceTypeProperty.ResourceType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-advancedbackupsettingresourcetype.html#cfn-backup-backupplan-advancedbackupsettingresourcetype-resourcetype
            '''
            result = self._values.get("resource_type")
            assert result is not None, "Required property 'resource_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdvancedBackupSettingResourceTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_backup.CfnBackupPlan.BackupPlanResourceTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "backup_plan_name": "backupPlanName",
            "backup_plan_rule": "backupPlanRule",
            "advanced_backup_settings": "advancedBackupSettings",
        },
    )
    class BackupPlanResourceTypeProperty:
        def __init__(
            self,
            *,
            backup_plan_name: builtins.str,
            backup_plan_rule: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBackupPlan.BackupRuleResourceTypeProperty", _IResolvable_a771d0ef]]],
            advanced_backup_settings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBackupPlan.AdvancedBackupSettingResourceTypeProperty", _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''
            :param backup_plan_name: ``CfnBackupPlan.BackupPlanResourceTypeProperty.BackupPlanName``.
            :param backup_plan_rule: ``CfnBackupPlan.BackupPlanResourceTypeProperty.BackupPlanRule``.
            :param advanced_backup_settings: ``CfnBackupPlan.BackupPlanResourceTypeProperty.AdvancedBackupSettings``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupplanresourcetype.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "backup_plan_name": backup_plan_name,
                "backup_plan_rule": backup_plan_rule,
            }
            if advanced_backup_settings is not None:
                self._values["advanced_backup_settings"] = advanced_backup_settings

        @builtins.property
        def backup_plan_name(self) -> builtins.str:
            '''``CfnBackupPlan.BackupPlanResourceTypeProperty.BackupPlanName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupplanresourcetype.html#cfn-backup-backupplan-backupplanresourcetype-backupplanname
            '''
            result = self._values.get("backup_plan_name")
            assert result is not None, "Required property 'backup_plan_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def backup_plan_rule(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBackupPlan.BackupRuleResourceTypeProperty", _IResolvable_a771d0ef]]]:
            '''``CfnBackupPlan.BackupPlanResourceTypeProperty.BackupPlanRule``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupplanresourcetype.html#cfn-backup-backupplan-backupplanresourcetype-backupplanrule
            '''
            result = self._values.get("backup_plan_rule")
            assert result is not None, "Required property 'backup_plan_rule' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBackupPlan.BackupRuleResourceTypeProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def advanced_backup_settings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBackupPlan.AdvancedBackupSettingResourceTypeProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBackupPlan.BackupPlanResourceTypeProperty.AdvancedBackupSettings``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupplanresourcetype.html#cfn-backup-backupplan-backupplanresourcetype-advancedbackupsettings
            '''
            result = self._values.get("advanced_backup_settings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBackupPlan.AdvancedBackupSettingResourceTypeProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BackupPlanResourceTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_backup.CfnBackupPlan.BackupRuleResourceTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "rule_name": "ruleName",
            "target_backup_vault": "targetBackupVault",
            "completion_window_minutes": "completionWindowMinutes",
            "copy_actions": "copyActions",
            "lifecycle": "lifecycle",
            "recovery_point_tags": "recoveryPointTags",
            "schedule_expression": "scheduleExpression",
            "start_window_minutes": "startWindowMinutes",
        },
    )
    class BackupRuleResourceTypeProperty:
        def __init__(
            self,
            *,
            rule_name: builtins.str,
            target_backup_vault: builtins.str,
            completion_window_minutes: typing.Optional[jsii.Number] = None,
            copy_actions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBackupPlan.CopyActionResourceTypeProperty", _IResolvable_a771d0ef]]]] = None,
            lifecycle: typing.Optional[typing.Union["CfnBackupPlan.LifecycleResourceTypeProperty", _IResolvable_a771d0ef]] = None,
            recovery_point_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
            schedule_expression: typing.Optional[builtins.str] = None,
            start_window_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param rule_name: ``CfnBackupPlan.BackupRuleResourceTypeProperty.RuleName``.
            :param target_backup_vault: ``CfnBackupPlan.BackupRuleResourceTypeProperty.TargetBackupVault``.
            :param completion_window_minutes: ``CfnBackupPlan.BackupRuleResourceTypeProperty.CompletionWindowMinutes``.
            :param copy_actions: ``CfnBackupPlan.BackupRuleResourceTypeProperty.CopyActions``.
            :param lifecycle: ``CfnBackupPlan.BackupRuleResourceTypeProperty.Lifecycle``.
            :param recovery_point_tags: ``CfnBackupPlan.BackupRuleResourceTypeProperty.RecoveryPointTags``.
            :param schedule_expression: ``CfnBackupPlan.BackupRuleResourceTypeProperty.ScheduleExpression``.
            :param start_window_minutes: ``CfnBackupPlan.BackupRuleResourceTypeProperty.StartWindowMinutes``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "rule_name": rule_name,
                "target_backup_vault": target_backup_vault,
            }
            if completion_window_minutes is not None:
                self._values["completion_window_minutes"] = completion_window_minutes
            if copy_actions is not None:
                self._values["copy_actions"] = copy_actions
            if lifecycle is not None:
                self._values["lifecycle"] = lifecycle
            if recovery_point_tags is not None:
                self._values["recovery_point_tags"] = recovery_point_tags
            if schedule_expression is not None:
                self._values["schedule_expression"] = schedule_expression
            if start_window_minutes is not None:
                self._values["start_window_minutes"] = start_window_minutes

        @builtins.property
        def rule_name(self) -> builtins.str:
            '''``CfnBackupPlan.BackupRuleResourceTypeProperty.RuleName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-rulename
            '''
            result = self._values.get("rule_name")
            assert result is not None, "Required property 'rule_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def target_backup_vault(self) -> builtins.str:
            '''``CfnBackupPlan.BackupRuleResourceTypeProperty.TargetBackupVault``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-targetbackupvault
            '''
            result = self._values.get("target_backup_vault")
            assert result is not None, "Required property 'target_backup_vault' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def completion_window_minutes(self) -> typing.Optional[jsii.Number]:
            '''``CfnBackupPlan.BackupRuleResourceTypeProperty.CompletionWindowMinutes``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-completionwindowminutes
            '''
            result = self._values.get("completion_window_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def copy_actions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBackupPlan.CopyActionResourceTypeProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBackupPlan.BackupRuleResourceTypeProperty.CopyActions``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-copyactions
            '''
            result = self._values.get("copy_actions")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBackupPlan.CopyActionResourceTypeProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def lifecycle(
            self,
        ) -> typing.Optional[typing.Union["CfnBackupPlan.LifecycleResourceTypeProperty", _IResolvable_a771d0ef]]:
            '''``CfnBackupPlan.BackupRuleResourceTypeProperty.Lifecycle``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-lifecycle
            '''
            result = self._values.get("lifecycle")
            return typing.cast(typing.Optional[typing.Union["CfnBackupPlan.LifecycleResourceTypeProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def recovery_point_tags(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
            '''``CfnBackupPlan.BackupRuleResourceTypeProperty.RecoveryPointTags``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-recoverypointtags
            '''
            result = self._values.get("recovery_point_tags")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def schedule_expression(self) -> typing.Optional[builtins.str]:
            '''``CfnBackupPlan.BackupRuleResourceTypeProperty.ScheduleExpression``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-scheduleexpression
            '''
            result = self._values.get("schedule_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start_window_minutes(self) -> typing.Optional[jsii.Number]:
            '''``CfnBackupPlan.BackupRuleResourceTypeProperty.StartWindowMinutes``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-backupruleresourcetype.html#cfn-backup-backupplan-backupruleresourcetype-startwindowminutes
            '''
            result = self._values.get("start_window_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BackupRuleResourceTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_backup.CfnBackupPlan.CopyActionResourceTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_backup_vault_arn": "destinationBackupVaultArn",
            "lifecycle": "lifecycle",
        },
    )
    class CopyActionResourceTypeProperty:
        def __init__(
            self,
            *,
            destination_backup_vault_arn: builtins.str,
            lifecycle: typing.Optional[typing.Union["CfnBackupPlan.LifecycleResourceTypeProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param destination_backup_vault_arn: ``CfnBackupPlan.CopyActionResourceTypeProperty.DestinationBackupVaultArn``.
            :param lifecycle: ``CfnBackupPlan.CopyActionResourceTypeProperty.Lifecycle``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-copyactionresourcetype.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "destination_backup_vault_arn": destination_backup_vault_arn,
            }
            if lifecycle is not None:
                self._values["lifecycle"] = lifecycle

        @builtins.property
        def destination_backup_vault_arn(self) -> builtins.str:
            '''``CfnBackupPlan.CopyActionResourceTypeProperty.DestinationBackupVaultArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-copyactionresourcetype.html#cfn-backup-backupplan-copyactionresourcetype-destinationbackupvaultarn
            '''
            result = self._values.get("destination_backup_vault_arn")
            assert result is not None, "Required property 'destination_backup_vault_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def lifecycle(
            self,
        ) -> typing.Optional[typing.Union["CfnBackupPlan.LifecycleResourceTypeProperty", _IResolvable_a771d0ef]]:
            '''``CfnBackupPlan.CopyActionResourceTypeProperty.Lifecycle``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-copyactionresourcetype.html#cfn-backup-backupplan-copyactionresourcetype-lifecycle
            '''
            result = self._values.get("lifecycle")
            return typing.cast(typing.Optional[typing.Union["CfnBackupPlan.LifecycleResourceTypeProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CopyActionResourceTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_backup.CfnBackupPlan.LifecycleResourceTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delete_after_days": "deleteAfterDays",
            "move_to_cold_storage_after_days": "moveToColdStorageAfterDays",
        },
    )
    class LifecycleResourceTypeProperty:
        def __init__(
            self,
            *,
            delete_after_days: typing.Optional[jsii.Number] = None,
            move_to_cold_storage_after_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param delete_after_days: ``CfnBackupPlan.LifecycleResourceTypeProperty.DeleteAfterDays``.
            :param move_to_cold_storage_after_days: ``CfnBackupPlan.LifecycleResourceTypeProperty.MoveToColdStorageAfterDays``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-lifecycleresourcetype.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if delete_after_days is not None:
                self._values["delete_after_days"] = delete_after_days
            if move_to_cold_storage_after_days is not None:
                self._values["move_to_cold_storage_after_days"] = move_to_cold_storage_after_days

        @builtins.property
        def delete_after_days(self) -> typing.Optional[jsii.Number]:
            '''``CfnBackupPlan.LifecycleResourceTypeProperty.DeleteAfterDays``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-lifecycleresourcetype.html#cfn-backup-backupplan-lifecycleresourcetype-deleteafterdays
            '''
            result = self._values.get("delete_after_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def move_to_cold_storage_after_days(self) -> typing.Optional[jsii.Number]:
            '''``CfnBackupPlan.LifecycleResourceTypeProperty.MoveToColdStorageAfterDays``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupplan-lifecycleresourcetype.html#cfn-backup-backupplan-lifecycleresourcetype-movetocoldstorageafterdays
            '''
            result = self._values.get("move_to_cold_storage_after_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LifecycleResourceTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_backup.CfnBackupPlanProps",
    jsii_struct_bases=[],
    name_mapping={"backup_plan": "backupPlan", "backup_plan_tags": "backupPlanTags"},
)
class CfnBackupPlanProps:
    def __init__(
        self,
        *,
        backup_plan: typing.Union[CfnBackupPlan.BackupPlanResourceTypeProperty, _IResolvable_a771d0ef],
        backup_plan_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Backup::BackupPlan``.

        :param backup_plan: ``AWS::Backup::BackupPlan.BackupPlan``.
        :param backup_plan_tags: ``AWS::Backup::BackupPlan.BackupPlanTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupplan.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "backup_plan": backup_plan,
        }
        if backup_plan_tags is not None:
            self._values["backup_plan_tags"] = backup_plan_tags

    @builtins.property
    def backup_plan(
        self,
    ) -> typing.Union[CfnBackupPlan.BackupPlanResourceTypeProperty, _IResolvable_a771d0ef]:
        '''``AWS::Backup::BackupPlan.BackupPlan``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupplan.html#cfn-backup-backupplan-backupplan
        '''
        result = self._values.get("backup_plan")
        assert result is not None, "Required property 'backup_plan' is missing"
        return typing.cast(typing.Union[CfnBackupPlan.BackupPlanResourceTypeProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def backup_plan_tags(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Backup::BackupPlan.BackupPlanTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupplan.html#cfn-backup-backupplan-backupplantags
        '''
        result = self._values.get("backup_plan_tags")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBackupPlanProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnBackupSelection(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_backup.CfnBackupSelection",
):
    '''A CloudFormation ``AWS::Backup::BackupSelection``.

    :cloudformationResource: AWS::Backup::BackupSelection
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupselection.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        backup_plan_id: builtins.str,
        backup_selection: typing.Union["CfnBackupSelection.BackupSelectionResourceTypeProperty", _IResolvable_a771d0ef],
    ) -> None:
        '''Create a new ``AWS::Backup::BackupSelection``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param backup_plan_id: ``AWS::Backup::BackupSelection.BackupPlanId``.
        :param backup_selection: ``AWS::Backup::BackupSelection.BackupSelection``.
        '''
        props = CfnBackupSelectionProps(
            backup_plan_id=backup_plan_id, backup_selection=backup_selection
        )

        jsii.create(CfnBackupSelection, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrBackupPlanId")
    def attr_backup_plan_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: BackupPlanId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrBackupPlanId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrSelectionId")
    def attr_selection_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: SelectionId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSelectionId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupPlanId")
    def backup_plan_id(self) -> builtins.str:
        '''``AWS::Backup::BackupSelection.BackupPlanId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupselection.html#cfn-backup-backupselection-backupplanid
        '''
        return typing.cast(builtins.str, jsii.get(self, "backupPlanId"))

    @backup_plan_id.setter
    def backup_plan_id(self, value: builtins.str) -> None:
        jsii.set(self, "backupPlanId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupSelection")
    def backup_selection(
        self,
    ) -> typing.Union["CfnBackupSelection.BackupSelectionResourceTypeProperty", _IResolvable_a771d0ef]:
        '''``AWS::Backup::BackupSelection.BackupSelection``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupselection.html#cfn-backup-backupselection-backupselection
        '''
        return typing.cast(typing.Union["CfnBackupSelection.BackupSelectionResourceTypeProperty", _IResolvable_a771d0ef], jsii.get(self, "backupSelection"))

    @backup_selection.setter
    def backup_selection(
        self,
        value: typing.Union["CfnBackupSelection.BackupSelectionResourceTypeProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "backupSelection", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_backup.CfnBackupSelection.BackupSelectionResourceTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "iam_role_arn": "iamRoleArn",
            "selection_name": "selectionName",
            "list_of_tags": "listOfTags",
            "resources": "resources",
        },
    )
    class BackupSelectionResourceTypeProperty:
        def __init__(
            self,
            *,
            iam_role_arn: builtins.str,
            selection_name: builtins.str,
            list_of_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBackupSelection.ConditionResourceTypeProperty", _IResolvable_a771d0ef]]]] = None,
            resources: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            '''
            :param iam_role_arn: ``CfnBackupSelection.BackupSelectionResourceTypeProperty.IamRoleArn``.
            :param selection_name: ``CfnBackupSelection.BackupSelectionResourceTypeProperty.SelectionName``.
            :param list_of_tags: ``CfnBackupSelection.BackupSelectionResourceTypeProperty.ListOfTags``.
            :param resources: ``CfnBackupSelection.BackupSelectionResourceTypeProperty.Resources``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-backupselectionresourcetype.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "iam_role_arn": iam_role_arn,
                "selection_name": selection_name,
            }
            if list_of_tags is not None:
                self._values["list_of_tags"] = list_of_tags
            if resources is not None:
                self._values["resources"] = resources

        @builtins.property
        def iam_role_arn(self) -> builtins.str:
            '''``CfnBackupSelection.BackupSelectionResourceTypeProperty.IamRoleArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-backupselectionresourcetype.html#cfn-backup-backupselection-backupselectionresourcetype-iamrolearn
            '''
            result = self._values.get("iam_role_arn")
            assert result is not None, "Required property 'iam_role_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def selection_name(self) -> builtins.str:
            '''``CfnBackupSelection.BackupSelectionResourceTypeProperty.SelectionName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-backupselectionresourcetype.html#cfn-backup-backupselection-backupselectionresourcetype-selectionname
            '''
            result = self._values.get("selection_name")
            assert result is not None, "Required property 'selection_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def list_of_tags(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBackupSelection.ConditionResourceTypeProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnBackupSelection.BackupSelectionResourceTypeProperty.ListOfTags``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-backupselectionresourcetype.html#cfn-backup-backupselection-backupselectionresourcetype-listoftags
            '''
            result = self._values.get("list_of_tags")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBackupSelection.ConditionResourceTypeProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def resources(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnBackupSelection.BackupSelectionResourceTypeProperty.Resources``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-backupselectionresourcetype.html#cfn-backup-backupselection-backupselectionresourcetype-resources
            '''
            result = self._values.get("resources")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BackupSelectionResourceTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_backup.CfnBackupSelection.ConditionResourceTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "condition_key": "conditionKey",
            "condition_type": "conditionType",
            "condition_value": "conditionValue",
        },
    )
    class ConditionResourceTypeProperty:
        def __init__(
            self,
            *,
            condition_key: builtins.str,
            condition_type: builtins.str,
            condition_value: builtins.str,
        ) -> None:
            '''
            :param condition_key: ``CfnBackupSelection.ConditionResourceTypeProperty.ConditionKey``.
            :param condition_type: ``CfnBackupSelection.ConditionResourceTypeProperty.ConditionType``.
            :param condition_value: ``CfnBackupSelection.ConditionResourceTypeProperty.ConditionValue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-conditionresourcetype.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "condition_key": condition_key,
                "condition_type": condition_type,
                "condition_value": condition_value,
            }

        @builtins.property
        def condition_key(self) -> builtins.str:
            '''``CfnBackupSelection.ConditionResourceTypeProperty.ConditionKey``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-conditionresourcetype.html#cfn-backup-backupselection-conditionresourcetype-conditionkey
            '''
            result = self._values.get("condition_key")
            assert result is not None, "Required property 'condition_key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def condition_type(self) -> builtins.str:
            '''``CfnBackupSelection.ConditionResourceTypeProperty.ConditionType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-conditionresourcetype.html#cfn-backup-backupselection-conditionresourcetype-conditiontype
            '''
            result = self._values.get("condition_type")
            assert result is not None, "Required property 'condition_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def condition_value(self) -> builtins.str:
            '''``CfnBackupSelection.ConditionResourceTypeProperty.ConditionValue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupselection-conditionresourcetype.html#cfn-backup-backupselection-conditionresourcetype-conditionvalue
            '''
            result = self._values.get("condition_value")
            assert result is not None, "Required property 'condition_value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConditionResourceTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_backup.CfnBackupSelectionProps",
    jsii_struct_bases=[],
    name_mapping={
        "backup_plan_id": "backupPlanId",
        "backup_selection": "backupSelection",
    },
)
class CfnBackupSelectionProps:
    def __init__(
        self,
        *,
        backup_plan_id: builtins.str,
        backup_selection: typing.Union[CfnBackupSelection.BackupSelectionResourceTypeProperty, _IResolvable_a771d0ef],
    ) -> None:
        '''Properties for defining a ``AWS::Backup::BackupSelection``.

        :param backup_plan_id: ``AWS::Backup::BackupSelection.BackupPlanId``.
        :param backup_selection: ``AWS::Backup::BackupSelection.BackupSelection``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupselection.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "backup_plan_id": backup_plan_id,
            "backup_selection": backup_selection,
        }

    @builtins.property
    def backup_plan_id(self) -> builtins.str:
        '''``AWS::Backup::BackupSelection.BackupPlanId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupselection.html#cfn-backup-backupselection-backupplanid
        '''
        result = self._values.get("backup_plan_id")
        assert result is not None, "Required property 'backup_plan_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def backup_selection(
        self,
    ) -> typing.Union[CfnBackupSelection.BackupSelectionResourceTypeProperty, _IResolvable_a771d0ef]:
        '''``AWS::Backup::BackupSelection.BackupSelection``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupselection.html#cfn-backup-backupselection-backupselection
        '''
        result = self._values.get("backup_selection")
        assert result is not None, "Required property 'backup_selection' is missing"
        return typing.cast(typing.Union[CfnBackupSelection.BackupSelectionResourceTypeProperty, _IResolvable_a771d0ef], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBackupSelectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnBackupVault(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_backup.CfnBackupVault",
):
    '''A CloudFormation ``AWS::Backup::BackupVault``.

    :cloudformationResource: AWS::Backup::BackupVault
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        backup_vault_name: builtins.str,
        access_policy: typing.Any = None,
        backup_vault_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        encryption_key_arn: typing.Optional[builtins.str] = None,
        notifications: typing.Optional[typing.Union["CfnBackupVault.NotificationObjectTypeProperty", _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::Backup::BackupVault``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param backup_vault_name: ``AWS::Backup::BackupVault.BackupVaultName``.
        :param access_policy: ``AWS::Backup::BackupVault.AccessPolicy``.
        :param backup_vault_tags: ``AWS::Backup::BackupVault.BackupVaultTags``.
        :param encryption_key_arn: ``AWS::Backup::BackupVault.EncryptionKeyArn``.
        :param notifications: ``AWS::Backup::BackupVault.Notifications``.
        '''
        props = CfnBackupVaultProps(
            backup_vault_name=backup_vault_name,
            access_policy=access_policy,
            backup_vault_tags=backup_vault_tags,
            encryption_key_arn=encryption_key_arn,
            notifications=notifications,
        )

        jsii.create(CfnBackupVault, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrBackupVaultArn")
    def attr_backup_vault_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: BackupVaultArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrBackupVaultArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrBackupVaultName")
    def attr_backup_vault_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: BackupVaultName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrBackupVaultName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="accessPolicy")
    def access_policy(self) -> typing.Any:
        '''``AWS::Backup::BackupVault.AccessPolicy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-accesspolicy
        '''
        return typing.cast(typing.Any, jsii.get(self, "accessPolicy"))

    @access_policy.setter
    def access_policy(self, value: typing.Any) -> None:
        jsii.set(self, "accessPolicy", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupVaultName")
    def backup_vault_name(self) -> builtins.str:
        '''``AWS::Backup::BackupVault.BackupVaultName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-backupvaultname
        '''
        return typing.cast(builtins.str, jsii.get(self, "backupVaultName"))

    @backup_vault_name.setter
    def backup_vault_name(self, value: builtins.str) -> None:
        jsii.set(self, "backupVaultName", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupVaultTags")
    def backup_vault_tags(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Backup::BackupVault.BackupVaultTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-backupvaulttags
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], jsii.get(self, "backupVaultTags"))

    @backup_vault_tags.setter
    def backup_vault_tags(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]],
    ) -> None:
        jsii.set(self, "backupVaultTags", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="encryptionKeyArn")
    def encryption_key_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::Backup::BackupVault.EncryptionKeyArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-encryptionkeyarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKeyArn"))

    @encryption_key_arn.setter
    def encryption_key_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "encryptionKeyArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="notifications")
    def notifications(
        self,
    ) -> typing.Optional[typing.Union["CfnBackupVault.NotificationObjectTypeProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Backup::BackupVault.Notifications``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-notifications
        '''
        return typing.cast(typing.Optional[typing.Union["CfnBackupVault.NotificationObjectTypeProperty", _IResolvable_a771d0ef]], jsii.get(self, "notifications"))

    @notifications.setter
    def notifications(
        self,
        value: typing.Optional[typing.Union["CfnBackupVault.NotificationObjectTypeProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "notifications", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_backup.CfnBackupVault.NotificationObjectTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "backup_vault_events": "backupVaultEvents",
            "sns_topic_arn": "snsTopicArn",
        },
    )
    class NotificationObjectTypeProperty:
        def __init__(
            self,
            *,
            backup_vault_events: typing.List[builtins.str],
            sns_topic_arn: builtins.str,
        ) -> None:
            '''
            :param backup_vault_events: ``CfnBackupVault.NotificationObjectTypeProperty.BackupVaultEvents``.
            :param sns_topic_arn: ``CfnBackupVault.NotificationObjectTypeProperty.SNSTopicArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupvault-notificationobjecttype.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "backup_vault_events": backup_vault_events,
                "sns_topic_arn": sns_topic_arn,
            }

        @builtins.property
        def backup_vault_events(self) -> typing.List[builtins.str]:
            '''``CfnBackupVault.NotificationObjectTypeProperty.BackupVaultEvents``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupvault-notificationobjecttype.html#cfn-backup-backupvault-notificationobjecttype-backupvaultevents
            '''
            result = self._values.get("backup_vault_events")
            assert result is not None, "Required property 'backup_vault_events' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def sns_topic_arn(self) -> builtins.str:
            '''``CfnBackupVault.NotificationObjectTypeProperty.SNSTopicArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-backup-backupvault-notificationobjecttype.html#cfn-backup-backupvault-notificationobjecttype-snstopicarn
            '''
            result = self._values.get("sns_topic_arn")
            assert result is not None, "Required property 'sns_topic_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationObjectTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_backup.CfnBackupVaultProps",
    jsii_struct_bases=[],
    name_mapping={
        "backup_vault_name": "backupVaultName",
        "access_policy": "accessPolicy",
        "backup_vault_tags": "backupVaultTags",
        "encryption_key_arn": "encryptionKeyArn",
        "notifications": "notifications",
    },
)
class CfnBackupVaultProps:
    def __init__(
        self,
        *,
        backup_vault_name: builtins.str,
        access_policy: typing.Any = None,
        backup_vault_tags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
        encryption_key_arn: typing.Optional[builtins.str] = None,
        notifications: typing.Optional[typing.Union[CfnBackupVault.NotificationObjectTypeProperty, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Backup::BackupVault``.

        :param backup_vault_name: ``AWS::Backup::BackupVault.BackupVaultName``.
        :param access_policy: ``AWS::Backup::BackupVault.AccessPolicy``.
        :param backup_vault_tags: ``AWS::Backup::BackupVault.BackupVaultTags``.
        :param encryption_key_arn: ``AWS::Backup::BackupVault.EncryptionKeyArn``.
        :param notifications: ``AWS::Backup::BackupVault.Notifications``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "backup_vault_name": backup_vault_name,
        }
        if access_policy is not None:
            self._values["access_policy"] = access_policy
        if backup_vault_tags is not None:
            self._values["backup_vault_tags"] = backup_vault_tags
        if encryption_key_arn is not None:
            self._values["encryption_key_arn"] = encryption_key_arn
        if notifications is not None:
            self._values["notifications"] = notifications

    @builtins.property
    def backup_vault_name(self) -> builtins.str:
        '''``AWS::Backup::BackupVault.BackupVaultName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-backupvaultname
        '''
        result = self._values.get("backup_vault_name")
        assert result is not None, "Required property 'backup_vault_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_policy(self) -> typing.Any:
        '''``AWS::Backup::BackupVault.AccessPolicy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-accesspolicy
        '''
        result = self._values.get("access_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def backup_vault_tags(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
        '''``AWS::Backup::BackupVault.BackupVaultTags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-backupvaulttags
        '''
        result = self._values.get("backup_vault_tags")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def encryption_key_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::Backup::BackupVault.EncryptionKeyArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-encryptionkeyarn
        '''
        result = self._values.get("encryption_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notifications(
        self,
    ) -> typing.Optional[typing.Union[CfnBackupVault.NotificationObjectTypeProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Backup::BackupVault.Notifications``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-backup-backupvault.html#cfn-backup-backupvault-notifications
        '''
        result = self._values.get("notifications")
        return typing.cast(typing.Optional[typing.Union[CfnBackupVault.NotificationObjectTypeProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBackupVaultProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_backup.IBackupPlan")
class IBackupPlan(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) A backup plan.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IBackupPlanProxy"]:
        return _IBackupPlanProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupPlanId")
    def backup_plan_id(self) -> builtins.str:
        '''(experimental) The identifier of the backup plan.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IBackupPlanProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''(experimental) A backup plan.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_backup.IBackupPlan"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupPlanId")
    def backup_plan_id(self) -> builtins.str:
        '''(experimental) The identifier of the backup plan.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "backupPlanId"))


@jsii.interface(jsii_type="monocdk.aws_backup.IBackupVault")
class IBackupVault(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) A backup vault.

    :stability: experimental
    '''

    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IBackupVaultProxy"]:
        return _IBackupVaultProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupVaultName")
    def backup_vault_name(self) -> builtins.str:
        '''(experimental) The name of a logical container where backups are stored.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IBackupVaultProxy(
    jsii.proxy_for(_IResource_8c1dbbbd) # type: ignore[misc]
):
    '''(experimental) A backup vault.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_backup.IBackupVault"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupVaultName")
    def backup_vault_name(self) -> builtins.str:
        '''(experimental) The name of a logical container where backups are stored.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "backupVaultName"))


@jsii.data_type(
    jsii_type="monocdk.aws_backup.TagCondition",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value", "operation": "operation"},
)
class TagCondition:
    def __init__(
        self,
        *,
        key: builtins.str,
        value: builtins.str,
        operation: typing.Optional["TagOperation"] = None,
    ) -> None:
        '''(experimental) A tag condition.

        :param key: (experimental) The key in a key-value pair. For example, in ``"ec2:ResourceTag/Department": "accounting"``, ``ec2:ResourceTag/Department`` is the key.
        :param value: (experimental) The value in a key-value pair. For example, in ``"ec2:ResourceTag/Department": "accounting"``, ``accounting`` is the value.
        :param operation: (experimental) An operation that is applied to a key-value pair used to filter resources in a selection. Default: STRING_EQUALS

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "key": key,
            "value": value,
        }
        if operation is not None:
            self._values["operation"] = operation

    @builtins.property
    def key(self) -> builtins.str:
        '''(experimental) The key in a key-value pair.

        For example, in ``"ec2:ResourceTag/Department": "accounting"``,
        ``ec2:ResourceTag/Department`` is the key.

        :stability: experimental
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''(experimental) The value in a key-value pair.

        For example, in ``"ec2:ResourceTag/Department": "accounting"``,
        ``accounting`` is the value.

        :stability: experimental
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operation(self) -> typing.Optional["TagOperation"]:
        '''(experimental) An operation that is applied to a key-value pair used to filter resources in a selection.

        :default: STRING_EQUALS

        :stability: experimental
        '''
        result = self._values.get("operation")
        return typing.cast(typing.Optional["TagOperation"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TagCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_backup.TagOperation")
class TagOperation(enum.Enum):
    '''(experimental) An operation that is applied to a key-value pair.

    :stability: experimental
    '''

    STRING_EQUALS = "STRING_EQUALS"
    '''(experimental) StringEquals.

    :stability: experimental
    '''
    DUMMY = "DUMMY"
    '''(experimental) Dummy member.

    :stability: experimental
    '''


@jsii.implements(IBackupPlan)
class BackupPlan(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_backup.BackupPlan",
):
    '''(experimental) A backup plan.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        backup_plan_name: typing.Optional[builtins.str] = None,
        backup_plan_rules: typing.Optional[typing.List[BackupPlanRule]] = None,
        backup_vault: typing.Optional[IBackupVault] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param backup_plan_name: (experimental) The display name of the backup plan. Default: - A CDK generated name
        :param backup_plan_rules: (experimental) Rules for the backup plan. Use ``addRule()`` to add rules after instantiation. Default: - use ``addRule()`` to add rules
        :param backup_vault: (experimental) The backup vault where backups are stored. Default: - use the vault defined at the rule level. If not defined a new common vault for the plan will be created

        :stability: experimental
        '''
        props = BackupPlanProps(
            backup_plan_name=backup_plan_name,
            backup_plan_rules=backup_plan_rules,
            backup_vault=backup_vault,
        )

        jsii.create(BackupPlan, self, [scope, id, props])

    @jsii.member(jsii_name="daily35DayRetention") # type: ignore[misc]
    @builtins.classmethod
    def daily35_day_retention(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        backup_vault: typing.Optional[IBackupVault] = None,
    ) -> "BackupPlan":
        '''(experimental) Daily with 35 day retention.

        :param scope: -
        :param id: -
        :param backup_vault: -

        :stability: experimental
        '''
        return typing.cast("BackupPlan", jsii.sinvoke(cls, "daily35DayRetention", [scope, id, backup_vault]))

    @jsii.member(jsii_name="dailyMonthly1YearRetention") # type: ignore[misc]
    @builtins.classmethod
    def daily_monthly1_year_retention(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        backup_vault: typing.Optional[IBackupVault] = None,
    ) -> "BackupPlan":
        '''(experimental) Daily and monthly with 1 year retention.

        :param scope: -
        :param id: -
        :param backup_vault: -

        :stability: experimental
        '''
        return typing.cast("BackupPlan", jsii.sinvoke(cls, "dailyMonthly1YearRetention", [scope, id, backup_vault]))

    @jsii.member(jsii_name="dailyWeeklyMonthly5YearRetention") # type: ignore[misc]
    @builtins.classmethod
    def daily_weekly_monthly5_year_retention(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        backup_vault: typing.Optional[IBackupVault] = None,
    ) -> "BackupPlan":
        '''(experimental) Daily, weekly and monthly with 5 year retention.

        :param scope: -
        :param id: -
        :param backup_vault: -

        :stability: experimental
        '''
        return typing.cast("BackupPlan", jsii.sinvoke(cls, "dailyWeeklyMonthly5YearRetention", [scope, id, backup_vault]))

    @jsii.member(jsii_name="dailyWeeklyMonthly7YearRetention") # type: ignore[misc]
    @builtins.classmethod
    def daily_weekly_monthly7_year_retention(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        backup_vault: typing.Optional[IBackupVault] = None,
    ) -> "BackupPlan":
        '''(experimental) Daily, weekly and monthly with 7 year retention.

        :param scope: -
        :param id: -
        :param backup_vault: -

        :stability: experimental
        '''
        return typing.cast("BackupPlan", jsii.sinvoke(cls, "dailyWeeklyMonthly7YearRetention", [scope, id, backup_vault]))

    @jsii.member(jsii_name="fromBackupPlanId") # type: ignore[misc]
    @builtins.classmethod
    def from_backup_plan_id(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        backup_plan_id: builtins.str,
    ) -> IBackupPlan:
        '''(experimental) Import an existing backup plan.

        :param scope: -
        :param id: -
        :param backup_plan_id: -

        :stability: experimental
        '''
        return typing.cast(IBackupPlan, jsii.sinvoke(cls, "fromBackupPlanId", [scope, id, backup_plan_id]))

    @jsii.member(jsii_name="addRule")
    def add_rule(self, rule: BackupPlanRule) -> None:
        '''(experimental) Adds a rule to a plan.

        :param rule: the rule to add.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addRule", [rule]))

    @jsii.member(jsii_name="addSelection")
    def add_selection(
        self,
        id: builtins.str,
        *,
        resources: typing.List[BackupResource],
        allow_restores: typing.Optional[builtins.bool] = None,
        backup_selection_name: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> BackupSelection:
        '''(experimental) Adds a selection to this plan.

        :param id: -
        :param resources: (experimental) The resources to backup. Use the helper static methods defined on ``BackupResource``.
        :param allow_restores: (experimental) Whether to automatically give restores permissions to the role that AWS Backup uses. If ``true``, the ``AWSBackupServiceRolePolicyForRestores`` managed policy will be attached to the role. Default: false
        :param backup_selection_name: (experimental) The name for this selection. Default: - a CDK generated name
        :param role: (experimental) The role that AWS Backup uses to authenticate when backuping or restoring the resources. The ``AWSBackupServiceRolePolicyForBackup`` managed policy will be attached to this role. Default: - a new role will be created

        :stability: experimental
        '''
        options = BackupSelectionOptions(
            resources=resources,
            allow_restores=allow_restores,
            backup_selection_name=backup_selection_name,
            role=role,
        )

        return typing.cast(BackupSelection, jsii.invoke(self, "addSelection", [id, options]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''(experimental) Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupPlanArn")
    def backup_plan_arn(self) -> builtins.str:
        '''(experimental) The ARN of the backup plan.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "backupPlanArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupPlanId")
    def backup_plan_id(self) -> builtins.str:
        '''(experimental) The identifier of the backup plan.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "backupPlanId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupVault")
    def backup_vault(self) -> IBackupVault:
        '''(experimental) The backup vault where backups are stored if not defined at the rule level.

        :stability: experimental
        '''
        return typing.cast(IBackupVault, jsii.get(self, "backupVault"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="versionId")
    def version_id(self) -> builtins.str:
        '''(experimental) Version Id.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "versionId"))


@jsii.implements(IBackupVault)
class BackupVault(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_backup.BackupVault",
):
    '''(experimental) A backup vault.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        access_policy: typing.Optional[_PolicyDocument_b5de5177] = None,
        backup_vault_name: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        notification_events: typing.Optional[typing.List[BackupVaultEvents]] = None,
        notification_topic: typing.Optional[_ITopic_465e36b9] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param access_policy: (experimental) A resource-based policy that is used to manage access permissions on the backup vault. Default: - access is not restricted
        :param backup_vault_name: (experimental) The name of a logical container where backups are stored. Backup vaults are identified by names that are unique to the account used to create them and the AWS Region where they are created. Default: - A CDK generated name
        :param encryption_key: (experimental) The server-side encryption key to use to protect your backups. Default: - an Amazon managed KMS key
        :param notification_events: (experimental) The vault events to send. Default: - all vault events if ``notificationTopic`` is defined
        :param notification_topic: (experimental) A SNS topic to send vault events to. Default: - no notifications
        :param removal_policy: (experimental) The removal policy to apply to the vault. Note that removing a vault that contains recovery points will fail. Default: RemovalPolicy.RETAIN

        :stability: experimental
        '''
        props = BackupVaultProps(
            access_policy=access_policy,
            backup_vault_name=backup_vault_name,
            encryption_key=encryption_key,
            notification_events=notification_events,
            notification_topic=notification_topic,
            removal_policy=removal_policy,
        )

        jsii.create(BackupVault, self, [scope, id, props])

    @jsii.member(jsii_name="fromBackupVaultName") # type: ignore[misc]
    @builtins.classmethod
    def from_backup_vault_name(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        backup_vault_name: builtins.str,
    ) -> IBackupVault:
        '''(experimental) Import an existing backup vault.

        :param scope: -
        :param id: -
        :param backup_vault_name: -

        :stability: experimental
        '''
        return typing.cast(IBackupVault, jsii.sinvoke(cls, "fromBackupVaultName", [scope, id, backup_vault_name]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupVaultArn")
    def backup_vault_arn(self) -> builtins.str:
        '''(experimental) The ARN of the backup vault.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "backupVaultArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="backupVaultName")
    def backup_vault_name(self) -> builtins.str:
        '''(experimental) The name of a logical container where backups are stored.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "backupVaultName"))


__all__ = [
    "BackupPlan",
    "BackupPlanProps",
    "BackupPlanRule",
    "BackupPlanRuleProps",
    "BackupResource",
    "BackupSelection",
    "BackupSelectionOptions",
    "BackupSelectionProps",
    "BackupVault",
    "BackupVaultEvents",
    "BackupVaultProps",
    "CfnBackupPlan",
    "CfnBackupPlanProps",
    "CfnBackupSelection",
    "CfnBackupSelectionProps",
    "CfnBackupVault",
    "CfnBackupVaultProps",
    "IBackupPlan",
    "IBackupVault",
    "TagCondition",
    "TagOperation",
]

publication.publish()
