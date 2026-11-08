import json
from typing import List, Optional


class Product:
    """Класс для описания товара."""
    name: str
    description: str
    quantity: int

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        """Инициализация товара."""
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Геттер для получения цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для установки цены с проверкой."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            confirm = input(
                f"Вы уверены, что хотите понизить цену "
                f"с {self.__price} до {new_price}? (y/n): "
            )
            if confirm.lower() != 'y':
                return

        self.__price = new_price

    def __str__(self) -> str:
        """Строковое отображение товара."""
        return (
            f"{self.name}, {self.price} руб. "
            f"Остаток: {self.quantity} шт."
        )

    def __add__(self, other: 'Product') -> float:
        """Сложение товаров (общая стоимость на складе)."""
        if isinstance(other, Product):
            return (
                (self.price * self.quantity) +
                (other.price * other.quantity)
            )
        raise TypeError("Можно складывать только товары!")

    @classmethod
    def new_product(
        cls, product_data: dict,
        existing_products: Optional[List['Product']] = None
    ) -> 'Product':
        """Класс-метод для создания товара из словаря."""
        name = product_data.get("name")
        description = product_data.get("description")
        price = product_data.get("price")
        quantity = product_data.get("quantity")

        if existing_products:
            for prod in existing_products:
                if prod.name == name:
                    prod.quantity += quantity
                    if price > prod.price:
                        prod._Product__price = price
                    return prod

        return cls(name, description, price, quantity)


class Category:
    """Класс для описания категории товаров."""
    name: str
    description: str

    category_count: int = 0
    product_count: int = 0

    def __init__(
        self, name: str, description: str,
        products: Optional[List[Product]] = None
    ) -> None:
        """Инициализация категории."""
        self.name = name
        self.description = description
        self.__products = products if products else []

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product) -> None:
        """Добавление продукта в категорию."""
        self.__products.append(product)
        Category.product_count += 1

    def get_products(self) -> List[Product]:
        """Возвращает список объектов Product."""
        return self.__products

    @property
    def products(self) -> str:
        """Геттер для вывода списка товаров в виде строки."""
        return "".join([str(prod) + "\n" for prod in self.__products])

    def __str__(self) -> str:
        """Строковое отображение категории."""
        total_quantity = sum(
            prod.quantity for prod in self.__products
        )
        return (
            f"{self.name}, количество продуктов: "
            f"{total_quantity} шт."
        )


class CategoryIterator:
    """Итератор для перебора товаров в категории."""

    def __init__(self, category: Category):
        """Инициализация итератора."""
        self._products = category.get_products()
        self._index = 0

    def __iter__(self):
        """Возвращает итератор."""
        return self

    def __next__(self) -> Product:
        """Возвращает следующий товар."""
        if self._index < len(self._products):
            result = self._products[self._index]
            self._index += 1
            return result
        raise StopIteration


def load_data_from_json(file_path: str) -> List[Category]:
    """Загрузка категорий и товаров из JSON."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    categories = []
    for cat_data in data:
        products = []
        for prod_data in cat_data.get("products", []):
            product = Product.new_product(prod_data)
            products.append(product)

        category = Category(
            name=cat_data["name"],
            description=cat_data["description"],
            products=products
        )
        categories.append(category)

    return categories
