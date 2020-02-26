# Building-Cyber-Infrastructure-for-Researchers

### Mentors: Abraham Matta(matta@bu.edu), Ali Raza (araza@bu.edu)

### Team Members: Tian Chen（ct970808@bu.edu）, Donovan Jones（jonesde@bu.edu）, Komal Kango（komalk@bu.edu）, Jing Song(jingsong@bu.edu), Kristi Perreault（kristip@bu.edu） 
   <br/>	

## 1.  Vision and Goals Of The Project

<br/> The system will be a cloud based infrastructure that runs code written in Python or R over specified data sets to create and             compare models that predict ecological forecasts. High-Level Goals for this Project include:

   -   Providing a web service with a simple user experience such that researchers can submit code and periodically run it on data sets.
   -   Developing infrastructure on the cloud using either VM or containers to run code and balance workload.
   -   Providing a user interface that allows for comparisons between multiple models on the same data set along with comparisons of            models using periodic data sets in order to determine model accuracy.
   <br/>

## 2.  Users/ Personas of the Project 
<br/> The system will be deployed by system administrators and used by two segments of end-users in the BU Department of Earth and Enviornment. The end-users will be segemented as project leaders and project team members. The system targets end-users, specifically ecological researchers. It does not target:

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
    
<br/> Orchestrator & Scheduler:
   -   Analyze the submitted code and install code dependencies
   -   Distribute code across different cloud platforms for computation to balance load
   -   The cloud to run openWhisk can only exist for seven days, after that the recourse will be retrieved, and we need to reapply the access to the recourse, so we need an O&S to Monitor the availability of the VMs in the cluster, so that no code is sent to invalid VMs. 
   -   Resend code to a new machine when one VM fails
   <br/>

<br/> VM Environment: free cloud serverless platform GENI & Chameleon
   -   Install Openwhisk on a cluster of VMs (so that there is no need to renew VM every week)
   -   Openwhisk calls the cluster to run the code
   -   Code distributed by O&S to run either on GENI edge nodes or Chameleon cloud
    <br/>
    
<br/> Database Management: 
   -   User information stored and managed in MongoDB
   -   Store output of computation in DynamoDB (Dynamo allows computation configuration)

<br/> Security: provide secure storage of user data and computation output
<br/>
<br/>

## 4.  Solution Concept
<img src="Solution_Diagram.PNG"><br/>

<br/> The main problem for the system is the lack of a way to monitor it to tell which containers are full or have failed to run the           code. So we plan to overhaul the web interface with a system for logging in that allows administrators to have access to the             performance of the system. Once users sign in they will be presented with options based on their credentials. All users will be         able to input data, code, and offline containers.
<br/>
<br/>
    
## 5.  Acceptance Criteria
<br/> The minimum acceptance criteria is a single-running process which the code submitted by the user is taken by Openwhisk and               distributed by O&S to run across different cloud serverless platforms and the output of computation is shown to the user on UI.         Stretch goals are:

   -   More visualization functionality for showing the computation output
   -   Code storage optimization (close to data source? User, etc.)
   -   Parallel Code Execution
   <br/>

## 6.  Release Planning
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
   -   Submission portal 
        -   User can upload code in R in text box or file upload 
        -   Data stored in MongoDB 
   -   Userregistration/login 
        -   User able to register for an account with email
        -   User able to login 
   -   Admin system 
        -   Ability for admins to approve registration requests 
   -   VM environment 
        -   Install Openwhisk on a cluster

<br/> Release \#3 (due week 8) 
   -   Submission portal
        -   User can upload code in R via container link/code link 
   -   Results display 
        -   Data visualization results surfaced to user
   -   Admin system
        -   Manage accounts; add, delete, update users
   -   Build O&S
        -   Analyze the submitted code, install code dependencies
   -   VM environment
        -   Openwhisk calls the cluster to run the code

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
