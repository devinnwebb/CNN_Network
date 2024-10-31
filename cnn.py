# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
import re

# Step 1: Scraping Internal Links from CNN
def get_internal_links(url, base_url="https://www.cnn.com"):
    """Fetch internal CNN links from a given URL."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            # Filter for CNN internal links only
            if href.startswith("/") and not re.search(r"^(/videos|/live|/interactive)", href):
                full_link = base_url + href
                links.append(full_link)
        return links
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

# Define the main CNN page and section URLs to analyze
start_urls = [
    'https://www.cnn.com', 
    'https://www.cnn.com/politics', 
    'https://www.cnn.com/world', 
    'https://www.cnn.com/health'
]
edges = []

# Gather links for each starting section
for url in start_urls:
    links = get_internal_links(url)
    for link in links:
        edges.append((url, link))  # Forming edges as (source, target)

# Step 2: Create the Graph
G = nx.DiGraph()  # Directed graph for CNN's internal link structure
G.add_edges_from(edges)

# Step 3: Calculate Centrality Measures
# Degree Centrality
degree_centrality = nx.degree_centrality(G)

# PageRank
pagerank = nx.pagerank(G)

# Betweenness Centrality
betweenness_centrality = nx.betweenness_centrality(G)

# Step 4: Identify Important Nodes
top_degree_nodes = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:3]
top_pagerank_nodes = sorted(pagerank, key=pagerank.get, reverse=True)[:3]
top_betweenness_nodes = sorted(betweenness_centrality, key=betweenness_centrality.get, reverse=True)[:3]

print("Top 3 articles by Degree Centrality:", top_degree_nodes)
print("Top 3 articles by PageRank:", top_pagerank_nodes)
print("Top 3 articles by Betweenness Centrality:", top_betweenness_nodes)

# Combine all top nodes into one set to avoid duplicates
highlighted_nodes = set(top_degree_nodes + top_pagerank_nodes + top_betweenness_nodes)

# Step 5: Visualize the Graph with Highlighted Nodes
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G)  # Define layout

# Draw all nodes in the network
nx.draw_networkx_nodes(G, pos, node_size=20, node_color="blue", alpha=0.5)

# Highlight top nodes with larger size and different color
nx.draw_networkx_nodes(G, pos, nodelist=highlighted_nodes, node_size=100, node_color="red", alpha=0.9)

# Draw edges
nx.draw_networkx_edges(G, pos, edge_color="gray", alpha=0.5, arrows=True)

# Add labels only for the highlighted nodes
nx.draw_networkx_labels(G, pos, labels={node: node for node in highlighted_nodes}, font_size=8, font_color="black")

plt.title("Highlighted Important Nodes in CNN's Internal Link Structure")
plt.show()

# Step 6: Data Cleaning (Duplicate and Self-loop Removal)
# Remove self-loops (links from a page to itself) and duplicates
G.remove_edges_from(nx.selfloop_edges(G))
edges = list(set(edges))  # Ensure edges are unique
