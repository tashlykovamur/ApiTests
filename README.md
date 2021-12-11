### В проекте содержатся тесты на HTTP методы:

* GET /characters
* GET /character?name
* POST /character
* PUT /character
* DELETE /character?name

### Установка
#### Установка python 3
```bash
python3 -m venv venv
source venv/bin/activate
pip install pip --upgrade
```

#### Клонирование репозитория
```bash
bash
git clone 

```

#### Установка файла с библиотеками
```bash
pip install -U -r requirements.txt
```

### Allure reports ####
#### Установка Allure:
```bash
brew install allure
```

## Запуск тестов

**1) Перед запуском необходимо прописать username и password в config.py**

**2) Выполнить команду в терминале**
```bash
python -m pytest -k tests --alluredir=./allure_report
```
**Либо Через IDE (PyCharm):**
* Правой кнопкой мыши кликнуть по папке с тестами
* Выбрать **Run 'Python tests in test...'**

#### Запуск отчета локально
```bash
allure serve ./allure_report
```




