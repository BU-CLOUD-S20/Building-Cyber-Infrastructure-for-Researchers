# Building-Cyber-Infrastructure-for-Researchers

### Mentors: Abraham Matta(matta@bu.edu), Ali Raza (araza@bu.edu)

### Team Members: Tian Chen（ct970808@bu.edu）, Donovan Jones（jonesde@bu.edu）, Komal Kango（komalk@bu.edu）, Jing Song(jingsong@bu.edu), Kristi Perreault（kristip@bu.edu） 
   <br/>	

## 1.  Vision and Goals Of The Project

<br/> The system will be a cloud based infrastructure that runs code written in Python or R over specified data sets to create and             compare models that predict ecological forecasts. High-Level Goals for this Project include:

   -   Providing a web service with a simple user experience such that researchers can submit code and periodically run it on data sets.
   -   Developing reliable infrastructure on unreliable nodes using a Kubernetes Cluster
   -   Focusing on Function as a Service with OpenWhisk as a proof of concept
   -   Providing a user interface that allows for comparisons between multiple models on the same data set along with comparisons of            models using periodic data sets in order to determine model accuracy.
   <br/>

## 2.  Users/ Personas of the Project 
<br/> The system will be deployed by system administrators and used by the end-users in the earth science department of BU. It targets end-users, specifically ecological       researchers. It does not target:

   -   Non-ecological Researchers
   -   Advanced users with complex requirements beyond the scope of the project.
   <br/>

## 3.  Scope and Features of the Project
<br/> UI: an easy-to-use web interface for users
   -   System Administrator: developers
        -   Approve project proposals from project leads
        -   Assign users as project leads
        -   Management of all existing projects and users in the system
        -   Access to information about the current VM cluster
   -   Project Leads: usually professors
        -   Approve requests from users to join projects (request received through email)
        -   Add or remove team members
        -   View the working progress of team members
   -   Team Members: usually graduate students
        -   Could be assigned as project leads/administrators
   -  Front-end features for all users
        -   User registration and login
        -   Allows changing password
        -   Allows search for specific projects and requests to join
        -   Management of all previous logs of computations
        -   Allows submission of new computation code
        -   Code submitted by users either through a link to the container or with code and libraries which are then put together into a container by Docker Hub
        -   Online editor for code input, instead of text box
        -   Trigger set by users to start executing the code
        -   Standardized visualization of output from running the code (extra z-axis in the plot being the the confidence of prediction)
        -   Comparison of different models over time on the same set of data
        -   Accuracy measurement of the prediction model by comparing it with real-time updated data 
    <br/>
    
<br/> Unreliable Nodes:
   -   Utilize Chameleon and GENI as the unreliable nodes to build infrastructure on top of
   -   Capability for infrastructure to "loan out" these nodes to services or applications as needed
   -   Monitor the availability of these nodes, including up/down time and proximity to data stores
   <br/>
    
<br/> Orchestration with Kubernetes:
   -   Allows for a consistent layer over which anything can be deployed. For this project, the focus is Function as a Service (FaaS) with OpenWhisk
   -   Determine where the code from the researchers will run depending on where it is stored
   -   Explore possibility of deploying Kubernetes Cluster on the Mass Open Cloud
   -   Provide a view of available nodes, including locations to data stores (stretch goal)
   <br/>


<br/> Compute with OpenWhisk: 
   -   Run OpenWhisk on Kubernetes cluster as first service offering for the Cyber Infrastructure platform
   -   Commands sent to OpenWhisk, which is running on a cluster determined by Kubernetes based on node availablity and location


<br/> Database Management: 
   -   User information stored and managed in MongoDB
   -   Store output of computation in DynamoDB (Dynamo allows computation configuration)

<br/> Security: provide secure storage of user data and computation output
<br/>
<br/>

## 4.  Solution Concept
<img src="https://github.com/BU-CLOUD-S20/Building-Cyber-Infrastructure-for-Researchers/blob/master/solution%20concept.PNG"><br/>

<br/> The main issue the team is attempting to solve is the unreliability of Chameleon and GENI nodes for running researcher's code. Chameleon and GENI are used due to their low cost, but the trade off is there is low availablity. By building an infrastructure layer over these nodes, and utilizing a Kubernetes cluster to orchestrate the use of nodes, researchers will be able to rely on this system to compute and store their data without having to overpay. As a proof of concept, the team will build this infrastructure layer with ecological researchers at BU in mind, and will first attempt to install OpenWhisk on the Kubernetes cluster to test the function as a service avenue. In addition, a basic UI will be provided to allow researchers to input code and compare data models, and system admins to manage access requests.
<br/>
<br/>
    
## 5.  Acceptance Criteria
<br/> The minimum acceptance criteria is an infrastructure service running OpenWhisk in a Kubernetes cluster, deployed to the MOC. The Kubernetes cluster orchestrates where the code runs based on node availablity and proximity to where the data is stored. In addition, a basic UI is provided for users to submit code, and system admin to monitor access requests. Stretch goals are:

   -   Preview of the node locations and availablity surfaced through the UI
   -   Optimization of node location and data store proximity
   -   More robust user experience
   <br/>

## 6a.  Release Planning - Proposed
<br/> For full release plans, please visit the team’s project space:
      https://tree.taiga.io/project/mosayyebzadeh-building-cyber-infrastructure-for-researchers/timeline

<br/> Release \#1 (due week 4) 
   -   Project goals determined and understood 
   -   Front end framework determined 
   -   New project created & outlined 
        -   User submission 
        -   User registration/login 
        -   Results display 
        -   Admin system

<br/> Release \#2 (due week 6) 
   -   UI Component
        -   User able to register for an account with email
        -   User able to login
        -   User data stored in MongoDB database
   -   Backend/Cloud Component 
        -   Install Openwhisk on a cluster
        -   Stand up a function to run on the cluster

<br/> Release \#3 (due week 8) 
   -   UI Component
        -   User can upload code in R via container link/code link
        -   Admin portal created with ability to manage users
   -   Backend/Cloud Component
        -   Ability to add and remove the unreliable Chameleon nodes

<br/> Release \#4 (due week 10)
   -   Submission portal
        -   User can upload code in python
   -   Results display
        -   Data visualization results compared to different models
   -   Admin system
        -   View system health
   -   O&S
        -   Distribute code
        -   Monitor VM availability

<br/> Release \#5 (due week 12)
   -   Results display
        -   Trigger set by users
        -   Ability to view previous results
        -   Real time data visualization

<br/> Release \#6 (due week 14) - TBD

<br/> Release \#7 (due week 16) - TBD

## 6b.  Release Planning - Actual

<br/> Release \#1 (due week 2) 
   -   Project goals determined and understood 
   -   Front end framework determined 
   -   New project created & outlined 
        -   User submission 
        -   User registration/login 
        -   Results display 
        -   Admin system

<br/> Release \#2 (due week 4) 
   -   UI Component
        -   User login & registration
        -   Dashboard
   -   Backend/Cloud Component 
        -   Access to MOC and OpenWhisk
        -   OpenWhisk running on one VM in MOC
        -   Code standards & team working agreement

<br/> Release \#3 (due week 6)
   -   UI Component
        -   Code submission page in UI
   -   Backend/Cloud Component 
        -   OpenWhisk API mock call from UI
        -   OpenWhisk on Kubernetes work started

<br/> Release \#4 (due week 8) - TBD

<br/> Release \#5 (due week 10) - TBD

<br/> Release \#6 (due week 12) - TBD

