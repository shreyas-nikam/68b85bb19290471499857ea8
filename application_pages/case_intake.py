"""
import streamlit as st
import pandas as pd
import plotly.express as px

def load_synthetic_data():
    """
    Generates synthetic KYC, transaction, alert, and notes data for AML analysis.
    Arguments:
        None
    Output:
        Returns a dictionary containing Pandas DataFrames for customers, transactions, alerts, and notes.
    """
    # Generate synthetic KYC data
    customers = pd.DataFrame({
        'customer_id': [f"C{i:03d}" for i in range(1, 11)],
        'name': [f"Customer {i}" for i in range(1, 11)],
        'kyc_risk_score': [round(i * 0.5, 2) + 1 for i in range(1, 11)],
        'country': ['USA', 'CAN', 'MEX', 'USA', 'GBR', 'FRA', 'DEU', 'JPN', 'AUS', 'USA']
    })

    # Generate synthetic transaction data
    transaction_data = []
    for i in range(200):
        customer_id = f"C{pd.np.random.randint(1, 11):03d}"
        transaction_type = pd.np.random.choice(['deposit', 'withdrawal', 'transfer_in', 'transfer_out'])
        amount = round(pd.np.random.uniform(100, 10000), 2)
        timestamp = pd.to_datetime('2023-01-01') + pd.Timedelta(minutes=pd.np.random.randint(0, 525600)) # Last year
        channel = pd.np.random.choice(['online', 'branch', 'atm', 'mobile'])
        branch = pd.np.random.choice([f"B{j:02d}" for j in range(1, 6)])
        counterparty_id = f"P{pd.np.random.randint(1, 21):03d}"
        transaction_data.append({
            'transaction_id': f"T{i:05d}",
            'customer_id': customer_id,
            'timestamp': timestamp,
            'type': transaction_type,
            'amount': amount,
            'channel': channel,
            'branch': branch,
            'counterparty_id': counterparty_id
        })
    transactions = pd.DataFrame(transaction_data)

    # Generate synthetic alert data
    alerts = pd.DataFrame({
        'alert_id': [f"A{i:03d}" for i in range(1, 6)],
        'customer_id': [f"C{pd.np.random.randint(1, 11):03d}" for _ in range(5)],
        'transaction_id': [f"T{pd.np.random.randint(1, 201):05d}" for _ in range(5)],
        'alert_type': pd.np.random.choice(['smurfing', 'structuring', 'wire_fraud'], 5),
        'status': pd.np.random.choice(['open', 'closed'], 5),
        'raised_date': pd.to_datetime(['2023-05-10', '2023-06-15', '2023-07-20', '2023-08-25', '2023-09-30'])
    })

    # Generate synthetic notes data
    notes = pd.DataFrame({
        'note_id': [f"N{i:03d}" for i in range(1, 8)],
        'customer_id': [f"C{pd.np.random.randint(1, 11):03d}" for _ in range(7)],
        'note_text': [f"Note {i} about customer {pd.np.random.randint(1, 11)}" for i in range(1, 8)],
        'created_by': pd.np.random.choice(['Analyst1', 'Analyst2'], 7),
        'created_date': pd.to_datetime(['2023-01-05', '2023-02-10', '2023-03-15', '2023-04-20', '2023-05-25', '2023-06-30', '2023-07-05'])
    })

    return {'customers': customers, 'transactions': transactions, 'alerts': alerts, 'notes': notes}

def calculate_summary_kpis(transactions):
    """
    Calculates key performance indicators (KPIs) from transaction data, such as total transaction volume, 
    average transaction amount, and number of transactions per customer.
    Arguments:
        transactions (Pandas DataFrame)
    Output:
        Returns a dictionary containing the calculated KPIs.
    """
    if transactions.empty:
        return {
            "# Transactions": 0,
            "Total Inflow": 0,
            "Total Outflow": 0,
            "# Branches": 0,
            "# Unique Customers": 0,
            "Time Window": "N/A"
        }

    total_transactions = len(transactions)
    total_inflow = transactions[transactions['type'].isin(['deposit', 'transfer_in'])]['amount'].sum()
    total_outflow = transactions[transactions['type'].isin(['withdrawal', 'transfer_out'])]['amount'].sum()
    num_branches = transactions['branch'].nunique()
    num_unique_customers = transactions['customer_id'].nunique()
    min_date = transactions['timestamp'].min()
    max_date = transactions['timestamp'].max()
    time_window = f"{min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}"

    return {
        "# Transactions": total_transactions,
        "Total Inflow": total_inflow,
        "Total Outflow": total_outflow,
        "# Branches": num_branches,
        "# Unique Customers": num_unique_customers,
        "Time Window": time_window
    }

def run_case_intake():
    st.header("Case Intake")
    st.markdown("Upload your case bundles here or use synthetic data to get started.")

    # About / Controls panel
    with st.expander("About / Controls"):
        st.markdown(r"""
        This section outlines key regulatory guidance and risk considerations for AML analysis and SAR drafting:

        **BSA/FinCEN SAR Requirements:**
        The Bank Secrecy Act (BSA) requires financial institutions to report suspicious transactions to FinCEN. 
        SARs are critical tools in combating money laundering and terrorist financing. 
        Key requirements include timely filing (within 30-60 days), comprehensive narratives, and adherence to specific reporting thresholds.
        More information: [FinCEN SAR Home Page](https://www.fincen.gov/sar-home-page)

        **FinCEN Narrative Guidance:**
        FinCEN provides guidance on writing effective SAR narratives. Narratives should be:
        *   **Clear, concise, and chronological:** Present facts in a logical order.
        *   **Specific:** Include names, dates, amounts, and transaction types.
        *   **Comprehensive:** Cover all suspicious activity identified.
        *   **Fact-based:** Avoid speculation or legal conclusions.
        *   **5Ws:** Address Who, What, When, Where, Why (and How).
        More information: [FinCEN SAR Guidance](https://www.fincen.gov/resources/sar-guidance)

        **OCC/SR 11-7 Model Risk Management:**
        The Office of the Comptroller of the Currency (OCC) Supervisory Guidance SR 11-7 addresses model risk management. 
        When using AI/ML models for AML, it