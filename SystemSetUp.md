# System Setup

Following are the components that needs to be setup for running BCIFR. 

Most of the system setup tutorials are coming from the official documents, because we don't want you to have version problems like us 

## 1. Kubernetes and OpenWhisk

install openwhisk on native ubuntu [[link]](https://github.com/apache/openwhisk/tree/master/tools/ubuntu-setup)

PS1: some software such as cryptography 2.8 may need to be installed or updated

PS2: use ansible-playbook -i setup.yml to automatically install couchdb

Creating a single control-plane cluster with kubeadm [[link]](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)

