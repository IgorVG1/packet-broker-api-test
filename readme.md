# Прогон авто-тестов


## Команды для запуска прогона


### Команда №1 :

```shell
pytest -m regression --alluredir=allure-results
```


###### 1. Запускает все тесты из набора "regression" в области видимости директории
> pytest -m regression

###### 2. По завершении прогона генерирует allure-отчет о его результатах в директории ./allure-results
> --alluredir=allure-results

###### 3. Прогон авто-тестов выполняется в двух потоках
- Первый поток прогоняет позитивные сценарии
- Второй поток прогоняет негативные сценарии
- параметр **--dist=loadgroup** отвечает за принцип сортировки тестов по потокам
> --numprocesses=2 --dist=loadgroup


### Команда №2 :

```shell
swagger-coverage-tool save-report
```

###### 1. Генерирует отчет о покрытии Swagger-документации запущенными авто-тестами

###### 2. Сгенерированный отчет доступен в файле ./coverage.html

### Команда №3 :

```shell
allure serve ./allure-results
```

###### 1. Открывает allure-отчет локально в браузере

###### 2. После закрытия отчета необходимо в терминале завершить процесс
```shell
<Ctrl> + <C>
yes
```

### Команда №4 :

```shell
allure generate ./allure-results --output=./allure-report
```

###### 1. Генерирует allure-отчет и сохраняет его html-файл в root:
> ./allure-report/index.html