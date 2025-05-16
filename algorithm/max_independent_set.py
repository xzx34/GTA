def find_max_independent_set_size(graph):
    """
    Find the size of the maximum independent set in the graph.
    An independent set is a set of vertices such that no two vertices are adjacent.
    
    Args:
        graph: The graph representation (adjacency list)
        
    Returns:
        int: Size of the maximum independent set
    """
    def is_independent(vertices):
        # Check if no two vertices in the set are adjacent
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                u, v = vertices[i], vertices[j]
                # Check if there's an edge between u and v
                if v in [n if not isinstance(n, tuple) else n[0] for n in graph.get(u, [])]:
                    return False
        return True
    
    def backtrack(remaining, current_set):
        if not remaining:
            return len(current_set)
        
        # Take the first vertex
        v = remaining[0]
        new_remaining = remaining[1:]
        
        # Option 1: Don't include v in the independent set
        size1 = backtrack(new_remaining, current_set)
        
        # Option 2: Include v in the independent set
        new_set = current_set + [v]
        if is_independent(new_set):
            # Filter out v's neighbors from remaining vertices
            v_neighbors = [n if not isinstance(n, tuple) else n[0] for n in graph.get(v, [])]
            filtered_remaining = [u for u in new_remaining if u not in v_neighbors]
            size2 = backtrack(filtered_remaining, new_set)
            return max(size1, size2)
        
        return size1
    
    # Start with all vertices
    vertices = list(graph.keys())
    return backtrack(vertices, []) 