"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('authors/', views.author_view, name='authors'),
    path('authors/<int:author_id>/', views.author_view, name='author-detail'),
    path('books/', views.book_view, name='books'),
    path('books/<int:book_id>/', views.book_view, name='book-detail'),
    path('author-book/', views.author_book_view, name='author-book'),
    path('author-book/<int:relationship_id>/', views.author_book_view, name='author-book-detail'),
]
