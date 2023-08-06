from datetime import datetime
from typing import Optional

from kisters.water.rest_client import RESTClient

from ..network import Network


class NetworkStore:
    _resource = "rest", "networks"

    def __init__(self, client: RESTClient):
        self._client = client

    def list_networks(self):
        return self._client.get(self._resource)

    def get_network(
        self,
        network_uid: str,
        dt: Optional[datetime] = None,
        group_uid: Optional[str] = None,
    ):
        return Network(network_uid, self._client, dt=dt, group_uid=group_uid)
