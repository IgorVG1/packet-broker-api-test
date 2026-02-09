# Прогон авто-тестов (Команды для запуска прогона)


## Команда №1 :

```shell
pytest -m regression --alluredir=allure-results
```


###### 1. Запускает все тесты из набора "regression" в области видимости директории
> pytest -m regression

###### 2. По завершении прогона генерирует allure-отчет о его результатах в директории ./allure-results
> --alluredir=allure-results


## Команда №2 :

```shell
swagger-coverage-tool save-report
```

###### 1. Генерирует отчет о покрытии Swagger-документации запущенными авто-тестами

###### 2. Сгенерированный отчет доступен в файле ./coverage.html

## Команда №3 :

```shell
allure serve ./allure-results
```

###### 1. Открывает динамический allure-отчет локально в браузере


## Команда №4 :

```shell
allure generate ./allure-results --output=./allure-report --clean
```

###### 1. Генерирует статический отчет из директории, которую мы указываем (./allure-results) 
> generate ./allure-results

###### 2. Параметр определяет, в какую директорию (./allure-report) будет помещен статический отчет (index.html)
> --output=./allure-report

###### 3. Параметр определяет необходимость перезаписи существующей папки отчета
> --clean