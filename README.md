# Building pipeline for data preparation and model training 

## Description

Yandex Real Estate represents a marketplace for renting and purchasing residential and commercial real estate. Company acts as a middleman between sellers and potential buyers.

### Problem

The key objective of the company is to make the communication between both sides efficient and secure, since during negotiations there appears a number of questions which may result in arguments and therefore the deal will not be struck. For such a marketplace this is not an desirable outcome and that is why product managers stated exploring potential directions of growth of the company and discovered that disagreements often arise due to the price of the real estate object. This is about sellers and buyers having different opinions about the market price of a flat - it is important to enables them to come to a mutual agreement.

Product managers hypothesize that the mean monthly number of deal may increase if the business sides will have an opportunity to conduct objective external evaluation of the real estate objects.

### Business task

Creating an MVP of the algorithm based on machine learning for evaluating the value of real estate objects provided their characteristics. 

## Process 

### Stage 1 - Data collection

| Name | File/dir name | Location | 
| :---------------------- | :---------------------- | :---------------------- |
| DAG-init | `flats_init_etl.py` | [Link](part1_airflow/dags/flats_init_etl.py) |
| DAG-plugins | `real_estate.py` | [Link](part1_airflow/plugins/steps/real_estate.py)|
| Telegram-callbacks | `messages.py` | [Link](part1_airflow/plugins/steps/messages.py)|

### Stage 2 - Data cleaning

| Name | File/dir name | Location | 
| :---------------------- | :---------------------- | :---------------------- |
| DAG-init | `flats_clean_etl.py` | [Link](part1_airflow/dags/flats_clean_etl.py) |
| DAG-plugins | `real_estate_cleaning.py` | [Link](part1_airflow/plugins/steps/real_estate_cleaning.py) |
| Telegram-callbacks | `messages.py` | [Link](part1_airflow/plugins/steps/messages.py)|
| Jupyter notebook | `data_cleaning.py` | [Link](part1_airflow/notebooks/data_cleaning.ipynb)|

### Stage 3 - Creating DVC-pipeline of model training

| Name | File/dir name | Location | 
| :---------------------- | :---------------------- | :---------------------- |
| DVC-scripts | `scripts` | [Link](part2_dvc/scripts/) |
| DVC-yaml-config | `dvc.yaml` | [Link](part2_dvc/dvc.yaml) |
| DVC-lock-config | `dvc.lock` | [Link](part2_dvc/dvc.lock)|
| Params-config | `params.yaml` | [Link](part2_dvc/params.yaml)|
| Jupyter notebook | `cleaned_data_inspection.ipynb` | [Link](part2_dvc/notebooks/cleaned_data_inspection.ipynb)|
