pipeline {
    agent any

    options {
        // Prevent multiple builds from running at the same time
        disableConcurrentBuilds()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Gitleaks') {
            steps {
                sh '''
                    docker run --rm \
                      -v "$WORKSPACE:/repo" \
                      zricethezav/gitleaks:latest \
                      git /repo \
                      --redact \
                      --exit-code 1
                '''
            }
        }

        stage('Bandit') {
            steps {
                sh '''
                    docker run --rm \
                      -v "$WORKSPACE:/src" \
                      python:3.12-slim \
                      sh -c "pip install --no-cache-dir bandit && bandit -r /src -ll"
                '''
            }
        }

        stage('pip-audit') {
            steps {
                sh '''
                    docker run --rm \
                      -v "$WORKSPACE:/src" \
                      python:3.12-slim \
                      sh -c "pip install --no-cache-dir pip-audit && pip-audit -r /src/requirements.txt"
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('Semgrep') {
            steps {
                sh '''
                    docker run --rm \
                      -v "$WORKSPACE:/src" \
                      semgrep/semgrep \
                      semgrep scan --config auto /src \
                      --exclude terraform/
                '''
            }
        }

        stage('Hadolint') {
            steps {
                sh '''
                    docker run --rm \
                      -i \
                      hadolint/hadolint < "$WORKSPACE/Dockerfile"
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build \
                      -t recipebhook:ci \
                      "$WORKSPACE"
                '''
            }
        }

        stage('Trivy') {
            steps {
                sh '''
                    docker run --rm \
                      -v /var/run/docker.sock:/var/run/docker.sock \
                      aquasec/trivy:latest \
                      image \
                      --severity HIGH,CRITICAL \
                      --exit-code 1 \
                      recipebhook:ci
                '''
            }
        }
    }
}