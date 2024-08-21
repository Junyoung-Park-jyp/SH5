pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // GitHub에서 소스 코드를 체크아웃
                git url: 'https://github.com/Junyoung-Park-jyp/SH5', branch: 'backend'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Docker 이미지를 빌드
                script {
                    dockerImage = docker.build("my-django-app:${env.BUILD_ID}")
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                // Docker 컨테이너 내부에서 명령 실행
                script {
                    dockerImage.inside {
                        sh 'pip install --upgrade pip'
                        sh 'pip install -r requirements.txt'
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                // Docker 컨테이너 내부에서 Django 유닛 테스트 실행
                script {
                    dockerImage.inside {
                        sh 'python manage.py test'
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // 기존 컨테이너 정리
                    sh "docker stop my-django-app || true"
                    sh "docker rm my-django-app || true"

                    // Docker 이미지를 컨테이너로 실행
                    dockerImage.run("-d -p 8000:8000 --name my-django-app --env-file .env")
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
