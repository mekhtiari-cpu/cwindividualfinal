from django.db import models

class Author(models.Model): # an author could have many books
    """Represents an author who can write multiple books."""
    name = models.CharField(max_length=100)
    birthdate = models.DateField()

    def __str__(self):
        """Returns the string representation of the author."""
        return self.name
    
class Book(models.Model): # a book can have more than one author
    """Represents a book, which can have multiple authors."""
    title = models.CharField(max_length=100)
    blurb = models.TextField()
    is_fiction= models.BooleanField(default=False)

    def __str__(self):
        """Returns the string representation of the book."""
        return self.title

class AuthorBook(models.Model): # through model with extra field for contribution 
    """Represents the relationship between authors and books, with an extra
    field for the percentage contribution of the author to the book."""
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contribution = models.IntegerField() # percentage of what they contributed

    def __str__(self):
        """Returns the string representation of the author-book relationship."""
        return f"{self.author.name} - {self.book.title}"
    