>>> from bruteforceDict import bruteforceDict
>>> a = bruteforceDict(count=4, fileName='res.txt', chars='asd')
>>> a.toFile() # Запись в файл res.txt
>>> arr = []
>>> for i in a.bruteforce():
>>>     arr.append(i) # Заполнение массива
>>> print(*arr)