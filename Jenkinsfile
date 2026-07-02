pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "rahamshaik/flask-backend"
        IMAGE_TAG = "v1.0.${BUILD_NUMBER}"
        // Replace with your actual Config Repo URL
        CONFIG_REPO = "github.com/devopsbyraham/python-app-k8s-manifest.git"
     }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pytest
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} ."
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                        docker logout
                    '''
                }
            }
        }

        stage('GitOps Handoff (Update Config Repo)') {
            steps {
                withCredentials([string(credentialsId: 'github-pat-secret', variable: 'GITHUB_TOKEN')]) {
                    sh """
                        # 1. Clone the configuration repository using the PAT
                        git clone https://${GITHUB_TOKEN}@${CONFIG_REPO} config-repo
                        cd config-repo

                        # 2. Configure Git Identity
                        git config user.email "jenkins@enterprise.com"
                        git config user.name "Jenkins Automation Bot"

                        # 3. Use 'sed' to dynamically find and replace the image tag in deployment.yaml
                        sed -i "s|image: ${DOCKER_IMAGE}:.*|image: ${DOCKER_IMAGE}:${IMAGE_TAG}|g" deployment.yaml

                        # 4. Commit and Push back to GitHub
                        git add deployment.yaml
                        git commit -m "CD Auto-Sync: Deploying image tag ${IMAGE_TAG}"
                        git push https://${GITHUB_TOKEN}@${CONFIG_REPO} main
                    """
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
