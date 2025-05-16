def parse_graph_string(graph_string, has_weight=False, has_capacity=False):
    """
    Parse a graph from string format to adjacency list.
    
    The input format is expected to be:
    "n m
    u1 v1 [weight1] [capacity1]
    u2 v2 [weight2] [capacity2]
    ...
    um vm [weightm] [capacitym]"
    
    Where:
    - n is the number of vertices
    - m is the number of edges
    - each subsequent line contains an edge (u, v) with optional weight and capacity
    
    Args:
        graph_string: String representation of the graph
        has_weight: Whether the graph has weight information
        has_capacity: Whether the graph has capacity information
        
    Returns:
        dict: Adjacency list representation of the graph
    """
    lines = graph_string.strip().split('\n')
    
    # Extract n and m from the first line
    n, m = map(int, lines[0].split())
    
    # Initialize adjacency list
    adjacency_list = {i: [] for i in range(1, n+1)}
    
    # Parse edges
    for i in range(1, m+1):
        if i < len(lines):
            parts = list(map(int, lines[i].split()))
            u, v = parts[0], parts[1]
            
            # 处理不同情况：无权无容量、带权无容量、无权带容量、带权带容量
            if len(parts) == 2:  # 无权无容量
                adjacency_list[u].append(v)
                adjacency_list[v].append(u)
            elif len(parts) >= 3:
                if has_weight and has_capacity and len(parts) >= 4:
                    # 带权带容量的情况
                    weight = parts[2]
                    capacity = parts[3]
                    adjacency_list[u].append((v, capacity, weight))  # 注意：这里交换了capacity和weight的顺序
                    adjacency_list[v].append((u, capacity, weight))  # 让capacity在前，符合最大流算法的期望
                elif has_capacity and not has_weight:
                    # 无权带容量的情况
                    capacity = parts[2]
                    adjacency_list[u].append((v, capacity))
                    adjacency_list[v].append((u, capacity))
                elif has_weight and not has_capacity:
                    # 带权无容量的情况
                    weight = parts[2]
                    adjacency_list[u].append((v, weight))
                    adjacency_list[v].append((u, weight))
                else:
                    # 默认情况，使用第一个额外参数
                    value = parts[2]
                    adjacency_list[u].append((v, value))
                    adjacency_list[v].append((u, value))
    
    return adjacency_list 