<template>
  <div>
    <BaseComponent
      title="Prospect"
      :breadcrumb="breadcrumb"
    >
      <template v-slot:action>
        <router-link :to="`/prospects/${$route.params.id}/modifier`">
          <el-button
            type="text"
            icon="el-icon-edit"
          >
            Modifier
          </el-button>
        </router-link>
      </template>
      <ProspectsView :prospect="prospect" />
    </BaseComponent>
    <BaseComponent title="Employés">
      <template v-slot:action>
        <router-link :to="`/prospects/${$route.params.id}/employes/ajouter`">
          <el-button
            type="text"
            icon="el-icon-plus"
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
          <template slot-scope="scope">
            <router-link :to="`/prospects/${$route.params.id}/employes/${scope.row.id}/voir`">
              <el-button
                type="text"
                size="small"
              >
                {{ scope.row.firstname }} {{ scope.row.lastname }}
              </el-button>
            </router-link>
          </template>
        </el-table-column>
        <el-table-column
          label="Poste"
          prop="position"
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
      breadcrumb: [
        {
          name: "Lister des prospects",
          link: "/prospects"
        },
        {
          name: "",
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
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error"})
        })
    },
    updateProspect () {
      this.loading = true
      axios.put(
        `/api/prospects/${this.$route.params.id}/`,
        this.prospect,
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
    getEmployes () {
      axios.get(
        `/api/prospects/${this.$route.params.id}/employes/`,
        {withCredentials: true}
      ).then((res) => {
        this.employes = res.data
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error"})
        })
    }
  }
}
</script>

<style>

</style>
