from django.contrib import admin
from .models import Author, Book, AuthorBook

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(AuthorBook)