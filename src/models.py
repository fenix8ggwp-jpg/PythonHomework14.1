import json
from typing import List


class Product:
    """Класс для описания товара."""
    name: str
    description: str
    price: float
    quantity: int

    def __init__(
            self, name: str, description: str, price: float, quantity: int
    ) -> None:
        """Инициализация товара."""
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс для описания категории товаров."""
    name: str
    description: str
    products: List[Product]

    # Атрибуты класса (общие для всех экземпляров)
    category_count: int = 0
    product_count: int = 0

    def __init__(
            self, name: str, description: str, products: List[Product] = None
    ) -> None:
        """Инициализация категории."""
        self.name = name
        self.description = description
        self.products = products if products else []

        # Увеличиваем счетчики при создании новой категории
        Category.category_count += 1
        # Добавляем к общему количеству товаров количество
        # товаров в этой категории
        Category.product_count += len(self.products)


def load_data_from_json(file_path: str) -> List[Category]:
    """Дополнительное задание: загрузка категорий и товаров из JSON."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    categories = []
    for cat_data in data:
        products = []
        for prod_data in cat_data.get("products", []):
            product = Product(
                name=prod_data["name"],
                description=prod_data["description"],
                price=prod_data["price"],
                quantity=prod_data["quantity"]
            )
            products.append(product)

        category = Category(
            name=cat_data["name"],
            description=cat_data["description"],
            products=products
        )
        categories.append(category)

    return categories
