pipeline {
    agent any

    parameters {
        choice(name: 'BROWSER',
               choices: ['chromium', 'firefox', 'webkit'],
               description: 'Select the browser to run tests.')
        string(name: 'MARKER', defaultValue: 'full_regression', description: 'Pytest marker to run tests (e.g. smoke, regression, ui). Leave empty to run all.')
    }

    tools {
        allure 'Allure'
    }

    environment {
        PYTHON_ENV = 'venv'
        PATH = "/usr/local/bin:${env.PATH}"
        BROWSER = "${params.BROWSER}"
        MARKER  = "${params.MARKER}"
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
                  pytest -v -B ${BROWSER} -m "${MARKER}" --alluredir=allure-results || true
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/screenshots/*.png', allowEmptyArchive: true
            script {
                if (fileExists('allure-results')) {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        results: [[ path: 'allure-results' ]],
                    ])
                } else {
                    echo "Allure results directory not found. Skipping report generation."
                }
            }
        }
    }
}