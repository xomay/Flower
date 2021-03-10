<template>
  <BaseComponent
    title="Liste des membres"
    :breadcrumb="breadcrumb"
  >
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
          :min="2010"
          :max="2100"
          size="mini"
          :disabled="!doesFilterPromo"
          @change="updateFilters"
        />
      </el-col>
      <el-col
        v-if="isAdmin()"
      >
        <el-checkbox
          v-model="doesFilterUser"
          class="marginL"
          @change="updateFilters"
        />
        <span class="marginL">
          Filtrer par compte :
        </span>
        <el-switch
          v-model="userFilterValue"
          style="margin-left: 10px; margin-top: -2px;"
          active-text="Avec compte"
          inactive-text="Sans compte"
          :disabled="!doesFilterUser"
          @change="updateFilters"
        />
      </el-col>
      <el-col>
        <el-checkbox
          v-model="doesFilterName"
          class="marginL"
          @change="updateFilters"
        />
        <span class="marginL">
          Filtrer par nom :
        </span>
        <el-input
          v-model="nameFilterValue"
          style="width: 40%; height: 80%"
          size="mini"
          placeholder="Entrez un nom"
          prefix-icon="el-icon-search"
          :disabled="!doesFilterName"
          @change="updateFilters"
          @input="updateFilters"
        />
      </el-col>
    </el-row>
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
        <template slot-scope="scope">
          <router-link :to="`/membres/${scope.row.id}/voir`">
            <el-button
              type="text"
              size="small"
            >
              {{ scope.row.fullname }}
            </el-button>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column
        prop="promotion"
        label="Promotion"
        sortable
      />
      <el-table-column
        prop="poste"
        label="Poste"
        sortable
      />
      <el-table-column
        prop="email"
        label="Email"
        sortable
      />
      <el-table-column
        prop="email_junior"
        label="Email Junior"
        sortable
      />
      <el-table-column
        v-if="isAdmin()"
        style="width: 80%"
        label="Créer un compte"
      >
        <template
          slot-scope="scope"
        >
          <el-button
            v-show="isButtonOn(scope.$index)"
            ref="btn_{{scope.$index}}"
            size="medium"
            type="warning"
            @click="openAccount(scope.$index)"
          >
            Ouvrir un compte utilisateur
          </el-button>
          <el-col v-show="!isButtonOn(scope.$index)">
            <div class="grid-content bg-purple-light" />
          </el-col>
        </template>
      </el-table-column>
    </el-table>
  </BaseComponent>
</template>

<script>
import { registerMemberMixin } from "../mixins/RegisterMember.js"
import { Permissions } from "@/mixins/Permissions"
const axios = require("axios")

export default {
  name: "MembresVoir",
  mixins: [registerMemberMixin, Permissions],
  data () {
    return {
      membres: [],
      currentSelected: [],
      btnsDesactivated: [],
      promotionFilterValue: 2021,
      userFilterValue: false,
      nameFilterValue: "",
      doesFilterPromo: false,
      doesFilterUser: false,
      doesFilterName: false,
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
      res.data.forEach((elt) => elt.fullname = `${elt.firstname} ${elt.lastname}`)
      res.data.forEach((elt) => elt.poste = (elt.poste == undefined ? undefined : (elt.gender == "M." ? elt.poste.name : elt.poste.name_feminine)))
      this.membres = res.data
      this.currentSelected = this.membres
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les membres pour le moment : " + err, type: "error"})
    }).finally(() => {
      this.loading = false
    })
  },
  methods: {
    openAccount (memberID) {
      if(this.isAdmin()) {
        if( ! this.membres[memberID].user ) {
          this.mixinRegisterMember(axios, this.membres[memberID])
        } else {
          this.$message({ message: "Une erreur est survenue : le compte était déjà présent.", type: "error" })
        }
      } else {
        this.$message({ message: "Il faut être administrateur pour faire cette action !", type: "error" })
      }
    },
    isButtonOn (memberID) {
      return ! this.membres[memberID].user
    },
    refilterUser (displayWithUser) {
      if(displayWithUser)
        this.currentSelected = this.currentSelected.filter(m => m.user != undefined)
      else
        this.currentSelected = this.currentSelected.filter(m => m.user == undefined)
    },
    filterWithPromotion (promotion) {
      this.currentSelected = this.currentSelected.filter(m => m.promotion === promotion)
    },
    filterWithName (name) {
      this.currentSelected = this.currentSelected.filter(m => m.fullname.toLowerCase().includes(name.toLowerCase()))
    },
    updateFilters () {
      this.currentSelected = this.membres
      if(this.doesFilterName) {
        console.log(this.nameFilterValue)
        this.filterWithName(this.nameFilterValue)
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
  .bg-purple-light {
    background: #e5e9f2;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
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
