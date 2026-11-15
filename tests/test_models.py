import pytest
from src.main import Product, Category, Smartphone, LawnGrass

# --- ФИКСТУРЫ ---
@pytest.fixture
def product_1():
    return Product("Яблоко", "Вкусное", 50, 10)

@pytest.fixture
def product_2():
    return Product("Груша", "Сладкая", 80, 5)

@pytest.fixture
def smartphone_1():
    # name, description, price, quantity, efficiency, model, memory, color
    return Smartphone("iPhone", "Смартфон", 100000, 2, 100, "13 Pro", 256, "Black")

@pytest.fixture
def smartphone_2():
    return Smartphone("Samsung", "Смартфон", 80000, 3, 90, "S21", 128, "White")

@pytest.fixture
def lawn_grass_1():
    # name, description, price, quantity, country, germination_period, color
    return LawnGrass("Трава", "Газонная", 1000, 50, "Россия", "10 дней", "Зеленый")


# --- ТЕСТЫ СТАРОГО ФУНКЦИОНАЛА ---
def test_product_initialization(product_1):
    assert product_1.name == "Яблоко"
    assert product_1.price == 50
    assert product_1.quantity == 10

def test_category_initialization():
    # Сбрасываем счетчики перед тестом
    Category.total_categories = 0
    Category.total_products = 0
    cat = Category("Фрукты", "Свежие")
    assert cat.name == "Фрукты"
    assert Category.total_categories == 1

def test_add_product_to_category(product_1):
    Category.total_products = 0 # Сброс
    cat = Category("Фрукты", "Свежие")
    cat.add_product(product_1)
    # Проверяем, что товар добавился (через геттер products)
    assert "Яблоко" in cat.products
    assert Category.total_products == 1

def test_product_str(product_1):
    assert str(product_1) == "Яблоко, 50 руб. Остаток: 10 шт."

def test_product_add_old_logic(product_1, product_2):
    # 50 * 10 + 80 * 5 = 500 + 400 = 900
    assert product_1 + product_2 == 900

def test_product_price_setter_valid(product_1):
    product_1.price = 150
    assert product_1.price == 150

def test_product_price_setter_invalid(capsys, product_1):
    product_1.price = -50
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


# --- ТЕСТЫ НОВОГО ФУНКЦИОНАЛА (Задания 1, 2, 3) ---
def test_smartphone_initialization(smartphone_1):
    assert smartphone_1.model == "13 Pro"
    assert smartphone_1.memory == 256
    assert smartphone_1.color == "Black"
    assert smartphone_1.efficiency == 100

def test_lawn_grass_initialization(lawn_grass_1):
    assert lawn_grass_1.country == "Россия"
    assert lawn_grass_1.germination_period == "10 дней"
    assert lawn_grass_1.color == "Зеленый"

def test_add_same_types(smartphone_1, smartphone_2):
    # 100000 * 2 + 80000 * 3 = 200000 + 240000 = 440000
    assert smartphone_1 + smartphone_2 == 440000

def test_add_different_types_error(smartphone_1, lawn_grass_1):
    with pytest.raises(TypeError):
        _ = smartphone_1 + lawn_grass_1
    with pytest.raises(TypeError):
        _ = lawn_grass_1 + smartphone_1

def test_add_invalid_object_to_category():
    cat = Category("Электроника", "Гаджеты")
    with pytest.raises(TypeError):
        cat.add_product("Просто строка")
    with pytest.raises(TypeError):
        cat.add_product(12345)

def test_add_heirs_to_category(smartphone_1, lawn_grass_1):
    cat = Category("Разное", "Товары")
    cat.add_product(smartphone_1)
    cat.add_product(lawn_grass_1)
    # Проверяем, что оба наследника добавились
    assert "iPhone" in cat.products
    assert "Трава" in cat.products

# ==========================================
# НОВЫЙ ТЕСТ ДЛЯ ЗАДАНИЯ 2 (Миксин)
# ==========================================
def test_logging_mixin_output(capsys):
    """Тест: миксин печатает информацию о создании объекта."""
    # Создаем объект (он должен напечатать текст)
    product = Product("Тестовый товар", "Описание", 500, 2)

    # Перехватываем то, что было напечатано
    captured = capsys.readouterr()

    # Проверяем, что в консоли есть название класса и параметры
    assert "Product('Тестовый товар', 'Описание', 500, 2)" in captured.out


# ==========================================
# ТЕСТЫ ДЛЯ ЗАДАНИЯ 17.1
# ==========================================

def test_product_zero_quantity_raises_error():
    """Тест: при создании товара с нулевым количеством выбрасывается ValueError."""
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Бракованный товар", "Описание", 100, 0)


def test_category_middle_price_empty():
    """Тест: средняя цена в пустой категории равна 0."""
    category = Category("Пустая категория", "Описание")
    assert category.middle_price() == 0


def test_category_middle_price_with_products():
    """Тест: корректный подсчет средней цены."""
    category = Category("Электроника", "Гаджеты")
    # Создаем товары с ценами 100 и 300 (средняя должна быть 200)
    p1 = Product("Товар 1", "Описание", 100, 5)
    p2 = Product("Товар 2", "Описание", 300, 2)

    category.add_product(p1)
    category.add_product(p2)

    # Проверяем, что средняя цена = 200
    assert category.middle_price() == 200
