<template>
  <div class="container">
    <router-link to="/">index</router-link>
    <b-form-file
      v-model="file"
      :state="Boolean(file)"
      placeholder="Choose a file or drop it here..."
      drop-placeholder="Drop file here...">
    </b-form-file>
    <div class="mt-3">Selected file: {{ file ? file.name : '' }}</div>
    <b-button type="submit" variant="primary" v-on:click=submitFile()>Enviar</b-button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      file: '',
    };
  },
  methods: {
    submitFile() {
      const formData = new FormData();
      formData.append('file', this.file);
      axios.post('http://localhost:5000/insert_card_names', formData,
        { headers: { 'Content-Type': 'multipart/form-data' } });
    },
  },
};
</script>
