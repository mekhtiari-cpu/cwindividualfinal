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
        <div>
          <button @click="editRelation(relation)" class="btn btn-primary btn-sm">Edit</button>
          <button @click="deleteRelation(relation.id)" class="btn btn-danger btn-sm">Remove</button>
        </div>
      </li>
    </ul>
    <button @click="showAddModal = true" class="btn btn-success mt-3">Add Relationship</button>

    <!-- Add/Edit Relationship Modal -->
    <div v-if="showAddModal || showEditModal" class="modal show" tabindex="-1" style="display: block;">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ showEditModal ? "Edit Relationship" : "Add Relationship" }}
            </h5>
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
            <button
              type="button"
              class="btn btn-primary"
              @click="submitForm"
            >
              {{ showEditModal ? "Update" : "Add" }}
            </button>
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
      showEditModal: false,
      relationshipForm: {
        id: null,
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
    submitForm() {
      if (this.showEditModal) {
        this.updateRelationship();
      } else {
        this.addRelationship();
      }
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
    editRelation(relation) {
      this.showEditModal = true;
      this.relationshipForm = {
        id: relation.id,
        author_id: this.authors.find((a) => a.name === relation.author)?.id || '',
        book_id: this.books.find((b) => b.title === relation.book)?.id || '',
        contribution: relation.contribution,
      };
    },
    updateRelationship() {
      fetch(`/api/author-book/${this.relationshipForm.id}/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          author_id: this.relationshipForm.author_id,
          book_id: this.relationshipForm.book_id,
          contribution: this.relationshipForm.contribution,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          const index = this.relationships.findIndex((rel) => rel.id === data.id);
          if (index !== -1) {
            this.relationships[index] = data; // Update the relationship in the list
          }
          this.closeModal();
        });
    },

    deleteRelation(id) {
      fetch(`/api/author-book/${id}/`, {
        method: 'DELETE',
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error('Failed to delete relationship');
          }
          this.relationships = this.relationships.filter((rel) => rel.id !== id);
        })
        .catch((error) => {
          console.error('Error deleting relationship:', error);
          alert('Failed to delete relationship.');
        });
    },

    closeModal() {
      this.showAddModal = false;
      this.showEditModal = false;
      this.relationshipForm = { id: null, author_id: '', book_id: '', contribution: '' };
    },
  },
  mounted() {
    this.fetchRelationships();
    this.fetchAuthorsAndBooks();
  },
};
</script>
