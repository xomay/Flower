<template>
  <BaseComponent
    title="Création d'action commerciale"
    :breadcrumb="breadcrumb"
  >
    <h1 class="text-xl">
      Action commerciale
    </h1>
    <el-form
      ref="devisForm1"
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
            <el-select v-model="actionCommerciale.type">
              <el-option value="Linked In">
                Linked In
              </el-option>
              <el-option value="Salon">
                Salon
              </el-option>
              <el-option value="Téléphone">
                Téléphone
              </el-option>
              <el-option value="Mailing">
                Mailing
              </el-option>
            </el-select>
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
      <el-row>
        <el-col :span="8">
          <el-form-item
            label="Prospect cible :"
            prop="prospect"
            label-width="10vw"
            :rules="[{ required: true, message: 'Obligatoire' , trigger: 'change' }]"
          >
            <MemberPicker
              v-model="actionCommerciale.prospect"
              :item-list="prospects"
              placeholder="Nom du prospect"
              :style="{width:'100%'}"
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
        prop="consignes"
        label-width="10vw"
        :rules="[{ required: true, message: 'Obligatoire' , trigger: 'blur' }]"
      >
        <el-input
          v-model="actionCommerciale.consignes"
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
      breadcrumb: [],
      loading: false,
      // Données exportées au final
      actionCommerciale: {
        type: "",
        name: "",
        date: "",
        prospect: "",
        participants: [],
        consignes: ""
      },
      // Fields pour stocker les données.
      prospects: [],
      members: []
    }
  },
  created () {
    axios.get(
      "/api/prospects",
      {withCredentials: true}
    ).then((res) => {
      res.data.forEach((elt) => elt.value = elt.name)
      this.prospects = res.data
    }).
      catch((err) => {
        console.log(err)
        this.$message({message: "Impossible de récupérer la liste des prospects.",
          type: "error",
          offset: 40})
      })
    axios.get(
      "/api/membres",
      {withCredentials: true}
    ).then((res) => {
      res.data.forEach((elt) => elt.value = `${elt.firstname} ${elt.lastname}`)
      this.members = res.data
    }).
      catch((err) => {
        console.log(err)
        this.$message({message: "Impossible de récupérer la liste des membres.",
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
      console.log("====> ["+this.actionCommerciale.participants+"]")
    },
    addParticipant () {
      const newParticipant = {
        idMembre: NaN,
        display: "",
        arrayIndex: this.actionCommerciale.participants.length
      }
      this.actionCommerciale.participants.push(newParticipant)
      console.log("Group added ("+newParticipant.arrayIndex+")")
    },
    deleteParticipant (participantIndex) {
      console.log("Delete id="+participantIndex)
      this.actionCommerciale.participants.splice(
        participantIndex,
        1
      )
    },
  }
}
</script>