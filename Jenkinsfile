pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/yourusername/your-vue-repo', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // 명시적으로 Dockerfile의 경로를 지정
                    sh 'docker build -t my-vue-app:latest -f Dockerfile .'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh 'docker run --rm my-vue-app:latest npm run test'
                }
            }
        }

        stage('Deploy Docker Container') {
            steps {
                script {
                    sh 'docker stop my-vue-app || true'
                    sh 'docker rm my-vue-app || true'
                    sh 'docker run -d -p 80:80 --name my-vue-app my-vue-app:latest'
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
