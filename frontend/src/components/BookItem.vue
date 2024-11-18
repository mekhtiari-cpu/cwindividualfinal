<template>
    <li class="list-group-item d-flex justify-content-between align-items-center">
      {{ book.title }} - {{ book.is_fiction ? "Fiction" : "Non-Fiction" }}
      <div>
        <button @click="$emit('edit', book)" class="btn btn-primary btn-sm">Edit</button>
        <button @click="$emit('delete', book.id)" class="btn btn-danger btn-sm">Delete</button>
      </div>
    </li>
</template>
  
<script>
    export default {
        props: {
            book: {
                type: Object,
                required: true,
            },
        },
    };
</script>
