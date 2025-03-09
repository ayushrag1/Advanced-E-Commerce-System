from django.core.management.base import BaseCommand

from ...models import Category


class Command(BaseCommand):
    help = "Populate the Category model with sample data"

    def handle(self, *args, **kwargs):
        categories = [
            ("Technology", "Latest advancements in AI, software development, and emerging tech trends."),
            ("Science", "Discoveries, research, and breakthroughs in physics, chemistry, and biology."),
            ("Health", "Articles and tips on wellness, medical research, and healthy living."),
            ("Sports", "Updates on global sports events, athletes, and fitness routines."),
            ("Education", "Innovations in learning, teaching methods, and academic research."),
            ("Entertainment", "The latest movies, TV shows, celebrity news, and entertainment trends."),
            ("Business", "Market trends, entrepreneurship, and corporate insights."),
            ("Travel", "Guides, experiences, and tips for exploring destinations worldwide."),
            ("Food", "Delicious recipes, culinary arts, and restaurant reviews."),
            ("Fashion", "Latest fashion trends, designers, and style inspiration."),
            ("Music", "News, reviews, and history of music across genres."),
            ("Photography", "Tips, tricks, and inspiration for photographers."),
            ("Movies", "Film reviews, industry news, and behind-the-scenes insights."),
            ("Politics", "Analysis and updates on local and international political affairs."),
            ("History", "Exploring historical events, figures, and civilizations."),
            ("Literature", "Book reviews, writing tips, and discussions on classic and modern literature."),
            ("Fitness", "Workout routines, diet tips, and mental health guidance."),
            ("Gaming", "Video game news, reviews, and esports coverage."),
            ("Nature", "Wildlife, conservation, and environmental awareness topics."),
            ("Finance", "Investment strategies, personal finance management, and economic trends."),
        ]

        category_objects = [
            Category(name=name, description=description) for name, description in categories
        ]

        # Bulk insert the categories
        Category.objects.bulk_create(category_objects, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(f"Successfully inserted {len(categories)} categories!"))
