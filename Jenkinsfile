pipeline {
    agent any

    parameters {
        string(name: 'MARK', defaultValue: '', description: 'Pytest marker to run (e.g. smoke, regression, ui). Leave empty to run all tests.')
    }

    environment {
        PYTHON_ENV = 'venv'
    }

    tools {
        python 'Python3'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create venv & Install Requirements') {
            steps {
                sh '''
                    python -m venv ${PYTHON_ENV}
                    . ${PYTHON_ENV}/bin/activate
                    pip install --upgrade pip
                    pip install -r testsMailProject/requirements.txt
                    playwright install --with-deps
                '''
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def markerOption = params.MARK?.trim() ? "-m ${params.MARK}" : ""
                    sh """
                        . ${PYTHON_ENV}/bin/activate
                        pytest testsMailProject/ ${markerOption} --alluredir=testsMailProject/allure-results
                    """
                }
            }
        }

        stage('Allure Report') {
            when {
                expression { fileExists('testsMailProject/allure-results') }
            }
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'testsMailProject/allure-results']]
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/screenshots/*.png', allowEmptyArchive: true
        }
        failure {
            echo '❌ Tests failed!'
        }
    }
}