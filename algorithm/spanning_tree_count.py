import numpy as np
import collections

def count_spanning_trees(graph):
    """
    Counts the number of spanning trees in an undirected graph (can be a multigraph)
    using the Matrix-Tree Theorem (Kirchhoff's Theorem).

    Args:
        graph: The graph representation as an adjacency list. Assumes undirected.
               Example: {0: [1, 2], 1: [0, 2], 2: [0, 1]}
               Example (Multigraph): {0: [1, 1, 2], 1: [0, 0], 2: [0]}

    Returns:
        int: Number of spanning trees in the graph. Returns 0 if the graph
             has no vertices or is disconnected (considering only the part
             represented in the graph dict).
    """
    if not graph:
        # Handle empty graph representation or graph with nodes but no edges defined via keys
        # Let's refine this: find all nodes first.
        pass

    # --- Step 1: Identify ALL unique vertices ---
    nodes = set(graph.keys())
    for u in graph:
        for neighbor_info in graph.get(u, []):
            v = neighbor_info if not isinstance(neighbor_info, tuple) else neighbor_info[0]
            nodes.add(v)

    if not nodes:
        return 0 # No nodes at all

    sorted_vertices = sorted(list(nodes))
    n = len(sorted_vertices)

    # Trivial cases
    if n == 0:
       return 0 # Should not happen if nodes is populated, but for safety
    if n == 1:
       # Check if there are edges (loops). The theorem usually assumes no loops,
       # but let's see. A single node has 1 spanning tree (itself).
       # We need to ensure it's connected if n > 1 later.
       # If graph was {0: [0]}, degree is 1 or 2 depending on loop definition.
       # Standard definition: 1 spanning tree for a single vertex.
       return 1

    # Create a vertex to index mapping
    vertex_to_idx = {vertex: i for i, vertex in enumerate(sorted_vertices)}

    # --- Step 2: Create the Laplacian matrix ---
    # L = D - A
    # Correctly handles multigraphs
    L = np.zeros((n, n), dtype=float) # Use float for determinant calculation

    for u_node, neighbors in graph.items():
        if u_node not in vertex_to_idx: continue # Should not happen with corrected node finding
        u_idx = vertex_to_idx[u_node]

        # Add degree to diagonal
        L[u_idx, u_idx] = len(neighbors) # Degree includes multi-edges

        # Subtract 1 for each edge in off-diagonal
        neighbor_counts = collections.Counter(
            (neighbor if not isinstance(neighbor, tuple) else neighbor[0])
            for neighbor in neighbors
        )

        for v_node, count in neighbor_counts.items():
            if v_node in vertex_to_idx:
                v_idx = vertex_to_idx[v_node]
                if u_idx != v_idx: # Avoid self-loops affecting off-diagonal
                   L[u_idx, v_idx] -= count

    # --- Step 3: Calculate any cofactor ---
    # Remove the first row and column (arbitrary choice)
    # Check if matrix dimension is sufficient
    if n <= 1:
         # We already handled n=1, this is safety for n=0 or unexpected n=1 reach
         # If n=1, L is [[degree]]. Reduced matrix doesn't exist. Should return 1 based on earlier check.
         # If somehow we get here with n=1, let's stick to the definition.
         # A graph needs >= 2 vertices for the cofactor method to be applied typically.
         # Let's rely on the n=1 check earlier. If n=0, L is empty.
         if n == 1: return 1 # Reiterate the single node case
         return 0 # No spanning tree if n=0


    # Check if the graph might be disconnected *before* calculating determinant.
    # A quick check (though not foolproof for all cases) is if any node degree is 0
    # for n > 1. But the determinant method handles this anyway.

    L_reduced = L[1:, 1:] # Remove row 0 and column 0

    # --- Step 4: Calculate determinant ---
    try:
        # Use np.linalg.det which is generally robust
        det_val = np.linalg.det(L_reduced)
        # Result must be an integer, round carefully due to potential float precision issues
        # Use a tolerance check before rounding if very large numbers are expected
        tree_count = round(abs(det_val))
        # Check if rounding was significant
        if not np.isclose(abs(det_val), tree_count):
             print(f"Warning: Determinant {abs(det_val)} significantly differs from rounded value {tree_count}. Potential precision issue.")
             # Fallback or raise error might be needed depending on context

        # Ensure integer type
        return int(tree_count)

    except np.linalg.LinAlgError:
        # Matrix might be singular (e.g., graph disconnected)
        return 0
    except Exception as e:
        # Catch other potential errors
        print(f"An error occurred during determinant calculation: {e}")
        return 0