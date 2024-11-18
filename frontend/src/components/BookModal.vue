<template>
    <div class="modal show" tabindex="-1" style="display: block;">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEdit ? "Edit Book" : "Add Book" }}</h5>
            <button type="button" class="btn-close" @click="$emit('close')"></button>
          </div>
          <div class="modal-body">
            <input v-model="form.title" type="text" class="form-control" placeholder="Book Title" />
            <textarea v-model="form.blurb" class="form-control mt-2" placeholder="Blurb"></textarea>
            <div class="form-check mt-2">
              <input type="checkbox" class="form-check-input" v-model="form.is_fiction" />
              <label class="form-check-label">Fiction</label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="$emit('close')">Close</button>
            <button type="button" class="btn btn-primary" @click="submitForm">Submit</button>
          </div>
        </div>
      </div>
    </div>
</template>
  
<script>
  export default {
    props: {
      isEdit: {
        type: Boolean,
        required: true,
      },
      initialForm: {
        type: Object,
        required: true,
      },
    },
    emits: ['close', 'submit'],
    data() {
      return {
        form: { ...this.initialForm },
      };
    },
    methods: {
      submitForm() {
        this.$emit('submit', this.form); // Emits the form data to the parent
      },
    },
  };
</script>
  