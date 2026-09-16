pipeline {
    agent any

    options {
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
    }
}