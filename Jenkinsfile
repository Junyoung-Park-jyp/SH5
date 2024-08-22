pipeline {
    agent any

    environment {
        ENV_FILE_PATH = '/home/ubuntu/.env'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Junyoung-Park-jyp/SH5', branch: 'backend'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t my-django-app:${env.BUILD_ID} ."
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // 컨테이너 내부에서 환경 변수 출력
                    sh "docker run --rm --env-file ${env.ENV_FILE_PATH} my-django-app:${env.BUILD_ID} printenv"
                    sh "docker run --rm -w /app/SOLoTrip --env-file ${env.ENV_FILE_PATH} my-django-app:${env.BUILD_ID} python manage.py test"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh "docker stop my-django-app || true"
                    sh "docker rm my-django-app || true"
                    sh "docker run -d -p 8000:8000 --name my-django-app --env-file ${env.ENV_FILE_PATH} my-django-app:${env.BUILD_ID}"
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
