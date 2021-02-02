<template>
  <BaseComponent
    title="Lister les actions commerciales"
    :breadcrumb="breadcrumb"
  >
    <el-row
      :style="{margin:'100px, 100px, 0, 1em'}"
    >
      <el-col :span="8">
        <h2 class="labelSlide">
          Cacher les <u>anciennes</u> actions commerciales :
        </h2>
      </el-col>
      <el-col
        :span="8"
      >
        <el-switch
          v-model="onlyFuture"
          @change="updateData"
        />
      </el-col>
    </el-row>
    <router-link to="/prospects/actionCommerciale/ajouter">
      <el-button
        type="primary"
        :style="{margin:'2vh 0 0 1vh'}"
      >
        Créer une action commerciale
      </el-button>
    </router-link>
    <el-divider />
    <el-table
      v-loading="loading"
      :data="displayedData"
      :default-sort="{prop: 'date', order: 'descending'}"
      :row-class-name="colorRow"
      @row-click="rowClicked"
    >
      <el-table-column
        prop="name"
        label="Nom de l'action"
        sortable
      >
        <template slot-scope="scope">
          <font style="color: #333333;">
            <b>{{ scope.row.name }}</b>
          </font>
        </template>
      </el-table-column>
      <el-table-column
        prop="date"
        label="Date"
        sortable
      />
      <el-table-column
        prop="type"
        label="Type d'action"
        sortable
      >
        <template slot-scope="scope">
          {{ getActionType(scope.row.type) }}
        </template>
      </el-table-column>
      <el-table-column
        prop="participants"
        label="Participants"
        sortable
      >
        <template slot-scope="scope">
          <el-popover
            placement="top-start"
            :title="participantsToTitle(scope.row.participants.length)"
            width="200"
            trigger="hover"
            :content="participantsToContent(scope.row.participants)"
          >
            <p slot="reference">
              {{ participantsToTitle(scope.row.participants.length) }}
            </p>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column
        prop="appointments"
        label="Nombre de RDV issus"
        sortable
      />
      <el-table-column
        prop="studies"
        label="Nombre d'études issues"
        sortable
      />
    </el-table>
  </BaseComponent>
</template>

<script>

const axios = require("axios")

export default {
  name: "ActionCommerciale",
  data () {
    return {
      breadcrumb: [
        {
          name: "Lister des actions commerciales",
          link: "/prospects/actionCommerciale/"
        }
      ],
      loading: false,
      onlyFuture: false,
      displayedData: [],
      // Tableaux de valeurs, générés au chargement de la page
      actionsComs: [],
      actionComsFuture: [],
      membres: [],
      typesActions: []
    }
  },
  created () {
    axios.get(
      "/api/actioncom",
      {withCredentials: true}
    ).then((res) => {
      res.data.forEach((elt) => elt.value = elt.name)
      this.actionsComs = res.data
      this.actionComsFuture = Array.from(res.data).filter(ac => {
        const tokens = ac.date.split("-")
        return Date.parse(new Date(tokens[1]+" "+tokens[2]+" "+tokens[0])) >= Date.now()
      })
      this.updateData()
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer la liste des actions commerciales : " + err,
        type: "error",
        offset: 40})
    })
    axios.get(
      "/api/actioncom/types",
      {withCredentials: true}
    ).then((res) => {
      this.typesActions = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer la liste des prospects : " + err,
        type: "error",
        offset: 40})
    })
    axios.get(
      "/api/membres/",
      {withCredentials: true}
    ).then((res) => {
      this.membres = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer la liste des membres : " + err,
        type: "error",
        offset: 40})
    })
  },
  methods: {
    getActionType (id) {
      const at = this.typesActions.find(a => a.id === id)
      return at == undefined ? "<ERROR>" : at.type
    },
    colorRow ({row}) {
      const todayDate = Date.now()
      const tokens = row.date.split("-")
      const actionDate = Date.parse(new Date(tokens[1]+" "+tokens[2]+" "+tokens[0]))
      const twoDays = 1000*60*60*24 * 2
      if(actionDate < todayDate) {
        return "old-row"
      } else if ((actionDate - todayDate - twoDays) < 0) {
        return "almost-row"
      } else {
        return "future-row"
      }
    },
    updateData () {
      if(this.onlyFuture)
        this.displayedData = this.actionComsFuture
      else
        this.displayedData = this.actionsComs
    },
    rowClicked (a) {
      this.$router.push("/prospects/actionCommerciale/"+a.id+"/voir")
    },
    participantsToTitle (size) {
      return size + " participant" + (size > 1 ? "s":"")
    },
    participantsToContent (array) {
      var str = ""
      array.forEach(p => {
        if(str !== "")
          str += ", "
        str += this.getMembre(p)
      })
      return str
    },
    getMembre (id) {
      const mb = this.membres.find(m => m.id === id)
      return mb == undefined ? "<ERROR>" : mb.firstname + " " + mb.lastname
    }
  }
}
</script>

<style>
  /* Ligne où la date est dépassée. Teinte grisée */
  .el-table .old-row {
    background: rgba(75, 73, 72, .25);
  }
  .el-table .old-row:hover {
    background: rgba(196, 194, 192, .25);
  }
  /* Ligne où la date est dans 2 jours. Teinte orangée */
  .el-table .almost-row {
    background: rgba(167, 139, 14, .25);
  }
  .el-table .almost-row:hover {
    background: rgba(240, 200, 21, .25);
  }
  /* Ligne où la date est dans plus de 2 jours. Teinte bleue/verte */
  .el-table .future-row {
    background: rgba(94, 155, 155, .25);
  }
  .el-table .future-row:hover {
    background: rgba(151, 247, 247, .25);
  }
  /* style tu texte à gauche du slider */
  .labelSlide {
    font-size: 1.01em;
  }
</style>
