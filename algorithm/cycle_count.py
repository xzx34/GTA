import collections
def count_cycles(graph):
    """
    Counts the total number of unique simple cycles in a given UNDIRECTED graph
    more efficiently by finding cycles where the starting node has the minimum ID.

    A simple cycle is a path starting and ending at the same vertex, containing
    at least three distinct vertices, and not repeating other vertices.

    Args:
        graph: The graph representation as an adjacency list (dictionary).
               Assumes an undirected graph. Neighbors can be node IDs or tuples.

    Returns:
        int: Number of unique simple cycles found in the graph.
    """
    cycles = set() # Stores canonical representation (tuple) of cycles found
    
    # Pre-process graph for faster neighbor access and ensure node IDs are comparable
    adj = collections.defaultdict(list)
    nodes = set()
    for u, neighbors in graph.items():
        nodes.add(u)
        for v_info in neighbors:
            v = v_info[0] if isinstance(v_info, tuple) else v_info
            # Ensure undirectedness for traversal, store only IDs
            if u != v: # Avoid adding self-loops to adj list here if not needed for cycle def
                 adj[u].append(v)
                 adj[v].append(u)
            # Note: Simple cycles usually don't involve repeating edges immediately,
            # so self-loops aren't typically part of simple cycles > length 2.
            # If self-loops should form length-1 cycles, handle separately if needed.
            # Standard simple cycles need >= 3 distinct vertices.
            nodes.add(v)

    # Sort nodes to process them in a consistent order (optional but good practice)
    sorted_nodes = sorted(list(nodes))

    def get_canonical_cycle_min_start(path, start_node):
        """
        Generates canonical form assuming start_node is the minimum node ID.
        Compares forward path (s, v1, v2...) with reverse (s, ..., v2, v1).
        """
        if not path or len(path) < 3:
            return None # Not a valid simple cycle for our definition

        # Path already starts with the minimum node 'start_node'
        path_tuple = tuple(path)

        # Generate the reverse path starting from start_node
        # Example: path = [0, 1, 3]. reverse = [0, 3, 1]
        # path[1:] gives [1, 3]. [::-1] gives [3, 1]. Prepend start_node.
        reverse_path_list = [start_node] + path[1:][::-1]
        reverse_path_tuple = tuple(reverse_path_list)

        # Return the lexicographically smaller tuple
        if path_tuple < reverse_path_tuple:
            return path_tuple
        else:
            return reverse_path_tuple

    # --- DFS function ---
    # path: current sequence of nodes visited
    # visited_on_path: set for O(1) lookup of nodes in the current path
    def dfs_util(u, start_node, path, visited_on_path):
        path.append(u)
        visited_on_path.add(u)

        for neighbor in adj.get(u, []):
            # Condition 1: Closing a cycle back to the *original* start_node
            if neighbor == start_node:
                if len(path) >= 3: # Check length requirement
                    canonical = get_canonical_cycle_min_start(path, start_node)
                    if canonical:
                        cycles.add(canonical)
                # Continue search from u for other potential cycles

            # Condition 2: Explore node only if ID > start_node and not visited yet on this path
            # This prevents finding cycles where start_node isn't the minimum ID,
            # and also prevents revisiting nodes on the current simple path.
            elif neighbor > start_node and neighbor not in visited_on_path:
                dfs_util(neighbor, start_node, path, visited_on_path)

        # Backtrack
        path.pop()
        visited_on_path.remove(u)

    # --- Main loop ---
    for start_node in sorted_nodes:
        # Initiate DFS from start_node to find cycles where start_node is the minimum element
        dfs_util(start_node, start_node, [], set()) # Initial path is empty, visited set is empty

    return len(cycles)