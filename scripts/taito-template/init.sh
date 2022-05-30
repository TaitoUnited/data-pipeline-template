#!/bin/bash -e
: "${taito_company:?}"
: "${taito_vc_repository:?}"
: "${taito_vc_repository_alt:?}"

if [[ ${taito_verbose:-} == "true" ]]; then
  set -x
fi

echo
echo
echo "######################"
echo "#    Choose stack"
echo "######################"
echo
echo "If you are unsure, just accept the defaults."
echo

function prune () {
  local message=$1
  local name=$2

  echo
  read -r -t 1 -n 1000 || :
  read -p "$message" -n 1 -r confirm
  if ( [[ "$message" == *"[y/N]"* ]] && ! [[ "${confirm}" =~ ^[Yy]$ ]] ) || \
     ( [[ "$message" == *"[Y/n]"* ]] && ! [[ "${confirm}" =~ ^[Yy]*$ ]] ); then
    echo
    echo "  Removing ${name}..."
    rm -rf "$name"
    sed -i "s/ $name / /" scripts/taito/project.sh

    if [[ $name == "bi" ]]; then
      sed -i "s/ bidb / /" scripts/taito/project.sh

      rm -rf database/local-bi-db.sh

      sed -i "/^  data_pipeline_template-bi:\r*\$/,/^\r*$/d" docker-compose.yaml
      sed -i "/^  data_pipeline_template-biinit:\r*\$/,/^\r*$/d" docker-compose.yaml
      sed -i "/^  data_pipeline_template-biworker:\r*\$/,/^\r*$/d" docker-compose.yaml
      sed -i "/^  data_pipeline_template-bibeat:\r*\$/,/^\r*$/d" docker-compose.yaml
      sed -i "/^  data_pipeline_template-redis:\r*\$/,/^\r*$/d" docker-compose.yaml

      sed -i "/^        # BI API: Superset api\r*\$/,/^        }\r*$/d" docker-nginx.conf
      sed -i "/^        # BI: Superset\r*\$/,/^        }\r*$/d" docker-nginx.conf

      sed -i "/^# Additional databases\r*\$/,/^\r*$/d" scripts/taito/project.sh

      sed -i '/superset/d' scripts/taito/project.sh
      sed -i '/Superset/d' docker-compose.yaml

      sed -i '/BIDB_/d' docker-compose.yaml
      sed -i '/bidb_/d' docker-compose.yaml
      sed -i '/bidb_/d' scripts/taito/env-local.sh
      sed -i '/bidb_/d' scripts/taito/project.sh
    fi
  fi
}

prune "Include Apache Superset (bi)? [y/N] " bi

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
if [[ ! $server_debug_port ]]; then server_debug_port=$(shuf -i 4000-4999 -n 1); fi
if [[ ! $storage_port ]]; then storage_port=$(shuf -i 2000-2999 -n 1); fi
sed -i "s/8888/${storage_port}/g" \
  docker-compose.yaml \
  scripts/taito/env-local.sh \
  scripts/taito/TAITOLESS.md &> /dev/null || :
sed -i "s/4229/${server_debug_port}/g" \
  docker-compose.yaml \
  .vscode/launch.json &> /dev/null || :
sed -i "s/9999/${ingress_port}/g" \
  scripts/taito/DEVELOPMENT.md \
  scripts/taito/TAITOLESS.md \
  scripts/taito/config/main.sh \
  scripts/taito/env-local.sh \
  docker-compose.yaml \
    &> /dev/null || :

./scripts/taito-template/common.sh
echo init done
