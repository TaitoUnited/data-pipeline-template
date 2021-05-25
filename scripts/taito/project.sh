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

taito_containers="bi lab worker"
if [[ ${taito_env} == "local" ]]; then
  taito_containers="${taito_containers} database "
fi
taito_static_contents=
taito_databases="database"
taito_networks="default"

# Buckets
taito_buckets="bucket"
st_bucket_name="$taito_random_name-$taito_env"

# ------ Secrets ------
# Configuration instructions:
# https://taitounited.github.io/taito-cli/tutorial/06-env-variables-and-secrets/

# Secrets for all environments
taito_secrets="
  $db_database_app_secret:random
  $db_bi_app_secret:random
"

# Secrets for local environment only
taito_local_secrets="
"

# Secrets for non-local environments
taito_remote_secrets="
  $taito_project-$taito_env-basic-auth.auth:htpasswd-plain
  $taito_project-$taito_env-storage.accessKeyId:manual
  $taito_project-$taito_env-storage.secretKey:manual
  $db_database_viewer_secret:random
  $db_bi_viewer_secret:random
  ${db_database_mgr_secret}${taito_cicd_secrets_path}:random
  ${db_bi_mgr_secret}${taito_cicd_secrets_path}:random
  cicd-proxy-serviceaccount.key:read/common
"

# Secrets required by CI/CD
taito_cicd_secrets="
  cicd-proxy-serviceaccount.key
  $db_database_mgr_secret
  $db_database_ssl_ca_secret
  $db_database_ssl_cert_secret
  $db_database_ssl_key_secret
  $db_bi_mgr_secret
  $db_bi_ssl_ca_secret
  $db_bi_ssl_cert_secret
  $db_bi_ssl_key_secret
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
  * bi[:ENV]=$taito_app_url/superset/welcome/ Superset BI (:ENV)
  * lab[:ENV]=$taito_app_url/lab Jupyter Lab (:ENV)
  * lessons[:ENV]=$taito_app_url/lab/tree/lessons/Contents.ipynb Lessons on Jupyter Lab (:ENV)
  * git=https://$taito_vc_repository_url Git repository
"
