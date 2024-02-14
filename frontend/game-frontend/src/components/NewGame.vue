<template>
  <div class="hello">
    <div class="container">
      <h2 class="alert alert-info">Create A New Game</h2>
      <form @submit.prevent="addGame(this.userId)">
        <div class="row">
          <div class="col">
            <div class="form-group">
              <label class="form-label ml-2">Id</label>
              <input type="text" class="form-control" v-model="game.id" />
            </div>
            <div class="form-group">
              <label class="form-label ml-2">Name</label>
              <input type="text" class="form-control" v-model="game.name" />
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col">
            <div class="form-group">
              <label class="form-label ml-2">Genre</label>
              <input type="text" class="form-control" v-model="game.genre" />
            </div>
          </div>
          <div class="col">
            <div class="form-group">
              <label class="form-label ml-2">Played</label>
              <input type="text" class="form-control" v-model="game.played" />
            </div>
          </div>
          <div class="col">
            <div class="form-group">
              <label class="form-label ml-2">User_Id</label>
              <input type="text" class="form-control" v-model="this.userId" />
            </div>
          </div>
        </div>
        <button type="submit" class="btn btn-primary mt-3">Save</button>
      </form>
    </div>

    <!-- Success Popup -->
    <div v-if="showSuccessPopup" class="success-popup">
      <p>New Game added successfully!</p>
      <button class="success-btn">
        <router-link to="/games" class="link">Games</router-link>
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Games",
  data() {
    return {
      games: [],
      currentGame: {},
      showSuccessPopup: false,
      userId: null,
      api: "http://localhost:5000/resources/games/all",
      game: {
        name: "",
        genre: "",
        played: "",
        user_id: "",
      },
    };
  },
  message: "",
  methods: {
    openModal() {
      this.isModalOpen = !this.isModalOpen;
    },
    closeModal() {
      this.isModalOpen = false;
    },
    parseJWT(token) {
      let base64Url = token.split(".")[1];
      let base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
      let jsonPayload = decodeURIComponent(
        atob(base64)
          .split("")
          .map(function (c) {
            return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
          })
          .join("")
      );
      return JSON.parse(jsonPayload);
    },
    getUserIDFromToken() {
      const token = localStorage.getItem("token");
      // Check if token exists
      if (!token) {
        console.error("Token not found in local storage");
        return null;
      }
      console.log("d", token);
      let payload = this.parseJWT(token);
      console.log(payload.user_id);
      return payload.user_id;
    },
    getGames() {
      this.userId = this.getUserIDFromToken();
      // Make sure userId is not null or undefined
      if (!this.userId) {
        console.error("User ID is missing in local storage");
        return;
      }
      axios
        .get(`http://localhost:5000/resources/games?user_id=${this.userId}`)
        .then((res) => {
          console.log(res);
          this.games = res.data.map((game) => ({
            ...game,
            userId: game.user_id,
          }));
        })
        .catch((err) => {
          console.error(err);
        });
    },
    addGame(userId) {
      this.userId = userId;
      this.game.user_id = this.userId;
      let apiTest = `http://localhost:5000/resources/games?user_id=${this.userId}`;
      axios.post(apiTest, this.game).then((response) => {
        console.log(response.data);
        this.game = {};
        // for message alert
        this.showSuccessPopup = true;
        this.message = "Game added";
        // to show message when game is added
        this.showMessage = true;
      });
      this.getGames();
    },
  },
  // lifecycle hooks
  created() {
    this.getGames();
  },
};
</script>

<style scoped>
/* Form Styles */
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  height: 600px;
  margin-top: 50px;
}

.form-group {
  margin-bottom: 15px;
}

.float-left {
  float: left;
}

.ml-2 {
  margin-left: 10px;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
}

/* Table Styles */
.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

/* Popup Styles */
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

/* Modal Styles */
.modal {
  display: none;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
</style>
