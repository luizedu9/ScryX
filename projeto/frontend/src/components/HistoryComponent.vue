<template>
  <div class="container">

    <div role="tablist">
      <div v-for="i in lengthOptions" :key="i"> <!-- ACCORDION DE COTAÇÕES -->

        <b-card no-body class="mb-1">
          <b-card-header header-tag="header" class="p-0" role="tab">
            <b-button block v-b-toggle="'accordion-' + i" variant="primary"> {{ card_list[lengthOptions - i]['deck_name'].concat(' - ', card_list[lengthOptions - i]['date']) }} </b-button>
          </b-card-header>
          <b-collapse :id="'accordion-' + i" accordion="quote-accordion" role="tabpanel">
            <b-card-body>
              
              <div v-for="j in card_list[lengthOptions-i]['result'].length" :key="j"> <!-- ACCORDION DE OPÇÕES -->

                <b-card no-body class="mb-1">
                  <b-card-header header-tag="header" class="p-0" role="tab">
                    <b-button block v-b-toggle="'accordionOption-' + j" variant="success"> Opção {{ j }} </b-button>
                  </b-card-header>
                  <b-collapse :id="'accordionOption-' + j" accordion="option-accordion" role="tabpanel">
                    <b-card-body>

                      <table class="table table-sm table-striped"> <!--TABLE CABEÇALHO -->
                        <thead>
                          <tr class="table-warning">
                            <th>Valor Total:</th>
                            <th>{{ card_list[lengthOptions-i]['result'][j-1]['price'].toFixed(2) }}</th>
                            <th>Quantidade de lojas:</th>
                            <th>{{ Object.keys(card_list[lengthOptions-i]['result'][j-1]).length - 2 }}</th>
                          </tr>
                        </thead>
                      </table>

                      <div v-for="(store, key) in card_list[lengthOptions-i]['result'][j-1]" :key="store"> <!--TABLE LOJAS -->

                        <table class="table table-sm table-striped" v-if="key != 'missing_list' && key != 'price'"> <!--TABLE LOJAS -->
                          <thead>
                            <tr class="table-primary">
                              <th>Loja:</th>
                              <th>{{ key }}</th>
                              <th>Valor:</th>
                              <th>{{ store['price'].toFixed(2) }}</th>
                            </tr>
                          </thead>
                          <thead>
                            <tr>
                              <th>Nome</th>
                              <th>Quantidade</th>
                              <th>Preço Unitário</th>
                              <th>Preço</th>
                            </tr>
                          </thead>
                          <tbody>

                            <tr v-for="card in store['cards']" :key="card">
                              <td>{{ card.name }}</td>
                              <td>{{ card.quantity }}</td>
                              <td>{{ card.price.toFixed(2) }}</td>
                              <td v-if="typeof card.total_price == typeof 0">{{ card.total_price.toFixed(2) }}</td>
                              <td v-else></td>
                            </tr>

                          </tbody>
                        </table>
                        <table class="table table-sm table-striped" v-if="key == 'missing_list' && store.length > 0"> <!--TABLE DE CARTAS NÃO ENCONTRADAS -->
                          <thead>
                            <tr class="table-danger">
                              <th colspan="2">Cartas não encontradas:</th>
                            </tr>
                          </thead>
                          <thead>
                            <tr>
                              <th>Nome</th>
                              <th>Quantidade</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="card in store" :key="card">
                              <td>{{ card.name }}</td>
                              <td>{{ card.quantity }}</td>
                            </tr>
                          </tbody>
                        </table>
                      
                      </div>  

                    </b-card-body>
                    </b-collapse>
                </b-card>

              </div>

            </b-card-body>
            </b-collapse>
        </b-card>

      </div>
    </div>

  </div>
</template>

<script>
import axiosAuth from '@/api/axios-auth'

export default {
  data() {
    return {
      message: '',
      warningAlert: false,
      card_list: '',
      lengthOptions: '',
    };
  },
  created() {
    const path = `http://localhost:5000/history/${localStorage.getItem('username')}`;
    axiosAuth.get(path)
      .then((res) => {
        if (res.data.status == 0) {


          this.card_list = JSON.parse(res.data.history);
          this.lengthOptions = this.card_list.length


        } else {
          this.message = 'Houve um erro inesperado. Tente mais tarde';
          this.warningAlert = true;
        }
    })
  },
};
</script>
