<template>
  <BaseComponent
    title="Lister les actions commerciales"
    :breadcrumb="breadcrumb"
  >
    TODO la liste des ACs. Il y en a {{ actionsComs.length }}.
  </BaseComponent>
</template>

<script>

const axios = require("axios")

export default {
  name: "ActionCommerciale",
  data () {
    return {
      breadcrumb: [],
      loading: false,
      actionsComs: []
    }
  },
  created () {
    axios.get(
      "/api/actioncom",
      {withCredentials: true}
    ).then((res) => {
      res.data.forEach((elt) => elt.value = elt.name)
      this.actionsComs = res.data
    }).
      catch((err) => {
        console.log(err)
        this.$message({message: "Impossible de récupérer la liste des actions commerciales.",
          type: "error",
          offset: 40})
      })
  }
}
</script>