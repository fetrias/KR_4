from sqlalchemy import text

from app.db import engine


def seed_initial_products() -> None:
    products = [
        {"title": "Headphones", "price": 99.99, "count": 5},
        {"title": "Speaker", "price": 149.0, "count": 3},
    ]

    with engine.begin() as conn:
        for product in products:
            conn.execute(
                text(
                    "INSERT INTO products (title, price, count) VALUES (:title, :price, :count)"
                ),
                product,
            )


if __name__ == "__main__":
    seed_initial_products()
