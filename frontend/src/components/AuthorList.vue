<template>
    <div>
      <h3>Authors</h3>
      <ul class="list-group">
        <li v-for="author in authors" :key="author.id" class="list-group-item d-flex justify-content-between align-items-center">
          {{ author.name }} - {{ author.birthdate }}
          <div>
            <button @click="editAuthor(author)" class="btn btn-primary btn-sm">Edit</button>
            <button @click="deleteAuthor(author.id)" class="btn btn-danger btn-sm">Delete</button>
          </div>
        </li>
      </ul>
      <button @click="showAddModal = true" class="btn btn-success mt-3">Add Author</button>
  
      <!-- Add/Edit Author Modal -->
      <div v-if="showAddModal || showEditModal" class="modal show" tabindex="-1" style="display: block;">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">{{ showEditModal ? 'Edit Author' : 'Add Author' }}</h5>
              <button type="button" class="btn-close" @click="closeModal"></button>
            </div>
            <div class="modal-body">
              <input v-model="authorForm.name" type="text" class="form-control" placeholder="Author Name" />
              <input v-model="authorForm.birthdate" type="date" class="form-control mt-2" placeholder="Birthdate" />
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">Close</button>
              <button type="button" class="btn btn-primary" @click="submitForm">{{ showEditModal ? 'Update' : 'Add' }}</button>
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
        authors: [],
        showAddModal: false,
        showEditModal: false,
        authorForm: {
          id: null,
          name: '',
          birthdate: '',
        },
      };
    },
    methods: {
      fetchAuthors() {
        fetch('/api/authors/')
          .then(response => response.json())
          .then(data => {
            this.authors = data;
          });
      },
      submitForm() {
        if (this.showEditModal) {
          this.updateAuthor();
        } else {
          this.addAuthor();
        }
      },
      addAuthor() {
        fetch('/api/authors/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.authorForm)
        })
          .then((response) => response.json())
          .then((data) => {
            this.authors.push(data);
            this.closeModal();
          });
      },
      editAuthor(author) {
        this.showEditModal = true;
        this.authorForm = { ...author };
      },
      updateAuthor() {
        fetch(`/api/authors/${this.authorForm.id}/`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.authorForm)
        })
          .then((response) => response.json())
          .then((data) => {
            const index = this.authors.findIndex(a => a.id === data.id);
            this.authors[index] = data;
            this.closeModal();
          });
      },
      deleteAuthor(id) {
        fetch(`/api/authors/${id}/`, { method: 'DELETE' }).then(() => {
          this.authors = this.authors.filter((author) => author.id !== id);
        });
      },
      closeModal() {
        this.showAddModal = false;
        this.showEditModal = false;
        this.authorForm = { id: null, name: '', birthdate: '' };
      },
    },
    mounted() {
      this.fetchAuthors();
    },
  };
  </script>
  