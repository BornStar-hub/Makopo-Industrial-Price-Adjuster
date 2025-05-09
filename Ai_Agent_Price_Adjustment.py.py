import pandas as pd
import pdfplumber

try:
    import streamlit as st
except ImportError:
    raise ImportError("Streamlit is not installed. Please install it using: pip install streamlit")

# Function to load vendor catalog and apply price adjustment
def adjust_prices(catalog, percentage_increase=25):
    if 'Price' not in catalog.columns:
        raise ValueError("The catalog must have a 'Price' column.")

    # Calculate the new prices
    catalog['New Price'] = catalog['Price'] * (1 + percentage_increase / 100)
    return catalog

# Function to extract table from PDF (assuming tabular data)
def extract_pdf_table(file_path):
    with pdfplumber.open(file_path) as pdf:
        first_page = pdf.pages[0]
        table = first_page.extract_table()

        # Convert table to DataFrame
        df = pd.DataFrame(table[1:], columns=table[0])
        return df

# Streamlit App UI
st.set_page_config(page_title="Makopo Industrial Price Adjuster", page_icon="💰", layout="wide")
st.title("📊 Makopo Industrial - Vendor Catalog Price Adjuster")
st.markdown("Upload your vendor catalog (CSV, Excel, or PDF) to automatically adjust the prices by 25%.")

uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "pdf"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            catalog = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            catalog = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith(".pdf"):
            catalog = extract_pdf_table(uploaded_file)

        st.subheader("Original Catalog")
        st.write(catalog)

        adjusted_catalog = adjust_prices(catalog)

        st.subheader("Updated Catalog (Price +25%)")
        st.write(adjusted_catalog)

        st.download_button(
            label="Download Updated Catalog",
            data=adjusted_catalog.to_csv(index=False),
            file_name="updated_vendor_catalog.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.image("https://makopoindustrial.com/wp-content/uploads/2025/01/cropped-cropped-makopo_industrial_logo-removebg-preview-AQEy5BpLvjsDq6E1.png", width=150)
    st.markdown("### Troubleshooting Guide")
    st.markdown("1. Ensure your file is CSV, Excel, or PDF.\n2. Make sure the 'Price' column is included.\n3. Contact support if issues persist.")
