import streamlit as st
import pickle

# Load the recommendation model (rules) using pickle
with open('product_recommendation_model.pkl', 'rb') as f:
    rules_fpgrowth = pickle.load(f)

# Function to get recommendations
def get_recommendations(input_products, rules):
    recommendations = []
    
    for index, rule in rules.iterrows():
        if all(item in input_products for item in rule['antecedents']):
            recommendations.extend(list(rule['consequents']))
    
    # Remove input products from the recommendations
    recommendations = list(set(recommendations) - set(input_products))
    
    return recommendations

# Streamlit UI
st.title("Product Recommendation System Based on Basket Analysis")

# Input for product list
input_products = st.text_input("Enter product ASINs (comma-separated)", "")

if input_products:
    input_products_list = [item.strip() for item in input_products.split(',')]
    recommendations = get_recommendations(input_products_list, rules_fpgrowth)
    
    st.write("Recommended products:")
    for product in recommendations:
        st.write(product)
