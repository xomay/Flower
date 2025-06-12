<template>
  <div>
    <div
      v-for="(detail, index) in value"
      :key="index"
      class="my-4"
    >
      <el-form
        ref="nfsdetailform"
        :model="detail"
      >
        <el-row>
          <el-col :span="1">
            <el-button
              :loading="loading"
              type="text"
              icon="CaretTop"
              :disabled="index === 0"
              style="margin-left: 10px;"
              @click="exchangeBlocs(index, index-1)"
            />
            <el-button
              :loading="loading"
              type="text"
              icon="CaretBottom"
              :disabled="index === (value.length - 1)"
              @click="exchangeBlocs(index, index+1)"
            />
            <el-button
              :loading="loading"
              type="text"
              icon="Delete"
              style="color: red;"
              @click="deleteBloc(detail.id, index)"
            />
          </el-col>
          <el-col
            :span="8"
          >
            Description de la dépense :
            <el-form-item
              prop="description"
              style="margin-bottom: 30px;"
              :rules="[{ required: true, message: 'Obligatoire.', trigger: 'change'}]"
            >
              <el-input
                v-model="detail.description"
                placeholder="Description de la dépense."
                type="textarea"
                :rows="5"
              />
            </el-form-item>
          </el-col>
          <el-col
            :span="12"
            :offset="1"
          >
            <el-row>
              Type :
              <el-switch
                v-model="detail.detailType"
                active-text="Normale"
                active-value="N"
                active-color="#13ce6655"
                inactive-text="Kilométrique"
                inactive-value="K"
                inactive-color="#ff494955"
                style="margin-left: 20px; margin-top: -6px"
              />
            </el-row>
            <div v-show="detail.detailType == 'N'">
              <el-row>
                Montant H.T. :<br>
                <el-form-item
                  prop="prixHT"
                  :rules="[
                    { required: true, validator: numberValidator, trigger: 'change' },
                    { required: true, message: 'Obligtoire.', trigger: 'change' }
                  ]"
                >
                  <el-input
                    v-model="detail.prixHT"
                    placeholder="Prix HT"
                    style="width: 250px;"
                  >
                    <template slot="append">
                      €
                    </template>
                  </el-input>
                </el-form-item>
              </el-row>
              <el-row>
                TVA :<br>
                <el-form-item
                  prop="tva"
                  :rules="[
                    { required: true, validator: percentageValidator, trigger: 'change' },
                    { required: true, message: 'Obligtoire.', trigger: 'change' }
                  ]"
                >
                  <el-input
                    v-model="detail.tva"
                    placeholder="TVA"
                    style="width: 250px;"
                  />
                </el-form-item>
              </el-row>
            </div>
            <div v-show="detail.detailType == 'K'">
              <el-row>
                Nombre de kilomètres :<br>
                <el-form-item
                  prop="nbKilometres"
                  :rules="[
                    { required: true, validator: integerValidator, trigger: 'change' },
                    { required: true, message: 'Obligtoire.', trigger: 'change' }
                  ]"
                >
                  <el-input-number
                    v-model="detail.nbKilometres"
                    :min="0"
                    :max="99999"
                    controls-position="right"
                    style="width: 250px;"
                  >
                    <template slot="append">
                      km
                    </template>
                  </el-input-number>
                </el-form-item>
              </el-row>
              <el-row>
                Prix au kilomètre :<br>
                <el-input-number
                  v-model="detail.prixCentimesKilometres"
                  :min="0"
                  :max="100"
                  controls-position="right"
                  style="width: 250px;"
                  :rules="[
                    { required: true, validator: integerValidator, trigger: 'change' },
                    { required: true, message: 'Obligtoire.', trigger: 'change' }
                  ]"
                >
                  <template slot="append">
                    centimes
                  </template>
                </el-input-number>
              </el-row>
            </div>
          </el-col>
        </el-row>
      </el-form>
      <hr class="spitHR">
    </div>
    <div class="flex justify-center">
      <el-button
        :loading="loading"
        @click="addBloc"
      >
        Ajouter une dépense
      </el-button>
    </div>
  </div>
</template>

<script>
export default {
  name: "NFsDetailForm",
  props: {
    value: { type: Array, required: true },
    loading: { type: Boolean, required: true }
  },
  methods: {
    addBloc () {
      this.$emit("add-bloc")
    },
    exchangeBlocs (index1, index2) {
      if (index1 < 0 || index1 >= this.value.length || index2 < 0 || index2 >= this.value.length) {
        return
      }
      [
        this.value[index1].index,
        this.value[index2].index
      ] = [
        this.value[index2].index,
        this.value[index1].index
      ]
      this.value = this.value.sort((a, b) => a.index - b.index)
    },
    deleteBloc (blocId, blocIndex) {
      this.$emit("delete-bloc", blocId, blocIndex)
    },
    // validators
    numberValidator (rule, value, callback) {
      if ( ! String(value).match(/^-?\d+(|.\d+)$/g)) {
        callback(new Error("Nombre non valide"))
      } else {
        callback()
      }
    },
    percentageValidator (rule, value, callback) {
      if ( ! String(value).match(/^(1(|.0+)|0(|.\d+))$/g)) {
        callback(new Error("Pourcentage non valide"))
      } else {
        callback()
      }
    },
    integerValidator (rule, value, callback) {
      if ( ! String(value).match(/^\d+$/g)) {
        callback(new Error("Nombre non valide"))
      } else {
        callback()
      }
    }
  }
}
</script>

<style scoped>
  .spitHR {
    margin: 20px auto 30px auto;
    border-top: 2px solid rgba(150, 150, 150, 0.39);
  }
</style>
