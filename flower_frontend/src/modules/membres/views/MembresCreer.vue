<template>
  <BaseComponent
    title="Ajout d'un membre"
    :breadcrumb="breadcrumb"
  >
    <!-- <el-form :model="form" :rules="formRules" label-position="left">
            <el-row :gutter="5">
                <el-col :span="12">
                    <el-form-item label="Prénom" prop="firstname" label-width="26%">
                        <el-input v-model="form.firstname"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="12">
                    <el-form-item label="Nom" prop="lastname" label-width="26%">
                        <el-input v-model="form.lastname"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="12">
                    <el-form-item label="Genre" prop="gender" label-width="26%">
                        <el-select v-model="form.gender">
                            <el-option value="M.">M.</el-option>
                            <el-option value="Mme.">Mme.</el-option>
                            <el-option value="">Non renseigné</el-option>
                        </el-select>
                    </el-form-item>
                </el-col>
                <el-col :span="12">
                    <el-form-item label="Promotion" prop="promotion" label-width="26%">
                        <el-input-number v-model="form.promotion" controls-position="right" :min="2020" :max="2050"></el-input-number>
                    </el-form-item>
                </el-col>
                <el-col :span="24">
                    <el-form-item label="Email INSA" prop="email" label-width="13%">
                        <el-input v-model="form.email"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="24">
                    <el-form-item label="Email Juniors" prop="email_junior" label-width="13%">
                        <el-input v-model="form.email_junior"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="24">
                    <el-form-item label="Mobile" prop="mobile" label-width="13%">
                        <el-input v-model="form.mobile"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="24">
                    <el-form-item label="Adresse" prop="address" label-width="13%">
                        <el-input v-model="form.address"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="8">
                    <el-form-item label="Code postal" prop="postcode" label-width="39%">
                        <el-input v-model="form.postcode"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="8">
                    <el-form-item label="Ville" prop="town" label-width="39%">
                        <el-input v-model="form.town"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="8">
                    <el-form-item label="Pays" prop="country" label-width="39%">
                        <el-input v-model="form.country"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="24">
                    <el-form-item label="Nationalité" prop="nationality" label-width="13%">
                        <el-input v-model="form.nationality"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="12">
                    <el-form-item label="Date de naissance" prop="birth_date" label-width="26%">
                        <el-date-picker
                            format="dd-MM-yyyy"
                            value-format="yyyy-MM-dd"
                            v-model="form.birth_date"
                            type="date"
                            placeholder="Date de naissance"
                            :firstDayOfWeek="1">
                        </el-date-picker>
                    </el-form-item>
                </el-col>
                <el-col :span="12">
                    <el-form-item label="Lieu de naissance" prop="birth_place" label-width="26%">
                        <el-input v-model="form.birth_place"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="24">
                    <el-form-item>
                        <el-button @click="registerMember" :loading="loading" type="success">Enregistrer</el-button>
                    </el-form-item>
                </el-col>
            </el-row>
        </el-form> -->
    <MemberForm
      v-model="form"
      :loading="loading"
      @save="registerMember"
    />
  </BaseComponent>
</template>

<script>
import MemberForm from "../components/MemberForm"

const axios = require("axios")

export default {
  name: "EtudeCreer",
  components: {MemberForm},
  data () {
    return {
      form: {
        firstname: "",
        lastname: "",
        gender: "",
        promotion: "2021",
        email: "",
        email_junior: "",
        mobile: "",
        address: "",
        postcode: "",
        town: "",
        country: "",
        nationality: "",
        birth_date: "",
        birth_place: ""
      },
      loading: false,
      breadcrumb: [
        {
          name: "Liste des membres",
          link: "/membres"
        },
        {
          name: "Ajouter un membre",
          link: "/membres/ajouter"
        }
      ]
    }
  },
  methods: {
    registerMember () {
      this.loading = true
      axios.post(
        `${this.$server_url}/membres/`,
        this.form,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: "Le membre a bien été ajouté",
          type: "success"})
        this.$router.push("/membres")
      }).
        catch((err) => {
          this.$message({message: err,
            type: "error"})
        }).
        finally(() => {
          this.loading = false
        })
    }
  }
}
</script>

<style>

</style>
