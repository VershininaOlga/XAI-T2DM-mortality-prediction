import argparse
import pandas as pd
from pathlib import Path
from src.t2dm_model import t2dm_model


def parse_args():
    parser = argparse.ArgumentParser(description='Predicting mortality probability in patients with T2DM')
    parser.add_argument('--file_name', default='data.xlsx', help='Data file name')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    X_raw = pd.read_excel(Path('data')/args.file_name, index_col='Patient ID')
    model = t2dm_model()
    pred_prob = model.predict(X_raw)
    pred_prob_fn = Path('results/predictions.xlsx')
    pred_prob_fn.parent.mkdir(parents=True, exist_ok=True)
    pred_prob.to_excel(pred_prob_fn, index=False)
    model.plot_local_shap(X_raw)


if __name__ == "__main__":
    main()
