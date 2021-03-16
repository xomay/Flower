<template>
  <BaseComponent
    :title="title"
    :breadcrumb="breadcrumb"
  >
    <template v-slot:action>
      <router-link :to="`/tresorerie/nfs/${$route.params.id}/modifier/`">
        <el-button
          type="text"
          icon="el-icon-edit"
        >
          Modifier
        </el-button>
      </router-link>
    </template>
    <!-- PRÉSENTATION -->
    <div class="nfsdTableau">
      <el-row
        class="ctn"
      >
        <el-col
          :span="3"
          class="nfLabel"
        >
          Demandeur :
        </el-col>
        <el-col
          :span="5"
        >
          <el-link
            :href="`/membres/${nf.demandeur.id}/voir`"
            type="primary"
            size="small"
          >
            {{ nicePeople(nf.demandeur) }}
          </el-link>
        </el-col>
        <el-col
          :span="3"
          class="nfLabel"
        >
          Date :
        </el-col>
        <el-col
          :span="5"
        >
          {{ niceDate(nf.date) }}
        </el-col>
        <el-col
          :span="3"
          class="nfLabel"
        >
          Type :
        </el-col>
        <el-col
          v-show="nf.isKilometrique"
          :span="5"
          style="background: rgba(112, 177, 157, 0.2);"
        >
          <b>Kilométrique</b>
        </el-col>
        <el-col
          v-show="!nf.isKilometrique"
          :span="5"
          style="background: rgba(177, 168, 168, 0.2);"
        >
          <b>Normale</b>
        </el-col>
      </el-row>
      <el-row>
        <el-col
          :span="3"
          class="ctn nfLabel"
        >
          Objet :
        </el-col>
        <el-col :span="21">
          {{ nf.objet }}
        </el-col>
      </el-row>
      <el-row
        style="border-bottom: none;"
        class="ctn"
      >
        <el-col
          :span="3"
          class="nfLabel"
        >
          Montant HT :
        </el-col>
        <el-col :span="5">
          {{ nf.montantHT }} €
        </el-col>
        <el-col
          :span="3"
          class="nfLabel"
        >
          Montant TVA :
        </el-col>
        <el-col :span="5">
          {{ nf.montantTVA }} €
        </el-col>
        <el-col
          :span="3"
          class="nfLabel"
        >
          Montant TTC :
        </el-col>
        <el-col :span="5">
          {{ nf.montantTTC }} €
        </el-col>
      </el-row>
    </div>
    <hr>
    <el-row
      style="margin: 20px 12px;"
    >
      <el-upload
        class="upload-demo"
        action="/api/upload/"
        :http-request="requestPostFile"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :before-remove="beforeRemove"
        multiple
        drag
        :limit="3"
        :on-exceed="handleExceed"
        :file-list="fileList"
      >
        <i class="el-icon-upload" />
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
    </el-row>
    <hr>
    <!-- DÉTAILS TYPE (NORMAUX) -->
    <el-table
      v-show="detailsN.length > 0"
      :data="detailsN"
      :striped="true"
      :border="true"
      row-class-name="nfTabRow"
      header-row-class-name="nfTabHeader"
    >
      <el-table-column
        label="Description"
        prop="description"
      />
      <el-table-column
        label="Montant HT"
        prop="prixHT"
        fixed="right"
        width="120px"
        align="center"
        :formatter="euroFormatter"
      />
      <el-table-column
        label="TVA"
        fixed="right"
        width="90px"
        align="center"
      >
        <template slot-scope="scope">
          {{ scope.row.tva * 100 }} %
        </template>
      </el-table-column>
      <el-table-column
        label="Montant TVA"
        prop="montantTVA"
        fixed="right"
        width="120px"
        align="center"
        :formatter="euroFormatter"
      />
      <el-table-column
        label="Montant TTC"
        prop="montantTTC"
        style="font-weight: bold;"
        fixed="right"
        width="120px"
        align="center"
        class-name="nfBolded"
        :formatter="euroFormatter"
      />
    </el-table>
    <!-- DÉTAILS TYPE (KILOMETRIQUES) -->
    <el-table
      v-show="detailsK.length > 0"
      :data="detailsK"
      :striped="true"
      :border="true"
      style="margin-top: 20px;"
      row-class-name="nfTabRow"
      header-row-class-name="nfTabHeader"
      cell-class-name=""
    >
      <el-table-column
        label="Description"
        prop="description"
      />
      <el-table-column
        label="Nombre de kilomètres"
        prop="nbKilometres"
        fixed="right"
        width="190px"
        align="center"
      />
      <el-table-column
        label="Prix / kilomètre"
        fixed="right"
        width="140px"
        align="center"
      >
        <template slot-scope="scope">
          {{ scope.row.prixCentimesKilometres }} cts
        </template>
      </el-table-column>
      <el-table-column
        label="Montant TTC"
        prop="montantTTC"
        fixed="right"
        width="120px"
        align="center"
        class-name="nfBolded"
        :formatter="euroFormatter"
      />
    </el-table>
  </BaseComponent>
</template>

<script>
const axios = require("axios")
import UtilsMixin from "@/mixins/Utils"
export default {
  name: "NFsVoir",
  mixins: [UtilsMixin],
  data () {
    return {
      nf: {
        demandeur: {
          firstname: "",
          lastname: "",
          id: 0
        },
        details: []
      },
      fileList: [],
      title: "NF <loading>",
      loading: true,
      breadcrumb: [
        {
          name: "Liste des NF",
          link: "/tresorerie/nfs/voir/"
        },
        {
          name: "<loading>",
          link: `/tresorerie/nfs/${this.$route.params.id}/voir/`
        }
      ]
    }
  },
  computed: {
    detailsN () { return this.nf.details.filter(d => ! d.isKilometrique) },
    detailsK () { return this.nf.details.filter(d => d.isKilometrique) }
  },
  beforeCreate () {
    axios.get(
      `/api/ndfs/${this.$route.params.id}/`,
      { withCredentials: true }
    ).then((res) => {
      this.nf = res.data
      this.breadcrumb[1].name = this.nf.reference
      this.title = "NF " + this.nf.reference
      this.nf.linkedFiles.forEach(lf => {
        this.fileList.push({
          ...lf,
          name: lf.displayName
        })
      })
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer la NF : " + err, type: "error"})
    })
  },
  methods: {
    requestPostFile (request) {
      console.log("Start request")
      this.loading = true
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
          `/api/ndfs/${this.$route.params.id}/files/`,
          {new_file : new_file_id},
          {withCredentials: true}
        ).then((end) => {
          this.$message({message: "NF mise à jour avec succès.", type: "success"})
          console.log(end)
          this.nf.linkedFiles.push(new_file_id)
        }).catch((err) => {
          this.$message({message: "Échec de la mise à jour : " + err, type: "error"})
          console.log("fail set")
        }).finally(() => {
          this.loading = false
        })
      }).catch((err) => {
        this.$message({message: "Échec de l'upload : " + err, type: "error"})
        this.loading = false
      })
    },
    handleRemove (file, fileList) {
      console.log(file, fileList)
    },
    handlePreview (file) {
      console.log(file)
    },
    handleExceed (files, fileList) {
      this.$message.warning(`La limite est 3, vous avez choisi ${files.length} fichiers, soit ${files.length + fileList.length} au total.`)
    },
    beforeRemove (file, fileList) {
      return this.$confirm(`Supprimer le transfert de ${ file.name } [${fileList}] ?`)
    }
  }
}
</script>

<style>

  .nfsdTableau {
    border-collapse: collapse;
    margin: 35px auto 25px auto;
    font-size: 0.9em;
    color: rgb(68, 62, 62);
    font-family: sans-serif;
    min-width: 500px;
    width: 98%;
    box-shadow: 5px 2px 10px rgba(0, 0, 60, 0.15);
  }

  .nfsdTableau .el-row {
    border-bottom: solid rgba(145, 130, 130, 0.6) 1px;
  }

  .nfsdTableau .el-col {
    border-right: solid rgba(145, 130, 130, 0.6) 1px;
    padding: 12px 10px;
  }

  .empty {
    background: rgba(146, 147, 179, 0.2);
  }

  .ctn {
    text-align: center;
  }

  .nfLabel {
    font-weight: bold;
  }

  .nfTabRow {
    color: rgb(68, 62, 62);
  }

  .nfTabHeader {
    color: rgb(75, 75, 75)
  }

  .nfBolded {
    font-weight: bold;
  }
</style>
