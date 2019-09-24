<template>
  <div class="container">
    <div class="alert alert-danger" role="alert" v-if="warningAlert">
      {{ message }}
    </div>
    <div class="alert alert-success" role="alert" v-if="successfulAlert">
      {{ message }}
    </div>
    <div class="alert alert-warning" role="alert" v-if="infoAlert">
      {{ message }}
    </div>
    <div class="container" v-if="adminMode">
      <p> Submeter lista de nomes de cartas - MTGJson</p>
      <table class="table table-borderless">
        <tr>
          <td>
            <b-form-file
              v-model="file"
              :state="Boolean(file)"
              placeholder="Arraste o arquivo aqui..."
              drop-placeholder="Solte o arquivo aqui...">
            </b-form-file>
          </td>
          <td>
            <b-button type="submit" variant="primary" v-on:click=submitFile()>Enviar</b-button>
          </td>
        </tr>
      </table>
      <hr>
    </div>
    <div class="container">
      <font size="+3"> Perfil: </font>
      <table class="table table-borderless">
        <tr>
          <td>
            Nome: <br>
            {{ user.name }}
          </td>
          <td>
            Data de Cadastro: <br>
            {{ user.entrydate }}
          </td>
        </tr>
        <tr>
          <td>
            Usuário: <br>
            {{ user.username }}
          </td>
          <td>
            Data de Nascimento: <br>
            {{ user.birthdate }}
          </td>
        </tr>
        <tr>
          <td>
            E-mail: <br>
            {{ user.email}}
          </td>
          <td>
            <b-button type="submit" variant="primary" v-b-modal.password-modal>Alterar Senha</b-button>
          </td>
        </tr>
        <tr>
          <td>
            <b-button type="submit" variant="primary" v-b-modal.email-modal>Alterar E-mail</b-button>
          </td>
          <td>
            <b-button type="submit" variant="danger" v-b-modal.delete-modal>Apagar Conta</b-button>
          </td>
        </tr>
      </table>
    </div>

    <b-modal ref="passwordModal"
              id="password-modal"
              title="Alterar Senha"
              hide-footer>
      <div class="alert alert-danger" role="alert" v-if="passwordAlert">
        {{ message }}
      </div>
      <b-form-group id="form-title-edit-group"
                    label="Senha Atual:"
                    label-for="form-title-edit-input">
        <b-form-input type="password" v-model="user.password" placeholder="Digite sua senha atual"></b-form-input>
      </b-form-group>
      <b-form-group id="form-title-edit-group"
                    label="Nova Senha:"
                    label-for="form-title-edit-input">
        <b-form-input type="password" v-model="user.newPassword" placeholder="Digite a nova senha"></b-form-input>
      </b-form-group>
      <b-form-group id="form-title-edit-group"
                    label="Confirme Nova Senha:"
                    label-for="form-title-edit-input">
      <b-form-input type="password" v-model="user.rePassword" placeholder="Confirme a nova senha"></b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary" v-on:click=updatePassword()>Alterar</b-button>
    </b-modal>

    <b-modal ref="emailModal"
              id="email-modal"
              title="Alterar Email"
              hide-footer>
      <div class="alert alert-danger" role="alert" v-if="emailAlert">
        {{ message }}
      </div>
      <b-form-group id="form-email-group" label="Novo E-mail:" label-for="form-email-input">
        <b-form-input id="form-email-input" type="email" v-model="newEmail" placeholder="Digite o novo e-mail" required></b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary" v-on:click=updateEmail()>Alterar</b-button>
    </b-modal>

    <b-modal ref="deleteModal"
              id="delete-modal"
              title="Deletar Conta"
              hide-footer>
    <b-form-group id="form-title-edit-group"
                    label="NÃO SERÁ MAIS POSSIVEL RECUPERAR SUA CONTA.
                    TEM CERTEZA DISSO?"
                    label-for="form-title-edit-input">
        <b-button type="submit" variant="danger" v-on:click=deleteAccount()>DELETAR</b-button>
      </b-form-group>
      
    </b-modal>

  </div>
</template>

<script>
import axiosAuth from '@/api/axios-auth'

export default {
  data() {
    return {
      file: '',
      message: '',
      successfulAlert: false,
      warningAlert: false,
      infoAlert: false,
      emailAlert: false,
      passwordAlert: false,
      adminMode: false,
      newEmail: '',
      user: {
        name: '',
        username: '',
        password: '',
        rePassword: '',
        newPassword: '',
        email: '',
        birthdate: '',
        entrydate: '',
      },
    };
  },
  created() {
    this.getUser();
  },
  methods: {
    getUser() {
      const path = `http://localhost:5000/user/${localStorage.getItem('username')}`;
      axiosAuth.get(path)
        .then((res) => {
          this.user.name = res.data.name;
          this.user.username = res.data.username;
          this.user.email = res.data.email;
          this.user.birthdate = res.data.birthdate;
          this.user.entrydate = res.data.entrydate;
          if (res.data.admin == true) {
            this.adminMode = true;
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    submitFile() {
      this.resetAlert();
      this.message = 'Enviando...'
      this.infoAlert = true;
      const formData = new FormData();
      formData.append('file', this.file);
      axiosAuth.post('http://localhost:5000/insert_card_names', formData,
        { headers: { 'Content-Type': 'multipart/form-data' } })
        .then((res) => {
          if (res.data.status == 0) {
            this.infoAlert = false;
            this.message = 'Enviado com sucesso!';
            this.successfulAlert = true;
          } else if (res.data.status == 2) {
            this.infoAlert = false;
            this.message = 'Acesso negado!';
            this.warningAlert = true;
          } else {
            this.infoAlert = false;
            this.message = 'Houve um erro inesperado. Tente mais tarde';
            this.warningAlert = true;
          }
      })
    },
    deleteAccount() {
      this.resetAlert();
      const path = `http://localhost:5000/user/${localStorage.getItem('username')}`;
      axiosAuth.delete(path)
        .then((res) => {
          if (res.data.status == 0) {
            this.$store.dispatch('auth/logout');
          } else {
            this.message = 'Houve um erro inesperado. Tente mais tarde';
            this.warningAlert = true;
          }
      })
    },
    updateEmail() {
      this.resetAlert();
      const payload = {
          username: this.user.username,
          email: this.newEmail,
      }
      axiosAuth.put('http://localhost:5000/user/email', payload)
        .then((res) => {
          if (res.data.status == 0) {
            this.message = 'E-mail alterado com sucesso';
            this.successfulAlert = true;
            this.user.email = this.newEmail;
            this.newEmail = '';
            this.$refs.emailModal.hide();
          } else if (res.data.status == 2) {
            this.message = 'E-mail já está cadastrado';
            this.emailAlert = true;
          } else {
            this.message = 'Houve um erro inesperado. Tente mais tarde';
            this.warningAlert = true;
            this.$refs.emailModal.hide();
          }
      })
    },
    updatePassword() {
      this.resetAlert();
      if (this.user.newPassword != this.user.rePassword) {
        this.message = 'Senhas divergentes'
        this.passwordAlert = true;
      } else {
        const payload = {
            username: this.user.username,
            password: this.user.password,
            newPassword: this.user.newPassword,
        }
        axiosAuth.put('http://localhost:5000/user/password', payload)
          .then((res) => {
            if (res.data.status == 0) {
              this.message = 'Senha alterada com sucesso';
              this.successfulAlert = true;                  
              this.$refs.passwordModal.hide();
            } else if (res.data.status == 2) {
              this.message = 'Senha atual incorreta';
              this.passwordAlert = true;
            } else {
              this.message = 'Houve um erro inesperado. Tente mais tarde';
              this.warningAlert = true;
              this.$refs.emailModal.hide();
            }
        })
      }
    },
    resetAlert() {
      this.message = '';
      this.successfulAlert = false;
      this.warningAlert = false;
      this.infoAlert = false;
      this.emailAlert = false;
      this.passwordAlert = false;
    },
  },
};
</script>
