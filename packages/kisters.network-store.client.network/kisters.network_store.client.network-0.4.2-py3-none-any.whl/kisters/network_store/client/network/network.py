from datetime import datetime
from typing import List, Optional

from kisters.network_store.model_library.base import (
    BaseGroup,
    BaseLink,
    BaseNode,
    LocationExtent,
    LocationSet,
)
from kisters.network_store.model_library.util import element_from_dict
from kisters.water.rest_client import RESTClient


class Network:
    """Access the network store API

    Provideds convenient methods to access the network store API from python
    scripts and adapters.

    :param name:
        ID of the network to use
    :param client:
        An instance of RESTClient or equivalent
    :param drop_existing:
        Delete any existing elements (deprecated- use `network.drop()`)
    :param dt:
        Optional default dt that will be used for all queries
    """

    _resource = "rest", "networks"

    def __init__(
        self,
        name: str,
        client: RESTClient,
        drop_existing: bool = False,  # Deprecated- use `network.drop()`
        dt: Optional[datetime] = None,
        group_uid: Optional[str] = None,
    ):
        self._name = name
        self._client = client
        self._network_resource = (*self._resource, self.name)
        if drop_existing:
            self.drop()
        self._default_dt = dt
        self._default_group_uid = group_uid

    def initialize(
        self,
        nodes: Optional[List[BaseNode]] = None,
        links: Optional[List[BaseLink]] = None,
        groups: Optional[List[BaseGroup]] = None,
    ):
        """Clear a network, optionally setting new links, nodes, and groups

        Note that this does not purge the network history- older versions of
        networks can be revisited even after being initialised. Useful for
        defining a complete network in one call.

        :param nodes:
            Optional list of nodes
        :param links:
            Optional list of links
        :param groups:
            Optional list of groups
        """
        nodes = ",".join((e.json(exclude_none=True) for e in nodes)) if nodes else ""
        links = ",".join((e.json(exclude_none=True) for e in links)) if links else ""
        groups = ",".join((e.json(exclude_none=True) for e in groups)) if groups else ""
        network_data = f'{{"nodes":[{nodes}],"links":[{links}],"groups":[{groups}]}}'
        self._client.post(
            self._network_resource,
            data=network_data,
            headers={"content-type": "application/json"},
        )

    def get_extent(
        self,
        location_set: LocationSet = LocationSet.GEOGRAPHIC,
        *,
        dt: Optional[datetime] = None,
    ) -> LocationExtent:
        """Gets the min and max values over all node locations

        Note that at the moment, only nodes are considered. Link vertices are
        ignored.

        :param location_set:
            The name of the location attribute, one of the LocationSet enum
        :param dt:
            Optional timestamp to access a historical version of the model
        """
        params = {"location_set": location_set}
        dt = dt or self._default_dt
        if dt:
            params["datetime"] = dt.isoformat()
        extents = self._client.get((*self._network_resource, "extent"), params=params)
        return LocationExtent.parse_obj(extents)

    def get_links(
        self,
        uids: Optional[List[str]] = None,
        display_names: Optional[List[str]] = None,
        element_class: Optional[str] = None,
        group_uids: Optional[List[str]] = None,
        adjacent_nodes: Optional[List[str]] = None,
        only_interior: Optional[bool] = True,
        include_subgroups: Optional[bool] = False,
        dt: Optional[datetime] = None,
    ) -> List[BaseLink]:
        """Gets an iterable of links

        Gets the the links in the network. The links are filterable by optional
        kwargs.

        :param uids:
            Optional list of uid strings to match
        :param display_names:
            Optional list of display name strings to match
        :param element_class:
            Optional element class string to match
        :param adjacent_nodes:
            Optional list of node uids that the links are connected to
        :param only_interior:
            Don't to match links that are attached at only one end to an adjacent_node
        :param include_subgroups:
            Recursively include groups that are subgroups of group_uids
        :param dt:
            Optional timestamp to access a historical version of the model
        """
        params = {}
        data = {}
        if uids:
            data["uids"] = uids
        if display_names:
            data["display_names"] = display_names
        if element_class:
            if isinstance(element_class, str):
                params["element_class"] = element_class
            elif hasattr(element_class, "__name__"):
                params["element_class"] = element_class.__name__
            else:
                raise ValueError(
                    "kwarg element_class {} should be string or element class".format(
                        element_class
                    )
                )
        if group_uids:
            data["group_uids"] = group_uids
        elif self._default_group_uid:
            data["group_uids"] = [self._default_group_uid]
        if adjacent_nodes:
            data["adjacent_node_uids"] = [
                (node if isinstance(node, str) else node.uid) for node in adjacent_nodes
            ]
        if not only_interior:
            params["only_interior"] = "False"
        if include_subgroups:
            params["include_subgroups"] = include_subgroups
        dt = dt or self._default_dt
        if dt:
            params["datetime"] = dt.isoformat()
        result = self._client.post(
            (*self._network_resource, "links", "search"),
            params=params,
            json=data,
        )
        return [element_from_dict(e) for e in result]

    def get_nodes(
        self,
        uids: Optional[List[str]] = None,
        display_names: Optional[List[str]] = None,
        element_class: Optional[List[str]] = None,
        group_uids: Optional[List[str]] = None,
        extent: Optional[LocationExtent] = None,
        schematic_extent: Optional[LocationExtent] = None,
        include_subgroups: Optional[bool] = False,
        dt: Optional[datetime] = None,
    ) -> List[BaseNode]:
        """Gets an iterable of nodes

        Gets the the nodes in the network. The nodes are filterable by optional
        kwargs.

        :param uids:
            Optional list of uid strings to match
        :param display_names:
            Optional list of display name strings to match
        :param element_class:
            Optional element type string to match
        :param extent:
            Optional mapping of extent dimensions to min and max extent of that
            dimension that returned nodes should be found within.
        :param schematic_extent:
            Optional mapping of schematic_extent dimensions to min and max extent
            of that dimension that returned nodes should be found within.
        :param include_subgroups:
            Recursively include groups that are subgroups of group_uids
        :param dt:
            Optional timestamp to access a historical version of the model
        """
        params = {}
        data = {}
        if uids:
            data["uids"] = uids
        if display_names:
            data["display_names"] = display_names
        if element_class:
            if isinstance(element_class, str):
                params["element_class"] = element_class
            elif hasattr(element_class, "__name__"):
                params["element_class"] = element_class.__name__
            else:
                raise ValueError(
                    "kwarg element_class {} should be string or element class".format(
                        element_class
                    )
                )
        if group_uids:
            data["group_uids"] = group_uids
        elif self._default_group_uid:
            data["group_uids"] = [self._default_group_uid]
        if extent:
            if isinstance(extent, dict):
                extent = LocationExtent.parse_obj(extent)
            data["extent"] = extent.dict()
        if schematic_extent:
            if isinstance(schematic_extent, dict):
                schematic_extent = LocationExtent.parse_obj(schematic_extent)
            data["schematic_extent"] = schematic_extent.dict()
        if include_subgroups:
            params["include_subgroups"] = include_subgroups
        dt = dt or self._default_dt
        if dt:
            params["datetime"] = dt.isoformat()

        result = self._client.post(
            (*self._network_resource, "nodes", "search"),
            params=params,
            json=data,
        )
        return [element_from_dict(e) for e in result]

    def get_groups(
        self,
        uids: Optional[List[str]] = None,
        display_names: Optional[List[str]] = None,
        element_class: Optional[List[str]] = None,
        group_uids: Optional[List[str]] = None,
        include_subgroups: Optional[bool] = False,
        dt: Optional[datetime] = None,
    ) -> List[BaseGroup]:
        """Gets an iterable of groups

        Gets the the groups in the network. The groups are filterable by optional
        kwargs.

        :param uids:
            Optional list of uid strings to match
        :param display_names:
            Optional list of display name strings to match
        :param element_class:
            Optional element type string to match
        :param include_subgroups:
            Recursively include groups that are subgroups of group_uids
        :param dt:
            Optional timestamp to access a historical version of the model
        """
        params = {}
        data = {}
        if uids:
            data["uids"] = uids
        if display_names:
            data["display_names"] = display_names
        if element_class:
            if isinstance(element_class, str):
                params["element_class"] = element_class
            elif hasattr(element_class, "__name__"):
                params["element_class"] = element_class.__name__
            else:
                raise ValueError(
                    "kwarg element_class {} should be string or element class".format(
                        element_class
                    )
                )
        if group_uids:
            data["group_uids"] = group_uids
        elif self._default_group_uid:
            data["group_uids"] = [self._default_group_uid]
        if include_subgroups:
            params["include_subgroups"] = include_subgroups
        dt = dt or self._default_dt
        if dt:
            params["datetime"] = dt.isoformat()

        result = self._client.post(
            (*self._network_resource, "groups", "search"),
            params=params,
            json=data,
        )
        return [element_from_dict(e) for e in result]

    def save_nodes(self, nodes: List[BaseNode]):
        """Save a list of nodes"""
        if not nodes:
            return
        nodes = ",".join((e.json(exclude_none=True) for e in nodes))
        nodes_data = f'{{"elements":[{nodes}]}}'
        self._client.post(
            (*self._network_resource, "nodes"),
            data=nodes_data,
            headers={"content-type": "application/json"},
        )

    def save_links(self, links: List[BaseLink]):
        """Save a list of links"""
        if not links:
            return
        links = ",".join((e.json(exclude_none=True) for e in links))
        links_data = f'{{"elements":[{links}]}}'
        self._client.post(
            (*self._network_resource, "links"),
            data=links_data,
            headers={"content-type": "application/json"},
        )

    def save_groups(self, groups: List[BaseGroup]):
        """Save a list of groups"""
        if not groups:
            return
        groups = ",".join((e.json(exclude_none=True) for e in groups))
        groups_data = f'{{"elements":[{groups}]}}'
        self._client.post(
            (*self._network_resource, "groups"),
            data=groups_data,
            headers={"content-type": "application/json"},
        )

    def drop(self, purge: bool = False):
        """Removes the network"""
        self._client.delete(self._network_resource, params={"purge": purge})

    def drop_links(self, uids: Optional[List[str]] = None, purge: bool = False):
        """Deletes the links with the given uids"""
        self._client.delete(
            (*self._network_resource, "links"),
            json={"uids": uids} if uids else None,
            params={"purge": purge},
        )

    def drop_nodes(self, uids: Optional[List[str]] = None, purge: bool = False):
        """Deletes the nodes with the given uids"""
        self._client.delete(
            (*self._network_resource, "nodes"),
            json={"uids": uids} if uids else None,
            params={"purge": purge},
        )

    def drop_groups(self, uids: Optional[List[str]] = None, purge: bool = False):
        """Deletes the groups with the given uids"""
        self._client.delete(
            (*self._network_resource, "groups"),
            json={"uids": uids} if uids else None,
            params={"purge": purge},
        )

    @property
    def name(self) -> str:
        """The name of the network"""
        return self._name
