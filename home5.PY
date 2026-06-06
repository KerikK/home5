from datetime import datetime, timedelta


# MODELS

class NewsArticle:
    """Represents a news article"""

    def __init__(self, headline, content, author, category="General"):
        self.headline = headline
        self.content = content
        self.author = author
        self.category = category
        self.created_at = datetime.now()
        self.likes = 0
        self.comments = []

    def is_breaking_news(self):
        """Check if article is newer than 2 hours"""
        return datetime.now() - self.created_at < timedelta(hours=2)

    def add_like(self):
        self.likes += 1

    def add_comment(self, author, text):
        self.comments.append({
            "author": author,
            "text": text,
            "created_at": datetime.now()
        })


class NewsManager:
    """Simple database manager"""

    def __init__(self):
        self._articles = []

    def create(self, **kwargs):
        article = NewsArticle(**kwargs)
        self._articles.append(article)
        return article

    def all(self):
        return self._articles

    def filter_by_category(self, category):
        return [
            article for article in self._articles
            if article.category.lower() == category.lower()
        ]

    def get_breaking_news(self):
        return [
            article for article in self._articles
            if article.is_breaking_news()
        ]


db = NewsManager()


# TEMPLATES

def header_template():
    return "=" * 50 + "\n" + "SUPER NEWS PORTAL".center(50) + "\n" + "=" * 50


def menu_template():
    return """
1. Show all news
2. Show breaking news
3. Create article
4. View article details
5. Search by category
0. Exit
"""


def article_list_template(articles, title="News"):
    result = f"\n=== {title} ===\n"

    if not articles:
        return result + "No articles found.\n"

    for index, article in enumerate(articles, start=1):
        breaking = "[BREAKING]" if article.is_breaking_news() else ""

        result += f"""
{index}. {article.headline} {breaking}
   Author: {article.author}
   Category: {article.category}
   Likes: {article.likes}
"""

    return result


def article_detail_template(article):
    result = f"""
{'=' * 50}
{article.headline}
{'=' * 50}
Author: {article.author}
Category: {article.category}
Date: {article.created_at.strftime('%d.%m.%Y %H:%M')}
Likes: {article.likes}

Content:
{article.content}

Comments:
"""

    if not article.comments:
        result += "No comments yet.\n"
    else:
        for comment in article.comments:
            result += f"- {comment['author']}: {comment['text']}\n"

    return result


# VIEWS

def index_view():
    print(header_template())
    print(menu_template())


def list_articles_view():
    articles = db.all()
    print(article_list_template(articles, "All News"))


def breaking_news_view():
    articles = db.get_breaking_news()
    print(article_list_template(articles, "Breaking News"))


def article_detail_view(index):
    articles = db.all()

    if index < 1 or index > len(articles):
        print("Article not found.")
        return

    article = articles[index - 1]

    print(article_detail_template(article))

    like = input("Add like? (y/n): ").strip().lower()
    if like == "y":
        article.add_like()
        print("Like added.")

    comment = input("Add comment? (y/n): ").strip().lower()
    if comment == "y":
        author = input("Your name: ")
        text = input("Comment: ")
        article.add_comment(author, text)
        print("Comment added.")


def create_article_view(data):
    article = db.create(**data)
    print(f"Article '{article.headline}' created successfully.")


def category_view(category):
    articles = db.filter_by_category(category)
    print(article_list_template(articles, f"Category: {category}"))


# DISPATCHER

def run_portal():

    db.create(
        headline="Portal Launch",
        content="Today a new news portal was launched.",
        author="Admin",
        category="Technology"
    )

    db.create(
        headline="Sports Victory",
        content="The team won an important final match.",
        author="John",
        category="Sports"
    )

    while True:
        index_view()

        choice = input("Choose action: ").strip()

        if choice == "1":
            list_articles_view()
            input("\nPress Enter to continue...")

        elif choice == "2":
            breaking_news_view()
            input("\nPress Enter to continue...")

        elif choice == "3":
            headline = input("Headline: ")
            content = input("Content: ")
            author = input("Author: ")
            category = input("Category: ")

            create_article_view({
                "headline": headline,
                "content": content,
                "author": author,
                "category": category
            })

            input("\nPress Enter to continue...")

        elif choice == "4":
            list_articles_view()

            try:
                index = int(input("Article number: "))
                article_detail_view(index)
            except ValueError:
                print("Please enter a valid number.")

            input("\nPress Enter to continue...")

        elif choice == "5":
            category = input("Enter category: ")
            category_view(category)
            input("\nPress Enter to continue...")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    run_portal()