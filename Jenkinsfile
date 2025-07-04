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
            archiveArtifacts artifacts: '**/screenshots/*.png', allowEmptyArchive: true
        }
    }
}