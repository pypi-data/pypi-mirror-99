import unittest

import pandas as pd
import numpy as np
from pandas.api.types import is_categorical_dtype, is_numeric_dtype

from sklearn.ensemble import RandomForestClassifier

import plotly.graph_objects as go

from explainerdashboard.explainers import ClassifierExplainer
from explainerdashboard.datasets import titanic_survive, titanic_names


class ClassifierExplainerTests(unittest.TestCase):
    def setUp(self):
        X_train, y_train, X_test, y_test = titanic_survive()
        train_names, test_names = titanic_names()

        model = RandomForestClassifier(n_estimators=5, max_depth=2)
        model.fit(X_train, y_train)

        self.explainer = ClassifierExplainer(model, X_test, y_test,  
                            cats=[{'Gender': ['Sex_female', 'Sex_male', 'Sex_nan']}, 
                                                'Deck', 'Embarked'],
                            cats_notencoded={'Gender':'No Gender'},
                            idxs=test_names, 
                            labels=['Not survived', 'Survived'])

    def test_pos_label(self):
        self.explainer.pos_label = 1
        self.explainer.pos_label = "Not survived"
        self.assertIsInstance(self.explainer.pos_label, int)
        self.assertIsInstance(self.explainer.pos_label_str, str)
        self.assertEqual(self.explainer.pos_label, 0)
        self.assertEqual(self.explainer.pos_label_str, "Not survived")

    def test_custom_metrics(self):
        def meandiff_metric1(y_true, y_pred):
            return np.mean(y_true)-np.mean(y_pred)

        def meandiff_metric2(y_true, y_pred, cutoff):
            return np.mean(y_true)-np.mean(np.where(y_pred>cutoff, 1, 0))

        def meandiff_metric3(y_true, y_pred, pos_label):
            return np.mean(np.where(y_true==pos_label, 1, 0))-np.mean(y_pred[:, pos_label])

        def meandiff_metric4(y_true, y_pred, cutoff, pos_label):
            return np.mean(np.where(y_true==pos_label, 1, 0))-np.mean(np.where(y_pred[:, pos_label] > cutoff, 1, 0))

        metrics = np.array(list(self.explainer.metrics(
            show_metrics=[meandiff_metric1, meandiff_metric2, meandiff_metric3, meandiff_metric4]
            ).values()))
        self.assertTrue(np.all(metrics==metrics[0]))


    def test_pred_probas(self):
        self.assertIsInstance(self.explainer.pred_probas(), np.ndarray)
        self.assertIsInstance(self.explainer.pred_probas(1), np.ndarray)
        self.assertIsInstance(self.explainer.pred_probas("Survived"), np.ndarray)

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

    def test_plot_cumulutive_precision(self):
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

        fig = self.explainer.plot_lift_curve(add_wizard=False, round=3)
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


if __name__ == '__main__':
    unittest.main()

