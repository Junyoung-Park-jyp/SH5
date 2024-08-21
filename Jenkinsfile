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
                    // 컨테이너 내부에서 /app 디렉토리로 이동한 후, manage.py 파일을 찾음
                    sh "docker run --rm -w /app my-django-app:${env.BUILD_ID} ls /app"  // 디버깅을 위해 /app 디렉토리의 파일 확인
                    sh "docker run --rm -w /app my-django-app:${env.BUILD_ID} ls /app/SOLoTrip"  // 디버깅을 위해 /app 디렉토리의 파일 확인
                    sh "docker run --rm -w /app/SOLoTrip my-django-app:${env.BUILD_ID} python manage.py test"
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
