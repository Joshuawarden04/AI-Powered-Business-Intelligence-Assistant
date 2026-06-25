import streamlit as st
import pandas as pd
import ollama

# Read Excel File
df = pd.read_excel("sales_dataset.xlsx")

# Title
st.title("AI Business Intelligence Assistant")

# Show Dataset
st.subheader("Dataset")
st.dataframe(df)

# KPIs
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Sales", f"₹{total_sales:,}")

with col2:
    st.metric("Total Profit", f"₹{total_profit:,}")

# Sales by Region
sales_region = df.groupby("Region")["Sales"].sum()

st.subheader("Sales by Region")
st.bar_chart(sales_region)

# Product Analysis
product_sales = df.groupby("Product")["Sales"].sum()

# Ask Questions
st.subheader("Ask Questions")

question = st.text_input(
    "Type your business question here"
)

if question:

    q = question.lower()

    # Highest Sales Region
    if "highest sales" in q or "best region" in q:

        region = sales_region.idxmax()
        amount = sales_region.max()

        st.success(
            f"{region} region has the highest sales of ₹{amount:,}"
        )

    # Total Sales
    elif "total sales" in q:

        st.success(
            f"Total Sales = ₹{total_sales:,}"
        )

    # Total Profit
    elif "total profit" in q:

        st.success(
            f"Total Profit = ₹{total_profit:,}"
        )

    # Best Product
    elif "best product" in q or "highest product" in q:

        best_product = product_sales.idxmax()
        amount = product_sales.max()

        st.success(
            f"{best_product} is the best-selling product with sales of ₹{amount:,}"
        )

    # Recommendation using AI
    elif "recommendation" in q:

        prompt = f"""
        You are a business analyst.

        Dataset:

        {df.to_string(index=False)}

        Give 3 short business recommendations.
        """

        response = ollama.chat(
            model="phi3:mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        st.success(
            response["message"]["content"]
        )

    else:

        st.warning(
            """
Try questions like:

• Which region has highest sales?

• What is total sales?

• What is total profit?

• Which is the best product?

• Give recommendation
"""
        )

# Executive Summary
st.subheader("Executive Summary")

if st.button("Generate Summary"):

    best_region = sales_region.idxmax()

    weak_region = sales_region.idxmin()

    best_product = product_sales.idxmax()

    st.success(f"""
Total Sales : ₹{total_sales:,}

Total Profit : ₹{total_profit:,}

Best Region : {best_region}

Weakest Region : {weak_region}

Best Product : {best_product}

Recommendation :

1. Focus marketing in weak-performing regions.

2. Increase inventory for best-selling products.

3. Improve promotional activities to increase profit.
""")

# Footer
st.markdown("---")
st.caption(
    "AI Business Intelligence Assistant using Streamlit, Pandas and Ollama (Phi-3 Mini)"
)
