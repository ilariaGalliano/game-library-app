<template>
  <div class="hello">
    <div class="container">
      <h2 class="alert alert-info">Create A New Game</h2>
      <form @submit.prevent="addGame(game.user_id)">
        <div class="row">
          <div class="col">
            <div class="form-group">
              <label class="form-label float-left ml-2">Id</label>
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
      data: [],
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
    getGames() {
      this.userId = 1;
      localStorage.setItem("user_id", this.userId);
      const userID = localStorage.getItem("user_id");
      axios
        .get(`http://localhost:5000/resources/games?user_id=${userID}`)
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
      this.game.user_id = userId;
      axios.post(this.api, this.game).then((response) => {
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
  mounted() {
    axios
      .get("http://localhost:5000/api/data")
      .then((response) => {
        this.data = response.data;
        console.log("data", this.data);
        this.data.forEach((g) => {
          console.log("dd", g.id);
          this.userID = g.user_id[0];
        });
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
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
