 # 📧 testsMailProject

Проект для автоматизированного тестирования UI и API почтового веб-клиента.

## 📦 Стек технологий

- **Python** + **pytest** — фреймворк для написания и запуска тестов
- **Playwright** — для UI тестирования
- **Allure** — для генерации отчетов
- **Docker + docker-compose** — контейнеризация окружения
- **Jenkins** — CI/CD пайплайн
- **Pydantic** — валидация и сериализация данных
- **requests** — тестирование API

## 🧪 Структура проекта

```
testsMailProject/
│
├── config/                # Настройки окружения и базовые конфигурации
│── services/
│   ├── api/
│       ├── name module/   # Для каждого модуля создается отдельный пакет
│           ├── models/    # Pydantic модель для обработки json
│   ├── ui/  
│       ├── pages/   # PageObject 
├── tests/
│   ├── api/               # Тесты API
│   └── ui/                # Тесты UI
│
├── conftest.py            # Общие фикстуры
├── pytest.ini             # Конфигурация pytest
├── requirements.txt       # Зависимости проекта
├── docker-compose.yml     # Описание контейнеров
├── Jenkinsfile            # Скрипт CI для Jenkins
├── .env                   # Переменные окружения
└── README.md
```

## 🚀 Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/thebazhenov/testsMail.git
cd testsMailProject
```

### 2. Установите зависимости

```bash
pip install -r requirements.txt
```

### 3. Запуск Docker-окружения

```bash
docker-compose up -d
```

### 4. Запуск тестов

- Все тесты:

```bash
pytest
```

- UI тесты:

```bash
pytest -m ui
```

- API тесты:

```bash
pytest -m api
```

### 5. Генерация Allure отчета

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

## ⚙️ Jenkins

В Jenkins используется параметризованный pipeline:

- `BROWSER` — выбор браузера: `chromium`, `firefox`, `webkit`
- `MARKER` — выбор группы тестов (например, `ui`, `api`)

### Пример запуска в Jenkins:

```groovy
parameters {
    choice(name: 'BROWSER', choices: ['chromium', 'firefox', 'webkit'], description: 'Browser')
    string(name: 'MARKER', defaultValue: 'ui', description: 'Pytest marker')
}
```

## ✅ Маркеры тестов

- `@pytest.mark.ui` — UI тесты
- `@pytest.mark.api` — API тесты

## 📁 Переменные окружения

Создайте `.env` файл на основе шаблона и укажите параметры:

```env
USERNAME=test@localhost.com
PASSWORD=test
```

## 📌 Зависимости

См. `requirements.txt` для полного списка библиотек.

