# System Setup

Following are the components that needs to be setup for running BCIFR. 

Most of the system setup tutorials are coming from the official documents, because we don't want you to have version problems like us 

## 1. Kubernetes and OpenWhisk

[install openwhisk on native ubuntu](https://github.com/apache/openwhisk/tree/master/tools/ubuntu-setup)

PS1: some software such as cryptography 2.8 may need to be installed or updated

PS2: use ansible-playbook -i setup.yml to automatically install couchdb

[Creating a single control-plane cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)

[Deploy OpenWhisk on kubernetes](https://github.com/apache/openwhisk-deploy-kube)

PS: if you choose MOC, that means you are using a Kubernetes cluster you built yourself

[Deploying OpenWhisk on kind](https://github.com/apache/openwhisk-deploy-kube/blob/master/docs/k8s-kind.md#configuring-openwhisk)

PS: Using kind is only appropriate for development and testing purposes. It is not recommended for production deployments of OpenWhisk.

[Scaling-up OpenWhisk Deployment on custom-built-kubernetes cluster](https://github.com/apache/openwhisk-deploy-kube/blob/master/docs/k8s-custom-build-cluster-scaleup.md)

PS: you can use helm upgrade to upgrade yaml

[Cluster Management](https://kubernetes.io/docs/tasks/administer-cluster/cluster-management/)

[join a node to the cluster](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-join/)

[Running in multiple zones](https://kubernetes.io/docs/setup/best-practices/multiple-zones/)

[Building large clusters](https://kubernetes.io/docs/setup/best-practices/cluster-large/)

[Creating Highly Available clusters with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/)
