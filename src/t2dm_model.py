import pickle
import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pathlib import Path


class t2dm_model:
    def __init__(self):
        with open('model/model.pkl', 'rb') as file:
            self.model = pickle.load(file)
        self.predictor = self.model['predictor']
        self.features = self.model['features']
        self.zscaler = self.model['zscaler']
        self.bgrd = self.model['bgrd']
        self.seed = self.model['seed']

    def prepare_data(self, X_raw):
        X = pd.DataFrame(index=X_raw.index)
        zscaler = self.zscaler
        for f in X_raw.columns:
            if f in zscaler['features'].values:
                m = zscaler[zscaler['features'] == f]['means'].values[0]
                s = zscaler[zscaler['features'] == f]['stds'].values[0]
                X[f] = (X_raw[f] - m) / s
            else:
                X[f] = X_raw[f]
        X = X[self.features]
        if np.any(X.isna()):
            X = X.dropna()
            print('Samples containing missing values (NaNs) ​​were removed!')
        return X

    def predict_mortality(self, X, t=6142):
        survival_function = self.predictor.predict_survival_function(X)
        survival_function = stepfn_to_dataframe(survival_function, X.index.values) 
        survival_t = survival_function[survival_function.columns.values[np.argmin(np.abs(survival_function.columns.values - t))]].values
        mortality_t = 1 - survival_t
        return mortality_t

    def predict(self, X_raw):
        X = self.prepare_data(X_raw)
        pred_prob = pd.DataFrame({'Patient ID': X.index, '16.8-year mortality probability': self.predict_mortality(X, 6142)})
        return pred_prob

    def plot_local_shap(self, X_raw, dpi=100):
        print('Constructing explainability plots...')
        X = self.prepare_data(X_raw)
        X_raw = X_raw[self.features]
        explainer = shap.Explainer(self.predict_mortality, self.bgrd, feature_names=self.features, seed=self.seed)
        shap_values = explainer(X)
        
        for ind in range(0, len(X_raw)):
            X_raw_p = X_raw.loc[X_raw.index.values[ind],:].values
            shap_values_p = shap_values[ind,:].values
            base_value_p = shap_values[ind,:].base_values
            shap_values_p_abs = np.abs(shap_values_p)
            inds_sort = np.argsort(shap_values_p_abs)
            features_sort = self.features[inds_sort]
            shap_values_p_sort = shap_values_p[inds_sort]
            X_raw_p_sort = X_raw_p[inds_sort]    # the original values, not the normalized ones, will be indicated in the figure
        
            x_lim = [0.0, 1.0]
            x_range = x_lim[1] - x_lim[0]
            
            x_start = base_value_p
            y_start = 0.0
            y_h = 0.05
            y_gap = 0.01
            ylim_add = 0.02
        
            fig, ax = plt.subplots(figsize=(8, 6))
            yticks = []
            yticklabels = []
            for i in range(0, len(shap_values_p_sort)):
                length = shap_values_p_sort[i]
                if length > 0:
                    color = 'crimson'
                    x_arrow = 0.01
                else:
                    color = 'dodgerblue'
                    x_arrow = -0.01
        
                x_1, y_1 = x_start, y_start
                x_2, y_2 = x_start + length - x_arrow, y_start + y_h
                x_3, y_3 = x_start + length, y_start + y_h/2
        
                ax.axhline(y_3, c='whitesmoke', ls='dotted', zorder=0)
                
                yticks.append(y_3)
                yticklabels.append(f'{round(X_raw_p_sort[i], 3)} = {features_sort[i]}')
        
                if abs(length) > abs(x_arrow):
                    vertices = [(x_1, y_1), (x_1, y_2), (x_2, y_2), (x_3, y_3), (x_2, y_1)]
                elif length < x_arrow:
                    vertices = [(x_1, y_1), (x_1, y_2), (x_3, y_3)]
                elif length > x_arrow:
                    vertices = [(x_1, y_1), (x_1, y_2), (x_3, y_3)]
        
                poly = Polygon(vertices, closed=True, facecolor=color)
                ax.add_patch(poly)
        
                text_in = f'+{round(length, 3)}' if length > 0 else f'{round(length, 3)}'
                if length > 0:
                    text_color = 'crimson'
                    x_arrow = 0.01
                    text_start = x_start + length
                    ax.text(text_start, y_start + y_h/2.5, text_in, c=text_color, fontsize=11)
                else:
                    text_color = 'dodgerblue'
                    x_arrow = -0.01
                    text_start = x_start + length
                    ax.text(text_start, y_start + y_h/2.5, text_in, c=text_color, fontsize=11, horizontalalignment='right')
        
                ax.plot([x_3, x_3], [y_3, y_2+y_gap], c='silver', ls='dotted', zorder=0)
        
                x_start = x_start + length
                y_start = y_start + y_h + y_gap
        
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
        
            ax.set_yticks(yticks)
            ax.set_yticklabels(yticklabels, fontsize=14)
            ax.set_ylim(-ylim_add, y_2+ylim_add)
        
            xticks = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            ax.set_xticks(xticks)
            ax.set_xticklabels(xticks, fontsize=14)
            ax.set_xlim(x_lim)
        
            ax.axvline(base_value_p, c='lightgray', ls='dashed', zorder=0)
            ax.text(base_value_p+0.002, -0.015, f'E[f(X)] = {round(base_value_p, 3)}', c='dimgray', fontsize=11)
            ax.text(x_3, y_2+ylim_add, f'f(x) = {round(x_3, 3)}', fontsize=11)
            ax.plot([x_3, x_3], [-ylim_add, y_3], c='silver', ls='dotted', zorder=0)
            ax.set_xlabel('16.8-year mortality probability', fontsize=14)

            pict_fn = Path(f'results/local_expl/{X_raw.index.values[ind]}.png')
            pict_fn.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(pict_fn, dpi=dpi, bbox_inches='tight', facecolor='w')


def stepfn_to_dataframe(stepfn, p_inds):
    dataframe = []
    for fn in stepfn:
        times = fn.x
        dataframe.append(list(fn(fn.x)))
    dataframe = pd.DataFrame(dataframe)
    dataframe.index = p_inds
    dataframe.columns = times
    return dataframe
        