#!groovy


def agentLabel
if (env.BRANCH_NAME == "release"){
    agentLabel = "production"
} else {
    agentLabel = "phys"
}
pipeline {
    agent { label agentLabel }
    stages {
        stage("Build and up") {
            steps {
                sh "cp /home/jenkins/weights/antivape.env .env"
                sh "docker-compose -f docker-compose.prod.yml -p antivape up -d --build --remove-orphans"
            }
        }
    }
}
