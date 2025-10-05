pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIAL_ID = 'dockerhub-login'
        DOCKERHUB_REGISTRY = 'https://registry.hub.docker.com'
        DOCKERHUB_REPOSITORY = 'cristiandevcode/classifier-api'
        KUBECONFIG_CREDENTIAL_ID = 'rackspace-kubeconfig'
        K8S_NAMESPACE = 'classifier-namespace' 
        DEPLOYMENT_NAME = 'classifier-deployment'
    }
    stages {
        stage('Clone Repository') {
            steps {
                script {
                    echo 'Cloning GitHub Repository...'
                    checkout scmGit(
                        branches: [[name: '*/main']], 
                        extensions: [], 
                        userRemoteConfigs: [[
                            credentialsId: 'ml-lab-token', 
                            url: 'https://github.com/crisdevcode/music-genre-classifier.git'  
                        ]]
                    )
                }
            }
        }
        stage('Lint Code') {
            steps {
                script {
                    echo 'Linting Python Code...'
                }
            }
        }
        stage('Test Code') {
            steps {
                script {
                    echo 'Setting up Python environment and Testing Python Code...'
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install pytest
                        pytest tests/
                    '''
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    dockerImage = docker.build("${DOCKERHUB_REPOSITORY}:latest")
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    echo 'Pushing Docker Image to DockerHub...'
                    docker.withRegistry("${DOCKERHUB_REGISTRY}", "${DOCKERHUB_CREDENTIAL_ID}") {
                        dockerImage.push('latest')
                    }
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo 'Deploying to Kubernetes cluster on Rackspace...'
                    withCredentials([file(credentialsId: "${KUBECONFIG_CREDENTIAL_ID}", variable: 'KUBECONFIG_FILE')]) {
                        sh '''
                            export KUBECONFIG=${KUBECONFIG_FILE}
                            kubectl set image deployment/${DEPLOYMENT_NAME} classifier-container=${DOCKERHUB_REPOSITORY}:latest -n ${K8S_NAMESPACE}
                            kubectl rollout status deployment/${DEPLOYMENT_NAME} -n ${K8S_NAMESPACE}
                        '''
                    }
                }
            }
        }
    }
}
