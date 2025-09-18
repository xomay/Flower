<template>
  <BaseComponent
    title="Prospection"
    :v-loading="loading"
    :breadcrumb="breadcrumb"
  >
    <template #action>
      <router-link to="/prospects/ajouter/">
        <el-button
          type="success"
          icon="Plus"
          style="margin: 0 10px;"
        >
          Ajouter un prospect
        </el-button>
      </router-link>
      <router-link to="/prospects/actionCommerciale/">
        <el-button
          type="primary"
        >
          Voir les actions commerciales
        </el-button>
      </router-link>
    </template>
    <DatePopup
      popup-title="Entrez la nouvelle date"
      :date-name="tampon.dateTitle"
      v-model:visibility="popupVisible"
      :placeholder="tampon.nextDate"
      @finish="popupClosed"
      style="width: 25vw; min-width: 300px;"
    />
    <el-row class="filterRow">
      <el-checkbox v-model="showFilters" icon="Filter" size="large" border style="margin-right: 10px;">
        <el-icon size="large"><Filter /></el-icon>
      </el-checkbox>
      <el-input
        v-model="nameFilterValue"
        style="width: 50%; height: 80%;"
        size="large"
        placeholder="Entrez un nom"
        prefix-icon="Search"
        @change="updateFilters"
        @input="updateFilters"
      />
    </el-row>
    <el-row style="margin: 10px 0;" v-if="showFilters">
      <el-select
        v-model="filteredMembers"
        style="width: 50%;"
        multiple
        size="large"
        placeholder="Filtrer par chargés Dev'co"
        @change="updateFilters"
      >
        <el-option
          v-for="membre in membres"
          :key="membre.id"
          :label="membre.firstname + ' ' + membre.lastname"
          :value="membre.id"
        />
      </el-select>
    </el-row>
    <el-row style="display: flex; flex-wrap: nowrap;">
      <DragZone
        list-id="NC"
        :content="prospectsNouveaux"
        :prospectsLength="prospectsNouveaux.length + prospectToRelancer.length + prospectToDevis.length"
        title="Prospect à traiter"
        :membres-list="membres"
        :contacts-list="contacts"
        @dropped="acceptDrop"
      />
      <DragZone
        list-id="AR"
        :content="prospectToRelancer"
        :prospectsLength="prospectsNouveaux.length + prospectToRelancer.length + prospectToDevis.length"
        title="Traitement en cours"
        :membres-list="membres"
        :contacts-list="contacts"
        @dropped="acceptDrop"
        @changedate="changeDate"
      />
      <DragZone
        list-id="PC"
        :content="prospectToDevis"
        :prospectsLength="prospectsNouveaux.length + prospectToRelancer.length + prospectToDevis.length"
        title="Rédaction du devis"
        :membres-list="membres"
        :contacts-list="contacts"
        @dropped="acceptDrop"
        @changedate="changeDate"
      />
      <DragZone
        list-id="WIN"
        :content="prospectWin"
        :prospectsLength="prospectWin.length + prospectLose.length"
        :items="items"
        title="Prospects gagnés"
        :membres-list="membres"
        :contacts-list="contacts"
        @dropped="acceptDrop"
        @changedate="changeDate"
      />
      <DragZone
        list-id="LO"
        :content="prospectLose"
        :prospectsLength="prospectWin.length + prospectLose.length"
        :items="items"
        title="Prospects perdus"
        :membres-list="membres"
        :contacts-list="contacts"
        @dropped="acceptDrop"
        @changedate="changeDate"
      />
    </el-row>
  </BaseComponent>
</template>

<script>
import DatePopup from "../components/DatePopup"
import DragZone from "../components/DragZone"

const axios = require("axios")

export default {
  name: "ProspectsVoir",
  components: {DragZone, DatePopup},
  data () {
    return {
      prospects: [],
      membres: [],
      filteredMembers: [],
      nameFilterValue: "",
      contacts: [],
      items: [],
      originalItems: [],
      loading: true,
      popupVisible: false,
      showFilters: false,
      tampon: {
        item: {},
        listID: "",
        dateTitle: "Dernier contact :",
        nextDate: new Date().toISOString().split("T")[0]
      },
      breadcrumb: [
        {
          name: "Liste des prospects",
          link: "/prospects"
        }
      ]
    }
  },
  computed: {
    prospectsNouveaux () {
      return this.items.filter(item => item.list == "NC")
    },
    prospectToRelancer () {
      return this.items.filter(item => item.list == "AR")
    },
    prospectToDevis () {
      return this.items.filter(item => (item.list == "PC"))
    },
    prospectWin () {
      return this.items.filter(item => (item.list == "WIN"))
    },
    prospectLose () {
      return this.items.filter(item => (item.list == "LO"))
    },
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      "/api/prospects/",
      {withCredentials: true}
    ).then((res) => {
      this.prospects = res.data
      console.log(this.prospects)
      this.calculateItems()
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les prospects pour le moment: "+err, type: "error"})
    })
    axios.get(
      "/api/contactway/",
      {withCredentials: true}
    ).then((res) => {
      this.contacts = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les contacts pour le moment: "+err, type: "error"})
    })
    axios.get(
      "/api/membres/",
      {withCredentials: true}
    ).then((res) => {
      this.membres = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les membres pour le moment: "+err, type: "error"})
    }).finally(() => {
      this.loading = false
    })
  },
  methods: {
    // itemID : l'id de l'item
    // listID : l'id de la liste (NC, AR, [WIN, PC])
    // forced : si sur true, il y aura une update sur l'API même si aucun changement de source de liste n'est détecté. Utile pour le cas de la dernière colonne.
    acceptDrop (itemID, listID, forced) {
      const item = this.items.find(item => item.id == itemID)
      const prospect = this.prospects.find(i => i.id == itemID)
      if(listID != prospect.advancement || forced) { // Pas de call d'API si on ne change rien :D
        // Mise à jour du "tampon"
        this.tampon = {
          item: item,
          listID: listID,
          dateTitle: "Dernier contact :",
          nextDate: item.nextDate ? item.nextDate : new Date().toISOString().split("T")[0]
        }
        if(listID == "NC") {
          // si on va dans la 1ère colonne, on ne met pas de date de contact.
          this.popupClosed(true, null)
        } else {
          // sinon, on ouvre pas le popup
          this.popupClosed(true, this.tampon.nextDate)
        }
       //this.popupClosed(true, this.tampon.nextDate) //comportement temporaire pour éviter le popup
      }
    },
    changeDate (itemID, listID, forced) {
      const item = this.items.find(item => item.id == itemID)
      const prospect = this.prospects.find(i => i.id == itemID)
      // Mise à jour du "tampon"
      console.log("Changing date for", item)
      this.tampon = {
        item: item,
        listID: listID,
        dateTitle: "Dernier contact :",
        nextDate: item.prospect.nextDate ? item.prospect.nextDate : new Date().toISOString().split("T")[0]
      }
      this.startPopup()
    },
    // ouvre le popup
    startPopup () {
      this.popupVisible = true
    },
    // Referme le popup
    popupClosed (success, out) {
      const prospect = this.tampon.item.prospect
      if(success) {
        this.tampon.item.list = this.tampon.listID
        prospect.nextDate = out
        prospect.advancement = this.tampon.listID
        this.updateProspect(prospect)
      }
      this.popupVisible = false
    },
    // Met à jour le prospect sur le back
    updateProspect (prospect) {
      this.loading = true
      axios.put(
        `/api/prospects/${prospect.id}/`,
        prospect,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Le prospect a bien été mis à jour", type: "success"})
      }).catch((err) => {
        this.$message({message: "Impossible d'update le prospect : "+err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    // transforme les prospects en objets qui sont draggables
    calculateItems () {
      this.originalItems = []
      for (const pr of this.prospects) {
        this.originalItems.push({
          id: pr.id,
          prospect: pr,
          list: pr.advancement,
          win: (pr.advancement === "WIN")
        })
      }
      this.items = [...this.originalItems]
      this.updateFilters()
    },
    // modifie le prototype de Date pour ajouter des jours
    addDaysToDate (date, days) {
      Date.prototype.addDays = function (days) {
        var date = new Date(this.valueOf())
        date.setDate(date.getDate() + days)
        return date
      }
      return date.addDays(days)
    },
    updateFilters () {
      console.log("Updating filters", this.originalItems)
      // Toujours partir des données originales
      let filteredItems = [...this.originalItems]
      
      // Filtrer par nom
      if (this.nameFilterValue) {
        filteredItems = filteredItems.filter(item => 
          item.prospect.name.toLowerCase().includes(this.nameFilterValue.toLowerCase())
        )
      }
      
      // Filtrer par membres si activé
      if (this.filteredMembers.length > 0) {
        filteredItems = filteredItems.filter(item => 
          this.filteredMembers.includes(item.prospect.charge)
        )
      }
      
      this.items = filteredItems
    },
  }
}
</script>

<style scoped>
.filterRow {
  width: 85vw;
  margin-top: 40px;
  margin-bottom: 10px; 
  justify-content: center; 
  align-items: center;
}
</style>
