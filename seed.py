from app import create_app
from extensions import db
from models import User, Category, Product, CartItem, Favorite, Order


def seed():
    app = create_app()
    with app.app_context():
        # Создаём таблицы, если их ещё нет
        db.create_all()

        # Чистим старые данные (на случай повторного запуска)
        Order.query.delete()
        Favorite.query.delete()
        CartItem.query.delete()
        Product.query.delete()
        Category.query.delete()
        User.query.delete()
        db.session.commit()

        # === Категории ===
        cat_tshirts = Category(name='Футболки', slug='tshirts')
        cat_notebooks = Category(name='Блокноты', slug='notebooks')
        cat_hoodies = Category(name='Кофты', slug='hoodies')
        db.session.add_all([cat_tshirts, cat_notebooks, cat_hoodies])
        db.session.commit()

        # === Товары ===
        tshirt_names = [
            'Футболка СКСиС', 'Футболка oversize', 'Футболка белая',
            'Футболка чёрная', 'Футболка с принтом', 'Футболка базовая',
            'Футболка поло', 'Футболка с логотипом', 'Футболка с карманом',
            'Футболка хлопок',
        ]
        notebook_names = [
            'Блокнот А5', 'Блокнот А4', 'Блокнот в клетку',
            'Блокнот в линейку', 'Блокнот на пружине', 'Блокнот кожаный',
            'Блокнот с закладкой', 'Блокнот в точку', 'Блокнот мини',
            'Блокнот подарочный',
        ]
        hoodie_names = [
            'Кофта с капюшоном', 'Кофта oversize', 'Кофта на молнии',
            'Кофта серая', 'Кофта чёрная', 'Кофта с принтом',
            'Кофта тёплая', 'Кофта с карманом', 'Кофта базовая',
            'Кофта спортивная',
        ]

        products = []

        for i, name in enumerate(tshirt_names):
            products.append(Product(
                title=name,
                price=1500 + i * 100,
                image='/products/tshirt-1.jpg' if i % 2 == 0 else '/products/tshirt-2.jpg',
                category_id=cat_tshirts.id,
            ))

        for i, name in enumerate(notebook_names):
            products.append(Product(
                title=name,
                price=300 + i * 50,
                image='/products/notebook.jpg',
                category_id=cat_notebooks.id,
            ))

        for i, name in enumerate(hoodie_names):
            products.append(Product(
                title=name,
                price=2500 + i * 150,
                image='/products/hoodie.jpg',
                category_id=cat_hoodies.id,
            ))

        db.session.add_all(products)
        db.session.commit()

        # === Пользователи ===
        users_data = [
            ('ivan@example.com', 'Иван Иванов', '+7 (900) 111-11-11', 'password123'),
            ('maria@example.com', 'Мария Петрова', '+7 (900) 222-22-22', 'password123'),
            ('alexey@example.com', 'Алексей Смирнов', '+7 (900) 333-33-33', 'password123'),
            ('olga@example.com', 'Ольга Кузнецова', '+7 (900) 444-44-44', 'password123'),
            ('dmitry@example.com', 'Дмитрий Попов', '+7 (900) 555-55-55', 'password123'),
        ]

        users = []
        for email, name, phone, pwd in users_data:
            u = User(email=email, name=name, phone=phone)
            u.set_password(pwd)
            users.append(u)
        db.session.add_all(users)
        db.session.commit()

        # === Избранное ===
        for p in products[:3]:
            db.session.add(Favorite(user_id=users[0].id, product_id=p.id))

        # === Корзина ===
        db.session.add(CartItem(
            user_id=users[0].id,
            product_id=products[0].id,
            qty=1,
            size='m',
        ))
        db.session.commit()

        # === Заказы ===
        cities = ['Сыктывкар', 'Ухта', 'Воркута', 'Печора', 'Инта']
        statuses = ['new', 'paid', 'shipped']

        for i in range(15):
            p = products[i % len(products)]
            u = users[i % len(users)]
            qty = 1 + (i % 3)
            delivery = 'courier' if i % 2 else 'pickup'
            delivery_price = 500 if delivery == 'courier' else 200
            total = p.price * qty + delivery_price

            db.session.add(Order(
                user_id=u.id,
                product_id=p.id,
                qty=qty,
                size='m',
                customer_name=u.name,
                phone=u.phone or '+7 (900) 000-00-00',
                address='ул. Ленина, 1',
                city=cities[i % len(cities)],
                delivery=delivery,
                delivery_price=delivery_price,
                total=total,
                status=statuses[i % len(statuses)],
            ))

        db.session.commit()

        # === Итог ===
        print('✅ Seed готов:')
        print(f'   Категорий: {Category.query.count()}')
        print(f'   Товаров:   {Product.query.count()}')
        print(f'   Юзеров:    {User.query.count()}')
        print(f'   Заказов:   {Order.query.count()}')
        print(f'   Избранных: {Favorite.query.count()}')
        print(f'   В корзине: {CartItem.query.count()}')


if __name__ == '__main__':
    seed()