import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Training logic
data = {
    'attendance': [95, 40, 85, 60, 90, 35, 75, 50, 98, 45],
    'm10': [90, 45, 80, 55, 88, 40, 70, 52, 95, 42],
    'mInter': [92, 42, 78, 50, 85, 38, 72, 48, 96, 40],
    'performance': [2, 0, 1, 0, 2, 0, 1, 0, 2, 0] 
}

df = pd.DataFrame(data)
model = RandomForestClassifier(n_estimators=100)
model.fit(df[['attendance', 'm10', 'mInter']], df['performance'])

with open('student_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("✅ ML Model student_model.pkl created!")