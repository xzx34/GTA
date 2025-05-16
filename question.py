import random
import json
import os
import argparse
from graph import GraphGenerator, GraphDescriber
from algorithm import (
    check_connectivity, check_bipartite, count_cycles, count_triangles, 
    find_minimum_cycle, parse_graph_string, find_max_clique_size, 
    find_max_independent_set_size, count_bridges, count_biconnected_components,
    has_eulerian_path, has_eulerian_circuit, has_hamiltonian_path, 
    has_hamiltonian_circuit, count_spanning_trees, find_shortest_path_length,
    find_mst_weight, find_second_mst_weight, find_tree_diameter, find_tree_centroid,
    find_tree_lca, find_tree_max_independent_set, find_maximum_flow, find_minimum_cut,
    find_min_cost_max_flow
)

# List of task types and their parameters
TASKS = [
    {
        "name": "Connectivity",
        "description": "Check if two vertices are connected",
        "nodes": 16,
        "graph_types": ["sparse", "dense"],
        "is_connected": None, 
        "is_weighted": False,
        "has_capacity": False
    },
    {
        "name": "Bipartite",
        "description": "Determine if the graph is bipartite",
        "nodes": 16,
        "graph_types": ["sparse", "dense"],
        "is_connected": None,
        "is_weighted": False,
        "has_capacity": False
    },
    {
        "name": "Minimum Cycle",
        "description": "Find the size of the smallest cycle in the graph",
        "nodes": 16,
        "graph_types": ["sparse", "dense"],
        "is_connected": None,
        "is_weighted": False,
        "has_capacity": False
    },
    {
        "name": "Maximum Clique",
        "description": "Find the size of the maximum clique in the graph",
        "nodes": 16,
        "graph_types": ["sparse", "dense"],
        "is_connected": True,
        "is_weighted": False,
        "has_capacity": False
    },
    {
        "name": "Maximum Independent Set",
        "description": "Find the size of the maximum independent set in the graph",
        "nodes": 16,
        "graph_types": ["sparse", "dense"],
        "is_connected": None,
        "is_weighted": False,
        "has_capacity": False
    },
    {
        "name": "Eulerian Path",
        "description": "Determine if the graph has an Eulerian path",
        "nodes": 16,
        "graph_types": ["sparse", "dense"],
        "is_connected": True,
        "is_weighted": False,
        "has_capacity": False
    },
    {
        "name": "Eulerian Circuit",
        "description": "Determine if the graph has an Eulerian circuit",
        "nodes": 16,
        "graph_types": ["sparse", "dense"],
        "is_connected": True,
        "is_weighted": False,
        "has_capacity": False
    },
    {
        "name": "Hamiltonian Path",
        "description": "Determine if the graph has a Hamiltonian path",
        "nodes": 16,
        "graph_types": ["sparse", "dense"],
        "is_connected": True,
        "is_weighted": False,
        "has_capacity": False
    },
    {
        "name": "Hamiltonian Circuit",
        "description": "Determine if the graph has a Hamiltonian circuit",
        "nodes": 16,
        "graph_types": ["sparse", "dense"],
        "is_connected": True,
        "is_weighted": False,
        "has_capacity": False
    },
    {
        "name": "Biconnected Components",
        "description": "Count the number of biconnected components in the graph",
        "nodes": 12,
        "graph_types": ["sparse", "dense"],
        "is_connected": None,
        "is_weighted": False,
        "has_capacity": False
    },
    {
        "name": "Bridge Count",
        "description": "Count the number of bridges (cut edges) in the graph",
        "nodes": 12,
        "graph_types": ["sparse", "dense"],
        "is_connected": None,
        "is_weighted": False,
        "has_capacity": False
    },
    {
        "name": "Triangle Count",
        "description": "Count the number of triangles (cycles of length 3) in the graph",
        "nodes": 12,
        "graph_types": ["sparse", "dense"],
        "is_connected": None,
        "is_weighted": False,
        "has_capacity": False
    },
    {
        "name": "Cycle Count",
        "description": "Count the number of cycles in the graph",
        "nodes": 7,
        "graph_types": ["sparse", "dense"],
        "is_connected": None,
        "is_weighted": False,
        "has_capacity": False
    },
    {
        "name": "Spanning Tree Count",
        "description": "Count the number of spanning trees in the graph",
        "nodes": 7,
        "graph_types": ["sparse", "dense"],
        "is_connected": True,
        "is_weighted": False,
        "has_capacity": False
    },
    {
        "name": "Shortest Path",
        "description": "Find the shortest path length between two vertices",
        "nodes": 15,
        "graph_types": ["sparse", "dense"],
        "is_connected": True,
        "is_weighted": True,
        "has_capacity": False
    },
    {
        "name": "Minimum Spanning Tree",
        "description": "Find the total weight of the minimum spanning tree",
        "nodes": 15,
        "graph_types": ["sparse", "dense"],
        "is_connected": True,
        "is_weighted": True,
        "has_capacity": False
    },
    {
        "name": "Second MST",
        "description": "Find the total weight of the second minimum spanning tree",
        "nodes": 12,
        "graph_types": ["sparse", "dense"],
        "is_connected": True,
        "is_weighted": True,
        "has_capacity": False
    },
    {
        "name": "Tree Diameter",
        "description": "Find the diameter of the tree",
        "nodes": 30,
        "graph_types": ["tree"],
        "is_connected": True,
        "is_weighted": False,
        "has_capacity": False
    },
    {
        "name": "Tree Centroid",
        "description": "Find the centroid of the tree with minimum index",
        "nodes": 30,
        "graph_types": ["tree"],
        "is_connected": True,
        "is_weighted": False,
        "has_capacity": False
    },
    {
        "name": "Tree LCA",
        "description": "Find the lowest common ancestor of two nodes (with node 1 as root)",
        "nodes": 30,
        "graph_types": ["tree"],
        "is_connected": True,
        "is_weighted": False,
        "has_capacity": False
    },
    {
        "name": "Tree Max Independent Set",
        "description": "Find the size of the maximum independent set in the tree",
        "nodes": 30,
        "graph_types": ["tree"],
        "is_connected": True,
        "is_weighted": False,
        "has_capacity": False
    },
    {
        "name": "Maximum Flow",
        "description": "Find the maximum flow from source to sink",
        "nodes": 12,
        "graph_types": ["sparse", "dense"],
        "is_connected": True,
        "is_weighted": False,
        "has_capacity": True
    },
    {
        "name": "Minimum Cut",
        "description": "Find the minimum cut capacity from source to sink",
        "nodes": 12,
        "graph_types": ["sparse", "dense"],
        "is_connected": True,
        "is_weighted": False,
        "has_capacity": True
    },
    {
        "name": "Min Cost Max Flow",
        "description": "Find the minimum cost maximum flow from source to sink",
        "nodes": 10,
        "graph_types": ["sparse", "dense"],
        "is_connected": True,
        "is_weighted": True,
        "has_capacity": True
    }
]

class QuestionGenerator:
    def __init__(self):
        self.describer = GraphDescriber()
    
    def generate_random_question(self):
        task = random.choice(TASKS)
        return self.generate_question(task)
    
    def generate_question(self, task):
        # Randomly choose number of vertices as task["nodes"] +/- 1
        base_vertices = task["nodes"]
        variation = random.choice([-1, 0, 1])  # Randomly add -1, 0, or 1
        num_vertices = max(5, base_vertices + variation)  # Ensure at least 5 vertices
        
        # Randomly choose a graph type from available types
        graph_type = random.choice(task["graph_types"])
        
        # Calculate number of edges based on graph type and number of vertices
        if graph_type == "sparse":
            # For sparse graph: edges = nodes/2 to 2*nodes
            min_edges = max(num_vertices - 1, int(num_vertices / 2))  # At least n-1 edges to ensure connectivity
            max_edges = 2 * num_vertices
            num_edges = random.randint(min_edges, max_edges)
        elif graph_type == "dense":
            # For dense graph: edges = node*(node-5)/2 to node*(node-1)/2
            min_edges = max(num_vertices - 1, int(num_vertices * (num_vertices - 5) / 2))  # At least n-1 edges
            max_edges = int(num_vertices * (num_vertices - 1) / 2)  # Complete graph has n*(n-1)/2 edges
            num_edges = random.randint(min_edges, max_edges)
        elif graph_type == "tree":
            num_edges = num_vertices - 1
        else:
            # Default to sparse if type not recognized
            min_edges = max(num_vertices - 1, int(num_vertices / 2))
            max_edges = 2 * num_vertices
            num_edges = random.randint(min_edges, max_edges)
        
        # Use the is_connected value directly, don't randomly decide when None
        is_connected = task["is_connected"]
        
        # For tree type, always set is_connected to True
        if graph_type == "tree":
            is_connected = True
        
        generator = GraphGenerator(
            num_vertices=num_vertices,
            num_edges=num_edges,
            is_connected=is_connected,
            is_weighted=task["is_weighted"],
            has_capacity=task["has_capacity"]
        )
        
        if graph_type == "tree":
            generator.graph_types = ["tree"]
            
        graph_output = generator.generate()
        
        # Select vertices for specific task types
        if task["name"] in ["Connectivity", "Shortest Path", "Tree LCA", 
                           "Maximum Flow", "Minimum Cut", "Min Cost Max Flow"]:
            vertex_a = random.randint(1, num_vertices)
            vertex_b = random.randint(1, num_vertices)
            while vertex_a == vertex_b:
                vertex_b = random.randint(1, num_vertices)
        else:
            vertex_a = vertex_b = None
        
        descriptions = {
            "natural": self.describer.natural_language_description(
                graph_output, 
                has_weights=task["is_weighted"], 
                has_capacity=task["has_capacity"]
            ),
            "structured": self.describer.structured_text_description(
                graph_output, 
                has_weights=task["is_weighted"], 
                has_capacity=task["has_capacity"]
            ),
            "matrix": self.describer.adjacency_matrix_description(
                graph_output, 
                has_weights=task["is_weighted"], 
                has_capacity=task["has_capacity"]
            ),
            "list": self.describer.adjacency_list_description(
                graph_output, 
                has_weights=task["is_weighted"], 
                has_capacity=task["has_capacity"]
            )
        }
        
        question_text = self._format_question(task, vertex_a, vertex_b)
        
        # Calculate the answer using the appropriate algorithm
        answer = self._calculate_answer(task["name"], graph_output, vertex_a, vertex_b)
        
        return {
            "task_name": task["name"],
            "task_description": task["description"],
            "question_text": question_text,
            "graph_output": graph_output,
            "descriptions": descriptions,
            "vertices": [vertex_a, vertex_b],
            "answer": answer
        }
    
    def _calculate_answer(self, task_name, graph, vertex_a, vertex_b):
        """
        Calculate the answer for a given task using the appropriate algorithm.
        
        Args:
            task_name: The name of the task
            graph: The graph representation (string format)
            vertex_a: First vertex (for connectivity or shortest path tasks)
            vertex_b: Second vertex (for connectivity or shortest path tasks)
            
        Returns:
            The answer to the question
        """
        has_weight = task_name in ["Shortest Path", "Minimum Spanning Tree", "Second MST", "Min Cost Max Flow"]
        has_capacity = task_name in ["Maximum Flow", "Minimum Cut", "Min Cost Max Flow"]
        
        # Parse the graph string to adjacency list format with appropriate flags
        adjacency_list = parse_graph_string(graph, has_weight=has_weight, has_capacity=has_capacity)
        
        if task_name == "Connectivity":
            return check_connectivity(adjacency_list, vertex_a, vertex_b)
        
        elif task_name == "Bipartite":
            return check_bipartite(adjacency_list)
        
        elif task_name == "Cycle Count":
            return count_cycles(adjacency_list)
        
        elif task_name == "Triangle Count":
            return count_triangles(adjacency_list)
        
        elif task_name == "Minimum Cycle":
            return find_minimum_cycle(adjacency_list)
        
        elif task_name == "Maximum Clique":
            return find_max_clique_size(adjacency_list)
        
        elif task_name == "Maximum Independent Set":
            return find_max_independent_set_size(adjacency_list)
        
        elif task_name == "Bridge Count":
            return count_bridges(adjacency_list)
        
        elif task_name == "Biconnected Components":
            return count_biconnected_components(adjacency_list)
        
        elif task_name == "Eulerian Path":
            return has_eulerian_path(adjacency_list)
        
        elif task_name == "Eulerian Circuit":
            return has_eulerian_circuit(adjacency_list)
        
        elif task_name == "Hamiltonian Path":
            return has_hamiltonian_path(adjacency_list)
        
        elif task_name == "Hamiltonian Circuit":
            return has_hamiltonian_circuit(adjacency_list)
        
        elif task_name == "Spanning Tree Count":
            return count_spanning_trees(adjacency_list)
        
        elif task_name == "Shortest Path":
            return find_shortest_path_length(adjacency_list, vertex_a, vertex_b)
        
        elif task_name == "Minimum Spanning Tree":
            return find_mst_weight(adjacency_list)
        
        elif task_name == "Second MST":
            return find_second_mst_weight(adjacency_list)
        
        elif task_name == "Tree Diameter":
            return find_tree_diameter(adjacency_list)
        
        elif task_name == "Tree Centroid":
            return find_tree_centroid(adjacency_list)
        
        elif task_name == "Tree LCA":
            return find_tree_lca(adjacency_list, vertex_a, vertex_b)
        
        elif task_name == "Tree Max Independent Set":
            return find_tree_max_independent_set(adjacency_list)
        
        elif task_name == "Maximum Flow":
            return find_maximum_flow(adjacency_list, vertex_a, vertex_b)
        
        elif task_name == "Minimum Cut":
            return find_minimum_cut(adjacency_list, vertex_a, vertex_b)
        
        elif task_name == "Min Cost Max Flow":
            _, min_cost = find_min_cost_max_flow(adjacency_list, vertex_a, vertex_b)
            return min_cost
        
        return None
    
    def _format_question(self, task, vertex_a, vertex_b):
        if task["name"] == "Connectivity":
            return f"Given the graph, determine if vertex {vertex_a} and vertex {vertex_b} are connected."
        
        elif task["name"] == "Bipartite":
            return "Determine if the given graph is bipartite (can be divided into two sets where no two vertices within the same set are adjacent)."
        
        elif task["name"] == "Cycle Count":
            return "Count the total number of simple cycles in the given graph."
        
        elif task["name"] == "Triangle Count":
            return "Count the number of triangles (cycles of length 3) in the given graph."
        
        elif task["name"] == "Minimum Cycle":
            return "Find the length of the smallest cycle in the given graph."
        
        elif task["name"] == "Maximum Clique":
            return "Find the size of the maximum clique in the given graph. A clique is a subset of vertices such that every two distinct vertices are adjacent."
        
        elif task["name"] == "Maximum Independent Set":
            return "Find the size of the maximum independent set in the given graph. An independent set is a set of vertices such that no two vertices are adjacent."
        
        elif task["name"] == "Bridge Count":
            return "Count the number of bridges (cut edges) in the given graph. A bridge is an edge whose removal increases the number of connected components."
        
        elif task["name"] == "Biconnected Components":
            return "Count the number of biconnected components in the given graph. A biconnected component is a maximal biconnected subgraph."
        
        elif task["name"] == "Eulerian Path":
            return "Determine if the graph has an Eulerian path. An Eulerian path is a path that visits every edge exactly once."
        
        elif task["name"] == "Eulerian Circuit":
            return "Determine if the graph has an Eulerian circuit. An Eulerian circuit is a cycle that visits every edge exactly once."
        
        elif task["name"] == "Hamiltonian Path":
            return "Determine if the graph has a Hamiltonian path. A Hamiltonian path is a path that visits each vertex exactly once."
        
        elif task["name"] == "Hamiltonian Circuit":
            return "Determine if the graph has a Hamiltonian circuit. A Hamiltonian circuit is a cycle that visits each vertex exactly once and returns to the starting vertex."
        
        elif task["name"] == "Spanning Tree Count":
            return "Count the number of spanning trees in the given graph. A spanning tree is a tree that includes all vertices of the graph."
        
        elif task["name"] == "Shortest Path":
            return f"Find the shortest path length from vertex {vertex_a} to vertex {vertex_b} in the weighted graph."
        
        elif task["name"] == "Minimum Spanning Tree":
            return "Find the total weight of the minimum spanning tree (MST) in the weighted graph."
        
        elif task["name"] == "Second MST":
            return "Find the total weight of the strict second minimum spanning tree in the weighted graph. The strict second minimum spanning tree is the spanning tree with minimum total weight among all spanning trees whose weight is strictly greater than the minimum spanning tree weight."
        
        elif task["name"] == "Tree Diameter":
            return "Find the diameter of the given tree. The diameter is the length of the longest path between any two nodes in the tree."
        
        elif task["name"] == "Tree Centroid":
            return "Find the centroid of the given tree with the minimum index. A centroid is a node whose removal results in subtrees of size at most n/2."
        
        elif task["name"] == "Tree LCA":
            return f"Find the lowest common ancestor (LCA) of nodes {vertex_a} and {vertex_b} in the given tree, with node 1 as the root."
        
        elif task["name"] == "Tree Max Independent Set":
            return "Find the size of the maximum independent set in the given tree. An independent set is a set of vertices such that no two vertices are adjacent."
        
        elif task["name"] == "Maximum Flow":
            return f"Calculate the maximum flow from vertex {vertex_a} (source) to vertex {vertex_b} (sink) in the given undirected network. In this undirected network, flow can travel in both directions along each edge."
        
        elif task["name"] == "Minimum Cut":
            return f"Calculate the minimum cut capacity from vertex {vertex_a} (source) to vertex {vertex_b} (sink) in the given undirected network. In this undirected network, flow can travel in both directions along each edge."
        
        elif task["name"] == "Min Cost Max Flow":
            return f"Calculate the minimum cost maximum flow from vertex {vertex_a} (source) to vertex {vertex_b} (sink) in the given undirected network. Each edge has both a capacity constraint and a cost per unit flow, and flow can travel in both directions along each edge. Return the cost of sending the maximum possible flow."
        
        return "Analyze the given graph."
    
    def generate_question_sets(self, questions_per_task=5):
        """
        Generate question sets for each task and graph type combination.
        
        Args:
            questions_per_task: Number of questions to generate for each task and graph type combination
            
        Returns:
            dict: Dictionary of question sets organized by description type
        """
        question_sets = {
            "natural": [],
            "structured": [],
            "matrix": [],
            "list": []
        }
        
        for task in TASKS:
            # For each task, generate questions for each graph type
            for graph_type in task["graph_types"]:
                for _ in range(questions_per_task):
                    # Create a copy of the task to modify for this specific graph type
                    task_copy = task.copy()
                    task_copy["graph_types"] = [graph_type]  # Force this graph type for this question
                    
                    # Generate the question with the specified graph type
                    question = self.generate_question(task_copy)
                    
                    # Create separate entries for each description type
                    for desc_type in question_sets.keys():
                        instruction = "Please provide the reasoning process and the final answer directly to the question.\n\n"
                        # Combine instruction, question_text and description into prompt
                        prompt = instruction + question["question_text"] + "\n\n" + question["descriptions"][desc_type]
                        
                        # Create a copy of the question with combined prompt
                        question_copy = {
                            "task_name": question["task_name"],
                            "task_description": question["task_description"],
                            "graph_type": graph_type,  # Add graph type to the output
                            "prompt": prompt,
                            "graph_output": question["graph_output"],
                            "vertices": question["vertices"],
                            "answer": question["answer"]
                        }
                        question_sets[desc_type].append(question_copy)
        
        return question_sets
    
    def save_question_sets_to_json(self, questions_per_task=23):
        """Generate and save question sets to JSON files"""
        # Create data directory if it doesn't exist
        data_dir = "data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        question_sets = self.generate_question_sets(questions_per_task)
        
        # Save each question set to a JSON file in the data folder
        for desc_type, questions in question_sets.items():
            filename = os.path.join(data_dir, f"{desc_type}.json")
            with open(filename, 'w') as f:
                json.dump(questions, f, indent=2)
            
            # Count questions by task and graph type
            task_counts = {}
            for q in questions:
                task = q["task_name"]
                graph_type = q["graph_type"]
                key = f"{task} ({graph_type})"
                task_counts[key] = task_counts.get(key, 0) + 1
            
            # Print summary
            print(f"Saved {len(questions)} questions to {filename}")
            for task, count in task_counts.items():
                print(f"  {task}: {count} questions")
        
        # Create and save a shuffled dataset with all questions
        self.save_shuffled_dataset(question_sets)
    
    def save_shuffled_dataset(self, question_sets):
        """
        Create and save a dataset with all questions shuffled in random order
        
        Args:
            question_sets: Dictionary containing all question sets
        """
        # Collect all questions from all description types
        all_questions = []
        for desc_type, questions in question_sets.items():
            # Add description type as a field to each question
            for q in questions:
                q_copy = q.copy()
                q_copy["description_type"] = desc_type
                all_questions.append(q_copy)
        
        # Shuffle all questions
        random.shuffle(all_questions)
        
        # Save to file
        filename = os.path.join("data", "all.json")
        with open(filename, 'w') as f:
            json.dump(all_questions, f, indent=2)
        
        print(f"Saved {len(all_questions)} shuffled questions to {filename}")

if __name__ == "__main__":
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Generate graph theory problem sets')
    parser.add_argument('--questions', '-q', type=int, default=10,
                        help='Number of questions to generate for each task and graph type combination')
    args = parser.parse_args()
    
    # Use the passed parameter instead of hardcoded number
    question_gen = QuestionGenerator()
    question_gen.save_question_sets_to_json(args.questions)