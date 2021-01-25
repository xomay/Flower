<template>
  <BaseComponent
    title="Prospection"
    :loading="loading"
    :breadcrumb="breadcrumb"
  >
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
    <!--<el-table
      v-loading="loading"
      class="grid"
      :style="{margin:'1vh auto 2vh 1vw'}"
      :data="prospects"
      :stripe="true"
    >
      <el-table-column
        prop="name"
        label="Nom"
        sortable
      >
        <template slot-scope="scope">
          <router-link :to="'/prospects/' + scope.row.id + '/voir'">
            <el-button
              type="text"
              size="small"
            >
              {{ scope.row.name }}
            </el-button>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column
        prop="town"
        label="Ville"
        sortable
      />
    </el-table>-->
    <div class="rowStyle">
      <DragZone
        list-id="NC"
        :content="prospectsNouveaux"
        title="Nouveaux prospects"
        @dropped="acceptDrop"
      />
      <DragZone
        list-id="AR"
        :content="prospectToRelancer"
        title="Prospects à relancer"
        @dropped="acceptDrop"
      />
      <DragZone
        list-id="RDV"
        :content="prospectWithRDV"
        title="Devis à envoyer / Rendez-vous obtenu"
        @dropped="acceptDrop"
      />
    </div>
  </BaseComponent>
</template>

<script>
import DragZone from "../components/DragAndDrop/DragZone"

const axios = require("axios")

export default {
  name: "ProspectsVoir",
  components: {DragZone},
  data () {
    return {
      prospects: [],
      items: [],
      loading: true,
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
      finally(() => {
        this.loading = false
      })
  },
  methods: {
    acceptDrop (itemID, listID) {
      const item = this.items.find(item => item.id == itemID)
      item.list = listID

      const prospect = this.prospects.find(i => i.id == itemID)
      if(listID != prospect.advancement) { // Pas de call d'API si on ne change rien :D
        prospect.advancement = listID
        this.updateProspect(prospect)
      }
    },
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
    calculateItems () {
      for (const pr of this.prospects) {
        this.items.push({
          id: pr.id,
          prospect: pr,
          list: pr.advancement
        })
      }
    }
  }
}
</script>
