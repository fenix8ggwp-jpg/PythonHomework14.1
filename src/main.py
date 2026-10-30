from src.models import Category, Product, load_data_from_json


def main() -> None:
    """Точка входа в программу."""
    product1 = Product("Samsung Galaxy S23", "256GB, Серый", 50000.0, 10)
    product2 = Product("Iphone 15", "512GB, Черный", 100000.0, 5)

    category1 = Category("Смартфоны", "Телефоны", [product1])

    # Демонстрация метода add_product
    category1.add_product(product2)

    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")

    # Демонстрация геттера products
    print("\nТовары в категории 'Смартфоны':")
    print(category1.products)

    # Демонстрация работы сеттера цены
    print("Пробуем установить отрицательную цену:")
    product1.price = -100

    # Демонстрация класс-метода new_product
    print("\nСоздаем новый товар через класс-метод:")
    new_prod = Product.new_product({
        "name": "Xiaomi", "description": "128GB, Синий", "price": 20000.0, "quantity": 20
    })
    print(f"Создан товар: {new_prod.name}, Цена: {new_prod.price}")


if __name__ == "__main__":
    main()
