import pandas as pd
from pyxlsb import open_workbook

# geo = "e-comerce_Olist_dataset/olist_geolocation_dataset.xlsb"
# with open_workbook(geo) as wb:
#     with wb.get_sheet(1) as sheet:
#         geolocation = pd.DataFrame(sheet.rows())

orderitem = "e-comerce_Olist_dataset/olist_order_items_dataset.xlsb"
with open_workbook(orderitem) as wb:
    with wb.get_sheet(1) as sheet:
        order_items = pd.DataFrame(sheet.rows())

customers = pd.read_csv("e-comerce_Olist_dataset/olist_customers_dataset.csv")
order_payments = pd.read_csv("e-comerce_Olist_dataset/olist_order_payments_dataset.csv")
order_reviews = pd.read_csv("e-comerce_Olist_dataset/olist_order_reviews_dataset.csv")

# Para borrar columnas
# order_reviews.drop(['review_comment_title', 'review_comment_message'], axis=1, inplace=True)
# order_reviews.to_csv("e-comerce_Olist_dataset/olist_order_reviews_dataset.csv", index=False)

olistorders = "e-comerce_Olist_dataset/olist_orders_dataset.xlsb"
with open_workbook(orderitem) as wb:
    with wb.get_sheet(1) as sheet:
        orders = pd.DataFrame(sheet.rows())

orders.drop(['order_delivered_carrier_date', 'order_estimated_delivery_date'], axis=1, inplace=True)
with pd.ExcelWriter(output_file_path, engine='pyxlsb') as writer:
    orders.to_excel(writer, index=False)


products = pd.read_csv("e-comerce_Olist_dataset/olist_products_dataset.csv")
#products.drop(["product_name_lenght","product_description_lenght","product_photos_qty","product_weight_g","product_length_cm","product_height_cm","product_width_cm"], axis=1, inplace=True)
#products.to_csv("e-comerce_Olist_dataset/olist_products_dataset.csv")

# sellers = pd.read_csv("e-comerce_Olist_dataset/olist_sellers_dataset.csv")
# product_category_name_translation = pd.read_csv(
#     "e-comerce_Olist_dataset/product_category_name_translation.csv"
# )
# closed_deals = pd.read_csv("olist_Funnel_marketing/olist_closed_deals_dataset.csv")
# marketing_leads = pd.read_csv("olist_Funnel_marketing/olist_marketing_qualified_leads_dataset.csv")



# # Merge the datasets
# df = orders.merge(
#     customers, how="left", on="customer_id"
# ).merge(
#     geolocation, how="left", left_on="customer_zip_code_prefix", right_on="geolocation_zip_code_prefix"
# ).merge(
#     order_items, how="left", on="order_id"
# ).merge(
#     order_payments, how="left", on="order_id"
# ).merge(
#     order_reviews, how="left", on="order_id"
# ).merge(
#     products, how="left", on="product_id"
# ).merge(
#     sellers, how="left", on="seller_id"
# ).merge(
#     closed_deals, how="left", on="seller_id" 
# ).merge(
#     marketing_leads, how="left", on="seller_id"  
# )

# # Translate the product category names
# df["product_category_name_english"] = df["product_category_name"].map(
#     product_category_name_translation.set_index("product_category_name")["product_category_name_english"]
# )

# # Group the data by seller_id and calculate the number of orders
# df_grouped = df.groupby("seller_id")["order_id"].count()

# # Sort the data by the number of orders
# df_grouped = df_grouped.sort_values(ascending=False)

# # Get the top 10 sellers
# top_10_sellers = df_grouped.head(10)

# # Print the top 10 sellers
# print(top_10_sellers)