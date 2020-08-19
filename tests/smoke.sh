#!/usr/bin/env bash

export XDG_CONFIG_HOME="$(pwd)/tests"
export CLUSTER_NAME="kube-janitor-smoke-tests"
python main.py

helm lint charts/kube-janitor