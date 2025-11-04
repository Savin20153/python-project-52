### Hexlet tests and linter status:
[![Actions Status](https://github.com/Savin20153/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Savin20153/python-project-52/actions)
[![Python CI](https://github.com/Savin20153/python-project-52/actions/workflows/ci.yml/badge.svg)](https://github.com/Savin20153/python-project-52/actions/workflows/ci.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Savin20153_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Savin20153_python-project-52)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Savin20153_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Savin20153_python-project-52)

https://python-task-manager-4t2f.onrender.com/

**Менеджер задач** — это веб-приложение, предоставляющее следующие возможности:

- регистрация новых пользователей через специальную форму;

- вход в систему с использованием учетных данных;

- просмотр списка всех зарегистрированных пользователей на отдельной странице без необходимости авторизации;

- изменение и удаление собственных данных (удаление недоступно, если пользователь является автором или исполнителем какой-либо задачи);

- после входа в систему — просмотр, создание, редактирование и удаление статусов и меток задач (при этом те, что связаны с задачами, удалить нельзя);

- после входа в систему — просмотр, создание, редактирование и удаление самих задач (удалять их может только автор);


## Установка

1. Склонировать репозиторий:
```
git@github.com:Savin20153/python-project-52.git```

2. Прейти в директорию проекта:
```
cd python-project-52
```

3. Установить проект:
```
make install
```

4. В проекте иcпользуется База данных postgresql
   Она должна быть установлена, и сервер запущен.



## Запуск
Локально:
```
make start
```