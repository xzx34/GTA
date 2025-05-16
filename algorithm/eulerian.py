import collections

def has_eulerian_path(graph):
    """
    Determines if an UNDIRECTED graph has an Eulerian path.
    An Eulerian path visits every edge exactly once.

    Conditions for an undirected graph:
    1. All vertices with non-zero degree belong to the same connected component.
    2. The number of vertices with odd degree is 0 or 2.

    Args:
        graph: The graph representation as an adjacency list (dictionary).
               Example: {0: [1, 2], 1: [0, 2], 2: [0, 1]}
               Handles potential asymmetry (e.g., if 1 is in 0's list, 0 might
               not be in 1's list initially, but the edge (0,1) is considered).
               Handles self-loops (e.g., {0: [0, 1], 1: [0]}) and multiple edges
               if represented (e.g., {0: [1, 1], 1: [0, 0]}).

    Returns:
        bool: True if the graph has an Eulerian path, False otherwise.
    """
    # Use defaultdict for convenience
    adj = collections.defaultdict(list)
    degrees = collections.defaultdict(int)
    nodes_with_edges = set() # Keep track of nodes involved in any edge

    # 1. Calculate degrees and build a symmetric adjacency list for connectivity check
    #    Process each edge exactly once to avoid double counting degrees.
    processed_edges = set()
    all_nodes = set(graph.keys()) # Start with nodes defined as keys

    if not graph:
        return True # An empty graph or graph with only isolated nodes has an empty path

    for u, neighbors in graph.items():
        all_nodes.add(u) # Ensure node u is tracked
        for v_info in neighbors:
            # Handle potential metadata associated with neighbors (like weights)
            v = v_info if not isinstance(v_info, tuple) else v_info[0]

            all_nodes.add(v) # Ensure node v is tracked

            # Add edge to symmetric adjacency list for traversal
            adj[u].append(v)
            if u != v: # Avoid adding self-loop twice to neighbor list if already present
                adj[v].append(u)

            # Mark nodes as having edges
            nodes_with_edges.add(u)
            nodes_with_edges.add(v)

            # Calculate degree by processing each edge pair {u, v} once
            # Sort nodes to create a canonical representation for the edge
            edge = tuple(sorted((u, v)))
            if edge not in processed_edges:
                degrees[u] += 1
                # Add degree for v even if v is the same as u (self-loop adds 2)
                degrees[v] += 1
                processed_edges.add(edge)

    # If there are no edges in the graph, it has an Eulerian path (the empty path)
    if not nodes_with_edges:
        return True

    # 2. Check degree condition
    odd_degree_count = 0
    for node in nodes_with_edges: # Only consider nodes that have edges
        if degrees[node] % 2 != 0:
            odd_degree_count += 1

    # An Eulerian path exists only if odd degree count is 0 or 2
    if odd_degree_count > 2:
        return False

    # 3. Check connectivity condition for non-isolated vertices
    visited = set()
    # Start DFS/BFS from any node that has at least one edge
    start_node = next(iter(nodes_with_edges))
    stack = [start_node]
    visited.add(start_node)

    while stack:
        u = stack.pop()
        # Iterate using the possibly corrected/symmetrized adjacency list 'adj'
        # Only explore neighbors that are part of the graph with edges
        for v in adj[u]:
             # Important: Only consider nodes that originally had edges.
             # This prevents jumping to isolated components via adj list construction.
             # Although, adj construction should only include nodes involved in edges.
             # Double check: if v has degree 0, it shouldn't be in adj[u] unless it was
             # specifically added like {0:[1], 1:[]}. The degree calculation handles this.
             # We only need to ensure we explore the component containing nodes_with_edges.
            if v in nodes_with_edges and v not in visited:
                visited.add(v)
                stack.append(v)

    # Check if all nodes with edges were visited
    if len(visited) != len(nodes_with_edges):
        return False # The subgraph induced by edges is not connected

    # If both degree and connectivity conditions are met
    return True

def has_eulerian_circuit(graph):
    """
    Determines if an undirected graph has an Eulerian circuit.
    An Eulerian circuit is a cycle that visits every edge exactly once.

    Conditions for an undirected graph to have an Eulerian circuit:
    1. All vertices with non-zero degree belong to a single connected component.
    2. All vertices have an even degree.

    Args:
        graph: The graph representation as an adjacency list.
               Assumes an undirected graph, meaning if v is in graph[u],
               then u should be in graph.get(v, []).
               Example: {0: [1, 2], 1: [0, 2], 2: [0, 1]}

    Returns:
        bool: True if the graph has an Eulerian circuit, False otherwise.
    """
    if not graph:
        return True # An empty graph has a trivial Eulerian circuit

    degrees = collections.defaultdict(int)
    nodes_with_edges = set()
    all_nodes = set(graph.keys()) # Start with keys

    # Ensure all nodes mentioned (keys and neighbors) are considered
    # and calculate degrees based on adjacency list length (assuming symmetry)
    nodes_to_process = set(graph.keys())
    processed_nodes = set()
    
    # Temporarily collect all nodes mentioned
    temp_all_nodes = set(graph.keys())
    for u, neighbors in graph.items():
         for neighbor_info in neighbors:
            v = neighbor_info if not isinstance(neighbor_info, tuple) else neighbor_info[0]
            temp_all_nodes.add(v)

    # Calculate degrees correctly using graph.get for robustness
    for node in temp_all_nodes:
        # The degree of a node in an undirected graph represented symmetrically
        # is the length of its adjacency list. graph.get handles nodes that might only be neighbors.
        degree = len(graph.get(node, []))
        degrees[node] = degree
        if degree > 0:
            nodes_with_edges.add(node)
        # Check for odd degree immediately
        if degree % 2 != 0:
            return False # Condition 2 failed: Found a vertex with odd degree

    # If we are here, all vertices have even degree (or degree 0).
    # Now check connectivity of the component(s) containing edges.

    # If there are no edges in the graph, it has an Eulerian circuit.
    if not nodes_with_edges:
        return True # Only isolated vertices or empty graph after degree check

    # Check Condition 1: All vertices with non-zero degree must be connected.
    # Perform BFS or DFS starting from an arbitrary node with edges.
    visited = set()
    # Use collections.deque for efficient BFS queue operations
    queue = collections.deque([next(iter(nodes_with_edges))]) # Start BFS from one node with edges
    visited.add(queue[0])

    while queue:
        u = queue.popleft()
        for neighbor_info in graph.get(u, []):
            v = neighbor_info if not isinstance(neighbor_info, tuple) else neighbor_info[0]
            # We only care about exploring the graph structure.
            # If a neighbor hasn't been visited, add it to the queue and mark visited.
            if v not in visited:
                visited.add(v)
                # We only need to explore from nodes that can lead to others.
                # No need to add zero-degree nodes explicitly, but visiting them is fine.
                queue.append(v)

    # After traversal, check if all nodes *with edges* were visited.
    # This confirms that all nodes involved in edges belong to the same component.
    connected = all(node in visited for node in nodes_with_edges)

    # Both conditions must be met (Even degrees already checked)
    return connected