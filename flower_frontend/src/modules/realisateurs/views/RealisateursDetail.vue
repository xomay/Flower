<template>
  <BaseComponent
    title="Voir le réalisateur"
    :breadcrumb="breadcrumb"
  >
    <div style="width: 35%; float:left">
      <RealisateurView
        :realisateur="realisateur"
      />
    </div>
    <div style="width: 60%; float:right; margin-left: 5%">
      <RealisateurCommentsView
        :realisateur="realisateur"
      />
    </div>
  </BaseComponent>
</template>

<script>
import RealisateurView from "../components/RealisateurView"
import RealisateurCommentsView from "../components/RealisateurCommentsView"

const axios = require("axios")

export default {
  name: "RealisateursVoir",
  components: {RealisateurView, RealisateurCommentsView},
  data () {
    return {
      realisateur: {},
      loading: true,
      breadcrumb: [
        {
          name: "Liste des réalisateurs",
          link: "/realisateurs"
        },
        {
          name: "<loading>",
          link: `/realisateurs/${this.$route.params.id}/voir`
        }
      ]
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      `/api/realisateurs/${this.$route.params.id}`,
      {withCredentials: true}
    ).then((res) => {
      this.realisateur = res.data
      this.breadcrumb[1].name = `${this.realisateur.firstname} ${this.realisateur.lastname}`
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer le réalisateur pour le moment : " + err,
        type: "error",
        offset: 40})
    }).finally(() => {
      this.loading = false
    })
  },
  methods: {
    getRatingColor (rating) {
      if(rating < 1) {
        return "red"
      } else if(rating < 3) {
        return "orange"
      } else {
        return "green"
      }
    },
    niceArray (array) {
      var str = ""
      const MAX = 5
      var count = 1
      for (const c of array) {
        if(str !== "")
          str += ", "
        if(count > MAX) {
          const remaining = array.length - MAX
          str += remaining + " autre"+(remaining>1?"s":"")+"."
          break
        }
        str += c
        count ++
      }
      return str
    }
  }
}
</script>
