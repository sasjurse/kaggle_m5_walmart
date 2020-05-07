# For local setup
# https://hub.docker.com/r/codait/max-text-sentiment-classifier
# docker run -it -p 5000:5000 codait/max-text-sentiment-classifier
# docker run -it -p 5432:5432 -e POSTGRES_PASSWORD='yolo' postgres:12.2

docker build -t twitterk8cr.azurecr.io/python-runner .

az acr login --name twitterk8cr
docker push twitterk8cr.azurecr.io/python-runner

kubectl delete -f deployments/dashboard.yaml
kubectl apply -f deployments/dashboard.yaml
