<template>
  <div>
    <el-card
      v-for="item in realisateur.comments"
      :key="item.id"
      :style="'margin: 12px'"
    >
      <div>
        <div style="width: 60px; float:left;">
          <span>
            <u>Date : </u>
          </span>
        </div>
        <div style="width: 48px; float:left;">
          <span>
            {{ getComment(item).date }}
          </span>
        </div>
        <div style="width: 50%; float:right">
          <el-rate
            :value="getComment(item).rating"
            :max="10"
            :disabled="true"
            :allow-half="true"
            :low-threshold="3.33"
            :high-threshold="6.66"
            :colors="['#ff1111', '#ffa200', '#62da05']"
          />
        </div>
      </div>
      <el-divider class="dividerStyle" />
      <p>
        <u>Commentaire :</u><br>
        {{ getComment(item).content }}
      </p>
    </el-card>
  </div>
</template>

<script>
const axios = require("axios")

export default {
  name: "RealisateurCommentsView",
  props: {
    realisateur: { type: Object, required: true }
  },
  data () {
    return {
      comments: []
    }
  },
  created () {
    axios.get(
      "/api/realisateurs/cmts",
      {withCredentials: true}
    ).then((res) => {
      this.comments = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les commentaires : " + err, type: "error", offset: 40})
    })
  },
  methods: {
    getComment (id) {
      const found = this.comments.find(c => c.id === id)
      return found != undefined ? found : {content:"",date:"",rating:-1}
    }
  }
}
</script>

<style scoped>
  .dividerStyle {
    margin: 38px 0 12px 0 !important;
  }
</style>