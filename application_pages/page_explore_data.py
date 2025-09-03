import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt # For drawing the graph
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def create_geo_map_visualization(transactions):
    """Generates a geographic map visualization of transaction origins and destinations.

    Args:
        transactions (Pandas DataFrame): DataFrame with transaction data, including
                                      'origin_latitude', 'origin_longitude',
                                      'destination_latitude', 'destination_longitude', and 'transaction_amount' columns.

    Returns:
        A Plotly figure object.
    """

    if transactions.empty:
        print("Transactions DataFrame is empty. Cannot create geo map.")
        return go.Figure()

    required_columns = ['origin_latitude', 'origin_longitude', 'destination_latitude', 'destination_longitude', 'transaction_amount']
    for col in required_columns:
        if col not in transactions.columns:
            raise KeyError(f"Column '{col}' missing in DataFrame. Please ensure synthetic data includes these or add dummy values.")

    # Check if lat/lon columns are numeric
    for col in ['origin_latitude', 'origin_longitude', 'destination_latitude', 'destination_longitude']:
        if not pd.api.types.is_numeric_dtype(transactions[col]):
            raise TypeError(f"Column '{col}' must contain numeric data.")

    # Normalize transaction amounts to [0, 1]
    norm_transaction_amount = (transactions['transaction_amount'] - transactions['transaction_amount'].min()) / (transactions['transaction_amount'].max() - transactions['transaction_amount'].min())

    fig = go.Figure(data=go.Scattergeo(
        lon=transactions['origin_longitude'],
        lat=transactions['origin_latitude'],
        mode='markers',
        marker=dict(
            size=transactions['transaction_amount'] / transactions['transaction_amount'].max() * 20,  # Scale marker size by amount
            opacity=0.8,
            color=norm_transaction_amount,
            colorscale='Blues',
            reversescale=True,
            symbol='circle',
            line=dict(
                width=0,
                color='rgba(102, 102, 102)'
            ),
            sizemode='area',
        ),
        text=[f"Amount: {amount:,.2f}" for amount in transactions['transaction_amount']],
    ))

    fig.update_layout(
        title_text='Transaction Origins (Marker Color ~ Amount)',
        geo=dict(
            scope='world',
            showland=True,
            landcolor="rgb(217, 217, 217)",
        )
    )

    return fig



def create_counterparty_network_graph(transactions):
    """Creates a network graph of transaction counterparties.

    Args:
        transactions (Pandas DataFrame): DataFrame with transaction data,
                                      expected to have 'Source' and 'Target' columns.

    Returns:
        networkx.Graph: A NetworkX graph object.
    """
    
    st.write("Creating a counterparty network graph only for the first 100 transactions")
    graph = nx.Graph()
    if transactions.empty:
        return graph

    required_columns = ['Source', 'Target']
    for col in required_columns:
        if col not in transactions.columns:
            raise KeyError(f"Column '{{col}}' missing in DataFrame. Please ensure synthetic data includes these or add dummy values.")

    # Add edges to the graph
    for index, row in transactions[:100].iterrows():
        source = row['Source']
        target = row['Target']
        if source != target: # Avoid self-loops for clearer visualization
            graph.add_edge(source, target)
    return graph


def run_page():
    st.markdown("# Explore Data")
    
    if 'data' not in st.session_state:
        st.error("Please load synthetic data first. Go to the **Case Intake** page.")
        
        return
    
    data = st.session_state.data
    customers = data['customers']
    transactions = data['transactions']
    alerts = data['alerts']
    notes = data['notes']
    
    st.markdown('''
    
### Geographic Analysis

Geographic analysis is a critical component of AML investigations, as the physical locations of transactions can reveal significant risk cues. A geo map visualization helps analysts identify unusual transaction origins or destinations, clusters of suspicious activity in high-risk jurisdictions, or unexpected money flows across borders.

### Business Value of Geographic Risk Cues

*   **Risk Identification:** Pinpoint transactions originating from or destined for high-risk countries or regions.
*   **Pattern Recognition:** Identify common routes for illicit funds movement.
*   **Contextual Insight:** Understand the geographical nexus of a suspicious activity, which is crucial for determining the 'Where' of the 5Ws.
''')
    
    st.write("Transactions data:")
    st.dataframe(transactions.head())
    st.write("Transactions dataset information:", transactions.shape)

    geomap_fig = create_geo_map_visualization(transactions)
    st.plotly_chart(geomap_fig, use_container_width=True)
    
    
    st.markdown('''
                ### Findings from the Geo Map Visualization

(Interpretation based on generated plot)

This interactive geographic map highlights the origins of transactions, with marker size indicating the transaction amount. Key insights an analyst can glean include:

*   **Risky Geographies:** Identification of transaction clusters in known high-risk regions or jurisdictions with weak AML controls.
*   **Unexpected Locations:** Transactions originating from or destined for locations that have no logical business or personal connection to the customer.
*   **Concentration:** A high concentration of large transactions in specific areas could suggest a focal point for suspicious activity.

For example, if a customer primarily operates domestically but shows a sudden surge of transactions originating from a known offshore tax haven, this visualization would immediately flag that anomaly. This visual data is crucial for establishing the 'Where' of the suspicious activity in the SAR narrative.
''')
    
    st.markdown('''
                ## 5. Data Exploration: Counterparty Network Graph

Analyzing the network of relationships between customers and their counterparties is fundamental to uncovering complex money laundering schemes. A counterparty network graph visualizes these connections, revealing direct and indirect associations that might not be apparent from tabular data alone.

### Business Value of Network Graphs

*   **Relationship Mapping:** Clearly shows who is transacting with whom, identifying key intermediaries or beneficiaries.
*   **Hub Identification:** Pinpoints central nodes (customers) who act as significant connectors within the network, potentially orchestrating illicit activities.
*   **Anomaly Detection:** Helps in discovering unusual or circular transaction patterns, isolated groups, or unexpected links to known high-risk entities.

Mathematically, a graph $G = (V, E)$ is used, where:
*   $V$ is the set of vertices (customers/counterparties).
*   $E$ is the set of edges (transactions or relationships between $V$).

The graph can then be analyzed for properties like centrality (which nodes are most connected), shortest paths (how funds might flow), and community detection (groups of closely related entities).

This visualization technique helps an analyst piece together the 'Who' aspect of the 5Ws, revealing the full scope of individuals or entities involved in a suspicious activity.''')
    
    
    # Create the network graph
    counterparty_graph = create_counterparty_network_graph(transactions)

    # Visualize the graph (for demonstration, using matplotlib)
    plt.figure(figsize=(10, 8))
    if counterparty_graph.number_of_nodes() > 0:
        pos = nx.spring_layout(counterparty_graph, k=0.15, iterations=20) # positions for all nodes
        nx.draw_networkx_nodes(counterparty_graph, pos, node_size=200, node_color='skyblue')
        nx.draw_networkx_edges(counterparty_graph, pos, width=1, alpha=0.5, edge_color='gray')
        nx.draw_networkx_labels(counterparty_graph, pos, font_size=8, font_color='black')
        plt.title("Counterparty Network Graph")
        plt.axis('off') # Hide the axes
    else:
        plt.text(0.5, 0.5, "No nodes or edges to display.", horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)

    st.pyplot(plt)

    st.write(f"Number of nodes in the graph: {counterparty_graph.number_of_nodes()}")
    st.write(f"Number of edges in the graph: {counterparty_graph.number_of_edges()}")

    st.markdown('''
### Findings from the Counterparty Network Graph


The counterparty network graph visually represents the relationships between different customers based on their transactions. From this visualization, an AML analyst can derive several critical insights:

*   **Central Nodes/Hubs:** Customers with many connections (high degree centrality) are often central to the network. These 'hubs' might be facilitators, orchestrators, or key beneficiaries in a money laundering scheme. For example, if 'Customer 5' is connected to 20 other customers, they warrant closer inspection.
*   **Anomalous Connections:** Unexpected links between customers who seemingly have no legitimate business or personal relationship can be red flags.
*   **Dense Clusters:** Closely knit groups of customers might indicate a syndicate or a group acting in concert.
*   **Isolated Nodes:** Customers with very few connections might represent individual suspicious actors or the edges of a larger network.

This network perspective is invaluable for understanding the 'Who' is involved and how they are connected, moving beyond individual transactions to a holistic view of the suspicious ecosystem. It helps in building a more comprehensive SAR narrative.
''')
    
    
    st.markdown('''## Fact Snippet Selection (Simulated)

In a real-world AML investigation, an analyst sifts through vast amounts of data—transactions, alerts, KYC information, and notes—to identify the most pertinent facts. This curation process involves selecting specific pieces of information that directly support the narrative of suspicious activity. It's a critical human-in-the-loop step, ensuring that only relevant and factual data informs the SAR.

### How Analysts Curate Facts

Analysts act as filters, extracting the 'needle in the haystack' of data. They might highlight specific transactions that breach thresholds, alerts that align with known typologies, or notes that provide critical context. This process ensures the eventual SAR narrative is evidence-based and free from irrelevant noise.

### Technical Implementation (Simulated `selected_facts`)

To simulate this process, we will manually select a few representative rows from our synthetic `transactions`, `customers`, and `alerts` DataFrames. In a live system, this might be done via a UI where an analyst clicks to add facts to a 'facts tray'. For our purposes, we'll create a list of dictionaries, where each dictionary represents a key fact with relevant details. This structured `selected_facts` object will then be passed to the 5W extraction and LLM prompt building functions.)
''')
    
    st.write("Simulate an analyst selecting key facts for the SAR")
    
    
    # Simulate an analyst selecting key facts for the SAR
    # We'll pick a few transactions and an alert for a specific customer.

    # Let's focus on a hypothetical customer, e.g., customer_id = 7
    # Find customer details
    st.write("Find customer details")
    focused_customer_id = st.selectbox("Choose a customer to focus on", customers['customer_id'].unique(), index=6)
    customer_details = customers[customers['customer_id'] == focused_customer_id].to_dict('records')[0] if not customers[customers['customer_id'] == focused_customer_id].empty else {}
    st.dataframe(customer_details)

    # Find some transactions for this customer
    st.write("Find some transactions for this customer")
    customer_transactions = transactions[transactions['customer_id'] == focused_customer_id].head(3).to_dict('records')
    st.dataframe(customer_transactions)

    # Find an alert for this customer
    st.write("Find an alert for this customer")
    customer_alert = alerts[alerts['customer_id'] == focused_customer_id].head(1).to_dict('records')[0] if not alerts[alerts['customer_id'] == focused_customer_id].empty else {}
    st.dataframe(customer_alert)

    # Combine into selected_facts
    st.write("Combine into selected_facts")
    selected_facts = []
    if customer_details:
        selected_facts.append({"type": "Customer Info", **customer_details})

    for i, trans in enumerate(customer_transactions):
        selected_facts.append({"type": f"Transaction {i+1}", **trans})

    if customer_alert:
        selected_facts.append({"type": "Alert", **customer_alert})

    # If no specific customer data, just pick some random facts
    if not selected_facts:
        st.write("If no specific customer data, just pick some random facts")
        selected_facts.append({"type": "Customer Info", **customers.sample(1).to_dict('records')[0]})
        selected_facts.append({"type": "Transaction 1", **transactions.sample(1).to_dict('records')[0]})
        selected_facts.append({"type": "Alert", **alerts.sample(1).to_dict('records')[0]})

    st.write("Selected Facts:")
    st.dataframe(selected_facts)

    st.session_state.selected_facts = selected_facts
    
    st.markdown('''
### Confirming Selected Facts

The output above displays the `selected_facts` that an analyst has hypothetically curated for the SAR. This structured collection of information represents the core evidence supporting the suspicious activity. These facts will directly inform the subsequent 5W extraction process and, ultimately, the AI's narrative generation.

Each dictionary in the list provides specific details about a customer, transaction, or alert. For example, we can see:

*   **Customer Information:** `customer_id`, `name`, `country`, `risk_score`.
*   **Transaction Details:** `transaction_id`, `customer_id`, `transaction_amount`, `timestamp`, and dummy geographical coordinates.
*   **Alert Details:** `alert_id`, `customer_id`, `reason`, `timestamp`.

This confirmation step ensures that the LLM will receive the correct and relevant input, preventing the generation of narratives based on erroneous or irrelevant data. It bridges the gap between raw data and structured evidence, which is critical for a compliant SAR.

Next, draft the SAR narrative based on the selected facts. Head to the `Draft SAR (AI-augmented)` page.
                ''')