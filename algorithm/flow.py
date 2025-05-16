import collections
from math import inf

def find_maximum_flow(graph, source, sink):
    """
    Calculates the maximum flow from source to sink using the Edmonds-Karp
    algorithm (Ford-Fulkerson with BFS for finding augmenting paths).

    Args:
        graph: Adjacency list representation of the graph.
               Format: {node: [(neighbor, capacity), ...]}
               Assumes non-negative integer capacities.
        source: The source node ID.
        sink: The sink node ID.

    Returns:
        int: The value of the maximum flow.
    """
    source = int(source)
    sink = int(sink)

    # Build the residual graph structure using adjacency list.
    # Stores [neighbor, residual_capacity, index_of_reverse_edge_in_neighbor_list]
    adj = collections.defaultdict(list)
    nodes = set(graph.keys()) # Collect all nodes initially

    for u_str, neighbors in graph.items():
        u = int(u_str) # Ensure node IDs are integers
        nodes.add(u)
        for neighbor_info in neighbors:
            v = None
            capacity = 1 # Default capacity for unweighted edges

            if isinstance(neighbor_info, tuple) and len(neighbor_info) >= 2:
                # Weighted edge: (neighbor_vertex, capacity)
                v_str, capacity_val = neighbor_info[:2]
                v = int(v_str)
                capacity = int(capacity_val)
            elif isinstance(neighbor_info, (int, str)):
                 # Unweighted edge, neighbor is just the ID
                v = int(neighbor_info)
            else:
                # Skip invalid neighbor format
                continue

            nodes.add(v) # Ensure neighbor node is tracked

            # Add forward and backward edges to the residual graph structure
            # Need to know the index of the reverse edge *before* adding it
            idx_rev = len(adj[v])
            idx_fwd = len(adj[u])
            adj[u].append([v, capacity, idx_rev])
            adj[v].append([u, 0, idx_fwd]) # Initial residual capacity of reverse edge is 0

    max_flow = 0

    while True:
        # Find an augmenting path using BFS
        # parent stores {node: (parent_node, index_of_edge_in_parent's_adj_list)}
        parent = {node: None for node in nodes}
        queue = collections.deque([source])
        path_found = False

        # Standard BFS to find a path with available capacity
        while queue:
            u = queue.popleft()
            if u == sink:
                path_found = True
                break

            # Explore neighbors in the residual graph
            for i, edge_data in enumerate(adj[u]):
                v, residual_capacity, _ = edge_data
                # If neighbor not visited and there's residual capacity
                if parent[v] is None and residual_capacity > 0:
                    parent[v] = (u, i) # Store parent and edge index used to reach v
                    if v == sink: # Early exit if sink is reached
                         path_found = True
                         queue.clear() # Clear queue to stop BFS
                         break
                    queue.append(v)

        # If no augmenting path found, we are done
        if not path_found or parent[sink] is None:
            break

        # Calculate the bottleneck capacity of the found path
        path_flow = inf
        curr = sink
        while curr != source:
            prev, edge_index = parent[curr]
            # Find the residual capacity of the edge used in the path
            edge_capacity = adj[prev][edge_index][1]
            path_flow = min(path_flow, edge_capacity)
            curr = prev # Move to the parent

        # Augment the flow along the path
        max_flow += path_flow
        v = sink
        while v != source:
            u, edge_index = parent[v]
            # Decrease residual capacity of the forward edge
            adj[u][edge_index][1] -= path_flow

            # Increase residual capacity of the backward edge
            # Find the index of the reverse edge using the stored information
            reverse_edge_index = adj[u][edge_index][2]
            adj[v][reverse_edge_index][1] += path_flow

            v = u # Move to the parent

    return max_flow


def find_minimum_cut(graph, source, sink):
    """
    Calculates the capacity of the minimum cut between source and sink.
    This is equivalent to the maximum flow value (Max-Flow Min-Cut Theorem).

    Args:
        graph: Adjacency list representation of the graph.
               Format: {node: [(neighbor, capacity), ...]}
        source: The source node ID.
        sink: The sink node ID.

    Returns:
        int: The capacity of the minimum cut.
    """
    # The capacity of the minimum cut is equal to the maximum flow value.
    return find_maximum_flow(graph, source, sink)