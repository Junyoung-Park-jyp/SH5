pipeline {
    agent any

    environment {
        AILAB_API_KEY = credentials('AILAB_API_KEY')
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Junyoung-Park-jyp/SH5', branch: 'develop-front'
            }
        }

        stage('Print Env') {
            steps {
                script {
                    echo "AILAB_API_KEY: ${AILAB_API_KEY}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build --build-arg VUE_APP_AILAB_API_KEY=$AILAB_API_KEY -t my-vue-app:latest -f Frontend/Dockerfile Frontend/'
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
