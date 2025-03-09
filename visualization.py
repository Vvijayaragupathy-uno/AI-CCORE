import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from chatbot import chatbot

def visualization_page():

    if st.button("<"):
        st.session_state.page = "public"
        st.rerun()
    st.header("Model Benchmark Visualization")
    st.write("Explore the performance and cost-effectiveness of different models.")

    # Load the data
    data = pd.read_csv(r'D:\AICCORE\models benchmark1.csv')

    # Convert 'Parameters (B)' column to numeric, coercing errors to NaN
    data['Parameters (B)'] = pd.to_numeric(data['Parameters (B)'], errors='coerce')

    # Sidebar filters
    st.sidebar.header("Filters")

    # Organization filter
    selected_organization = st.sidebar.multiselect(
        "Select Organization", 
        data['Organisation'].unique()
    )

    # License type filter
    selected_license = st.sidebar.multiselect(
        "Select License Type", 
        data['License'].unique()
    )
    # Benchmark filter
    selected_benchmarks = st.sidebar.multiselect(
        "Select Benchmarks", 
        ['GPQA', 'MMLU', 'MMLU Pro', 'DROP', 'HumanEval']
    )

    # Filter data based on selections
    filtered_data = data

    if selected_organization:
        filtered_data = filtered_data[filtered_data['Organisation'].isin(selected_organization)]

    if selected_license:
        filtered_data = filtered_data[filtered_data['License'].isin(selected_license)]

    # Display filtered data
    st.write("Filtered Data:", filtered_data)

    # Calculate total cost
    filtered_data['Total Cost $/M'] = filtered_data['Input $/M'] + filtered_data['Output $/M']

   
    # Top Models by Benchmark
    st.header("Top Models by Benchmark")

    # Select benchmark for top performers
    selected_benchmark = st.selectbox(
        "Select Benchmark for Top Performers",
        ['GPQA', 'MMLU', 'MMLU Pro', 'DROP', 'HumanEval']
    )

    # Get top 5 models for the selected benchmark
    top_models = filtered_data.dropna(subset=[selected_benchmark]).sort_values(by=selected_benchmark, ascending=False).head(5)

    # Display top models in a table
    st.write(f"Top 5 Models by {selected_benchmark}:")
    st.table(top_models[['Model', 'Organisation', selected_benchmark]])

    # Allow user to select chart type
    chart_type = st.selectbox(
        "Select Chart Type",
        ["Bar Chart", "Line Chart", "Scatter Plot"]
    )

    # Visualize top models based on selected chart type
    st.header(f"Top 5 Models by {selected_benchmark} ({chart_type})")
    plt.figure(figsize=(10, 6))

    if chart_type == "Bar Chart":
        # Bar Chart
        sns.barplot(x='Model', y=selected_benchmark, data=top_models, hue='Organisation')
        plt.xticks(rotation=45)
        plt.title(f"Top 5 Models by {selected_benchmark} (Bar Chart)")

    elif chart_type == "Line Chart":
        # Line Chart
        sns.lineplot(x='Model', y=selected_benchmark, data=top_models, hue='Organisation', marker='o')
        plt.xticks(rotation=45)
        plt.title(f"Top 5 Models by {selected_benchmark} (Line Chart)")

    elif chart_type == "Scatter Plot":
        # Scatter Plot
        sns.scatterplot(x='Model', y=selected_benchmark, data=top_models, hue='Organisation', s=100)
        plt.xticks(rotation=45)
        plt.title(f"Top 5 Models by {selected_benchmark} (Scatter Plot)")

    # Display the plot in Streamlit
    st.pyplot(plt)
     # Plot GPQA scores
    if 'GPQA' in selected_benchmarks:
        st.header("GPQA Scores by Model")
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Model', y='GPQA', data=filtered_data.sort_values(by='GPQA', ascending=False))
        plt.xticks(rotation=90)
        st.pyplot(plt)

    # Plot MMLU scores
    if 'MMLU' in selected_benchmarks:
        st.header("MMLU Scores by Model")
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Model', y='MMLU', data=filtered_data.sort_values(by='MMLU', ascending=False))
        plt.xticks(rotation=90)
        st.pyplot(plt)

    # Plot MMLU Pro scores
    if 'MMLU Pro' in selected_benchmarks:
        st.header("MMLU Pro Scores by Model")
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Model', y='MMLU Pro', data=filtered_data.sort_values(by='MMLU Pro', ascending=False))
        plt.xticks(rotation=90)
        st.pyplot(plt)

    # Plot DROP scores
    if 'DROP' in selected_benchmarks:
        st.header("DROP Scores by Model")
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Model', y='DROP', data=filtered_data.sort_values(by='DROP', ascending=False))
        plt.xticks(rotation=90)
        st.pyplot(plt)

    # Plot HumanEval scores
    if 'HumanEval' in selected_benchmarks:
        st.header("HumanEval Scores by Model")
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Model', y='HumanEval', data=filtered_data.sort_values(by='HumanEval', ascending=False))
        plt.xticks(rotation=90)
        st.pyplot(plt)


    # Bar chart: Open vs. Proprietary Models
    st.header("Open vs. Proprietary Models")
    license_counts = filtered_data['License'].value_counts()
    plt.figure(figsize=(6, 4))
    sns.barplot(x=license_counts.index, y=license_counts.values)
    st.pyplot(plt)

    st.header("Performance Distribution by Organization")
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Organisation', y='GPQA', data=filtered_data)
    plt.xticks(rotation=90)
    st.pyplot(plt)
    
