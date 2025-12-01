pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "python-app"
        DOCKER_TAG   = "latest"
    }

    stages {

        /* -----------------------------------------
           1. Install Dependencies (Python + Docker)
           -----------------------------------------*/
        stage('Install Dependencies') {
            steps {
                sh '''
                    echo "Installing Python and Docker packages..."

                    # Update system packages
                    apt-get update -y

                    # Install Python3, pip and venv
                    apt-get install -y python3 python3-pip python3-venv

                    # Install Docker client (usually already present in Jenkins Docker agent)
                    if ! command -v docker > /dev/null; then
                        apt-get install -y docker.io
                    fi

                    python3 --version
                    pip3 --version
                    docker --version
                '''
            }
        }

        /* -------------------------
           2. Setup Python Environment
           -------------------------*/
        stage('Setup Python Environment') {
            steps {
                sh '''
                    echo "Setting up Python venv..."
                    python3 -m venv venv
                    . venv/bin/activate

                    pip install --upgrade pip
                    pip install -r requirements.txt || true
                '''
            }
        }

        /* -------------------------
           3. Lint (Optional)
           -------------------------*/
        stage('Lint') {
            steps {
                sh '''
                    echo "Running flake8..."
                    . venv/bin/activate
                    pip install flake8
                    flake8 || true
                '''
            }
        }

        /* -------------------------
           4. Build Docker Image
           -------------------------*/
        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "Building Docker image..."
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                '''
            }
        }

        /* -------------------------
           5. Push to DockerHub
           -------------------------*/
        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USERNAME',
                    passwordVariable: 'DOCKER_PASSWORD'
                )]) {
                    sh '''
                        echo "Logging into DockerHub..."
                        echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin

                        echo "Tagging image..."
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_USERNAME}/${DOCKER_IMAGE}:${DOCKER_TAG}

                        echo "Pushing image..."
                        docker push ${DOCKER_USERNAME}/${DOCKER_IMAGE}:${DOCKER_TAG}
                    '''
                }
            }
        }
    }

    /* -------------------------
       Post step cleanup
       -------------------------*/
    post {
        always {
            cleanWs()
        }
    }
}
