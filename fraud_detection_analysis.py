"""
Financial Fraud Detection System
Author: [Your Name]
Description: Analyzing transaction patterns and detecting fraudulent activities
using machine learning and statistical methods
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class FraudDetectionSystem:
    """
    A comprehensive fraud detection system for financial transactions
    """
    
    def __init__(self, data_path):
        """Initialize the fraud detection system"""
        self.data_path = data_path
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.model = None
        
    def load_data(self):
        """Load and perform initial data exploration"""
        print("Loading data...")
        self.df = pd.read_csv(self.data_path)
        print(f"Data loaded successfully. Shape: {self.df.shape}")
        print("\nFirst few rows:")
        print(self.df.head())
        print("\nData Info:")
        print(self.df.info())
        print("\nClass Distribution:")
        print(self.df['Class'].value_counts())
        return self.df
    
    def exploratory_analysis(self):
        """Perform comprehensive EDA"""
        print("\n" + "="*50)
        print("EXPLORATORY DATA ANALYSIS")
        print("="*50)
        
        # Statistical summary
        print("\nStatistical Summary:")
        print(self.df.describe())
        
        # Check for missing values
        print("\nMissing Values:")
        print(self.df.isnull().sum())
        
        # Fraud vs Normal transaction distribution
        fraud_count = self.df['Class'].value_counts()
        print(f"\nNormal Transactions: {fraud_count[0]}")
        print(f"Fraudulent Transactions: {fraud_count[1]}")
        print(f"Fraud Percentage: {(fraud_count[1]/len(self.df))*100:.2f}%")
        
        # Visualizations
        self._create_eda_visualizations()
        
    def _create_eda_visualizations(self):
        """Create EDA visualizations"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Class Distribution
        self.df['Class'].value_counts().plot(kind='bar', ax=axes[0, 0], color=['green', 'red'])
        axes[0, 0].set_title('Transaction Class Distribution', fontsize=14, fontweight='bold')
        axes[0, 0].set_xlabel('Class (0: Normal, 1: Fraud)')
        axes[0, 0].set_ylabel('Count')
        
        # 2. Amount Distribution
        axes[0, 1].hist(self.df[self.df['Class']==0]['Amount'], bins=50, alpha=0.5, label='Normal', color='green')
        axes[0, 1].hist(self.df[self.df['Class']==1]['Amount'], bins=50, alpha=0.5, label='Fraud', color='red')
        axes[0, 1].set_title('Transaction Amount Distribution', fontsize=14, fontweight='bold')
        axes[0, 1].set_xlabel('Amount')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].legend()
        axes[0, 1].set_yscale('log')
        
        # 3. Time Distribution
        axes[1, 0].scatter(self.df[self.df['Class']==0]['Time'], 
                          self.df[self.df['Class']==0]['Amount'], 
                          alpha=0.3, label='Normal', s=1, color='green')
        axes[1, 0].scatter(self.df[self.df['Class']==1]['Time'], 
                          self.df[self.df['Class']==1]['Amount'], 
                          alpha=0.8, label='Fraud', s=10, color='red')
        axes[1, 0].set_title('Transactions Over Time', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('Time')
        axes[1, 0].set_ylabel('Amount')
        axes[1, 0].legend()
        
        # 4. Correlation heatmap (sample of features)
        correlation_matrix = self.df[['Time', 'Amount', 'Class']].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=axes[1, 1])
        axes[1, 1].set_title('Feature Correlation Heatmap', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('eda_visualizations.png', dpi=300, bbox_inches='tight')
        print("\nEDA visualizations saved as 'eda_visualizations.png'")
        plt.show()
        
    def preprocess_data(self):
        """Prepare data for modeling"""
        print("\n" + "="*50)
        print("DATA PREPROCESSING")
        print("="*50)
        
        # Separate features and target
        X = self.df.drop('Class', axis=1)
        y = self.df['Class']
        
        # Train-test split (80-20)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"Training set size: {len(self.X_train)}")
        print(f"Test set size: {len(self.X_test)}")
        print(f"Fraud cases in training: {sum(self.y_train)}")
        print(f"Fraud cases in test: {sum(self.y_test)}")
        
        # Scale features
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)
        
        print("\nData preprocessing completed!")
        
    def train_model(self):
        """Train Random Forest classifier"""
        print("\n" + "="*50)
        print("MODEL TRAINING")
        print("="*50)
        
        print("Training Random Forest Classifier...")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1,
            class_weight='balanced'  # Handle imbalanced data
        )
        
        self.model.fit(self.X_train, self.y_train)
        print("Model training completed!")
        
    def evaluate_model(self):
        """Evaluate model performance"""
        print("\n" + "="*50)
        print("MODEL EVALUATION")
        print("="*50)
        
        # Predictions
        y_pred = self.model.predict(self.X_test)
        y_pred_proba = self.model.predict_proba(self.X_test)[:, 1]
        
        # Classification Report
        print("\nClassification Report:")
        print(classification_report(self.y_test, y_pred))
        
        # ROC-AUC Score
        roc_auc = roc_auc_score(self.y_test, y_pred_proba)
        print(f"\nROC-AUC Score: {roc_auc:.4f}")
        
        # Visualizations
        self._create_evaluation_visualizations(y_pred, y_pred_proba)
        
        return y_pred, y_pred_proba
        
    def _create_evaluation_visualizations(self, y_pred, y_pred_proba):
        """Create model evaluation visualizations"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # 1. Confusion Matrix
        cm = confusion_matrix(self.y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0])
        axes[0].set_title('Confusion Matrix', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Predicted')
        axes[0].set_ylabel('Actual')
        
        # 2. ROC Curve
        fpr, tpr, _ = roc_curve(self.y_test, y_pred_proba)
        roc_auc = roc_auc_score(self.y_test, y_pred_proba)
        
        axes[1].plot(fpr, tpr, color='darkorange', lw=2, 
                     label=f'ROC curve (AUC = {roc_auc:.2f})')
        axes[1].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        axes[1].set_xlim([0.0, 1.0])
        axes[1].set_ylim([0.0, 1.05])
        axes[1].set_xlabel('False Positive Rate')
        axes[1].set_ylabel('True Positive Rate')
        axes[1].set_title('ROC Curve', fontsize=14, fontweight='bold')
        axes[1].legend(loc="lower right")
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('model_evaluation.png', dpi=300, bbox_inches='tight')
        print("\nEvaluation visualizations saved as 'model_evaluation.png'")
        plt.show()
        
    def feature_importance_analysis(self):
        """Analyze feature importance"""
        print("\n" + "="*50)
        print("FEATURE IMPORTANCE ANALYSIS")
        print("="*50)
        
        # Get feature importance
        feature_names = self.df.drop('Class', axis=1).columns
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1][:10]  # Top 10 features
        
        # Print feature ranking
        print("\nTop 10 Important Features:")
        for i, idx in enumerate(indices):
            print(f"{i+1}. {feature_names[idx]}: {importances[idx]:.4f}")
        
        # Visualization
        plt.figure(figsize=(12, 6))
        plt.bar(range(10), importances[indices], color='teal')
        plt.xticks(range(10), [feature_names[i] for i in indices], rotation=45, ha='right')
        plt.xlabel('Features')
        plt.ylabel('Importance')
        plt.title('Top 10 Feature Importances', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
        print("\nFeature importance visualization saved as 'feature_importance.png'")
        plt.show()
        
    def anomaly_detection(self):
        """Additional anomaly detection using Isolation Forest"""
        print("\n" + "="*50)
        print("ANOMALY DETECTION (Isolation Forest)")
        print("="*50)
        
        # Train Isolation Forest on normal transactions only
        normal_data = self.df[self.df['Class'] == 0].drop('Class', axis=1)
        normal_data_scaled = self.scaler.fit_transform(normal_data)
        
        iso_forest = IsolationForest(
            contamination=0.01,
            random_state=42,
            n_jobs=-1
        )
        
        iso_forest.fit(normal_data_scaled)
        
        # Predict on all data
        all_data_scaled = self.scaler.transform(self.df.drop('Class', axis=1))
        anomaly_predictions = iso_forest.predict(all_data_scaled)
        
        # -1 for anomalies, 1 for normal
        anomaly_predictions = [1 if x == -1 else 0 for x in anomaly_predictions]
        
        print(f"\nAnomalies detected: {sum(anomaly_predictions)}")
        print(f"Actual fraud cases: {sum(self.df['Class'])}")
        
        # Compare with actual fraud
        from sklearn.metrics import accuracy_score, precision_score, recall_score
        print(f"\nIsolation Forest Performance:")
        print(f"Accuracy: {accuracy_score(self.df['Class'], anomaly_predictions):.4f}")
        print(f"Precision: {precision_score(self.df['Class'], anomaly_predictions):.4f}")
        print(f"Recall: {recall_score(self.df['Class'], anomaly_predictions):.4f}")

    def plot_precision_recall_curve(self, y_pred_proba):
        """Plot Precision-Recall curve for imbalanced data"""
        from sklearn.metrics import precision_recall_curve, average_precision_score
        
        precision, recall, _ = precision_recall_curve(self.y_test, y_pred_proba)
        avg_precision = average_precision_score(self.y_test, y_pred_proba)
        
        plt.figure(figsize=(8, 6))
        plt.plot(recall, precision, color='blue', lw=2, 
                label=f'Precision-Recall curve (AP = {avg_precision:.2f})')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision-Recall Curve - Important for Imbalanced Data', 
                fontsize=14, fontweight='bold')
        plt.legend(loc="lower left")
        plt.grid(True, alpha=0.3)
        plt.savefig('precision_recall_curve.png', dpi=300, bbox_inches='tight')
        print(f"\nAverage Precision Score: {avg_precision:.4f}")
        plt.close()


def main():
    """Main execution function"""
    print("="*50)
    print("FINANCIAL FRAUD DETECTION SYSTEM")
    print("="*50)
    
    # Initialize system
    fraud_system = FraudDetectionSystem('creditcard.csv')
    
    # Step 1: Load data
    fraud_system.load_data()
    
    # Step 2: Exploratory Analysis
    fraud_system.exploratory_analysis()
    
    # Step 3: Preprocess data
    fraud_system.preprocess_data()
    
    # Step 4: Train model
    fraud_system.train_model()
    
    # Step 5: Evaluate model
    y_pred, y_pred_proba = fraud_system.evaluate_model()

    # NEW: Add precision-recall curve
    fraud_system.plot_precision_recall_curve(y_pred_proba)
    
    # Step 6: Feature importance
    fraud_system.feature_importance_analysis()
    
    # Step 7: Anomaly detection
    fraud_system.anomaly_detection()
    
    print("\n" + "="*50)
    print("ANALYSIS COMPLETE!")
    print("="*50)
    print("\nGenerated files:")
    print("1. eda_visualizations.png")
    print("2. model_evaluation.png")
    print("3. feature_importance.png")


if __name__ == "__main__":
    main()