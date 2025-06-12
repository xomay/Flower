<template>
  <BaseComponent
    title="Gestion des uploads"
    :breadcrumb="breadcrumb"
  >
    <el-table
      class="grid"
      :data="uploads"
      :stripe="true"
      :border="true"
    >
      <el-table-column
        align="center"
        prop="author"
        label="Auteur"
        width="170px"
        fixed="left"
        sortable
      >
        <template v-slot="scope">
          <router-link :to="`/realisateurs/${scope.row.author.id}/voir`">
            <el-button
              type="text"
              size="small"
            >
              {{ scope.row.author.firstname + " " + scope.row.author.lastname }}
            </el-button>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column
        align="center"
        prop="displayName"
        label="Nom"
        sortable
      />
      <el-table-column
        align="center"
        prop="size"
        label="Taille"
        width="150px"
        fixed="right"
        sortable
      >
        <template v-slot="scope">
          {{ niceSize(scope.row.size) }}
        </template>
      </el-table-column>
      <el-table-column
        align="center"
        prop="uploadDate"
        label="Date d'upload"
        width="250px"
        fixed="right"
        sortable
      />
      <el-table-column
        align="center"
        prop="size"
        label="Opérations"
        width="150px"
        fixed="right"
        sortable
      >
        <template v-slot="scope">
          <el-button
            type="text"
            icon="Link"
            :loading="loading"
            @click="getLink(scope.row.id)"
          />
          <el-button
            type="text"
            :icon="scope.row.got ? 'el-icon-check' : 'el-icon-download'"
            :disabled="scope.row.got"
            :loading="loading"
            style="color: #54b20b;"
            @click="downloadUpload(scope.row)"
          />
          <el-button
            type="text"
            icon="Delete"
            :loading="loading"
            style="color: red;"
            @click="deleteUpload(scope.row.id, scope.$index)"
          />
        </template>
      </el-table-column>
    </el-table>
  </BaseComponent>
</template>

<script>
const axios = require("axios")
import Publishing from "@/mixins/Publishing"
export default {
  name: "UploadManagement",
  mixins: [Publishing],
  data () {
    return {
      breadcrumb: [
        {
          name: "Gestion des uploads",
          link: "/administration/postes"
        }
      ],
      loading: true,
      uploads: []
    }
  },
  created () {
    axios.get(
      "/api/upload/",
      { withCredentials: true }
    ).then((res) => {
      res.data.forEach(elt => elt.got= false)
      this.uploads = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les uploads : " + err, type: "error"})
    }).finally(() => {
      this.loading = false
    })
  },
  methods: {
    niceSize (size) {
      if(size < 1000)
        return size + " o"
      else if(size < 1000000)
        return (size / 1000).toFixed(2) + " Ko"
      else if(size < 1000000000)
        return (size / 1000000).toFixed(2) + " Mo"
      else
        return (size / 1000000000).toFixed(2) + " Go"
    },
    downloadUpload (upl) {
      this.loading = true
      axios.get(
        `/api/upload/${upl.id}/`,
        { withCredentials: true, responseType: "blob" }
      ).then((res) => {
        this.createDownloadElement(res.data, res.headers["content-disposition"].split("=")[1])
        upl.got = true
      }).catch((err) => {
        this.$message({message: `Impossible de récupérer l'upload ${upl.id} : ${err}.`, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    deleteUpload (id, arrayID) {
      this.loading = true
      axios.delete(
        `/api/upload/${id}/`,
        { withCredentials: true }
      ).then(() => {
        this.$message({message: "Upload supprimé avec succès.", type: "success"})
        this.uploads.splice(arrayID, 1)
      }).catch((err) => {
        this.$message({message: "Impossible de supprimer l'upload "+id+" : " + err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    getLink (uploadId) {
      this.loadingInvoice = true
      axios.get(`/api/upload/sharedurl/${uploadId}`, { withCredentials: true }).then((response) => {
        console.log(response)
        let url = location.protocol + "//" + location.host + response.data
        navigator.clipboard.writeText(url)
        this.$message({ message: "Lien copié", type: "succes" })
      }).catch(err => {
        this.$message({ message: "Une erreur est survenue lors de la génération du lien du document : " + err, type: "error" })
      }).finally(() => {
        this.loadingInvoice = false
      })
    },
  }
}
</script>