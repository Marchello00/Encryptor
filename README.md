# Encryptor

Данная программа умеет кодировать/декодировать используя шифр Цезаря, 
Вернама или Виженераб а так же взламывать шифр Цезаря

## Использование

Чтобы посмотреть список аргументов используйте параметр -h
```
$ ./encryptor -h
usage: encryptor.py [-h] {encode,decode,train,hack} ...

positional arguments:
  {encode,decode,train,hack}
                        List of commands
    encode              Encode message
    decode              Decode message
    train               Create train model on your text
    hack                Try to hack message

optional arguments:
  -h, --help            show this help message and exit
$ ./encryptor.py train -h
usage: encryptor.py train [-h] [--text_file TEXT_FILE]
                          [--model_file MODEL_FILE] [--ngrams NGRAMS] [--punc]
                          [--top TOP] [--count_avg]

optional arguments:
  -h, --help            show this help message and exit
  --text_file TEXT_FILE, -i TEXT_FILE
                        Text for training
  --model_file MODEL_FILE, -m MODEL_FILE
                        Trained model will be written to this file
  --ngrams NGRAMS, -n NGRAMS
                        N for n-grams analyse
  --punc, -p            If exist punctuation will be also analysed
  --top TOP, -t TOP     How many most common words remember
  --count_avg, -c       Count average statistics on your text(may work slower)
```

## alphabet

Для многих операций может пригодиться использование параметра `--alphabet` или
`--file_alphabet`, с его помощью можно задать алфавит на котором будут 
осуществляться сдвиги во время шифровки (шифроваться будут только символы из алфавита).

Параметром `--alphabet` можно задавать стандартные алфавиты:
* eng - латинский алфавит (заглавные и строчные)
* engup - латинский алфавит (заглавные буквы)
* engpunc - лфтинский алфавит с пунктуацией (знаки препинания так же будут шифроваться)
* rus - кириллица
* bin - 0 и 1
* hex - 16-ричные символы
* all - весь латинский алфавит, кириллица, пунктуация и пробелы

*Замечание: по умолчанию используется eng, а в rus и all нет буквы ё*

Можно указать свой алфавит передав путь к файлу в параметре `--file_alphabet`, 
который будет интерпретирован как алфавит 
(никаких преобразований производиться не будет, все символы из файла будут в алфавите
не исключая повторений и пробелов, в том числе переноса строки).
### encode

Шифрует сообщение, переданное через стандартный ввод или считанное из файла 
(параметр `--input_file`), результат записывается в стандартный поток или
в файл (параметр `--output_file`). 

Обязательно указывать шифр (`--cipher`) - один из:
* caesar - шифр Цезаря
* vigenere - шифр Виженера
* vernam - шифр Вернама

и ключ для шифрования (`--key`), удовлетворяющий следующим требованиям:
* Для шифра Цезаря ключ обязательно натуральное число
* Для шифров Вернама и Виженера ключи это строки, состоящие только из символов алфавита
* Для шифра вернама размер ключа должен совпадать с размером сообщения

Обратите внимание, символы, которых нет в используемом алфавите, не будут шифроваться,
поэтому не забудьте указать `--alphabet`, если текст не английский.
### decode

Расшифровывает сообщение, переданное через стандартный ввод или считанное из файла 
(параметр `--input_file`), если известен шифр и ключ с которыми его зашифровали, 
результат записывается в стандартный поток или в файл (параметр `--output_file`). 

Аналогичные *encode* требования к `--cipher` и `--key` и аналогичное
использование `--alphabet`.

### hack

Помимо типичных аргументов `--input_file`, `--output_file` и `--alphabet`,
назначение которых не отличается от предыдущих случаев, принимает аргумент 
`--model_file`, далее чуть подробнее о нём.

Взлом основан на анализе известных настоящих текстов (подсчете частотности букв/
слов и т.д.), поэтому для качественного взлома необходима модель, которая строится 
по тексту (см. *train*). Путь к файлу с моделью необходимо передать через параметр
`--model_file`. В папке models есть 3 заранее подготовленные модели:
* eng - основана на анализе соннетов Шекспира (язык английский)
* eng2 - основана на анализе писейм Джейн Остин (язык английский)
* rus - основана на первом томе романа "Война и мир" Л.Н.Толстого (язык русский)

*Замечание: по умолчанию используется модель eng*

### train

Режим необходим для построения модели для взлома на вашем тексте.

Путь к тексту передаётся через параметр `--text_file`, а путь к файлу, 
в который будет сохранена модель, через параметр `--model_file`.

Параметры для настройки анализатора:
* `--ngrams` - необходимо передать число. Анализатор подсчитывает частотность 
каждой `n + 1`-й буквы для всех возможных `n` предыдущих, 
встречающихся в тексте подряд. Желаемое число `n` и есть этот параметр. По
умолчанию используется `n = 2`
* `--punc` необходимо указать, если в n-граммы не нужно игнорировать пунктуацию.
* `--top` - необходимо передать число. Ограничение для запоминания моделью только 
`n` самых частотоных слов.
* `--count_avg` необходимо указать, если вы хотите подсчитать статистику на вашем
тексте (крайне рекомендумется, улучшает точность взлома, но может замедлить 
обработку текста).

## Примеры

### encode

```
$ cat in.txt
Привет, как дела?
$ ./encryptor.py encode -c caesar -k 7 -i in.txt -a rus
Цчпймщ, сзс лмтз?
$ cat alph.txt 
приветкадл
$ ./encryptor.py encode -c caesar -k 7 -i in.txt -f alph.txt 
Пдлпри, вев трке?

$ cat in.txt 
Army is here.
$ ./encryptor.py encode -c vigenere -k bad -i in.txt
Brpz iv ieuf.
```

### decode

```
$ cat in.txt 
Army is here.
$ ./encryptor.py encode -c vigenere -k bad -i in.txt -o out.txt
$ cat out.txt 
Brpz iv ieuf.
$ ./encryptor.py decode -c vigenere -k bad -i out.txt
Army is here.
$ ./encryptor.py encode -c caesar -k 13 -i in.txt -o out.txt
$ cat out.txt 
NEzL vF urEr.
$ ./encryptor.py decode -c caesar -k 13 -i out.txt
Army is here.
```

### train

```
$ ./encryptor.py train -i models/original/WarAndPeace.txt -m models/rus -pc -t1000 -n2
$ ./encryptor.py train -i mytext.txt -m mymodel.txt -t 3000 -c -n 4
```

### hack

```
$ cat out.txt 
NEzL vF urEr.
$ ./encryptor.py hack -i out.txt
Army is here.
$ cat in.txt 
Привет, как дела?
$ ./encryptor.py encode -c caesar -k7 -i in.txt -o out.txt -a rus
$ cat out.txt 
Цчпймщ, сзс лмтз?
$ ./encryptor.py hack -i out.txt -m models/rus -a rus
Привет, как дела?
```

## Установка

Можно пользоваться скриптом encryptor.py, находящимся в папке encryptor,
а можно установить его при помощи setup.py (в таком случае во всех
примерах выше стоит заменить ./encryptor.py на просто encryptor)

```
$ python setup.py install
```