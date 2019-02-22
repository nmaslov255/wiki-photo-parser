Парсер фотографий чиновников из википедии.

### Установка
1. git clone https://github.com/nmaslov255/wiki-photo-parser.git
2. cd wiki-photo-parser
3. python3 -m venv .
4. source bin/activate
5. pip3 install -r requirements.txt
6. curl 'https://declarator.org/media/dumps/person.json' -o 'persons.json'
7. python3 parser/main.py 'persons.json' 'results.json'

### Если нужно продолжить загрузку с предыдущих результатов
python3 parser/main.py 'persons.json' 'results.json' --start-from 'results.json'
