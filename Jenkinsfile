pipeline {
    agent any

    environment {
        PYTHON_ENV = 'venv'
        PATH = "/usr/local/bin:${env.PATH}"  // чтобы python3 из /usr/local/bin был доступен
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
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
            when {
                expression { fileExists('allure-results') }
            }
            steps {
                // вызов DSL-шага Allure Jenkins Plugin
                allure([
                    includeProperties: false,
                    jdk: '',                              // если нужен JDK, иначе оставьте ''
                    results: [[ path: 'allure-results' ]],
                ])
            }
        }
    }

    post {
        always {
            // сохраняем скриншоты, если они есть
            archiveArtifacts artifacts: '**/screenshots/*.png', allowEmptyArchive: true
        }
    }
}