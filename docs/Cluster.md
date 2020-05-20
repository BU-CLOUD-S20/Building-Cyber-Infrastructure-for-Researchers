# Kubernetes Cluster
The Kubernetes Cluster is a DIY cluster created with ubuntu using an [openwhisk deployment guide](https://github.com/apache/openwhisk-deploy-kube/blob/master/docs/k8s-diy-ubuntu.md).

# Cluster Structure
The master node was created by using `ifconfig docker0` to get the IP of the network interface of docker running on the MOC VM.

To get the nodes of the cluster run: `kubectl get nodes`


