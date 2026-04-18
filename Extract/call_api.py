import os
import json
import time
import logging
import requests
from typing import Dict, List, Optional
import datetime
from dotenv import load_dotenv
import pandas as pd


# Load environment variables from .env file
load_dotenv()


class APIClient:
    """A client for making API calls to the specified endpoint."""

    def __init__(self, restaurant_id: str):
        self.restaurant_id = restaurant_id
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        os.makedirs(self.data_dir, exist_ok=True)
        self.base_url = "https://api.fu.do/v1alpha1"
        self.auth_url = "https://auth.fu.do/api"
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
            "Content-Type": "application/json"
        }
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
        self.logger = logging.getLogger(__name__)
        self.logger.info("API Client initialized with base URL: %s", self.base_url)

    def get_token(self):
        """Get token from auth endpoint
        Returns: 
            self.token: The authentication token
        """
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        payload = {"apiKey": self.api_key, "apiSecret": self.api_secret}
        try:
            response = requests.post(self.auth_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            token = response.json().get("token")
            if not token:
                raise ValueError("Token not found in auth response")
            self.token = token
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Authentication failed: {e}")
            raise

    def get_sales(self, sale_date: datetime):
        """Gets a days worth of sales from the API. From that day 7AM UTC to next day 6.59AM UTC
        Args:
            sale_date: The date of the sales to get
        Returns:
            List of sales
        """
        has_data = True
        self.json_data = []
        page = 0
        end_date_plusone = sale_date + datetime.timedelta(days=1)
        date_filter = f"and(gte.{sale_date}T07:00:00Z,lte.{end_date_plusone}T06:59:59Z)"
        headers = {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}
        self.filename = f"{self.restaurant_id}_{sale_date}"

        while has_data:
            page += 1
            params = {
                "filter[createdAt]": date_filter,
                "include": "items,items.product,items.product.productCategory,items.subitems,payments,payments.paymentMethod,discounts,customer", # "items,items.product,items.product.productCategory,items.subitems,payments,payments.paymentMethod,discounts,customer"
                "page[size]": 500,
                "page[number]": page
            }
            try:
                response = requests.get(f"{self.base_url}/sales", headers=headers, params=params, timeout=60)
                response.raise_for_status()

            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error fetching sales page {page}: {e}")
                return None

            if response.json().get("data") == []:
                has_data = False
                return

            self.json_data.append(response.json())
            
        
    
    def filter_json(self):
        self.sales = []
        self.included = []

        for json_data in self.json_data:
            self.sales.extend(json_data.get("data", []))
            self.included.extend(json_data.get("included", []))

        
        self.sales_filtered = [{k: v for k, v in sale.items() if k != 'relationships'} for sale in self.sales]
        self.items = [item for item in self.included if item['type'] == 'Item']
        self.discounts = [discount for discount in self.included if discount['type'] == 'Discount']
        self.payments = [payment for payment in self.included if payment['type'] == 'Payment']
        self.customers = [customer for customer in self.included if customer['type'] == 'Customer'] 
        self.products = [product for product in self.included if product['type'] == 'Product']
        self.product_categories = [product_category for product_category in self.included if product_category['type'] == 'ProductCategory']
        self.subitems = [subitem for subitem in self.included if subitem['type'] == 'Subitem']
        self.payment_methods = [payment_method for payment_method in self.included if payment_method['type'] == 'PaymentMethod']



    def save_to_local_file(self):
        """Saves data to a local file
        Args:
            data: The data to save
        """
        try:
            with open(os.path.join(self.data_dir, "json_raw_" + self.filename + ".json"), "w") as f:
                json.dump(self.json_data, f, indent=4)
            self.logger.info(f"Data saved to json_raw_{self.filename}.json")
        except Exception as e:
            self.logger.error(f"Error saving data to json_raw_{self.filename}.json: {e}")

    def create_dataframe(self):
        self.df_sales = pd.json_normalize(self.sales_filtered)
        self.df_items = pd.json_normalize(self.items)
        self.df_discounts = pd.json_normalize(self.discounts)
        self.df_payments = pd.json_normalize(self.payments)
        self.df_customers = pd.json_normalize(self.customers)
        self.df_products = pd.json_normalize(self.products)
        self.df_product_categories = pd.json_normalize(self.product_categories)
        self.df_subitems = pd.json_normalize(self.subitems)
        self.df_payment_methods = pd.json_normalize(self.payment_methods)
        

    def save_df_to_local_file(self):
        """Saves data to a local file
        Args:
            data: The data to save
        """
        self.df_sales.to_csv(os.path.join(self.data_dir, "sales_" + self.filename + ".csv"), index=False)
        self.df_items.to_csv(os.path.join(self.data_dir, "items_" + self.filename + ".csv"), index=False)
        self.df_discounts.to_csv(os.path.join(self.data_dir, "discounts_" + self.filename + ".csv"), index=False)
        self.df_payments.to_csv(os.path.join(self.data_dir, "payments_" + self.filename + ".csv"), index=False)
        self.df_customers.to_csv(os.path.join(self.data_dir, "customers_" + self.filename + ".csv"), index=False)
        self.df_products.to_csv(os.path.join(self.data_dir, "products_" + self.filename + ".csv"), index=False)
        self.df_product_categories.to_csv(os.path.join(self.data_dir, "product_categories_" + self.filename + ".csv"), index=False)
        self.df_subitems.to_csv(os.path.join(self.data_dir, "subitems_" + self.filename + ".csv"), index=False)
        self.df_payment_methods.to_csv(os.path.join(self.data_dir, "payment_methods_" + self.filename + ".csv"), index=False)
        self.logger.info(f"Data saved to csv files")

if __name__ == "__main__":
    api_client = APIClient("Ike")
    print(api_client.data_dir)

    api_client.get_token()

    api_client.get_sales(datetime.date(2026, 3, 22))
    api_client.filter_json()
    api_client.save_to_local_file()
    api_client.create_dataframe()
    api_client.save_df_to_local_file()
