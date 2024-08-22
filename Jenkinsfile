pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // GitHub에서 소스 코드를 체크아웃
                git url: 'https://github.com/Junyoung-Park-jyp/SH5', branch: 'develop-front'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Docker 이미지를 빌드
                    sh 'docker build -t my-vue-app:latest .'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // 컨테이너에서 테스트를 실행
                    sh 'docker run --rm my-vue-app:latest npm run test'
                }
            }
        }

        stage('Deploy Docker Container') {
            steps {
                script {
                    // 기존 컨테이너를 중지 및 제거
                    sh 'docker stop my-vue-app || true'
                    sh 'docker rm my-vue-app || true'

                    // 새 컨테이너를 백그라운드에서 실행
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
