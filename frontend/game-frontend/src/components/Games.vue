<template>
  <div class="hello">
    <div class="container">
      <button type="button" class="btn btn-success mt-4 mb-3">
        Add new game
      </button>
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
            <th scope="row">{{ game.ID }}</th>
            <td>{{ game.NAME }}</td>
            <td>{{ game.GENRE }}</td>
            <td>{{ game.PLAYED }}</td>
            <td>
              <button type="button" class="btn btn-info mx-3">Upload</button>
              <button type="button" class="btn btn-danger">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
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
    };
  },
  methods: {
    getResponse() {
      // flask app url
      const path = "http://localhost:5000/api/v1/resources/games/all";
      axios
        .get(path)
        .then((res) => {
          console.log(res);
          this.games = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
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
