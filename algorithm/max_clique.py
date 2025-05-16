import collections

def find_max_clique_size(graph):
    """
    Finds the size of the maximum clique in an undirected graph using the
    Bron-Kerbosch algorithm with pivoting.

    A clique is a subset of vertices where every two distinct vertices are adjacent.
    The maximum clique is the largest such subset.

    Args:
        graph: The graph representation as an adjacency list (dictionary).
               Keys are nodes, values are iterables (list, tuple, or set) of neighbors.
               Handles neighbors represented as node IDs or tuples (node_id, weight).

    Returns:
        int: The size of the maximum clique found in the graph. Returns 0 for an empty graph.
    """
    if not graph:
        return 0

    # --- Preprocessing: Ensure neighbors are stored in sets for efficient operations ---
    adj = collections.defaultdict(set)
    all_nodes = set()
    for u, neighbors in graph.items():
        all_nodes.add(u)
        for neighbor in neighbors:
            v = neighbor[0] if isinstance(neighbor, tuple) else neighbor
            # Ensure undirectedness for Bron-Kerbosch logic if input might be asymmetric
            adj[u].add(v)
            adj[v].add(u) # Add edge in both directions
            all_nodes.add(v) # Make sure all mentioned nodes are included

    # --- Bron-Kerbosch Algorithm with Pivoting ---
    max_size = 0

    def bron_kerbosch_pivot(R, P, X):
        """
        Recursive helper function for Bron-Kerbosch.
        Args:
            R: Set of vertices currently in the potential clique being built.
            P: Set of candidate vertices that can extend R (connected to all in R).
            X: Set of vertices already processed and excluded from extending R.
        """
        nonlocal max_size # Allow modification of the outer scope's max_size

        # Base case: If no more candidates and no excluded nodes that could form a clique with R
        if not P and not X:
            max_size = max(max_size, len(R))
            return

        # Pruning: If P is empty, we can't extend further from here.
        if not P:
            return

        # --- Pivoting Strategy ---
        # Choose a pivot 'u' from P union X with the largest number of neighbors in P.
        # This heuristic helps to reduce the number of recursive calls.
        pivot_candidates = P | X # Union of candidates and excluded nodes
        pivot = next(iter(pivot_candidates)) # Initial pivot choice (can be any node)
        max_neighbors_in_p = -1

        # Find the best pivot (maximizes neighbors in P)
        # Iterate through a temporary list to avoid issues modifying set during iteration
        for u_potential in list(pivot_candidates):
            neighbors_of_u_in_p = len(P & adj.get(u_potential, set()))
            if neighbors_of_u_in_p > max_neighbors_in_p:
                max_neighbors_in_p = neighbors_of_u_in_p
                pivot = u_potential

        # --- Recursive Step ---
        # Iterate only over candidates 'v' in P that are *not* neighbors of the pivot.
        # Any maximal clique must contain the pivot *or* a node not connected to the pivot.
        P_without_pivot_neighbors = P - adj.get(pivot, set())

        # Iterate through a copy, because P gets modified inside the loop
        for v in list(P_without_pivot_neighbors):
            neighbors_v = adj.get(v, set())
            # Recursively call for the clique extended by 'v'
            bron_kerbosch_pivot(R | {v}, P & neighbors_v, X & neighbors_v)
            # Backtrack: Move 'v' from candidates P to excluded X
            P.remove(v)
            X.add(v)

    # Initial call to the algorithm
    # R starts empty, P contains all nodes, X starts empty
    bron_kerbosch_pivot(set(), all_nodes.copy(), set())

    return max_size