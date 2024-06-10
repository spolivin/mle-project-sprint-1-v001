# Разработка пайплайнов подготовки данных и обучения модели [Проект 1 спринта]


S3 Bucket Name: `s3-student-mle-20240523-34f645dbbf`


## Этап 1 - Сбор данных

| Name | File/dir name | Location | 
| :---------------------- | :---------------------- | :---------------------- |
| DAG-init | `flats_init_etl.py` | [Link](part1_airflow/dags/flats_init_etl.py) |
| DAG-plugins | `real_estate.py` | [Link](part1_airflow/plugins/steps/real_estate.py)|
| Telegram-callbacks | `messages.py` | [Link](part1_airflow/plugins/steps/messages.py)|

## Этап 2 - Очистка данных

| Name | File/dir name | Location | 
| :---------------------- | :---------------------- | :---------------------- |
| DAG-init | `flats_clean_etl.py` | [Link](part1_airflow/dags/flats_clean_etl.py) |
| DAG-plugins | `real_estate_cleaning.py` | [Link](part1_airflow/plugins/steps/real_estate_cleaning.py) |
| Telegram-callbacks | `messages.py` | [Link](part1_airflow/plugins/steps/messages.py)|
| Jupyter notebook | `data_cleaning.py` | [Link](part1_airflow/notebooks/data_cleaning.ipynb)|

## Этап 3 - Создание DVC-пайплайна обучения модели

| Name | File/dir name | Location | 
| :---------------------- | :---------------------- | :---------------------- |
| DVC-scripts | `scripts` | [Link](part2_dvc/scripts/) |
| DVC-yaml-config | `dvc.yaml` | [Link](part2_dvc/dvc.yaml) |
| DVC-lock-config | `dvc.lock` | [Link](part2_dvc/dvc.lock)|
| Params-config | `params.yaml` | [Link](part2_dvc/params.yaml)|
| Jupyter notebook | `cleaned_data_inspection.ipynb` | [Link](part2_dvc/notebooks/cleaned_data_inspection.ipynb)|
