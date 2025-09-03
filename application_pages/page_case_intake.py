import streamlit as st
import pandas as pd
import numpy as np
import numpy as np
import pandas as pd
import math

def load_synthetic_data(seed: int | None = 42):
    """Generates synthetic data for AML analysis with US-only, region-clustered lat/lon."""
    if seed is not None:
        np.random.seed(seed)

    # ----------------------------
    # Region clusters (centers, weights, spread)
    # weights control how dense each region is
    # spread_km ~ radius of typical activity around the center
    # ----------------------------
    clusters = [
        {"name": "NYC",        "lat": 40.7128, "lon": -74.0060,  "weight": 0.18, "spread_km": 60},
        {"name": "LA",         "lat": 34.0522, "lon": -118.2437, "weight": 0.15, "spread_km": 70},
        {"name": "Chicago",    "lat": 41.8781, "lon": -87.6298,  "weight": 0.12, "spread_km": 55},
        {"name": "Miami",      "lat": 25.7617, "lon": -80.1918,  "weight": 0.10, "spread_km": 45},
        {"name": "Dallas",     "lat": 32.7767, "lon": -96.7970,  "weight": 0.10, "spread_km": 55},
        {"name": "San Fran",   "lat": 37.7749, "lon": -122.4194, "weight": 0.08, "spread_km": 40},
        {"name": "Atlanta",    "lat": 33.7490, "lon": -84.3880,  "weight": 0.08, "spread_km": 50},
        {"name": "Seattle",    "lat": 47.6062, "lon": -122.3321, "weight": 0.06, "spread_km": 40},
        {"name": "Phoenix",    "lat": 33.4484, "lon": -112.0740, "weight": 0.07, "spread_km": 50},
        {"name": "Denver",     "lat": 39.7392, "lon": -104.9903, "weight": 0.06, "spread_km": 45},
    ]
    # Optional tiny background probability for lightly populated areas
    background_weight = 0.02 # set to e.g. 0.02 for a little uniform scatter

    # CONUS bounding box (approx)
    LAT_MIN, LAT_MAX = 24.396308, 49.384358
    LON_MIN, LON_MAX = -124.848974, -66.885444

    def _km_to_deg_lat(km: float) -> float:
        return km / 111.0  # ~111 km per degree latitude

    def _km_to_deg_lon(km: float, at_lat_deg: float) -> float:
        return km / (111.0 * max(math.cos(math.radians(at_lat_deg)), 1e-6))

    def _sample_points_from_clusters(n: int, same_cluster_prob: float = 0.7):
        """Return origin/destination lat/lon arrays sampled from weighted clusters.
        same_cluster_prob controls how often dest stays in the same cluster as origin.
        """
        # Normalize weights
        w = np.array([c["weight"] for c in clusters], dtype=float)
        w = w / w.sum()
        # Choose origin clusters
        origin_idx = np.random.choice(len(clusters), size=n, p=w)

        # Choose destination clusters (often same as origin)
        dest_idx = origin_idx.copy()
        switch_mask = np.random.rand(n) > same_cluster_prob
        if switch_mask.any():
            # For those switching, choose a different cluster index
            alt_choices = np.random.choice(len(clusters), size=switch_mask.sum(), p=w)
            # Ensure different cluster; if equal, re-sample once (rare to collide twice)
            same = alt_choices == origin_idx[switch_mask]
            if same.any():
                alt_choices[same] = (alt_choices[same] + 1) % len(clusters)
            dest_idx[switch_mask] = alt_choices

        # Draw points around centers with Gaussian noise (spread in km -> degrees)
        o_lat = np.empty(n)
        o_lon = np.empty(n)
        d_lat = np.empty(n)
        d_lon = np.empty(n)

        for i, (oi, di) in enumerate(zip(origin_idx, dest_idx)):
            oc = clusters[oi]
            dc = clusters[di]

            # Origin jitter
            o_lat_sigma = _km_to_deg_lat(oc["spread_km"])
            o_lon_sigma = _km_to_deg_lon(oc["spread_km"], oc["lat"])
            o_lat[i] = np.random.normal(loc=oc["lat"], scale=o_lat_sigma)
            o_lon[i] = np.random.normal(loc=oc["lon"], scale=o_lon_sigma)

            # Destination jitter
            d_lat_sigma = _km_to_deg_lat(dc["spread_km"])
            d_lon_sigma = _km_to_deg_lon(dc["spread_km"], dc["lat"])
            d_lat[i] = np.random.normal(loc=dc["lat"], scale=d_lat_sigma)
            d_lon[i] = np.random.normal(loc=dc["lon"], scale=d_lon_sigma)

        # Optional light background sprinkle
        if background_weight > 0:
            bg_mask = np.random.rand(n) < background_weight
            if bg_mask.any():
                o_lat[bg_mask] = np.random.uniform(LAT_MIN, LAT_MAX, size=bg_mask.sum())
                o_lon[bg_mask] = np.random.uniform(LON_MIN, LON_MAX, size=bg_mask.sum())
                d_lat[bg_mask] = np.random.uniform(LAT_MIN, LAT_MAX, size=bg_mask.sum())
                d_lon[bg_mask] = np.random.uniform(LON_MIN, LON_MAX, size=bg_mask.sum())

        # Clip to US bounding box to guarantee in-range
        o_lat = np.clip(o_lat, LAT_MIN, LAT_MAX)
        o_lon = np.clip(o_lon, LON_MIN, LON_MAX)
        d_lat = np.clip(d_lat, LAT_MIN, LAT_MAX)
        d_lon = np.clip(d_lon, LON_MIN, LON_MAX)

        return o_lat, o_lon, d_lat, d_lon

    # ----------------------------
    # Customer data
    # ----------------------------
    num_customers = 1000
    customer_ids = range(1, num_customers + 1)
    customers_df = pd.DataFrame({
        "customer_id": list(customer_ids),
        "name": [f"Customer {i}" for i in customer_ids],
        "country": np.random.choice(["USA"], size=num_customers),
        "risk_score": np.random.randint(0, 100, size=num_customers),
    })

    # ----------------------------
    # Transaction data
    # ----------------------------
    num_transactions = 5000
    o_lat, o_lon, d_lat, d_lon = _sample_points_from_clusters(num_transactions, same_cluster_prob=0.72)

    transactions_df = pd.DataFrame({
        "transaction_id": range(1, num_transactions + 1),
        "customer_id": np.random.choice(list(customer_ids), size=num_transactions),
        "transaction_amount": np.random.uniform(10, 1000, size=num_transactions),
        "timestamp": pd.date_range("2023-01-01", periods=num_transactions, freq="h"),
        "origin_latitude": o_lat,
        "origin_longitude": o_lon,
        "destination_latitude": d_lat,
        "destination_longitude": d_lon,
        "Source": np.random.choice(list(customer_ids), size=num_transactions),
        "Target": np.random.choice(list(customer_ids), size=num_transactions),
    })

    # ----------------------------
    # Alerts data
    # ----------------------------
    num_alerts = 50
    alerts_df = pd.DataFrame({
        "alert_id": range(1, num_alerts + 1),
        "customer_id": np.random.choice(list(customer_ids), size=num_alerts),
        "reason": np.random.choice([
            "Suspicion concerning the source of funds",
            "Transaction(s) below CTR threshold",
            "Check",
            "Transaction with no apparent economic, business, or lawful purpose",
            "Transaction out of pattern for customer(s)",
            "Suspicious EFT/wire transfers",
            "Suspicious use of multiple transaction locations",
            "Credit/Debit card",
            "Identity theft",
            "Fraud - Other"
        ], size=num_alerts),
        "timestamp": pd.date_range("2023-01-05", periods=num_alerts, freq="D"),
    })

    # ----------------------------
    # Notes data
    # ----------------------------
    num_notes = 30
    notes_df = pd.DataFrame({
        "note_id": range(1, num_notes + 1),
        "customer_id": np.random.choice(list(customer_ids), size=num_notes),
        "note": [f"Note for customer {i}" for i in range(1, num_notes + 1)],
        "timestamp": pd.date_range("2023-01-10", periods=num_notes, freq="D"),
    })

    return {
        "customers": customers_df,
        "transactions": transactions_df,
        "alerts": alerts_df,
        "notes": notes_df,
    }



def calculate_summary_kpis(transactions):
    """Calculates key performance indicators (KPIs) from transaction data."""

    total_transaction_volume = transactions['transaction_amount'].sum()
    average_transaction_amount = transactions['transaction_amount'].mean() if not transactions.empty else 0
    transactions_per_customer = transactions.groupby('customer_id').size().to_dict()

    return {
        'Total Transaction Volume': total_transaction_volume,
        'Average Transaction Amount': average_transaction_amount,
        'Transactions per Customer': transactions_per_customer,
    }


def run_page():
    st.markdown("# Case Intake")
    
    st.markdown('''
## Data Loading and Preparation

In this section, we define and execute a function to generate synthetic data. This data simulates various aspects of an AML investigation, including customer profiles, financial transactions, system alerts, and analyst notes. Using synthetic data allows us to demonstrate the SAR narrative generator's capabilities without handling sensitive real-world information.

### Synthetic Data Schemas

*   **Customers:** `customer_id`, `name`, `country`, `risk_score`
*   **Transactions:** `transaction_id`, `customer_id`, `amount`, `timestamp`
*   **Alerts:** `alert_id`, `customer_id`, `reason`, `timestamp`
*   **Notes:** `note_id`, `customer_id`, `note`, `timestamp`

This structured data will serve as the foundation for extracting key facts and insights that feed into our AI-assisted narrative generation process.
''')


    # Option to load synthetic data if no file is uploaded
    if st.button("Load Synthetic Data"): # Using a button for demonstration
        data = load_synthetic_data()
        
        customers = data["customers"]
        transactions = data["transactions"]
        alerts = data["alerts"]
        notes = data["notes"]
        
        st.session_state.data = data
        st.session_state.customers = customers
        st.session_state.transactions = transactions
        st.session_state.alerts = alerts
        st.session_state.notes = notes
        
        st.markdown('''
### Data Overview: Shapes and Row Counts

After generating the synthetic datasets, it's good practice to quickly inspect their dimensions to ensure the data has been loaded as expected. This helps confirm that each dataset contains a reasonable number of records and columns, providing a preliminary check before diving into analysis.

*   `customers`: Represents individual customer entities.
*   `transactions`: Details of financial transactions, including amounts and timestamps.
*   `alerts`: Records of system-generated alerts for suspicious activities.
*   `notes`: Manual notes added by analysts during case investigation.

Confirming these shapes validates the initial data loading step and sets the stage for further exploration and processing.''')

        # Rename 'amount' to 'transaction_amount' for consistency with KPI function
        transactions = transactions.rename(columns={'amount': 'transaction_amount'})

        # Calculate and display summary KPIs
        kpis = calculate_summary_kpis(transactions)
        st.session_state.kpis = kpis

        st.subheader("Synthetic Data Loaded")
        st.write("Preview of synthetic transaction data:")
        st.dataframe(transactions.head())

        st.markdown(r'''## Case Intake and Summary KPIs

At the initial stage of a SAR investigation, it's critical for AML analysts to quickly grasp the scope and key characteristics of a case. Calculating summary Key Performance Indicators (KPIs) provides an immediate, high-level overview of the transactional activity associated with the suspicious entity or account. This rapid assessment helps in prioritizing cases, understanding the magnitude of activity, and identifying initial areas of interest.

### Business Value of Early Summarization

*   **Rapid Assessment:** Analysts can quickly determine the scale of the customer's financial activity.
*   **Prioritization:** High-volume or high-value cases might warrant immediate attention.
*   **Context Setting:** Provides a quantitative baseline for understanding subsequent detailed investigations.

1.  **Total Transaction Volume:** This is the sum of all `transaction_amount`s, representing the total monetary value processed. Mathematically, it's calculated as:
    
    $$\text{Total Volume} = \sum_{i=1}^{N} \text{transaction\_amount}_i $$

  where $N$ is the total number of transactions.

2.  **Average Transaction Amount:** This gives a sense of the typical size of a transaction, calculated as the total volume divided by the number of transactions:
    
    $$ \text{Average Amount} = \frac{\text{Total Volume}}{\text{Number of Transactions}} $$

3.  **Transactions per Customer:** This aggregates the number of transactions for each unique customer, revealing activity levels at an individual level.

These KPIs are fundamental for painting an initial picture of the case, guiding the analyst on where to focus their deeper investigative efforts.
''')
        
        
        kpis = calculate_summary_kpis(transactions)
        st.write("### Summary KPIs:")
        for key, value in kpis.items():
            if key == 'Transactions per Customer':
                st.write(f"  {key}: {len(value)} unique customers with transactions")
            else:
                st.write(f"  {key}: {value:,.2f}")
        
        st.markdown('''
### Interpreting the KPIs

The summary KPIs provide immediate insights into the transaction data:

*   **Total Transaction Volume:** Indicates the overall monetary scale of transactions within the dataset. A high volume might suggest significant financial activity, warranting closer scrutiny.
*   **Average Transaction Amount:** Gives a representative value for individual transactions. Deviations from expected averages could signal unusual behavior, such as a large number of small, structured transactions (smurfing) or a few exceptionally large, anomalous transactions.
*   **Transactions per Customer:** Shows the distribution of activity across customers. A customer with a disproportionately high number of transactions compared to others could be a central figure in a suspicious network.

These metrics are vital for an AML analyst to quickly size up a case, identify potential red flags, and determine the next steps for a more detailed investigation. For instance, if the total volume is high but the average amount is low, it might point towards micro-transactions designed to evade detection thresholds. Conversely, a few very large transactions could indicate a direct movement of illicit funds.                    
''')
        st.divider()
        
        st.write("Customers data:")
        st.dataframe(customers.head())
        st.write("Customers dataset information:", customers.shape)
        
        st.write("Transactions data:")
        st.dataframe(transactions.head())
        st.write("Transactions dataset information:", transactions.shape)
        
        st.write("Alerts data:")
        st.dataframe(alerts.head())
        st.write("Alerts dataset information:", alerts.shape)
        
        st.write("Notes data:")
        st.dataframe(notes.head())
        st.write("Notes dataset information:", notes.shape)

        st.write("Now head over to the `Explore Data` page to explore the data.")
        
        

if __name__ == "__main__":
    run_page()
