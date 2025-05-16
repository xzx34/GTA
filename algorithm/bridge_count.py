def count_bridges(graph):
    """
    Count the number of bridges (cut edges) in the graph.
    A bridge is an edge whose removal increases the number of connected components.
    
    Args:
        graph: The graph representation (adjacency list)
        
    Returns:
        int: Number of bridges in the graph
    """
    # Use Tarjan's algorithm to find bridges
    
    def dfs(node, parent, visited, disc, low, bridges):
        nonlocal time
        # Mark current node as visited
        visited[node] = True
        
        # Initialize discovery time and low value
        disc[node] = low[node] = time
        time += 1
        
        # Go through all neighbors
        for neighbor in graph.get(node, []):
            neighbor_id = neighbor if not isinstance(neighbor, tuple) else neighbor[0]
            
            # If neighbor is not visited
            if not visited[neighbor_id]:
                dfs(neighbor_id, node, visited, disc, low, bridges)
                
                # Check if the subtree rooted at neighbor has a connection
                # to one of the ancestors of node
                low[node] = min(low[node], low[neighbor_id])
                
                # If the lowest vertex reachable from subtree under neighbor
                # is below node in DFS tree, then node-neighbor is a bridge
                if low[neighbor_id] > disc[node]:
                    bridges.append((node, neighbor_id))
            
            # Update low value of node if neighbor is already visited and not parent
            elif neighbor_id != parent:
                low[node] = min(low[node], disc[neighbor_id])
    
    if not graph:
        return 0
        
    vertices = list(graph.keys())
    n = len(vertices)
    
    # Arrays to track discovery time, lowest reachable vertex, and visited status
    visited = {v: False for v in vertices}
    disc = {v: float('inf') for v in vertices}
    low = {v: float('inf') for v in vertices}
    bridges = []
    
    # Time counter for discovery time
    time = 0
    
    # Call DFS for each unvisited vertex
    for v in vertices:
        if not visited[v]:
            dfs(v, -1, visited, disc, low, bridges)
    
    return len(bridges) 