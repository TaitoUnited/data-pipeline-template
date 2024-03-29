#!/usr/bin/env bash
# shellcheck disable=SC2034
# shellcheck disable=SC2154

##########################################################################
# Project specific settings
##########################################################################

# Taito CLI: Project specific plugins (for the selected database, etc.)
taito_plugins="
  ${taito_plugins}
  postgres-db sqitch-db
"

# Environments: In the correct order (e.g. dev test uat stag canary prod)
taito_environments="${template_default_environments}"

# Basic auth: Uncomment the line below to disable basic auth from ALL
# environments. Use env-prod.sh to disable basic auth from prod
# environment only.
# taito_basic_auth_enabled=false

# ------ Stack ------
# Configuration instructions:
# TODO

taito_containers=" bi lab server storage worker "
if [[ ${taito_env} == "local" ]]; then
  taito_containers="${taito_containers} database "
fi
taito_static_contents=
taito_databases=" database bidb "
taito_networks="default"

# Buckets
taito_buckets="bucket"
st_bucket_name="$taito_random_name-$taito_env"

# Additional databases
db_bidb_name=${taito_project//-/_}_bidb_${taito_env}
db_bidb_port=5001
if [[ ${taito_env} == "local" ]] || [[ ${taito_vpn_enabled} == "true" ]]; then
  db_bidb_port=5432
fi
db_bidb_mgr_username="${db_bidb_name}${db_database_username_suffix}"
db_bidb_mgr_secret="${db_bidb_name//_/-}-db-mgr.password"
db_bidb_app_username="${db_bidb_name}${db_database_app_user_suffix}${db_database_username_suffix}"
db_bidb_app_secret="${db_bidb_name//_/-}-db-app.password"
db_bidb_viewer_username="${db_bidb_name}${db_database_viewer_user_suffix}${db_database_username_suffix}"
db_bidb_viewer_secret="${db_bidb_name//_/-}-db-viewer.password"
db_bidb_default_username="${db_bidb_mgr_username}"
db_bidb_default_secret="${db_bidb_mgr_secret}"

# ------ Secrets ------
# Configuration instructions:
# https://taitounited.github.io/taito-cli/tutorial/06-env-variables-and-secrets/

# Secrets for all environments
taito_secrets="
  $db_database_app_secret:manual
  $db_bidb_app_secret:random
  $taito_project-$taito_env-django.secretKey:random-50
  $taito_project-$taito_env-api.apiKey:random-50
  $taito_project-$taito_env-api.apiKeyEtl:random-50
"

# Secrets for local environment only
taito_local_secrets="
  $taito_project-$taito_env-storage.accessKeyId:manual
  $taito_project-$taito_env-storage.secretKey:manual
"

# Secrets for non-local environments
# TODO: remove s3proxy secret if not Azure
taito_remote_secrets="
  $taito_project-$taito_env-basic-auth.auth:htpasswd-plain
  $taito_project-$taito_env-s3proxy.accessKeyId:random
  $taito_project-$taito_env-s3proxy.secretKey:random
  $db_database_viewer_secret:random
  $db_bidb_viewer_secret:random
  ${db_database_mgr_secret}${taito_cicd_secrets_path}:random
  ${db_bidb_mgr_secret}${taito_cicd_secrets_path}:random
  cicd-proxy-serviceaccount.key:read/common
"

# Secrets required by CI/CD
taito_cicd_secrets="
  cicd-proxy-serviceaccount.key
  $db_database_mgr_secret
  $db_database_ssl_ca_secret
  $db_database_ssl_cert_secret
  $db_database_ssl_key_secret
  $db_bidb_mgr_secret
  $db_bidb_ssl_ca_secret
  $db_bidb_ssl_cert_secret
  $db_bidb_ssl_key_secret
  $taito_project-$taito_env-django.secretKey
  $taito_project-$taito_env-api.apiKey
  $taito_project-$taito_env-api.apiKeyEtl
"

# Secrets required by CI/CD tests
taito_testing_secrets="
  $taito_project-$taito_env-basic-auth.auth
"

# Secret hints and descriptions
taito_secret_hints="
  * basic-auth=Basic authentication is used to hide non-production environments from public.
  * serviceaccount=Service account is typically used to access Cloud resources.
  * example=Just an example secret. You can type anything as a value.
"

# ------ Links ------
# Add custom links here. You can regenerate README.md links with
# 'taito project generate'. Configuration instructions: TODO

link_urls="
  * server[:ENV]=$taito_app_url/api/uptimez/ Server API status (:ENV)
  * git=https://$taito_vc_repository_url Git repository
"

if [[ ${taito_env} == "local" ]]; then
  link_urls="
    ${link_urls}
    * bi[:ENV]=$taito_app_url/superset/welcome/ Superset BI (:ENV)
    * admin[:ENV]=$taito_app_url/admin/ Django Admin (:ENV)
    * lab[:ENV]=$taito_app_url/lab Jupyter Lab (:ENV)
    * lessons[:ENV]=$taito_app_url/lab/tree/lessons/Contents.ipynb Lessons on Jupyter Lab (:ENV)
  "
fi
