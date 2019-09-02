<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <button
          type="button"
          class="btn btn-success btn-sm"
          v-b-modal.register-modal>Registrar</button>
      </div>
    </div>
    <b-modal ref="registerModal" id="register-modal" title="Cadastro" hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-name-group" label="Nome:" label-for="form-name-input">
          <b-form-input
            id="form-name-input"
            type="text"
            v-model="addUserForm.name"
            required
            placeholder="Insira seu nome"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="form-email-group" label="E-mail:" label-for="form-email-input">
          <b-form-input
            id="form-email-input"
            type="text"
            v-model="addUserForm.email"
            required
            placeholder="Insira seu e-mail"
          ></b-form-input>
        </b-form-group>
        <b-form-group
          id="form-birthdate-group"
          label="Data de Nascimento:"
          label-for="form-birthdate-input">
          <b-form-input
            id="form-birthdate-input"
            type="text"
            v-model="addUserForm.birthdate"
            required
            placeholder="Insira sua data de nascimento"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="form-gender-group" label="Gênero:" label-for="form-gender-input">
          <b-form-input
            id="form-gender-input"
            type="text"
            v-model="addUserForm.gender"
            required
            placeholder="Insira seu gênero"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="form-username-group" label="Usuário:" label-for="form-username-input">
          <b-form-input
            id="form-username-input"
            type="text"
            v-model="addUserForm.username"
            required
            placeholder="Insira um nome de usuário"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="form-password-group" label="Senha:" label-for="form-password-input">
          <b-form-input
            id="form-password-input"
            type="password"
            v-model="addUserForm.password"
            required
            placeholder="Insira sua senha"
          ></b-form-input>
        </b-form-group>
        <b-form-group
          id="form-repassword-group"
          label="Confirme Senha:"
          label-for="form-repassword-input"
          ><b-form-input
            id="form-repassword-input"
            type="password"
            v-model="addUserForm.repassword"
            required
            placeholder="Confirme sua senha"
          ></b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Registrar</b-button>
          <b-button type="reset" variant="danger">Limpar</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <router-link to="/admin">admin</router-link>
  </div>
</template>

<script>
// import axios from 'axios';

export default {
  data() {
    return {
      addUserForm: {
        name: '',
        username: '',
        password: '',
        repassword: '',
        email: '',
        birthdate: '',
        gender: '',
      },
    };
  },
  methods: {
    initForm() {
      this.addUserForm.name = '';
      this.addUserForm.username = '';
      this.addUserForm.password = '';
      this.addUserForm.repassword = '';
      this.addUserForm.gender = '';
      this.addUserForm.email = '';
      this.addUserForm.birthdate = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.registerModal.hide();
      // if (this.addBookForm.read[0]) read = true;
      const payload = {
        title: this.addBookForm.title,
        author: this.addBookForm.author,
      };
      this.addBook(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.initForm();
    },
  },
};
</script>
