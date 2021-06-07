#!/bin/bash -e
: "${taito_company:?}"
: "${taito_vc_repository:?}"
: "${taito_vc_repository_alt:?}"

if [[ ${taito_verbose:-} == "true" ]]; then
  set -x
fi

# Remove the example site
rm -rf www/site
sed -i '/\/site\/node_modules" # FOR GATSBY ONLY/d' docker-compose.yaml
sed -i '/\/site\/node_modules" # FOR GATSBY ONLY/d' docker-compose-remote.yaml

# Replace some strings
echo "Replacing project and company names in files. Please wait..."
find . -type f -exec sed -i \
  -e "s/data_pipeline_template/${taito_vc_repository_alt}/g" 2> /dev/null {} \;
find . -type f -exec sed -i \
  -e "s/data-pipeline-template/${taito_vc_repository}/g" 2> /dev/null {} \;
find . -type f -exec sed -i \
  -e "s/datapipelinetemplate/${taito_vc_repository//-/}/g" 2> /dev/null {} \;
find . -type f -exec sed -i \
  -e "s/companyname/${taito_company}/g" 2> /dev/null {} \;
find . -type f -exec sed -i \
  -e "s/DATA-PIPELINE-TEMPLATE/data-pipeline-template/g" 2> /dev/null {} \;

# Generate ports
echo "Generating unique random ports (avoid conflicts with other projects)..."
if [[ ! $ingress_port ]]; then ingress_port=$(shuf -i 8000-9999 -n 1); fi
sed -i "s/9999/${ingress_port}/g" \
  scripts/taito/DEVELOPMENT.md \
  scripts/taito/TAITOLESS.md \
  scripts/taito/config/main.sh \
  scripts/taito/env-local.sh \
  docker-compose.yaml \
    &> /dev/null || :

./scripts/taito-template/common.sh
echo init done
