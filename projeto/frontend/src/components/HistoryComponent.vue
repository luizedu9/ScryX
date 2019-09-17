<template>
  <div class="container">
    <div class="alert alert-danger" role="alert" v-if="warningAlert">
      {{ message }}
    </div>
    {{ card_list }}
  </div>
</template>

<script>
import axiosAuth from '@/api/axios-auth'

export default {
  data() {
    return {
      card_list: '',
      message: '',
      warningAlert: false,
    };
  },
  created() {
    const path = `http://localhost:5000/history/${localStorage.getItem('username')}`;
    axiosAuth.get(path)
      .then((res) => {
        if (res.data.status == 0) {
          this.card_list = res.data.history;
        } else {
          this.message = 'Houve um erro inesperado. Tente mais tarde';
          this.warningAlert = true;
        }
    })
  },
};
</script>
