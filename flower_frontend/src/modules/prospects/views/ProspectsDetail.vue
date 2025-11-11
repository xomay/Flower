<template>
  <div>
    <BaseComponent
      :title="titleProspect"
      :breadcrumb="breadcrumb"
    >
      <template v-slot:action>
        <router-link :to="`/prospects/${$route.params.id}/modifier`">
          <el-button
            type="text"
            icon="Edit"
          >
            Modifier
          </el-button>
        </router-link>
      </template>
      <ProspectsView
        :prospect="prospect"
        @updated-prospect="prospect = $event"
      />
    </BaseComponent>
    <BaseComponent
      title="Employés"
      :breadcrumb="[]"
    >
      <template v-slot:action>
        <router-link :to="`/prospects/${$route.params.id}/employes/ajouter`">
          <el-button
            type="text"
            icon="Plus"
          >
            Ajouter
          </el-button>
        </router-link>
      </template>
      <el-table
        class="grid"
        :data="employes"
        :stripe="true"
      >
        <el-table-column
          label="Nom"
          prop="firstname"
          sortable
        >
          <template #default="{ row }">
            <router-link :to="`/prospects/${$route.params.id}/employes/${row.id}/voir`">
              <el-button
                type="text"
                size="small"
              >
                {{ row.firstname }} {{ row.lastname }}
              </el-button>
            </router-link>
          </template>
        </el-table-column>
        <el-table-column
          label="Poste"
          prop="position"
          sortable
        />
        <el-table-column
          label="Email"
          prop="email"
          sortable
        />
        <el-table-column
          label="Mobile"
          prop="mobile"
          sortable
        />
      </el-table>
    </BaseComponent>
  </div>
</template>

<script>
import ProspectsView from "../components/ProspectsView"
const axios = require("axios")

export default {
  name: "ProspectsDetail",
  components: {ProspectsView},
  data () {
    return {
      prospect: {},
      employes: [],
      loading: false,
      titleProspect: "<loading>",
      breadcrumb: [
        {
          name: "Lister des prospects",
          link: "/prospects"
        },
        {
          name: "<loading>",
          link: "/prospects/ajouter"
        }
      ]
    }
  },
  created () {
    this.getProspect()
    this.getEmployes()
  },
  methods: {
    getProspect () {
      axios.get(
        `/api/prospects/${this.$route.params.id}/`,
        {withCredentials: true}
      ).then((res) => {
        this.prospect = res.data
        this.breadcrumb[1].name = this.prospect.name
        this.titleProspect = this.prospect.name
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer les prospects : "+err, type: "error"})
      })
    },
    getEmployes () {
      axios.get(
        `/api/prospects/${this.$route.params.id}/employes/`,
        {withCredentials: true}
      ).then((res) => {
        this.employes = res.data
      }).catch((err) => {
        this.$message({message: "Erreur lors de la récupération des employés : "+err, type: "error"})
      })
    }
  }
}
</script>
