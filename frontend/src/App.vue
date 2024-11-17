<template>
    <div class="container pt-3">
      <div class="h1 text-center border rounded bg-light p-2 mb-3">
        Books and Authors
      </div>
  
      <ul class="nav nav-tabs mb-3">
        <li class="nav-item">
          <a class="nav-link" :class="{ active: selectedTab === 'authors' }" @click="selectedTab = 'authors'">Authors</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: selectedTab === 'books' }" @click="selectedTab = 'books'">Books</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: selectedTab === 'relationships' }" @click="selectedTab = 'relationships'">Author-Book Relationships</a>
        </li>
      </ul>
  
      <div v-if="selectedTab === 'authors'">
        <AuthorList />
      </div>
      <div v-if="selectedTab === 'books'">
        <BookList />
      </div>
      <div v-if="selectedTab === 'relationships'">
        <AuthorBookList />
      </div>
    </div>
  </template>
  
  <script>
  import AuthorList from './components/AuthorList.vue';
  import BookList from './components/BookList.vue';
  import AuthorBookList from './components/AuthorBookList.vue';
  
  export default {
    data() {
      return {
        selectedTab: 'authors',  // Default to the authors tab
      };
    },
    components: {
      AuthorList,
      BookList,
      AuthorBookList,
    },
  };
  </script>
  
  <style>
  /* Add any custom styles here if needed */
  </style>  