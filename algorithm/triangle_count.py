def count_triangles(graph):
    """
    Count the number of triangles (cycles of length 3) in the graph.
    
    Args:
        graph: The graph representation (adjacency list)
        
    Returns:
        int: Number of triangles in the graph
    """
    count = 0
    
    # For each node, check if any of its neighbors are connected to each other
    for node in graph:
        neighbors = []
        
        # Extract neighbor IDs
        for neighbor in graph.get(node, []):
            neighbor_id = neighbor[0] if isinstance(neighbor, tuple) else neighbor
            neighbors.append(neighbor_id)
        
        # Check for edges between neighbors
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                neighbor_i = neighbors[i]
                neighbor_j = neighbors[j]
                
                # Check if there's an edge between neighbor_i and neighbor_j
                if neighbor_i in graph and any(
                    (n[0] if isinstance(n, tuple) else n) == neighbor_j 
                    for n in graph.get(neighbor_i, [])
                ):
                    count += 1
    
    # Each triangle is counted 3 times (once from each vertex)
    return count // 3 