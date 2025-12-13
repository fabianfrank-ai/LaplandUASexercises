"""
Creates a networking graph with clustering via plotly, so everything is interactable.
Further explanation can be found in the notebook

# here is some documentation I needed, since I never used plotly before
https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html
https://plotly.com/python/

"""
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import numpy as np
import urllib.request

# suggestion by ChatGPT in a brainstorming session, explained it in the corresponding notebook
from networkx.algorithms import community as nx_comm
from scipy.spatial import ConvexHull
import plotly.io as pio


class network_graph:
    """
    Visualize stock correlations as a network graph using Plotly.

    Nodes represent tickers, edges represent correlations above a specified threshold.
    Node colors indicate connectivity, and hover text provides company info and average correlations.

    Parameters
    ----------
    correlations : pd.DataFrame
        Square DataFrame of pairwise ticker correlations (Pearson coefficients).
    threshold : float
        Minimum absolute correlation to create an edge between two nodes.

    Attributes
    ----------
    fig : go.Figure
        Plotly figure for the network graph.
    G : nx.Graph
        NetworkX graph object created from correlations.
    pos : dict
        Dictionary mapping nodes to their 2D positions for plotting.
    company_info : dict
        Dictionary mapping tickers to company name and sector.

    Methods
    -------
    get_company_info()
        Fetch company names and sectors from Wikipedia for hover info.
    create_network()
        Build a NetworkX graph using nodes and edges filtered by threshold.
    plot_network()
        Generate the Plotly network visualization.
    clustering()
        Identify clusters of connected nodes and optionally draw convex hulls around them.
    """

    def __init__(self, correlations: pd.DataFrame, threshold: float):
        # store the input correlation matrix and threshold for edge vreation
        self.correlations = correlations
        self.threshold = threshold

        # initialize the plotly figure
        self.fig = go.Figure()

        # automatically generate and plot the network
        self.plot_network()

    def get_company_info(self):
        """
        Fetch S&P 500 company names and sectors from Wikipedia.

        Creates a dictionary `self.company_info` mapping ticker symbols to
        {'name': company name, 'sector': sector}.  
        Necessary for informative hover text in the network graph.
        """

        # fetch the wikipedia page
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        req = urllib.request.Request(
            url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read()
        tables = pd.read_html(html)

        # Look through all tables to find the one containing company info
        for table in tables:
            try:
                company_names = table['Security'].tolist()
                company_sector = table['GICS Sector'].tolist()
                sp500_tickers = table['Symbol'].tolist()
            except Exception:
                pass

        # wikipedia uses dots in some ticker symbols, but yfinance needs dashes (e.g. BF.B -> BF-B)
        sp500_tickers = [t.replace(".", "-") for t in sp500_tickers]

        # create a dictionary mapping tickers to names and sectors
        self.company_info = {}
        for i, ticker in enumerate(sp500_tickers):
            # map ticker to name and sector
            self.company_info[ticker] = {
                'name': company_names[i],
                'sector': company_sector[i]
            }

    def create_network(self):
        """
        Build a NetworkX graph from the correlation matrix.

        Nodes are tickers, edges exist if abs(correlation) >= threshold.
        Edge weights correspond to correlation coefficients.
        """

        self.G = nx.Graph()

        nodes = self.correlations.index.to_list()

        # get tickers as nodes
        self.G.add_nodes_from(nodes)

        # Add edges for all pairs with correlation above the threshold
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                corr_value = self.correlations.iloc[i, j]
                if abs(corr_value) >= self.threshold:
                    self.G.add_edge(nodes[i], nodes[j], weight=corr_value)

    # threshold is chosen for best performance and visibility

    def plot_network(self):
        """
        Plot the correlation network using Plotly.

        - Nodes are sized and colored by number of connections.
        - Edges are colored green for positive correlations, red for negative.
        - Clusters are optionally highlighted with convex hulls.
        """

        self.create_network()

        # set the default template to dark
        pio.templates.default = "plotly_dark"

        # Generate 2D positions for nodes using spring layout
        # k=6 spreads nodes apart; seed ensures reproducibility
        self.pos = nx.spring_layout(self.G, seed=42, k=6, method="energy")

        # Lists to store edge coordinates and colors for Plotly
        edge_x = []
        edge_y = []
        edge_info = []
        edge_colors = []

        # append the lists with data from the edges
        for edge in self.G.edges():
            # Get positions of the two nodes connected by the edge
            x0, y0 = self.pos[edge[0]]
            x1, y1 = self.pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

            weight = self.G[edge[0]][edge[1]]['weight']
            edge_info.append(f'{edge[0]} - {edge[1]}: {weight:.3f}')

            # Color edges based on correlation sign ( isnt used yet)
            if weight > 0:
                edge_colors.extend(['green', 'green', None])
            else:
                edge_colors.extend(['red', 'red', None])

        # Prepare node coordinates, hover text, and colors
        node_x = []
        node_y = []
        node_text = []
        node_colors = []

        # fetch company info
        self.get_company_info()

        # aoppend with data from teh nodes
        for node in self.G.nodes():
            x, y = self.pos[node]
            node_x.append(x)
            node_y.append(y)

            # Compute adjacency information for hover text
            adjacencies = list(self.G.neighbors(node))
            node_info = f'{node}<br> Company: {self.company_info.get(node, {}).get("name", "N/A")} <br> Sector: {self.company_info.get(node, {}).get("sector", "N/A")} <br> Connections: {len(adjacencies)}'
            if len(adjacencies) > 0:
                correlations = [self.G[node][adj]['weight']
                                for adj in adjacencies]
                avg_corr = np.nanmean(correlations) if len(
                    correlations) else 0.0
                node_info += f'<br>Avg Correlation: {avg_corr:.3f}'

            node_text.append(node_info)

            # change colours based on amount of adjacencies(not yet implemented)
            node_colors.append(len(adjacencies))

        # Identify clusters and optionally draw convex hulls
        self.clustering()

        # Add edges to Plotly figure
        self.fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#8888aa'),
            hoverinfo='none',
            mode='lines',
            name='Connections'))

        # add nodes with data
        self.fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=list(self.G.nodes()),
            hovertext=node_text,
            textposition="middle center",
            marker=dict(
                showscale=True,
                colorscale='jet',
                color=node_colors,
                size=20,
                colorbar=dict(
                    thickness=15,
                    len=0.5,
                    x=1.1,
                    title="Connections"),
            ),
            name='Stocks'))

        # created with the help of claude since I usually never use plotly, also very tiring/boring to do all of it by myself
        # Layout settings for dark theme and cleaner look
        self.fig.update_layout(
            title=dict(
                text=f'Stock Correlation Network (threshold: {self.threshold})',
                font=dict(size=16)),
            autosize=True,
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            annotations=[dict(
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002,
                xanchor='left', yanchor='bottom',
                font=dict(color='gray', size=10))],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='black',
            paper_bgcolor='black',
            font_color='white',
            hoverlabel=dict(
                bgcolor="white",
                font_color="black"))

    def clustering(self):
        """
        Identify clusters of connected nodes using greedy modularity and draw convex hulls.

        Clusters with at least 3 nodes are highlighted with semi-transparent shapes.
        """

        # remove non-existing nodes and partition the existing ones (otherwise nx will literally scream at you in agony)
        # replaced louvain with greedy modularity because louvain failed consistently
        # https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.modularity_max.greedy_modularity_communities.html
        G_clean = self.G.copy()
        G_clean.remove_nodes_from(list(nx.isolates(G_clean)))

        # Detect communities with greedy modularity
        communities = nx_comm.greedy_modularity_communities(G_clean)

        # map each node to its cluster ID
        partition = {node: cid for cid, comm in enumerate(
            communities) for node in comm}

        # Group the clusters
        clusters = {}
        for node, cid in partition.items():
            clusters.setdefault(cid, []).append(node)

        # Create a convec hull and a shape
        for cid, nodes in clusters.items():
            if len(nodes) >= 3:

                points = np.array([self.pos[node] for node in nodes])
                hull = ConvexHull(points)
                hull_points = points[hull.vertices]

                x_hull = list(hull_points[:, 0]) + [hull_points[0, 0]]
                y_hull = list(hull_points[:, 1]) + [hull_points[0, 1]]

                # color code the clusters
                color = f"rgba({(cid*53) % 256}, {(cid*97) % 256}, {(cid*137) % 256}, 0.2)"

                # add clusters as shape
                self.fig.add_shape(
                    type="path",
                    path="M " + " L ".join(f"{x},{y}" for x,
                                           y in zip(x_hull, y_hull)) + " Z",
                    fillcolor=color,
                    line=dict(color="rgba(100, 100, 255, 0.2)"),
                    layer="below")

            else:
                continue
