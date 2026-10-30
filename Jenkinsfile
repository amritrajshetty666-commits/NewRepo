
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'devops-app-api'
        K8S_DEPLOYMENT = 'api'
        K8S_CONTAINER = 'api'
        KIND_CLUSTER = 'devops-lab'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    set -eu
                    command -v python3
                    python3 --version
                    python3 -m venv .venv-ci
                    .venv-ci/bin/python -m pip install \
                      -r backend/requirements.txt \
                      -r requirements-dev.txt
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '.venv-ci/bin/python -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                      -t ${IMAGE_NAME}:${BUILD_NUMBER} \
                      -t ${IMAGE_NAME}:latest \
                      backend
                '''
            }
        }

        stage('Verify Kubernetes Access') {
            steps {
                sh '''
                    set -eu
                    command -v docker
                    command -v kind
                    command -v kubectl

                    kind get clusters | grep -qx "${KIND_CLUSTER}"

                    kubectl config use-context kind-${KIND_CLUSTER}
                    kubectl get nodes
                '''
            }
        }

        stage('Load Image into Kind') {
            steps {
                sh '''
                    kind load docker-image \
                      ${IMAGE_NAME}:${BUILD_NUMBER} \
                      --name ${KIND_CLUSTER}
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl set image deployment/${K8S_DEPLOYMENT} \
                      ${K8S_CONTAINER}=${IMAGE_NAME}:${BUILD_NUMBER}
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    set -eu

                    kubectl rollout status deployment/${K8S_DEPLOYMENT} \
                      --timeout=180s

                    kubectl get pods -l app=api -o wide

                    kubectl exec deployment/api -- \
                      python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=5).read().decode())"
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD successful: application tested, image built and deployed to Kubernetes.'
        }

        failure {
            echo 'CI/CD failed. Review the failed stage and Jenkins console output.'
        }

        always {
            echo 'Pipeline execution completed.'
        }
    }
}

