## 🚀 Live Demo
👉 [https://smart-sales-analytics.streamlit.app](https://smart-sales-analytics-xbjhl3hehextqwpbdpv4qv.streamlit.app/)



# 📊 Smart Sales Analytics & Revenue Forecasting Platform

An end-to-end enterprise-grade sales analytics system that performs real-time business intelligence and machine-learning-based revenue forecasting using MySQL/PostgreSQL, Python, SQL, and Streamlit.

This project simulates how real companies build internal analytics products for management-level decision making.

---

## 🚀 Key Features

### Business Analytics (BI)
- Monthly revenue trend analysis
- Category-wise revenue performance
- Customer segmentation by city
- Product-wise profitability analysis
- Executive KPI cards (Revenue, Customers, Categories)

### Machine Learning
- Revenue forecasting using Linear Regression
- Trained model saved and reused (.pkl)
- Interactive prediction via dashboard

### Interactive Dashboard
- Clean, professional UI
- Filters by city and product category
- Live database-driven analytics
- Web-based Streamlit application

---

## 🛠 Tech Stack
- Python 3.10+
- MySQL or PostgreSQL
- SQLAlchemy
- Pandas
- scikit-learn
- Streamlit
- Git & GitHub

---

## 📁 Project Structure

Smart-Sales-Analytics/
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
│
├── data/
│
├── scripts/
│   ├── db_connect.py
│   ├── load_data.py
│   └── kpi_analysis.py
│
├── model/
│   ├── train_model.py
│   ├── predict.py
│   └── revenue_model.pkl
│
└── .venv/

---

## 📋 Prerequisites
- Python 3.10+
- MySQL 8+ or PostgreSQL 13+
- pip
- Git

---

## ⚙️ Installation & Setup

### Clone Repository
git clone https://github.com/yourusername/smart-sales-analytics.git
cd smart-sales-analytics

### Create Virtual Environment
python -m venv .venv
.venv\Scripts\activate

### Install Dependencies
pip install -r requirements.txt

### Configure Database URL
Set `DB_URL` as an environment variable (preferred):

PowerShell:
setx DB_URL "mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/demo"

Or set it in `.streamlit/secrets.toml`:

DB_URL="mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/demo"

PostgreSQL example:

DB_URL="postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/demo"

For Supabase pooling connections (PostgreSQL), use the exact pooler credentials from Supabase:
- Host: `aws-<region>.pooler.supabase.com`
- Port: usually `6543`
- User: `postgres.<project_ref>`
- Password: your database password
- Include SSL (`?sslmode=require` or equivalent)

---

## 🗄 MySQL Setup (Recommended)

CREATE DATABASE demo;
USE demo;

CREATE TABLE customers (
  customer_id INT PRIMARY KEY,
  name VARCHAR(50),
  city VARCHAR(50),
  age INT
);

CREATE TABLE products (
  product_id INT PRIMARY KEY,
  product_name VARCHAR(50),
  categoty VARCHAR(50),
  price DECIMAL(10,2)
);

CREATE TABLE sales (
  sale_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT,
  product_id INT,
  quantity INT,
  sale_date DATE,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

---

## Optional PostgreSQL Setup

CREATE DATABASE demo;

CREATE TABLE customers (
  customer_id INT PRIMARY KEY,
  name VARCHAR(50),
  city VARCHAR(50),
  age INT
);

CREATE TABLE products (
  product_id INT PRIMARY KEY,
  product_name VARCHAR(50),
  categoty VARCHAR(50),
  price NUMERIC(10,2)
);

CREATE TABLE sales (
  sale_id SERIAL PRIMARY KEY,
  customer_id INT REFERENCES customers(customer_id),
  product_id INT REFERENCES products(product_id),
  quantity INT,
  sale_date DATE
);

---

## Load Sample Data
python scripts/load_data.py

---

## Train Model
python model/train_model.py

---

## Run Dashboard
streamlit run app.py

Open browser: http://localhost:8501

---

## License
MIT License

---

## Author
Harish Uta
