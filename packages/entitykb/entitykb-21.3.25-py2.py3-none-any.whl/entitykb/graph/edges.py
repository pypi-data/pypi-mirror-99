from pathlib import Path
from typing import Set, Optional, List, Tuple, Iterable

from dawg import CompletionDAWG

from entitykb import (
    Node,
    Edge,
    Direction,
    Neighbor,
    TripleSep as TS,
    ensure_iterable,
    create_index,
)


class EdgeIndex(object):
    def __init__(self, root: Path):
        self.dawg_path = root / "edges.dawg"
        self.cache = create_index(str(root / "edges"))
        self.dawg: CompletionDAWG = self._load_dawg()

    def __len__(self) -> int:
        return len(self.cache)

    def __contains__(self, edge: Edge) -> bool:
        return self.cache.__contains__(edge.key)

    def __getitem__(self, key) -> Edge:
        edge = Edge.from_line(key)
        edge.set_data(self.get_data(key=key))
        return edge

    def get_verbs(self) -> Set[str]:
        verbs = set()
        for line in self.dawg.iterkeys(TS.vbs.value):
            verbs.add(line[1:])
        return verbs

    def save(self, edge: Edge):
        self.cache[edge.key] = edge.data

    def remove(self, edge: Edge) -> Optional[Edge]:
        item = self.cache.pop(edge.key, None)
        return item

    def get_data(self, *, edge: Edge = None, key=None):
        key = key or edge.key
        return self.cache[key]

    def iterate(self, verbs=None, directions=None, nodes=None):
        verbs = (None,) if not verbs else verbs
        nodes = (None,) if nodes is None else nodes
        directions = Direction.as_tuple(directions, all_if_none=True)

        for verb in ensure_iterable(verbs):
            for direction in ensure_iterable(directions):
                for node in ensure_iterable(nodes):
                    node_key = Node.to_key(node)
                    it = self._iterate_ts_line(direction, node_key, verb)
                    for ts, line in it:
                        edge = Edge.from_line(line, ts=ts)
                        yield edge.get_other(direction), edge

    def get_neighbors(
        self,
        node_key,
        verb: str = None,
        direction: Optional[Direction] = None,
        label: str = None,
        offset: int = 0,
        limit: int = 10,
    ) -> Tuple[List[Neighbor], int]:

        neighbors = []
        count = 0

        directions = Direction.as_tuple(direction, all_if_none=True)
        for direction in directions:
            it = self._iterate_ts_line(direction, node_key, verb)
            for ts, line in it:
                if label and not line.endswith(f"|{label}"):
                    continue

                count += 1
                if count <= offset:
                    continue

                if count < (offset + limit):
                    edge = Edge.from_line(line, ts=ts)
                    neighbor = Neighbor(
                        key=edge.get_other(direction),
                        verb=edge.verb,
                        direction=direction.value,
                        edge=edge,
                    )
                    neighbors.append(neighbor)

        return neighbors, count

    def reload(self):
        self.dawg = self._load_dawg()

    def reindex(self):
        self.dawg = self._create_dawg()
        self.dawg.save(self.dawg_path)

    def clear(self):
        self.cache.clear()
        self.reindex()

    def clean(self, node_index):
        for key in self.cache.keys():
            edge = Edge.from_line(key, ts=TS.sve)
            if edge.start not in node_index:
                self.remove(edge)
            elif edge.end not in node_index:
                self.remove(edge)

    # private methods

    def _load_dawg(self):
        if self.dawg_path.is_file():
            return CompletionDAWG().load(str(self.dawg_path))
        return CompletionDAWG([])

    def _create_dawg(self) -> CompletionDAWG:
        def generate_dawg_keys():
            vbs_set = set()
            for sve_key in self.cache.keys():
                yield sve_key

                # creating shallow edge from key is faster than
                # retrieval full edge from cache index
                edge = Edge.from_line(sve_key, ts=TS.sve)
                yield edge.vse
                yield edge.evs
                vbs_set.add(edge.vbs)

            yield from vbs_set

        it_keys = generate_dawg_keys()
        dawg = CompletionDAWG(it_keys)
        return dawg

    def _iterate_ts_line(
        self, direction, node_key, verb
    ) -> Iterable[Tuple[TS, str]]:
        ts, tokens = self._sep_split(direction, node_key, verb)

        if ts:
            prefix = ts.join(tokens)
            for line in self.dawg.iterkeys(prefix):
                yield ts, line

    @classmethod
    def _sep_split(cls, direction, node_key, verb) -> Tuple[TS, List[str]]:
        sep = None
        tokens = [""]

        if node_key:
            sep = TS.sve if direction.is_outgoing else TS.evs
            tokens.append(node_key)

        if verb:
            sep = sep or TS.vse
            tokens.append(verb)

        tokens.append("")

        return sep, tokens
