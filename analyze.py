import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def extract_hashmap(data):
    hashmap = {}
    for line in data.strip().split('\n'):
        parts = line.split('\t')
        number = int(parts[0])
        name = parts[1].strip('"')
        hashmap[number] = name
    return hashmap

# open text file
with open('network.txt', 'r') as f:
    data = f.read()

hashmap = extract_hashmap(data)

# Open the CSV and create a DataFrame
file_path = 'graph.csv'  # Replace with the path to your CSV file
df = pd.read_csv(file_path)
# display the dataframe
# Create a SourceName and TargetName column
df['SourceName'] = df['Source'].map(hashmap)
df['TargetName'] = df['Target'].map(hashmap)
# display the dataframe
# Save the DataFrame as a CSV file
df.to_csv('graphan.csv', index=False)

# Read the CSV file
file_path = 'graphan.csv'  # Replace with the path to your CSV file
df = pd.read_csv(file_path)

# Create a graph from the DataFrame
G = nx.from_pandas_edgelist(df, 'Source', 'Target')  # Replace 'Source' and 'Target' with your column names for source and target nodes

# Draw the graph
pos = nx.spring_layout(G)

# Create a dictionary that maps node names to their corresponding labels
labels = {node: hashmap[node] for node in G.nodes}

# Draw the graph with labels
nx.draw(G, pos, labels=labels, with_labels=True, node_size=600, font_size=10)
plt.show()

# outlaw nodes of interest:
# 0: pablo escobar, 7: la quica, 5: jorge ochoa, 6: fabio ochoa, 8: poison, 29: blackie, 41: limon
# law nodes of interest:
# 1: stephen murphy, 2: javier pena, 13: cesar gaviria, 4: colonel carrillo, 43: ambdassador crosby, 53: colonel martinez
# bridge nodes of interest:
# alberto suarez: 35, fernando duque: 12, ivan torres: 62

# create a list of the outlaws
outlaws = [0, 7, 5, 6, 8, 29, 41]

# create a list of the law
law = [1, 2, 13, 4, 43, 53]

# create a list of the bridge nodes
bridge = [35, 12, 62]

# for each bridge, calculate the average shortest path to the outlaws and the law with and without the bridge
# copy the graph
for node in bridge:
    total_distance_before = 0
    total_distance_after = 0
    for outlaw in outlaws:
        for law_node in law:
            graph = G.copy()
            # find the shortest path between the outlaw and the law
            shortest_path = nx.shortest_path_length(graph, source=outlaw, target=law_node)
            total_distance_before += shortest_path
            # remove the bridge node
            graph.remove_node(node)
            # find the shortest path between the outlaw and the law
            shortest_path_no_bridge = nx.shortest_path_length(graph, source=outlaw, target=law_node)
            total_distance_after += shortest_path_no_bridge
    # calculate the average shortest path between the outlaws and the law
    average_distance_before = total_distance_before / (len(outlaws) * len(law))
    average_distance_after = total_distance_after / (len(outlaws) * len(law))
    # print the before and after average shortest path
    print(f'Average shortest path between outlaws and law after removing {hashmap[node]}: {average_distance_after}')
    print(f'Average shortest path between outlaws and law before removing {hashmap[node]}: {average_distance_before}')
