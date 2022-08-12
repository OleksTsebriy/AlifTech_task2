# AlifTech Test Task
 
## Project description

This project is designed to help credit company to determine the risk of non-repayment of the loan by the borrowers. 
ML model was trained on dataset with potentially human-made desigions, which are quite messy and probably not the best possible desigions.

## Phase 1. Data exploration and training ML model
Dataset exploration jupyter notebook file **aliftech_test_task.ipnb** and datasets may be found in **RnD/** directory

## Phase 2. Creating API that recieve data and return model prediction

### Model description

Project uses supervised ML model - DesigionTreeClassifier. Borrower's data and other relevant information about credit is used to predict probability of non-opening credit account. 

### Data preprocessing

ML pipeline uses on-hot encoding to encode categorical features like gender and marital status. One-hot encoder was fitted on train data and could not encode new categories. Some data fields, like job position and living region, may contain rare observations, which are not captured by model (data with less than 150 observations were combined to "other" category during data preprocessing stage). In case of using data with rare or unique category, one-hot encoder will return all-zeros for relevant encoded variable, and model would not take it into account.

### Usage

#### Requirements

- Install packages `docker make`
- Copy `.env.dist` to `.env`

#### Build service

`make build`

#### Run service

`make up`

#### Stop service

`make down`

#### See container logs

`make logs`

## Example request

**POST** `0.0.0.0:7777/predict`

Body (json):

```json
{
  "gender": "M",
  "age": 32,
  "marital_status": "MAR",
  "job_position": "SPC",
  "credit_sum": 100000,
  "credit_month": 12,
  "tariff_id": "1.6",
  "score_shk": 0.459589,
  "education": "GRD",
  "living_region": "КРАСНОДАРСКИЙ КРАЙ",
  "monthly_income": 45000,
  "credit_count": 2,
  "overdue_credit_count": 0
}
```

## Example response

```json
{
  "open_account_flg_probability": 0.07609513723089946
}
```

#### Healthcheck

**GET** `0.0.0.0:7777/health`