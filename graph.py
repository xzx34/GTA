import random

class GraphGenerator:
    def __init__(self, num_vertices, num_edges, is_connected=True, is_weighted=False, has_capacity=False):
        self.num_vertices = num_vertices
        self.num_edges = num_edges
        self.is_connected = is_connected
        self.is_weighted = is_weighted
        self.has_capacity = has_capacity
    
    def generate(self):
        # Initialize an empty graph
        graph = []
        edges_set = set()  # Used to check for duplicate edges
        
        if "tree" in getattr(self, "graph_types", []):
            self.num_edges = self.num_vertices - 1
            self.is_connected = True  
        
        # If we want a connected graph, first generate a tree
        if self.is_connected is True:
            self._generate_tree(graph, edges_set)
            if "tree" in getattr(self, "graph_types", []) or self.num_edges == self.num_vertices - 1:
                return self.format_output(graph)
            self._add_remaining_edges(graph, edges_set)
            return self.format_output(graph)
        elif self.is_connected is False:
            # Directly add random edges
            self._add_random_edges(graph, edges_set)
            # Check connectivity, if required to be disconnected but graph is connected, regenerate
            if not self._is_connected(graph):
                return self.format_output(graph)
            # If graph is connected but required to be disconnected, regenerate
            return self.generate()
        else:  # self.is_connected is None
            # No connectivity check required, just add random edges
            self._add_random_edges(graph, edges_set)
            return self.format_output(graph)
    
    def _generate_tree(self, graph, edges_set):
        """Generate a random spanning tree as the basis for a connected graph"""
        # Initialize connected and unconnected vertex sets
        connected_vertices = {1}
        unconnected_vertices = set(range(2, self.num_vertices + 1))
        
        # Create a spanning tree
        while unconnected_vertices:
            v1 = random.choice(list(connected_vertices))
            v2 = random.choice(list(unconnected_vertices))
            
            weight = random.randint(1, 100) if self.is_weighted else 1
            capacity = random.randint(1, 10) if self.has_capacity else 0
            
            edge = [v1, v2]
            if self.is_weighted:
                edge.append(weight)
            if self.has_capacity:
                edge.append(capacity)
            
            graph.append(edge)
            edges_set.add((v1, v2))
            edges_set.add((v2, v1))  # For undirected graph, add both directions
            
            connected_vertices.add(v2)
            unconnected_vertices.remove(v2)
    
    def _add_remaining_edges(self, graph, edges_set):
        """Add the remaining random edges"""
        remaining_edges = self.num_edges - len(graph)
        
        while remaining_edges > 0:
            v1 = random.randint(1, self.num_vertices)
            v2 = random.randint(1, self.num_vertices)
            
            # Avoid self-loops and duplicate edges
            if v1 != v2 and (v1, v2) not in edges_set:
                weight = random.randint(1, 100) if self.is_weighted else 1
                capacity = random.randint(1, 10) if self.has_capacity else 0
                
                edge = [v1, v2]
                if self.is_weighted:
                    edge.append(weight)
                if self.has_capacity:
                    edge.append(capacity)
                
                graph.append(edge)
                edges_set.add((v1, v2))
                edges_set.add((v2, v1))
                remaining_edges -= 1
    
    def _add_random_edges(self, graph, edges_set):
        """Add a specified number of random edges"""
        edges_added = 0
        
        while edges_added < self.num_edges:
            v1 = random.randint(1, self.num_vertices)
            v2 = random.randint(1, self.num_vertices)
            
            # Avoid self-loops and duplicate edges
            if v1 != v2 and (v1, v2) not in edges_set:
                weight = random.randint(1, 100) if self.is_weighted else 1
                capacity = random.randint(1, 10) if self.has_capacity else 0
                
                edge = [v1, v2]
                if self.is_weighted:
                    edge.append(weight)
                if self.has_capacity:
                    edge.append(capacity)
                
                graph.append(edge)
                edges_set.add((v1, v2))
                edges_set.add((v2, v1))
                edges_added += 1
    
    def _is_connected(self, graph):
        """Check if the graph is connected"""
        if not graph:
            return self.num_vertices <= 1
        
        # Build adjacency list
        adj_list = [[] for _ in range(self.num_vertices + 1)]
        for edge in graph:
            v1, v2 = edge[0], edge[1]
            adj_list[v1].append(v2)
            adj_list[v2].append(v1)
        
        # Use DFS to check connectivity
        visited = [False] * (self.num_vertices + 1)
        
        def dfs(node):
            visited[node] = True
            for neighbor in adj_list[node]:
                if not visited[neighbor]:
                    dfs(neighbor)
        
        # Start DFS from node 1
        dfs(1)
        
        # Check if all nodes were visited
        return all(visited[1:])
    
    def format_output(self, graph):
        result = f"{self.num_vertices} {self.num_edges}\n"
        
        for edge in graph:
            result += " ".join(map(str, edge)) + "\n"
            
        return result


class GraphDescriber:    
    def natural_language_description(self, graph_output, has_weights=False, has_capacity=False):
        lines = graph_output.strip().split('\n')
        first_line = lines[0].split()
        
        num_vertices = int(first_line[0])
        num_edges = int(first_line[1])
        
        # Parse edges
        edges = []
        for i in range(1, len(lines)):
            if lines[i].strip():  # Ensure line is not empty
                parts = list(map(int, lines[i].split()))
                edge_info = {"from": parts[0], "to": parts[1]}
                
                if has_weights and len(parts) > 2:
                    edge_info["weight"] = parts[2]
                
                if has_capacity and len(parts) > (3 if has_weights else 2):
                    edge_info["capacity"] = parts[-1]
                
                edges.append(edge_info)

        description = f"This is an undirected graph with {num_vertices} vertices and {num_edges} edges. "
        
        if has_weights and has_capacity:
            description += "The graph has both weights and capacity constraints on its edges. "
        elif has_weights:
            description += "Each edge in the graph has a weight value. "
        elif has_capacity:
            description += "Each edge in the graph has a capacity constraint. "
        
        description += "\n\nThe graph contains the following connections:\n\n"
        
        for edge in edges:
            v1, v2 = edge["from"], edge["to"]
            edge_desc = f"There is an edge between vertex {v1} and vertex {v2}"
            
            if "weight" in edge and "capacity" in edge:
                edge_desc += f" with a weight of {edge['weight']} and a capacity of {edge['capacity']}."
            elif "weight" in edge:
                edge_desc += f" with a weight of {edge['weight']}."
            elif "capacity" in edge:
                edge_desc += f" with a capacity of {edge['capacity']}."
            else:
                edge_desc += "."
            
            description += edge_desc + "\n"
        
        return description
    
    def structured_text_description(self, graph_output, has_weights=False, has_capacity=False):
        lines = graph_output.strip().split('\n')
        first_line = lines[0].split()
        
        num_vertices = int(first_line[0])
        num_edges = int(first_line[1])
        
        # Check graph connectivity
        edges = []
        for i in range(1, len(lines)):
            if lines[i].strip():
                parts = list(map(int, lines[i].split()))
                edges.append({"from": parts[0], "to": parts[1]})
        
        graph_type = "Undirected"
        if has_weights:
            graph_type += ", Weighted"
        if has_capacity:
            graph_type += ", With Capacity"
        
        description = f"{graph_type} Graph with {num_vertices} vertices and {num_edges} edges\n\n"
        
        # Edge format description
        if has_weights and has_capacity:
            description += "Edges (Format: Node Node Weight Capacity):\n"
        elif has_weights:
            description += "Edges (Format: Node Node Weight):\n"
        elif has_capacity:
            description += "Edges (Format: Node Node Capacity):\n"
        else:
            description += "Edges (Format: Node Node):\n"
        
        for i in range(1, len(lines)):
            if lines[i].strip():  # Ensure line is not empty
                description += lines[i] + "\n"
        
        return description
        
    def adjacency_matrix_description(self, graph_output, has_weights=False, has_capacity=False):
        """Generate adjacency matrix description of the graph"""
        lines = graph_output.strip().split('\n')
        first_line = lines[0].split()
        
        num_vertices = int(first_line[0])
        num_edges = int(first_line[1])
        
        # Initialize adjacency matrices with zeros
        adjacency_matrix = [[0 for _ in range(num_vertices + 1)] for _ in range(num_vertices + 1)]
        capacity_matrix = [[0 for _ in range(num_vertices + 1)] for _ in range(num_vertices + 1)]
        
        # Fill the adjacency matrices
        for i in range(1, len(lines)):
            if lines[i].strip():
                parts = list(map(int, lines[i].split()))
                v1, v2 = parts[0], parts[1]
                
                # For weighted graph
                if has_weights and len(parts) > 2:
                    weight = parts[2]
                    adjacency_matrix[v1][v2] = weight
                    adjacency_matrix[v2][v1] = weight
                else:
                    adjacency_matrix[v1][v2] = 1
                    adjacency_matrix[v2][v1] = 1
                
                # For graph with capacity
                if has_capacity:
                    capacity_idx = 3 if has_weights else 2
                    if len(parts) > capacity_idx:
                        capacity = parts[capacity_idx]
                        capacity_matrix[v1][v2] = capacity
                        capacity_matrix[v2][v1] = capacity
        
        # Build the text description
        description = f"This is an undirected graph with {num_vertices} vertices and {num_edges} edges.\n\n"
        
        # Add explanation
        if has_weights and has_capacity:
            description += "The graph has both weights and capacities on its edges.\n"
            description += "- Weight Matrix: Shows the weight of each edge (0 means no connection).\n"
            description += "- Capacity Matrix: Shows the capacity of each edge (0 means no connection).\n\n"
        elif has_weights:
            description += "The graph has weights on its edges.\n"
            description += "- Weight Matrix: Shows the weight of each edge (0 means no connection).\n\n"
        elif has_capacity:
            description += "The graph has capacity constraints on its edges.\n"
            description += "- Adjacency Matrix: 1 indicates an edge exists, 0 means no connection.\n"
            description += "- Capacity Matrix: Shows the capacity of each edge (0 means no connection).\n\n"
        else:
            description += "- Adjacency Matrix: 1 indicates an edge exists, 0 means no connection.\n\n"
        
        # Format and add matrices
        header = "    " + " ".join(f"{i:3d}" for i in range(1, num_vertices + 1))
        separator = "   " + "-" * (4 * num_vertices)
        
        # Add adjacency/weight matrix with appropriate title
        if has_weights:
            description += f"Weight Matrix ({num_vertices}×{num_vertices}):\n\n"
        else:
            description += f"Adjacency Matrix ({num_vertices}×{num_vertices}):\n\n"
            
        description += header + "\n" + separator + "\n"
        for i in range(1, num_vertices + 1):
            row = f"{i:2d} |"
            for j in range(1, num_vertices + 1):
                row += f"{adjacency_matrix[i][j]:3d} "
            description += row + "\n"
        
        # Add capacity matrix if needed
        if has_capacity:
            description += f"\nCapacity Matrix ({num_vertices}×{num_vertices}):\n\n"
            description += header + "\n" + separator + "\n"
            for i in range(1, num_vertices + 1):
                row = f"{i:2d} |"
                for j in range(1, num_vertices + 1):
                    row += f"{capacity_matrix[i][j]:3d} "
                description += row + "\n"
        
        return description
        
    def adjacency_list_description(self, graph_output, has_weights=False, has_capacity=False):
        """Generate adjacency list description of the graph"""
        lines = graph_output.strip().split('\n')
        first_line = lines[0].split()
        
        num_vertices = int(first_line[0])
        num_edges = int(first_line[1])
        
        # Initialize adjacency lists
        adj_list = [[] for _ in range(num_vertices + 1)]
        
        # Fill the adjacency lists
        for i in range(1, len(lines)):
            if lines[i].strip():
                parts = list(map(int, lines[i].split()))
                v1, v2 = parts[0], parts[1]
                
                # Create edge information
                edge_info1 = {"vertex": v2}
                edge_info2 = {"vertex": v1}
                
                if has_weights and len(parts) > 2:
                    weight = parts[2]
                    edge_info1["weight"] = weight
                    edge_info2["weight"] = weight
                
                if has_capacity:
                    capacity_idx = 3 if has_weights else 2
                    if len(parts) > capacity_idx:
                        capacity = parts[capacity_idx]
                        edge_info1["capacity"] = capacity
                        edge_info2["capacity"] = capacity
                
                adj_list[v1].append(edge_info1)
                adj_list[v2].append(edge_info2)  # For undirected graph
        
        # Build the text description
        description = f"This is an undirected graph with {num_vertices} vertices and {num_edges} edges.\n\n"
        
        # Add explanation
        if has_weights and has_capacity:
            description += "The graph has both weights and capacities on its edges.\n"
            description += "- Adjacency List: For each vertex, lists all connected vertices with edge weights and capacities.\n\n"
        elif has_weights:
            description += "The graph has weights on its edges.\n"
            description += "- Adjacency List: For each vertex, lists all connected vertices with edge weights.\n\n"
        elif has_capacity:
            description += "The graph has capacity constraints on its edges.\n"
            description += "- Adjacency List: For each vertex, lists all connected vertices with edge capacities.\n\n"
        else:
            description += "- Adjacency List: For each vertex, lists all connected vertices.\n\n"
        
        # Format and add adjacency list
        description += "Adjacency List:\n\n"
        
        for i in range(1, num_vertices + 1):
            vertex_desc = f"Vertex {i}: "
            
            if not adj_list[i]:
                vertex_desc += "No connections"
            else:
                connections = []
                for edge in adj_list[i]:
                    conn = f"{edge['vertex']}"
                    if has_weights and "weight" in edge and has_capacity and "capacity" in edge:
                        conn += f" (weight={edge['weight']}, capacity={edge['capacity']})"
                    elif has_weights and "weight" in edge:
                        conn += f" (weight={edge['weight']})"
                    elif has_capacity and "capacity" in edge:
                        conn += f" (capacity={edge['capacity']})"
                    connections.append(conn)
                
                vertex_desc += ", ".join(connections)
            
            description += vertex_desc + "\n"
        
        return description



# is_weighted=0
# has_capacity=0
# generator = GraphGenerator(5, 7, is_connected=True, is_weighted=is_weighted, has_capacity=has_capacity)
# graph = generator.generate()
# describer = GraphDescriber()
# print(describer.natural_language_description(graph, has_weights=is_weighted, has_capacity=has_capacity))
# print("\n" + "-"*50 + "\n")
# print(describer.structured_text_description(graph, has_weights=is_weighted, has_capacity=has_capacity))
# print("\n" + "-"*50 + "\n")
# print(describer.adjacency_matrix_description(graph, has_weights=is_weighted, has_capacity=has_capacity))
# print("\n" + "-"*50 + "\n")
# print(describer.adjacency_list_description(graph, has_weights=is_weighted, has_capacity=has_capacity))
