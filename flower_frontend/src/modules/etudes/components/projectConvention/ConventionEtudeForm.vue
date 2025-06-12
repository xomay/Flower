<template>
  <el-form
    :model="ce"
    label-position="left"
    :rules="formRules"
    ref="ceForm"
  >
    <el-form-item
      label="Signataire Junior"
      label-width="140px"
      style="margin-top: 30px;"
      prop="signer1"
    >
      <MemberPicker
        v-model="ce.signer1"
        :item-list="members"
        placeholder="Entrez le nom du signataire Junior"/>
    </el-form-item>

    <el-form-item
      label="Signataire prospect"
      label-width="140px"
      prop="signer2"
      style="margin-bottom: 40px;"
    >
      <MemberPicker
        v-model="ce.signer2"
        :item-list="employees"
        placeholder="Entrez le nom du signataire du prospect"/>
    </el-form-item>
    <el-form-item
      label="Montant des frais"
      label-width="140px"
      prop="application_fees"
      style="margin-bottom: 40px;"
    >
      <el-input-number
        v-model="ce.application_fees"
        controls-position="right"
        :min="0"
      />
    </el-form-item>
    <el-form-item
      label="Nombre d'intervenants"
      label-width="140px"
      prop="consultantNumber"
      style="margin-bottom: 40px;"
    >
      <el-input-number
        v-model="ce.consultantNumber"
        controls-position="right"
        :min="1"
      />
    </el-form-item>
    <el-form-item 
      label="Contexte et objectifs de l'étude"
      label-width="140px"
      prop="description">
      <el-input
        v-model="ce.description"
        type="textarea"
        :rows="7"
        placeholder="Description concise de l’entreprise et de l’activité du client dans un premier paragraphe. (5-6 lignes)
Description du contexte du client et des raisons qui l’amène à l’émission de cette CC en un ou deux paragraphes.
Présentation de la solution livrée au client."
      />
    </el-form-item>
    <el-form-item 
      label="Présentation des intervenants"
      label-width="140px"
      prop="real_desc">
      <el-input
        v-model="ce.real_desc"
        type="textarea"
        :rows="7"
        placeholder='Présentez votre intervenant ou votre futur intervenant s’il n’est pas encore choisi. 
Mettez en avant ses compétences, expériences… : tout élément valorisant. Vous pouvez aussi faire transparaître ses motivations'
      />
    </el-form-item>
    <el-form-item
      label="Frais matériels ou de déplacements"
      label-width="140px"
      style="margin-bottom: 40px;"
    >
      <el-checkbox v-model="ce.hasMaterialFees" />
    </el-form-item>
    <el-form-item
      v-if="ce.hasMaterialFees"
      label="Montant des frais matériels"
      label-width="140px"
      style="margin-bottom: 40px;"
    >
      <el-input-number
        v-model="ce.materialFees"
        controls-position="right"
        :min=0
        :max=1000
      />
    </el-form-item>
    <el-form-item
      v-if="ce.hasMaterialFees"
      label="Description des frais matériels"
      label-width="140px"
      style="margin-bottom: 40px;"
    >
      <el-input
        v-model="ce.materialDesc"
        type="textarea"
        :rows="3"
        placeholder="Description des frais matériels ou de déplacements"
      />
    </el-form-item>
    <el-form-item
      label="Points de contrôle"
      label-width="140px">
      <el-table
      class="grid"
      :data="ce.controls"
      :row-key="row => row.id"
      >
        <el-table-column
          label="Description"
        >
          <template #default="{row}">
            <el-input
              v-model="row.desc"
              placeholder="Description du point de contrôle"
            />
          </template>
        </el-table-column>
        <el-table-column
          width="200"
          label="Format"
        >
          <template #default="{row}">
            <el-autocomplete
              v-model="row.format"
              class="inline-input"
              :fetch-suggestions="querySearchFormat"
              placeholder="Entrez le format"
            />
          </template>
        </el-table-column>
        <el-table-column
          width="110"
          label="Nécessaire à la phase"
        >
          <template #default="{row}">
            <el-input-number
              v-model="row.phase"
              controls-position="right"
              :min="1"
              :max="99"
              style="width: 90%"
              size="small"
            />
          </template>
        </el-table-column>
        <el-table-column
          width="80"
        >
          <template #default="{row}">
            <el-button
              type="text"
              icon="Delete"
              @click="deleteControl(row, ce.controls)"
            />
          </template>
        </el-table-column>
      </el-table>
      <div class="my-4" style="width: 100%;">
        <div class="flex justify-center">
          <el-button
          type="text"
          icon="Plus"
          @click="addControl(ce.controls)"
          >
          Ajouter un point de contrôle
        </el-button>
      </div>
    </div>
    </el-form-item>
    <el-form-item>
      <el-button
        type="success"
        @click="saveCE"
      >
        Enregistrer
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import MemberPicker from "@/modules/membres/components/MemberPicker"
const axios = require("axios")
export default {
  name: "ConventionEtudeForm",
  components: {
    MemberPicker
  },
  props: {
    etude: { type: Object, required: true }
  },
  data () {
    return {
      ce: {},
      autocomplete: {},
      members: [],
      employees: [],
      formats: [
        { value: "Pdf" },
        { value: "Word" },
        { value: "Excel" },
        { value: "PowerPoint" },
        { value: "Texte" },
        { value: "Image" }
      ],
      formRules: {
        signDate: [
          { required: true, message: "La date de signature est obligatoire", trigger: "blur" }
        ],
        signer1: [
          { required: true, message: "Le signataire junior est obligatoire", trigger: "blur" }
        ],
        signer2: [
          { required: true, message: "Le signataire prospect est obligatoire", trigger: "blur" }
        ],
        consultantNumber: [
          { required: true, message: "Le nombre d'intervenants est obligatoire", trigger: "blur" }
        ],
        real_desc: [
          { required: true, message: "La présentation des intervenants est obligatoire", trigger: "blur" }
        ],
        description: [
          { required: true, message: "Le contexte et les objectifs de l'étude sont obligatoires", trigger: "blur" }
        ],
        application_fees: [
          { required: true, message: "Le montant des frais est obligatoire", trigger: "blur" }
        ]
      }
    }
  },
  watch: {
    etude () {
      this.getCE(this.etude.id)
      this.getEmployees(this.etude.prospect.id)
    }
  },
  created () {
    this.getMembers()
  },
  methods: {
    addControl (controls) {
      controls.push({id: controls.length + 1, desc: "", format: "", phase: ""})
    },
    deleteControl (control, controls) {
      const index = controls.indexOf(control)
      if (index > -1) {
        controls.splice(index, 1)
      }
    },
    querySearchFormat (queryString, cb) {
      const results = queryString ? this.formats.filter((f) => f.toLowerCase().
        includes(queryString.toLowerCase())) : this.formats
      cb(results)
    },
    personFullname (person) {
      if (person) {
        return `${person.firstname} ${person.lastname}`
      }
      return ""
    },
    saveCE () {
      this.ce.signDate = new Date()
      this.etude.application_fees = this.ce.application_fees
      axios.put(
        `/api/etudes/${this.$route.params.id}/ce/`,
        this.ce,
        {withCredentials: true}
      ).then(() => {
        axios.put(
            `/api/etudes/${this.$route.params.id}/`,
            {
              prospect: this.etude.prospect.id,
              application_fees: this.etude.application_fees,
              confidential: this.etude.confidential,
              name: this.etude.name,
              description: this.etude.description,
              mandat: this.etude.mandat,
              number: this.etude.number,
              id: this.etude.id
            },
            {withCredentials: true}
          ).then(() => {
            this.$message({message: "Le document a bien été mis à jour", type: "success"})
            this.$router.push(`/etudes/${this.$route.params.id}/voir`)
          }).catch((err) => {
            this.$message({message: "Impossible de sauvegarder les infos : "+err, type: "error"})
          })
      }).catch((err) => {
        this.$message({message: "Impossible de sauvegarder les infos : "+err, type: "error"})
      })
    },
    getMembers () {
      axios.get(
        "/api/membres",
        {withCredentials: true}
      ).then((res) => {
        res.data.forEach(m => m.value = this.personFullname(m))
        this.members = res.data
        console.log("Members: ", this.members)
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error",
            offset: 40})
        })
    },
    getEmployees (prospectId) {
      axios.get(
        `/api/prospects/${prospectId}/employes/`,
        {withCredentials: true}
      ).then((res) => {
        res.data.forEach(m => m.value = this.personFullname(m))
        this.employees = res.data
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error",
            offset: 40})
        })
    },
    getCE (projectId) {
      axios.get(
        `/api/etudes/${projectId}/ce/`,
        {withCredentials: true}
      ).then((res) => {
        this.ce = res.data
        if (typeof this.ce.materialFees === "string") {
          this.ce.materialFees = parseFloat(this.ce.materialFees)
        }
        console.log("CE : ", this.ce)
        this.autocomplete = {signer1: this.personFullname(this.ce.signer1),
          signer2: this.personFullname(this.ce.signer2)}
        this.ce.signer1 = this.ce.signer1 ? this.ce.signer1.id : null
        this.ce.signer2 = this.ce.signer2 ? this.ce.signer2.id : null
        this.ce.application_fees = Number(this.etude.application_fees)
      }).catch((err) => {
        this.$message({message: err, type: "error"})
      })
    }
  }
}
</script>
