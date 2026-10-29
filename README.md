# 🛡️ NETGUARD AI

> **Network Threat Detection & Incident Analysis Console**  
> Powered by Machine Learning (Random Forest) trained on the UNSW-NB15 dataset.

[![Netlify Status](https://img.shields.io/badge/Netlify-Live%20Demo-37d4a2?style=for-the-badge&logo=netlify&logoColor=white)](https://netguard-ai-console.netlify.app)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Random%20Forest-orange?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Dataset](https://img.shields.io/badge/Dataset-UNSW--NB15-blueviolet?style=for-the-badge)](https://research.unsw.edu.au/projects/unsw-nb15-dataset)

---

## 🌐 Live Web Console (Netlify)
Experience the interactive NetGuard AI console deployed on Netlify:  
👉 **[https://netguard-ai-console.netlify.app](https://netguard-ai-console.netlify.app)**

---

## 📝 GitHub Repository Short Description (< 350 Chars)
Use this exact text in your GitHub repository **About / Description** field:

```text
NetGuard AI is an intelligent network intrusion detection & incident analysis console powered by Machine Learning (Random Forest) trained on the UNSW-NB15 dataset. Features real-time threat scoring, protocol profiling, XAI feature transparency, and automated incident reporting.
```
*(Character count: 278 / 350)*

---

## 🚀 Overview

**NETGUARD AI** is an end-to-end cybersecurity analytics platform engineered to ingest network flow records, classify traffic anomalies, predict malicious intrusions with high confidence, and provide incident response capabilities through an intuitive visual dashboard.

The detection core utilizes an ensemble **Random Forest Classifier** trained on the comprehensive **UNSW-NB15** network benchmark dataset across 39 distinct flow, content, and time-window features.

---

## ✨ Key Features

- **⚡ Real-Time Threat Classification**: Instantly predicts whether network flows represent benign traffic or active attack vectors.
- **🎛️ Dynamic Alert Risk Threshold**: Adjustable threshold slider (0–100%) enabling SOC analysts to tune sensitivity between high recall and high precision.
- **🚨 Priority Incident Queue**: Filtered queue sorting critical threats by risk score with deep packet parameter inspection.
- **🌐 Threat Profiling**: Breakdown of active anomalies by transport layer protocol (TCP, UDP, ARP) and network service (HTTP, DNS, FTP, SMTP, etc.).
- **🧠 Explainable AI (XAI)**: Visualizes the top 15 most important features (`ct_dst_src_ltm`, `sttl`, `ct_dst_sport_ltm`, `sbytes`, `ct_state_ttl`, etc.) for auditing and model transparency.
- **📑 Security Report Export**: One-click download of timestamped, enriched CSV threat logs for incident documentation.

---

## 📂 Repository Structure

```
NETGUARD_AI/
├── app.py                      # Main Streamlit security console dashboard
├── requirements.txt            # Python dependencies
├── REPO_DESCRIPTION.txt        # Ready-to-copy GitHub description (< 350 chars)
├── README.md                   # Project documentation
├── models/
│   └── netguard_model.pkl      # Pre-trained Random Forest model (39 features)
├── data/
│   ├── UNSW_NB15_training-set.csv   # Training dataset
│   └── UNSW_NB15_testing-set.csv    # Testing dataset
├── src/
│   ├── data_loader.py          # Data ingestion module
│   ├── check_missing_values.py # Data quality validator
│   ├── explore_data.py         # Statistical data exploration
│   ├── prepare_data.py         # Feature engineering & preprocessing
│   └── train_model.py          # Random Forest model training pipeline
└── web/                        # Netlify-hosted web application
    ├── index.html              # Interactive client-side threat console
    ├── sample_data.js          # UNSW-NB15 sample data stream
    └── netlify.toml            # Netlify deployment and headers config
```

---

## 🛠️ Local Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/NETGUARD_AI.git
cd NETGUARD_AI
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Dashboard
```bash
streamlit run app.py
```
The application will launch automatically in your browser at `http://localhost:8501`.

---

## 🧪 Training & Machine Learning Pipeline

To retrain the Random Forest model on updated traffic data:

```bash
cd src
python train_model.py
```

### Model Performance Metrics:
- **Algorithm**: Random Forest Classifier (100 estimators, parallelized)
- **Features Analyzed**: 39 network flow attributes
- **Target**: Binary classification (`0`: Normal, `1`: Attack)
- **Top Predictive Features**:
  1. `ct_dst_src_ltm` (Connection density between source/destination)
  2. `sttl` (Source-to-destination Time To Live)
  3. `ct_dst_sport_ltm` (Destination-to-source port connection count)
  4. `sbytes` (Source transaction bytes)
  5. `ct_state_ttl` (State to TTL correlation)

---

## ☁️ Deployment

### Netlify Deployment
The `web/` directory contains the production-ready web console:
```bash
netlify deploy --dir web --prod
```
Live URL: **[https://netguard-ai-console.netlify.app](https://netguard-ai-console.netlify.app)**

---

## 📄 License
This project is open-source under the MIT License.

