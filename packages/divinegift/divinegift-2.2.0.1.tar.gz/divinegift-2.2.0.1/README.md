**The most useful package for you, young s7_it programer :)**

# How to use it

## Install this packages before use

* sqlalchemy            - For works with databases
* cx_Oracle             - Oracle driver
* sqlalchemy-pytds      - MSSQL driver
* psycopg2-binary       - Postgres driver
* xlutils               - For Excel
* xlsxwriter            - for Excel
* openpyxl              - For Excel  
* transliterate         - For Transliteration
* confluent-kafka[avro] - For work with kafka

## logging

```
# Import necessary functions
from divinegift.logger import log_info, log_err, log_warning, set_loglevel

# info msg
log_info('Your message')

# error msg
log_err('Error msg',
        src='Error source',  # e.g. str(sys.argv[0])
        mode=['telegram', 'email']  # May be empty
        channel={ 
            "telegram": -1001343660695, 
            "email": {"TO": ["your@domain.ru"], "FROM": "from@domain.com", 
                "HOST": "smtp.domain.com", "usr": "from@domain.com", "pwd": "supersecretpassword"}  
        })  # You can add "CC" to "email" for add copy_to addresses

# error msg with out sending problem to external system
log_err('Error msg', src='Error src')
```

## Pass log_level and log_name through cmd arguments

To specify log_level and log_name in your app you can send it through arguments:
```
if __name__ == '__main__':
    # Get all args from cmd:
    args = get_args()
    # Get log_level, log_name, log_dir
    lp = get_log_param(args)
    # Set log_level and log_name:
    set_loglevel(lp.get('log_level'), lp.get('log_name'), lp.get('log_dir'))
```
You should pass your args by pairs: key value, e.g. --log_level INFO
Available variants for logging are:
* --log_level or shortcut is -ll
* --log_name or shortcut is -ln
* --log_dir or shortcut is -ld

log_level could be DEBUG, INFO, WARNING, ERROR

Example of starting app with arguments:
```
python test.py -ll INFO -ln test.log
```

## Config parsing 

To parsing configs you can use class *divinegift.config.Settings* .
By default, it's use yaml as config language. But you can use json-style too.

### YAML-config
```
from divinegift.config import Settings  # Necessary imports

settings = {}

# You should use divinegift.logger.set_loglevel before config parsing
s = Settings()
s.parse_settings('./settings.ini')
settings = s.get_settings()
```

#### Config example
```
monitoring:
- telegram
- email
- slack
monitoring_channel:
    email_to:
    - aims.control@s7.ru
    telegram: -1001343660695
```

### JSON-config

```
from divinegift.config import Settings  # Necessary imports

settings = {}

# You should use divinegift.logger.set_loglevel before config parsing
s = Settings()
s.parse_settings('./settings.ini', use_yaml=False)
settings = s.get_settings()
```

#### Config example

```
{
    "log_level": "INFO",
    "log_name": "YourAwesomeProject.log",
    "monitoring": [
        "telegram",
        "email"
    ],
    "monitoring_channel": {
        "telegram": -1001343660695,
        "email_to": [
            "aims.control@s7.ru"
        ]
    }
 }
```

## Working with DB (sqlalchemy)

You should define dict with db_conn creditional.
For example:

### Oracle
Install oracle driver:
```
pip install cx_oracle
```
```
db_conn = {
    "db_user": "dbuser",             # username
    "db_pass": "dbpass",             # password
    "db_host": "dbhost",             # host (ip, fqdn). could be empty if we connect via tns
    "db_port": "",                   # port (string). could be empty if we connect via tns
    "db_name": "dbname",             # database name
    "db_schm": "",                   # db scheme if not equal username
    "dialect": "oracle"              # if use cx_Oracle or oracle+another_dialect
}
```
### MSSQL
Install mssql driver:
```
pip install sqlalchemy-pytds
```
```
db_conn = {
    "db_user": "dbuser",             # username
    "db_pass": "dbpass",             # password
    "db_host": "",                   # host (ip, fqdn). could be empty if we connect via tns
    "db_port": "",                   # port (string). could be empty if we connect via tns
    "db_name": "dbname",             # database name
    "db_schm": "",                   # db scheme if not equal username
    "dialect": "mssql+pytds"         # mssql dialect
}
```
### Postgres
Install postgres driver:
```
pip install psycopg2
```
```
db_conn = {
    "db_user": "dbuser",             # username
    "db_pass": "dbpass",             # password
    "db_host": "",                   # host (ip, fqdn). could be empty if we connect via tns
    "db_port": "",                   # port (string). could be empty if we connect via tns
    "db_name": "dbname",             # database name
    "db_schm": "",                   # db scheme if not equal username
    "dialect": "postgresql+psycopg2" # dialect
}
```

### Create connection

Use class Connection to create connection to DB. Old-styled functions, which contained in *divinegift.db* module directly, are deprecated but still works.
```
from divinegift.db import Connection
connection = Connection(db_conn)            # db_conn - variable which was described above
# Describe which fields you wants to method get_conn will returned (possible fields are 'engine', 'conn' and 'metadata')
engine, conn, metadata = connection.get_conn(fields=['engine', 'conn', 'metadata'])  
```

If you need to call stored procedure with db cursors you should use raw connection.
```
from divinegift.db import Connection
connection = Connection(db_conn, do_initialize=False)            # db_conn - variable which was described above
connection.set_raw_conn()
conn = connection.get_conn(fields='conn')  
```

### Get data from sript (file or just string)

After you got "connection" variable you can  get data from file or from str variable directly.

```
from divinegift.db import Connection
connection = Connection(db_conn)

result = connection.get_data('path/to/scripts/some_script.sql')
# or you can use str variable:
script = 'select * from dual'
result = connection.get_data(script)
print(result)
>>>[{'dummy': 'X'}]
```

You can use specific encoding for your files (by default it's 'cp1251').
Just put it into args:
```
result = connection.get_data('path/to/scripts/some_script.sql', encoding='utf8')
```

Also you can add some variables into your script (e.g. date) and then you can pass it into a function:
```
from divinegift.db import Connection
connection = Connection(db_conn)

script = """select * from dual
where dummy = '$param'"""
parameters = {'param': 'X'}
result = connection.get_data(script, **parameters)
# Or another variant
result = connection.get_data(script, param='X')
print(result)
>>>[{'dummy': 'X'}]
```

### Run script without getting data

You can run script without recieving data.
You should use *divinegift.db.Connection.run_script* for this like get_data, e.g.:
```
from divinegift.db import Connection
connection = Connection(db_conn)
connection.run_script('path/to/scripts/some_script.sql')
```

## Sending email

You can use function send_mail from class *divinegift.sender.Sender*

You should set your msg, subject and list of recipients, and account which should be used for sending email
Simple example:
```
from divinegift.sender import Sender

sender = Sender()
sender.send_mail('Test message', 'Test subject', TO=['your@domain.com'],
           FROM="from@domain.com", HOST="smtp.domain.com", usr="from", pwd="pwd")
```

You can specify TO, CC, BCC, HOST, FROM and attachments. Also you can send it like html-message or like text.

You should pass list of attachments files with absolute path to it. You can use function *divinegift.main.get_list_files* for get it.
For sending email with attahment(s):
```
from divinegift.main import get_list_files
from divinegift.sender import Sender

sender = Sender()
attachment_list = get_list_files('/path/to/files', add_path=True)
sender.send_mail('Hello! This are files in attach', 'Test sending attachments', ['your@domain.com'], 
                  FROM="from@domain.com", HOST="smtp.domain.com", usr="from", pwd="pwd",
                  attachments=attachment_list)
# Also you can send only one file:
attachment = '/path/to/file/file_name'
sender.send_mail('Hello! There is file in attach', 'File', ['your@domain.com'], 
                FROM="from@domain.com", HOST="smtp.domain.com", usr="from", pwd="pwd",
                attachments=attachment)
```

If you set IS_HTML to False (by default it is True), you could send an email like simple text message, not html

## Work with JSON

You can simple parse and create JSONs

To create json you could use *divinegift.main.create_json*
To parse it you could use *divinegift.main.parse_json*
Or you could use class *divinegift.main.Json* instead of it

For example:
```
from divinegift.main import create_json, parse_json
A = {'key1': 'data1', 'key2': 'data2'}
create_json(A, 'json_file_name.json')
B = parse_json('json_file_name.json')

print(B)
>>> {'key1': 'data1', 'key2': 'data2'}

from divinegift.main import Json
A = {'key1': 'data1', 'key2': 'data2'}
json_obj = Json('json_file_class.json')
json_obj.set_data(A)
json_obj.create()
B = json_obj.parse()
```

## Work with YAML

You can simple parse and create YAMLs

To create json you could use *divinegift.main.create_yaml*
To parse it you could use *divinegift.main.parse_yaml*
Or you could use class *divinegift.main.Yaml* instead of it

For example:
```
from divinegift.main import create_yaml, parse_yaml
A = {'key1': 'data1', 'key2': 'data2'}
create_yaml(A, 'yaml_file_name.yml')
B = parse_yaml('yaml_file_name.yml')

print(B)
>>> {'key1': 'data1', 'key2': 'data2'}

from divinegift.main import Yaml
A = {'key1': 'data1', 'key2': 'data2'}
yml_obj = Yaml('yml_file_class.yml')
yml_obj.set_data(A)
yml_obj.create()
B = yml_obj.parse()
```

## Transliterate strings between Russian and English and back

From version 1.0.8 you can use transliterate library to transliterate strings between languages

Example:
```
from divinegift.translit import translit

name = 'SHEVCHENKO ANDREY'
name_r = translit(name, 'ru_ext')
name_e = translit(name_r, 'ru_ext', reversed=True)
name_r_cap = translit(name, 'ru_ext').capitalize()
name_r_low = translit(name, 'ru_ext').lower()

print(f'From English to Russian: {name}\t->\t{name_r}')
print(f'From Russian to English: {name_r}\t->\t{name_e}')
print(f'Capitalize             : {name}\t->\t{name_r_cap}')
print(f'Lower                  : {name}\t->\t{name_r_low}')
```

Code from above will show next:
```
From English to Russian: SHEVCHENKO ANDREY  ->  ШЕВЧЕНКО АНДРЕЙ
From Russian to English: ШЕВЧЕНКО АНДРЕЙ    ->  SHEVCHENKO ANDREI
Capitalize             : SHEVCHENKO ANDREY  ->  Шевченко андрей
Lower                  : SHEVCHENKO ANDREY  ->  шевченко андрей
```

## Encryption
From version 1.0.10 you can use encryption module

### Simple example
Example:
```
from divinegift.cipher import get_key, get_cipher, encrypt_str, decrypt_str

cipher_key = get_key()
cipher = get_cipher(cipher_key)
text = 'qwerty1234!!'
text_enc = encrypt_str(text, cipher)
print(text_enc)
text_dec = decrypt_str(text_enc, cipher)
print(text_dec)
```

Code above will output next:
```
gAAAAABcanXfhUr9i__R_24rPyrHzZoMgQSTYiBmx9ZtVqdcMiGZPOxoSz4gkAW0Y9TDWpAJ6jzAjPo-mrK_IcJcdByyfWrbhQ==
qwerty1234!!
```

If you use parameter get_str=False in functions encrypt_str and decrypt_str than this functions will returns binary string

### Works with key in file

Save your key in file by *write_key* function:
```
from divinegift.cipher import get_key, write_key

cipher_key = get_key()
write_key('key.ck', cipher_key)
```

Read your key file by *read_key* function:
```
from divinegift.cipher import read_key

cipher_key = read_key('key.ck')
```

### Caesar

You can use caesar encrypt/decrypt:
```
from divinegift.cipher import caesar_code

text = caesar_code('Hello, World!', shift=5)
print(text)
```
It will output next:
```
Mjqqt, 1twqi!
```

### Easy encription/decryption database-passwords for more security

Before all you should encrypt your file with settings.
Use next code to do this once:
```
from divinegift.config import Settings

s = Settings()
s.parse_settings('settings.conf')
s.initialize_cipher()
s.encrypt_password('db_conn')   # db_conn - name of db connection in settings.conf which contains "db_pass"
s.save_settings('settings.conf')
```

After that your password in section 'db_conn' will automaticaly encrypted.
If you have more db-connections just add s.encrypt_password('db_conn_name_you_have') before saving function

Next you must use decryption function in your code to use connection:
```
from divinegift.config import Settings

s = Settings()
s.parse_settings('settings.conf')
s.decrypt_password('db_conn')   # db_conn - name of db connection in settings.conf which contains "db_pass"
```


## Live templates. Start create your app as easy as possible

From version 1.0.11 you can create files from templates.
You should use module *templator* for this.

Example:
Create tmp.py with following text and run it:
```
from divinegift.templator import Templator

t = Templator()
# create console app, or main logic (you can omit the file extension, '.py' will add automaticaly.):
t.create_console('your_awesome_name.py')
# or
t.create_console()  # it will create 'main.py' file

# create QT-app:
t.create_gui(your_awesome_name.py')
# or
t.create_gui()  # it will create 'main_gui.py' file

# create config file:
t.create_config('your_config_name.ini')
# or
t.create_config()       # it will create 'settings.ini' file

# After creating file with config you can add email section on it:
t.add_email_config('your_config_name.ini')
# or
t.add_email_config()    # it will add email section to 'settings.ini'
```

## Kafka Client

From version 1.3.0 you can use kafka client to read and write data from/to topics


Example:
```
from divinegift.kafka_client import KafkaClient

kafka_client = KafkaClient()

# Reader
kafka_client.set_consumer(**s.settings.get('consumer_config'))

messages = kafka_client.read_messages(topic_name)
# You can read all messages from begin if you needed:
messages = kafka_client.read_messages(topic_name, from_beginning=True)

# Writer
kafka_client.set_consumer(**s.settings.get('producer_config'))

kafka_client.send_message(topic_name, msg)
```

Config example from example above:
```
kafka_config: &kafka_config
    bootstrap_servers:
    - server.domain:9093
    security_protocol: SSL
    ssl_check_hostname: False
    ssl_cafile: CARoot.pem
    ssl_certfile: certificate.pem
    ssl_keyfile: key.pem
producer_config:
    <<: *kafka_config
consumer_config:
    <<: *kafka_config
    consumer_timeout_ms: 1000
```

## Working with Excel

### Reading file

For reading excel-file you should use function *divinegift.excel.read_excel*

You should pass filename, array with column names

Optional fields are:
    sheet_name, int_columns, date_columns, start_row

```
from divinegift import excel

filename = 'your/path/to/excel.xlsx'      # or it could be xls
excel_header = ['column1', 'column2', ]
excel_data = excel.read_excel(filename, excel_header)
```

By default, all cells are read as strings, but if you need read int columns/date columns, you could pass their names 
in parameters int_columns/date_columns. You should name it like you pass it at excel_header

```
from divinegift import excel

filename = 'your/path/to/excel.xlsx'      # or it could be xls
excel_header = ['column1', 'column2', 'int_col', 'date_col']
excel_data = excel.read_excel(filename, excel_header, int_columns=['int_col'], date_col=['date_col'])
```

### Writing file

For writing excel-file you should use function *divinegift.excel.create_excel*

You should pass filename and list with data

Optional fields are:
    sheet_name, header
    
When you set excel_header, you could set column width
    
```
from divinegift import excel

filename = 'path/to/excel/your.xlsx'
data = [{'col1': 1, 'col2': 2,},]    # or it could be just list of list

excel_header = {'col1': 10, 'col2', 13, }
excel.create_excel(data, filename, excel_header=excel_header)
```