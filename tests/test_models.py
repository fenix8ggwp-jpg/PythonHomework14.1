import json
#import pytest#from unittest.mock import patch
from src.models import Category, Product, load_data_from_json
def test_category_add_product():
    """Тест добавления товара через метод add_product."""
    Category.category_count = 0
    Category.product_count = 0

    p1 = Product("Товар 1", "Описание", 100.0, 1)
    category = Category("Категория", "Описание")

    category.add_product(p1)

    assert Category.product_count == 1
    assert "Товар 1, 100.0 руб. Остаток: 1 шт." in category.products


def test_product_price_setter_valid():
    """Тест установки корректной цены."""
    p = Product("Товар", "Описание", 100.0, 1)
    p.price = 150.0
    assert p.price == 150.0


def test_product_price_setter_invalid(capsys):
    """Тест установки неверной цены (должно вывестись сообщение)."""
    p = Product("Товар", "Описание", 100.0, 1)
    p.price = -50.0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert p.price == 100.0  # Цена не изменилась


def test_product_new_product():
    """Тест класс-метода new_product."""
    data = {"name": "Новый", "description": "Описание", "price": 200.0, "quantity": 5}
    p = Product.new_product(data)
    assert p.name == "Новый"
    assert p.price == 200.0
    assert p.quantity == 5


def test_product_new_product_duplicate():
    """Тест класс-метода new_product с дубликатом."""
    p1 = Product("Новый", "Описание", 200.0, 5)
    existing = [p1]
    data = {"name": "Новый", "description": "Другое", "price": 250.0, "quantity": 3}

    p2 = Product.new_product(data, existing)

    assert p2.quantity == 8  # 5 + 3
    assert p2.price == 250.0  # Выбрали максимальную цену
    assert len(existing) == 1  # Новый объект не создан


def test_load_data_from_json(tmp_path):
    """Тест загрузки данных из JSON."""
    test_data = [
        {
            "name": "Смартфоны",
            "description": "Мобильные телефоны",
            "products": [
                {
                    "name": "Samsung",
                    "description": "256GB",
                    "price": 50000.0,
                    "quantity": 10
                }
            ]
        }
    ]

    file_path = tmp_path / "test_products.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False)

    categories = load_data_from_json(str(file_path))

    assert len(categories) == 1
    assert categories[0].name == "Смартфоны"

from unittest.mock import patch

def test_main_execution():
    """Тест запуска функции main для покрытия src/main.py."""
    from src.main import main
    with patch("builtins.input", return_value="n"): # На случай, если сработает сеттер
        with patch("builtins.print"):
            main()
