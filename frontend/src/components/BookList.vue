<template>
  <div>
    <h3>Books</h3>
    <ul class="list-group">
      <!-- Loop through books and display them -->
      <book-item
        v-for="book in books"
        :key="book.id"
        :book="book"
        @edit="editBook"
        @delete="deleteBook"
      ></book-item>
    </ul>
    <button @click="showAddModal = true" class="btn btn-success mt-3">Add Book</button>

    <!-- Add/Edit Book Modal -->
    <book-modal
      v-if="showAddModal || showEditModal"
      :is-edit="showEditModal"
      :initial-form="bookForm"
      @close="closeModal"
      @submit="submitForm"
    ></book-modal>
  </div>
</template>

<script>
import BookItem from './BookItem.vue';
import BookModal from './BookModal.vue';

export default {
  components: { BookItem, BookModal },
  data() {
    return {
      books: [], // Holds the list of books
      showAddModal: false, // Controls the Add modal visibility
      showEditModal: false, // Controls the Edit modal visibility
      bookForm: {
        id: null,
        title: '',
        blurb: '',
        is_fiction: false,
      },
    };
  },
  methods: {
    // Fetch all books from the server
    fetchBooks() {
      fetch('/api/books/')
        .then((response) => response.json())
        .then((data) => {
          this.books = data; // Populate the books array with the fetched data
        })
        .catch((error) => {
          console.error("Failed to fetch books:", error);
        });
    },
    // Handle form submission for adding or updating a book
    submitForm(form) {
      if (this.showEditModal) {
        this.updateBook(form);
      } else {
        this.addBook(form);
      }
    },
    // Add a new book to the server
    addBook(form) {
      fetch('/api/books/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form), // Use the passed form object
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to add book");
          }
          return response.json();
        })
        .then((data) => {
          this.books.push(data); // Add the new book to the list
          this.closeModal(); // Close the modal
        })
        .catch((error) => {
          console.error("Error adding book:", error);
          alert("An error occurred while adding the book.");
        });
    },
    // Edit an existing book (populate the form with the book's data)
    editBook(book) {
      this.showEditModal = true;
      this.bookForm = { ...book }; // Clone the book data into the form
    },
    // Update an existing book on the server
    updateBook(form) {
      fetch(`/api/books/${form.id}/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to update book");
          }
          return response.json();
        })
        .then((data) => {
          const index = this.books.findIndex((b) => b.id === data.id);
          if (index !== -1) {
            this.books[index] = data; // Update the book in the list
          }
          this.closeModal(); // Close the modal
        })
        .catch((error) => {
          console.error("Error updating book:", error);
          alert("An error occurred while updating the book.");
        });
    },
    // Delete a book from the server
    deleteBook(id) {
      fetch(`/api/books/${id}/`, { method: 'DELETE' })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to delete book");
          }
          this.books = this.books.filter((book) => book.id !== id); // Remove the book from the list
        })
        .catch((error) => {
          console.error("Error deleting book:", error);
          alert("An error occurred while deleting the book.");
        });
    },
    // Close the Add/Edit modal and reset the form
    closeModal() {
      this.showAddModal = false;
      this.showEditModal = false;
      this.bookForm = { id: null, title: '', blurb: '', is_fiction: false }; // Reset the form
    },
  },
  mounted() {
    this.fetchBooks(); // Fetch books when the component is mounted
  },
};
</script>

  