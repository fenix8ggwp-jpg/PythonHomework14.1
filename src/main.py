from abc import ABC, abstractmethod


# ==========================================
# ЗАДАНИЕ 1: Абстрактный класс BaseProduct
# ==========================================
class BaseProduct(ABC):
    """Базовый абстрактный класс для всех продуктов."""

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.quantity = quantity

    @abstractmethod
    def __str__(self):
        """Строковое отображение продукта."""
        pass


# ==========================================
# ЗАДАНИЕ 2: Класс-миксин
# ==========================================
class LoggingMixin:
    """Миксин, который печатает в консоль информацию о создании объекта."""

    def __init__(self, *args, **kwargs):
        # Печатаем информацию
        class_name = self.__class__.__name__
        # Собираем аргументы в читаемый вид
        args_str = ", ".join(repr(arg) for arg in args)
        kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())

        # Формируем строку (с запятыми между позиционными и именованными)
        if args_str and kwargs_str:
            all_params = f"{args_str}, {kwargs_str}"
        else:
            all_params = args_str or kwargs_str

        print(f"{class_name}({all_params})")

        # Обязательно вызываем super().__init__, чтобы цепочка наследования работала
        super().__init__(*args, **kwargs)


# ==========================================
# Класс Product (теперь наследуется от Mixin и ABC)
# ==========================================
class Product(LoggingMixin, BaseProduct):
    """Класс для продуктов. Наследует миксин и абстрактный класс."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        # Так как BaseProduct абстрактный, мы должны вызвать его __init__
        super().__init__(name, description, price, quantity)
        self.price = price

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price: float):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов!")
        return (self.price * self.quantity) + (other.price * other.quantity)


# ==========================================
# Класс Category (без изменений)
# ==========================================
class Category:
    total_categories = 0
    total_products = 0

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.__products = []
        Category.total_categories += 1

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только объекты Product и его наследников!")
        self.__products.append(product)
        Category.total_products += 1

    @property
    def products(self):
        return "\n".join([str(product) for product in self.__products])

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


# ==========================================
# Классы-наследники (без изменений)
# ==========================================
class Smartphone(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: int, model: str, memory: int, color: str):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color
