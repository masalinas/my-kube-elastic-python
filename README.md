# Description
Connect to elasticsearch deployed in minikube from different sources validating SSL connections to recover all indices.

# Some local configurations
Edit the hosts file under **/etc/hosts** to set some IP aliases

```
127.0.0.1 avib-elastic
172.23.0.2 minikube.io
```

- The first entrance represent a **localhost IP alias** for the domain included in the elastic certificates default deployment, to validate certifcates in SSL connections
- The second entrance represent a **minikube cluster IP alias** to used in our requests from kubernetes Ingress


# Some elastic configurations
- Create first the proxy port-forward connecting to the port 9200 exposed by the elastic service

```
$ kubectl port-forward svc/avib-elastic 9200
```

- Create a elastic ingress entrance inside our minikube ingress controller to configure external connections to Elasticsearch. Write a **ingress-elastic.yaml** file like this:

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/backend-protocol: HTTPS
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    nginx.ingress.kubernetes.io/ssl-passthrough: "true"
  name: ingress-elastic
  namespace: default
spec:
  tls:
  - hosts:
    - minikube.io
    secretName: avib-elastic-certs
  rules:
  - host: minikube.io
    http:
      paths:
      - path: /elastic(/|$)(.*)
        pathType: ImplementationSpecific
        backend:
          service:
            name: avib-elastic
            port:
              number: 9200
```

Deploy the ingress in kubernetes:
```
$ kubectl apply -f ingress-elastic.yaml
```

# Some python configurations

Load python dependencies before execute any python sample

```
$ pip install -r requirements.txt
```

Recover root ca certificate value from elasticsearch secrets called **avib-elastic-certs** and attribute called  **ca.crt** from dashboard or executing
this command. Then paste the value inside a file called ca.crt used by our python or curl samples to validate our certifcates

```
$ kubectl get secrets avib-elastic-certs -o jsonpath='{.data}'
```

# Testing our elastic server from different sources and validating the SSL connections:

1) Recover indices from proxy port-forward just created. Not validating the SSL connection

```
$ curl -k -u elastic https://localhost:9200/_cat/indices
green open patients_1000    WaQ1vUAcRwysAuzyNTKpRA 1 0    1000 0 124.4kb 124.4kb
green open patients_10000   -cmyUQ1RQIql1Bf0ev4t3w 1 0   10000 0   1.1mb   1.1mb
green open patients_1000000 esGSW_h3Q9avWjnN5Wa9GA 1 0 1000000 0 112.2mb 112.2mb
green open patients_100000  zAimCaWbTyaZhO2liBPVnA 1 0  100000 0  11.1mb  11.1mb
```

2) Recover indices from ingress controlle just created.  Not validating the SSL connection
```
$ curl -k -u elastic https://minikube.io/elastic/_cat/indices
Enter host password for user 'elastic':
green open patients_1000    WaQ1vUAcRwysAuzyNTKpRA 1 0    1000 0 124.4kb 124.4kb
green open patients_10000   -cmyUQ1RQIql1Bf0ev4t3w 1 0   10000 0   1.1mb   1.1mb
green open patients_1000000 esGSW_h3Q9avWjnN5Wa9GA 1 0 1000000 0 112.2mb 112.2mb
green open patients_100000  zAimCaWbTyaZhO2liBPVnA 1 0  100000 0  11.1mb  11.1mb
```

3)Recover indices from proxy port-forward just created but using a localhost alias included in elastic cerficates. Validating the SSL connection
```
$ curl -u elastic --cacert ca.crt https://avib-elastic:9200/_cat/indices
green open patients_1000    WaQ1vUAcRwysAuzyNTKpRA 1 0    1000 0 124.4kb 124.4kb
green open patients_10000   -cmyUQ1RQIql1Bf0ev4t3w 1 0   10000 0   1.1mb   1.1mb
green open patients_1000000 esGSW_h3Q9avWjnN5Wa9GA 1 0 1000000 0 112.2mb 112.2mb
green open patients_100000  zAimCaWbTyaZhO2liBPVnA 1 0  100000 0  11.1mb  11.1mb
```

4) Recover indices from elastic python adapter.

We can recover indices using three different types of connections
- A domain included inside the certificates autogenerate by elastic when installed. In our because we don't specifie any configuration for it
so the domain used by elastic is the default service used to expose elastic for example 'avib-elastic', 'avib-elastic.default', 'avib-elastic.default.svc'
In this case we can recover the ca.crt file from kubernetes secrets and pass it to python adpater with the attribute **verify_certs**=True in our python client

- A domain represent our ingress configuration. In this case this domain is not included in the certificates so we can not validate our certificate autoasign.
So we must to set the attribute **verify_certs**=False in our python client

- A domain from our proxy port-forward. Also in this case  the domain is not inckluded in the certificates


execute the python sample
```
python3 main.py
{'patients_1000': {'aliases': {}}, 'patients_10000': {'aliases': {}}, 'patients_1000000': {'aliases': {}}, 'patients_100000': {'aliases': {}}}
```
