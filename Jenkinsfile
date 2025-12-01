pipeline {
    agent any

    environment {
        DOCKER_CREDS = credentials('dockerhub-creds')
        DOCKER_IMAGE = "my-python-app"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/codingforentrepreneurs/full-stack-python.git'
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    source venv/bin/activate
                    pip install flake8
                    flake8 .
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    docker build -t ${DOCKER_IMAGE}:latest .
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                sh """
                    echo "${DOCKER_CREDS_PSW}" | docker login -u "${DOCKER_CREDS_USR}" --password-stdin
                    docker tag ${DOCKER_IMAGE}:latest ${DOCKER_CREDS_USR}/${DOCKER_IMAGE}:latest
                    docker push ${DOCKER_CREDS_USR}/${DOCKER_IMAGE}:latest
                """
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
