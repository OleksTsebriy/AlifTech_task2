# AlifTech_task2
 
## Second part of AlifTech test task.

### Project description

This project is designed to help credit company to determine the risk of non-repayment of the loan by the borrowers. 
App uses supervised ML model - DesigionTreeClassifier to predict probability of non-opening credit account. 
ML model was trained on dataset with potentially human-made desigions, which are quite messy and probably not the best possible desigions.

### Input data

You should fill in request field and send it to ML server. Output would be probability of open_account_flg.

### Data preprocessing

ML pipeline uses on-hot encoding to encode categorical features like gender and marital status. One-hot encoder was fitted on train data and could not encode new categories. Some data fields, like job position and living region, may contain rare observations, which are not captured by model (data with less than 150 observations were combined to "other" category during data preprocessing stage). In case of using data with rare or unique category, one-hot encoder will return all-zeros for relevant encoded variable, and model would not take it into account.
