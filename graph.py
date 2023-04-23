import plotly.graph_objs as go
import plotly.offline as pyo
import networkx as nx
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('drugData.db')

# Execute SQL query to retrieve drug interaction data
cur = conn.cursor()
cur.execute('SELECT D_Name_1, D_Name_2, I_Description FROM Interacts WHERE D_Name_1 = ? LIMIT 10', ("Ibuprofen",))

# Fetch the results and create a list of edges
interactions = cur.fetchall()

# Create the graph
G = nx.Graph()
for interaction in interactions:
    D_Name_1, D_Name_2, description = interaction
    G.add_edge(D_Name_1, D_Name_2, description=description)

# Close the database connection
conn.close()

# Define node positions for the graph layout
pos = nx.spring_layout(G)

# Create a list of edge trace objects with descriptions
edge_trace = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    trace = go.Scatter(x=[x0, x1, None], y=[y0, y1, None],
                       mode='lines',
                       line=dict(width=10),
                       hoverinfo='text', # set hoverinfo to "text"
                       hovertext=G[edge[0]][edge[1]]['description']) # set hovertext to description
    edge_trace.append(trace)

# Create a list of node trace objects
node_trace = go.Scatter(x=[], y=[], text=[], mode='markers', hoverinfo='text',
                        marker=dict(color='black', size=10, line=dict(width=2)))

# Add node positions and labels to the node trace
for node in G.nodes():
    x, y = pos[node]
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])
    node_trace['text'] += tuple([node])

# Create the figure object
fig = go.Figure(data=edge_trace + [node_trace],
                layout=go.Layout(
                    title='<br>Drug Interaction Graph',
                    titlefont_size=16,
                    showlegend=True,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

# Display the figure
pyo.plot(fig, filename='drug_interaction_graph.html')
