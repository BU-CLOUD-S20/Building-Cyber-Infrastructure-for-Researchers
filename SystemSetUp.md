# System Setup

Following are the components that needs to be setup for running BCIFR. 

Most of the system setup tutorials are coming from the official documents, because we don't want you to have version problems like us 

## 1. Kubernetes and OpenWhisk

[install openwhisk on native ubuntu](https://github.com/apache/openwhisk/tree/master/tools/ubuntu-setup)

PS1: some software such as cryptography 2.8 may need to be installed or updated

PS2: use ansible-playbook -i setup.yml to automatically install couchdb

[Creating a single control-plane cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)

[Deploy OpenWhisk on kubernetes](https://github.com/apache/openwhisk-deploy-kube#using-a-kubernetes-cluster-you-built-yourself)

PS: if you choose MOC, that means you are using a Kubernetes cluster you built yourself

[Deploying OpenWhisk on kind](https://github.com/apache/openwhisk-deploy-kube/blob/master/docs/k8s-kind.md#configuring-openwhisk)

PS: Using kind is only appropriate for development and testing purposes. It is not recommended for production deployments of OpenWhisk.

[Scaling-up OpenWhisk Deployment on custom-built-kubernetes cluster](https://github.com/apache/openwhisk-deploy-kube/blob/master/docs/k8s-custom-build-cluster-scaleup.md)

PS: you can use helm upgrade to upgrade yaml

[Cluster Management](https://kubernetes.io/docs/tasks/administer-cluster/cluster-management/)

[join a node to the cluster](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/#join-nodes)

[Running in multiple zones](https://kubernetes.io/docs/setup/best-practices/multiple-zones/)

[Building large clusters](https://kubernetes.io/docs/setup/best-practices/cluster-large/)

[Creating Highly Available clusters with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/)

<br>

## 2. Web Interface

- Local Depolyment

  - Git clone the project to your local directory <br>
        `git clone https://github.com/BU-CLOUD-S20/Building-Cyber-Infrastructure-for-Researchers.git`
    
  - [Set up local environment](https://flask.palletsprojects.com/en/1.1.x/installation/#installation) <br>
        - Create the enviroment: `python3 -m venv venv` or `py -3 -m venv venv` on Windows <br>
        - Activivate the environment: `. venv/bin/activate` or `venv\Scripts\activate` <br>
        - Install Flask: `pip install Flask` <br>
        - Install virtualenv: `sudo python2 Downloads/get-pip.py` and then `sudo python2 -m pip install virtualenv` <br>
  
  - Set up local MongoDB <br>
        - [Download MongoDB community edition](https://docs.mongodb.com/manual/installation/#tutorial-installation) according to your operating system and following the installation guide <br>
        - Run Mongo Shell (mongo.exe)  <br>
        - Create a new database "admin": `use admin` <br>
        - Create collections "tempusers", "projects", "wsk_results": <br>
              `db.createCollection("tempusers")` <br>
              `db.createCollection("projects")` <br>
              `db.createCollection("wsk_results")` <br>
            
  - Run Application: `python -m flask run` <br>
            
- Web Server http://ecoforecast.bu.edu <br>
  - Once the flask module is successfully deployed on the webserver, our users would be able to access our web interface via http://ecoforecast.bu.edu

