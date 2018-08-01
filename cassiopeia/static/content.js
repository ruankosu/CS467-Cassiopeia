var baseUrl = 'http://127.0.0.1:8000'
const EventBus = new Vue();

Vue.component('article-paginator', {
  props: ['settings'],
  methods: {
    next: function() {
      console.log("Emitting!")
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
        <li v-on:click="next" class="nav-item">
          <a class="nav-link" href="#">Next</a>
        </li>
      </ul>
    </div>
  `
});

// Vue Components and functions, API call with Axios
new Vue({
  el: '#app-content',
  data () {
    return {
      info: null,
      loading: true,
      last_id: null,
      errored: false,
      first_page: false,
      page_number: 0
      // groceryList: null
    }
  },
  methods: {
    nextPage: function() {
      this.loading = true;
      this.page_number += 1;
      axios
      .get(baseUrl + '/api/article?language=eng&page=' + this.page_number + '&dir=next&last_id=' + this.last_id, {withCredentials: true})
      .then(response => {
        this.info = response.data.contents;
        this.last_id = response.data.last_id;
        this.first_page = false;
      })
      .catch(error => {
        this.errored = true;
      })
      .finally(() => this.loading = false);
    },
    prevPage: function() {
      this.loading = true;
      this.page_number -= 1;
      if (this.page_number === 1) 
        this.first_page = true
      axios
      .get(baseUrl + '/api/article?language=eng&page=' + this.page_number + '&dir=prev&last_id=' + this.last_id, {withCredentials: true})
      .then(response => {
        this.info = response.data.contents;
        this.last_id = response.data.last_id;
      })
      .catch(error => {
        this.errored = true;
      })
      .finally(() => this.loading = false);    }
  },
  filters: {
    // currencydecimal (value) {
    //   return value.toFixed(2);
    // }
  },
  mounted () {
    axios
      .get(baseUrl + '/api/article?language=eng&page=1', {withCredentials: true})
      .then(response => {
        this.info = response.data.contents;
        this.last_id = response.data.last_id;
        this.page_number = 1;
        this.first_page = true;
      })
      .catch(error => {
        this.errored = true;
      })
      .finally(() => this.loading = false);

    // Handle emitters
    this.$root.$on('next', this.nextPage);
    this.$root.$on('prev', this.prevPage);
  }
});
  

