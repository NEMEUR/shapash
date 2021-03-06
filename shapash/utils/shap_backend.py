"""
shap_backend allow to compute contribution if needed
No tuning possible here:
The goal we are pursuing is to allow the user to have
a first level of explanation with very little code
the idea here is to purpose a simple implementation
to compute a first explanation in one line of code
but if you are looking a particular technique
we invite you to code it yourself.
You can check the reference https://github.com/slundberg/shap
You can also watch the tutorials which shows how to use shapash
with contributions calculated by lime or eli5 library
"""
import pandas as pd
import shap
from shapash.utils.model_synoptic import simple_tree_model, catboost_model, linear_model, svm_model

def shap_contributions(model, x_df, explainer=None):
    """
    Compute the local shapley contributions of each individual,
    feature.
    Using shap to

    Parameters
    ----------
    model: model object from sklearn, catboost, xgboost or lightgbm library
        this model is used to choose a shap explainer and to compute
        shapley values
    x_df: pd.DataFrame
    explainer : explainer object from shap, optional (default: None)
        this explainer is used to compute shapley values


    Returns
    -------
    np.array or list of np.array

    """
    if explainer is None:
        if str(type(model)) in simple_tree_model:
            explainer = shap.TreeExplainer(model)
            print("Backend: Shap TreeExplainer")

        elif str(type(model)) in catboost_model:
            explainer = shap.TreeExplainer(model)
            print("Backend: Shap TreeExplainer")

        elif str(type(model)) in linear_model:
            explainer = shap.LinearExplainer(model, x_df)
            print("Backend: Shap LinearExplainer")

        elif str(type(model)) in svm_model:
            explainer = shap.KernelExplainer(model.predict, x_df)
            print("Backend: Shap KernelExplainer")

    if str(type(model)) not in list(sum((simple_tree_model,catboost_model,linear_model,svm_model),())):
        raise ValueError(
            """
            model not supported by shapash, please compute contributions
            by yourself before using shapash
            """
        )

    contributions = explainer.shap_values(x_df)

    return contributions, explainer

def check_explainer(explainer):
    """
    Check if explainer class correspond to a shap explainer object
    """
    if explainer is not None:
        if explainer.__class__.__base__.__name__ != 'Explainer':
            raise ValueError(
                "explainer doesn't correspond to a shap explainer object"
            )
    return explainer
