import unittest

import pandas as pd
from pandas.api.types import is_categorical_dtype, is_numeric_dtype

from sklearn.ensemble import RandomForestRegressor
import plotly.graph_objects as go

from explainerdashboard.explainers import RegressionExplainer
from explainerdashboard.datasets import titanic_fare, titanic_names


class RegressionBunchTests(unittest.TestCase):
    def setUp(self):
        X_train, y_train, X_test, y_test = titanic_fare()
        self.test_len = len(X_test)

        train_names, test_names = titanic_names()
        _, self.names = titanic_names()

        model = RandomForestRegressor(n_estimators=5, max_depth=2)
        model.fit(X_train, y_train)

        self.explainer = RegressionExplainer(
                            model, X_test, y_test, 
                            cats=[{'Gender': ['Sex_female', 'Sex_male', 'Sex_nan']}, 
                                                'Deck', 'Embarked'],
                            cats_notencoded={'Gender':'No Gender'},
                            idxs=test_names)

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

        fig = self.explainer.plot_residuals_vs_feature("Gender", points=False)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_residuals_vs_feature("Gender", winsor=10)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_y_vs_feature(self):
        fig = self.explainer.plot_y_vs_feature("Age")
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_y_vs_feature("Age", dropna=True)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_y_vs_feature("Gender", points=False)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_y_vs_feature("Gender", winsor=10)
        self.assertIsInstance(fig, go.Figure)

    def test_plot_preds_vs_feature(self):
        fig = self.explainer.plot_preds_vs_feature("Age")
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_preds_vs_feature("Age", dropna=True)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_preds_vs_feature("Gender", points=False)
        self.assertIsInstance(fig, go.Figure)

        fig = self.explainer.plot_preds_vs_feature("Gender", winsor=10)
        self.assertIsInstance(fig, go.Figure)


if __name__ == '__main__':
    unittest.main()

