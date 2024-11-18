<template>
  <div>
    <h3>Books</h3>
    <ul class="list-group">
      
      <book-item
        v-for="book in books"
        :key="book.id"
        :book="book"
        @edit="editBook"
        @delete="deleteBook"
      ></book-item>
    </ul>
    <button @click="showAddModal = true" class="btn btn-success mt-3">Add Book</button>

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
      books: [], 
      showAddModal: false, 
      showEditModal: false,
      bookForm: {
        id: null,
        title: '',
        blurb: '',
        is_fiction: false,
      },
    };
  },
  methods: {
    fetchBooks() {
      fetch('/api/books/')
        .then((response) => response.json())
        .then((data) => {
          this.books = data; 
        })
        .catch((error) => {
          console.error("Failed to fetch books:", error);
        });
    },
    
    submitForm(form) {
      if (this.showEditModal) {
        this.updateBook(form);
      } else {
        this.addBook(form);
      }
    },
    
    addBook(form) {
      fetch('/api/books/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form), 
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to add book");
          }
          return response.json();
        })
        .then((data) => {
          this.books.push(data); 
          this.closeModal(); 
        })
        .catch((error) => {
          console.error("Error adding book:", error);
          alert("An error occurred while adding the book.");
        });
    },
   
    editBook(book) {
      this.showEditModal = true;
      this.bookForm = { ...book }; 
    },
    
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
            this.books[index] = data; 
          }
          this.closeModal(); 
        })
        .catch((error) => {
          console.error("Error updating book:", error);
          alert("An error occurred while updating the book.");
        });
    },
    
    deleteBook(id) {
      fetch(`/api/books/${id}/`, { method: 'DELETE' })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to delete book");
          }
          this.books = this.books.filter((book) => book.id !== id); 
        })
        .catch((error) => {
          console.error("Error deleting book:", error);
          alert("An error occurred while deleting the book.");
        });
    },
    
    closeModal() {
      this.showAddModal = false;
      this.showEditModal = false;
      this.bookForm = { id: null, title: '', blurb: '', is_fiction: false }; 
    },
  },
  mounted() {
    this.fetchBooks(); 
  },
};
</script>

  