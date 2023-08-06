# workstation-cli

This tool registers a work station given a daas-token generated from DaaS Website.

## prerequisites

- python >=3.6
- openssl

## Install

```bash
pip install sourcesense-vessel
```

## Usage

```bash
Usage: vessel-cli [OPTIONS] COMMAND [ARGS]...

  Vessel cli tool

Options:
  --debug    output debug log [False]
  --version  Show version and exits
  --help     Show this message and exit.

Commands:
  completion  Install completion script
  deployment  Generated and Deploy agent, sentinel and event-engine...
  init        Init vault
  kubebench
  register    Register workstaion to Vessel with the given TOKEN
  unseal      Unseal vault
  update      Updates agent and sentinel deployments


```

### Register

```bash
Usage: vessel-cli register [OPTIONS] TOKEN

  Register workstaion to Vessel with the given TOKEN

Options:
  --cluster-host TEXT  Hostname of the cluster to control  [required]
  --cluster-ro TEXT    Cluster read-only service-account token  [required]
  --cluster-rw TEXT    Cluster read-write service-account token  [required]
  --vault TEXT         Vault endpoint [http://vault.local]
  --openshift          Cluster is an Openshift distribution [False]
  --init               Initialize Vault [False]
  --deploy             Deploy agent and sentinel container automatically
                       [False]

  --vessel-api TEXT    Vessel API RPC endpoint [http://cloud-
                       api.oc.corp.sourcesense.com/rpc]

  --help               Show this message and exit.
```

### Deployment

```bash
Usage: vessel-cli deployment [OPTIONS] TOKEN

  Generated and Deploy agent, sentinel and event-engine deployments to
  internal kubernetes for given TOKEN

Options:
  --sentinel TEXT  Generates sentinel at given tag [None]
  --agent TEXT     Generates agent yaml at given tag [None]
  --event TEXT     Generates event-engine yaml at given tag [None]
  --apply          run kubectl apply on generated deployments [False]
  --help           Show this message and exit.
```

### development tests

From inside the vagrant box `workstation-ansible` you can register a cluster this way after obtained the `<TOKEN>` from the webapp:

```bash
vessel-cli init
# choose a password

vessel-cli --debug register --cluster-host https://192.168.58.2:6443 --cluster-ro $DAAS_CLU_READER_TOKEN --cluster-rw $DAAS_MANAGER_TOKEN <TOKEN>

# apply deployemnts of agent sentinel and event-engine
vessel-cli deployment --event latest --sentinel latest --agent latest --apply

```

## Configure prometheus

Update alertmanager.tyaml config

`kubectl -n monitoring create secret generic alertmanager-prometheus-kube-prometheus-alertmanager --dry-run=client -o yaml --from-file=alertmanager.yaml | kubectl -n monitoring apply -f -`

## DEBUG

```bash
# setup python environment
brew install pyenv
pyenv install 3.7.7
echo eval "$(pyenv init -)" > ~/.bashrc

pyenv global 3.7.7
pyenv virtualenv vessel
pyenv local vessel

python setup.py develop
```
