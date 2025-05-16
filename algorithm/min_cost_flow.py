from collections import defaultdict, deque
import heapq # Keep heapq import if other parts of the file use it, otherwise remove
from math import inf

def find_min_cost_max_flow(graph, source, sink):
    """
    Calculates the minimum cost maximum flow from source to sink in a graph
    with capacities and costs using the successive shortest path algorithm with SPFA.
    """
    # Build residual graph structure:
    adj = defaultdict(list)
    nodes = set(graph.keys())

    for u, neighbors in graph.items():
        nodes.add(u)
        for edge_data in neighbors:
            v, capacity, cost = -1, 0, 0

            if isinstance(edge_data, tuple):
                if len(edge_data) >= 3:
                    v, capacity, cost = edge_data[:3]
                elif len(edge_data) == 2:
                    v, capacity = edge_data
                    cost = 0
                elif len(edge_data) == 1:
                     v = edge_data[0]
                     capacity = 1
                     cost = 0
                else: continue
            else:
                v = edge_data
                capacity = 1
                cost = 0

            if capacity < 0:
                raise ValueError("Edge capacity cannot be negative")

            nodes.add(v)

            idx_uv = len(adj[u])
            idx_vu = len(adj[v])
            adj[u].append([v, capacity, cost, idx_vu])
            adj[v].append([u, 0, -cost, idx_uv])

    # Convert source/sink now that nodes are collected, allows non-int IDs
    # If source/sink might not be in nodes, add check
    if source not in nodes or sink not in nodes:
         # Return 0,0 or raise error based on expected behavior
         # print(f"Warning: Source {source} or Sink {sink} not found in graph nodes.")
         return 0, 0

    max_flow = 0
    min_cost = 0
    num_nodes = len(nodes)

    # SPFA (Shortest Path Faster Algorithm) implementation
    def find_shortest_path_spfa():
        dist = {node: inf for node in nodes}
        parent_edge = {node: -1 for node in nodes}
        parent_node = {node: -1 for node in nodes}
        in_queue = {node: False for node in nodes}
        queue = deque()

        # Handle cases where source or sink might not be properly connected initially
        if source not in dist:
             return None # Source node isolated or invalid

        dist[source] = 0
        queue.append(source)
        in_queue[source] = True

        processed_count = 0 # Basic check against infinite loop for positive cycles

        while queue:
            # Basic protection against potential infinite loops in non-negative cycle cases
            processed_count += 1
            # if processed_count > num_nodes * num_nodes: # Heuristic limit
            #     print("Warning: SPFA processed suspiciously many nodes, potential issue?")
            #     # Depending on needs, could return None or raise error here
            #     return None # Assume issue if processing excessively

            u = queue.popleft()
            in_queue[u] = False


            for i in range(len(adj.get(u, []))): # Use .get for safety if u somehow not in adj keys
                edge = adj[u][i]
                v, capacity, cost, _ = edge

                # Check if v exists in dist before attempting access
                if v in dist and capacity > 0 and dist[u] + cost < dist[v]:
                    dist[v] = dist[u] + cost
                    parent_node[v] = u
                    parent_edge[v] = i
                    if not in_queue[v]:
                        queue.append(v)
                        in_queue[v] = True

        # Check reachability to sink
        if sink not in dist or dist[sink] == inf:
            return None # No path found

        # Reconstruct path and calculate path capacity
        path_flow = inf
        curr = sink
        while curr != source:
            # Check if curr exists in parent_node (handles disconnected cases)
            if curr not in parent_node or parent_node[curr] == -1:
                 # Path reconstruction failed, should not happen if dist[sink] != inf
                 # print(f"Error: Path reconstruction failed for sink {sink}") # Debugging line
                 return None # Indicate failure

            prev = parent_node[curr]
            edge_idx = parent_edge[curr]
            # Check if prev and edge_idx are valid before accessing adj
            if prev not in adj or edge_idx < 0 or edge_idx >= len(adj[prev]):
                # print(f"Error: Invalid parent/edge index during path reconstruction.") # Debugging line
                return None # Indicate failure
            path_flow = min(path_flow, adj[prev][edge_idx][1])
            curr = prev

        # Ensure path_flow calculation didn't fail or result in non-positive
        if path_flow == inf or path_flow <= 0:
             # This could happen if sink == source or other edge cases
             # If sink == source, dist[sink] = 0, but path reconstruction loop won't run
             # Let's handle sink == source earlier if needed, otherwise assume path_flow > 0 here
             return None if sink != source else (0, 0, parent_node, parent_edge) # Return 0 flow if source==sink


        # ***MODIFIED RETURN STATEMENT***
        return path_flow, dist[sink], parent_node, parent_edge

    # Main loop of the successive shortest path algorithm
    while True:
        # ***MODIFIED CALL SITE***
        spfa_result = find_shortest_path_spfa()

        if spfa_result is None:
            break # No more augmenting paths

        # ***UNPACK RETURNED VALUES***
        path_flow, path_cost, current_parent_node, current_parent_edge = spfa_result

        if path_flow <= 0: # Safeguard
             break

        max_flow += path_flow
        min_cost += path_flow * path_cost

        # Update residual capacities along the path
        curr = sink
        while curr != source:
            # ***USE RETURNED DICTIONARIES***
            # Check if curr exists in the dictionaries before access
            if curr not in current_parent_node: break # Path broken somehow, stop update
            prev = current_parent_node[curr]
            if curr not in current_parent_edge: break # Path broken somehow, stop update
            edge_idx = current_parent_edge[curr]

            # Add checks for valid indices and keys before modifying adj
            if prev not in adj or edge_idx < 0 or edge_idx >= len(adj[prev]): break
            rev_edge_idx = adj[prev][edge_idx][3]
            if curr not in adj or rev_edge_idx < 0 or rev_edge_idx >= len(adj[curr]): break

            # Decrease capacity of forward edge
            adj[prev][edge_idx][1] -= path_flow
            # Increase capacity of backward edge
            adj[curr][rev_edge_idx][1] += path_flow

            curr = prev

    return max_flow, min_cost