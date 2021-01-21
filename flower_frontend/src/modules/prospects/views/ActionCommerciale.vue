<template>
  <BaseComponent
    title="Création d'action commerciale"
    :breadcrumb="breadcrumb"
  >
    <h1 class="text-xl">
      Action commerciale
    </h1>
    <el-form
      ref="devisForm1"
      :model="actionCommerciale"
      label-position="left"
      size="small"
    >
      <el-col :span="24">
        <el-form-item
          label="Type d'action"
          prop="type"
          label-width="26%"
        >
          <el-select v-model="actionCommerciale.type">
            <el-option value="Linked In">
              Linked In
            </el-option>
            <el-option value="Salon">
              Salon
            </el-option>
            <el-option value="Téléphone">
              Téléphone
            </el-option>
            <el-option value="Mailing">
              Mailing
            </el-option>
          </el-select>
        </el-form-item>
      </el-col>
    </el-form>
  </BaseComponent>
</template>

<script>
//import MemberPicker from "@/modules/membres/components/MemberPicker"

const axios = require("axios")

export default {
  name: "ActionCommerciale",
  //components: {MemberPicker},
  data () {
    return {
      breadcrumb: [],
      loading: false,
      // Données exportées au final
      actionCommerciale: {
        actionCommerciale: "",
        name: "",
        projectManager: ""
      },
      // Fields pour stocker les données.
      prospects: [],
    }
  },
  created () {
    axios.get(
      "/api/prospects",
      {withCredentials: true}
    ).then((res) => {
      res.data.forEach((elt) => elt.value = elt.name)
      this.prospects = res.data
    }).
      catch((err) => {
        console.log(err)
        this.$message({message: "Impossible de récupérer la liste des prospects.",
          type: "error",
          offset: 40})
      })
  },
  methods: {
    // Récupère le prospect avec l'ID de ce dernier
    finishedSelectProspect (idPR) {
      var pr = this.prospects.find(pre => pre.id == idPR)
      if(pr != undefined) {
        this.forceProspectValues(pr)
      } else {
        this.$message({message: "Prospect inconnu. ID="+idPR+".",
          type: "error"})
      }
    },
    // Vérifie que le nom de prospect n'est pas vide (ce champs est rempli avec l'ID sous forme de string)
    notEmptyCheck (rule, value, callback) {
      if (value == "") {
        callback(new Error("Nom de prospect inconnu."))
      } else {
        callback()
      }
    },
    // Force les valeurs des champs du prospect avec ce dernier
    forceProspectValues (pr) {
      this.etude.prospect.address = pr.address
      this.etude.prospect.postcode = pr.postcode
      this.etude.prospect.town = pr.town
    },
    // Vide le contenu du name de prospect si il n'est pas valide.
    checkIfProspectExists (fieldValue) {
      var pr = this.prospects.find(pre => pre.id == fieldValue)
      if(pr == undefined) {
        this.etude.prospect.name = ""
      }
    },
    // Valide tout le form, appelle le 'downloadDevis' en cas de réussite.
    validateAllFields () {
      var result = true
      this.$refs.devisForm1.validate((r) => result = (r ? result : false ))
      this.$refs.devisForm2.validate((r) => result = (r ? result : false ))
      this.$refs.devisForm3.validate((r) => result = (r ? result : false ))

      if(this.etude.groupes.length == 0) {
        this.$message({message: "Erreur : Le devis ne présente aucun groupe !", type: "error", offset: 40})
        return
      }

      if(result == true) {
        this.downloadDevis()
        //TODO push en arrière ?
      } else {
        this.$message({message: "Erreur : Certains champs ne sont pas valides !",
          type: "error",
          offset: 40})
      }
    }
  }
}
</script>