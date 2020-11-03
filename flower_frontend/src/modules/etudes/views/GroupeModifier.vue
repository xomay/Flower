<!-- SHOULD NOT BE USED ANYMORE -->
<template>
  <BaseComponent
    title="Modifier les groupes"
    :breadcrumb="breadcrumb"
  >
    <el-card
      v-for="(groupe, index) in groupes"
      :key="index"
    >
      <div class="flex">
        <div class="mr-2">
          <el-button
            type="text"
            icon="el-icon-caret-top"
            @click="exchangeItems(index, index-1)"
          /><br>
          <el-button
            type="text"
            icon="el-icon-caret-bottom"
            @click="exchangeItems(index, index+1)"
          /><br>
          <el-button
            type="text"
            icon="el-icon-delete"
            @click="deleteGroupe(groupe.id, index)"
          />
        </div>
        <div class="flex-grow">
          <el-input
            v-model="groupe.title"
            placeholder="Nom du groupe"
          />
          <el-input
            v-model="groupe.description"
            placeholder="Description du groupe"
            type="textarea"
          />
        </div>
      </div>
    </el-card>
    <el-button @click="addGroupe">
      Ajouter un groupe
    </el-button>
    <el-button @click="submitGroupes">
      Enregister
    </el-button>
  </BaseComponent>
</template>

<script>
const axios = require("axios")

export default {
  name: "GroupeModifier",
  data () {
    return {
      loading: true,
      groupes: [],
      breadcrumb: []
    }
  },
  created () {
    this.loading = true
    axios.get(
      `${this.$server_url}/etudes/${this.$route.params.id}`,
      {withCredentials: true}
    ).then((res) => {
      this.groupes = res.data.groupes.sort((a, b) => a.index - b.index)
      this.breadcrumb = [
        {
          name: "Suivi d'Etude",
          link: "/etudes"
        },
        {
          name: res.data.name,
          link: `/etudes/${this.$route.params.id}/voir`
        },
        {
          name: "Groupes",
          link: `/etudes/${this.$route.params.id}/groupes`
        }
      ]
    }).
      catch(() => {
        this.$message({message: "Impossible de récupérer l'études pour le moment",
          type: "error"})
      }).
      finally(() => {
        this.loading = false
      })
  },
  methods: {
    addGroupe () {
      const newGroup = {
        title: "Titre",
        description: "Description",
        project: this.$route.params.id,
        index: this.groupes.length + 1
      }
      axios.post(
        `${this.$server_url}/etudes/groupes/`,
        newGroup,
        {withCredentials: true}
      ).then((res) => {
        this.$message({message: "Le groupe a bien été créé",
          type: "success"})
        this.groupes.push(res.data)
      }).
        catch(() => {
          this.$message({message: "Impossible de créer un groupe pour le moment",
            type: "error"})
        }).
        finally(() => {
          this.loading = false
        })
    },
    submitGroupes () {
      axios.put(
        `${this.$server_url}/etudes/groupes/`,
        this.groupes,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Les groupes ont bien été enregistrés",
          type: "success"})
      }).
        catch(() => {
          this.$message({message: "Impossible d'enregistrer les groupes pour le moment",
            type: "error"})
        }).
        finally(() => {
          this.loading = false
        })
    },
    deleteGroupe (groupeId, groupeIndex) {
      axios.delete(
        `${this.$server_url}/etudes/groupes/${groupeId}/`,
        {withCredentials: true}
      ).then(() => {
        this.groupes.splice(
          groupeIndex,
          1
        )
        this.$message({message: "Le groupe a bien été supprimé",
          type: "success"})
      }).
        catch(() => {
          this.$message({message: "Impossible de supprimer cette phase pour le moment",
            type: "error"})
        })
    },
    exchangeItems (index1, index2) {
      if (index1 < 0 || index1 >= this.groupes.length || index2 < 0 || index2 >= this.groupes.length) {
        return
      }
      [
        this.groupes[index1].index,
        this.groupes[index2].index
      ] = [
        this.groupes[index2].index,
        this.groupes[index1].index
      ]
      this.groupes = this.groupes.sort((a, b) => a.index - b.index)
    }
  }
}
</script>

<style>

</style>
