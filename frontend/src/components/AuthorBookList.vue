<template>
    <div>
      <h3>Author-Book Relationships</h3>
      <ul class="list-group">
        <li
          v-for="relation in relationships"
          :key="relation.id"
          class="list-group-item d-flex justify-content-between align-items-center"
        >
          {{ relation.author }} - {{ relation.book }} ({{ relation.contribution }}%)
          <button @click="deleteRelation(relation.id)" class="btn btn-danger btn-sm">Remove</button>
        </li>
      </ul>
      <button @click="showAddModal = true" class="btn btn-success mt-3">Add Relationship</button>
  
      <!-- Add Relationship Modal -->
      <div v-if="showAddModal" class="modal show" tabindex="-1" style="display: block;">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Add Relationship</h5>
              <button type="button" class="btn-close" @click="closeModal"></button>
            </div>
            <div class="modal-body">
              <select v-model="relationshipForm.author_id" class="form-select">
                <option disabled value="">Select Author</option>
                <option v-for="author in authors" :key="author.id" :value="author.id">
                  {{ author.name }}
                </option>
              </select>
              <select v-model="relationshipForm.book_id" class="form-select mt-2">
                <option disabled value="">Select Book</option>
                <option v-for="book in books" :key="book.id" :value="book.id">
                  {{ book.title }}
                </option>
              </select>
              <input
                v-model="relationshipForm.contribution"
                type="number"
                class="form-control mt-2"
                placeholder="Contribution (%)"
              />
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">Close</button>
              <button type="button" class="btn btn-primary" @click="addRelationship">Add</button>
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
        relationships: [],
        authors: [],
        books: [],
        showAddModal: false,
        relationshipForm: {
          author_id: '',
          book_id: '',
          contribution: '',
        },
      };
    },
    methods: {
      fetchRelationships() {
        fetch('/api/author-book/')
          .then((response) => response.json())
          .then((data) => {
            this.relationships = data;
          });
      },
      fetchAuthorsAndBooks() {
        fetch('/api/authors/')
          .then((response) => response.json())
          .then((data) => {
            this.authors = data;
          });
        fetch('/api/books/')
          .then((response) => response.json())
          .then((data) => {
            this.books = data;
          });
      },
      addRelationship() {
        fetch('/api/author-book/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.relationshipForm),
        })
          .then((response) => response.json())
          .then((data) => {
            this.relationships.push(data);
            this.closeModal();
          });
      },
      deleteRelation(id) {
        fetch(`/api/author-book/${id}/`, { method: 'DELETE' }).then(() => {
          this.relationships = this.relationships.filter((rel) => rel.id !== id);
        });
      },
      closeModal() {
        this.showAddModal = false;
        this.relationshipForm = { author_id: '', book_id: '', contribution: '' };
      },
    },
    mounted() {
      this.fetchRelationships();
      this.fetchAuthorsAndBooks();
    },
  };
  </script>
  