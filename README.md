# 🌬️ Air Quality Prediction

[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-yes-blue)](https://www.docker.com/)
[![MLflow](https://img.shields.io/badge/MLflow-enabled-brightgreen)](https://mlflow.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Predict air quality in Beijing using **machine learning** and **deep learning** techniques. This project demonstrates the full **MLOps lifecycle**, from data exploration and preprocessing to modeling, deployment, tracking, and monitoring.

Air pollution is a pressing concern in urban areas. This project predicts **PM2.5 levels** and other air quality metrics using the historical **Beijing Air Quality Dataset** from Kaggle. The workflow includes data exploration, cleaning, feature engineering, model training, deployment, experiment tracking, and real-time monitoring.

## 🚀 Project Overview

The main goals of this project are:

- Analyze air quality trends in Beijing and uncover seasonal and pollutant patterns.
- Build predictive models to forecast PM2.5 levels using **XGBoost**, **LightGBM**, **LSTM**, and **BiLSTM**.
- Track experiments and model performance using **MLflow** with a **PostgreSQL** backend.
- Deploy the models using **Docker** and maintain CI/CD pipelines for automated updates.
- Monitor model performance and system health with **Prometheus** and **Grafana**.

## 🌟 Features

- **Exploratory Data Analysis (EDA)**: Visualize trends, correlations, and seasonal effects.
- **Data Preprocessing & Cleaning**: Handle missing data, normalize features, and engineer meaningful features.
- **Predictive Modeling**:
  - Tree-based models: XGBoost, LightGBM
  - Sequence models: LSTM, BiLSTM
- **Experiment Tracking**: Track model versions, hyperparameters, and performance metrics in MLflow.
- **Deployment & CI/CD**: Containerized deployment using Docker with automated CI/CD pipelines.
- **Monitoring & Alerts**: Real-time monitoring using Prometheus and dashboards in Grafana.

## 📊 Screenshots

### MLflow Experiment Tracking
![MLflow Screenshot](path/to/mlflow_screenshot.png)

### Prometheus Metrics Collection
![Prometheus Screenshot](path/to/prometheus_screenshot.png)

### Grafana Dashboard
![Grafana Screenshot](path/to/grafana_screenshot.png)


## 🛠️ Tech Stack

| Layer               | Tools & Frameworks                               |
|--------------------|-------------------------------------------------|
| Data Processing     | Python, Pandas, NumPy, Scikit-learn           |
| Modeling            | XGBoost, LightGBM, TensorFlow/Keras (LSTM, BiLSTM) |
| Experiment Tracking | MLflow, PostgreSQL                             |
| Deployment          | Docker, CI/CD (GitHub Actions / Jenkins)      |
| Monitoring          | Prometheus, Grafana                            |

## ⚡ Installation & Setup

1. **Clone the repository**  
   Clone the project repository and navigate into the project folder:

   ```bash
   git clone https://github.com/yourusername/air-quality-prediction.git
   cd air-quality-prediction

2. **Install dependencies**
   Install all required Python packages using pip:
    
    ```bash
    pip install -r requirements.txt

3. **Run Docker containers**
   Build and start all services using Docker Compose:

   
    ```bash
    docker-compose up --build
   
4. **Access services**  
   Open the following URLs in your browser to access the dashboards:

   - MLflow UI: [http://localhost:5000](http://localhost:5000)  
   - Prometheus: [http://localhost:9090](http://localhost:9090)  
   - Grafana: [http://localhost:3000](http://localhost:3000)


