<template>
  <BaseComponent
    title="Liste des membres"
    :breadcrumb="breadcrumb"
  >
    <template #action>
      <router-link to="/membres/ajouter">
        <el-button
          v-if="!isOnlyPious()"
          type="primary"
          icon="Plus"
          plain
          style="margin: 0 10px;"
        >
          Ajouter un membre
        </el-button>
      </router-link>
    </template>
    <el-row
      style="margin-left: 4%; margin-right: 4%"
    >
      <el-col
        style="align-content: center;"
      >
        <el-checkbox
          v-model="doesFilterPromo"
          class="marginL"
          @change="updateFilters"
        />
        <span class="marginL">
          Filtrer par promotion :
        </span>
        <el-input-number
          v-model="promotionFilterValue"
          class="marginL"
          controls-position="right"
          size="small"
          :disabled="!doesFilterPromo"
          @change="updateFilters"
        />
      </el-col>
      <el-col>
        <el-input
          v-model="nameFilterValue"
          style="width: 70%; height: 80%; margin-top: 10px;"
          size="large"
          placeholder="Entrez un nom"
          prefix-icon="Search"
          :disabled="!doesFilterName"
          @change="updateFilters"
          @input="updateFilters"
        />
      </el-col>
    </el-row>
    <el-tabs
      v-model="currentTab"
      type="card"
      style="margin-top: 20px; margin-bottom: 5px;"
    >
      <el-tab-pane
        label="Mandat en cours"
        name="mandat"
      />
      <el-tab-pane
        label="Tous les membres"
        name="all"
      />
    </el-tabs>
    <el-table
      v-loading="loading"
      class="grid"
      :data="currentSelected"
      :stripe="true"
    >
      <el-table-column
        prop="firstname"
        label="Membre"
        sortable
      >
        <template #default="{row}">
          <router-link :to="`/membres/${row.id}/voir`">
            <el-button
              type="text"
              size="small"
            >
              {{ row.fullname }}
            </el-button>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column
        prop="poste"
        label="Poste"
        sortable
      />
      <el-table-column
        prop="mobile"
        label="Mobile"
      />
      <el-table-column
        prop="email"
        label="Email"
      />
      <el-table-column
        prop="email_junior"
        label="Email Junior"
      />
    </el-table>
  </BaseComponent>
</template>

<script>
import { registerMemberMixin } from "../mixins/RegisterMember.js"
import { Permissions } from "@/mixins/Permissions"
import Utils from "@/mixins/Utils"
const axios = require("axios")

export default {
  name: "MembresVoir",
  mixins: [registerMemberMixin, Permissions, Utils],
  data () {
    return {
      membres: [],
      currentSelected: [],
      currentTab: "mandat",
      btnsDesactivated: [],
      promotionFilterValue: 2021,
      userFilterValue: false,
      nameFilterValue: "",
      doesFilterPromo: false,
      doesFilterUser: false,
      doesFilterName: true,
      loading: true,
      breadcrumb: [
        {
          name: "Liste des membres",
          link: "/membres"
        }
      ]
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      "/api/membres/",
      {withCredentials: true}
    ).then((res) => {
      res.data.forEach((elt) => elt.fullname = this.nicePeople(elt))
      res.data.forEach((elt) => elt.poste = this.displayPoste(elt))
      this.membres = res.data
      this.currentSelected = this.membres
      this.updateFilters()
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les membres pour le moment : " + err, type: "error"})
    }).finally(() => {
      this.loading = false
    })
  },
  watch: {
    currentTab () {
      this.updateFilters()
    },
  },
  methods: {
    refilterUser (displayWithUser) {
      if(displayWithUser)
        this.currentSelected = this.currentSelected.filter(m => m.user != undefined)
      else
        this.currentSelected = this.currentSelected.filter(m => m.user == undefined)
    },
    filterWithPromotion (promotion) {
      this.currentSelected = this.currentSelected.filter(m => m.promotion === promotion)
    },
    filterWithNameOrPoste (name) {
      this.currentSelected = this.currentSelected.filter(m => m.fullname.toLowerCase().includes(name.toLowerCase()) || m.poste.toLowerCase().includes(name.toLowerCase()))
    },
    updateFilters () {
      if(this.currentTab === "mandat") {
        this.currentSelected = this.membres.filter(m => m.is_active)
      } else {
        this.currentSelected = this.membres
      }
      if(this.doesFilterName) {
        this.filterWithNameOrPoste(this.nameFilterValue)
      }
      if(this.doesFilterPromo) {
        this.filterWithPromotion(this.promotionFilterValue)
      }
      if(this.doesFilterUser) {
        this.refilterUser(this.userFilterValue)
      }
    }
  }
}
</script>

<style scoped>
  .el-col {
    border-radius: 4px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
  .filtresDiv {
    width: 95%;
    height: 8vh;
    border: 1px solid black;
    margin: 1em;
  }
  .marginL {
    margin-left: 12px;
    margin-top: 5px;
  }
</style>
