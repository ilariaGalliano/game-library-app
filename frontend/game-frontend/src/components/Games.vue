<template>
  <div class="hello">
    <div class="container">
      <h1>My Games list:</h1>
      <table class="table mt-5">
        <thead>
          <tr>
            <!-- <th scope="col">#</th> -->
            <th scope="col">Name</th>
            <th scope="col">Genre</th>
            <th scope="col">Played</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="game in games" :key="game.id">
            <!-- <th scope="row">{{ game.id }}</th> -->
            <td>{{ game.name }}</td>
            <td>{{ game.genre }}</td>
            <td>{{ game.played }}</td>
            <td>
              <button
                type="button"
                class="btn btn-info mx-3"
                @click="editBtn(game.id)"
              >
                Edit
              </button>
              <button
                type="button"
                class="btn btn-danger"
                @click="deleteGame(game.id)"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div class="row d-flex justify-content-center">
        <div>
          <!-- Modal -->
          <div v-if="isModalOpen" class="card-info">
            <form @submit.prevent="edit" class="modal-content">
              <label for="name">Name:</label>
              <input type="text" id="name" v-model="editForm.name" />

              <label for="genre">Genre:</label>
              <input type="text" id="genre" v-model="editForm.genre" />

              <label for="played">Played:</label>
              <input type="text" id="played" v-model="editForm.played" />

              <div>
                <button
                  type="submit"
                  class="btn btn-info"
                  variant="outline-info"
                >
                  Update
                </button>
                <button
                  type="reset"
                  variant="outline-danger close"
                  @click="closeModal"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Games",
  props: {
    visible: Boolean,
  },
  data() {
    return {
      isModalOpen: this.visible,
      games: [],
      data: [],
      currentGame: {},
      userId: null,
      api: "http://localhost:5000/resources/games/all",
      game: {
        name: "",
        genre: "",
        played: "",
        user_id: "",
      },
      editForm: {
        name: "",
        genre: "",
        played: "",
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

      let payload = this.parseJWT(token);
      console.log(payload.user_id);
      return payload.user_id;
    },
    getGames() {
      const userId = this.getUserIDFromToken();

      // Make sure userId is not null or undefined
      if (!userId) {
        console.error("User ID is missing in local storage");
        return;
      }
      axios
        .get(`http://localhost:5000/resources/games?user_id=${userId}`)
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
    editBtn(id) {
      this.isModalOpen = !this.isModalOpen;
      console.log("test", this.isModalOpen);
      console.log(id);
      // ricontrollare
      this.games.map((game) => {
        if (game.id === id) {
          console.log("gamdde:", game.id);
          this.currentGame = {
            id: game.id,
            name: game.name,
            genre: game.genre,
            played: game.played,
          };
          this.editForm = {
            name: game.name,
            genre: game.genre,
            played: game.played,
          };
        }
        console.log("game:", this.currentGame);
      });
      console.log("game2:", this.currentGame);
    },
    edit() {
      const apiEdit = `http://localhost:5000/resources/edit_game/${this.currentGame.id}`;
      console.log("game3:", this.currentGame);
      axios.put(apiEdit, this.editForm).then((response) => {
        console.log("data", response.data);
        this.editForm = {};
        // for message alert
        this.message = "Game updated";
        // to show message when game is added
        this.showMessage = true;
        this.getGames();
      });
    },
    deleteGame(id) {
      if (confirm("Are you sure you want to delete this game?")) {
        const apiUrl = `http://localhost:5000/resources/delete_game/${id}`;
        axios
          .delete(apiUrl)
          .then((response) => {
            console.log(response.data.message);
            // Remove the deleted game from the frontend
            this.games = this.games.filter((game) => game.id !== id);
          })
          .catch((error) => {
            console.error("Error deleting game:", error);
            // Handle error
          });
      }
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
  max-width: 700px;
  margin: 0 auto;
  padding: 20px;
  height: 800px;
}

.hello {
  height: 100%;
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
  background-color: #34a3c682;
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

/* Modal Styles */
/* Modal Styles */
.card-info {
  background-color: #fff;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  z-index: 999;
}

.modal-content {
  width: 100%;
}

label {
  margin-bottom: 5px;
  display: block;
}

input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;
}

button[type="submit"] {
  background-color: #007bff;
  color: #fff;
  border: none;
}

button[type="reset"] {
  background-color: transparent;
  color: #007bff;
  border: 1px solid #007bff;
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
