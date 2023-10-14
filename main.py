from elasticsearch import Elasticsearch

ES_HOST_1 = "https://localhost:9200" # Host expose from a kubernetes proxy port-forward
ES_HOST_2 = "https://minikube.io:443/elastic" # Host expose from a ingress controller
ES_HOST_3 = "https://avib-elastic:9200" # Host expose from a kubernetes proxy port-forward but using a domain alias included inside elastic certs
ES_USERNAME = "elastic"
ES_PASSWORD = "password"
ES_CA_CERTS = "ca.crt"

# Create the client instance. Only ES_HOST_3 ca use TLS validation because when
es = Elasticsearch(
    ES_HOST_3,
    basic_auth=(ES_USERNAME, ES_PASSWORD),
    ca_certs=ES_CA_CERTS,
    verify_certs=True
)

# get all indices from elastic
resp = es.indices.get_alias(index="*")
print(resp)
