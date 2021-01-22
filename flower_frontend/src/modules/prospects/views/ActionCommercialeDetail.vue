<template>
  <BaseComponent
    title="Action commerciale"
    :breadcrumb="breadcrumb"
  >
    <template v-slot:action>
      <router-link :to="`/prospects/actionCommerciale/${$route.params.id}/modifier`">
        <el-button
          type="text"
          icon="el-icon-edit"
        >
          Modifier
        </el-button>
      </router-link>
    </template>
    <ACView :action-commerciale="actionCom" />
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
      ]
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
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error"})
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
