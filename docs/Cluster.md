# Kubernetes Cluster
The Kubernetes Cluster is a DIY cluster created with on an Ubuntu LTS 18.04 VM on the MOC using an [openwhisk deployment guide](https://github.com/apache/openwhisk-deploy-kube/blob/master/docs/k8s-diy-ubuntu.md).

# Cluster Structure
The master node was created by using `ifconfig docker0` to get the IP of the network interface of docker running on the MOC VM.

To get the nodes of the cluster run: `kubectl get nodes`

Nodes can be added with:
`kubeadm join 172.17.0.1:6443 --token 29am26.3fw2znktwbbff0we \
    --discovery-token-ca-cert-hash sha256:eb32f7f58ae6907f26ed5c075ecd4ef6756d832b6c358fd4b2f408e52d18a369`

