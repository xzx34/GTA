
def has_hamiltonian_path(graph):
    if not graph:
        return False
    if len(graph) == 1:
        return True

    vertices = list(graph.keys())
    n = len(vertices)

    def backtrack(current, visited, path):
        if len(path) == n:
            return True
        for neighbor in graph.get(current, []):
            neighbor_id = neighbor if not isinstance(neighbor, tuple) else neighbor[0]
            if neighbor_id in visited and not visited[neighbor_id]:
                visited[neighbor_id] = True
                path.append(neighbor_id)
                if backtrack(neighbor_id, visited, path):
                    return True
                path.pop()
                visited[neighbor_id] = False
        return False

    for start_vertex in vertices:
        visited = {v: False for v in vertices}
        visited[start_vertex] = True
        if backtrack(start_vertex, visited, [start_vertex]):
            return True
    return False

def has_hamiltonian_circuit(graph):
    if not graph:
        return False
    if len(graph) == 1:
        node = list(graph.keys())[0]
        for neighbor in graph.get(node, []):
            neighbor_id = neighbor if not isinstance(neighbor, tuple) else neighbor[0]
            if neighbor_id == node:
                return True
        return False

    vertices = list(graph.keys())
    n = len(vertices)

    def backtrack(current, visited, path):
        if len(path) == n:
            # Check if we can return to start
            for neighbor in graph.get(current, []):
                neighbor_id = neighbor if not isinstance(neighbor, tuple) else neighbor[0]
                if neighbor_id == path[0]:
                    return True
            return False
        for neighbor in graph.get(current, []):
            neighbor_id = neighbor if not isinstance(neighbor, tuple) else neighbor[0]
            if neighbor_id in visited and not visited[neighbor_id]:
                visited[neighbor_id] = True
                path.append(neighbor_id)
                if backtrack(neighbor_id, visited, path):
                    return True
                path.pop()
                visited[neighbor_id] = False
        return False

    for start_vertex in vertices:
        visited = {v: False for v in vertices}
        visited[start_vertex] = True
        if backtrack(start_vertex, visited, [start_vertex]):
            return True

    return False