📦 City Hive Project

🚀 A full-stack application for processing, validating, and storing inventory data.
Built using Python, Ruby on Rails (API mode), MongoDB, and Pandas.

📂 Project Structure

city-hive-project/
│── CityHive.py               # Python script for fetching, processing, and uploading inventory data
│── storage_validation_api/   # Rails API for storing and validating inventory data
│── README.md                 # Project documentation

🛠 Installation & Setup

1️⃣ Clone the Repository

git clone https://github.com/JuliusShade/city-hive-project.git
cd city-hive-project

🐍 Python Script Setup

2️⃣ Install Python Dependencies

Ensure you have Python 3.x installed, then run:

pip install pandas requests

3️⃣ Run the Python Script

The script has three modes:

📌 Generate CSV file

python CityHive.py generate_csv

✅ Fetches inventory data, processes it, and saves a transformed CSV file.

📌 Upload Data to API

python CityHive.py upload

✅ Sends processed inventory data to the Rails API.

📌 List All Uploads

python CityHive.py list_uploads

✅ Retrieves and prints all uploaded inventory batches.

💎 Rails API Setup

4️⃣ Install Ruby & Rails

Ensure you have Ruby (3.x) and Rails (7.x or 8.x) installed.
If not, install using:

gem install rails

5️⃣ Install MongoDB

Since the Rails API uses MongoDB, install and start MongoDB:

# macOS (Homebrew)
brew install mongodb-community@6.0  

# Linux
sudo apt install mongodb  

For Windows, download from: MongoDB Official Site

Then start MongoDB:

mongod --dbpath=/data/db

6️⃣ Set Up the Rails API

cd storage_validation_api
bundle install
rails s

✅ The API will start at http://localhost:3000.

📡 API Endpoints

🔹 Upload Inventory Data

POST /inventory_uploads.jsonRequest Body (JSON):

{
  "inventory_units": [
    {
      "item_num": "123456",
      "name": "Test Product",
      "price": 19.99,
      "department": "Electronics",
      "properties": {"quantity": 10},
      "tags": ["high_margin"]
    }
  ]
}

Response:

{
  "message": "Inventory uploaded successfully",
  "batch_id": "batch_001"
}

🔹 Get Inventory Upload Summary

GET /inventory_uploads.jsonResponse:

[
  {
    "batch_id": "batch_001",
    "number_of_units": 100,
    "average_price": 25.5,
    "total_quantity": 500
  }
]

🎯 Summary

✅ Fetch inventory data from S3 and process it using Python.✅ Upload the processed data to a Rails API.✅ Store and validate inventory records in MongoDB.✅ List all uploaded inventory batches.

📌 Contributing

Fork the repository

Create a new branch (git checkout -b feature-branch)

Commit your changes (git commit -m "Added new feature")

Push the branch (git push origin feature-branch)

Submit a Pull Request! 🚀

📄 License

This project is licensed under the MIT License.

🚀 Now you're ready to run the City Hive Project! Let me know if you need any modifications. 🎉
