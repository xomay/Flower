<template>
  <BaseComponent
    title="Action commerciale"
    :breadcrumb="breadcrumb"
  >
    <template v-slot:action>
      <router-link :to="`/prospects/actionCommerciale/${$route.params.id}/modifier`">
        <el-button
          type="text"
          icon="Edit"
        >
          Modifier
        </el-button>
      </router-link>
    </template>
    <ACView
      :action-commerciale="actionCom"
      :membres-list="membres"
      :actions-types="typesActions"
    />
  </BaseComponent>
</template>

<script>
import ACView from "../components/ACView"
const axios = require("axios")

export default {
  name: "ProspectsDetail",
  components: {ACView},
  data () {
    return {
      actionCom: {},
      loading: false,
      breadcrumb: [
        {
          name: "Lister des actions commerciales",
          link: "/prospects/actionCommerciale/"
        },
        {
          name: "",
          link: "/prospects/actionCommerciale/ajouter"
        }
      ],
      typesActions: [],
      membres: []
    }
  },
  created () {
    this.getProspect()
  },
  methods: {
    getProspect () {
      axios.get(
        `/api/actioncom/${this.$route.params.id}/`,
        {withCredentials: true}
      ).then((res) => {
        this.actionCom = res.data
        this.breadcrumb[1].name = this.actionCom.name
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer l'action commerciale : "+ err, type: "error"})
      })
      axios.get(
        "/api/actioncom/types",
        {withCredentials: true}
      ).then((res) => {
        this.typesActions = res.data
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer la liste des prospects : " + err,
          type: "error",
          offset: 40})
      })
      axios.get(
        "/api/membres/",
        {withCredentials: true}
      ).then((res) => {
        this.membres = res.data
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer la liste des membres : " + err,
          type: "error",
          offset: 40})
      })
    },
    updateProspect () {
      this.loading = true
      axios.put(
        `/api/actioncom/${this.$route.params.id}/`,
        this.actionCom,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "L'action commerciale a bien été mise à jour",
          type: "success"})
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error"})
        }).
        finally(() => {
          this.loading = false
        })
    }
  }
}
</script>

<style>

</style>
