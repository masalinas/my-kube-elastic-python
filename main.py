from elasticsearch import Elasticsearch

ES_HOST_1 = "https://localhost:9200" # Host expose from a kubernetes proxy port-forward
ES_HOST_2 = "https://minikube.io:443/elastic" # Host expose from a ingress controller
ES_HOST_3 = "https://avib-elastic:9200" # Host expose from a kubernetes proxy port-forward but using a domain alias included inside elastic certs
ES_HOST_4 = "https://avispe.edv.uniovi.es:443/kubernetes/elastic" # Host expose from a ingress controller
ES_USERNAME = "elastic"
ES_PASSWORD = "password"
ES_CA_CERTS_01 = "ca-elastic-local.crt"
ES_CA_CERTS_02 = "ca-elastic-avib.crt"

# Create the client instance. Only ES_HOST_3 or ES_HOST_4 ca use TLS validation because when
es = Elasticsearch(
    ES_HOST_4,
    basic_auth=(ES_USERNAME, ES_PASSWORD),
    ca_certs=ES_CA_CERTS_02,
    verify_certs=True
)

# get elastic health
print("Elasticsearch cluster health:")
resp = es.cluster.health()
print(resp)

print("")

# get all indices from elastic
print("Get Elasticsearch indices:")
resp = es.indices.get_alias(index="*")
print(resp)
