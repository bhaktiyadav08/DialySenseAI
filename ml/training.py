import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
import joblib

# 1. Load dataset
df = pd.read_csv('../data/raw/dataset.csv')

# 2. Convert labels to numbers
df['status'] = df['status'].map({'normal': 0, 'blockage': 1})

# 3. Split features and target
X = df[['temperature', 'flow_rate', 'water_level']]
y = df['status']

# 4. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5. Create XGBoost model
model = XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=4
)

# 6. Train model
model.fit(X_train, y_train)

# 7. Predict
y_pred = model.predict(X_test)

# 8. Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# 9. Save model
joblib.dump(model, '../models/model.pkl')

print("Model trained and saved successfully!")