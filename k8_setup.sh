az group create --name k8group --location northeurope

# create cluster
az aks create --resource-group k8group \
  --name twitterk8 \
  --node-count 2 \
  --location eastus \
  --enable-addons monitoring \
   --node-vm-size Standard_D2_v3

# Get access to cluster with kubectl
az aks get-credentials --resource-group  k8group --name twitterk8

# Create container registry
az acr create --resource-group k8group --name twitterk8cr --sku Basic
az acr login --name twitterk8cr

# Give the cluster access to the container registry
az aks update -n twitterk8 -g k8group --attach-acr twitterk8cr

# push the first image
docker tag codait/max-text-sentiment-classifier twitterk8cr.azurecr.io/sentiment_classifier
docker push twitterk8cr.azurecr.io/sentiment_classifier

# kubectl apply -f classifier_api.yaml
# kubectl get pods
# kubectl logs -p add-tweets-1588430880-k66jb
# kubectl exec -it {pod_name} printenv

