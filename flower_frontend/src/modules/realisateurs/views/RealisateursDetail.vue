<template>
  <BaseComponent
    title="Voir le réalisateur"
    :breadcrumb="breadcrumb"
  >
    <template v-slot:action>
      <router-link :to="`/realisateurs/${$route.params.id}/modifier`">
        <el-button
          type="text"
          icon="el-icon-edit"
        >
          Modifier
        </el-button>
      </router-link>
    </template>
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
    <br>
    <div style="width: 100%; float:left; margin-left: 32%">
      <span><div v-if="realisateur.ba">BA: {{ realisateur.ba }}</div><div v-if="!realisateur.ba">Ba: Non généré</div></span>
      <el-button
        :loading="loadingopenaccount"
        type="warning"
        @click="downloadBA()"
      >
        Générer BA
      </el-button>
      <br><br>
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
    },
    downloadBA () {
      console.log()
      axios.get(
        `/api/publish/barea/${this.realisateur.id}`,
        {withCredentials: true,
          responseType: "blob"}
      ).then((response) => {
        this.createDownloadElement(
          response.data,
          `BA-${this.realisateur.lastname}-${this.realisateur.firstname}.docx`
        )
      }).
        catch((err) => {
          this.$message({message: `Une erreur est survenue lors de la génération du bulletin d'adhésion : ${err}`,
            type: "error"})
        }).
        finally(() => {
          this.loading = false
        })
    },
    createDownloadElement (data, filename) {
      const fileURL = window.URL.createObjectURL(new Blob([data])),
        fileLink = document.createElement("a")

      fileLink.href = fileURL
      fileLink.setAttribute(
        "download",
        filename
      )
      document.body.appendChild(fileLink)

      fileLink.click()
    }
  }
}

</script>
