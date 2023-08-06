import unittest

import pandas as pd
import numpy as np
from pandas.api.types import is_categorical_dtype, is_numeric_dtype

import plotly.graph_objs as go

from catboost import CatBoostClassifier, CatBoostRegressor

from explainerdashboard import RegressionExplainer, ClassifierExplainer
from explainerdashboard.datasets import *

class CatBoostRegressionTests(unittest.TestCase):
    def setUp(self):
        X_train, y_train, X_test, y_test = titanic_fare()
        self.test_len = len(X_test)

        train_names, test_names = titanic_names()
        _, self.names = titanic_names()

        model = CatBoostRegressor(iterations=5, verbose=0).fit(X_train, y_train)
        explainer = RegressionExplainer(model, X_test, y_test, cats=['Deck', 'Embarked'])
        X_cats, y_cats = explainer.X_merged, explainer.y
        model = CatBoostRegressor(iterations=5, verbose=0).fit(X_cats, y_cats, cat_features=[8, 9])
        self.explainer = RegressionExplainer(model, X_cats, y_cats, cats=['Sex'], idxs=X_test.index)


    def test_explainer_len(self):
        self.assertEqual(len(self.explainer), self.test_len)

    def test_int_idx(self):
        self.assertEqual(self.explainer.get_idx(self.names[0]), 0)

    def test_random_index(self):
        self.assertIsInstance(self.explainer.random_index(), int)
        self.assertIsInstance(self.explainer.random_index(return_str=True), str)

    def test_row_from_input(self):
        input_row = self.explainer.get_row_from_input(
            self.explainer.X.iloc[[0]].values.tolist())
        self.assertIsInstance(input_row, pd.DataFrame)
        
        input_row = self.explainer.get_row_from_input(
            self.explainer.X_merged
            [self.explainer.columns_ranked_by_shap()]
            .iloc[[0]].values.tolist(), ranked_by_shap=True)
        self.assertIsInstance(input_row, pd.DataFrame)

    def test_prediction_result_df(self):
        df = self.explainer.prediction_result_df(0)
        self.assertIsInstance(df, pd.DataFrame)

    def test_preds(self):
        self.assertIsInstance(self.explainer.preds, np.ndarray)

    def test_pred_percentiles(self):
        self.assertIsInstance(self.explainer.pred_percentiles(), np.ndarray)

    def test_columns_ranked_by_shap(self):
        self.assertIsInstance(self.explainer.columns_ranked_by_shap(), list)

    def test_ordered_cats(self):
        self.assertEqual(self.explainer.ordered_cats("Sex"), ['NOT_ENCODED', 'Sex_female', 'Sex_male'])
        self.assertEqual(self.explainer.ordered_cats("Deck", topx=2, sort='alphabet'), ['Deck_A', 'Deck_B'])

        self.assertIsInstance(self.explainer.ordered_cats("Deck", sort='freq'), list)
        self.assertIsInstance(self.explainer.ordered_cats("Deck", topx=3, sort='freq'), list)
        self.assertIsInstance(self.explainer.ordered_cats("Deck", sort='shap'), list)
        self.assertIsInstance(self.explainer.ordered_cats("Deck", topx=3, sort='shap'), list)

    def test_get_col(self):
        self.assertIsInstance(self.explainer.get_col("Sex"), pd.Series)
        self.assertTrue(is_categorical_dtype(self.explainer.get_col("Sex")))

        self.assertIsInstance(self.explainer.get_col("Age"), pd.Series)
        self.assertTrue(is_numeric_dtype(self.explainer.get_col("Age")))

    def test_permutation_importances(self):
        self.assertIsInstance(self.explainer.get_permutation_importances_df(), pd.DataFrame)

    def test_X_cats(self):
        self.assertIsInstance(self.explainer.X_cats, pd.DataFrame)

    def test_metrics(self):
        self.assertIsInstance(self.explainer.metrics(), dict)
        self.assertIsInstance(self.explainer.metrics_descriptions(), dict)

    def test_mean_abs_shap_df(self):
        self.assertIsInstance(self.explainer.get_mean_abs_shap_df(), pd.DataFrame)

    def test_permutation_importances_df(self):
        self.assertIsInstance(self.explainer.get_permutation_importances_df(), pd.DataFrame)
        self.assertIsInstance(self.explainer.get_permutation_importances_df(topx=3), pd.DataFrame)
        self.assertIsInstance(self.explainer.get_permutation_importances_df(cutoff=0.01), pd.DataFrame)

    def test_contrib_df(self):
        self.assertIsInstance(self.explainer.get_contrib_df(0), pd.DataFrame)
        self.assertIsInstance(self.explainer.get_contrib_df(0, topx=3), pd.DataFrame)
        self.assertIsInstance(self.explainer.get_contrib_df(0, sort='importance'), pd.DataFrame)
        self.assertIsInstance(self.explainer.get_contrib_df(X_row=self.explainer.X.iloc[[0]]), pd.DataFrame)



    def test_contrib_summary_df(self):
        self.assertIsInstance(self.explainer.get_contrib_summary_df(0), pd.DataFrame)
        self.assertIsInstance(self.explainer.get_contrib_summary_df(0, topx=3), pd.DataFrame)
        self.assertIsInstance(self.explainer.get_contrib_summary_df(0, round=3), pd.DataFrame)
        self.assertIsInstance(self.explainer.get_contrib_summary_df(0, sort='high-to-low'), pd.DataFrame)
        self.assertIsInstance(self.explainer.get_contrib_summary_df(0, sort='low-to-high'), pd.DataFrame)
        self.assertIsInstance(self.explainer.get_contrib_summary_df(0, sort='importance'), pd.DataFrame)
        self.assertIsInstance(self.explainer.get_contrib_summary_df(X_row=self.explainer.X.iloc[[0]]), pd.DataFrame)

    def test_shap_base_value(self):
        self.assertIsInstance(self.explainer.shap_base_value(), (np.floating, float))

    def test_shap_values_shape(self):
        self.assertTrue(self.explainer.get_shap_values_df().shape == (len(self.explainer), len(self.explainer.merged_cols)))

    def test_shap_values(self):
        self.assertIsInstance(self.explainer.get_shap_values_df(), pd.DataFrame)

    def test_mean_abs_shap(self):
        self.assertIsInstance(self.explainer.get_mean_abs_shap_df(), pd.DataFrame)

    def test_calculate_properties(self):
        self.explainer.calculate_properties()

    def test_pdp_df(self):
        self.assertIsInstance(self.explainer.pdp_df("Age"), pd.DataFrame)
        self.assertIsInstance(self.explainer.pdp_df("Sex"), pd.DataFrame)
        self.assertIsInstance(self.explainer.pdp_df("Deck"), pd.DataFrame)
        self.assertIsInstance(self.explainer.pdp_df("Age", index=0), pd.DataFrame)
        self.assertIsInstance(self.explainer.pdp_df("Sex", index=0), pd.DataFrame)

    def test_plot_importances(self):
        fig = self.explainer.plot_importances()
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_importances(kind='permutation')
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_importances(topx=3)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_shap_detailed(self):
        fig = self.explainer.plot_importances_detailed()
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_importances_detailed(topx=3)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_dependence(self):
        fig = self.explainer.plot_dependence("Age")
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_dependence("Sex")
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_dependence("Age", "Sex")
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_dependence("Age", highlight_index=0)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_dependence("Sex", highlight_index=0)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_dependence("Deck", topx=3, sort="freq")
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_dependence("Deck", topx=3, sort="shap")
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_dependence("Deck", sort="freq")
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_dependence("Deck", sort="shap")
        self.assertIsInstance(fig, go.Figure)

    def test_plot_contributions(self):
        fig = self.explainer.plot_contributions(0)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_contributions(0, topx=3)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_contributions(0, sort='high-to-low')
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_contributions(0, sort='low-to-high')
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_contributions(0, sort='importance')
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_contributions(X_row=self.explainer.X.iloc[[0]])
        self.assertIsInstance(fig, go.Figure)

    def test_plot_pdp(self):
        fig = self.explainer.plot_pdp("Age")
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_pdp("Sex")
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_pdp("Sex", index=0)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_pdp("Age", index=0)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_pdp("Age", X_row=self.explainer.X.iloc[[0]])
        self.assertIsInstance(fig, go.Figure)

    def test_yaml(self):
        yaml = self.explainer.to_yaml()
        self.assertIsInstance(yaml, str)

    def test_residuals(self):
        self.assertIsInstance(self.explainer.residuals, pd.Series)

    def test_metrics(self):
        metrics_dict = self.explainer.metrics()
        self.assertIsInstance(metrics_dict, dict)
        self.assertTrue('root-mean-squared-error' in metrics_dict)
        self.assertTrue('mean-absolute-error' in metrics_dict)
        self.assertTrue('R-squared' in metrics_dict)
        self.assertIsInstance(self.explainer.metrics_descriptions(), dict) 

    def test_plot_predicted_vs_actual(self):
        fig = self.explainer.plot_predicted_vs_actual(logs=False)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_predicted_vs_actual(logs=True)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_predicted_vs_actual(log_x=True, log_y=True)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_residuals(self):
        fig = self.explainer.plot_residuals()
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_residuals(vs_actual=True)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_residuals(residuals='ratio')
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_residuals(residuals='log-ratio')
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_residuals(residuals='log-ratio', vs_actual=True)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_residuals_vs_feature(self):
        fig = self.explainer.plot_residuals_vs_feature("Age")
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_residuals_vs_feature("Age", residuals='log-ratio')
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_residuals_vs_feature("Age", dropna=True)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_residuals_vs_feature("Sex", points=False)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_residuals_vs_feature("Sex", winsor=10)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_y_vs_feature(self):
        fig = self.explainer.plot_y_vs_feature("Age")
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_y_vs_feature("Age", dropna=True)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_y_vs_feature("Sex", points=False)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_y_vs_feature("Sex", winsor=10)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_preds_vs_feature(self):
        fig = self.explainer.plot_preds_vs_feature("Age")
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_preds_vs_feature("Age", dropna=True)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_preds_vs_feature("Sex", points=False)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_preds_vs_feature("Sex", winsor=10)
        self.assertIsInstance(fig, go.Figure)


class CatBoostClassifierTests(unittest.TestCase):
    def setUp(self):
        X_train, y_train, X_test, y_test = titanic_survive()
        train_names, test_names = titanic_names()

        model = CatBoostClassifier(iterations=100, verbose=0).fit(X_train, y_train)
        explainer = ClassifierExplainer(
                            model, X_test, y_test, 
                            cats=['Deck', 'Embarked'],
                            labels=['Not survived', 'Survived'])

        X_cats, y_cats = explainer.X_merged, explainer.y.astype("int")
        model = CatBoostClassifier(iterations=5, verbose=0).fit(X_cats, y_cats, cat_features=[8, 9])
        self.explainer = ClassifierExplainer(model, X_cats, y_cats, 
                                cats=['Sex'], 
                                labels=['Not survived', 'Survived'],
                                idxs=X_test.index)

    def test_explainer_len(self):
        self.assertEqual(len(self.explainer), len(titanic_survive()[2]))

    def test_int_idx(self):
        self.assertEqual(self.explainer.get_idx(titanic_names()[1][0]), 0)

    def test_random_index(self):
        self.assertIsInstance(self.explainer.random_index(), int)
        self.assertIsInstance(self.explainer.random_index(return_str=True), str)

    def test_ordered_cats(self):
        self.assertEqual(self.explainer.ordered_cats("Sex"), ['NOT_ENCODED', 'Sex_female', 'Sex_male'])
        self.assertEqual(self.explainer.ordered_cats("Deck", topx=2, sort='alphabet'), ['Deck_A', 'Deck_B'])

        self.assertIsInstance(self.explainer.ordered_cats("Deck", sort='freq'), list)
        self.assertIsInstance(self.explainer.ordered_cats("Deck", topx=3, sort='freq'), list)
        self.assertIsInstance(self.explainer.ordered_cats("Deck", sort='shap'), list)
        self.assertIsInstance(self.explainer.ordered_cats("Deck", topx=3, sort='shap'), list)

    def test_preds(self):
        self.assertIsInstance(self.explainer.preds, np.ndarray)

    def test_row_from_input(self):
        input_row = self.explainer.get_row_from_input(
            self.explainer.X.iloc[[0]].values.tolist())
        self.assertIsInstance(input_row, pd.DataFrame)

        input_row = self.explainer.get_row_from_input(
            self.explainer.X_merged
            [self.explainer.columns_ranked_by_shap()]
            .iloc[[0]].values.tolist(), ranked_by_shap=True)
        self.assertIsInstance(input_row, pd.DataFrame)
        

    def test_pred_percentiles(self):
        self.assertIsInstance(self.explainer.pred_percentiles(), np.ndarray)

    def test_columns_ranked_by_shap(self):
        self.assertIsInstance(self.explainer.columns_ranked_by_shap(), list)

    def test_permutation_importances(self):
        self.assertIsInstance(self.explainer.get_permutation_importances_df(), pd.DataFrame)
        
    def test_X_cats(self):
        self.assertIsInstance(self.explainer.X_cats, pd.DataFrame)

    def test_metrics(self):
        self.assertIsInstance(self.explainer.metrics(), dict)

    def test_mean_abs_shap_df(self):
        self.assertIsInstance(self.explainer.get_mean_abs_shap_df(), pd.DataFrame)

    def test_top_interactions(self):
        self.assertIsInstance(self.explainer.top_shap_interactions("Age"), list)
        self.assertIsInstance(self.explainer.top_shap_interactions("Age", topx=4), list)

    def test_permutation_importances_df(self):
        self.assertIsInstance(self.explainer.get_permutation_importances_df(), pd.DataFrame)
        self.assertIsInstance(self.explainer.get_permutation_importances_df(topx=3), pd.DataFrame)
        self.assertIsInstance(self.explainer.get_permutation_importances_df(cutoff=0.01), pd.DataFrame)

    def test_contrib_df(self):
        self.assertIsInstance(self.explainer.get_contrib_df(0), pd.DataFrame)
        self.assertIsInstance(self.explainer.get_contrib_df(X_row=self.explainer.X.iloc[[0]]), pd.DataFrame)

    def test_shap_base_value(self):
        self.assertIsInstance(self.explainer.shap_base_value(), (np.floating, float))

    def test_shap_values_shape(self):
        self.assertTrue(self.explainer.get_shap_values_df().shape == (len(self.explainer), len(self.explainer.merged_cols)))

    def test_shap_values(self):
        self.assertIsInstance(self.explainer.get_shap_values_df(), pd.DataFrame)

    def test_calculate_properties(self):
        self.explainer.calculate_properties()

    def test_prediction_result_df(self):
        df = self.explainer.prediction_result_df(0)
        self.assertIsInstance(df, pd.DataFrame)

    def test_pdp_df(self):
        self.assertIsInstance(self.explainer.pdp_df("Age"), pd.DataFrame)
        self.assertIsInstance(self.explainer.pdp_df("Deck"), pd.DataFrame)
        self.assertIsInstance(self.explainer.pdp_df("Age", index=0), pd.DataFrame)
        self.assertIsInstance(self.explainer.pdp_df("Age", X_row=self.explainer.X.iloc[[0]]), pd.DataFrame)

    def test_plot_importances(self):
        fig = self.explainer.plot_importances()
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_importances(kind='permutation')
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_importances(topx=3)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_contributions(self):
        fig = self.explainer.plot_contributions(0)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_contributions(X_row=self.explainer.X.iloc[[0]], sort='importance')
        self.assertIsInstance(fig, go.Figure)


    def test_plot_shap_detailed(self):
        fig = self.explainer.plot_importances_detailed()
        self.assertIsInstance(fig, go.Figure)


    def test_plot_dependence(self):
        fig = self.explainer.plot_dependence("Age")
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_dependence("Sex")
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_dependence("Age", "Sex")
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_dependence("Sex", "Sex")
        self.assertIsInstance(fig, go.Figure)



    def test_plot_pdp(self):
        fig = self.explainer.plot_pdp("Age")
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_pdp("Sex")
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_pdp("Sex", index=0)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_pdp("Age", index=0)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_pdp("Age", X_row=self.explainer.X.iloc[[0]])
        self.assertIsInstance(fig, go.Figure)


    def test_yaml(self):
        yaml = self.explainer.to_yaml()
        self.assertIsInstance(yaml, str)

    def test_pos_label(self):
        self.explainer.pos_label = 1
        self.explainer.pos_label = "Not survived"
        self.assertIsInstance(self.explainer.pos_label, int)
        self.assertIsInstance(self.explainer.pos_label_str, str)
        self.assertEqual(self.explainer.pos_label, 0)
        self.assertEqual(self.explainer.pos_label_str, "Not survived")

    def test_pred_probas(self):
        self.assertIsInstance(self.explainer.pred_probas(), np.ndarray)

    
    def test_metrics(self):
        self.assertIsInstance(self.explainer.metrics(), dict)
        self.assertIsInstance(self.explainer.metrics(cutoff=0.9), dict)
        self.assertIsInstance(self.explainer.metrics_descriptions(cutoff=0.9), dict)


    def test_precision_df(self):
        self.assertIsInstance(self.explainer.get_precision_df(), pd.DataFrame)
        self.assertIsInstance(self.explainer.get_precision_df(multiclass=True), pd.DataFrame)
        self.assertIsInstance(self.explainer.get_precision_df(quantiles=4), pd.DataFrame)

    def test_lift_curve_df(self):
        self.assertIsInstance(self.explainer.get_liftcurve_df(), pd.DataFrame)

    def test_calculate_properties(self):
        self.explainer.calculate_properties()
        
    def test_plot_precision(self):
        fig = self.explainer.plot_precision()
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_precision(multiclass=True)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_precision(quantiles=10, cutoff=0.5)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_cumulative_precision(self):
        fig = self.explainer.plot_cumulative_precision()
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_cumulative_precision(percentile=0.5)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_cumulative_precision(percentile=0.1, pos_label=0)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_confusion_matrix(self):
        fig = self.explainer.plot_confusion_matrix(normalized=False, binary=False)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_confusion_matrix(normalized=False, binary=True)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_confusion_matrix(normalized=True, binary=False)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_confusion_matrix(normalized=True, binary=True)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_lift_curve(self):
        fig = self.explainer.plot_lift_curve()
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_lift_curve(percentage=True)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_lift_curve(cutoff=0.5)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_lift_curve(self):
        fig = self.explainer.plot_lift_curve()
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_lift_curve(percentage=True)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_lift_curve(cutoff=0.5)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_classification(self):
        fig = self.explainer.plot_classification()
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_classification(percentage=True)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_classification(cutoff=0)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_classification(cutoff=1)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_roc_auc(self):
        fig = self.explainer.plot_roc_auc(0.5)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_roc_auc(0.0)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_roc_auc(1.0)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_pr_auc(self):
        fig = self.explainer.plot_pr_auc(0.5)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_pr_auc(0.0)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_pr_auc(1.0)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_prediction_result(self):
        fig = self.explainer.plot_prediction_result(0)
        self.assertIsInstance(fig, go.Figure)