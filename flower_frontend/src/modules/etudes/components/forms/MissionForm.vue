<template>
  <div>
    <el-form
      v-for="(mission, index) in value"
      :key="index"
      ref="refFormMission"
      :model="mission"
      class="mb-4"
      label-position="left"
    >
      <el-row>
        <el-col :span="10">
          <el-form-item
            label="Consultant"
            prop="consultant"
            :rules="[{required: true, message: 'Champs obligatoire', trigger: 'blur'}]"
          >
            <MemberPicker
              v-model="mission.consultant"
              :item-list="members"
              placeholder="Membre de la JE"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-button
            type="danger"
            icon="el-icon-delete"
            :style="'margin-left: 5%'"
            @click="deleteMission(mission, index)"
          >
            Supprimer la mission
          </el-button>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item
            label="Date de début"
            prop="missionBegin"
            :rules="[{required: true, message: 'Date obligatoire', trigger: 'change'}]"
          >
            <el-date-picker
              v-model="mission.missionBegin"
              format="dd-MM-yyyy"
              value-format="yyyy-MM-dd"
              type="date"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item
            label="Date de fin"
            prop="missionEnd"
            :rules="[{required: true, message: 'Date obligatoire', trigger: 'change'}]"
          >
            <el-date-picker
              v-model="mission.missionEnd"
              format="dd/MM/yyyy"
              value-format="yyyy-MM-dd"
              type="date"
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="8">
          <el-form-item
            label="Pourcentage Junior"
            prop="percentageJunior"
            label-width="50%"
            :rows="1"
            :rules="[
              {required: true, message: 'Pourcentage obligatoire', trigger: 'blur'},
              {required: true, pattern: /^(1(|\.[0]+)|0\.[0-9]+)$/, message: 'Entrez une valeur entre 0 et 1.', trigger: 'change'}
            ]"
          >
            <el-input
              v-model="mission.percentageJunior"
              label="%"
            />
          </el-form-item>
        </el-col>
        <el-col
          :span="7"
          :offset="1"
        >
          <el-form-item
            label="Nombre de JEH"
            prop="JEHNumber"
            :rules="[
              {required: true, message: 'Valeur obligatoire', trigger: 'blur'},
              {required: true, pattern: /^[0-9]+$/, message: 'Entrez un nombre entier positif', trigger: 'change'}
            ]"
          >
            <el-input-number
              v-model="mission.JEHNumber"
              :min="0"
              :max="100"
              controls-position="right"
            />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item
            label="Prix d'un JEH"
            prop="JEHPrice"
            :rules="[{required: true, message: 'Valeur obligatoire', trigger: 'blur'}]"
          >
            <el-input-number
              v-model="mission.JEHPrice"
              :precision="2"
              :step="50"
              :min="50"
              :max="400"
              controls-position="right"
            />
          </el-form-item>
        </el-col>
        <el-col :span="24">
          <el-form-item
            label="Phases"
            prop="phases"
            :rules="[
              {required: true, message: 'Entrez au moins une phase.', trigger: 'blur'}
            ]"
          >
            <el-select
              v-model="mission.phases"
              class="w-full"
              multiple
              placeholder="Phases"
            >
              <el-option
                v-for="item in phases"
                :key="item.id"
                :label="item.title"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-divider />
    </el-form>
    <el-button
      :loading="loading"
      type="primary"
      @click="validateForm"
    >
      Enregistrer
    </el-button>
  </div>
</template>

<script>
import MemberPicker from "@/modules/membres/components/MemberPicker"

const axios = require("axios")

export default {
  name: "MissionForm",
  components: {MemberPicker},
  props: {
    value: { type: Array, required: true },
    loading: { type: Boolean, required: true },
    phases: { type: Array, required: true }
  },
  data () {
    return {
      members: []
    }
  },
  created () {
    this.getMembers()
  },
  methods: {
    getMembers () {
      axios.get(
        "/api/membres",
        {withCredentials: true}
      ).then((res) => {
        res.data.forEach((member) => member.value = `${member.firstname} ${member.lastname}`)
        this.members = res.data
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer les membres : "+err,
          type: "error",
          offset: 40})
      })
    },
    deleteMission (mission, index) {
      this.value.splice(index, 1)
      console.log("Deleted index " + index + " of mission " + mission)
      /*axios.delete(
        `/api/etudes/${this.$route.params.id}/missions/${mission.id}/`,
        {withCredentials: true}
      ).then(() => {
        this.value.splice(index, 1)
      }).catch((err) => {
        this.$message({message: "Impossible de supprimer la mission : "+err,
          type: "error",
          offset: 40})
      })*/
    },
    validateForm () {
      var result = this.$refs.refFormMission.length > 0
      for(const form of this.$refs.refFormMission) {
        form.validate((r) => {
          if(!r)
            result = false
        })
      }
      if(result) {
        //$emit('save')
      } else {
        this.$message({message: "Cerains champs sont invalides !", type: "error"})
      }
    }
  }
}
</script>
