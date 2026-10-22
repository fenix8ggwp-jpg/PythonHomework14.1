from src.models import Category, Product, load_data_from_json


def main() -> None:
    """Точка входа в программу."""
    # Создаем товары
    product1 = Product("Samsung Galaxy S23", "256GB, Серый", 50000.0, 10)
    product2 = Product("Iphone 15", "512GB, Черный", 100000.0, 5)
    product3 = Product("Xiaomi Redmi", "128GB, Синий", 20000.0, 20)

    # Создаем категории
    category1 = Category("Смартфоны", "Телефоны", [product1, product2])
    category2 = Category("Бюджетные", "Недорогие", [product3])
    category3 = Category("Ноутбуки", "Портативные", [])

    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")
    print(f"В категории '{category1.name}' товаров: {len(category1.products)}")
    print(f"В категории '{category2.name}' товаров: {len(category2.products)}")
    print(f"В категории '{category3.name}' товаров: {len(category3.products)}")

    try:
        categories = load_data_from_json("products.json")
        print(f"Загружено категорий из JSON: {len(categories)}")
    except FileNotFoundError:
        print("Файл products.json не найден.")
