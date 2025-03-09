import random

from django.core.management.base import BaseCommand

from ...models import Category, Product


class Command(BaseCommand):
    help = "Populate the Product model with sample data"

    def handle(self, *args, **kwargs):
        # Ensure categories exist before creating products
        if not Category.objects.exists():
            self.stdout.write(self.style.ERROR("No categories found. Run `populate_categories` first!"))
            return

        products = [
            ("Laptop", 1200.00, "A high-performance laptop for professionals and gamers.", "Technology"),
            ("Smartphone", 800.00, "Latest model with advanced camera and AI-powered features.", "Technology"),
            ("Wireless Earbuds", 150.00, "Noise-canceling wireless earbuds with long battery life.", "Technology"),
            ("Fiction Book", 25.00, "A thrilling novel from a bestselling author.", "Literature"),
            ("Running Shoes", 100.00, "Comfortable and durable running shoes for athletes.", "Fitness"),
            ("Smartwatch", 250.00, "Tracks your fitness and health metrics seamlessly.", "Fitness"),
            ("Cooking Pan", 45.00, "Non-stick frying pan for easy and healthy cooking.", "Food"),
            ("Espresso Machine", 350.00, "Brew rich and delicious espresso at home.", "Food"),
            ("Mountain Bike", 800.00, "Durable mountain bike for outdoor adventures.", "Sports"),
            ("Football", 30.00, "Professional-grade football for matches and training.", "Sports"),
            ("Noise-canceling Headphones", 200.00, "Immersive sound with active noise cancellation.", "Music"),
            ("Digital Camera", 700.00, "Capture high-resolution photos and 4K videos.", "Photography"),
            ("Movie Streaming Subscription", 15.00, "Access thousands of movies and TV shows online.", "Movies"),
            ("Political Science Book", 40.00, "A deep dive into global politics and governance.", "Politics"),
            ("History Documentary DVD", 20.00, "Explore major historical events and civilizations.", "History"),
            ("Investment Guide Book", 50.00, "Learn the secrets of smart investing.", "Finance"),
            ("Gaming Console", 500.00, "Next-gen gaming console with 4K graphics.", "Gaming"),
            ("Camping Tent", 120.00, "Waterproof and spacious tent for outdoor camping.", "Nature"),
            ("Travel Backpack", 75.00, "Durable and lightweight backpack for travel.", "Travel"),
            ("Fashion Sneakers", 130.00, "Stylish sneakers with a modern design.", "Fashion"),
        ]

        product_objects = []
        for name, price, description, category_name in products:
            category = Category.objects.filter(name=category_name).first()
            if category:
                product_objects.append(
                    Product(name=name, price=price, stock=random.randrange(5, 20) , description=description, category=category)
                )

        if product_objects:
            Product.objects.bulk_create(product_objects, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"Successfully inserted {len(product_objects)} products!"))
        else:
            self.stdout.write(self.style.WARNING("No products were added. Ensure the categories exist."))
