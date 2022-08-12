import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder
import pickle

from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel 

class request_body(BaseModel):
    gender : str = 'M'
    age : int = '32'
    marital_status: str = 'MAR'
    job_position: str = 'SPC'
    credit_sum: float = 100000
    credit_month: int = 12
    tariff_id: str = '1.6'
    score_shk: float = 0.459589
    education: str = 'GRD'
    living_region: str = 'КРАСНОДАРСКИЙ КРАЙ'
    monthly_income: int = 45000
    credit_count: int = 2
    overdue_credit_count: int = 0

app = FastAPI()

# Loading model
model = pickle.load(open('model', 'rb'))

# Loading encoder
oh_encoder = pickle.load(open('one_hot_encoder', 'rb'))

# Get encoded column names
cat_cols_encoded = pickle.load(open('encoded_colnames', 'rb'))

# Categorical column names
cat_columns = [ 'gender', 'marital_status', 'job_position', 
                'tariff_id', 'education', 'living_region']

# Defining path operation for root endpoint
@app.get('/')
def main():
    return {'message': 'This is APP root. Go to  http://127.0.0.1:5000/docs'}
 
# Predicting open_account_flg_probability probability by request data
@app.post('/predict')
def predict(data : request_body):
    credit_data = pd.DataFrame.from_dict([data.dict()])

    # constructing new features as in training pipeline
    # actually here should be some external module call 
    credit_data['monthly_pay'] = credit_data['credit_sum'] / credit_data['credit_month']
    credit_data['pay_ratio'] = credit_data['monthly_pay'] / credit_data['monthly_income']
    credit_data['overdue_ratio'] = credit_data['overdue_credit_count'] / credit_data['credit_count']
    credit_data['overdue_ratio'] = credit_data['overdue_ratio'].fillna(-1)

    encoded_cols = oh_encoder.transform(credit_data[cat_columns])
    df_enc = pd.DataFrame(encoded_cols, columns = cat_cols_encoded, index = credit_data.index)
    X = pd.concat([credit_data.drop(columns = cat_columns), df_enc], axis="columns")
    predict_prob = model.predict_proba(X)
    return { 'open_account_flg_probability' : predict_prob[0,1]}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)
