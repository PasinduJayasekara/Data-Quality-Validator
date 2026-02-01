# Data-Quality-Validator
A full-stack Python tool to validate, profile, and clean CSV datasets, designed for anyone working with tabular data. 
This project automatically detects data quality issues, generates actionable suggestions, and allows users to download cleaned CSV files.

Features<br>
1.Detect missing values and duplicates<br>
2.Identify outliers using z-score method<br>
3.Column-level data profiling (data type, min, max, mean, median, unique values)<br>
4.Schema validation against a predefined structure<br>
5.Generate data cleaning suggestions<br>
6.Calculate an overall data quality score<br>
7.Clean the dataset (remove duplicates & fill missing numeric values)<br>
8.Download cleaned CSV directly from the web interface<br>

Tech Stack<br>
Backend: Python, FastAPI, Pandas, NumPy<br>
Frontend: Streamlit (web interface for file upload, validation report, and download)<br>
Server: Uvicorn (ASGI server)<br>

Installation<br>
Clone the repository:<br>
git clone https://github.com/yourusername/data-quality-validator.git<br>
cd data-quality-validator<br>

Create a virtual environment:<br>
python -m venv venv<br>
source venv/bin/activate    # Linux/macOS<br>
venv\Scripts\activate       # Windows<br>

Install dependencies:<br>
pip install -r requirements.txt<br>

Running the Project<br>
Start the backend server:<br>
uvicorn backend.main:app --reload<br>

Open the Streamlit frontend:<br>
streamlit run frontend/app.py<br>

Upload a CSV file via the web interface to:<br>
Validate data quality<br>
View detailed profiling and suggestions<br>
Download a cleaned CSV<br>

Example Workflow<br>
Upload a CSV file containing raw data.<br>
Inspect the validation report:<br>
Missing values per column<br>
Duplicate row count<br>
Outlier count per numeric column<br>
Column profiling summary<br>
Schema issues<br>
Overall data quality score<br>
Apply cleaning suggestions and download the cleaned dataset.<br>

Future Improvements<br>
Support additional file formats (Excel, JSON, Parquet)<br>
Visualize profiling data with charts<br>
