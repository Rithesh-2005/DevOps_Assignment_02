pipeline {
    agent any

    environment {
        // Replace with your Docker Hub username
        DOCKERHUB_USERNAME = 'rithesh2005'
        // This is the ID of the 'Username and Password' credential you set up in Jenkins
        DOCKERHUB_CREDS_ID = 'docker-hub-cred-id' 
        // This is the ID of the 'kubeconfig' credential you set up in Jenkins
        KUBE_CONFIG_ID = 'kubeconfig' 
        DOCKER_IMAGE_NAME = "${DOCKERHUB_USERNAME}/ticket-app"
    }

    stages {
    
        

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image 
                    bat "docker build -t ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER} ."
                    bat "docker tag ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER} ${DOCKER_IMAGE_NAME}:latest"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                // Log in to Docker Hub and push the image [cite: 20]
                withCredentials([usernamePassword(credentialsId: DOCKERHUB_CREDS_ID, passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    bat "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"
                    bat "docker push ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}"
                    bat "docker push ${DOCKER_IMAGE_NAME}:latest"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                // Use the kubeconfig credential to deploy 
                withKubeConfig([credentialsId: KUBE_CONFIG_ID]) {
                    // We must update the image in the deployment file first
                    // This uses 'sed' to find the 'image:' line and replace it with the new build
                    powershell "Get-Content k8s\\deployment.yaml | ForEach-Object { $_ -replace 'image: .*', \"image: ${env.DOCKER_IMAGE_NAME}:latest\" } | Set-Content k8s\\deployment.yaml"
                    
                    // Apply the updated deployment and service manifests 
                    bat "kubectl apply -f kubernetes/deployment.yaml"
                    bat "kubectl apply -f kubernetes/service.yaml"
                    bat "kubectl rollout status deployment/ticket-app-deployment"
                }
            }
        }
    }

    post {
        always {
            // Clean up workspace
            cleanWs()
            // Log out from Docker Hub
            bat "docker logout"
        }
    }
