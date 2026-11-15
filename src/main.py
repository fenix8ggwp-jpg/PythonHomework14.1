class Product:
    """Базовый класс для всех продуктов."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут цены (из домашки 14.2)
        self.quantity = quantity

    @property
    def price(self):
        """Геттер для цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float):
        """Сеттер для цены с проверкой."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price

    def __str__(self):
        """Строковое отображение."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """
        Сложение товаров
        Задание 2: Ограничение сложения по типу.
        """
        # Проверяем, что типы объектов абсолютно одинаковые
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов!")

        # Считаем общую стоимость: (цена * количество) + (цена * количество)
        return (self.price * self.quantity) + (other.price * other.quantity)


class Category:
    """Класс категории товаров."""

    # Атрибуты класса
    total_categories = 0
    total_products = 0

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.__products = []  # Приватный список товаров

        # Увеличиваем счетчики при создании категории
        Category.total_categories += 1

    def add_product(self, product):
        """
        Добавление продукта в категорию.
        Задание 3 (текущее): Защита от добавления посторонних объектов.
        """
        # Проверяем, является ли объект экземпляром Product или его наследником
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только объекты Product и его наследников!")

        self.__products.append(product)
        Category.total_products += 1

    @property
    def products(self):
        """
        Геттер для вывода списка товаров.
        """
        return "\n".join([str(product) for product in self.__products])

    def __str__(self):
        """Строковое отображение категории."""
        # Считаем общее количество товаров на складе
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


class Smartphone(Product):
    """Класс Смартфон (наследник Product)."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: int, model: str, memory: int, color: str):
        # Вызываем конструктор родителя
        super().__init__(name, description, price, quantity)

        # Добавляем уникальные атрибуты смартфона
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс Трава газонная (наследник Product)."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        # Вызываем конструктор родителя
        super().__init__(name, description, price, quantity)

        # Добавляем уникальные атрибуты травы
        self.country = country
        self.germination_period = germination_period
        self.color = color