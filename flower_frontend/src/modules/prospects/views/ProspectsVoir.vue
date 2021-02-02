<template>
  <BaseComponent
    title="Prospection"
    :v-loading="loading"
    :breadcrumb="breadcrumb"
  >
    <DatePopup
      popup-title="Entrez la nouvelle date"
      :date-name="tampon.dateTitle"
      :visibility="popupVisible"
      :placeholder="tampon.nextDate"
      @finish="popupClosed"
    />
    <el-row
      :style="{margin:'3vh auto 2vh 1vw'}"
    >
      <el-col
        :span="3"
      >
        <h1
          class="text-xl"
          :style="{width:'100%'}"
        >
          Actions commerciales
        </h1>
      </el-col>
      <el-col
        :span="3"
        :offset="1"
      >
        <router-link to="/prospects/actionCommerciale/">
          <el-button
            type="primary"
          >
            Voir les actions commerciales
          </el-button>
        </router-link>
      </el-col>
    </el-row>
    <el-row
      :style="{margin:'3vh auto 2vh 1vw'}"
    >
      <el-col
        :span="3"
      >
        <h1
          class="text-xl"
        >
          Ajouter un prospect :
        </h1>
      </el-col>
      <el-col
        :span="3"
        :offset="1"
      >
        <router-link to="/prospects/ajouter/">
          <el-button
            type="success"
            icon="el-icon-plus"
          />
        </router-link>
      </el-col>
    </el-row>
    <div class="filtresDiv">
      Les filtres seront là dans une future mise à jour.
    </div>
    <div class="rowStyle">
      <DragZone
        list-id="NC"
        :content="prospectsNouveaux"
        title="Nouveaux prospects"
        :membres-list="membres"
        :contacts-list="contacts"
        @dropped="acceptDrop"
      />
      <DragZone
        list-id="AR"
        :content="prospectToRelancer"
        title="Prospects à relancer"
        :membres-list="membres"
        :contacts-list="contacts"
        @dropped="acceptDrop"
      />
      <DragZone
        list-id="RDV"
        :content="prospectWithRDV"
        title="Devis à envoyer / Rendez-vous obtenu"
        :membres-list="membres"
        :contacts-list="contacts"
        @dropped="acceptDrop"
      />
    </div>
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
      contacts: [],
      items: [],
      loading: true,
      popupVisible: false,
      constantsDate: {
        NC: "texte impossible à afficher !",
        AR: "Date du dernier contact :",
        RDV: "Date du rendez-vous :",
        DS: "Deadline du devis :"
      },
      tampon: {
        item: {},
        listID: "",
        dateTitle: "",
        nextDate: this.createDate()
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
    prospectWithRDV () {
      return this.items.filter(item => (item.list == "RDV" || item.list == "DS"))
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      "/api/prospects/",
      {withCredentials: true}
    ).then((res) => {
      this.prospects = res.data
      this.calculateItems()
    }).
      catch(() => {
        this.$message({message: "Impossible de récupérer les prospects pour le moment",
          type: "error"})
      }).
      finally(() => {})
    axios.get(
      "/api/contactway/",
      {withCredentials: true}
    ).then((res) => {
      this.contacts = res.data
    }).
      catch(() => {
        this.$message({message: "Impossible de récupérer les contacts pour le moment",
          type: "error"})
      }).
      finally(() => {})
    axios.get(
      "/api/membres/",
      {withCredentials: true}
    ).then((res) => {
      this.membres = res.data
    }).
      catch(() => {
        this.$message({message: "Impossible de récupérer les membres pour le moment",
          type: "error"})
      }).
      finally(() => {
        this.loading = false
      })
  },
  methods: {
    // itemID : l'id de l'item
    // listID : l'id de la liste (NC, AR, [DS, RDV])
    // forced : si sur true, il y aura une update sur l'API même si aucun changement de source de liste n'est détecté. Utile pour le cas de la dernière colonne.
    acceptDrop (itemID, listID, forced) {
      const item = this.items.find(item => item.id == itemID)
      const prospect = this.prospects.find(i => i.id == itemID)
      if(listID != prospect.advancement || forced) { // Pas de call d'API si on ne change rien :D
        // Mise à jour du "tampon"
        this.tampon = {
          item: item,
          listID: listID,
          dateTitle: this.constantsDate[listID],
          nextDate: this.createDate()
        }
        if(listID == "NC") {
          // si on va dans la 1ère colonne, il n'y a aucun intéret à demander de date.
          this.popupClosed(true, this.tampon.nextDate)
        } else {
          // sinon, on ouvre le popup
          this.startPopup()
        }
      }
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
        this.$message({message: "Le prospect a bien été mis à jour",
          type: "success"})
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error"})
        }).
        finally(() => {
          this.loading = false
        })
    },
    // transforme les prospects en objets qui sont draggables
    calculateItems () {
      for (const pr of this.prospects) {
        this.items.push({
          id: pr.id,
          prospect: pr,
          list: pr.advancement,
          devisOn: (pr.advancement === "DS")
        })
      }
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
    // créer une date 15 jours après aujourd'hui
    createDate () {
      var today = new Date()
      today = this.addDaysToDate(today, 15)
      var dd = String(today.getDate())
      dd = dd.padStart(2, "0")
      var mm = String(today.getMonth() + 1).padStart(2, "0")
      var yyyy = today.getFullYear()
      return yyyy + "-" + mm + "-" + dd
    }
  }
}
</script>

<style scoped>
.filtresDiv {
  width: 95%;
  height: 5vh;
  border: 1px solid black;
  margin: 1em;
  text-align: center;
}
</style>
