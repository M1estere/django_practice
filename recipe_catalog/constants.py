from .utils import Recipe

recipes = [
    Recipe(1, 'Суп с яичными хлопьями', [
               ('Бульон', 250, 100, 120),
               ('Яйцо', 140, 70, 80),
               ('Мука', 300, 150, 150),
               ('Молоко', 100, 50, 80),
               ('Пармезан', 300, 100, 350),
               ('Манная крупа', 150, 70, 80),
           ]),
    Recipe(2, 'Селёдочный салат', [
        ('Сельдь', 300, 150, 140),
        ('Картофель', 50, 120, 100),
        ('Свёкла', 75, 100, 90),
        ('Яблоки', 50, 75, 55),
        ('Сельдерей', 35, 60, 55),
        ('Укроп', 55, 75, 65),
    ])
]