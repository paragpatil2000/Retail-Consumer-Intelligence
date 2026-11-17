# Retail Consumer Intelligence Platform

An end-to-end Data Science project for retail analytics, consumer behavior analysis, and business intelligence.

## Overview

The Retail Consumer Intelligence Platform is a data-driven project inspired by real-world retail analytics and market research workflows. It uses synthetic retail data to explore sales performance, customer purchasing behavior, product associations, promotion effectiveness, and sales forecasting.

The platform combines Python-based analytics, machine learning, a SQL database, a Power BI dashboard, and a REST API to demonstrate an end-to-end analytics workflow.

## Key Features

- **Sales Analytics:** Analyze sales revenue, transactions, units sold, and average transaction value.
- **Sales Forecasting:** Generate sales predictions using machine learning models.
- **Customer Segmentation:** Group customers using RFM-based behavioral analysis.
- **Market Basket Analysis:** Identify product associations and generate product recommendations.
- **Promotion Effectiveness:** Compare sales performance for promotional and non-promotional transactions.
- **Interactive Dashboard:** Explore retail KPIs and business insights using Power BI.
- **REST API:** Access analytics through FastAPI endpoints.
- **Containerization:** Package the API using Docker and deploy it on Render.

## Technology Stack

- **Programming:** Python, SQL
- **Data Analysis:** Pandas, NumPy
- **Machine Learning:** Scikit-learn
- **API Development:** FastAPI, Uvicorn
- **Database:** SQLite
- **Business Intelligence:** Power BI
- **Deployment:** Docker, Docker Hub, Render
- **Version Control:** Git, GitHub

## Project Modules

1. Synthetic Data Generation
2. Data Preprocessing and Feature Engineering
3. Sales Analytics
4. Sales Forecasting
5. Customer Segmentation
6. Market Basket Analysis
7. Promotion Effectiveness Analysis
8. Power BI Dashboard
9. FastAPI REST API
10. Docker-based Deployment

## System Architecture

```
flowchart TD
    A[Synthetic Retail Data] --> B[Data Preprocessing]
    B --> C[SQLite Database]
    C --> D[Python Analytics and ML]
    D --> E[FastAPI REST API]
    D --> F[Power BI Dashboard]
    E --> G[Docker Container]
    G --> H[Docker Hub]
    H --> I[Render Deployment]
    I --> J[Live API Documentation]
```


## Live Demo

- **Live API:** https://retail-consumer-intelligence-api.onrender.com
- **API Documentation (Swagger):** https://retail-consumer-intelligence-api.onrender.com/docs
- **Docker Hub:** https://hub.docker.com/r/paragpatil2000/retail-consumer-intelligence

## API Endpoints

| Endpoint | Description |
|---|---|
| `/health` | Check API health |
| `/sales/summary` | Retrieve sales KPIs |
| `/products/top` | Retrieve top-selling products |
| `/customers/segments` | Retrieve customer segment summaries |
| `/promotions/effectiveness` | Compare promotion performance |
| `/forecast` | Retrieve sales forecast results |
| `/recommendations/{product_id}` | Retrieve product recommendations |

## Dataset

The project uses synthetically generated retail data, including customers, products, stores, promotions, calendar dates, and transactions.

| Dataset | Records |
|---|---:|
| Customers | 100,000 |
| Products | 500 |
| Stores | 50 |
| Promotions | 100 |
| Calendar | 1,096 |
| Transactions | 1,000,000 |

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/paragpatil2000/Retail-Consumer-Intelligence.git
cd Retail-Consumer-Intelligence
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
uvicorn api.main:app --reload
```

Open http://127.0.0.1:8000/docs to explore the API locally.

## Future Improvements

- Improve sales forecasting accuracy through time-series validation and model comparison.
- Refine product recommendations using more meaningful product associations.
- Add automated data-quality checks and monitoring.
- Enhance dashboard interactivity and business insights.

## Disclaimer

This project uses synthetic data for demonstration and portfolio purposes. Its results should not be interpreted as actual retail market findings.