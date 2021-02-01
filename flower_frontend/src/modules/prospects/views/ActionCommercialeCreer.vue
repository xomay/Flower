<template>
  <BaseComponent
    title="Création d'action commerciale"
    :breadcrumb="breadcrumb"
  >
    <h1 class="text-xl">
      Action commerciale
    </h1>
    <el-form
      ref="acForm"
      :model="actionCommerciale"
      label-position="left"
      size="small"
    >
      <el-row>
        <el-col :span="10">
          <el-form-item
            label="Nom de l'action :"
            prop="name"
            label-width="10vw"
            :rules="[{ required: true, message: 'Obligatoire' , trigger: 'blur' }]"
          >
            <el-input
              v-model="actionCommerciale.name"
              placeholder="Nom de l'action commerciale"
            />
          </el-form-item>
        </el-col>
        <el-col
          :span="12"
          :offset="2"
        >
          <el-form-item
            label="Type d'action :"
            prop="type"
            label-width="10vw"
            :rules="[{ required: true, message: 'Obligatoire' , trigger: 'blur' }]"
          >
            <MemberPicker
              v-model="actionCommerciale.type"
              :item-list="typesAction"
              placeholder="Type d'action"
              :style="'width: 100%'"
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="8">
          <el-form-item
            label="Date :"
            prop="date"
            label-width="10vw"
            :rules="[{ required: true, message: 'Obligatoire' , trigger: 'blur' }]"
          >
            <el-date-picker
              v-model="actionCommerciale.date"
              format="dd-MM-yyyy"
              value-format="yyyy-MM-dd"
              type="date"
              placeholder="Date de l'action"
              :first-day-of-week="1"
            />
          </el-form-item>
        </el-col>
      </el-row>
      <h1 class="text-xl">
        Participants :
      </h1>
      <el-row>
        <el-col :span="8">
          <MembersGroup
            v-model="actionCommerciale.participants"
            :item-list="members"
            @add-participant="addParticipant"
            @delete-participant="deleteParticipant"
          />
        </el-col>
      </el-row>
      <h1 class="text-xl">
        Autre :
      </h1>
      <el-form-item
        label="Consignes du BU :"
        prop="instructions"
        label-width="10vw"
        :rules="[{ required: true, message: 'Obligatoire' , trigger: 'blur' }]"
      >
        <el-input
          v-model="actionCommerciale.instructions"
          type="textarea"
          placeholder="Consignes supplémentaires"
        />
      </el-form-item>
    </el-form>
    <el-button
      :loading="loading"
      type="success"
      :style="{margin:'2vh 2vw 2vh 2vw'}"
      @click="validateAllFields"
    >
      Créer l'action commerciale
    </el-button>
  </BaseComponent>
</template>

<script>
import MemberPicker from "@/modules/membres/components/MemberPicker"
import MembersGroup from "@/modules/membres/components/MembersGroup"

const axios = require("axios")

export default {
  name: "ActionCommerciale",
  components: {MemberPicker, MembersGroup},
  data () {
    return {
      breadcrumb: [
        {
          name: "Lister des actions commerciales",
          link: "/prospects/actionCommerciale/"
        },
        {
          name: "Créer une action commerciale",
          link: "/prospects/actionCommerciale/ajouter"
        }
      ],
      loading: false,
      // Données exportées au final
      actionCommerciale: {
        type: "",
        name: "",
        date: "",
        participants: [],
        instructions: ""
      },
      // Fields pour stocker les données.
      typesAction: [],
      members: []
    }
  },
  created () {
    axios.get(
      "/api/membres",
      {withCredentials: true}
    ).then((res) => {
      res.data.forEach((elt) => elt.value = `${elt.firstname} ${elt.lastname}`)
      this.members = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer la liste des membres : " + err,
        type: "error",
        offset: 40})
    })
    axios.get(
      "/api/actioncom/types",
      {withCredentials: true}
    ).then((res) => {
      this.typesAction = res.data.map(d => {
        return {
          id: d.id,
          value: d.type
        }
      })
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer la liste des types d'actions : " + err,
        type: "error",
        offset: 40})
    })
  },
  mounted: function () {
    this.$nextTick(
      function () {
        // Sert à générer la première case de participant après le chargement de la page
        this.addParticipant()
      }
    )
  },
  methods: {
    validateAllFields () {
      var valid = true
      this.$refs.acForm.validate((r) => {
        if(!r) {
          this.$message({message: "Erreur : Ce devis présente des erreurs.", type: "error", offset: 40})
          valid = false
        }
      })

      if(this.actionCommerciale.participants.length < 1) {
        this.$message({message: "Erreur : Il faut ajouter au moins un participant.", type: "error", offset: 40})
        valid = false
      }
      for(var i = 0; i < this.actionCommerciale.participants.length; i++) {
        if(this.actionCommerciale.participants[i] < 1) {
          this.$message({message: `Erreur : Le participant [${i+1}] n'est pas défini.`, type: "error", offset: 40})
          valid = false
        }
      }
      // Les return ne quittent pas la fonction....
      if(valid) {
        this.sendForm()
      }
    },
    sendForm () {
      this.loading = true
      console.log(this.actionCommerciale)
      axios.post(
        "/api/actioncom/",
        this.actionCommerciale,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "L'action commerciale a bien été ajouté",
          type: "success"})
        this.$router.push("/prospects/actionCommerciale/")
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error"})
        }).
        finally(() => {
          this.loading = false
        })
    },
    addParticipant () {
      const newParticipant = - this.actionCommerciale.participants.length
      this.actionCommerciale.participants.push(newParticipant)
    },
    deleteParticipant (participantIndex) {
      this.actionCommerciale.participants.splice(
        participantIndex,
        1
      )
    }
  }
}
</script>