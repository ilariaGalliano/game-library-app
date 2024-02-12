<template>
  <div>
    <input type="text" v-model="name" placeholder="Name" />
    <input type="email" v-model="email" placeholder="Email" />
    <input type="password" v-model="password" placeholder="Password" />
    <button @click="register">Register</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Register",
  data() {
    return {
      name: "",
      email: "",
      password: "",
    };
  },
  methods: {
    register() {
      axios
        .post("http://localhost:5000/register", {
          name: this.name,
          email: this.email,
          password: this.password,
        })
        .then((response) => {
          console.log(response.data.message);
          console.log(response.data);
          // Handle successful registration (e.g., display success message)
        })
        .catch((error) => {
          console.error("Error registering:", error.response.data.message);
          // Handle registration error (e.g., display error message)
        });
    },
  },
};
</script>
