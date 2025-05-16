def check_bipartite(graph):
    """
    Check if a graph is bipartite (can be divided into two sets where
    no two vertices within the same set are adjacent).
    
    Args:
        graph: The graph representation (adjacency list)
        
    Returns:
        bool: True if the graph is bipartite, False otherwise
    """
    # Handle empty graph
    if not graph:
        return True
        
    # Use coloring approach (0: uncolored, 1: color A, -1: color B)
    colors = {}
    
    # Process each component of the graph
    for node in graph:
        if node not in colors:
            # Start BFS from this unvisited node
            queue = [node]
            colors[node] = 1  # Assign first color
            
            while queue:
                current = queue.pop(0)
                
                # Check all neighbors
                for neighbor in graph.get(current, []):
                    neighbor_id = neighbor[0] if isinstance(neighbor, tuple) else neighbor
                    
                    # If neighbor is not colored yet
                    if neighbor_id not in colors:
                        # Assign opposite color to neighbor
                        colors[neighbor_id] = -colors[current]
                        queue.append(neighbor_id)
                    # If neighbor has the same color as current node
                    elif colors[neighbor_id] == colors[current]:
                        return False
    
    return True 