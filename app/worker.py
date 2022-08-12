import logging
import pickle

import pandas as pd


logger = logging.getLogger("waitress")


class Worker:
    def __init__(self):
        # Loading model
        with open("./models/model", "rb") as f:
            self.model = pickle.load(f)

        # Loading encoder
        with open("./models/one_hot_encoder", "rb") as f:
            self.oh_encoder = pickle.load(f)

        # Get encoded column names
        with open("./models/encoded_colnames", "rb") as f:
            self.cat_cols_encoded = pickle.load(f)

        # Categorical column names
        self.cat_columns = ["gender", "marital_status", "job_position", "tariff_id", "education", "living_region"]

    def predict(self, data: dict):
        error = None

        try:
            credit_data = pd.DataFrame.from_dict([data])

            # Preprocess the data - create additional features, perform one-hot encoding
            X = self.preprocess(credit_data)

            # Run the inference
            predict_prob = self.model.predict_proba(X)
            result = {"open_account_flg_probability": predict_prob[0, 1]}

        except Exception as e:
            return {}, e

        return result, error

    def preprocess(self, credit_data):
        credit_data["monthly_pay"] = credit_data["credit_sum"] / credit_data["credit_month"]
        credit_data["pay_ratio"] = credit_data["monthly_pay"] / credit_data["monthly_income"]
        credit_data["overdue_ratio"] = credit_data["overdue_credit_count"] / credit_data["credit_count"]
        credit_data["overdue_ratio"] = credit_data["overdue_ratio"].fillna(-1)

        encoded_cols = self.oh_encoder.transform(credit_data[self.cat_columns])
        df_enc = pd.DataFrame(encoded_cols, columns=self.cat_cols_encoded, index=credit_data.index)

        X = pd.concat([credit_data.drop(columns=self.cat_columns), df_enc], axis="columns")

        return X
