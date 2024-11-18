"""
from django.shortcuts import render
from django.http import JsonResponse


def test_api_view(request):
    return JsonResponse({
        'message': 'Good response!'
    })

"""

import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Author, Book, AuthorBook

@csrf_exempt
def author_view(request, author_id=None):
    """Handle operations related to authors, including retrieving, 
    creating, updating, and deleting authors."""
    if request.method == 'GET':
        if author_id:
            author = get_object_or_404(Author, id=author_id)
            response_data = {
                'id': author.id,
                'name': author.name,
                'birthdate': author.birthdate,
            }
        else:
            authors = Author.objects.all()
            response_data = [
                {'id': author.id, 'name': author.name, 'birthdate': author.birthdate,}
                for author in authors
            ]
        return JsonResponse(response_data, safe=False)

    elif request.method == 'POST':
        try:
            # Parse the JSON payload
            data = json.loads(request.body)

            # Create the author object
            author = Author.objects.create(
                name=data.get('name'),
                birthdate=data.get('birthdate')  # Ensure valid format from frontend
            )

            # Return the newly created author object
            return JsonResponse({
                'id': author.id,
                'name': author.name,
                'birthdate': author.birthdate,
            }, status=201)

        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            # Handle JSON, missing keys, or invalid data types
            return HttpResponseBadRequest("Invalid data format")


    elif request.method == 'PUT' and author_id:
        try:
            data = json.loads(request.body)
            author = get_object_or_404(Author, id=author_id)
            author.name = data.get('name', author.name)
            author.birthdate = data.get('birthdate', author.birthdate)
            author.save()
            return JsonResponse({'id': author.id, 'name': author.name, 'birthdate': author.birthdate})
        except (json.JSONDecodeError, KeyError, TypeError):
            return HttpResponseBadRequest("Invalid data format")

    elif request.method == 'DELETE' and author_id:
        author = get_object_or_404(Author, id=author_id)
        author.delete()
        return JsonResponse({'message': 'Author deleted'}, status=204)

    else:
        return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'DELETE'])


@csrf_exempt
def book_view(request, book_id=None):
    """Handle operations related to books, including retrieving,
    creating, updating, and deleting books."""
    if request.method == 'GET':
        if book_id:
            book = get_object_or_404(Book, id=book_id)
            response_data = {
                'id': book.id,
                'title': book.title,
                'blurb': book.blurb,
                'is_fiction': book.is_fiction
            }
        else:
            books = Book.objects.all()
            response_data = [
                {'id': book.id, 'title': book.title, 'blurb': book.blurb, 'is_fiction': book.is_fiction}
                for book in books
            ]
        return JsonResponse(response_data, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            book = Book.objects.create(
                title=data.get('title'),
                blurb=data.get('blurb'),
                is_fiction=data.get('is_fiction', False)
            )
            return JsonResponse({'id': book.id, 'title': book.title, 'blurb': book.blurb, 'is_fiction': book.is_fiction}, status=201)
        except (json.JSONDecodeError, KeyError, TypeError):
            return HttpResponseBadRequest("Invalid data format")

    elif request.method == 'PUT' and book_id:
        try:
            data = json.loads(request.body)
            book = get_object_or_404(Book, id=book_id)
            book.title = data.get('title', book.title)
            book.blurb = data.get('blurb', book.blurb)
            book.is_fiction = data.get('is_fiction', book.is_fiction)
            book.save()
            return JsonResponse({'id': book.id, 'title': book.title, 'blurb': book.blurb, 'is_fiction': book.is_fiction})
        except (json.JSONDecodeError, KeyError, TypeError):
            return HttpResponseBadRequest("Invalid data format")

    elif request.method == 'DELETE' and book_id:
        book = get_object_or_404(Book, id=book_id)
        book.delete()
        return JsonResponse({'message': 'Book deleted'}, status=204)

    else:
        return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'DELETE'])


@csrf_exempt
def author_book_view(request, relationship_id=None):
    """Handle operations related to the relationship between authors and books."""
    if request.method == 'GET':
        # Retrieve all author-book relationships
        relationships = AuthorBook.objects.all()
        response_data = [
            {
                'id': rel.id,
                'author': rel.author.name,
                'book': rel.book.title,
                'contribution': rel.contribution
            }
            for rel in relationships
        ]
        return JsonResponse(response_data, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            author = get_object_or_404(Author, id=data.get('author_id'))
            book = get_object_or_404(Book, id=data.get('book_id'))
            contribution = data.get('contribution')

            author_book = AuthorBook.objects.create(
                author=author,
                book=book,
                contribution=contribution
            )
            response_data = {
                'id': author_book.id,
                'author': author_book.author.name,
                'book': author_book.book.title,
                'contribution': author_book.contribution
            }
            return JsonResponse(response_data, status=201)
        except (json.JSONDecodeError, KeyError, TypeError):
            return HttpResponseBadRequest("Invalid data format")

    elif request.method == 'PUT' and relationship_id:
        try:
            data = json.loads(request.body)
            relationship = get_object_or_404(AuthorBook, id=relationship_id)
            
            # Retrieve new author and book if provided
            author = get_object_or_404(Author, id=data.get('author_id')) if 'author_id' in data else relationship.author
            book = get_object_or_404(Book, id=data.get('book_id')) if 'book_id' in data else relationship.book
            contribution = data.get('contribution', relationship.contribution)

            # Update the relationship
            relationship.author = author
            relationship.book = book
            relationship.contribution = contribution
            relationship.save()

            response_data = {
                'id': relationship.id,
                'author': relationship.author.name,
                'book': relationship.book.title,
                'contribution': relationship.contribution
            }
            return JsonResponse(response_data, status=200)
        except (json.JSONDecodeError, KeyError, TypeError):
            return HttpResponseBadRequest("Invalid data format")

    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            author = get_object_or_404(Author, id=data.get('author_id'))
            book = get_object_or_404(Book, id=data.get('book_id'))

            author_book = get_object_or_404(AuthorBook, author=author, book=book)
            author_book.delete()
            return JsonResponse({'message': 'Author-Book relation deleted'}, status=204)
        except (json.JSONDecodeError, KeyError, TypeError):
            return HttpResponseBadRequest("Invalid data format")

    else:
        return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'DELETE'])
