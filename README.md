# 🔍 Fraud Detection System

A machine learning project to detect fraudulent credit card transactions using Random Forest classification on 284,807 real transactions.

---

## 📌 About the Project

Credit card fraud is a major problem where customers get charged for purchases they never made. This project builds a system that automatically identifies fraudulent transactions using machine learning and SQL analytics.

The biggest challenge was the severe class imbalance — only 492 out of 284,807 transactions were fraud (0.17%). A naive model could get 99.83% accuracy by predicting everything as legitimate, while catching zero fraud. So I focused on **Recall** and **ROC-AUC** as my key metrics instead of accuracy.

---

## 📊 Results

| Metric | Value |
|--------|-------|
| ROC-AUC Score | **0.9766** |
| Frauds Caught (True Positive) | **81/98 (83%)** |
| Legitimate Correctly Identified | **56,846** |
| False Alarms (False Positive) | **18** |
| Missed Frauds (False Negative) | **17** |

---

## 🔑 Key Findings

- **V14, V10, V12** were the top 3 most important features for fraud detection
- **Amount and Time were NOT in top 10 features** — fraud cannot be detected by transaction amount alone
- **Fraud peaks at 2-4am** when customers are less likely to notice suspicious activity
- **Transactions below ₹10** show high fraud rates — typical card testing behavior where fraudsters verify stolen cards with tiny amounts first
- **Transactions above ₹500** show the highest fraud rate (0.37%) — fraudsters quickly escalate to large purchases after verifying the card works
- Top 3 features (V14, V10, V12) alone account for **over 40% of all model decisions**

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python |
| ML Model | Scikit-learn (RandomForestClassifier) |
| Data Processing | Pandas, NumPy |
| Preprocessing | StandardScaler, train_test_split |
| Visualization | Matplotlib, Seaborn |
| Database | SQLite3 |
| Model Saving | Joblib |
| Metrics | ROC-AUC, Confusion Matrix, Classification Report |

---

## 📁 Project Structure

```
fraud-detection-system/
├── notebooks/
│   ├── 01_data_exploration.ipynb    # EDA, visualizations, preprocessing
│   ├── 02_model_training.ipynb      # Model training and evaluation
│   └── 03_sql_analysis.ipynb        # SQL fraud pattern analysis
├── reports/
│   ├── class_distribution.png       # Class imbalance visualization
│   ├── amount_distribution.png      # Fraud vs legitimate amounts
│   ├── time_distribution.png        # Transactions over time
│   ├── confusion_matrix.png         # Model evaluation
│   ├── roc_curve.png                # ROC curve (AUC = 0.9766)
│   └── feature_importance.png       # Top 10 features
├── model/
│   ├── fraud_detection_model.pkl    # Saved trained model
│   └── scaler.pkl                   # Saved StandardScaler
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

**1. Clone the repository:**
```bash
git clone https://github.com/anshikag3006/fraud-detection-system.git
cd fraud-detection-system
```

**2. Install required libraries:**
```bash
pip install pandas numpy matplotlib seaborn scikit-learn joblib
```

**3. Download the dataset:**
- Download `creditcard.csv` from [Kaggle Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
- Place it in the root project folder (not committed due to file size)

**4. Run notebooks in order:**
```
01_data_exploration.ipynb   → EDA and preprocessing
02_model_training.ipynb     → Train and evaluate model
03_sql_analysis.ipynb       → SQL pattern analysis
```

---

## 📂 Dataset

| Property | Value |
|----------|-------|
| Source | [Kaggle Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) |
| Total Transactions | 284,807 |
| Fraud Cases | 492 (0.17%) |
| Legitimate Cases | 284,315 (99.83%) |
| Time Period | 2 days (September 2013) |
| Features | 30 (Time, Amount, V1-V28 via PCA transformation) |

> ⚠️ Note: V1-V28 are PCA transformed features due to confidentiality. Original feature names are not available.

---

## 🧠 Why Random Forest?

- Handles class imbalance well with `class_weight='balanced'`
- Works well on large datasets (284K+ transactions)
- Provides feature importance scores
- Resistant to overfitting compared to single decision trees
- 100 trees voting together gives more reliable predictions than any single model

---

## 📈 Model Performance Explained

Since the dataset is severely imbalanced (0.17% fraud), I used:

- **Recall** as primary metric — catching real frauds is more important than avoiding false alarms. Missing a fraud = real money stolen from customer.
- **ROC-AUC** as overall performance metric — measures how well the model separates fraud from legitimate across all thresholds. Score of 0.9766 means excellent separation ability.
- **NOT accuracy** — a model predicting everything as legitimate would get 99.83% accuracy while catching zero fraud.

---

## 👩‍💻 Author

**Anshika Gupta**
- 📧 anshikag3006@gmail.com
- 🔗 GitHub: [@anshikag3006](https://github.com/anshikag3006)
- 💼 LinkedIn: [linkedin.com/in/anshikag3006](https://linkedin.com/in/anshikag3006)