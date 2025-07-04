pipeline {
    agent any

    tools {
        allure 'Allure'
    }

    environment {
        PYTHON_ENV = 'venv'
        PATH = "/usr/local/bin:${env.PATH}"
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

        stage('Allure Report') {
            when { expression { fileExists('allure-results') } }
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[ path: 'allure-results' ]],
                ])
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/screenshots/*.png', allowEmptyArchive: true
        }
    }
}