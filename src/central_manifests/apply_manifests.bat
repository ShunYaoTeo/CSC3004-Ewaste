@echo off
setlocal

:: Set your base path here, or pass as a command line argument
set BASE_PATH=%~1
if "%BASE_PATH%"=="" (
    echo Base path not set. Please pass the base path as a command line argument.
    exit /b 1
)

:: Function to apply manifests
:applyManifests
for %%f in (%BASE_PATH%\%~1\%~2) do (
    kubectl apply -f %%f
)
exit /b 0

:: Apply DB manifests in order
call :applyManifests auth_manifests\auth_db_manifests db-auth-configmap.yaml
call :applyManifests auth_manifests\auth_db_manifests db-auth-pvc.yaml
call :applyManifests auth_manifests\auth_db_manifests db-secrets.yaml
call :applyManifests auth_manifests\auth_db_manifests db-auth-deploy.yaml
call :applyManifests auth_manifests\auth_db_manifests db-auth-service.yaml

call :applyManifests ewaste_manifests\ewaste_db_manifests db-ewaste-configmap.yaml
call :applyManifests ewaste_manifests\ewaste_db_manifests db-ewaste-pvc.yaml
call :applyManifests ewaste_manifests\ewaste_db_manifests db-secrets.yaml
call :applyManifests ewaste_manifests\ewaste_db_manifests db-ewaste-deploy.yaml
call :applyManifests ewaste_manifests\ewaste_db_manifests db-ewaste-service.yaml

call :applyManifests rewards_manifests\rewards_db_manifests db-rewards-configmap.yaml
call :applyManifests rewards_manifests\rewards_db_manifests db-rewards-pvc.yaml
call :applyManifests rewards_manifests\rewards_db_manifests db-secrets.yaml
call :applyManifests rewards_manifests\rewards_db_manifests db-rewards-deploy.yaml
call :applyManifests rewards_manifests\rewards_db_manifests db-rewards-service.yaml

:: Apply service manifests
call :applyManifests gateway_manifests *.yaml
call :applyManifests auth_manifests *.yaml
call :applyManifests ewaste_manifests *.yaml
call :applyManifests rewards_manifests *.yaml
