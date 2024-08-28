pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Junyoung-Park-jyp/SH5', branch: 'develop-front'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t my-vue-app:latest -f Frontend/Dockerfile Frontend/'
                }
            }
        }

        stage('Deploy Docker Container') {
            steps {
                script {
                    sh 'docker stop my-vue-app || true'
                    sh 'docker rm my-vue-app || true'
                    sh 'docker run -d -p 8081:80 --name my-vue-app my-vue-app:latest'
                }
            }
        }
    }

    post {
        always {
            echo 'Build finished'
        }
        success {
            echo 'Build succeeded!'
        }
        failure {
            echo 'Build failed!'
        }
    }
}
