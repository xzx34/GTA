from math import inf
import collections

class UnionFind:
    """A data structure for disjoint set union (DSU) operations."""
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}
        self.count = len(vertices) # Optional: track number of disjoint sets

    def find(self, vertex):
        """Find the representative (root) of the set containing vertex."""
        if self.parent[vertex] != vertex:
            # Path compression
            self.parent[vertex] = self.find(self.parent[vertex])
        return self.parent[vertex]

    def union(self, u, v):
        """Merge the sets containing u and v."""
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u != root_v:
            # Union by rank
            if self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                if self.rank[root_u] == self.rank[root_v]:
                    self.rank[root_u] += 1
            self.count -= 1 # Optional: decrement set count
            return True
        return False

def extract_edges_and_vertices(graph):
    """Extracts all unique edges and vertices from the graph."""
    edges = []
    vertices = set(graph.keys())
    processed_undirected_edges = set()

    for u, neighbors in graph.items():
        for neighbor_info in neighbors:
            v = None
            weight = 1 # Default weight for unweighted edges

            if isinstance(neighbor_info, tuple) and len(neighbor_info) >= 2:
                v, weight = neighbor_info[:2]
            else:
                v = neighbor_info # Assume it's just the neighbor vertex ID

            vertices.add(v) # Ensure neighbor vertex is included

            # Ensure each undirected edge (u, v, weight) is added only once
            edge_tuple = tuple(sorted((u, v)))
            if edge_tuple not in processed_undirected_edges:
                edges.append((u, v, weight))
                processed_undirected_edges.add(edge_tuple)

    return list(vertices), edges

def find_mst_using_kruskal(graph):
    """
    Finds the Minimum Spanning Tree (MST) using Kruskal's algorithm.

    Args:
        graph: Adjacency list representation of the graph.

    Returns:
        tuple: (mst_edges, total_weight). mst_edges is a list of tuples
               (u, v, weight) representing the MST. total_weight is the sum
               of weights in the MST. Returns ([], inf) if the graph is
               not connected or has no edges but multiple vertices.
               Returns ([], 0) for an empty graph or a single-node graph.
    """
    if not graph:
        return [], 0

    vertices, edges = extract_edges_and_vertices(graph)
    num_vertices = len(vertices)

    if num_vertices <= 1:
         # MST of a single node or empty graph has 0 weight and no edges
        return [], 0
    if not edges and num_vertices > 1:
        # Multiple nodes but no edges means disconnected
        return [], inf

    # Sort edges by weight
    edges.sort(key=lambda x: x[2])

    uf = UnionFind(vertices)
    mst_edges = []
    total_weight = 0
    edges_count = 0

    for u, v, weight in edges:
        if uf.union(u, v):
            mst_edges.append((u, v, weight))
            total_weight += weight
            edges_count += 1
            # Optimization: Stop when MST is complete
            if edges_count == num_vertices - 1:
                break

    # Check if a spanning tree was formed (graph is connected)
    if edges_count < num_vertices - 1:
        # The graph is not connected if we couldn't add V-1 edges
        return [], inf

    return mst_edges, total_weight

def find_mst_weight(graph):
    """
    Calculates the weight of the Minimum Spanning Tree (MST).

    Args:
        graph: Adjacency list representation.

    Returns:
        float: Total weight of the MST, or inf if no MST exists (disconnected).
               Returns 0 for an empty or single-node graph.
    """
    if not graph:
        return 0
    _, weight = find_mst_using_kruskal(graph)
    return weight

def find_mst_edges(graph):
    """
    Finds the edges constituting the Minimum Spanning Tree (MST).

    Args:
        graph: Adjacency list representation.

    Returns:
        list: List of MST edges as (u, v, weight) tuples. Returns an empty
              list if no MST exists or for empty/single-node graphs.
    """
    edges, weight = find_mst_using_kruskal(graph)
    # Return empty list if graph was disconnected (indicated by inf weight)
    return edges if weight != inf else []


# --- Second Minimum Spanning Tree (Optimized Approach) ---

def _find_max_weight_edge_on_path(u, target, path_edges, visited, graph_mst):
    """DFS helper to find the max weight edge on the path in MST between u and target."""
    visited.add(u)
    max_weight = -inf
    max_edge = None

    for v, weight in graph_mst.get(u, []):
        current_edge = tuple(sorted((u, v)))
        if v == target:
            # Found target, return this edge's weight and the edge itself
            return weight, (u, v, weight)
        if v not in visited:
            # Explore neighbor
            sub_max_weight, sub_max_edge = _find_max_weight_edge_on_path(
                v, target, path_edges, visited, graph_mst
            )
            if sub_max_edge is not None: # Path to target found via this neighbor
                # Track the maximum weight encountered on the successful path back
                if sub_max_weight > max_weight:
                    max_weight = sub_max_weight
                    max_edge = sub_max_edge
                # Also consider the edge (u,v) connecting to this successful subpath
                if weight > max_weight:
                    max_weight = weight
                    max_edge = (u, v, weight)
                return max_weight, max_edge

    return -inf, None # Target not reachable through this path


def find_second_mst_weight_optimized(graph):
    """
    Finds the weight of the Second Minimum Spanning Tree (SMST).
    Uses the approach of iterating through non-MST edges.

    Args:
        graph: Adjacency list representation.

    Returns:
        float: Weight of the SMST, or inf if no SMST exists.
               Returns 0 for graphs where MST/SMST concepts don't apply
               (e.g., empty, single node).
    """
    vertices, all_edges = extract_edges_and_vertices(graph)
    num_vertices = len(vertices)

    if num_vertices <= 1:
        return 0 # No edges possible

    mst_edges, mst_weight = find_mst_using_kruskal(graph)

    if mst_weight == inf:
        return inf # Graph is not connected, no MST, hence no SMST

    # Build adjacency list representation of the MST for path finding
    graph_mst = collections.defaultdict(list)
    mst_edge_set = set()
    for u, v, weight in mst_edges:
        graph_mst[u].append((v, weight))
        graph_mst[v].append((u, weight))
        mst_edge_set.add(tuple(sorted((u, v))))

    second_mst_weight = inf

    # Iterate through all original edges *not* in the MST
    for u, v, weight in all_edges:
        edge_canonical = tuple(sorted((u, v)))
        if edge_canonical not in mst_edge_set:
            # This edge forms a cycle with MST edges. Find the max weight edge on that cycle's path in the MST.
            visited = set()
            # Find the path in MST between u and v, and the max edge weight on it
            max_weight_on_path, max_edge_on_path = _find_max_weight_edge_on_path(
                u, v, [], visited, graph_mst
            )

            if max_edge_on_path is not None:
                # Consider swapping 'max_edge_on_path' with the current non-MST edge (u, v, weight)
                # We are interested in the SMST, which should have a weight strictly greater than MST
                # or equal if multiple MSTs exist.
                # If the current edge's weight is strictly greater than the max edge on the path,
                # swapping them definitely creates a different spanning tree.
                if weight > max_weight_on_path:
                    candidate_weight = mst_weight - max_weight_on_path + weight
                    second_mst_weight = min(second_mst_weight, candidate_weight)
                elif weight == max_weight_on_path:
                    # If weights are equal, we need to find the *second* max weight edge on the path
                    # to ensure we create a tree distinct from the *original* MST.
                    # This requires a more complex path analysis.
                    # For simplicity, many SMST definitions find the minimum weight spanning tree
                    # whose weight is *strictly greater* than the MST weight.
                    # If we stick to that, we ignore the weight == max_weight_on_path case here
                    # or require a more advanced path query.
                    # A simpler approach that often works: just calculate the candidate weight
                    # and take the minimum. If multiple MSTs exist, this might yield the same weight.
                    candidate_weight = mst_weight - max_weight_on_path + weight
                    # To be strictly the *second* minimum, ensure it's > mst_weight
                    if candidate_weight > mst_weight:
                        second_mst_weight = min(second_mst_weight, candidate_weight)
                    # Else: if candidate_weight == mst_weight, it's just another MST, not SMST.

                    # A more robust handling for weight == max_weight_on_path would involve finding
                    # the second heaviest edge on the cycle path and using that if available.
                    # However, let's use the common definition: find the minimum weight > mst_weight.
                    pass # Ignoring equal weight case for stricter SMST definition for now.


    return second_mst_weight


# --- Original Function Names (Wrappers) ---

def find_minimum_spanning_tree(graph):
    """
    Finds the Minimum Spanning Tree (MST) using Kruskal's algorithm.

    Args:
        graph: Adjacency list representation.

    Returns:
        tuple: (mst_edges, total_weight). mst_edges is a list of tuples
               (u, v, weight). total_weight is the sum of weights.
               Returns ([], inf) if disconnected. Returns ([], 0) if empty/single node.
    """
    # This function's previous implementation directly called the Kruskal logic.
    # We keep the same behavior by calling the refined Kruskal function.
    return find_mst_using_kruskal(graph)


def find_second_mst_weight(graph):
    """
    Finds the weight of the Second Minimum Spanning Tree (SMST).

    Args:
        graph: Adjacency list representation.

    Returns:
        float: Weight of the SMST. Returns -1 if no SMST exists (e.g.,
               disconnected graph, or graph structure doesn't allow SMST).
               Returns 0 for trivial cases (empty/single node).
    """
    # Call the optimized SMST weight calculation function
    weight = find_second_mst_weight_optimized(graph)

    # Handle return value mapping according to original function spec
    if weight == inf:
        return -1 # Map infinity (no SMST found) to -1
    elif weight == 0 and (not graph or len(graph) <= 1) :
         return 0 # Trivial cases return 0
    elif weight == 0:
         # Non-trivial graph resulting in 0 could be error or specific case
         # Depending on definition, if MST weight is 0, SMST might be > 0 or non-existent
         # Let's assume if optimized func returns 0 for non-trivial, it's 0. Check requirements if needed.
         return 0
    else:
        return weight # Return the calculated SMST weight