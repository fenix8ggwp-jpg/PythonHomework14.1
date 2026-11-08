from src.models import Category, Product, CategoryIterator


def main() -> None:
    """Точка входа в программу."""
    product1 = Product("Samsung Galaxy S23", "256GB, Серый", 50000.0, 10)
    product2 = Product("Iphone 15", "512GB, Черный", 100000.0, 5)

    category1 = Category("Смартфоны", "Телефоны", [product1])
    category1.add_product(product2)

    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")
    print("\nТовары в категории 'Смартфоны':")
    print(category1.products)

    print("Пробуем установить отрицательную цену:")
    product1.price = -100

    print("\nСоздаем новый товар через класс-метод:")
    new_prod = Product.new_product({
        "name": "Xiaomi",
        "description": "128GB",
        "price": 20000.0,
        "quantity": 20
    })
    print(f"Создан товар: {new_prod.name}, Цена: {new_prod.price}")

    print("\n--- Демонстрация новых методов ---")
    p1 = Product("Samsung", "256GB", 100.0, 10)
    p2 = Product("Iphone", "512GB", 200.0, 2)

    print("Строка продукта:", p1)
    print("Строка категории:", category1)
    print(f"Общая стоимость (p1 + p2): {p1 + p2} руб.")

    print("\nПеребор товаров в категории через итератор:")
    for product in CategoryIterator(category1):
        print(product.name)


if __name__ == "__main__":
    main()
