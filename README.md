## About The Project
Jira webhook to MS TEAMS incomming webhook translator written without any long
development plans. It simply listens for Jira create webhook and forms MS TEAMS
card

### How to deploy
Docker is used to deploy separate containers. And it is using local config
volume for configuration:  
copy configuration from `templates/configuration_template.py` to separate
directory, rename to configuration.py and edit Teams webhook as well as your
JIRA base URL.

#### Build the container
`docker build -t {docker image name}:{tag} {folder to docker image}`

#### Start the container
`docker run --name {name} -d -v $(pwd)/{cfg_folder}:/webhook_server/cfg -p
{PORT}:8080 --restart always {Docker image name}`  
{PORT} - por by which you would like to reach webhook from external  
{name} - will be docker name (optional)  
{cfg_folder} - directory with configuration.py file  
{Docker image name} - name of Docker image created previously 
