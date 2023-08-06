"""Resource representing an AWS Account as viewed in Orgs. This tags
on things like the Org itself and the OU in which this account lives."""
from typing import Dict, Type

from botocore.client import BaseClient

from altimeter.aws.resource.resource_spec import ListFromAWSResult
from altimeter.aws.resource.organizations import (
    OrganizationsResourceSpec,
    recursively_get_ou_details_for_parent,
)
from altimeter.aws.resource.organizations.org import OrgResourceSpec
from altimeter.aws.resource.organizations.ou import OUResourceSpec
from altimeter.aws.resource.unscanned_account import UnscannedAccountResourceSpec
from altimeter.core.graph.field.resource_link_field import ResourceLinkField
from altimeter.core.graph.field.scalar_field import ScalarField
from altimeter.core.graph.schema import Schema


class OrgsAccountResourceSpec(OrganizationsResourceSpec):
    """Resource representing an AWS Account as viewed in Orgs."""

    type_name = "account"
    schema = Schema(
        ScalarField("Name"),
        ScalarField("Status"),
        ScalarField("JoinedTimestamp"),
        ScalarField("Email"),
        ScalarField("Id", alti_key="account_id"),
        ResourceLinkField("OrganizationArn", OrgResourceSpec, value_is_id=True),
        ResourceLinkField("OUArn", OUResourceSpec, value_is_id=True),
    )
    allow_clobber = [UnscannedAccountResourceSpec]

    @classmethod
    def get_full_type_name(cls: Type["OrgsAccountResourceSpec"]) -> str:
        return f"{cls.provider_name}:{cls.type_name}"

    @classmethod
    def list_from_aws(
        cls: Type["OrgsAccountResourceSpec"], client: BaseClient, account_id: str, region: str
    ) -> ListFromAWSResult:
        """Return a dict of dicts of the format:

            {'ou_1_arn': {org_1_dict},
             'ou_2_arn': {org_2_dict},
             ...}

        Where the dicts represent results from list_accounts_for_parent."""
        org_resp = client.describe_organization()
        org_arn = org_resp["Organization"]["Arn"]
        # get all ou ids and arns as a dict
        ou_ids_arns = get_ou_ids_arns(client)
        # now look up accounts for each ou
        orgs_accounts = {}
        accounts_paginator = client.get_paginator("list_accounts_for_parent")
        for parent_id, parent_arn in ou_ids_arns.items():
            for accounts_resp in accounts_paginator.paginate(ParentId=parent_id):
                for account in accounts_resp["Accounts"]:
                    account_id = account["Id"]
                    account_arn = f"arn:aws::::account/{account_id}"
                    account["OrganizationArn"] = org_arn
                    account["OUArn"] = parent_arn
                    orgs_accounts[account_arn] = account
        return ListFromAWSResult(resources=orgs_accounts)


def get_ou_ids_arns(client: BaseClient) -> Dict[str, str]:
    """Build and return a dict of OU ids to arns"""
    ou_ids_arns = {}
    paginator = client.get_paginator("list_roots")
    for resp in paginator.paginate():
        for root in resp["Roots"]:
            root_id, root_arn = root["Id"], root["Arn"]
            ou_ids_arns[root_id] = root_arn
            root_path = f"/{root['Name']}"
            ou_details = recursively_get_ou_details_for_parent(
                client=client, parent_id=root_id, parent_path=root_path
            )
            for ou_detail in ou_details:
                ou_id, ou_arn = ou_detail["Id"], ou_detail["Arn"]
                ou_ids_arns[ou_id] = ou_arn
    return ou_ids_arns
