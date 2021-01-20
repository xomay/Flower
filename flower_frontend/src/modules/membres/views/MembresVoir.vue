<template>
  <BaseComponent
    title="Liste des membres"
    :breadcrumb="breadcrumb"
  >
    <el-table
      v-loading="loading"
      class="grid"
      :data="membres"
      :stripe="true"
    >
      <el-table-column
        prop="firstname"
        label="Prénom"
        sortable
      >
        <template slot-scope="scope">
          <router-link :to="`/membres/${scope.row.id}/voir`">
            <el-button
              type="text"
              size="small"
            >
              {{ scope.row.firstname }}
            </el-button>
          </router-link>
        </template>
      </el-table-column>
      <el-table-column
        prop="lastname"
        label="Nom"
        sortable
      />
      <el-table-column
        prop="promotion"
        label="Promotion"
        sortable
      />
      <el-table-column
        style="width: 80%"
        label="Créer un compte"
      >
        <template
          slot-scope="scope"
        >
          <el-button
            v-if="isButtonOn(scope.$index)"
            ref="btn_{{scope.$index}}"
            size="medium"
            type="warning"
            @click="openAccount(scope.$index)"
          >
            Ouvrir un compte utilisateur
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </BaseComponent>
</template>

<script>
import { registerMemberMixin } from "../mixins/RegisterMember.js"
const axios = require("axios")

export default {
  name: "MembresVoir",
  mixins: [registerMemberMixin],
  data () {
    return {
      membres: [],
      btnsDesactivated: [],
      loading: true,
      breadcrumb: [
        {
          name: "Lister des membres",
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
      this.membres = res.data
    }).
      catch(() => {
        this.$message({message: "Impossible de récupérer les membres pour le moment",
          type: "error",
          offset: 40})
      }).
      finally(() => {
        this.loading = false
      })
  },
  methods: {
    display (scope) {
      console.log(scope)
    },
    openAccount (memberID) {
      this.$refs.ref
      if( ! this.membres[memberID].user ) {
        this.mixinRegisterMember(axios, this.membres[memberID])
      } else {
        this.$message({
          message: "Une erreur est survenue : le compte était déjà présent.",
          type: "error",
          offset: 40
        })
      }
    },
    isButtonOn (memberID) {
      return ! this.membres[memberID].user
    }
  }
}
</script>
