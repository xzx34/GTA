import collections
from collections import deque

# Note: Assuming input 'graph' represents a tree for diameter, centroid, LCA,
# and max independent set calculations. Input format allows neighbors to be
# node IDs or tuples (node_id, weight), but weights are ignored in these functions.

def find_tree_diameter(graph):
    """
    Calculates the diameter of a tree (longest path between any two nodes).
    Uses two BFS traversals.
    """
    if not graph:
        return 0

    # Build unweighted adjacency list representation
    tree = collections.defaultdict(list)
    nodes = set()
    for node, neighbors in graph.items():
        nodes.add(node)
        for neighbor_info in neighbors:
            neighbor_node = neighbor_info[0] if isinstance(neighbor_info, tuple) else neighbor_info
            tree[node].append(neighbor_node)
            # Also add the reverse edge if not implicitly undirected
            # Assuming the input might not be perfectly symmetric
            tree[neighbor_node].append(node)
            nodes.add(neighbor_node)

    if not nodes:
         return 0 # Handle case where graph dict exists but is empty

    # Pick an arbitrary start node
    # Ensure start_node exists in the processed tree structure
    start_node = next(iter(nodes))

    # First BFS: Find the node farthest from the start node
    farthest_node_1, _ = _bfs_farthest(tree, start_node, nodes)
    if farthest_node_1 is None: # Graph might be empty or disconnected (not a tree)
        return 0 # Diameter is 0 if only one node or empty

    # Second BFS: Find the node farthest from farthest_node_1
    _, distance = _bfs_farthest(tree, farthest_node_1, nodes)

    return distance

def _bfs_farthest(tree, start, all_nodes):
    """Helper BFS to find the farthest node and distance from start."""
    if start not in tree and start not in all_nodes:
         # Start node doesn't exist
         return None, 0
    if not tree.get(start) and len(all_nodes) == 1 and start in all_nodes:
         # Handle single node graph correctly
         return start, 0

    visited = {start}
    queue = deque([(start, 0)])  # (node, distance)
    farthest_node = start
    max_distance = 0

    while queue:
        node, distance = queue.popleft()

        if distance > max_distance:
            max_distance = distance
            farthest_node = node

        # Check neighbors using tree.get for safety
        for neighbor in tree.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))

    return farthest_node, max_distance


def find_tree_centroid(graph):
    """
    Finds a centroid of the tree (node minimizing the max size of remaining components
    after its removal). Returns the smallest ID if multiple centroids exist.
    """
    if not graph:
        return 0 # Consistent with original, though None might be clearer

    # Build unweighted adjacency list representation
    tree = collections.defaultdict(list)
    all_nodes = set()
    node_count = 0
    processed_edges = set()

    for u, neighbors in graph.items():
        all_nodes.add(u)
        for v_info in neighbors:
            v = v_info[0] if isinstance(v_info, tuple) else v_info
            all_nodes.add(v)
            edge = tuple(sorted((u, v)))
            if edge not in processed_edges:
                tree[u].append(v)
                tree[v].append(u)
                processed_edges.add(edge)

    node_count = len(all_nodes)
    if node_count <= 1:
        # Handle empty or single-node graph
        return next(iter(all_nodes)) if node_count == 1 else 0

    subtree_size = collections.defaultdict(int)
    max_remaining_component_size = collections.defaultdict(lambda: float('inf'))
    visited = set()

    # DFS to calculate subtree sizes
    def dfs_size(node, parent):
        visited.add(node)
        current_size = 1
        max_child_subtree = 0
        for child in tree.get(node, []):
            if child != parent:
                if child not in visited: # Avoid cycles if input isn't strictly a tree
                   dfs_size(child, node)
                   current_size += subtree_size[child]
                   max_child_subtree = max(max_child_subtree, subtree_size[child])
                # If visited and not parent, indicates cycle - behavior undefined for non-tree
                # else: pass # ignore parent or already visited nodes in cycle

        subtree_size[node] = current_size
        # Calculate max size of remaining components if 'node' is removed
        size_of_parent_component = node_count - current_size
        max_remaining_component_size[node] = max(max_child_subtree, size_of_parent_component)

    # Start DFS from an arbitrary node
    start_node = next(iter(all_nodes))
    dfs_size(start_node, -1) # Use -1 or None to indicate no parent for root

    # Find the node(s) with the minimum max_remaining_component_size
    min_max_size = float('inf')
    centroid = -1 # Initialize centroid to an invalid value

    # Iterate through sorted nodes to find the smallest ID centroid
    for node in sorted(list(all_nodes)):
        # Need to handle cases where DFS didn't reach all nodes (disconnected graph)
        # If a node wasn't reached, its max_remaining_component_size remains 'inf'
        if node in max_remaining_component_size:
             current_max_size = max_remaining_component_size[node]
             if current_max_size < min_max_size:
                 min_max_size = current_max_size
                 centroid = node
             # If sizes are equal, the sorting ensures we keep the smaller node ID

    # Check if a valid centroid was found
    # If graph was disconnected, some nodes might not have been processed by DFS
    # and centroid might remain -1 or be incorrect.
    # For a true tree, centroid should always be found.
    if centroid == -1 and node_count > 0:
         # Fallback or error? If graph is guaranteed tree, this shouldn't happen.
         # If not guaranteed, maybe return the first node or signal error.
         # Sticking to original logic's potential flaws if centroid not found:
         return next(iter(all_nodes)) if all_nodes else 0 # Or return -1?
    elif centroid == -1 and node_count == 0:
        return 0

    return centroid


def find_tree_lca(graph, node1, node2):
    """
    Finds the Lowest Common Ancestor (LCA) of node1 and node2 in a tree,
    assuming the tree is rooted at node 1.
    """
    if not graph:
        return -1 # Return -1 for empty graph

    # Build unweighted adjacency list representation
    tree = collections.defaultdict(list)
    all_nodes = set()
    processed_edges = set()

    for u, neighbors in graph.items():
        all_nodes.add(u)
        for v_info in neighbors:
            v = v_info[0] if isinstance(v_info, tuple) else v_info
            all_nodes.add(v)
            edge = tuple(sorted((u, v)))
            if edge not in processed_edges:
                tree[u].append(v)
                tree[v].append(u)
                processed_edges.add(edge)

    root = 1 # Explicitly assume root is 1 as per original logic

    if root not in all_nodes:
         return -1 # Root node doesn't exist in the graph

    # Build parent pointers and depth using DFS from the assumed root
    parent = {root: -1}
    depth = {root: 0}
    queue = deque([root])
    visited_dfs = {root}

    # Perform BFS or DFS to build parent/depth - BFS might be slightly less prone to recursion depth issues
    while queue:
        u = queue.popleft()
        for v in tree.get(u, []):
             if v not in visited_dfs:
                  visited_dfs.add(v)
                  parent[v] = u
                  depth[v] = depth[u] + 1
                  queue.append(v)

    # Check if nodes exist in the tree component reachable from root 1
    if node1 not in depth or node2 not in depth:
        return -1

    # Level the nodes to the same depth
    # Use .get with default to avoid KeyError if a node wasn't reachable (though checked above)
    while depth.get(node1, -1) > depth.get(node2, -1):
        node1 = parent.get(node1, -1)
        if node1 == -1: return -1 # Should not happen if nodes are in depth map
    while depth.get(node2, -1) > depth.get(node1, -1):
        node2 = parent.get(node2, -1)
        if node2 == -1: return -1

    # Move both nodes up until they meet
    while node1 != node2:
        node1 = parent.get(node1, -1)
        node2 = parent.get(node2, -1)
        # If either becomes -1, it means they didn't share a common ancestor (implies graph wasn't connected tree rooted at 1)
        if node1 == -1 or node2 == -1:
            return -1

    return node1


def find_tree_max_independent_set(graph):
    """
    Calculates the size of the Maximum Independent Set (MIS) in a tree using DP.
    """
    if not graph:
        return 0

    # Build unweighted adjacency list representation
    tree = collections.defaultdict(list)
    all_nodes = set()
    processed_edges = set()

    for u, neighbors in graph.items():
        all_nodes.add(u)
        for v_info in neighbors:
            v = v_info[0] if isinstance(v_info, tuple) else v_info
            all_nodes.add(v)
            edge = tuple(sorted((u, v)))
            if edge not in processed_edges:
                tree[u].append(v)
                tree[v].append(u)
                processed_edges.add(edge)

    if not all_nodes:
        return 0

    # dp[node][0]: Max independent set size in subtree rooted at 'node', node NOT included.
    # dp[node][1]: Max independent set size in subtree rooted at 'node', node IS included.
    dp = collections.defaultdict(lambda: [0, 0])
    visited = set()

    def dfs_dp(node, parent):
        visited.add(node)
        dp[node][1] = 1 # If node is included, count = 1 + sum(dp[child][0])
        dp[node][0] = 0 # If node is not included, count = sum(max(dp[child][0], dp[child][1]))

        for child in tree.get(node, []):
            if child != parent:
                if child not in visited: # Process only unvisited children
                    dfs_dp(child, node)
                    dp[node][0] += max(dp[child][0], dp[child][1])
                    dp[node][1] += dp[child][0]
                # If visited and not parent -> cycle, MIS on general graphs is NP-hard.
                # Assuming tree input, this path shouldn't be taken.

    # Start DFS from an arbitrary node in the tree
    start_node = next(iter(all_nodes))
    dfs_dp(start_node, -1) # Use -1 or None for parent of root

    # Result is the max of including or not including the start_node
    # This assumes the graph is connected (a single tree)
    return max(dp[start_node][0], dp[start_node][1])