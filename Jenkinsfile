pipeline {
    agent {
        docker {
            image 'python:3.10'
            args '-u root'   // allows pip install and docker login
        }
    }

    environment {
        DOCKER_IMAGE = "python-app"
        DOCKER_TAG   = "latest"
    }

    stages {

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 --version
                    pip3 --version

                    python3 -m venv venv
                    . venv/bin/activate

                    pip install --upgrade pip
                    pip install -r requirements.txt || true
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install flake8
                    flake8 || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                '''
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                   
                )]) {
                    sh '''
                        echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin

                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_USERNAME}/${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${DOCKER_USERNAME}/${DOCKER_IMAGE}:${DOCKER_TAG}
                    '''
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
