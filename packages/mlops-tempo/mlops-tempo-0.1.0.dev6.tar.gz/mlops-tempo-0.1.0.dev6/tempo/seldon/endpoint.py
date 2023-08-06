import os

from kubernetes import client, config

from tempo.serve.metadata import ModelDetails
from tempo.serve.protocol import Protocol
from tempo.utils import logger

ENV_K8S_SERVICE_HOST = "KUBERNETES_SERVICE_HOST"
ISTIO_GATEWAY = "istio"


class Endpoint(object):
    """A Model Endpoint

    Only handles istio and seldon at present.

    """

    def __init__(self, model_name, namespace, protocol: Protocol, gateway=ISTIO_GATEWAY):
        self.inside_cluster = os.getenv(ENV_K8S_SERVICE_HOST)
        try:
            if self.inside_cluster:
                logger.debug("Loading cluster local config")
                config.load_incluster_config()
            else:
                logger.debug("Loading external kubernetes config")
                config.load_kube_config()
        except Exception:
            logger.warning("Failed to load kubeconfig. Only local mode is possible.")
        self.gateway = gateway
        self.model_name = model_name
        self.namespace = namespace
        self.protocol = protocol

    def get_url(self, model_details: ModelDetails):
        if self.gateway == ISTIO_GATEWAY:
            if self.inside_cluster is None:
                api_instance = client.CoreV1Api()
                res = api_instance.list_namespaced_service(
                    "istio-system", field_selector="metadata.name=istio-ingressgateway"
                )
                ingress_ip = res.items[0].status.load_balancer.ingress[0].ip
                if not ingress_ip:
                    ingress_ip = res.items[0].status.load_balancer.ingress[0].hostname
                return (
                    f"http://{ingress_ip}/seldon/{self.namespace}/{self.model_name}"
                    + self.protocol.get_predict_path(model_details)
                )
            else:
                # TODO check why needed this here
                config.load_incluster_config()
                api_instance = client.CustomObjectsApi()
                api_response = api_instance.get_namespaced_custom_object_status(
                    "machinelearning.seldon.io",
                    "v1",
                    self.namespace,
                    "seldondeployments",
                    self.model_name,
                )
                return api_response["status"]["address"]["url"]
        else:
            raise ValueError(f"gateway {self.gateway} unknown")
