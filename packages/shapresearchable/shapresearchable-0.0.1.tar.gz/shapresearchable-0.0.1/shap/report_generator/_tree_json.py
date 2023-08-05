#This is used to generate JSON data for treeExpainer


from __future__ import division

import warnings
import numpy as np
import numpy.ma as ma
import scipy as sp
from scipy.stats import gaussian_kde

from ..utils import safe_isinstance, OpChain, format_value
from ._utils import convert_ordering, merge_nodes, get_sort_order, sort_inds
from .. import Explanation

labels = {
    'MAIN_EFFECT': "SHAP main effect value for\n%s",
    'INTERACTION_VALUE': "SHAP interaction value",
    'INTERACTION_EFFECT': "SHAP interaction value for\n%s and %s",
    'VALUE': "SHAP value (impact on model output)",
    'GLOBAL_VALUE': "mean(|SHAP value|) (average impact on model output magnitude)",
    'VALUE_FOR': "SHAP value for\n%s",
    'PLOT_FOR': "SHAP plot for %s",
    'FEATURE': "Feature %s",
    'FEATURE_VALUE': "Feature value",
    'FEATURE_VALUE_LOW': "Low",
    'FEATURE_VALUE_HIGH': "High",
    'JOINT_VALUE': "Joint SHAP value",
    'MODEL_OUTPUT': "Model output value"
}

def reveal_distribution(shap_values, feature_values, feature_name):
    corr = ma.corrcoef(ma.masked_invalid(shap_values), ma.masked_invalid(feature_values))
    coef = corr[0,1]
    return coef


def json_tree_explainer(shap_values, features, feature_names=None, class_names=None):

    if str(type(shap_values)).endswith("Explanation'>"):
        print ('end with explanation')
        shap_exp = shap_values
        base_value = shap_exp.base_values
        shap_values = shap_exp.values
        if features is None:
            features = shap_exp.data
        if feature_names is None:
            feature_names = shap_exp.feature_names

    multi_class = False
    if isinstance(shap_values, list):
        multi_class = True

    print('1' * 20)

    if str(type(features)) == "<class 'pandas.core.frame.DataFrame'>":
        if feature_names is None:
            feature_names = features.columns
        features = features.values
        print('aaaa')
    elif isinstance(features, list):
        if feature_names is None:
            feature_names = features
        features = None
        print('bbb')
    elif (features is not None) and len(features.shape) == 1 and feature_names is None:
        feature_names = features
        features = None
        print('cccccc')

    num_features = (shap_values[0].shape[1] if multi_class else shap_values.shape[1])

    print('2' * 20)

    if features is not None:
        shape_msg = "The shape of the shap_values matrix does not match the shape of the " \
                    "provided data matrix."
        if num_features - 1 == features.shape[1]:
            assert False, shape_msg + " Perhaps the extra column in the shap_values matrix is the " \
                          "constant offset? Of so just pass shap_values[:,:-1]."
        else:
            assert num_features == features.shape[1], shape_msg


    if feature_names is None:
        feature_names = np.array([labels['FEATURE'] % str(i) for i in range(num_features)])

    max_display = 20

    if multi_class:
        feature_order = np.argsort(np.sum(np.mean(np.abs(shap_values), axis=1), axis=0))
    else:
        feature_order = np.argsort(np.sum(np.abs(shap_values), axis=0))
    feature_order = feature_order[-min(max_display, len(feature_order)):]

    print(feature_order)

    print('3' * 20)

    shap_feature_values = {'importance_sentences' : [], 'correlation_sentences' : [], 'names' : [], 'coefs' : [], 'importance_data' : []}

    if features is not None:
        print('in the violin if')
        global_low = np.nanpercentile(shap_values[:, :len(feature_names)].flatten(), 1)
        global_high = np.nanpercentile(shap_values[:, :len(feature_names)].flatten(), 99)

        for pos, i in enumerate(feature_order):
            shaps = shap_values[:, i]
            shap_min, shap_max = np.min(shaps), np.max(shaps)
            rng = shap_max - shap_min
            xs = np.linspace(np.min(shaps) - rng * 0.2, np.max(shaps) + rng * 0.2, 100)
            if np.std(shaps) < (global_high - global_low) / 100:
                ds = gaussian_kde(shaps + np.random.randn(len(shaps)) * (global_high - global_low) / 100)(xs)
            else:
                ds = gaussian_kde(shaps)(xs)
            ds /= np.max(ds) * 3

            values = features[:, i]
            window_size = max(10, len(values) // 20)
            smooth_values = np.zeros(len(xs) - 1)
            sort_inds = np.argsort(shaps)
            trailing_pos = 0
            leading_pos = 0
            running_sum = 0
            back_fill = 0

            #importances 
            abs_shaps = np.abs(shaps)
            average_abs_shaps = np.mean(abs_shaps, axis=0)
            importances_array = shap_feature_values['importance_data']
            importances_array.append(average_abs_shaps)

            #insert here
            coef = reveal_distribution(shaps, values, feature_names[i])
            coefs = shap_feature_values['coefs']
            if coef is ma.masked:
            	coefs.append(0)
            else:
            	coefs.append(coef)
            most_important_features = shap_feature_values['importance_sentences']
            names = shap_feature_values['names']
            names.append(feature_names[i])

            correlation_type = ''

            if coef > 0:
                correlation_type = 'positive'
            else:
                correlation_type = 'negative'

            if pos > len(feature_names) - 4:
                if pos == len(feature_names) - 1:
                    statement = 'The most important feature is %s and the correlation is %s' % (feature_names[i], correlation_type)
                elif pos == len(feature_names) - 2:
                    statement = 'The second important feature is %s and the correlation is %s.' % (feature_names[i], correlation_type)
                elif pos == len(feature_names) - 3:
                    statement = 'The third most important feature is %s and the correlation is %s.' % (feature_names[i], correlation_type)

                most_important_features.append(statement)
                


            most_correlated_features = shap_feature_values['correlation_sentences']
            if coef >=0.3:
                statement = 'the %s has strong positive correlation with the predicted value. So it would higher the result value.' % feature_names[i]
                most_correlated_features.append(statement)
            elif coef <= -0.3:
                statement = 'the %s has strong negative correlation with the predicted value. So it would lower the result value.' % feature_names[i]
                most_correlated_features.append(statement)

    print('json_tree_explainer')
    print(shap_feature_values)
    return shap_feature_values


