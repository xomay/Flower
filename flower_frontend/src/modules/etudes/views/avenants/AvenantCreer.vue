<template>
  <BaseComponent
    title="Ajouter un avenant"
    :breadcrumb="breadcrumb"
  >
    <AvenantForm
      :create="true"
      :avenant="avenant"
      :etude="etude"
      :avenantsRM="avenantsRM"
      :loading="loading"
      :membres="membres"
      :intervenants="intervenants"
      :employes="employes"
      :isClient="false"
      :isInter="false"
      @update-reference="updateReference"
      @update-rm-reference="updateRMReference($event)"
      @validate-avenant="saveAvenant"
    />
    
  </BaseComponent>
</template>

<script>
import AvenantForm from "@/modules/etudes/components/forms/AvenantForm"
import Utils from "@/mixins/Utils"
const axios = require("axios")
// Configuration d'axios pour CSRF
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.withCredentials = true;
export default {
  name: "AvenantCreer",
  components: {AvenantForm},
  mixins: [Utils],
  data () {
    return {
      membres: [],
      employes: [],
      loading: true,
      avenant: {
        ref: "AVx",
        etude: this.$route.params.id,
        doc_etude: {
          application_fees: 0,
          hasMaterialFees: false,
          materialFees: 0,
          materialDesc: "",
          signer1: 0,
          signer2: 0,
        },
        index: 1,
        comment: "",
        description: "",
        signataire_junior: null,
        signataire_prospect: null,
        is_delai: false,
        is_methodo: false,
        is_cdc: false,
        is_budget: false,
        new_dates: null,
        phases: [],
        phasesReal: [],
        phasesTransverse: [],
        requirements: [],
        originalPhases: [],
        signDate: null,
        type: "av",
        application_fees: 0,
        hasMaterialFees: false,
        materialFees: 0,
        materialDesc: "",
      },
      etude: {
        number: 0,
        phases: [],
      },
      intervenants: [],
      avenantsRM: [],
      breadcrumb: [
        {
          name: "Suivi d'étude",
          link: "/etudes"
        },
        {
          name: "<loading>",
          link: `/etudes/${this.$route.params.id}/voir`
        },
        {
          name: "Ajouter un avenant",
          link: `/etudes/${this.$route.params.id}/avenants/client/ajouter`
        },
      ]
    }
  },
  beforeCreate () {
    axios.get(
      `/api/etudes/${this.$route.params.id}/`,
      {withCredentials: true}
    ).then((res) => {
      this.etude = res.data
      this.avenant.doc_etude.signer1 = res.data.docEtude.signer1.id
      this.avenant.doc_etude.signer2 = res.data.docEtude.signer2.id
      this.avenant.doc_etude.application_fees = Number(res.data.docEtude.application_fees)
      this.avenant.doc_etude.hasMaterialFees = res.data.docEtude.hasMaterialFees
      this.avenant.doc_etude.materialFees = Number(res.data.docEtude.materialFees)
      this.avenant.doc_etude.materialDesc = res.data.docEtude.materialDesc
      this.avenant.etude = res.data.id
      this.avenant.index = res.data.avenants.length + 1
      this.avenant.requirements = res.data.requirements
      res.data.cc ? this.avenant.type = "bc" : this.avenant.type = "av"
      res.data.missions.forEach((mission) => {
        this.avenantsRM.push({
          id: mission.id,
          index: mission.avenants.length + 1,
          ref: "AVRM" + 1 +"-_" + mission.consultant.ref_ba + "_" + this.etude.number,
          inter: mission.consultant,
          consultant: mission.consultant.id,
          phases: [],
          originalPhases: [],
          phases_idx: [],
          mission: mission,
          is_delai: false,
          is_methodo: false,
          is_cdc: false,
          is_budget: false,
          description: "",
          doc_mission: {
            signDate: null,
          }
        })
      })
      this.breadcrumb[1].name = res.data.name
      this.updateReference()
      // get employés :
      axios.get(
        `/api/prospects/${res.data.prospect.id}/employes/`,
        {withCredentials: true}
      ).then((resEmpl) => {
        resEmpl.data.forEach((elt) => elt.value = this.nicePeople(elt))
        this.employes = resEmpl.data
      }).catch((err) => {
        this.$message({ message: "Impossible de récupérer les employés de cete étude : " + err, type: "error" })
      }).finally(() => {
        this.loading = false
      })
    }).catch((err) => {
      this.$message({ message: "Impossible de récupérer l'étude pour le moment : " + err, type: "error" })
      this.loading = false
    })
    axios.get(
      "/api/membres/",
      {withCredentials: true}
    ).then((resMembers) => {
      resMembers.data.forEach((elt) => elt.value = this.nicePeople(elt))
      this.membres = resMembers.data
    }).catch((err) => {
      this.$message({ message: "Impossible de récupérer les membres de la JE : " + err, type: "error" })
    })
    axios.get(
      "/api/realisateurs",
      {withCredentials: true}
    ).then((res) => {
      res.data.forEach((realisateur) => realisateur.value = `${realisateur.firstname} ${realisateur.lastname}`)
      this.intervenants = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les réalisateurs : "+err, type: "error", offset: 40})
    })
  },
  methods: {
    updateReference () {
      if (this.etude.cc){
        this.avenant.ref = "BCR" // 'AV'
        + this.avenant.index + "-" // numéro de l'avenant pour cette étude
        + ((this.avenant.is_delai ? "D," : "")
          + (this.avenant.is_methodo ? "M," : "")
          + (this.avenant.is_cdc ? "C," : "")
          + (this.avenant.is_budget ? "B," : "")).slice(0, -1) // bloc pour afficher les lettres du type (multiple) d'avenant
        + "_" + this.etude.number // numéro de l'étude
      }else {
        this.avenant.ref = "AV" // 'AV'
        + this.avenant.index + "-" // numéro de l'avenant pour cette étude
        + ((this.avenant.is_delai ? "D," : "")
          + (this.avenant.is_methodo ? "M," : "")
          + (this.avenant.is_cdc ? "C," : "")
          + (this.avenant.is_budget ? "B," : "")).slice(0, -1) // bloc pour afficher les lettres du type (multiple) d'avenant
        + "_" + this.etude.number // numéro de l'étude
      }
      //On reset les propriétées des phases de l'avenant quand le type d'avenant est annulé
      if (!this.avenant.is_delai){
        this.avenant.phases.forEach((phase) => {
          phase.period = this.etude.phases.find(p => p.index === phase.index).period
        })
      }
      if (!this.avenant.is_cdc){
        this.avenant.phases.forEach((phase) => {
          phase.spec = this.etude.phases.find(p => p.index === phase.index).spec
        })
      }
      if (!this.avenant.is_budget){
        this.avenant.phases.forEach((phase) => {
          phase.nbJEH = this.etude.phases.find(p => p.index === phase.index).nbJEH
        })
      }
      if (!this.avenant.is_methodo){
        this.avenant.phases.forEach((phase) => {
          const phaseRef = this.etude.phases.find(p => p.index === phase.index)
          phase.title = phaseRef.title
          phase.description = phaseRef.description
          phase.methodologie = phaseRef.methodologie
        })
      }
    },
    updateRMReference (avenant) {
        avenant.ref = "AVRM" // 'AV'
        + avenant.index + "-" // numéro de l'avenant pour cette étude
        + ((avenant.is_delai ? "D," : "")
          + (avenant.is_methodo ? "M," : "")
          + (avenant.is_cdc ? "C," : "")
          + (avenant.is_budget ? "B," : "")).slice(0, -1) // bloc pour afficher les lettres du type (multiple) d'avenant
        + "_" + avenant.inter.ref_ba + "_" + this.etude.number // numéro de l'étude
    },
    saveAvenant (filteredAvenantsRM, globalForm) {
      this.loading = true
      let promesses = []
      if (globalForm.is_client){
        const docEtude = {
          application_fees: this.avenant.doc_etude.application_fees,
          hasMaterialFees: this.avenant.doc_etude.hasMaterialFees,
          materialFees: this.avenant.doc_etude.materialFees,
          materialDesc: this.avenant.doc_etude.materialDesc,
          signer1: this.avenant.doc_etude.signer1,
          signer2: this.avenant.doc_etude.signer2,
        }
        const avenantEtude = {
          description: this.avenant.description,
          is_delai: this.avenant.is_delai,
          is_methodo: this.avenant.is_methodo,
          is_cdc: this.avenant.is_cdc,
          is_budget: this.avenant.is_budget,
          doc_etude: null,
          etude: this.$route.params.id,
          index: this.avenant.index,
        }
        promesses.push(this.saveDocs(docEtude, avenantEtude, true).then((resAvenant) => {
          const av = { ...resAvenant, phases: this.avenant.phases }
          this.savePhases(av, this.etude, true)
        }))
      }
      if (globalForm.is_inter){
        this.avenantsRM = filteredAvenantsRM
        this.avenantsRM.forEach((avRM) => {
          const doc_mission = avRM.doc_mission
          const avenantRM = {
            description: avRM.description,
            is_delai: avRM.is_delai,
            is_methodo: avRM.is_methodo,
            is_cdc: avRM.is_cdc,
            is_budget: avRM.is_budget,
            doc_etude: null,
            mission: avRM.mission.id,
            index: avRM.index,
          }
          const mission = { ...avRM.mission, phases: [...avRM.mission.phasesMission] }
          promesses.push(this.saveDocs(doc_mission, avenantRM, false).then((resAvenant) => {
            const av = { ...resAvenant, phases: avRM.phases }
            this.savePhases(av, mission, false)
          }))
        })
      }
      Promise.all(promesses).then(() => {
        this.$message({message: "Avenant créé avec succès", type: "success"})
        this.$router.push(`/etudes/${this.$route.params.id}/voir?active=Avenants`)
      }).catch((error) => {
        console.error("Erreur lors de la création de l'avenant", error)
        this.$message({message: "Erreur lors de la création de l'avenant : " + error, type: "error"})
        this.loading = false
      })
    },
    saveDocs(doc, avenant, client) {
      return new Promise((resolve, reject) => {
        axios.post(
          client ? `/api/etudes/ce/` : `/api/etudes/mission/doc/`,
          doc,
          {withCredentials: true}
        ).then((res) => {
          client ? avenant.doc_etude = res.data.id : avenant.doc_mission = res.data.id
          axios.post(
            client ? `/api/etudes/avenants/` : `/api/etudes/avenants/missions/`,
            avenant,
            {withCredentials: true}
          ).then((resAvenant) => {
            resolve(resAvenant.data)
          }).catch((error) => {
            console.error("Erreur lors de la création de l'avenant", error)
            reject(error)
          })
        }).catch((error) => {
          console.error("Erreur lors de la création du doc", error)
          reject(error)
        })
      })
    },
    savePhases(avenant, related, client) {
      this.loading = true
      avenant.phases.forEach((phase) => {
        phase.avenant_creer = avenant.id
      })
      related.phases.forEach((phase) => {
        phase.avenant_edit = avenant.id
      })
      const newPhases = avenant.phases.filter(p => p.id === undefined || p.id === null)
      //const phasesToSave = [...this.etude.phases.filter(p => this.avenant.phases.some(av_phase => av_phase.index === p.index)), ...this.avenant.phases.filter(p => p.id !== undefined && p.id !== null)]
      const phasesToSave = related.phases.filter(p => avenant.phases.some(av_phase => av_phase.index === p.index)).concat(avenant.phases.filter(p => p.id !== undefined && p.id !== null))
      return new Promise((resolve, reject) => {
        axios.post(
          client ? "/api/etudes/phases/" : "/api/etudes/phases/missions/",
          newPhases,
          {withCredentials: true}
        ).then(() => {
          axios.put(
            client ? "/api/etudes/phases/" : "/api/etudes/phases/missions/",
            phasesToSave,
            {withCredentials: true}
          ).then((res) => {
            resolve(res.data)
          }).catch((err) => {
            console.error("Erreur lors de la mise à jour des phases", err)
            reject(err)
          })
        }).catch((err) => {
          console.error("Erreur lors de l'enregistrement des phases", err)
          reject(err)
        })
      })
    },
  }
}
</script>