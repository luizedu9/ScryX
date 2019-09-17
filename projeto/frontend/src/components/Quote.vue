<template>
  <div class="container">
    <div class="alert alert-danger" role="alert" v-if="warningAlert">
      {{ message }}
      <div v-for="item in errorList" v-bind:key="item.id">
        {{ item }}
      </div>
    </div>
    <div class="alert alert-success" role="alert" v-if="successfulAlert">
      {{ message }}
    </div>
    <b-form-textarea
      id="textarea"
      v-model="card_list"
      placeholder="Ex: 4 Fog Bank"
      rows="15"
    ></b-form-textarea>
    <br>
    <b-button type="submit" variant="primary" v-on:click=submitList()>Enviar</b-button>
  </div>
</template>

<script>
import axiosAuth from '@/api/axios-auth'

export default {
  data() {
    return {
      card_list: '',
      message: '',
      errorList: [],
      successfulAlert: false,
      warningAlert: false,
    };
  },
  methods: {
    submitList() {
      this.successfulAlert = false;
      this.warningAlert = false;
      this.message = '';
      this.errorList = [];
      let payload = {
        'card_list': this.card_list,
        'username': localStorage.getItem('username')
      }
      axiosAuth.post('http://localhost:5000/request_list', payload)
        .then((res) => {
          if (res.data.status == 0) {
            this.message = 'Requisição em processamento. Isso pode demorar alguns minutos. O resultado será enviado para seu e-mail após concluido.';
            this.successfulAlert = true;
            this.card_list = '';
          } else if (res.data.status == 2) {
            this.message = 'Ocorreu um erro. Verifique as seguintes cartas: ';
            this.errorList = res.data.error_list;
            this.warningAlert = true;
          } else if (res.data.status == 3) {
            this.message = 'Ocorreu um erro. É esperado que a lista esteja no formato "Quantidade Carta".';
            this.warningAlert = true;
          } else {
            this.message = 'Ocorreu um erro inesperado. Tente mais tarde.';
            this.warningAlert = true;
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.message = 'Ocorreu um erro inesperado. Tente mais tarde.'
        });
    },
  },
};
</script>
