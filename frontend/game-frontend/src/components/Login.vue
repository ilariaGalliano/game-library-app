<template>
  <div class="hello">
    <div class="container">
      <h1>Login</h1>
      <input
        type="text"
        v-model="email"
        placeholder="Email"
        class="input-field"
      />
      <input
        type="password"
        v-model="password"
        placeholder="Password"
        class="input-field"
      />
      <button class="btn btn-primary mx-2" @click="login">Login</button>
      <!-- Success Popup -->
      <div v-if="showSuccessPopup" class="success-popup">
        <p>Registration successful!</p>
        <button class="success-btn">
          <router-link to="/games" class="link">Games</router-link>
        </button>
      </div>
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
      showSuccessPopup: false,
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
          this.showSuccessPopup = true;
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

<style scoped>
.hello {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 580px;
}

.container {
  text-align: center;
}

.input-field {
  padding: 8px;
  width: 200px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin: 8px;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-outline-dark {
  background-color: transparent;
  border: 1px solid #343a40;
  color: #343a40;
}

.success-popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #fff;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  z-index: 999;
}

.success-btn {
  padding: 8px 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 15px;
}

.link {
  color: #fff;
  text-decoration: none;
}
</style>
