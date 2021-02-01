<template>
  <el-form
    ref="acForm"
    :model="value"
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
            v-model="value.name"
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
          :rules="[{ required: true, message: 'Obligatoire' , trigger: 'change' }]"
        >
          <MemberPicker
            v-model="value.type"
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
            v-model="value.date"
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
          v-model="value.participants"
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
        v-model="value.instructions"
        type="textarea"
        placeholder="Consignes supplémentaires"
      />
    </el-form-item>
    <el-col :span="24">
      <el-form-item>
        <el-button
          :loading="loading || localLoading"
          type="success"
          @click="validateAllFields"
        >
          Enregistrer
        </el-button>
      </el-form-item>
      <el-form-item v-if="deletable">
        <el-button
          :loading="loading || localLoading"
          type="danger"
          @click="$emit('delete')"
        >
          Supprimer
        </el-button>
      </el-form-item>
    </el-col>
  </el-form>
</template>

<script>
import MemberPicker from "@/modules/membres/components/MemberPicker"
import MembersGroup from "@/modules/membres/components/MembersGroup"

const axios = require("axios")

export default {
  name: "ACForm",
  components: {MemberPicker, MembersGroup},
  props: {
    value: { type: undefined, required: true },
    loading: Boolean,
    deletable: Boolean
  },
  data () {
    return {
      // Fields pour stocker les données.
      typesAction: [],
      members: [],
      localLoading: false
    }
  },
  created () {
    this.localLoading = true
    axios.get(
      "/api/membres",
      {withCredentials: true}
    ).then((res) => {
      this.members = res.data.map(elt => ({...elt, value: `${elt.firstname} ${elt.lastname}`}))
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
    }).finally(() => {
      this.localLoading = false
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

      if(this.value.participants.length < 1) {
        this.$message({message: "Erreur : Il faut ajouter au moins un participant.", type: "error", offset: 40})
        valid = false
      }
      for(var i = 0; i < this.value.participants.length; i++) {
        if(this.value.participants[i] < 1) {
          this.$message({message: `Erreur : Le participant [${i+1}] n'est pas défini.`, type: "error", offset: 40})
          valid = false
        }
      }
      // Les return ne quittent pas la fonction....
      if(valid) {
        this.$emit("save")
      }
    },
    addParticipant () {
      if(this.value.participants != undefined) {
        const newParticipant = - this.value.participants.length
        this.value.participants.push(newParticipant)
      }
    },
    deleteParticipant (participantIndex) {
      this.value.participants.splice(
        participantIndex,
        1
      )
    }
  }
}
</script>
