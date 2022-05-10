<template>
  <el-row
    style="margin: 20px 12px;"
  >
    <el-col
      :span="fullScreen ? 8 : 24"
    >
      <el-upload
        class="upload-demo"
        action="/api/upload/"
        :http-request="requestPostFile"
        multiple
        drag
        :show-file-list="false"
      >
        <i :class="loading || loadingLocal ? 'el-icon-loading' : 'el-icon-upload'" />
        <div class="el-upload__text">
          Déposer les fichiers ici ou <em>cliquez pour envoyer</em>
        </div>
        <div
          slot="tip"
          class="el-upload__tip"
        >
          Fichiers avec une taille inférieure à 2.5 Mo.
        </div>
      </el-upload>
    </el-col>
    <br v-if="!fullScreen">
    <el-col
      :span="fullScreen ? 16 : 24"
    >
      <el-table
        class="grid"
        :data="linkedFiles"
        :stripe="true"
        :border="true"
        empty-text="Aucun document n'est lié à cette ressource"
      >
        <el-table-column
          align="center"
          prop="author"
          label="Uploader"
          width="170px"
          fixed="left"
          sortable
        >
          <template slot-scope="scope">
            <router-link :to="`/realisateurs/${scope.row.author.id}/voir`">
              <el-button
                type="text"
                size="small"
              >
                {{ nicePeople(scope.row.author) }}
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
          width="140px"
          fixed="right"
          sortable
        >
          <template slot-scope="scope">
            {{ niceFileSize(scope.row.size) }}
          </template>
        </el-table-column>
        <el-table-column
          align="center"
          prop="uploadDate"
          label="Date d'upload"
          width="200px"
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
          <template slot-scope="scope">
            <el-button
              type="text"
              icon="el-icon-link"
              :loading="loading"
              @click="getLink(scope.row.id)"
            />
            <el-button
              type="text"
              :icon="scope.row.got ? 'el-icon-check' : 'el-icon-download'"
              :disabled="scope.row.got"
              :loading="loading || loadingLocal"
              style="color: #54b20b;"
              @click="downloadUpload(scope.row)"
            />
            <el-button
              type="text"
              icon="el-icon-delete"
              :loading="loading || loadingLocal"
              style="color: red;"
              @click="deleteUpload(scope.row, scope.$index)"
            />
          </template>
        </el-table-column>
      </el-table>
    </el-col>
  </el-row>
</template>

<script>
const axios = require("axios")
import UtilsMixin from "@/mixins/Utils"
import Publishing from "@/mixins/Publishing"
export default {
  name: "UploaderLocal",
  mixins: [UtilsMixin, Publishing],
  props: {
    apiBaseUrl: { type: String, required: true },
    loading: { type: Boolean, required: true },
    initalList: { type: Array, required: true },
    fullScreen: { type: Boolean, default: true }
  },
  data () {
    return {
      loadingLocal: false,
      linkedFiles: []
    }
  },
  watch: {
    initalList (il) {
      this.linkedFiles = [...il]
    }
  },
  methods: {
    requestPostFile (request) {
      this.loadingLocal = true
      let formData = new FormData()
      formData.append("file", request.file)
      axios.post(
        "api/upload/",
        formData,
        {
          withCredentials: true,
          headers: {
            "Content-Type": "multipart/form-data", // pour le navigateur
            "enctype": "multipart/form-data" // pour Django
          }
        }
      ).then((res) => {
        this.$message({message: "Upload réussi.", type: "success"})
        const new_file_id = res.data[0]
        axios.put(
          `/api/${this.apiBaseUrl}/${this.$route.params.id}/files/`,
          {
            mode: "add",
            file_id : new_file_id
          },
          {withCredentials: true}
        ).then((end) => {
          this.$message({message: "Ressource mise à jour avec succès.", type: "success"})
          this.linkedFiles.push(end.data)
        }).catch((err) => {
          this.$message({message: "Échec de la mise à jour : " + err, type: "error"})
        }).finally(() => {
          this.loadingLocal = false
        })
      }).catch((err) => {
        this.$message({message: "Échec de l'upload : " + err, type: "error"})
        this.loadingLocal = false
      })
    },
    deleteUpload (file, arrayID) {
      this.loadingLocal = true
      axios.put(
        `/api/${this.apiBaseUrl}/${this.$route.params.id}/files/`,
        {
          mode: "remove",
          file_id : file.id,
          delete_file : true
        },
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Document mis à jour avec succès.", type: "success"})
        this.linkedFiles.splice(arrayID, 1)
      }).catch((err) => {
        this.$message({message: "Échec de la suppression : " + err, type: "error"})
      }).finally(() => {
        this.loadingLocal = false
      })
    },
    downloadUpload (upl) {
      this.loadingLocal = true
      axios.get(
        `/api/upload/${upl.id}/`,
        { withCredentials: true, responseType: "blob" }
      ).then((res) => {
        this.createDownloadElement(res.data, res.headers["content-disposition"].split("=")[1])
        upl.got = true
      }).catch((err) => {
        this.$message({message: `Impossible de récupérer l'upload ${upl.id} : ${err}.`, type: "error"})
      }).finally(() => {
        this.loadingLocal = false
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
