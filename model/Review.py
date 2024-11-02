class Review:
    def __init__(self, index, title, content, star_rating):
        self.index = index
        self.title = title
        self.content = content
        self.star_rating = star_rating

    def display_review(self):
        """Displays the review details in a formatted way."""
        print(f"Review Index: {self.index}")
        print(f"Title: {self.title}")
        print(f"Content: {self.content}")
        print(f"Star Rating: {self.star_rating} / 5")

    def __str__(self):
        """Provides a string representation of the review."""
        return f"Review {self.index}: {self.title} - {self.star_rating} Stars"

