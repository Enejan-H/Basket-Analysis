import streamlit as st
import pandas as pd
import pickle
import os  # Import os module for handling file paths

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

# Streamlit UI
st.title("Product Recommendation Based On Basket-Analysis")

# Page selection
page = st.sidebar.selectbox("Select Page", ["eBay", "Walmart", "Order Report"])

if page == "eBay":

    # Display the image
    st.image(os.path.join('images', 'ebay.png'), caption='', use_column_width=True)

    
    # Load models and data
    ebay_apriori_model = load_model(os.path.join('models','product_recommendation_model_ebay_apriori.pkl'))
    
    ebay_fpgrowth_model = load_model(os.path.join('models', 'product_recommendation_model_ebay_fp-growth.pkl'))
    
    ebay_data = load_data(os.path.join('data', 'eBay _Order_final.csv'))

    method = st.radio("Choose method", ("Apriori", "FP-Growth"))
    rules = ebay_apriori_model if method == "Apriori" else ebay_fpgrowth_model

    input_products = st.text_input("Enter Item Number (comma-separated)", "")
    if input_products:
        input_products_list = [item.strip() for item in input_products.split(',')]
        
        st.write("You entered the following products:")
        input_products_df = ebay_data[ebay_data['Item Number'].isin(input_products_list)].drop_duplicates(subset=['Item Number'])
        if not input_products_df.empty:
            for index, row in input_products_df.iterrows():
                st.write(f"{row['Item Number']}: {row['Item Title']}")
        else:
            st.write("No matching products found for the entered Item Number.")
        
        recommended_products = get_recommendations(input_products_list, rules, ebay_data, 'Item Number', 'Item Title')
        st.write("Top 5 Recommended products:")
        if not recommended_products.empty:
            st.dataframe(recommended_products)
        else:
            st.write("No recommendations found based on the entered products.")

elif page == "Walmart":
    
    # Display the image
    st.image(os.path.join('images', 'walmart.jpg'), caption='', use_column_width=True)

    # Load models and data
    walmart_apriori_model = load_model(os.path.join('models', 'product_recommendation_model_walmart_aprior.pkl'))
                                       
    walmart_fpgrowth_model = load_model(os.path.join('models', 'product_recommendation_model_walmart_fp-growth.pkl'))
                                        
    walmart_data = load_data(os.path.join('data', 'Walmart_Final_merged.csv'))

    method = st.radio("Choose method", ("Apriori", "FP-Growth"))
    rules = walmart_apriori_model if method == "Apriori" else walmart_fpgrowth_model

    input_products = st.text_input("Enter product SKUs (comma-separated)", "")
    if input_products:
        input_products_list = [item.strip() for item in input_products.split(',')]
        
        st.write("You entered the following products:")
        input_products_df = walmart_data[walmart_data['SKU'].isin(input_products_list)].drop_duplicates(subset=['SKU'])
        if not input_products_df.empty:
            for index, row in input_products_df.iterrows():
                st.write(f"{row['SKU']}: {row['Item_Description']}")
        else:
            st.write("No matching products found for the entered SKUs.")
        
        recommended_products = get_recommendations(input_products_list, rules, walmart_data, 'SKU', 'Item_Description')
        st.write("Top 5 Recommended products:")
        if not recommended_products.empty:
            st.dataframe(recommended_products)
        else:
            st.write("No recommendations found based on the entered products.")

elif page == "Order Report":
   
 # Display the image
    st.image(os.path.join('images', 'emsbay.jpg'), caption='', use_column_width=True)

    # Load models and data
    order_report_apriori_model = load_model(os.path.join('models', 'product_recommendation_model_order_apriori.pkl'))
    order_report_fpgrowth_model = load_model(os.path.join('models', 'product_recommendation_model_order_fp-growth.pkl'))
    order_report_data = load_data(os.path.join('data', 'order_report_final.csv'))

    method = st.radio("Choose method", ("Apriori", "FP-Growth"))
    rules = order_report_apriori_model if method == "Apriori" else order_report_fpgrowth_model

    input_products = st.text_input("Enter product ASINs (comma-separated)", "")
    if input_products:
        input_products_list = [item.strip() for item in input_products.split(',')]
        
        st.write("You entered the following products:")
        input_products_df = order_report_data[order_report_data['asin'].isin(input_products_list)].drop_duplicates(subset=['asin'])
        if not input_products_df.empty:
            for index, row in input_products_df.iterrows():
                st.write(f"{row['asin']}: {row['product']}")
        else:
            st.write("No matching products found for the entered ASINs.")
        
        recommended_products = get_recommendations(input_products_list, rules, order_report_data, 'asin', 'product')
        st.write("Top 5 Recommended products:")
        if not recommended_products.empty:
            st.dataframe(recommended_products)
        else:
            st.write("No recommendations found based on the entered products.")
