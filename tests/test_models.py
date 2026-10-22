import json
from unittest.mock import patch

import pytest

from src.models import Category, Product, load_data_from_json


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Сбрасывает счетчики перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


def test_product_initialization():
    """Тест корректности инициализации Product."""
    product = Product("Телефон", "Описание", 1000.0, 5)
    assert product.name == "Телефон"
    assert product.description == "Описание"
    assert product.price == 1000.0
    assert product.quantity == 5


def test_category_initialization():
    """Тест корректности инициализации Category."""
    product = Product("Телефон", "Описание", 1000.0, 5)
    category = Category("Электроника", "Гаджеты", [product])

    assert category.name == "Электроника"
    assert category.description == "Гаджеты"
    assert len(category.products) == 1
    assert category.products[0].name == "Телефон"


def test_category_count():
    """Тест подсчета количества категорий."""
    Category("Категория 1", "Описание")
    Category("Категория 2", "Описание")
    assert Category.category_count == 2


def test_product_count():
    """Тест подсчета количества продуктов."""
    p1 = Product("Товар 1", "Описание", 100.0, 1)
    p2 = Product("Товар 2", "Описание", 200.0, 2)
    p3 = Product("Товар 3", "Описание", 300.0, 3)

    Category("Категория 1", "Описание", [p1, p2])
    Category("Категория 2", "Описание", [p3])
    Category("Категория 3", "Описание", [])

    assert Category.product_count == 3


def test_load_data_from_json(tmp_path):
    """Тест загрузки данных из JSON (дополнительное задание)."""
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
    assert len(categories[0].products) == 1
    assert categories[0].products[0].name == "Samsung"
    assert Category.category_count == 1
    assert Category.product_count == 1


@patch("builtins.print")
def test_main_function(mock_print):
    """Тест запуска функции main."""
    from src.main import main
    main()
    assert mock_print.called
