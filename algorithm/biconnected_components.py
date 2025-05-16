import collections
def count_biconnected_components(graph):
    """
    Counts the number of edge-biconnected components (blocks) in an undirected graph.
    Uses Tarjan's algorithm to find bridges, then DFS to count components.

    Args:
        graph: The graph representation as an adjacency list (dictionary).
               Assumes an undirected graph. Neighbors can be node IDs or tuples.
               Example: {0: [1, 2], 1: [0, 2], 2: [0, 1]}

    Returns:
        int: Number of edge-biconnected components. Returns 0 for an empty graph.
    """
    if not graph:
        return 0

    # --- Step 0: Preprocessing and Initialization ---
    adj = collections.defaultdict(list)
    all_nodes = set()
    edges_original = set() # Store edges to handle potential asymmetry/duplicates

    for u, neighbors in graph.items():
        all_nodes.add(u)
        for v_info in neighbors:
            v = v_info[0] if isinstance(v_info, tuple) else v_info
            all_nodes.add(v)
            # Store edges uniquely and build symmetric adjacency list for traversal
            edge = tuple(sorted((u, v)))
            if edge not in edges_original:
                 adj[u].append(v)
                 adj[v].append(u) # Ensure symmetry for undirected traversal
                 edges_original.add(edge)

    if not all_nodes: # Handle graph defined but with no nodes/edges effectively
        return 0

    disc = collections.defaultdict(int) # Discovery time
    low = collections.defaultdict(int)  # Low-link value
    visited_tarjan = set() # Visited set for Tarjan's bridge finding
    bridges = set()      # Set to store bridges as canonical tuples (u, v) where u < v
    time = 0             # Global timer for discovery time

    # Helper to get canonical edge representation
    def get_canonical_edge(u, v):
        return tuple(sorted((u, v)))

    # --- Step 1: Tarjan's Algorithm to Find Bridges ---
    def find_bridges_dfs(u, parent):
        nonlocal time
        visited_tarjan.add(u)
        time += 1
        disc[u] = low[u] = time

        for v in adj[u]:
            if v == parent: # Skip the edge back to the parent
                continue

            if v in visited_tarjan:
                # Back edge: update low[u] with disc[v]
                low[u] = min(low[u], disc[v])
            else:
                # Tree edge: recurse
                find_bridges_dfs(v, u)
                # After recursion, update low[u] with low[v]
                low[u] = min(low[u], low[v])
                # Check for bridge condition
                if low[v] > disc[u]:
                    bridges.add(get_canonical_edge(u, v))

    # Run Tarjan's algorithm starting from all unvisited nodes
    for node in all_nodes:
        if node not in visited_tarjan:
            find_bridges_dfs(node, -1) # Use -1 or None as initial parent marker

    # --- Step 2: DFS to Count Components Excluding Bridges ---
    visited_component = set() # Visited set for the component counting DFS
    bcc_count = 0

    def collect_component_dfs(u):
        visited_component.add(u)
        for v in adj[u]:
            # Explore only if the neighbor hasn't been visited in *this phase*
            # AND the edge (u, v) is NOT a bridge
            if v not in visited_component and get_canonical_edge(u, v) not in bridges:
                collect_component_dfs(v)

    # Run component counting DFS starting from all unvisited nodes
    for node in all_nodes:
        if node not in visited_component:
            collect_component_dfs(node)
            bcc_count += 1 # Each time we start a new DFS, we've found a new BCC

    return bcc_count