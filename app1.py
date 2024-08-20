import streamlit as st
import pandas as pd
import pickle
import os
import networkx as nx
import matplotlib.pyplot as plt

# Function to load data
def load_data(file_path):
    return pd.read_csv(file_path)

# Function to load models
def load_model(model_path):
    with open(model_path, 'rb') as f:
        return pickle.load(f)

# Recommendation function
def get_recommendations(input_products, rules, data, key_column, description_col, max_recommendations=5):
    recommendations = set()

    for index, rule in rules.iterrows():
        if set(rule['antecedents']).issubset(set(input_products)):
            recommendations.update(rule['consequents'])

    recommendations = list(recommendations - set(input_products))
    recommended_products = data[data[key_column].isin(recommendations)]
    recommended_products = recommended_products[[key_column, description_col]].drop_duplicates().head(max_recommendations)

    return recommended_products

def plot_network_graph(rules):
    G = nx.DiGraph()
    
    # Add edges to the graph for all rules
    for _, row in rules.iterrows():
        for antecedent in row['antecedents']:
            for consequent in row['consequents']:
                G.add_edge(antecedent, consequent, weight=row['lift'])
    
    pos = nx.spring_layout(G, seed=42)
    
    plt.figure(figsize=(12, 12))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray')
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.title('Network Graph of Association Rules')
    st.pyplot(plt)

# Streamlit UI
# Center the title and split the text into two lines with different font sizes
st.markdown(
    """
    <h1 style='text-align: center; font-size: 56px;'>
        Product Recommendation
        <br>
        <span style='font-size: 36px;'>Based On Basket-Analysis</span>
    </h1>
    """,
    unsafe_allow_html=True
)


# Only one page option: Order Report
st.image(os.path.join('images', 'emsbay.jpg'), caption='', use_column_width=True)

order_report_apriori_model = load_model(os.path.join('models', 'product_recommendation_model_order_apriori.pkl'))
order_report_fpgrowth_model = load_model(os.path.join('models', 'product_recommendation_model_order_fp-growth.pkl'))
order_report_data = load_data(os.path.join('data', 'order_report_final.csv'))

method = st.radio("Choose method", ("Apriori", "FP-Growth"))
rules = order_report_apriori_model if method == "Apriori" else order_report_fpgrowth_model

# Dropdown for input_products using multiselect
input_products_list = st.multiselect(
    "Select ASINs",
    options=order_report_data['asin'].unique(),
    help="Select one or more ASINs for which you want recommendations."
)

if input_products_list:
    
    st.write("You selected the following products:")
    input_products_df = order_report_data[order_report_data['asin'].isin(input_products_list)].drop_duplicates(subset=['asin'])
    if not input_products_df.empty:
        for index, row in input_products_df.iterrows():
            st.write(f"{row['asin']}: {row['product']}")
    else:
        st.write("No matching products found for the selected ASINs.")
    
    recommended_products = get_recommendations(input_products_list, rules, order_report_data, 'asin', 'product')
    st.write("Top 5 Recommended products:")
    if not recommended_products.empty:
        st.dataframe(recommended_products)
    else:
        st.write("No recommendations found based on the selected products.")

    # Plot the network graph
    st.write("Network Graph of Top Association Rules:")
    plot_network_graph(rules)
