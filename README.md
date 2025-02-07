📦 City Hive Project
🚀 A full-stack application for processing, validating, and storing inventory data.
Built using Python, Ruby on Rails (API mode), MongoDB, and Pandas.

📂 Project Structure
graphql
Copy
Edit
city-hive-project/
│── CityHive.py               # Python script for fetching, processing, and uploading inventory data
│── storage_validation_api/   # Rails API for storing and validating inventory data
│── README.md                 # This file
🛠 Installation & Setup
1️⃣ Clone the Repository
sh
Copy
Edit
git clone https://github.com/JuliusShade/city-hive-project.git
cd city-hive-project
🐍 Python Script Setup
2️⃣ Install Python Dependencies
Ensure you have Python 3.x installed, then run:

sh
Copy
Edit
pip install pandas requests
3️⃣ Run the Python Script
The script has three modes:

Generate CSV file

sh
Copy
Edit
python CityHive.py generate_csv
✅ Fetches inventory data, processes it, and saves a transformed CSV file.

Upload Data to API

sh
Copy
Edit
python CityHive.py upload
✅ Sends processed inventory data to the Rails API.

List All Uploads

sh
Copy
Edit
python CityHive.py list_uploads
✅ Retrieves and prints all uploaded inventory batches.

💎 Rails API Setup
4️⃣ Install Ruby & Rails
Ensure you have Ruby (3.x) and Rails (7.x or 8.x) installed.
If not, install using:

sh
Copy
Edit
gem install rails
5️⃣ Install MongoDB
Since the Rails API uses MongoDB, install and start MongoDB:

sh
Copy
Edit
brew install mongodb-community@6.0  # macOS (Homebrew)
sudo apt install mongodb            # Linux
For Windows, download from: MongoDB Official Site

Then start MongoDB:

sh
Copy
Edit
mongod --dbpath=/data/db
6️⃣ Set Up the Rails API
sh
Copy
Edit
cd storage_validation_api
bundle install
rails s
✅ The API will start at http://localhost:3000.

📡 API Endpoints
🔹 Upload Inventory Data
POST /inventory_uploads.json
Request Body (JSON):

json
Copy
Edit
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

json
Copy
Edit
{
  "message": "Inventory uploaded successfully",
  "batch_id": "batch_001"
}
🔹 Get Inventory Upload Summary
GET /inventory_uploads.json
Response:

json
Copy
Edit
[
  {
    "batch_id": "batch_001",
    "number_of_units": 100,
    "average_price": 25.5,
    "total_quantity": 500
  }
]
🎯 Summary
✅ Fetch inventory data from S3 and process it using Python.
✅ Upload the processed data to a Rails API.
✅ Store and validate inventory records in MongoDB.
✅ List all uploaded inventory batches.

📌 Contributing
Fork the repository
Create a new branch (git checkout -b feature-branch)
Commit your changes (git commit -m "Added new feature")
Push the branch (git push origin feature-branch)
Submit a Pull Request! 🚀
📄 License
This project is licensed under the MIT License.
