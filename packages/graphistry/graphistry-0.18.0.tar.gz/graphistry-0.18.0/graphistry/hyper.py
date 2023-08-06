import logging
from typing import List, Optional
from graphistry.hyper_dask import hypergraph as hypergraph_new
logger = logging.getLogger(__name__)


class Hypergraph(object):

    @staticmethod
    def hypergraph(
        g, raw_events, entity_types: Optional[List[str]] = None, opts: dict = {},
        drop_na: bool = True, drop_edge_attrs: bool = False, verbose: bool = True, direct: bool = False,
        engine: str = 'pandas'
    ) -> dict:
        """
            raw_events can be pd.DataFrame or cudf.DataFrame
        """

        out = hypergraph_new(
            g, raw_events, entity_types, opts,
            drop_na, drop_edge_attrs, verbose, direct,
            engine=engine)

        return {
            'entities': out.entities,
            'events': out.events,
            'edges': out.edges,
            'nodes': out.nodes,
            'graph': out.graph
        }
