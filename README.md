Вариант №17

Задание №3 

Разработать инструмент командной строки для учебного конфигурационного 
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из 
входного формата в выходной. Синтаксические ошибки выявляются с выдачей 
сообщений. 

Входной текст на учебном конфигурационном языке принимается из 
стандартного ввода. Выходной текст на языке json попадает в файл, путь к 
которому задан ключом командной строки. 

Однострочные комментарии: 

:: Это однострочный комментарий 

Многострочные комментарии: 

/* 
Это многострочный 
комментарий 
*/ 

[ 
Словари: 
имя => значение, 
имя => значение, 
имя => значение, 
... 
] 

Имена:

[a-z]+ 

Значения: 

• Числа. 

• Словари. 

Объявление константы на этапе трансляции: 

(def имя значение); 

Вычисление константы на этапе трансляции: 

#{имя} 

Результатом вычисления константного выражения является значение. 

Все конструкции учебного конфигурационного языка (с учетом их 
возможной вложенности) должны быть покрыты тестами. Необходимо показать 2 
примера описания конфигураций из разных предметных областей.

Запуск программы - python main.py output.json
