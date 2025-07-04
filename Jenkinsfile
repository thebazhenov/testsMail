pipeline {
    agent any

    environment {
        PYTHON_ENV = 'venv'
        PATH = "/usr/local/bin:${env.PATH}"  // чтобы python3 из /usr/local/bin был доступен
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Setup Python & Dependencies') {
            steps {
                sh '''
                  python3 -m venv ${PYTHON_ENV}
                  . ${PYTHON_ENV}/bin/activate
                  pip install --upgrade pip
                  pip install -r requirements.txt
                  playwright install --with-deps
                '''
            }
        }

        stage('Start Services') {
            steps {
                sh 'docker-compose up -d --build'
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                  . ${PYTHON_ENV}/bin/activate
                  pytest --alluredir=allure-results
                '''
            }
        }
    }

    post {
        always {
            sh 'docker-compose down'
            archiveArtifacts artifacts: '**/screenshots/*.png', allowEmptyArchive: true
        }
    }
}