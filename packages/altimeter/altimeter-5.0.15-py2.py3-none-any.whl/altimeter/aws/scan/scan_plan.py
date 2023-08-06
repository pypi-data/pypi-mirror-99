"""A ScanPlan defines how to scan a set of accounts."""
from typing import Optional, Tuple

from altimeter.aws.auth.accessor import Accessor
from altimeter.core.base_model import BaseImmutableModel


class AccountScanPlan(BaseImmutableModel):
    """An AccountScanPlan defines how to scan an account.

    Arguments:
        account_id: account id to scan
        regions: regions to scan
        accessor: Accessor to use to access the accounts
    """

    account_id: str
    regions: Tuple[str, ...]
    accessor: Accessor


class ScanPlan(BaseImmutableModel):
    """A ScanPlan defines how to scan a set of accounts.

    Arguments:
        account_ids: account ids to scan
        regions: regions to scan
        accessor: Accessor to use to access the accounts
    """

    account_ids: Tuple[str, ...]
    regions: Tuple[str, ...]
    accessor: Accessor

    def build_account_scan_plans(
        self, account_id_blacklist: Optional[Tuple[str, ...]] = None
    ) -> Tuple[AccountScanPlan, ...]:
        if account_id_blacklist is None:
            account_id_blacklist = tuple()
        return tuple(
            [
                AccountScanPlan(account_id=account_id, regions=self.regions, accessor=self.accessor)
                for account_id in self.account_ids
                if account_id not in account_id_blacklist
            ]
        )
