import heapq
import collections
from math import inf

def find_shortest_path_length(graph, start, end):
    """
    Finds the shortest path length between two nodes in a possibly weighted graph
    using Dijkstra's algorithm.

    Args:
        graph: Adjacency list representation of the graph.
               Format: {node: [(neighbor, weight), ...]} or {node: [neighbor, ...]}
               Weights are numeric. Unweighted edges are assumed to have weight 1.
        start: The starting node.
        end: The ending node.

    Returns:
        The length of the shortest path as a number (int or float),
        or float('inf') if there is no path.
        Returns -1 if start or end node is not in the graph at all.
        (Note: Changed return value for no path from -1 to float('inf') internally
         for consistency, but will map back to -1 if required by original spec,
         though returning inf is more conventional for graph algorithms).
         The prompt asks to keep the output format, so we'll return -1.
    """

    # Build the weighted graph representation and collect all nodes
    weighted_graph = collections.defaultdict(list)
    all_nodes = set(graph.keys()) # Start with keys

    for node, neighbors in graph.items():
        for neighbor_info in neighbors:
            if isinstance(neighbor_info, tuple) and len(neighbor_info) >= 2:
                # Weighted edge: (neighbor_node, weight)
                neighbor_node, weight = neighbor_info[0], neighbor_info[1]
                # Basic check for non-numeric or negative weights if needed,
                # but standard Dijkstra assumes non-negative weights.
                if not isinstance(weight, (int, float)) or weight < 0:
                     raise ValueError(f"Edge ({node}, {neighbor_node}) has invalid weight: {weight}. Dijkstra requires non-negative weights.")
                weighted_graph[node].append((neighbor_node, weight))
                all_nodes.add(neighbor_node) # Add neighbor to the set of all nodes
            else:
                # Assume unweighted edge (neighbor_node only), default weight 1
                neighbor_node = neighbor_info
                weight = 1
                weighted_graph[node].append((neighbor_node, weight))
                all_nodes.add(neighbor_node) # Add neighbor to the set of all nodes

    # Check if start or end nodes exist in the graph structure
    if start not in all_nodes or end not in all_nodes:
        # If either node wasn't found anywhere (as key or neighbor)
        return -1

    # Initialize distances: infinite for all nodes except start
    distance = collections.defaultdict(lambda: inf)
    distance[start] = 0

    # Priority queue: stores tuples of (current_distance, node)
    # Using heapq makes it a min-priority queue
    pq = [(0, start)]

    # Set to keep track of nodes for which the shortest path has been finalized
    processed_nodes = set()

    while pq:
        # Get the node with the smallest distance from the priority queue
        current_dist, current_node = heapq.heappop(pq)

        # If we already found a shorter path to this node, skip
        # This handles cases where a node is added multiple times to the pq
        # with different distances. We only process the first (shortest) one.
        if current_dist > distance[current_node]:
             continue

        # If we reached the end node, return its distance
        if current_node == end:
            return current_dist if current_dist != inf else -1 # Map inf back to -1

        # Mark the node as processed (shortest path finalized)
        # Note: Adding to processed_nodes here instead of before the end check
        # ensures we return the distance even if end is the first node popped.
        # Some implementations use a slightly different visited logic, but this works.
        # Alternative: check `if current_node in processed_nodes: continue` here.
        # Let's stick to the common pattern of checking distance first.

        # Explore neighbors
        # Use weighted_graph which ensures weights exist
        for neighbor, weight in weighted_graph.get(current_node, []):
             # Calculate distance through the current node
             new_dist = current_dist + weight

             # If found a shorter path to the neighbor
             if new_dist < distance[neighbor]:
                 distance[neighbor] = new_dist
                 # Add the neighbor to the priority queue with the new distance
                 heapq.heappush(pq, (new_dist, neighbor))

    # If the loop finishes without reaching the end node
    final_distance = distance[end]
    return final_distance if final_distance != inf else -1