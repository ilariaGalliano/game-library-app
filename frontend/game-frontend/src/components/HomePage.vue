<template>
  <div class="hello">
    <h1>HomePage</h1>
    <p>Welcome to the Game library app</p>
    <img src="../assets/games.jpg" alt="game" style="width: 100%" />
    <p class="mt-3">
      Game Library is a web application where users can track the video games
      they own, add new games and edit the content.
    </p>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
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
