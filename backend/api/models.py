from django.db import models

class Author(models.Model): # an author could have many books
    name = models.CharField(max_length=100)
    birthdate = models.DateField()

    def __str__(self):
        return self.name
    
class Book(models.Model): # a book can have more than one author
    title = models.CharField(max_length=100)
    blurb = models.TextField()
    isFiction= models.BooleanField(default=False)

    def __str__(self):
        return self.title

class AuthorBook(models.Model): # through model with extra field for contribution 
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contribution = models.IntegerField() # percentage of what they contributed

    def __str__(self):
        return f"{self.author.name} - {self.book.title}"
    