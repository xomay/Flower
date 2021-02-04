<template>
  <div>
    <template>
      <div style="width: 50%; float:left">
        <p class="mainText">
          ERREUR 404
        </p>
        <hr class="brrr">
        <p class="subText">
          Ben alors on s'est perdu ?
        </p>
        <br><br>
        <p class="subsubText">
          Si cette action est inatendue, contacte ton resp SI favori en lui indiquant que l'url <b>{{ currentRouteName }}</b> n'existe pas !
        </p>
      </div>
      <div style="width: 50%; float:right">
        <img
          src="@/assets/wooow.gif"
          class="woooooaw"
        >
      </div>
    </template>
  </div>
</template>

<script>
export default {
  name: "Error404",
  computed: {
    currentRouteName () {
      return this.$router.history.current.path
    }
  }
}
</script>

<style>
  .mainText {
    text-align: center;
    display: block;
    margin-top: 10%;
    margin-bottom: 20%;
    margin-left: auto;
    margin-right: auto;
    font-size: 4em;
    color: rgb(104, 16, 5);
    font-weight: bolder;
  }

  .subText {
    text-align: center;
    display: block;
    margin-left: auto;
    margin-right: auto;
    font-size: 2em;
    margin-top: 15%;
  }

  .subsubText {
    text-align: center;
    display: block;
    font-style: italic;
    color: rgb(53, 51, 51);
    margin-left: auto;
    margin-right: auto;
    font-size: 1em;
    margin-top: 15%;
  }

  .brrr {
    margin-left: 10%;
  }

  .woooooaw {
    display: block;
    margin-top: 2%;
    width: 90%;
    margin: auto;
  }
</style>
