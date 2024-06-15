# 🌊 Marine Species Population Dynamics Prediction Platform

## Project Overview
With the acceleration of globalization and human activities, marine ecosystems are facing unprecedented pressure. To address this ecological crisis and promote the conservation and sustainable development of marine biodiversity, we have developed a Marine Species Population Dynamics Prediction Platform based on relational database technology. This platform aims to provide researchers, policymakers, and the public with a comprehensive service that integrates data filtering, querying, evaluation, and prediction.

## 📷 Screenshots
### Home Page
![Home Page](https://github.com/WinstonLiyt/OceanBioDynamicsHub/assets/104308117/b78d8342-04f9-469b-ab32-4112347b8ed5)

###  Business Process Flow Diagram
![Business Process Flow Diagram](https://github.com/WinstonLiyt/OceanBioDynamicsHub/assets/104308117/17aca435-e2c0-4794-ad23-464394243531)

### Entity-Relationship Diagram (ER Diagram)
![ER Diagram](https://github.com/WinstonLiyt/OceanBioDynamicsHub/assets/104308117/bbd6d2ee-c341-43c4-8022-67bc747d3ffb)

## 🌟 Core Features
### 🐠 Data Management
- **Data Collection & Input**: Supports diverse data sources, including biological records, measurements, datasets, accepted species, and sequences. Administrators can input and update key ecological data.
- **Data Maintenance & Cleaning**: Regular updates and validation ensure data accuracy and timeliness.
- **Data Access Control**: Role-based access management ensures secure data storage and access.

### 📊 Data Analysis & Visualization
- **Data Filtering & Search**: Researchers can filter and search data based on various criteria.
- **Trend Analysis**: Utilize statistical and deep learning techniques to analyze changes in marine species populations.
- **Data Visualization**: Use AMap (Gaode) API for visual representation of species' geographical locations.

### 🌐 User Interaction & Feedback
- **Query Interface**: Users can query specific species information.
- **User Feedback**: Users can evaluate and rate marine species, enhancing platform interactivity and educational value.
- **Education & Awareness**: Publish news on endangered species and extreme marine environments to raise public awareness.

### 👨‍🔬 Scientist-Specific Features
- **Research Prediction**: Scientists can input parameters for time-series predictions using an LSTM model, and view results as charts for further research and publication.

### 🔧 Admin-Specific Features
- **Permission Management**: Administrators can manage user accounts, including enabling/disabling accounts and upgrading/downgrading roles.
- **Content Management**: Admins can review, edit, or delete posts and manage marine data.

## 🛠️ Technology Stack
- **Frontend**: Vue.js, Element UI
- **Backend**: Flask, MySQL
- **Data Visualization**: AMap (Gaode) API
- **Tools**: PyCharm, HBuilder X, Navicat Premium

## 🚀 Getting Started
### Prerequisites
- Node.js
- Python 3.8
- MySQL 8.0

### Installation
1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-repo/marine-prediction-platform.git
    cd marine-prediction-platform
    ```

2. **Backend Setup**:
    - Navigate to the backend directory:
        ```bash
        cd backend
        ```
    - Install dependencies:
        ```bash
        pip install -r requirements.txt
        ```
    - Set up the database:
        ```bash
        mysql -u root -p < sea.sql
        ```
    - Run the backend server:
        ```bash
        python app.py
        ```

3. **Frontend Setup**:
    - Navigate to the frontend directory:
        ```bash
        cd ../frontend
        ```
    - Install dependencies:
        ```bash
        npm install
        ```
    - Run the frontend server:
        ```bash
        npm run serve
        ```

4. **Access the Platform**:
    Open your browser and go to `http://localhost:10001/` to start using the Marine Species Population Dynamics Prediction Platform.

## 🧑‍💻 Contributing
Welcome to make contributions to enhance the platform. Please fork the repository and submit pull requests for review.

## 📝 License
This project is licensed under the MIT License. See the `LICENSE` file for details.
