
import streamlit as st
import pandas as pd
import numpy as np

# Optional: Load environment variables from a .env file for local development
# For production, secrets should be managed securely (e.g., Kubernetes secrets, AWS Secrets Manager)
# load_dotenv() # This should be in app.py or a config.py if used globally

numpy.random.seed(42)

def load_synthetic_data():
    """Generates synthetic data for AML analysis."""

    # Customer data
    num_customers = 100
    customer_ids = range(1, num_customers + 1)
    customer_data = {
        "customer_id": customer_ids,
        "name": [f"Customer {i}" for i in customer_ids],
        "country": np.random.choice(["USA", "Canada", "UK", "Germany", "France"], size=num_customers),
        "risk_score": np.random.randint(0, 100, size=num_customers),
    }
    customers_df = pd.DataFrame(customer_data)

    # Transaction data
    num_transactions = 500
    transaction_data = {
        "transaction_id": range(1, num_transactions + 1),
        "customer_id": np.random.choice(customer_ids, size=num_transactions),
        "amount": np.random.uniform(10, 1000, size=num_transactions),
        "timestamp": pd.date_range("2023-01-01", periods=num_transactions, freq="H"),
        "origin_latitude": np.random.uniform(25, 50, size=num_transactions), # Dummy lat
        "origin_longitude": np.random.uniform(-120, -70, size=num_transactions), # Dummy lon
        "destination_latitude": np.random.uniform(25, 50, size=num_transactions), # Dummy lat
        "destination_longitude": np.random.uniform(-120, -70, size=num_transactions), # Dummy lon
        "Source": np.random.choice(customer_ids, size=num_transactions), # Dummy Source for network graph
        "Target": np.random.choice(customer_ids, size=num_transactions)  # Dummy Target for network graph
    }
    transactions_df = pd.DataFrame(transaction_data)

    # Alert data
    num_alerts = 50
    alert_data = {
        "alert_id": range(1, num_alerts + 1),
        "customer_id": np.random.choice(customer_ids, size=num_alerts),
        "reason": np.random.choice(["High transaction volume", "Unusual transaction location", "Suspicious activity"], size=num_alerts),
        "timestamp": pd.date_range("2023-01-05", periods=num_alerts, freq="D"),
    }
    alerts_df = pd.DataFrame(alert_data)

    # Notes data
    num_notes = 30
    note_data = {
        "note_id": range(1, num_notes + 1),
        "customer_id": np.random.choice(customer_ids, size=num_notes),
        "note": [f"Note for customer {i}" for i in range(1, num_notes + 1)],
        "timestamp": pd.date_range("2023-01-10", periods=num_notes, freq="D"),
    }
    notes_df = pd.DataFrame(note_data)

    return {
        "customers": customers_df,
        "transactions": transactions_df,
        "alerts": alerts_df,
        "notes": notes_df,
    }

def calculate_summary_kpis(transactions):
    """Calculates key performance indicators (KPIs) from transaction data."""

    total_transaction_volume = transactions['transaction_amount'].sum() if 'transaction_amount' in transactions.columns else transactions['amount'].sum()
    average_transaction_amount = transactions['transaction_amount'].mean() if 'transaction_amount' in transactions.columns and not transactions.empty else (transactions['amount'].mean() if 'amount' in transactions.columns and not transactions.empty else 0)
    transactions_per_customer = transactions.groupby('customer_id').size().to_dict()

    return {
        'total_transaction_volume': total_transaction_volume,
        'average_transaction_amount': average_transaction_amount,
        'transactions_per_customer': transactions_per_customer,
    }

def run_page():
    st.header("Case Intake")
    st.markdown("""
    This page allows you to load case bundles and get a quick overview of the key statistics. 
    You can either upload your own data or use the synthetic data provided for demonstration purposes.

    The application will automatically calculate key performance indicators (KPIs) and suggest possible typologies based on the loaded data.
    """)

    if st.button("Load Synthetic Data"):
        st.session_state.data = load_synthetic_data()
        st.session_state.data["transactions"] = st.session_state.data["transactions"].rename(columns={'amount': 'transaction_amount'})
        st.success("Synthetic data loaded successfully!")

    uploaded_file = st.file_uploader("Upload Case Bundle (e.g., CSV, Excel)", type=["csv", "xlsx"])
    if uploaded_file is not None:
        # In a real scenario, you'd parse multiple files in a "case bundle"
        # For simplicity, let's assume a single transaction file upload.
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.session_state.data["transactions"] = df.rename(columns={'amount': 'transaction_amount'})
            st.success("File loaded successfully into transactions data!")
        except Exception as e:
            st.error(f"Error loading file: {e}")

    if st.session_state.data and "transactions" in st.session_state.data:
        st.subheader("Data Overview: Transactions")
        st.write(st.session_state.data["transactions"].head())
        st.write(f"Shape: {st.session_state.data['transactions'].shape}")

        st.subheader("Quick Stats")
        transactions_df = st.session_state.data["transactions"]

        # Ensure timestamp is datetime for calculations
        if 'timestamp' in transactions_df.columns:
            transactions_df['timestamp'] = pd.to_datetime(transactions_df['timestamp'], errors='coerce')
            transactions_df = transactions_df.dropna(subset=['timestamp'])

        if not transactions_df.empty:
            kpis = calculate_summary_kpis(transactions_df)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="# Transactions", value=len(transactions_df))
                if 'transaction_amount' in transactions_df.columns:
                    st.metric(label="Total In/Out Volume", value=f"${kpis['total_transaction_volume']:.2f}")
            with col2:
                st.metric(label="# Customers", value=transactions_df['customer_id'].nunique())
                if 'transaction_amount' in transactions_df.columns:
                    st.metric(label="Average Transaction Amount", value=f"${kpis['average_transaction_amount']:.2f}")
            with col3:
                st.metric(label="Time Window", value=f"{transactions_df['timestamp'].min().strftime('%Y-%m-%d')} to {transactions_df['timestamp'].max().strftime('%Y-%m-%d')}" if not transactions_df.empty and 'timestamp' in transactions_df.columns else "N/A")
                st.metric(label="# Alerts", value=len(st.session_state.data['alerts']) if 'alerts' in st.session_state.data else 0)

            st.subheader("Possible Typologies")
            # This is a placeholder for actual typology detection. For now, it will be based on dummy reasons or patterns.
            typologies = []
            if 'alerts' in st.session_state.data and not st.session_state.data['alerts'].empty:
                typologies.extend(st.session_state.data['alerts']['reason'].unique().tolist())
            if kpis['total_transaction_volume'] > 50000 and 'High transaction volume' not in typologies:
                typologies.append('High Transaction Volume')
            if kpis['average_transaction_amount'] < 50 and 'Structuring (small amounts)' not in typologies:
                typologies.append('Structuring (small amounts)')

            if typologies:
                st.markdown(" ".join([f"<span style='background-color:#e6e6fa; padding: 5px 10px; border-radius: 15px; margin: 5px; display: inline-block;'>{t}</span>" for t in set(typologies)]), unsafe_allow_html=True)
            else:
                st.info("No specific typologies detected yet.")
        else:
            st.warning("No transaction data available to calculate quick stats.")
    else:
        st.info("Please load data using the buttons above.")
