<template>
  <div>
    <el-form
      v-for="(mission, index) in value"
      :key="index"
      :model="mission"
      class="mb-4"
    >
      <el-row>
        <el-col :span="24">
          <el-form-item label="Consultant">
            <MemberPicker
              v-model="mission.consultant"
              :item-list="members"
            />
            <el-button
              type="danger"
              icon="el-icon-delete"
              @click="deleteMission(mission, index)"
            >
              Supprimer la mission
            </el-button>
          </el-form-item>
        </el-col>
        <!-- <el-col :span="24">
                    <el-form-item label="Période">
                        <el-date-picker type="daterange" v-model="[mission.missionBegin, mission.missionBegin]"/>
                    </el-form-item>
                </el-col> -->
        <el-col :span="12">
          <el-form-item label="Date de début">
            <el-date-picker
              v-model="mission.missionBegin"
              format="dd-MM-yyyy"
              value-format="yyyy-MM-dd"
              type="date"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="Date de fin">
            <el-date-picker
              v-model="mission.missionEnd"
              format="dd-MM-yyyy"
              value-format="yyyy-MM-dd"
              type="date"
            />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="Pourcentage Junior">
            <el-input-number
              v-model="mission.percentageJunior"
              :precision="2"
              :step="1"
              :min="0"
              :max="100"
              controls-position="right"
            />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="Nombre de JEH">
            <el-input-number
              v-model="mission.JEHNumber"
              :min="0"
              :max="100"
              controls-position="right"
            />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="Prix d'un JEH">
            <el-input-number
              v-model="mission.JEHPrice"
              :precision="2"
              :step="1"
              :min="0"
              :max="400"
              controls-position="right"
            />
          </el-form-item>
        </el-col>
        <el-col :span="24">
          <el-form-item label="Phases">
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
      @click="$emit('save')"
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
    value: { type: Object, required: true },
    loading: { type: Boolean, required: true }
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
        `${this.$server_url}/membres`,
        {withCredentials: true}
      ).then((res) => {
        res.data.forEach((member) => member.value = `${member.firstname} ${member.lastname}`)
        this.members = res.data
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error",
            offset: 40})
        })
    },
    deleteMission (mission, index) {
      axios.delete(
        `${this.$server_url}/etudes/${this.$route.params.id}/missions/${mission.id}/`,
        {withCredentials: true}
      ).then(() => {
        this.value.splice(
          index,
          1
        )
      }).
        catch((err) => {
          console.error(err)
        })
    }
  }
}
</script>

<style>

</style>
