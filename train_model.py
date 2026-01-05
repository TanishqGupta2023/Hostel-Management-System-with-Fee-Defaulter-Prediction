import os
import django
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hostelml.settings")
django.setup()

from hostelapp.models import Student

print("✅ Collecting data from database...")

data = []
for student in Student.objects.all():
    if student.year is not None:
        data.append({
            'attendance_percent': student.attendance_percent,
            'internal_score': student.internal_score,
            'parent_income': student.parent_income,
            'cgpa': student.cgpa,
            'scholarship': int(student.scholarship),
            'fee_paid': int(student.has_paid_fees), 
        })

df = pd.DataFrame(data)


df.dropna(inplace=True)
print(f"✅ Total valid rows collected: {len(df)}")

print("\n📊 Fee status distribution in data:")
print(df['fee_paid'].value_counts())

X = df.drop('fee_paid', axis=1)
y = df['fee_paid']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


print("\n🔄 Balancing classes using SMOTE...")
sm = SMOTE(random_state=42)
X_resampled, y_resampled = sm.fit_resample(X_scaled, y)


X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)


y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)


print(f"\n✅ Model trained! Accuracy: {accuracy * 100:.2f}%")
print("\n🧾 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))


importances = model.feature_importances_
features = X.columns
importance_dict = dict(zip(features, importances))

print("\n📌 Feature Importances:")
for feature, importance in importance_dict.items():
    print(f"{feature}: {importance:.3f}")

plt.figure(figsize=(8, 5))
plt.barh(features, importances, color='skyblue')
plt.xlabel('Importance')
plt.title('Feature Importances')
plt.tight_layout()
plt.savefig('feature_importance.png')
print("\n📈 Feature importance graph saved as 'feature_importance.png'")


joblib.dump(model, 'fee_defaulter_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
print("\n💾 Model saved as 'fee_defaulter_model.pkl'")
print("💾 Scaler saved as 'scaler.pkl'")
