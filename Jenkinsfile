pipeline {
    agent any

    environment {
        IMAGE_NAME = 'devops-app-api'
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
                    .venv-ci/bin/python -m pip install -r backend/requirements.txt -r requirements-dev.txt
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '.venv-ci/bin/python3 -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -t ${IMAGE_NAME}:latest backend'
            }
        }
    }

    post {
        success {
            echo 'CI pipeline succeeded: tests passed and Docker image built.'
        }
        failure {
            echo 'CI pipeline failed. Review the stage logs.'
        }
        always {
            echo 'CI pipeline finished.'
        }
    }
}
