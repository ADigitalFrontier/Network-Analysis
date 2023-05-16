import pandas as pd
import networkx as nx

# Load the list of nodes from graphan.csv
df_nodes = pd.read_csv('graphan.csv')

# for each row in the dataframe, get the SourceName value and the Source value
nodes = {}
for i in range(len(df_nodes)):
    nodes[df_nodes['Source'][i]] = df_nodes['SourceName'][i]

# Load the CSV file into a DataFrame
df_edges = pd.read_csv('PRafter.csv')

# Initialize a MultiDiGraph
G = nx.MultiDiGraph()

# Add edges to the graph
for i in range(len(df_edges)):
    source = df_edges.loc[i, 'Source']
    target = df_edges.loc[i, 'Target']
    edge_type = df_edges.loc[i, 'Type']

    if edge_type == 'Directed':
        G.add_edge(source, target)
    else:  # Undirected
        G.add_edge(source, target)
        G.add_edge(target, source)

# Calculate PageRank
pagerank = nx.pagerank(G)

# Convert the PageRank dictionary to a DataFrame
pagerank_df = pd.DataFrame.from_dict(pagerank, orient='index', columns=['PageRank'])

# Convert the source column based on the nodes dictionary
pagerank_df['Source'] = pagerank_df.index
pagerank_df['SourceName'] = pagerank_df['Source'].map(nodes)

# Display the DataFrame
print(pagerank_df)