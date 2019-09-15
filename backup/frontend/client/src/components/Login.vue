<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <router-link to="/">index</router-link>
        <!--<router-link to="/">
          <span v-on:click="doSomethingCool">Home</span>
        </router-link>-->
      </div>
    </div>
    <b-form @submit="onSubmitLogin" class="w-100">
      <b-form-group id="form-login-username-group"
        label="Usuário:"
        label-for="form-login-username-input">
        <b-form-input
          id="form-login-username-input"
          type="text"
          v-model="addLoginForm.username"
          required
          placeholder="Insira seu nome de usuário"
        ></b-form-input>
      </b-form-group>
      <b-form-group id="form-login-password-group"
        label="Senha:"
        label-for="form-login-password-input">
        <b-form-input
          id="form-login-password-input"
          type="password"
          v-model="addLoginForm.password"
          required
          placeholder="Insira sua senha"
        ></b-form-input>
      </b-form-group>
      <b-button-group>
        <b-button type="submit" variant="primary">Entrar</b-button>
        <b-button
          type="button"
          variant="success"
          v-b-modal.register-modal>Registrar</b-button>
      </b-button-group>
    </b-form>
    <b-modal ref="registerModal" id="register-modal" title="Cadastro" hide-footer>
      <b-form @submit="onSubmitNewUser" @reset="onReset" class="w-100">
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
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      message: '',
      showMessage: false,
      addUserForm: {
        name: '',
        username: '',
        password: '',
        repassword: '',
        email: '',
        birthdate: '',
        gender: '',
      },
      addLoginForm: {
        username: '',
        password: '',
      },
    };
  },
  methods: {
    addUser(payload) {
      const path = 'http://localhost:5000/create_user';
      axios.post(path, payload)
        .then(() => {
          this.message = 'Sucesso!';
          this.showMessage = true;
        })
        .catch((error) => {
          this.message = 'Usuario ja existe!';
          this.showMessage = true;
          // eslint-disable-next-line
          console.error(error);
        });
    },
    loginUser(payload) {
      const path = 'http://localhost:5000/login';
      axios.post(path, payload)
        .then(() => {
          this.message = 'Sucesso!';
          this.showMessage = true;
          // eslint-disable-next-line
          console.log('Sucesso!');
        })
        .catch((error) => {
          this.message = 'Usuario ja existe!';
          this.showMessage = true;
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onSubmitNewUser(evt) {
      evt.preventDefault();
      this.$refs.registerModal.hide();
      const payload = {
        name: this.addUserForm.name,
        username: this.addUserForm.username,
        password: this.addUserForm.password,
        gender: this.addUserForm.gender,
        email: this.addUserForm.email,
        birthdate: this.addUserForm.birthdate,
      };
      this.addUser(payload);
      this.initForm();
    },
    onSubmitLogin(evt) {
      evt.preventDefault();
      const payload = {
        username: this.addLoginForm.username,
        password: this.addLoginForm.password,
      };
      this.loginUser(payload);
    },
    initForm() {
      this.addUserForm.name = '';
      this.addUserForm.username = '';
      this.addUserForm.password = '';
      this.addUserForm.repassword = '';
      this.addUserForm.gender = '';
      this.addUserForm.email = '';
      this.addUserForm.birthdate = '';
    },
    onReset(evt) {
      evt.preventDefault();
      this.initForm();
    },
  },
};
</script>
