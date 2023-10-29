import networkx as nx
import matplotlib.pyplot as plt
import time

# Function to perform Maximum Degree Heuristic
def maximum_degree_matching(graph):
    matching_graph = graph.copy()
    matching = []

    while matching_graph:
        max_degree_node = max(matching_graph, key=matching_graph.degree)
        neighbors = list(matching_graph.neighbors(max_degree_node))
        if neighbors:
            neighbor = neighbors[0]
            matching.append((max_degree_node, neighbor))
            matching_graph.remove_node(max_degree_node)
            matching_graph.remove_node(neighbor)
        else:
            break
    return matching

# Function to perform Maximum Weight Heuristic
def maximum_weight_matching(graph):
    matching_graph = graph.copy()
    matching = []

    edges = sorted(graph.edges(data=True), key=lambda x: -x[2].get('weight', 1))

    for edge in edges:
        u, v, data = edge
        if matching_graph.has_edge(u, v):
            matching.append((u, v))
            matching_graph.remove_node(u)
            matching_graph.remove_node(v)
    return matching

def get_matching_and_time(iterations, matching_func):
    matching_times = []
    mean_matching_size = []
    mean_matching_sizes = []

    for _ in range(iterations):
        graph = nx.generators.random_graphs.erdos_renyi_graph(120, 0.04)

        start_time = time.time()
        matching = matching_func(graph.copy())
        end_time = time.time()
        matching_times.append(end_time - start_time)

        mean_matching_size.append(len(matching))
        mean_matching_sizes.append(sum(mean_matching_size)/len(mean_matching_size))

    return matching_times, mean_matching_sizes

def compare_algorithms(iterations=100):

    degree_times, degree_mean_sizes = get_matching_and_time(iterations, maximum_degree_matching)
    weight_times, weight_mean_sizes = get_matching_and_time(iterations, maximum_weight_matching)

    x = range(1, len(degree_mean_sizes) + 1)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, degree_mean_sizes, label='Degree', color='blue')
    ax.plot(x, weight_mean_sizes, label='Weight', color='red')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Average Matching Size')
    ax.legend()
    plt.title('Comparison of Degree and Weight Solutions for Matching')
    plt.show()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(['Degree', 'Weight'], [sum(degree_times) / iterations, sum(weight_times) / iterations], color=['blue', 'red'])
    ax.set_xlabel('Algorithm')
    ax.set_ylabel('Processing Time')
    plt.title('Processing Time for Matching')
    plt.show()

    print(f'Average Degree Matching size for 1 iteration: {degree_mean_sizes[-1]}')
    print(f'Average Weight Matching size for 1 iteration: {weight_mean_sizes[-1]}', end='\n\n')

    print(f'Average Degree Processing Time for 1 iteration: {sum(degree_times) / iterations}')
    print(f'Average Weight Processing Time for 1 iteration: {sum(weight_times) / iterations}')

compare_algorithms(1000)