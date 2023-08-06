from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import tempfile
from pytest import importorskip
import numpy as np
import os
import joblib
import pandas as pd


y_clf = np.random.randint(0, 2, 100)
y_reg = np.random.uniform(0, 1, 100)
X_clf = np.random.normal(
    y_clf.reshape(1, 100) + np.arange(5).reshape(5, 1),
    0.5,
    size=(5, 100),
).T.astype('float32')
X_reg = np.random.normal(
    y_reg.reshape(1, 100) + np.arange(5).reshape(5, 1),
    0.5, size=(5, 100)
).T.astype('float32')
feature_names = list('abcde')

clf = RandomForestClassifier(n_estimators=10)
clf.fit(X_clf, y_clf)
reg = RandomForestRegressor(n_estimators=10)
reg.fit(X_reg, y_reg)


def test_pickle():
    from aict_tools.io import save_model

    with tempfile.TemporaryDirectory(prefix='aict_tools_test_') as tmpdir:
        model_path = os.path.join(tmpdir, 'model.pkl')
        save_model(clf, feature_names, model_path, label_text='classifier')

        clf_load = joblib.load(model_path)
        assert clf_load.feature_names == feature_names

    with tempfile.TemporaryDirectory(prefix='aict_tools_test_') as tmpdir:
        model_path = os.path.join(tmpdir, 'model.pkl')
        save_model(reg, feature_names, model_path, label_text='regressor')

        reg_load = joblib.load(model_path)
        assert reg_load.feature_names == feature_names
        assert np.all(reg.predict(X_reg) == reg_load.predict(X_reg))
        assert np.all(clf.predict(X_clf) == clf_load.predict(X_clf))


def test_pmml_classifier():
    importorskip('sklearn2pmml')
    importorskip('jpmml_evaluator')
    from aict_tools.pmml import PMMLModel
    from aict_tools.io import save_model

    with tempfile.TemporaryDirectory(prefix='aict_tools_test_') as tmpdir:
        model_path = os.path.join(tmpdir, 'model.pmml')
        save_model(clf, feature_names, model_path, label_text='classifier')

        model = PMMLModel(model_path)
        # order seems to be changing
        assert model.feature_names == feature_names

        proba = model.predict_proba(X_clf)
        assert np.allclose(proba[:, 1], clf.predict_proba(X_clf)[:, 1])

        # make sure pickle is also saved
        clf_load = joblib.load(model_path.replace('.pmml', '.pkl'))
        assert clf_load.feature_names == feature_names
        assert np.all(clf.predict(X_clf) == clf_load.predict(X_clf))


def test_pmml_regressor():
    importorskip('sklearn2pmml')
    importorskip('jpmml_evaluator')
    from aict_tools.pmml import PMMLModel
    from aict_tools.io import save_model

    with tempfile.TemporaryDirectory(prefix='aict_tools_test_') as tmpdir:
        model_path = os.path.join(tmpdir, 'model.pmml')
        save_model(reg, feature_names, model_path, label_text='regressor')

        model = PMMLModel(model_path)
        assert model.feature_names == feature_names
        assert np.allclose(model.predict(X_reg), reg.predict(X_reg))

        # make sure pickle is also saved
        reg_load = joblib.load(model_path.replace('.pmml', '.pkl'))
        assert reg_load.feature_names == feature_names
        assert np.all(reg.predict(X_reg) == reg_load.predict(X_reg))


def test_onnx_regressor():
    importorskip('skl2onnx')
    importorskip('onnxruntime')
    from aict_tools.io import save_model
    from aict_tools.onnx import ONNXModel

    with tempfile.TemporaryDirectory(prefix='aict_tools_test_') as tmpdir:
        model_path = os.path.join(tmpdir, 'model.onnx')
        save_model(clf, feature_names, model_path, label_text='classifier')

        model = ONNXModel(model_path)
        assert model.meta['model_author'] == 'aict-tools'
        assert model.meta['feature_names'].split(',') == feature_names
        assert model.feature_names == feature_names

        probas_onnx = model.predict_proba(X_clf)
        probas_skl = clf.predict_proba(X_clf)

        assert np.all(np.isclose(probas_onnx, probas_skl, rtol=1e-2, atol=1e-4))

        # make sure pickle is also saved
        clf_load = joblib.load(model_path.replace('.onnx', '.pkl'))
        assert clf_load.feature_names == feature_names
        assert np.all(clf.predict(X_clf) == clf_load.predict(X_clf))


def test_onnx_classifier():
    importorskip('skl2onnx')
    importorskip('onnxruntime')
    from aict_tools.io import save_model
    from aict_tools.onnx import ONNXModel

    with tempfile.TemporaryDirectory(prefix='aict_tools_test_') as tmpdir:
        model_path = os.path.join(tmpdir, 'model.onnx')
        save_model(reg, feature_names, model_path, label_text='regressor')

        model = ONNXModel(model_path)
        assert model.meta['model_author'] == 'aict-tools'
        assert model.meta['feature_names'].split(',') == feature_names
        assert model.feature_names == feature_names

        pred_onnx = reg.predict(X_reg)
        pred_skl = reg.predict(X_reg)

        assert np.all(np.isclose(pred_onnx, pred_skl))

        # make sure pickle is also saved
        reg_load = joblib.load(model_path.replace('.onnx', '.pkl'))
        assert reg_load.feature_names == feature_names
        assert np.all(reg.predict(X_reg) == reg_load.predict(X_reg))
