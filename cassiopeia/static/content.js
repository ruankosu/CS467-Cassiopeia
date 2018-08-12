var baseUrl = 'http://127.0.0.1:8000'
const EventBus = new Vue();

Vue.component('modal', {
  template: `
    <transition name="modal">
      <div class="modal-mask">
        <div class="modal-wrapper">
          <div class="modal-container">

            <div class="modal-header">
              <slot name="header">
                default header
              </slot>
              <button type="button" class="close" @click="$emit('close')" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>

            <div class="modal-body">
              <slot name="body">
                default body
              </slot>
            </div>

            <div class="modal-footer">
              <slot name="footer">
                <button type="button" class="btn btn-secondary" @click="$emit('close')">Close</button>
              </slot>
            </div>
          </div>
        </div>
      </div>
    </transition>
  `
})

Vue.component('content-sidebar', {
  props: ['settings'],
  methods: {
    languageSelected: function(value) {
      this.$root.$emit('languageSelected', value);
    },
    categorySelected: function(value) {
      this.$root.$emit('categorySelected', value);
    },
    historySelected: function() {
      this.$root.$emit('historySelected');
    }
  },
  template: `
    <!-- Sidebar  -->
    <nav id="sidebar">
        <ul class="list-unstyled components">
            <p>{{ settings.user_info.username }}</p>
            <li class="active">
                <a href="#categorySubmenu" data-toggle="collapse" aria-expanded="false" aria-controls="categorySubmenu" class="dropdown-toggle">Categories</a>
                <ul class="collapse list-unstyled" id="categorySubmenu">
                  <li v-for="category in settings.user_categories" :key="category.name" v-on:click="categorySelected(category.name)">
                    <a href="#">{{ category.name }}</a>
                  </li>
                </ul>
            </li>
            <li>
                <a href="#languageSubmenu" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle">Languages</a>
                <ul class="collapse list-unstyled" id="languageSubmenu">
                  <li v-for="language in settings.user_languages" :key="language.iso" v-on:click="languageSelected(language.iso)">
                    <a href="#">{{ language.language_name }} - {{ language.skill }}</a>
                  </li>
                </ul>
            </li>
            <li>
                <a href="#" v-on:click="historySelected()">History</a>
            </li>
            <li>
                <a href="#">Settings</a>
            </li>
        </ul>
    </nav>
  `
});

Vue.component('article-paginator', {
  props: ['settings'],
  methods: {
    next: function() {
      this.$root.$emit('next');
    },
    prev: function(event) {
      this.$root.$emit('prev');
    }
  },
  template: `
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="nav navbar-nav ml-auto">
        <li v-if="settings.first_page !== true" v-on:click="prev" class="nav-item">
          <a class="nav-link" href="#">Prev</a>
        </li>
        <li v-if="settings.last_page !== true" v-on:click="next" class="nav-item">
          <a class="nav-link" href="#">Next</a>
        </li>
      </ul>
    </div>
  `
});

// Vue Components and functions, API call with Axios
new Vue({
  el: '#app',
  data () {
    return {
      info: null,
      loading: true,
      last_id_prev: null,
      last_id_next: null,
      errored: false,
      first_page: false,
      last_page: false,
      page_number: 0,
      showHistory: false,
      showModal: false,
      snackbarData: {
        showSnackbar: false,
        rating: null
      },
      // groceryList: null
      modalData: {
        url: "",
        name: "",
        body: ""
      },
      userData: {
        user_info: {username: null, email: null, language: null, category: null},
        user_categories: null,
        user_languages: null
      }
    }
  },
  methods: {
    articleRated: function(content_id, rating, event) {
      var score = 0;
      switch(rating) {
        case "easy":
          score = -1;
          break;
        case "hard":
          score = 1;
          break;
        case "same":
          score = 0
        default:
          score = 0;
          break;
      }
      axios
      .post(baseUrl + '/api/article/rate', {
        content_id: content_id,
        rating: score
      })
      .then(response => {
        this.snackbarData.showSnackbar = true;
      })
      .catch(error => {
        this.errored = true;
      })
      .finally(() => setTimeout(() => this.snackbarData.showSnackbar = false, 1500));
    },
    getHistory: function() {
      this.loading = true; 
      this.showHistory = false;
      axios
      .get(baseUrl + '/api/history', {withCredentials: true})
      .then(response => {
        this.history = response.data;
      })
      .catch(error => {
        this.errored = true;
      })
      .finally(() => { 
        this.loading = false;
        this.showHistory = true; 
      });
    },
    nextPage: function() {
      this.loading = true;
      this.page_number += 1;

      axios
      .get(baseUrl + '/api/article?language=' + this.userData.user_info.language + '&page=' + this.page_number + '&dir=next&last_id=' + this.last_id_next, {withCredentials: true})
      .then(response => {
        this.info = response.data.contents;
        this.last_id_prev = response.data.last_id_prev;
        this.last_id_next = response.data.last_id_next;

        this.first_page = false;
        if (response.data.last_page === true) 
          this.last_page = true;
      })
      .catch(error => {
        this.errored = true;
      })
      .finally(() => this.loading = false);
    },
    prevPage: function() {
      this.loading = true;
      this.page_number -= 1;
      this.last_page = false;
      if (this.page_number === 1) 
        this.first_page = true;
      
      axios
      .get(baseUrl + '/api/article?language=' + this.userData.user_info.language + '&page=' + this.page_number + '&dir=prev&last_id=' + this.last_id_prev, {withCredentials: true})
      .then(response => {
        this.info = response.data.contents;
        this.last_id_prev = response.data.last_id_prev;
        this.last_id_next = response.data.last_id_next;
      })
      .catch(error => {
        this.errored = true;
      })
      .finally(() => this.loading = false);    
    },
    languageSelect: function(iso) {
      this.loading = true;
      this.showHistory = false;

      this.userData.user_info.language = iso; // Set newly selected language
      axios
      .get(baseUrl + '/api/article?' + this.userData.user_info.language + '&page=1', {withCredentials: true})
      .then(response => {
        this.info = response.data.contents;
        this.last_id_prev = response.data.last_id_prev;
        this.last_id_next = response.data.last_id_next;
        this.page_number = 1;
        this.first_page = true;
      })
      .catch(error => {
        this.errored = true;
      })
      .finally(() => this.loading = false);
    },
    contentClicked: function(content) {
      this.modalData.url = content.url;
      this.modalData.name = content.name;
      this.modalData.body = content.body;
      this.showModal = true;
    }
  },
  filters: {
    // currencydecimal (value) {
    //   return value.toFixed(2);
    // }
  },
  mounted () {
    axios
      .get(baseUrl + '/api/article?page=1', {withCredentials: true})
      .then(response => {
        this.info = response.data.contents;
        this.last_id_prev = response.data.last_id_prev;
        this.last_id_next = response.data.last_id_next;
        this.page_number = 1;
        this.first_page = true;

        this.userData.user_categories = response.data.user_categories;
        this.userData.user_languages = response.data.user_languages;

        // Set user info
        this.userData.user_info.username = response.data.user_info.username;
        this.userData.user_info.email = response.data.user_info.email;    
        this.userData.user_info.language = response.data.user_info.language;      // Default language     
        this.userData.user_info.category = response.data.user_info.category;      // Default category
      })
      .catch(error => {
        this.errored = true;
      })
      .finally(() => this.loading = false);

    // Handle emitters
    this.$root.$on('next', this.nextPage);
    this.$root.$on('prev', this.prevPage);
    this.$root.$on('languageSelected', this.languageSelect);
    this.$root.$on('categorySelected', this.categorySelect);
    this.$root.$on('historySelected', this.getHistory);
  }
});
  

