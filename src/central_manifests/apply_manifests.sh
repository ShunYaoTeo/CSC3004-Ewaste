#!/bin/bash

# Check if the user has provided a base path
if [ $# -eq 0 ]
  then
    echo "No base path provided. Exiting."
    exit 1
fi

# Base path provided by user
BASE_PATH=$1

# Define the services and their order
SERVICES=("auth" "ewaste" "rewards")

# Apply DB manifests for each service
for service in "${SERVICES[@]}"
do
  echo "Applying ${service}_db_manifests..."
  
  kubectl apply -f ${BASE_PATH}/${service}_manifests/${service}_db_manifests/db-${service}-configmap.yaml
  kubectl apply -f ${BASE_PATH}/${service}_manifests/${service}_db_manifests/db-${service}-pvc.yaml
  kubectl apply -f ${BASE_PATH}/${service}_manifests/${service}_db_manifests/db-secrets.yaml
  kubectl apply -f ${BASE_PATH}/${service}_manifests/${service}_db_manifests/db-${service}-deploy.yaml
  kubectl apply -f ${BASE_PATH}/${service}_manifests/${service}_db_manifests/db-${service}-service.yaml
done

# Apply the gateway manifests
echo "Applying gateway_manifests..."
kubectl apply -f ${BASE_PATH}/gateway_manifests/.

# Apply remaining manifests for each service
for service in "${SERVICES[@]}"
do
  echo "Applying ${service}_manifests..."
  kubectl apply -f ${BASE_PATH}/${service}_manifests/.
done

echo "Done."
