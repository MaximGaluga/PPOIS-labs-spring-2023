в# Отчет

В данной директории представлена реализация лаболаторной работы 3 по учебной дисциплине ППОИС. В рамках данной лабораторной работы было необходимо реализовать игру Asteroids используя библиотеку языка Python - Pygame.

В папке *util* находится вся необходимая для отрисовки спрайтов и обработки коллизий математика.

В файле *stage* находится определение класса, отвечающего за хранение, добавление, удаление и частичную обработку передвижения спрайтов.

Файл *soundManager* предоставляет собой обработчик звукых эффектов.

Файл *shooter* хранит в себе класс обработчика выстрелов и поведения пули.

Файл *ship* является реализацией класса игрока, хранящего параметры корабля, а также функции отрисовки, обработчики движения и выстрела. Примечательно, что корабю и выхлопу его двигателя выделены отдельные классы, так как последний имеет другое поведение требует особого обработчика отрисовки.

Файл *badies* описывает классы астеройдов, инопланетных кораблей и партиклов.

Файл *asteroids* объединяет в основном классе игры все остальные ресурсы, добавляя обработчик нажатий и игровое меню.