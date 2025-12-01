pipeline {
    agent any

    environment {
        VENV = "venv"
        // Optionally: docker image name
        DOCKER_IMAGE = "full-stack-python-app"
        // If pushing to Docker registry, define credentials in Jenkins
        DOCKERHUB_USER = credentials('dockerhub-username')
        DOCKERHUB_PASS = credentials('dockerhub-password')
    }

    stages {
        stage('Checkout') {
            steps {
                // Adjust repo URL & branch as needed
                git branch: 'main',
                    url: 'https://github.com/codingforentrepreneurs/full-stack-python.git'
            }
        }

        stage('Setup Virtualenv & Install Dependencies') {
            steps {
                sh """
                  python3 -m venv ${VENV}
                  source ${VENV}/bin/activate
                  pip install --upgrade pip
                  pip install -r requirements.txt
                """
            }
        }

        stage('Lint (flake8)') {
            steps {
                sh """
                  source ${VENV}/bin/activate
                  pip install flake8
                  flake8 .
                """
            }
        }

        stage('Optional: Run Tests') {
            steps {
                sh """
                  source ${VENV}/bin/activate
                  # if you have tests, e.g. pytest
                  if [ -f "pytest.ini" ] || [ -d "tests" ] ; then
                    pip install pytest
                    pytest -v --disable-warnings --maxfail=1
                  else
                    echo "No tests found — skipping pytest"
                  fi
                """
            }
        }

        stage('Security Scan (bandit)') {
            steps {
                sh """
                  source ${VENV}/bin/activate
                  pip install bandit
                  # scan entire project (or adjust path)
                  bandit -r .
                """
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:latest")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh """
                  echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin
                  docker tag ${DOCKER_IMAGE}:latest $DOCKERHUB_USER/${DOCKER_IMAGE}:latest
                  docker push $DOCKERHUB_USER/${DOCKER_IMAGE}:latest
                """
            }
        }
    }

    post {
        always {
            echo "Cleaning workspace"
            cleanWs()
        }
    }
}
