### Models
Models used for data preprocessing, analyzing and forecasting are in models folder. There are 4 models developed namely 'meta_data.sql, per_item_covariates.sql, target_time_series.sql' and 'data_for_forecasting.sql.'

Steps to execute models
```
cd dbt
dbt run
```

### Data Analysis and Visualzations
Go to data analysis folder. There are 2 scripts, one will generate datasets for analysis in csv file and other will generate visualizations. 
simple execute the script
```
python3 eda_script.py
```
this will both generate dataset and generate visualizations. The results are already generated in the 'plots_2' folder and the notes for stake holders are provided in 'findings_and_hypothese.txt' file.

### Forecasting.

Go to predictions directore
```
cd predictions
```
Execute 
```
python3 forecast_sales.py
```
this script will generate predictions in forecase_results folder. The results are already stored in the 'forecast' folder so need to generate again. 

### Findings and hypothesis

Go to data_analysis folder and look for 'findings_and_hypothesis.txt' file.

### Dependencies
```
sudo apt install python3-poetry
sudo apt install python-is-python3
poetry env use python3
poetry install
poetry shell
```
### For analysis
```
pip3 install matplotlib
pip3 install seaborn
pip3 install statsmodels
```

### Forecasting packages
```
pip3 install nixtla
pip3 install scikit-learn
```