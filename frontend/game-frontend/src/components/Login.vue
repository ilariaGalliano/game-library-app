<template>
  <div class="hello">
    <div class="container">
      <!-- <h1>{{ name }}</h1>
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
        </div> -->
      <input type="text" v-model="email" placeholder="Email" />
      <input type="password" v-model="password" placeholder="Password" />
      <button @click="login">Login</button>
      <!-- <button
          class="btn btn-outline-dark"
          type="submit"
          v-on:click.prevent="login()"
        >
          Login
        </button>
      </form> -->
    </div>

    <div>
      <h2>Data from Database</h2>
      <ul>
        <li v-for="item in data" :key="item.id">
          {{ item.column1 }} - {{ item.column2 }}
        </li>
      </ul>
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
      email: "",
      password: "",
      data: [],
    };
  },
  methods: {
    login() {
      axios
        .post("http://localhost:5000/login", {
          email: this.email,
          password: this.password,
        })
        .then((response) => {
          console.log(response.data.message);
          // Handle successful login (e.g., redirect to dashboard)
        })
        .catch((error) => {
          console.error("Error logging in:", error.response.data.message);
          // Handle login error (e.g., display error message)
        });
    },
  },
  // mounted() {
  //   axios
  //     .get("http://localhost:5000/api/data")
  //     .then((response) => {
  //       this.data = response.data;
  //       console.log("data", this.data);
  //     })
  //     .catch((error) => {
  //       console.error("Error fetching data:", error);
  //     });
  // },
};
</script>
