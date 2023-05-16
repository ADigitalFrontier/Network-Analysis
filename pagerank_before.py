import pandas as pd
import networkx as nx

# Load the list of nodes from graphan.csv
df = pd.read_csv('graphan.csv')

# for each row in the dataframe, get the SourceName value and the Source value
nodes = {}
for i in range(len(df)):
    nodes[df['Source'][i]] = df['SourceName'][i]

# Load the CSV file into a DataFrame
df = pd.read_csv('PRbefore.csv')

# Create a graph from the DataFrame
G = nx.from_pandas_edgelist(df, source='Source', target='Target', create_using=nx.Graph())

# Calculate PageRank
pagerank = nx.pagerank(G)

# Convert the PageRank dictionary to a DataFrame
pagerank_df = pd.DataFrame.from_dict(pagerank, orient='index', columns=['PageRank'])


# Convert the source column based on the nodes dictionary
pagerank_df['Source'] = pagerank_df.index
pagerank_df['SourceName'] = pagerank_df['Source'].map(nodes)

# Display the DataFrame
print(pagerank_df)