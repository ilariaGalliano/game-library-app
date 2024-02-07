<template>
  <div class="hello">
    <div class="container">
      <h1>{{ name }}</h1>
      <form action="/login" method="post" name="login-form">
        <div class="mb-3">
          <label for="name">Name: </label>
          <input type="text" id="name" v-model="input.name" />
        </div>
        <div class="mb-3">
          <label for="email">Email: </label>
          <input type="text" id="email" v-model="input.email" />
        </div>
        <div class="mb-3">
          <label for="password">Password: </label>
          <input type="password" id="password" v-model="input.password" />
        </div>
        <button
          class="btn btn-outline-dark"
          type="submit"
          v-on:click.prevent="login()"
        >
          Login
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Login",
  data() {
    return {
      input: {
        name: "",
        email: "",
        password: "",
      },
    };
  },
  methods: {
    // getStudents() {
    //   axios.get(this.path).then((response) => {
    //     console.log(response.data);
    //     this.students = response.data.students;
    //   });
    // },

    // saveStudent() {
    //   axios.post(this.path, this.student).then((response) => {
    //     console.log(response.data);
    //     this.student = {};
    //     this.getStudents();
    //   });
    // },
    getResponse() {
      // flask app url
      const path = "http://localhost:5000/login";
      axios
        .get(path)
        .then((res) => {
          console.log(res);
          this.name = res.name;
          this.email = res.email;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    login() {
      //make sure name OR password are not empty
      if (this.input.name != "" || this.input.password != "") {
        console.log("authenticated");
      } else {
        console.log("Name and Password can not be empty");
      }
    },
  },
  // lifecycle hooks
  created() {
    this.getResponse();
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
