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
            :rules="[{required: true, message: 'Champs obligatoire', trigger: 'change'}]"
          >
            <MemberPicker
              v-model="mission.consultant"
              :item-list="consultants"
              placeholder="Consultant"
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
    <el-alert
      v-show="value.length == 0"
      title="Vous n'avez ajouté aucune RdM"
      type="warning"
      description="Apputez sur le bouton ci-dessus pour en ajouter."
      :closable="false"
      center
      effect="dark"
      show-icon
    />
    <el-button
      :loading="loading"
      type="success"
      @click="validateForm"
    >
      Enregistrer les missions
    </el-button>
  </div>
</template>

<script>
import MemberPicker from "@/modules/membres/components/MemberPicker"

export default {
  name: "MissionForm",
  components: {MemberPicker},
  props: {
    value: { type: Array, required: true },
    loading: { type: Boolean, required: true },
    phases: { type: Array, required: true },
    consultants: { type: Array, required: true }
  },
  data () {
    return {
      deletedMissions: []
    }
  },
  methods: {
    deleteMission (mission, index) {
      if(mission.id != undefined)
        this.deletedMissions.push(mission.id)
      this.value.splice(index, 1)
    },
    validateForm () {
      var result = true
      for(const form of this.$refs.refFormMission) {
        form.validate((r) => {
          if(!r)
            result = false
        })
      }

      if(result) {
        this.$emit("save", this.deletedMissions)
      } else {
        this.$message({message: "Certains champs sont invalides !", type: "error"})
      }
    },
    goBack () {
      this.$router.push(`/etudes/${this.$route.params.id}/voir?active=Rédaction`)
    }
  }
}
</script>
