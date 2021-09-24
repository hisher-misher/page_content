# page_content
print page content

поднять контейнер в окне терминала
docker-compose up --build

в другом окне зайти в него
docker exec -it page_content_web_1 bash

запустить скрипт с параметрами по умолчанию: -u https://www.python.org/ -w 70 
python bs_parse.py

с выводом в файл и заменой изображений на ссылки
python bs_parse.py -f page_content.txt -u https://www.python.org/ -i

Дополнительно ввел один параметр -b (break_long_lines)
