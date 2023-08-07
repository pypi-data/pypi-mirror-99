'''
# AWS::AuditManager Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_auditmanager as auditmanager
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

import aws_cdk.core


@jsii.implements(aws_cdk.core.IInspectable)
class CfnAssessment(
    aws_cdk.core.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-auditmanager.CfnAssessment",
):
    '''A CloudFormation ``AWS::AuditManager::Assessment``.

    :cloudformationResource: AWS::AuditManager::Assessment
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html
    '''

    def __init__(
        self,
        scope_: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        assessment_reports_destination: typing.Optional[typing.Union["CfnAssessment.AssessmentReportsDestinationProperty", aws_cdk.core.IResolvable]] = None,
        aws_account: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAssessment.AWSAccountProperty"]] = None,
        description: typing.Optional[builtins.str] = None,
        framework_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        roles: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAssessment.RoleProperty"]]]] = None,
        scope: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAssessment.ScopeProperty"]] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Create a new ``AWS::AuditManager::Assessment``.

        :param scope_: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param assessment_reports_destination: ``AWS::AuditManager::Assessment.AssessmentReportsDestination``.
        :param aws_account: ``AWS::AuditManager::Assessment.AwsAccount``.
        :param description: ``AWS::AuditManager::Assessment.Description``.
        :param framework_id: ``AWS::AuditManager::Assessment.FrameworkId``.
        :param name: ``AWS::AuditManager::Assessment.Name``.
        :param roles: ``AWS::AuditManager::Assessment.Roles``.
        :param scope: ``AWS::AuditManager::Assessment.Scope``.
        :param status: ``AWS::AuditManager::Assessment.Status``.
        :param tags: ``AWS::AuditManager::Assessment.Tags``.
        '''
        props = CfnAssessmentProps(
            assessment_reports_destination=assessment_reports_destination,
            aws_account=aws_account,
            description=description,
            framework_id=framework_id,
            name=name,
            roles=roles,
            scope=scope,
            status=status,
            tags=tags,
        )

        jsii.create(CfnAssessment, self, [scope_, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
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
    @jsii.member(jsii_name="attrAssessmentId")
    def attr_assessment_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: AssessmentId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssessmentId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> aws_cdk.core.IResolvable:
        '''
        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(aws_cdk.core.IResolvable, jsii.get(self, "attrCreationTime"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrDelegations")
    def attr_delegations(self) -> aws_cdk.core.IResolvable:
        '''
        :cloudformationAttribute: Delegations
        '''
        return typing.cast(aws_cdk.core.IResolvable, jsii.get(self, "attrDelegations"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrFrameworkId")
    def attr_framework_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: FrameworkId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFrameworkId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        '''``AWS::AuditManager::Assessment.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-tags
        '''
        return typing.cast(aws_cdk.core.TagManager, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="assessmentReportsDestination")
    def assessment_reports_destination(
        self,
    ) -> typing.Optional[typing.Union["CfnAssessment.AssessmentReportsDestinationProperty", aws_cdk.core.IResolvable]]:
        '''``AWS::AuditManager::Assessment.AssessmentReportsDestination``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-assessmentreportsdestination
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAssessment.AssessmentReportsDestinationProperty", aws_cdk.core.IResolvable]], jsii.get(self, "assessmentReportsDestination"))

    @assessment_reports_destination.setter
    def assessment_reports_destination(
        self,
        value: typing.Optional[typing.Union["CfnAssessment.AssessmentReportsDestinationProperty", aws_cdk.core.IResolvable]],
    ) -> None:
        jsii.set(self, "assessmentReportsDestination", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="awsAccount")
    def aws_account(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAssessment.AWSAccountProperty"]]:
        '''``AWS::AuditManager::Assessment.AwsAccount``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-awsaccount
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAssessment.AWSAccountProperty"]], jsii.get(self, "awsAccount"))

    @aws_account.setter
    def aws_account(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAssessment.AWSAccountProperty"]],
    ) -> None:
        jsii.set(self, "awsAccount", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::AuditManager::Assessment.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="frameworkId")
    def framework_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::AuditManager::Assessment.FrameworkId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-frameworkid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frameworkId"))

    @framework_id.setter
    def framework_id(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "frameworkId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::AuditManager::Assessment.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roles")
    def roles(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAssessment.RoleProperty"]]]]:
        '''``AWS::AuditManager::Assessment.Roles``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-roles
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAssessment.RoleProperty"]]]], jsii.get(self, "roles"))

    @roles.setter
    def roles(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAssessment.RoleProperty"]]]],
    ) -> None:
        jsii.set(self, "roles", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scope")
    def scope(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAssessment.ScopeProperty"]]:
        '''``AWS::AuditManager::Assessment.Scope``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-scope
        '''
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAssessment.ScopeProperty"]], jsii.get(self, "scope"))

    @scope.setter
    def scope(
        self,
        value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAssessment.ScopeProperty"]],
    ) -> None:
        jsii.set(self, "scope", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        '''``AWS::AuditManager::Assessment.Status``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-status
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "status"))

    @status.setter
    def status(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "status", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-auditmanager.CfnAssessment.AWSAccountProperty",
        jsii_struct_bases=[],
        name_mapping={"email_address": "emailAddress", "id": "id", "name": "name"},
    )
    class AWSAccountProperty:
        def __init__(
            self,
            *,
            email_address: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param email_address: ``CfnAssessment.AWSAccountProperty.EmailAddress``.
            :param id: ``CfnAssessment.AWSAccountProperty.Id``.
            :param name: ``CfnAssessment.AWSAccountProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-awsaccount.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if email_address is not None:
                self._values["email_address"] = email_address
            if id is not None:
                self._values["id"] = id
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def email_address(self) -> typing.Optional[builtins.str]:
            '''``CfnAssessment.AWSAccountProperty.EmailAddress``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-awsaccount.html#cfn-auditmanager-assessment-awsaccount-emailaddress
            '''
            result = self._values.get("email_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''``CfnAssessment.AWSAccountProperty.Id``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-awsaccount.html#cfn-auditmanager-assessment-awsaccount-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''``CfnAssessment.AWSAccountProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-awsaccount.html#cfn-auditmanager-assessment-awsaccount-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AWSAccountProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-auditmanager.CfnAssessment.AWSServiceProperty",
        jsii_struct_bases=[],
        name_mapping={"service_name": "serviceName"},
    )
    class AWSServiceProperty:
        def __init__(
            self,
            *,
            service_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param service_name: ``CfnAssessment.AWSServiceProperty.ServiceName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-awsservice.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if service_name is not None:
                self._values["service_name"] = service_name

        @builtins.property
        def service_name(self) -> typing.Optional[builtins.str]:
            '''``CfnAssessment.AWSServiceProperty.ServiceName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-awsservice.html#cfn-auditmanager-assessment-awsservice-servicename
            '''
            result = self._values.get("service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AWSServiceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-auditmanager.CfnAssessment.AssessmentReportsDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination": "destination",
            "destination_type": "destinationType",
        },
    )
    class AssessmentReportsDestinationProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[builtins.str] = None,
            destination_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param destination: ``CfnAssessment.AssessmentReportsDestinationProperty.Destination``.
            :param destination_type: ``CfnAssessment.AssessmentReportsDestinationProperty.DestinationType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-assessmentreportsdestination.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination
            if destination_type is not None:
                self._values["destination_type"] = destination_type

        @builtins.property
        def destination(self) -> typing.Optional[builtins.str]:
            '''``CfnAssessment.AssessmentReportsDestinationProperty.Destination``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-assessmentreportsdestination.html#cfn-auditmanager-assessment-assessmentreportsdestination-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def destination_type(self) -> typing.Optional[builtins.str]:
            '''``CfnAssessment.AssessmentReportsDestinationProperty.DestinationType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-assessmentreportsdestination.html#cfn-auditmanager-assessment-assessmentreportsdestination-destinationtype
            '''
            result = self._values.get("destination_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssessmentReportsDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-auditmanager.CfnAssessment.DelegationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "assessment_id": "assessmentId",
            "assessment_name": "assessmentName",
            "comment": "comment",
            "control_set_id": "controlSetId",
            "created_by": "createdBy",
            "creation_time": "creationTime",
            "id": "id",
            "last_updated": "lastUpdated",
            "role_arn": "roleArn",
            "role_type": "roleType",
            "status": "status",
        },
    )
    class DelegationProperty:
        def __init__(
            self,
            *,
            assessment_id: typing.Optional[builtins.str] = None,
            assessment_name: typing.Optional[builtins.str] = None,
            comment: typing.Optional[builtins.str] = None,
            control_set_id: typing.Optional[builtins.str] = None,
            created_by: typing.Optional[builtins.str] = None,
            creation_time: typing.Optional[jsii.Number] = None,
            id: typing.Optional[builtins.str] = None,
            last_updated: typing.Optional[jsii.Number] = None,
            role_arn: typing.Optional[builtins.str] = None,
            role_type: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param assessment_id: ``CfnAssessment.DelegationProperty.AssessmentId``.
            :param assessment_name: ``CfnAssessment.DelegationProperty.AssessmentName``.
            :param comment: ``CfnAssessment.DelegationProperty.Comment``.
            :param control_set_id: ``CfnAssessment.DelegationProperty.ControlSetId``.
            :param created_by: ``CfnAssessment.DelegationProperty.CreatedBy``.
            :param creation_time: ``CfnAssessment.DelegationProperty.CreationTime``.
            :param id: ``CfnAssessment.DelegationProperty.Id``.
            :param last_updated: ``CfnAssessment.DelegationProperty.LastUpdated``.
            :param role_arn: ``CfnAssessment.DelegationProperty.RoleArn``.
            :param role_type: ``CfnAssessment.DelegationProperty.RoleType``.
            :param status: ``CfnAssessment.DelegationProperty.Status``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if assessment_id is not None:
                self._values["assessment_id"] = assessment_id
            if assessment_name is not None:
                self._values["assessment_name"] = assessment_name
            if comment is not None:
                self._values["comment"] = comment
            if control_set_id is not None:
                self._values["control_set_id"] = control_set_id
            if created_by is not None:
                self._values["created_by"] = created_by
            if creation_time is not None:
                self._values["creation_time"] = creation_time
            if id is not None:
                self._values["id"] = id
            if last_updated is not None:
                self._values["last_updated"] = last_updated
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if role_type is not None:
                self._values["role_type"] = role_type
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def assessment_id(self) -> typing.Optional[builtins.str]:
            '''``CfnAssessment.DelegationProperty.AssessmentId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-assessmentid
            '''
            result = self._values.get("assessment_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def assessment_name(self) -> typing.Optional[builtins.str]:
            '''``CfnAssessment.DelegationProperty.AssessmentName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-assessmentname
            '''
            result = self._values.get("assessment_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def comment(self) -> typing.Optional[builtins.str]:
            '''``CfnAssessment.DelegationProperty.Comment``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-comment
            '''
            result = self._values.get("comment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def control_set_id(self) -> typing.Optional[builtins.str]:
            '''``CfnAssessment.DelegationProperty.ControlSetId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-controlsetid
            '''
            result = self._values.get("control_set_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def created_by(self) -> typing.Optional[builtins.str]:
            '''``CfnAssessment.DelegationProperty.CreatedBy``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-createdby
            '''
            result = self._values.get("created_by")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def creation_time(self) -> typing.Optional[jsii.Number]:
            '''``CfnAssessment.DelegationProperty.CreationTime``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-creationtime
            '''
            result = self._values.get("creation_time")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''``CfnAssessment.DelegationProperty.Id``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def last_updated(self) -> typing.Optional[jsii.Number]:
            '''``CfnAssessment.DelegationProperty.LastUpdated``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-lastupdated
            '''
            result = self._values.get("last_updated")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnAssessment.DelegationProperty.RoleArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_type(self) -> typing.Optional[builtins.str]:
            '''``CfnAssessment.DelegationProperty.RoleType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-roletype
            '''
            result = self._values.get("role_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''``CfnAssessment.DelegationProperty.Status``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DelegationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-auditmanager.CfnAssessment.RoleProperty",
        jsii_struct_bases=[],
        name_mapping={"role_arn": "roleArn", "role_type": "roleType"},
    )
    class RoleProperty:
        def __init__(
            self,
            *,
            role_arn: typing.Optional[builtins.str] = None,
            role_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param role_arn: ``CfnAssessment.RoleProperty.RoleArn``.
            :param role_type: ``CfnAssessment.RoleProperty.RoleType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-role.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if role_type is not None:
                self._values["role_type"] = role_type

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''``CfnAssessment.RoleProperty.RoleArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-role.html#cfn-auditmanager-assessment-role-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_type(self) -> typing.Optional[builtins.str]:
            '''``CfnAssessment.RoleProperty.RoleType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-role.html#cfn-auditmanager-assessment-role-roletype
            '''
            result = self._values.get("role_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RoleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-auditmanager.CfnAssessment.ScopeProperty",
        jsii_struct_bases=[],
        name_mapping={"aws_accounts": "awsAccounts", "aws_services": "awsServices"},
    )
    class ScopeProperty:
        def __init__(
            self,
            *,
            aws_accounts: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAssessment.AWSAccountProperty"]]]] = None,
            aws_services: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAssessment.AWSServiceProperty"]]]] = None,
        ) -> None:
            '''
            :param aws_accounts: ``CfnAssessment.ScopeProperty.AwsAccounts``.
            :param aws_services: ``CfnAssessment.ScopeProperty.AwsServices``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-scope.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if aws_accounts is not None:
                self._values["aws_accounts"] = aws_accounts
            if aws_services is not None:
                self._values["aws_services"] = aws_services

        @builtins.property
        def aws_accounts(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAssessment.AWSAccountProperty"]]]]:
            '''``CfnAssessment.ScopeProperty.AwsAccounts``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-scope.html#cfn-auditmanager-assessment-scope-awsaccounts
            '''
            result = self._values.get("aws_accounts")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAssessment.AWSAccountProperty"]]]], result)

        @builtins.property
        def aws_services(
            self,
        ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAssessment.AWSServiceProperty"]]]]:
            '''``CfnAssessment.ScopeProperty.AwsServices``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-scope.html#cfn-auditmanager-assessment-scope-awsservices
            '''
            result = self._values.get("aws_services")
            return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnAssessment.AWSServiceProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScopeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-auditmanager.CfnAssessmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "assessment_reports_destination": "assessmentReportsDestination",
        "aws_account": "awsAccount",
        "description": "description",
        "framework_id": "frameworkId",
        "name": "name",
        "roles": "roles",
        "scope": "scope",
        "status": "status",
        "tags": "tags",
    },
)
class CfnAssessmentProps:
    def __init__(
        self,
        *,
        assessment_reports_destination: typing.Optional[typing.Union[CfnAssessment.AssessmentReportsDestinationProperty, aws_cdk.core.IResolvable]] = None,
        aws_account: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnAssessment.AWSAccountProperty]] = None,
        description: typing.Optional[builtins.str] = None,
        framework_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        roles: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnAssessment.RoleProperty]]]] = None,
        scope: typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnAssessment.ScopeProperty]] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::AuditManager::Assessment``.

        :param assessment_reports_destination: ``AWS::AuditManager::Assessment.AssessmentReportsDestination``.
        :param aws_account: ``AWS::AuditManager::Assessment.AwsAccount``.
        :param description: ``AWS::AuditManager::Assessment.Description``.
        :param framework_id: ``AWS::AuditManager::Assessment.FrameworkId``.
        :param name: ``AWS::AuditManager::Assessment.Name``.
        :param roles: ``AWS::AuditManager::Assessment.Roles``.
        :param scope: ``AWS::AuditManager::Assessment.Scope``.
        :param status: ``AWS::AuditManager::Assessment.Status``.
        :param tags: ``AWS::AuditManager::Assessment.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if assessment_reports_destination is not None:
            self._values["assessment_reports_destination"] = assessment_reports_destination
        if aws_account is not None:
            self._values["aws_account"] = aws_account
        if description is not None:
            self._values["description"] = description
        if framework_id is not None:
            self._values["framework_id"] = framework_id
        if name is not None:
            self._values["name"] = name
        if roles is not None:
            self._values["roles"] = roles
        if scope is not None:
            self._values["scope"] = scope
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def assessment_reports_destination(
        self,
    ) -> typing.Optional[typing.Union[CfnAssessment.AssessmentReportsDestinationProperty, aws_cdk.core.IResolvable]]:
        '''``AWS::AuditManager::Assessment.AssessmentReportsDestination``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-assessmentreportsdestination
        '''
        result = self._values.get("assessment_reports_destination")
        return typing.cast(typing.Optional[typing.Union[CfnAssessment.AssessmentReportsDestinationProperty, aws_cdk.core.IResolvable]], result)

    @builtins.property
    def aws_account(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnAssessment.AWSAccountProperty]]:
        '''``AWS::AuditManager::Assessment.AwsAccount``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-awsaccount
        '''
        result = self._values.get("aws_account")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnAssessment.AWSAccountProperty]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::AuditManager::Assessment.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def framework_id(self) -> typing.Optional[builtins.str]:
        '''``AWS::AuditManager::Assessment.FrameworkId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-frameworkid
        '''
        result = self._values.get("framework_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::AuditManager::Assessment.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def roles(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnAssessment.RoleProperty]]]]:
        '''``AWS::AuditManager::Assessment.Roles``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-roles
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, CfnAssessment.RoleProperty]]]], result)

    @builtins.property
    def scope(
        self,
    ) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnAssessment.ScopeProperty]]:
        '''``AWS::AuditManager::Assessment.Scope``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-scope
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[typing.Union[aws_cdk.core.IResolvable, CfnAssessment.ScopeProperty]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''``AWS::AuditManager::Assessment.Status``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        '''``AWS::AuditManager::Assessment.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[aws_cdk.core.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssessmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAssessment",
    "CfnAssessmentProps",
]

publication.publish()
