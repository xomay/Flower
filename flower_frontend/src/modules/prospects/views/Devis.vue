<template>
  <BaseComponent
    title="Génération de devis"
    :breadcrumb="breadcrumb"
  >
    <h1 class="text-xl">
      Prospect
    </h1>
    <el-form
      :model="etude.prospect"
      label-position="left"
    >
      <el-col :span="24">
        <el-form-item
          label="Nom du prospect"
          prop="name"
          label-width="200px"
        >
          <el-input v-model="etude.prospect.name" />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Adresse"
          prop="address"
          label-width="200px"
        >
          <el-input v-model="etude.prospect.address" />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Code postal"
          prop="postcode"
          label-width="200px"
        >
          <el-input v-model="etude.prospect.postcode" />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Ville"
          prop="town"
          label-width="200px"
        >
          <el-input v-model="etude.prospect.town" />
        </el-form-item>
      </el-col>
    </el-form>
    <h1 class="text-xl">
      Contact client
    </h1>
    <el-form
      :model="etude.prospect"
      label-position="left"
    >
      <el-col :span="24">
        <el-form-item
          label="Nom du contact client"
          prop="name"
          label-width="200px"
        >
          <el-input v-model="etude.clientContact.name" />
        </el-form-item>
      </el-col>
      <el-col :span="24">
        <el-form-item
          label="Poste du contact client"
          prop="name"
          label-width="200px"
        >
          <el-input v-model="etude.clientContact.position" />
        </el-form-item>
      </el-col>
    </el-form>
    <h1 class="text-xl">
      Etude
    </h1>
    <el-form
      :model="etude"
      label-position="left"
    >
      <el-form-item
        label="Nom de l'étude"
        prop="name"
        label-width="140px"
      >
        <el-input v-model="etude.name" />
      </el-form-item>
      <el-form-item
        label="Suiveur de projet"
        prop="projectManager"
        label-width="140px"
      >
        <MemberPicker
          v-model="etude.projectManager"
          :item-list="members"
        />
      </el-form-item>
      <el-form-item
        label="Frais de dossier"
        prop="application_fees"
        label-width="140px"
      >
        <el-input v-model="etude.application_fees" />
      </el-form-item>
    </el-form>
    <h1 class="text-xl">
      Phases
    </h1>
    <PhasesForm
      v-model="etude.groupes"
      :small="true"
      @add-groupe="addGroupe"
      @add-phase="addPhase"
      @delete-groupe="deleteGroupe"
      @delete-phase="deletePhase"
    />
    <el-button
      :loading="loading"
      type="primary"
      @click="downloadDevis"
    >
      Générer le devis
    </el-button>
  </BaseComponent>
</template>

<script>
import PhasesForm from "@/modules/etudes/components/forms/PhasesForm"
import MemberPicker from "@/modules/membres/components/MemberPicker"

const axios = require("axios")

export default {
  name: "Devis",
  components: {PhasesForm,
    MemberPicker},
  data () {
    return {
      breadcrumb: [],
      loading: false,
      etude: {
        name: "",
        projectManager: "",
        clientContact: {
          name: "",
          position: ""
        },
        application_fees: "",
        prospect: {
          name: "",
          address: "",
          postcode: "",
          town: ""
        },
        groupes: []
      },
      members: []
    }
  },
  created () {
    axios.get(
      `${this.$server_url}/membres`,
      {withCredentials: true}
    ).then((res) => {
      res.data.forEach((elt) => elt.value = `${elt.firstname} ${elt.lastname}`)
      this.members = res.data
    }).
      catch((err) => {
        console.log(err)
        this.$message({message: "Impossible de récupérer la liste des Membres",
          type: "error",
          offset: 40})
      })
  },
  methods: {
    addGroupe () {
      const newGroup = {
        title: "Titre",
        description: "Description",
        index: this.etude.groupes.length + 1,
        phases: []
      }
      this.etude.groupes.push(newGroup)
    },
    addPhase (groupe) {
      const newIndex = (Math.max.apply(
          Math,
          groupe.phases.map((phase) => phase.index)
        ) | 0) + 1,
        newPhase = {
          index: newIndex,
          goals: "",
          description: ""
        }
      groupe.phases.push(newPhase)
    },
    deleteGroupe ({groupeIndex}) {
      this.etude.groupes.splice(
        groupeIndex,
        1
      )
    },
    deletePhase ({phase, groupe}) {
      const index = groupe.phases.indexOf(phase)
      if (index > -1) {
        groupe.phases.splice(
          index,
          1
        )
      }
    },
    downloadDevis () {
      this.loading = true
      this.etude.totalPrice = 0
      this.etude.nbJEH = 0
      this.etude.groupes.forEach((groupe) => {
        groupe.totalPrice = 0
        groupe.phases.forEach((phase) => {
          phase.totalPrice = parseInt(phase.nbJEH) * parseFloat(phase.priceJEH)
          groupe.totalPrice += phase.totalPrice
          this.etude.nbJEH += parseInt(phase.nbJEH)
        })
        this.etude.totalPrice += groupe.totalPrice
      })
      this.etude.application_fees = parseInt(this.etude.application_fees)
      this.etude.totalTaxes = (this.etude.totalPrice + this.etude.application_fees) * 0.2
      this.etude.totalPriceTaxes = (this.etude.totalPrice + this.etude.application_fees) * 1.2
      axios.post(
        `${this.$server_url}/publish/devis/`,
        this.etude,
        {withCredentials: true,
          responseType: "blob"}
      ).then((response) => {
        this.createDownloadElement(
          response.data,
          `DEVIS-${this.etude.name}.docx`
        )
      }).
        catch((err) => {
          this.$message({message: `Une erreur est survenue lors de la génération du devis : ${err}`,
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

<style>

</style>
