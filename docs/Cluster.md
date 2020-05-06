# Kubernetes Cluster
Our Kubernetes cluster is created with kind version: using a kind-cluster.yaml file that can be found using `ls` as soon as you log into the VM.

The setup file specifies a code node and a worker nodes that have all been labeled as such using 
`kubectl label node kind-worker openwhisk-role=core`
`kubectl label node kind-worker2 openwhisk-role=invoker`
