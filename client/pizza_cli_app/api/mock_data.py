pizzas = [
    {"id": 1, "name": "Margherita", "description": "Tomato, mozzarella, and basil.", "price": 8.0},
    {"id": 2, "name": "Pepperoni", "description": "Tomato, mozzarella, and pepperoni.", "price": 10.0},
    {"id": 3, "name": "BBQ Chicken", "description": "BBQ sauce, chicken, red onions, and cilantro.", "price": 12.0},
    {"id": 4, "name": "Veggie", "price": 11.0},
    {"id": 5, "name": "Hawaiian", "description": "Tomato, mozzarella, ham, and pineapple.", "price": 10.5},
    {"id": 6, "name": "Meat Lovers", "description": "Tomato, mozzarella, pepperoni, sausage, ham, and bacon.", "price": 13.0},
    {"id": 7, "name": "Margherita Deluxe", "description": "Tomato, mozzarella, cherry tomatoes, basil, and garlic.", "price": 9.0},
    {"id": 8, "name": "Buffalo Chicken", "description": "Buffalo sauce, chicken, ranch, and red onions.", "price": 12.5},
    {"id": 9, "name": "Cheese", "price": 7.0},
    {"id": 10, "name": "Supreme", "description": "Tomato, mozzarella, pepperoni, sausage, mushrooms, onions, and olives.", "price": 14.0},
    {"id": 11, "name": "Garden", "description": "Tomato, mozzarella, spinach, artichokes, and olives.", "price": 11.5},
    {"id": 12, "name": "Sausage", "description": "Tomato, mozzarella, and sausage.", "price": 10.5},
    {"id": 13, "name": "Bacon", "description": "Tomato, mozzarella, and bacon.", "price": 11.0},
    {"id": 14, "name": "Mushroom", "description": "Tomato, mozzarella, and mushrooms.", "price": 10.0},
    {"id": 15, "name": "Onion", "description": "Tomato, mozzarella, and onions.", "price": 9.5},
    {"id": 16, "name": "Black Olive", "description": "Tomato, mozzarella, and black olives.", "price": 9.5},
    {"id": 17, "name": "White", "description": "Garlic, mozzarella, and ricotta.", "price": 10.0},
    {"id": 18, "name": "Spinach", "description": "Garlic, mozzarella, spinach, and artichokes.", "price": 11.5},
    {"id": 19, "name": "Chicken Alfredo", "description": "Alfredo sauce, chicken, and mozzarella.", "price": 12.0},
    {"id": 20, "name": "Pesto", "description": "Pesto sauce, mozzarella, and cherry tomatoes.", "price": 11.0},
    {"id": 21, "name": "Taco", "description": "Taco sauce, ground beef, lettuce, and tomatoes.", "price": 11.5},
    {"id": 22, "name": "Seafood", "description": "Tomato, mozzarella, shrimp, calamari, and clams.", "price": 14.0},
    {"id": 23, "name": "Caprese", "description": "Tomato, mozzarella, basil, and balsamic glaze.", "price": 11.0},
    {"id": 24, "name": "Greek", "description": "Tomato, mozzarella, feta, kalamata olives, and red onions.", "price": 12.0},
    {"id": 25, "name": "Buffalo Cauliflower", "description": "Buffalo sauce, cauliflower, and ranch.", "price": 12.5}
]


cart = {
    'id': 12345,
    'total_price': 55.95,
    'cart_items': [
        {
            'id': 1,
            'total_price': 10.99,
            'pizza_id': 101,
            'pizza_name': 'Margherita',
            'quantity': 1,
            'size': 'small',
            'dough': 'thin'
        },
        {
            'id': 2,
            'total_price': 13.99,
            'pizza_id': 102,
            'pizza_name': 'Pepperoni',
            'quantity': 1,
            'size': 'medium',
            'dough': 'classic'
        },
        {
            'id': 3,
            'total_price': 16.99,
            'pizza_id': 103,
            'pizza_name': 'Veggie Delight',
            'quantity': 1,
            'size': 'large',
            'dough': 'thin'
        },
        {
            'id': 4,
            'total_price': 10.99,
            'pizza_id': 101,
            'pizza_name': 'Margherita',
            'quantity': 1,
            'size': 'small',
            'dough': 'classic'
        },
        {
            'id': 5,
            'total_price': 12.99,
            'pizza_id': 104,
            'pizza_name': 'BBQ Chicken',
            'quantity': 1,
            'size': 'medium',
            'dough': 'thin'
        },
        {
            'id': 1,
            'total_price': 10.99,
            'pizza_id': 101,
            'pizza_name': 'Margherita',
            'quantity': 1,
            'size': 'small',
            'dough': 'thin'
        },
        {
            'id': 2,
            'total_price': 13.99,
            'pizza_id': 102,
            'pizza_name': 'Pepperoni',
            'quantity': 1,
            'size': 'medium',
            'dough': 'classic'
        },
        {
            'id': 3,
            'total_price': 16.99,
            'pizza_id': 103,
            'pizza_name': 'Veggie Delight',
            'quantity': 1,
            'size': 'large',
            'dough': 'thin'
        },
        {
            'id': 4,
            'total_price': 10.99,
            'pizza_id': 101,
            'pizza_name': 'Margherita',
            'quantity': 1,
            'size': 'small',
            'dough': 'classic'
        },
        {
            'id': 5,
            'total_price': 12.99,
            'pizza_id': 104,
            'pizza_name': 'BBQ Chicken',
            'quantity': 1,
            'size': 'medium',
            'dough': 'thin'
        },
        {
            'id': 1,
            'total_price': 10.99,
            'pizza_id': 101,
            'pizza_name': 'Margherita',
            'quantity': 1,
            'size': 'small',
            'dough': 'thin'
        },
        {
            'id': 2,
            'total_price': 13.99,
            'pizza_id': 102,
            'pizza_name': 'Pepperoni',
            'quantity': 1,
            'size': 'medium',
            'dough': 'classic'
        },
        {
            'id': 3,
            'total_price': 16.99,
            'pizza_id': 103,
            'pizza_name': 'Veggie Delight',
            'quantity': 1,
            'size': 'large',
            'dough': 'thin'
        },
        {
            'id': 4,
            'total_price': 10.99,
            'pizza_id': 101,
            'pizza_name': 'Margherita',
            'quantity': 1,
            'size': 'small',
            'dough': 'classic'
        },
        {
            'id': 5,
            'total_price': 12.99,
            'pizza_id': 104,
            'pizza_name': 'BBQ Chicken',
            'quantity': 1,
            'size': 'medium',
            'dough': 'thin'
        },
        {
            'id': 1,
            'total_price': 10.99,
            'pizza_id': 101,
            'pizza_name': 'Margherita',
            'quantity': 1,
            'size': 'small',
            'dough': 'thin'
        },
        {
            'id': 2,
            'total_price': 13.99,
            'pizza_id': 102,
            'pizza_name': 'Pepperoni',
            'quantity': 1,
            'size': 'medium',
            'dough': 'classic'
        },
        {
            'id': 3,
            'total_price': 16.99,
            'pizza_id': 103,
            'pizza_name': 'Veggie Delight',
            'quantity': 1,
            'size': 'large',
            'dough': 'thin'
        },
        {
            'id': 4,
            'total_price': 10.99,
            'pizza_id': 101,
            'pizza_name': 'Margherita',
            'quantity': 1,
            'size': 'small',
            'dough': 'classic'
        },
        {
            'id': 5,
            'total_price': 12.99,
            'pizza_id': 104,
            'pizza_name': 'BBQ Chicken',
            'quantity': 1,
            'size': 'medium',
            'dough': 'thin'
        }
    ]
}