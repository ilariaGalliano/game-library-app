<template>
  <div
    style="
      display: flex;
      flex-direction: column;
      align-items: center;
      height: 600px;
      justify-content: center;
      align-content: center;
      background-color: #34a3c682;
    "
  >
    <h1 class="mt-3 mb-3">Register here:</h1>
    <input
      type="text"
      v-model="name"
      placeholder="Name"
      style="
        margin-bottom: 10px;
        padding: 8px;
        width: 200px;
        border: 1px solid #ccc;
        border-radius: 4px;
      "
    />
    <input
      type="email"
      v-model="email"
      placeholder="Email"
      style="
        margin-bottom: 10px;
        padding: 8px;
        width: 200px;
        border: 1px solid #ccc;
        border-radius: 4px;
      "
    />
    <input
      type="password"
      v-model="password"
      placeholder="Password"
      style="
        margin-bottom: 10px;
        padding: 8px;
        width: 200px;
        border: 1px solid #ccc;
        border-radius: 4px;
      "
    />
    <button
      @click="register"
      style="
        padding: 8px 16px;
        background-color: #007bff;
        color: #fff;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        margin-top: 15px;
      "
    >
      Register
    </button>

    <!-- Success Popup -->
    <div
      v-if="showSuccessPopup"
      style="
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: #fff;
        padding: 20px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
        border-radius: 4px;
        z-index: 999;
      "
    >
      <p>Registration successful!</p>
      <button
        style="
          padding: 8px 16px;
          background-color: #007bff;
          color: #fff;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          margin-top: 15px;
        "
      >
        <router-link to="/login" style="color: #fff; text-decoration: none"
          >Login</router-link
        >
      </button>
    </div>
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
      showSuccessPopup: false,
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
          this.showSuccessPopup = true;

          // Reset the form fields
          this.name = "";
          this.email = "";
          this.password = "";
        })
        .catch((error) => {
          console.error("Error registering:", error.response.data.message);
          // Handle registration error (e.g., display error message)
        });
    },
  },
};
</script>
