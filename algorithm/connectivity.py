def check_connectivity(graph, vertex_a, vertex_b):
    """
    Check if two vertices are connected in a graph.
    
    Args:
        graph: The graph representation (adjacency list)
        vertex_a: First vertex
        vertex_b: Second vertex
        
    Returns:
        bool: True if vertices are connected, False otherwise
    """
    # Use BFS to check connectivity
    if vertex_a == vertex_b:
        return True
        
    visited = set()
    queue = [vertex_a]
    visited.add(vertex_a)
    
    while queue:
        current = queue.pop(0)
        
        # Check if current node is the target
        if current == vertex_b:
            return True
            
        # Add unvisited neighbors to queue
        for neighbor in graph.get(current, []):
            neighbor_id = neighbor[0] if isinstance(neighbor, tuple) else neighbor
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                queue.append(neighbor_id)
                
    return False 