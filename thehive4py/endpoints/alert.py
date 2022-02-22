from typing import List

from thehive4py.endpoints._base import EndpointBase
from thehive4py.query import QueryExpr
from thehive4py.query.filters import FilterExpr
from thehive4py.query.page import Paginate
from thehive4py.query.sort import SortExpr
from thehive4py.types.alert import (
    InputAlert,
    InputBulkUpdateAlert,
    InputUpdateAlert,
    OutputAlert,
)
from thehive4py.types.case import OutputCase
from thehive4py.types.observable import InputObservable, OutputObservable


class AlertEndpoint(EndpointBase):
    def create(self, alert: InputAlert) -> OutputAlert:
        return self._session.make_request("POST", path="/api/v1/alert", json=alert)

    def get(self, alert_id: str) -> OutputAlert:
        return self._session.make_request("GET", path=f"/api/v1/alert/{alert_id}")

    def update(self, alert_id: str, fields: InputUpdateAlert) -> None:
        return self._session.make_request(
            "PATCH", path=f"/api/v1/alert/{alert_id}", json=fields
        )

    def delete(self, alert_id: str) -> None:
        return self._session.make_request("DELETE", path=f"/api/v1/alert/{alert_id}")

    def bulk_update(self, fields: InputBulkUpdateAlert) -> None:
        return self._session.make_request(
            "PATCH", path="/api/v1/alert/_bulk", json=fields
        )

    def bulk_delete(self, ids: List[str]) -> None:
        return self._session.make_request(
            "POST", path="/api/v1/alert/delete/_bulk", json={"ids": ids}
        )

    def follow(self, alert_id: str) -> None:
        self._session.make_request("POST", path=f"/api/v1/alert/{alert_id}/follow")

    def unfollow(self, alert_id: str) -> None:
        self._session.make_request("POST", path=f"/api/v1/alert/{alert_id}/unfollow")

    def promote_to_case(self, alert_id: str) -> OutputCase:
        return self._session.make_request(
            "POST",
            path=f"/api/v1/alert/{alert_id}/case",
            json={"placholder": ""},  # TODO: replace with optional body definition
        )

    def create_observable(
        self, alert_id: str, observable: InputObservable
    ) -> List[OutputObservable]:
        # TODO: implement bulk creation with isZip
        return self._session.make_request(
            "POST", path=f"/api/v1/alert/{alert_id}/artifact", json=observable
        )

    def merge_into_case(self, alert_id: str, case_id: str) -> OutputCase:
        return self._session.make_request(
            "POST", path=f"/api/v1/alert/{alert_id}/merge/{case_id}"
        )

    def bulk_merge_into_case(self, case_id: str, alert_ids: List[str]) -> OutputCase:
        return self._session.make_request(
            "POST",
            path="/api/v1/alert/merge/_bulk",
            json={"caseId": case_id, "alertIds": alert_ids},
        )

    def find(
        self,
        filters: FilterExpr = None,
        sortby: SortExpr = None,
        paginate: Paginate = None,
    ) -> List[OutputAlert]:
        query: QueryExpr = [
            {"_name": "listAlert"},
            *self._build_subquery(filters=filters, sortby=sortby, paginate=paginate),
        ]

        return self._session.make_request(
            "POST",
            path="/api/v1/query",
            params={"name": "alerts"},
            json={"query": query},
        )

    def count(self, filters: FilterExpr = None) -> int:

        query: QueryExpr = [
            {"_name": "listAlert"},
            *self._build_subquery(filters=filters),
            {"_name": "count"},
        ]

        return self._session.make_request(
            "POST",
            path="/api/v1/query",
            params={"name": "alerts.count"},
            json={"query": query},
        )

    def find_observables(
        self,
        alert_id: str,
        filters: FilterExpr = None,
        sortby: SortExpr = None,
        paginate: Paginate = None,
    ) -> List[OutputObservable]:
        query: QueryExpr = [
            {"_name": "getAlert", "idOrName": alert_id},
            {"_name": "observables"},
            *self._build_subquery(filters=filters, sortby=sortby, paginate=paginate),
        ]
        return self._session.make_request(
            "POST",
            path="/api/v1/query",
            params={"name": "alert-observables"},
            json={"query": query},
        )
