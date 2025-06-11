# XAI-T2DM-mortality-prediction

This repository contains the XAI model for predicting the risk (probability) of death in patients with T2DM based on ten variables:
- Age, years
- Number of complications (0, 1, 2, 3, 4 or 5), where complications are diabetic neuropathy, diabetic nephropathy, diabetic retinopathy, atherosclerotic vascular disease, major adverse cardiovascular events (MACE)
- N-terminal prohormone of brain natriuretic peptide (NT-proBNP), ng/L
- Triglycerides, mg/dL
- Creatinine, mg/dL
- High-sensitivity C-reactive protein (hs-CRP), mg/L
- Red cell distribution width-standard deviation (RDW-SD), fL
- Apolipoprotein A1, mg/dL
- N-glycan NA3F (branching α-1,3-fucosylated triantennary glycan), %
- Disease duration (duration of T2DM), years


## Getting Started

### File structure
```
├── data                          <- Folder containing data files
│   └── data.xlsx                      <- Data file example
│
├── model                         <- Trained prediction model
│
├── results                       <- Results folder (will appear after running the model)
│
├── src                           <- Source code (packages for working with data, model and graphs)
│
├── requirements.txt              <- File for installing python dependencies
│
├── run_prediction.py             <- Script to run the model
│
└── README.md                     <- This file
```

### Requirements
Python 3.11  
joblib==1.4.2  
openpyxl==3.1.5  
numpy==1.26.4  
pandas==2.2.2  
matplotlib==3.10.0  
scikit-survival==0.23.0  
shap==0.46.0  

### Installing
```bash
# clone project
git clone https://github.com/VershininaOlga/XAI-T2DM-mortality-prediction
cd XAI-T2DM-mortality-prediction

# [OPTIONAL] create environment
python -m venv .t2dm
.t2dm\Scripts\activate

# install requirements
pip install -r requirements.txt
```

### Data preparation
You need to prepare a data .xlsx file containing the following columns: Patient ID (unique patient identifier), Age, Number of complications, NT-proBNP, Triglycerides, Creatinine, hs-CRP, RDW-SD, Apolipoprotein A1, N-glycan NA3F and Disease duration.  
The file with your data should be placed in the ```data``` folder.  
An example data file can be found in ```data/data.xlsx```.  

### Running the prediction model
To run the model:
```
python run_prediction.py --file_name <file_name>
```
where ```<file_name>``` - data file name, eg ```data.xlsx```

As a result of running the script, a ```results``` folder will be generated, which will contain  
- file with a table containing the predicted mortality probability of patients from data file
- subfolder ```local_expl``` containing local explainability plots of the model's predictions for each patient


## Citation
Olga Vershinina, Jacopo Sabbatinelli, Anna Rita Bonfigli, Dalila Colombaretti, Angelica Giuliani, Mikhail Krivonosov, Arseniy Trukhanov, Claudio Franceschi, Mikhail Ivanchenko, Fabiola Olivieri. Explainable artificial intelligence model predicting the risk of all-cause mortality in patients with type 2 diabetes mellitus, 2025.


## Acknowledgments
This work was supported by the Ministry of Economic Development of the Russian Federation (grant No 139-15-2025-004 dated 17.04.2025, agreement identifier 000000С313925P3X0002).
  
