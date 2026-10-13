pipeline {
    agent any
    
    environment {
        IMAGE_NAME = "devop93/time-app"
        TAG = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image for branch: ${env.BRANCH_NAME}"
                    sh "docker build -t ${IMAGE_NAME}:${TAG} -t ${IMAGE_NAME}:${env.BRANCH_NAME}-latest ."
                }
            }
        }
        
        stage('Push to Registry') {
            steps {
                script {
                    // Docker Hub login (Make sure to configure credentials in Jenkins)
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                        sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                    }
                    sh "docker push ${IMAGE_NAME}:${TAG}"
                    sh "docker push ${IMAGE_NAME}:${env.BRANCH_NAME}-latest"
                }
            }
        }
    }
}
