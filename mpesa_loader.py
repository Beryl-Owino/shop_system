import pandas as pd

# ==============================
# FUNCTION: LOAD MPESA DATA
# ==============================
def load_mpesa_data(file_path):
    df = pd.read_csv(file_path)
    print("Data loaded successfully!")
    return df

# ==============================
# FUNCTION: CLEAN MPESA DATA    
# ==============================
def clean_columns(df):
    df.columns = df.columns.str.strip().str.lower()
    df["date"] = pd.to_datetime(df["date"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0).astype(int)
    df["balance"] = pd.to_numeric(df["balance"], errors="coerce").fillna(0).astype(int)
    return df

# ==============================
# FUNCTION: TYPE MAPPING
# ==============================

def map_transaction_types(t_type):    # Data abstration layer - we convert raw types to "income" or "expense"
    t_type = t_type.lower()
    if "customer payment" in t_type:
        return "income"
    elif "paybill" in t_type:
        return "income"
    elif "buy goods" in t_type:
        return "income"
    elif "withdrawal" in t_type:
        return "expense"
    else:
        return "other"
    
def apply_type_mapping(df):    # We apply the mapping to create a new "category" column
    df["category"] = df["type"].apply(map_transaction_types)
    return df


# ==============================
# FUNCTION: FILTERING AND CREATING PIPELINE
# ==============================
def filter_valid(df):
    df = df[df["amount"] != 0]  # Remove zero-amount transactions
    df = df[df["category"] != "other"]  # Remove uncategorized transactions
    return df



def process_mpesa_data(file_path):
    df = load_mpesa_data(file_path)
    df = clean_columns(df)
    df = apply_type_mapping(df)
    df = filter_valid(df)
    df["date"] = df["date"].astype(str) 

    print(" MPESA Data Processed Successfully!")
    print(df.head())

    return df


