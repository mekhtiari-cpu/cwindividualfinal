<template>
    <div>
      <h3>Books</h3>
      <ul class="list-group">
        <li
          v-for="book in books"
          :key="book.id"
          class="list-group-item d-flex justify-content-between align-items-center"
        >
          {{ book.title }} - {{ book.is_fiction ? "Fiction" : "Non-Fiction" }}
          <div>
            <button @click="editBook(book)" class="btn btn-primary btn-sm">Edit</button>
            <button @click="deleteBook(book.id)" class="btn btn-danger btn-sm">Delete</button>
          </div>
        </li>
      </ul>
      <button @click="showAddModal = true" class="btn btn-success mt-3">Add Book</button>
  
      <!-- Add/Edit Book Modal -->
      <div v-if="showAddModal || showEditModal" class="modal show" tabindex="-1" style="display: block;">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">{{ showEditModal ? "Edit Book" : "Add Book" }}</h5>
              <button type="button" class="btn-close" @click="closeModal"></button>
            </div>
            <div class="modal-body">
              <input v-model="bookForm.title" type="text" class="form-control" placeholder="Book Title" />
              <textarea v-model="bookForm.blurb" class="form-control mt-2" placeholder="Blurb"></textarea>
              <div class="form-check mt-2">
                <input type="checkbox" class="form-check-input" v-model="bookForm.is_fiction" />
                <label class="form-check-label">Fiction</label>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">Close</button>
              <button type="button" class="btn btn-primary" @click="submitForm">{{ showEditModal ? "Update" : "Add" }}</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
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
          });
      },
      submitForm() {
        if (this.showEditModal) {
          this.updateBook();
        } else {
          this.addBook();
        }
      },
      addBook() {
        fetch('/api/books/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.bookForm),
        })
          .then((response) => response.json())
          .then((data) => {
            this.books.push(data);
            this.closeModal();
          });
      },
      editBook(book) {
        this.showEditModal = true;
        this.bookForm = { ...book };
      },
      updateBook() {
        fetch(`/api/books/${this.bookForm.id}/`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.bookForm),
        })
          .then((response) => response.json())
          .then((data) => {
            const index = this.books.findIndex((b) => b.id === data.id);
            this.books[index] = data;
            this.closeModal();
          });
      },
      deleteBook(id) {
        fetch(`/api/books/${id}/`, { method: 'DELETE' }).then(() => {
          this.books = this.books.filter((book) => book.id !== id);
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
  