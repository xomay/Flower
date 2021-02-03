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
          <StarRate
            :value="getComment(item).rating"
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
import StarRate from "./StarRate.vue"

const axios = require("axios")

export default {
  name: "RealisateurCommentsView",
  components: {StarRate},
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