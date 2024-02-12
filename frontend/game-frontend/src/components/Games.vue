<template>
  <div class="hello">
    <div class="container">
      <h2 class="alert alert-info">Create A New Game</h2>
      <form @submit.prevent="addGame()">
        <div class="row">
          <div class="col">
            <div class="form-group">
              <label class="form-label float-left ml-2">Id</label>
              <input type="text" class="form-control" v-model="game.id" />
            </div>
            <div class="form-group">
              <label class="form-label float-left ml-2">Name</label>
              <input type="text" class="form-control" v-model="game.name" />
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col">
            <div class="form-group">
              <label class="form-label float-left ml-2">Genre</label>
              <input type="text" class="form-control" v-model="game.genre" />
            </div>
          </div>
          <div class="col">
            <div class="form-group">
              <label class="form-label float-left ml-2">Played</label>
              <input type="text" class="form-control" v-model="game.played" />
            </div>
          </div>
        </div>
        <button type="submit" class="btn btn-primary float-left ml-2">
          Save
        </button>
      </form>
      <table class="table mt-5">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Name</th>
            <th scope="col">Genre</th>
            <th scope="col">Played</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="game in games" :key="game.id">
            <th scope="row">{{ game.id }}</th>
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
            <form @submit.prevent="edit" class="w-100 modal-content">
              <label for="name">Name:</label>
              <input type="text" id="name" v-model="editForm.name" />

              <label for="genre">Genre:</label>
              <input type="text" id="genre" v-model="editForm.genre" />

              <label for="played">Played:</label>
              <input type="text" id="played" v-model="editForm.played" />

              <div>
                <button type="submit" variant="outline-info">Update</button>
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
          <!-- end of modal 2 -->
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
      userID: "",
      currentGame: {},
      api: "http://localhost:5000/resources/games/all",
      game: {
        name: "",
        genre: "",
        played: "",
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
    getGames() {
      axios
        .get(this.api)
        .then((res) => {
          console.log(res);
          this.games = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    // getGames() {
    //   // if (!userId) {
    //   //   console.error("User is not logged in");
    //   //   return;
    //   // }
    //   localStorage.setItem("user_id", this.userID);
    //   const userId = localStorage.getItem("user_id");
    //   axios
    //     .get(`http://localhost:5000/resources/games/all?user_id=${userId}`)
    //     .then((res) => {
    //       console.log(res);
    //       this.games = res.data.map((game) => ({
    //         ...game,
    //         userId: game.user_id, // Add userId field to each game object
    //       }));
    //     })
    //     .catch((err) => {
    //       console.error(err);
    //     });
    // },
    addGame() {
      axios.post(this.api, this.game).then((response) => {
        console.log(response.data);
        this.game = {};
        // for message alert
        this.message = "Game added";
        // to show message when game is added
        this.showMessage = true;
        this.getGames();
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
  // mounted() {
  //   axios
  //     .get("http://localhost:5000/api/data")
  //     .then((response) => {
  //       this.data = response.data;
  //       console.log("data", this.data);
  //       this.data.forEach((g) => {
  //         console.log("dd", g.id);
  //         this.userID = g.user_id[0];
  //       });
  //     })
  //     .catch((error) => {
  //       console.error("Error fetching data:", error);
  //     });
  // },
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
/* MODAL */
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
