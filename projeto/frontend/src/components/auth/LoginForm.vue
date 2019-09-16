<template>
  <div class="container">
    <div class="row">
    </div>
    <b-form @submit="onSubmitLogin" class="w-100">
      <div class="alert alert-danger" role="alert" v-if="warningAlert">
        {{ message }}
      </div>
      <div class="alert alert-success" role="alert" v-if="successfulAlert">
        {{ message }}
      </div>
      <div class="alert alert-danger" role="alert" v-if="status">
        {{ status }}
      </div>
      <b-form-group id="form-login-username-group"
        label="Usuário:"
        label-for="form-login-username-input">
        <b-form-input
          id="form-login-username-input"
          type="text"
          v-model="loginForm.username"
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
          v-model="loginForm.password"
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
            type="email"
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
            type="date"
            v-model="addUserForm.birthdate"
            required
            placeholder="Insira sua data de nascimento"
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
import { mapGetters } from 'vuex'

export default {
  data() {
    return {
      message: '',
      successfulAlert: false,
      warningAlert: false,
      addUserForm: {
        name: '',
        username: '',
        password: '',
        repassword: '',
        email: '',
        birthdate: '',
      },
      loginForm: {
        username: '',
        password: '',
      },
    };
  },
  computed: {
		...mapGetters('auth', {
      status: 'getStatus'
    })
  },
  destroyed() {
    this.$store.dispatch('auth/cleanStatus');
    this.resetAlert();
  },
  methods: {
    onSubmitLogin() {
      this.resetAlert();
      let formData = {
        username: this.loginForm.username,
        password: this.loginForm.password,
      }
      this.$store.dispatch('auth/login', formData);
    },
    addUser(payload) {
      this.resetAlert();
      const path = 'http://localhost:5000/create_user';
      axios.post(path, payload)
        .then((response) => {
          if (response.data.status == '0') { 
            this.message = 'Cadastro realizado com sucesso!'
            this.successfulAlert = true;
          } else if (response.data.status == '2') {
            this.message = 'Nome de usuário indisponível.'
            this.warningAlert = true;
          } else if (response.data.status == '3') {
            this.message = 'E-mail já cadastrado.'
            this.warningAlert = true;
          } else {
            this.message = 'Houve um problema, tente mais tarde.';
            this.warningAlert = true;
          }
        })
        .catch((error) => {
          this.message = 'Houve um problema, tente mais tarde.';
          this.warningAlert = true;
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
        email: this.addUserForm.email,
        birthdate: this.addUserForm.birthdate,
      };
      this.addUser(payload);
      this.initForm();
    },
    initForm() {
      this.addUserForm.name = '';
      this.addUserForm.username = '';
      this.addUserForm.password = '';
      this.addUserForm.repassword = '';
      this.addUserForm.email = '';
      this.addUserForm.birthdate = '';
    },
    onReset(evt) {
      evt.preventDefault();
      this.initForm();
    },
    resetAlert() {
      this.message = '';
      this.successfulAlert = false;
      this.warningAlert = false;
    },
  },
};
</script>