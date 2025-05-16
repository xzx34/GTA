
from collections import deque

def find_minimum_cycle(graph):
    """
    Find the length of the smallest cycle in an undirected graph.
    If no cycle exists, return -1.
    
    Args:
        graph (dict): Adjacency list of the graph. Example:
                      {0: [1, 2], 1: [0, 2], 2: [0, 1]}
                      Handles neighbors as ints or tuples like (v, weight)
    
    Returns:
        int: Length of the smallest cycle, or -1 if none found
    """
    min_cycle_length = float('inf')

    # Preprocess: simplify neighbors to node IDs (ignore weights if any)
    simplified_graph = {
        u: [v[0] if isinstance(v, tuple) else v for v in neighbors]
        for u, neighbors in graph.items()
    }

    for start_node in simplified_graph:
        # Initialize distances and parents
        distance = {node: float('inf') for node in simplified_graph}
        parent = {node: None for node in simplified_graph}

        distance[start_node] = 0
        queue = deque()
        queue.append(start_node)

        while queue:
            current = queue.popleft()

            for neighbor in simplified_graph[current]:
                if distance[neighbor] == float('inf'):
                    # First time visiting neighbor
                    distance[neighbor] = distance[current] + 1
                    parent[neighbor] = current
                    queue.append(neighbor)
                elif parent[current] != neighbor:
                    # Found a back edge forming a cycle
                    cycle_length = distance[current] + distance[neighbor] + 1
                    min_cycle_length = min(min_cycle_length, cycle_length)

    return min_cycle_length if min_cycle_length != float('inf') else -1