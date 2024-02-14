<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light pb-3">
      <a class="navbar-brand" href="#">GAME·S</a>
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item active">
            <a class="nav-link" href="/">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/register">Register</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/login">Login</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/games">Games</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/new-games">New Games</a>
          </li>
        </ul>
      </div>
    </nav>
    <router-view />
    <div class="card">
      <div class="card-header">GAME·S website</div>
      <div class="card-body">
        <blockquote class="blockquote mb-0">
          <p>©copyright© 2024</p>
          <footer class="blockquote-footer">Ila •21</footer>
        </blockquote>
      </div>
    </div>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.card-header {
  background-color: #273a4d;
  color: #fff;
}
.card-body {
  background-color: #2c3e50;
  color: #fff;
}
nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
