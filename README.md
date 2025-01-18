### Models
This repository showcases a **data science case study** focused on data analysis and visualization. It includes comprehensive **ETL processes,** **data cleaning,** exploratory **data analysis** (EDA), and **insights generation**. Designed for business and analytical applications, it employs Python tools like Pandas, NumPy, and Matplotlib, offering a structured approach to solving real-world analytical problems.

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
