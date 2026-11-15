from abc import ABC, abstractmethod


# ==========================================
# БАЗОВЫЙ КЛАСС (без изменений)
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
        pass


# ==========================================
# МИКСИН (без изменений)
# ==========================================
class LoggingMixin:
    """Миксин, который печатает в консоль информацию о создании объекта."""

    def __init__(self, *args, **kwargs):
        class_name = self.__class__.__name__
        args_str = ", ".join(repr(arg) for arg in args)
        kwargs_str = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        all_params = f"{args_str}, {kwargs_str}" if args_str and kwargs_str else args_str or kwargs_str
        print(f"{class_name}({all_params})")
        super().__init__(*args, **kwargs)


# ==========================================
# КЛАСС PRODUCT (ДОБАВЛЕНА ПРОВЕРКА КОЛИЧЕСТВА)
# ==========================================
class Product(LoggingMixin, BaseProduct):

    def __init__(self, name: str, description: str, price: float, quantity: int):
        # ЗАДАНИЕ 1: Проверка на нулевое количество
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

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
# КЛАСС CATEGORY (ДОБАВЛЕН МЕТОД СРЕДНЕЙ ЦЕНЫ)
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

    # ЗАДАНИЕ 2: Метод подсчета средней цены
    def middle_price(self) -> float:
        """Возвращает среднюю цену товаров в категории. Если товаров нет — возвращает 0."""
        try:
            # Складываем цены всех товаров и делим на их количество
            total_price = sum(product.price for product in self.__products)
            return total_price / len(self.__products)
        except ZeroDivisionError:
            # Если товаров нет (деление на ноль), возвращаем 0
            return 0


# ==========================================
# КЛАССЫ-НАСЛЕДНИКИ (без изменений)
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
