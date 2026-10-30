import json
from typing import List, Optional


class Product:
    """Класс для описания товара."""
    name: str
    description: str
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """Инициализация товара."""
        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут
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

        # Дополнительное задание к заданию 4: проверка на понижение цены
        if new_price < self.__price:
            confirm = input(f"Вы уверены, что хотите понизить цену с {self.__price} до {new_price}? (y/n): ")
            if confirm.lower() != 'y':
                return  # Отмена действия

        self.__price = new_price

    @classmethod
    def new_product(cls, product_data: dict, existing_products: Optional[List['Product']] = None) -> 'Product':
        """Класс-метод для создания товара из словаря (с проверкой дубликатов)."""
        name = product_data.get("name")
        description = product_data.get("description")
        price = product_data.get("price")
        quantity = product_data.get("quantity")

        if existing_products:
            for prod in existing_products:
                if prod.name == name:
                    # Если товар найден, складываем количества и выбираем макс. цену
                    prod.quantity += quantity
                    if price > prod.price:
                        prod._Product__price = price  # Обходим сеттер, чтобы не спрашивать подтверждение
                    return prod

        # Если дубликата нет, создаем новый
        return cls(name, description, price, quantity)


class Category:
    """Класс для описания категории товаров."""
    name: str
    description: str

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None) -> None:
        """Инициализация категории."""
        self.name = name
        self.description = description
        self.__products = products if products else []  # Приватный атрибут

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product) -> None:
        """Добавление продукта в категорию."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер для вывода списка товаров в виде строки."""
        result = ""
        for prod in self.__products:
            result += f"{prod.name}, {prod.price} руб. Остаток: {prod.quantity} шт.\n"
        return result


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