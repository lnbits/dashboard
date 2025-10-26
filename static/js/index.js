window.app = Vue.createApp({
  el: '#vue',
  mixins: [windowMixin],
  delimiters: ['${', '}'],
  data: function () {
    return {
      icon: {
      show: false,
      options: [
          'home',
          'star',
          'bolt',
          'paid',
          'savings',
          'store',
          'videocam',
          'music_note',
          'flight',
          'train',
          'directions_car',
          'school',
          'construction',
          'science',
          'sports_esports',
          'sports_tennis',
          'theaters',
          'water',
          'headset_mic',
          'videogame_asset',
          'person',
          'group',
          'pets',
          'sunny',
          'elderly',
          'verified',
          'snooze',
          'mail',
          'forum',
          'shopping_cart',
          'shopping_bag',
          'attach_money',
          'print_connect',
          'dark_mode',
          'light_mode',
          'android',
          'network_wifi',
          'shield',
          'fitness_center',
          'lunch_dining'
        ]
      },
      currencyOptions: ['sat'],
      settingsFormDialog: {
        show: false,
        data: {}
      },

      ownerDataFormDialog: {
        show: false,
        data: {
          name: null,
          
        }
      },
      ownerDataList: [],
      ownerDataTable: {
        search: '',
        loading: false,
        columns: [
          {"name": "name", "align": "left", "label": "Name", "field": "name", "sortable": true},
          {"name": "updated_at", "align": "left", "label": "Updated At", "field": "updated_at", "sortable": true},
          {"name": "id", "align": "left", "label": "ID", "field": "id", "sortable": true},
          
        ],
        pagination: {
          sortBy: 'updated_at',
          rowsPerPage: 10,
          page: 1,
          descending: true,
          rowsNumber: 10
        }
      },

      clientDataFormDialog: {
        show: false,
        ownerData: {label: 'All Owner Data', value: ''},
        data: {}
      },
      clientDataList: [],
      clientDataTable: {
        search: '',
        loading: false,
        columns: [
          {"name": "name", "align": "left", "label": "Name", "field": "name", "sortable": true},
          {"name": "link", "align": "left", "label": "Link", "field": "link", "sortable": true},
          {"name": "icon", "align": "left", "label": "icon", "field": "icon", "sortable": true},
          {"name": "updated_at", "align": "left", "label": "Updated At", "field": "updated_at", "sortable": true},
          {"name": "id", "align": "left", "label": "ID", "field": "id", "sortable": true},
          
        ],
        pagination: {
          sortBy: 'updated_at',
          rowsPerPage: 10,
          page: 1,
          descending: true,
          rowsNumber: 10
        }
      }
    }
  },
  watch: {
    'ownerDataTable.search': {
      handler() {
        const props = {}
        if (this.ownerDataTable.search) {
          props['search'] = this.ownerDataTable.search
        }
        this.getOwnerData()
      }
    },
    'clientDataTable.search': {
      handler() {
        const props = {}
        if (this.clientDataTable.search) {
          props['search'] = this.clientDataTable.search
        }
        this.getClientData()
      }
    },
    'clientDataFormDialog.ownerData.value': {
      handler() {
        const props = {}
        if (this.clientDataTable.search) {
          props['search'] = this.clientDataTable.search
        }
        this.getClientData()
      }
    }
  },

  methods: {

    //////////////// Owner Data ////////////////////////
    async showNewOwnerDataForm() {
      this.ownerDataFormDialog.data = {
          name: null,
          
      }
      this.ownerDataFormDialog.show = true
    },
    async showEditOwnerDataForm(data) {
      this.ownerDataFormDialog.data = {...data}
      this.ownerDataFormDialog.show = true
    },
    async saveOwnerData() {
      
      try {
        const data = {extra: {}, ...this.ownerDataFormDialog.data}
        const method = data.id ? 'PUT' : 'POST'
        const entry = data.id ? `/${data.id}` : ''
        await LNbits.api.request(
          method,
          '/publicdash/api/v1/owner_data' + entry,
          null,
          data
        )
        this.getOwnerData()
        this.ownerDataFormDialog.show = false
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      }
    },

    async getOwnerData(props) {
      
      try {
        this.ownerDataTable.loading = true
        const params = LNbits.utils.prepareFilterQuery(
          this.ownerDataTable,
          props
        )
        const {data} = await LNbits.api.request(
          'GET',
          `/publicdash/api/v1/owner_data/paginated?${params}`,
          null
        )
        this.ownerDataList = data.data
        this.ownerDataTable.pagination.rowsNumber = data.total
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      } finally {
        this.ownerDataTable.loading = false
      }
    },
    async deleteOwnerData(ownerDataId) {
      await LNbits.utils
        .confirmDialog('Are you sure you want to delete this Owner Data?')
        .onOk(async () => {
          try {
            
            await LNbits.api.request(
              'DELETE',
              '/publicdash/api/v1/owner_data/' + ownerDataId,
              null
            )
            await this.getOwnerData()
          } catch (error) {
            LNbits.utils.notifyApiError(error)
          }
        })
    },
    async exportOwnerDataCSV() {
      await LNbits.utils.exportCSV(
        this.ownerDataTable.columns,
        this.ownerDataList,
        'owner_data_' + new Date().toISOString().slice(0, 10) + '.csv'
      )
    },

    //////////////// Client Data ////////////////////////
    async showNewItemForm() {
      this.clientDataFormDialog.data = {
          name: null,
          icon: null,
          link: null,
      }
      this.clientDataFormDialog.show = true
    },
    async showEditClientDataForm(data) {
      this.clientDataFormDialog.data = {...data}
      this.clientDataFormDialog.show = true
    },
    async saveClientData() {
      
      try {
        const data = {extra: {}, ...this.clientDataFormDialog.data}
        const method = data.id ? 'PUT' : 'POST'
        await LNbits.api.request(
          method,
          '/publicdash/api/v1/client_data',
          null,
          data
        )
        this.getClientData()
        this.clientDataFormDialog.show = false
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      }
    },

    async getClientData(props) {
      
      try {
        this.clientDataTable.loading = true
        let params = LNbits.utils.prepareFilterQuery(
          this.clientDataTable,
          props
        )
        const ownerDataId = this.clientDataFormDialog.ownerData.value
        if (ownerDataId) {
          params += `&owner_data_id=${ownerDataId}`
        }
        const {data} = await LNbits.api.request(
          'GET',
          `/publicdash/api/v1/client_data/paginated?${params}`,
          null
        )
        this.clientDataList = data.data
        this.clientDataTable.pagination.rowsNumber = data.total
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      } finally {
        this.clientDataTable.loading = false
      }
    },
    async deleteClientData(clientDataId) {
      await LNbits.utils
        .confirmDialog('Are you sure you want to delete this Client Data?')
        .onOk(async () => {
          try {
            
            await LNbits.api.request(
              'DELETE',
              '/publicdash/api/v1/client_data/' + clientDataId,
              null
            )
            await this.getClientData()
          } catch (error) {
            LNbits.utils.notifyApiError(error)
          }
        })
    },

    async exportClientDataCSV() {
      await LNbits.utils.exportCSV(
        this.clientDataTable.columns,
        this.clientDataList,
        'client_data_' + new Date().toISOString().slice(0, 10) + '.csv'
      )
    },

    //////////////// Utils ////////////////////////
    dateFromNow(date) {
      return moment(date).fromNow()
    },
    async fetchCurrencies() {
      try {
        const response = await LNbits.api.request('GET', '/api/v1/currencies')
        this.currencyOptions = ['sat', ...response.data]
      } catch (error) {
        LNbits.utils.notifyApiError(error)
      }
    }
  },
  ///////////////////////////////////////////////////
  //////LIFECYCLE FUNCTIONS RUNNING ON PAGE LOAD/////
  ///////////////////////////////////////////////////
  async created() {
    this.fetchCurrencies()
    this.getOwnerData()
    this.getClientData()

    
    
  }
})