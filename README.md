# Інтернет-магазин на Flask

Даний проєкт є інтернет-магазином, створеним з використанням Flask.

---

## Інструкція з розгортання проєкту

### 1. Клонування репозиторію

### 2. Створення віртуального середовища Python
    Команди в терміналі:
        python3 -m venv venv

        venv\Scripts\activate       для Windows
        source venv/bin/activate    для Linux

### 3. Встановлення залежностей:
    pip install -r requirements.tx

### 4. Створення файлу конфігурації .env
    Створіть файл .env у кореневій папці проєкту.
    Додайте наступні параметри:
        SECRET_KEY=your_secret_key
        DATABASE_URL=your_database_url

### 5. Ініціалізація бази даних
    Виконайте скрипт для створення бази даних:
        python site_project/py_scripts/create_db.py

### 6. Додавання початкових даних
    Виконайте скрипт для додавання початкових даних (наприклад, продуктів):
        python site_project/py_scripts/add_products.py

### 7. Запуск проєкту
    Запустіть локальний сервер:
    flask run
    або python site_project/app.py
