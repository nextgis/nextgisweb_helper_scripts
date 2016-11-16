# Описание

Имеется 2 сервера ngw. Скрипт делает двухстороннюю синхронизацию слоя между ними. У слоя одинаковая структура, при этом у них нет уникального идентификатора.  
Синхронизируются все атрибуты, геометрия, аттачменты и описание.
Принято, что одновременно на обоих серверах одна фича изменится не может. Если вдруг это произойдёт, то второй сервер перекроет первый.
Принято, что все данные можно одновременно вместить в память.
Слои на обоих серверах получены из одного дампа, поэтому в начале работы они одинаковы. Их идентификаторы одинаковы.

# Алгоритм

При первом запуске делаются локальные копии обоих слоёв. И чего-то с аттачментами.
При последующем запуске сравнивается слой с сервера 1 с локальной копией. Составляется чейнджсет
При последующем запуске сравнивается слой с сервера 2 с локальной копией. Составляется чейнджсет
У фич одинаковые идентификаторы, поэтому применяем изменения с 1 на 2 и с 2 на 1.
	В процессе применения изменений есть особенность: в аттрибутах нет уникального идентификатора, а id фичи менять нельзя. Поэтому 3 варианта:
	Если объект создан, то он просто создаётся.
	Если объект изменён, то находим во 2 слое фичу, у которой атрибуты совпадают с той, что изменили
	Если объект удалён, то находим во 2 слое фичу, у которой атрибуты  совпадают с той, что изменили !? Что если фичи дублируются? Надо удалять ровно столько фич?
	В чейнджсете записываются новые и старые состояния фич.
Обновляются локальные копии слоёв.

## Что если скрипт будет остановлен посредине работы? Следующий запуск будет таким же. Составятся такие же чейнджсеты. 
	Если объект уже был создан в прошлый раз, то что бы он не создался второй раз, выполняется проверка.
	Если объект уже был изменён в прошлый раз, то вроде ничего страшного не будет, если второй раз отправится запрос на изменение. !? Что с аттачами?
	Если объект уже был удалён в прошлый раз, то запрос на удаление выдаст ошибку, её надо просто игнорировать.


# Установка

1. git clone
2. Переименовать config.example.py в config.py
3. Записать в config.py адреса, пароли и id слоёв

# Примеры исходных данных

```

