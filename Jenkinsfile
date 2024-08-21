pipeline {
    agent any

    environment {
        ENV_FILE_PATH = '/home/ec2-user/.env'
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
                    // 프로젝트 루트에서 manage.py를 실행하되, SOLOTrip 설정 파일을 명시적으로 지정
                    sh "docker run --rm -w /app my-django-app:${env.BUILD_ID} python manage.py test --settings=SOLOTrip.settings"
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
