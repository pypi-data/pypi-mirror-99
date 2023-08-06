import pytest

from tempo.seldon.k8s import SeldonKubernetesRuntime
from tempo.serve.metadata import ModelFramework
from tempo.serve.model import Model


@pytest.mark.parametrize(
    "expected",
    [
        """apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: test-iris-sklearn
  namespace: default
spec:
  predictors:
  - graph:
      implementation: SKLEARN_SERVER
      modelUri: gs://seldon-models/sklearn/iris
      name: test-iris-sklearn
      type: MODEL
    name: default
    replicas: 1
  protocol: seldon
"""
    ],
)
def test_seldon_sklearn_model_yaml(expected):
    m = Model(
        name="test-iris-sklearn",
        runtime=SeldonKubernetesRuntime(),
        platform=ModelFramework.SKLearn,
        uri="gs://seldon-models/sklearn/iris",
        local_folder="",
    )
    assert m.to_k8s_yaml() == expected


@pytest.mark.parametrize(
    "expected",
    [
        """apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: test-iris-xgboost
  namespace: default
spec:
  predictors:
  - graph:
      implementation: XGBOOST_SERVER
      modelUri: gs://seldon-models/xgboost/iris
      name: test-iris-xgboost
      type: MODEL
    name: default
    replicas: 1
  protocol: seldon
"""
    ],
)
def test_seldon_xgboost_model_yaml(expected):
    m = Model(
        name="test-iris-xgboost",
        runtime=SeldonKubernetesRuntime(),
        platform=ModelFramework.XGBoost,
        uri="gs://seldon-models/xgboost/iris",
        local_folder="",
    )
    assert m.to_k8s_yaml() == expected
