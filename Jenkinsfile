pipeline {
    agent any

    environment {
        // Replace with your Docker Hub username
        DOCKERHUB_USERNAME = 'YOUR_DOCKERHUB_USERNAME'
        // This is the ID of the 'Username and Password' credential you set up in Jenkins
        DOCKERHUB_CREDS_ID = 'YOUR_DOCKERHUB_CREDS_ID' 
        // This is the ID of the 'kubeconfig' credential you set up in Jenkins
        KUBE_CONFIG_ID = 'YOUR_KUBECONFIG_ID' 
        DOCKER_IMAGE_NAME = "${DOCKERHUB_USERNAME}/ticket-app"
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout code from Git
                git scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image 
                    sh "docker build -t ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER} ."
                    sh "docker tag ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER} ${DOCKER_IMAGE_NAME}:latest"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                // Log in to Docker Hub and push the image [cite: 20]
                withCredentials([usernamePassword(credentialsId: DOCKERHUB_CREDS_ID, passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    sh "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"
                    sh "docker push ${DOCKER_IMAGE_NAME}:${env.BUILD_NUMBER}"
                    sh "docker push ${DOCKER_IMAGE_NAME}:latest"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                // Use the kubeconfig credential to deploy 
                withKubeConfig([credentialsId: KUBE_CONFIG_ID]) {
                    // We must update the image in the deployment file first
                    // This uses 'sed' to find the 'image:' line and replace it with the new build
                    sh "sed -i 's|image: .*|image: ${DOCKER_IMAGE_NAME}:latest|g' deployment.yaml"
                    
                    // Apply the updated deployment and service manifests 
                    sh "kubectl apply -f kubernetes/deployment.yaml"
                    sh "kubectl apply -f kubernetes/service.yaml"
                    sh "kubectl rollout status deployment/ticket-app-deployment"
                }
            }
        }
    }

    post {
        always {
            // Clean up workspace
            cleanWs()
            // Log out from Docker Hub
            sh "docker logout"
        }
    }
}   