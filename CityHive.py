import requests
import pandas as pd
import json
import io
import sys

# File paths - Insert your own respective file paths
local_file_path = r"C:\Users\shade\OneDrive\Documents\DevProject\inventory_export_sample_exercise.csv"
output_csv_path = r"C:\Users\shade\OneDrive\Documents\DevProject\transformed_output.csv"

# API Endpoints
API_BASE_URL = "http://localhost:3000"
UPLOAD_ENDPOINT = f"{API_BASE_URL}/inventory_uploads.json"

# S3 details
s3_bucket = "cityhive-stores"
region = "us-west-2"
object_key = "_utils/inventory_export_sample_exercise.csv"
s3_url = f"https://{s3_bucket}.s3.{region}.amazonaws.com/{object_key}"

# Function to fetch data from S3 and parse it into a DataFrame
def fetch_and_transform_data():
    response = requests.get(s3_url, stream=True)
    if response.status_code != 200:
        print(f"Failed to download file. HTTP Status Code: {response.status_code}")
        sys.exit(1)

    # Read the file into memory and parse into a DataFrame
    df = pd.read_csv(io.StringIO(response.content.decode('utf-8')), delimiter='|')

    # Remove the second row
    df = df.drop(index=1)

    # Add a department column using 'Dept_ID' with capitalization formatting
    df['Department'] = df['Dept_ID'].astype(str).str.title()

    # Check if 'ItemNum' is not greater than 5 characters, move values to 'internal_id' and blank 'ItemNum'
    if any(df['ItemNum'].astype(str).apply(lambda x: not x.isdigit() or len(x) <= 5)):
        df['internal_id'] = df['ItemNum'].apply(lambda x: f"biz_id_{x}")
        df['ItemNum'] = ''
    
    # Adjust Price Based on Margin
    df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Margin'] = (df['Price'] - df['Cost']) / df['Cost']
    df['Adjusted_Price'] = df.apply(lambda row: round(row['Price'] * 1.07, 2) if row['Margin'] > 0.3 else round(row['Price'] * 1.09, 2), axis=1)
    
    # Replace 'Price' column with 'Adjusted_Price' values and drop 'Adjusted_Price'
    df['Price'] = df['Adjusted_Price']
    df.drop(columns=['Adjusted_Price'], inplace=True)

    # Add a 'Name' column concatenating 'ItemName' and 'ItemName_Extra'
    df['Name'] = df[['ItemName', 'ItemName_Extra']].fillna('').agg(' '.join, axis=1).str.strip()

    # Filter only items sold during 2020
    df = df[df['Last_Sold'].astype(str).str.contains("2020", na=False)]

    # Add a 'Properties' column containing a JSON dict with department, vendor, and description
    df['Properties'] = df.apply(lambda row: json.dumps({
        "department": row['Department'],
        "vendor": row['ItemName_Extra'],
        "description": row['ItemName']
    }), axis=1)

    # Determine which column to use for duplicate_sku check
    sku_column = 'ItemNum' if df['ItemNum'].str.strip().any() else 'internal_id'

    # Add a 'Tags' field
    duplicate_counts = df[sku_column].value_counts()
    df['Tags'] = df.apply(lambda row: ",".join(filter(None, [
        "duplicate_sku" if duplicate_counts[row[sku_column]] > 1 else "",
        "high_margin" if row['Margin'] > 0.3 else "low_margin"
    ])), axis=1)

    return df

# Function to generate CSV file
def generate_csv():
    df = fetch_and_transform_data()
    df.to_csv(output_csv_path, index=False, encoding='utf-8')
    print(f"Transformed data saved to {output_csv_path}")

# Function to upload JSON data to the API
def upload_data():
    df = fetch_and_transform_data()
    
    # Prepare JSON payload
    inventory_data = df[["ItemNum", "Name", "Price", "Department", "Properties", "Tags"]].rename(
        columns={"ItemNum": "item_num", "Name": "name", "Price": "price", "Department": "department", "Properties": "properties", "Tags": "tags"}
    ).to_dict(orient="records")

    payload = {"inventory_units": inventory_data}

    response = requests.post(UPLOAD_ENDPOINT, json=payload, headers={"Content-Type": "application/json"})

    if response.status_code == 201:
        print(f"Successfully uploaded inventory batch: {response.json()}")
    else:
        print(f"Failed to upload inventory. Status Code: {response.status_code}, Response: {response.text}")

# Function to list all inventory uploads
def list_uploads():
    response = requests.get(UPLOAD_ENDPOINT, headers={"Accept": "application/json"})

    if response.status_code == 200:
        print("Inventory Uploads:")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Failed to retrieve inventory uploads. Status Code: {response.status_code}, Response: {response.text}")

# Entry point for the script
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <generate_csv|upload|list_uploads>")
        sys.exit(1)

    action = sys.argv[1].lower()

    if action == "generate_csv":
        generate_csv()
    elif action == "upload":
        upload_data()
    elif action == "list_uploads":
        list_uploads()
    else:
        print("Invalid argument. Use one of: generate_csv, upload, list_uploads")
        