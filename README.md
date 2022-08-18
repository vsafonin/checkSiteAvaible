## Простой скрипт для проверки доступности сайтов
Для проверки нужно заполнить Excel файл sites.xls.
Формат файла:
| URL |TITLE  |
|--|--|
Например:
|http://www.google.ru/|Google  |
|--|--|
|http://www.yandex.ru/  |Яндекс  |

**Установка**
1.  установить python
2.  установить через pip зависимости

```
pip install xlrd 
pip install requests ```
pip install bs4 


```

3.  Запустить скрипт.

```
python checkStatus

```
