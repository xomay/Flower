<template>
  <BaseComponent
    title="Ajouter un commentaire"
    :breadcrumb="breadcrumb"
  >
    <el-form
      ref="devisNC"
      :model="comment"
      label-position="left"
      size="small"
    >
      <el-col :span="24">
        <el-form-item
          label="Commentaire"
          prop="content"
          :rules="[{required: true, message: 'Obligatoire', trigger: 'blur'}]"
        >
          <el-input
            v-model="comment.content"
            type="textarea"
            :autosize="{ minRows: 2, maxRows: 8}"
            placeholder="Entrez un commentaire."
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Note :"
          prop="rating"
          :rules="[{required: true, validator: checkRate, trigger: 'change'}]"
        >
          <el-rate
            v-model="comment.rating"
            :max="10"
            :low-threshold="3.33"
            :high-threshold="6.66"
            :colors="['#ff1111', '#ffa200', '#62da05']"
            show-score
            text-color="#000000"
            :score-template="getDisplayNote()"
            style="margin-top: 7px"
          />
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item
          label="Date :"
          prop="date"
          :rules="[{required: true, message: 'Obligatoire', trigger: 'change'}]"
        >
          <el-date-picker
            v-model="comment.date"
            placeholder="Choisissez un jour"
            format="DD-MM-YYYY"
            value-format="YYYY-MM-DD"
            type="date"
            :first-day-of-week="1"
          />
        </el-form-item>
      </el-col>
    </el-form>
    <el-button
      :loading="loading"
      type="success"
      icon="Check"
      @click="validateForm()"
    >
      Sauvegarder le commentaire
    </el-button>
  </BaseComponent>
</template>

<script>
const axios = require("axios")
export default {
  name: "NewComment",
  data () {
    return {
      etude: {},
      realisateur: {},
      loading: false,
      comment: {
        content: "",
        rating: -1,
        associatedEtude: this.$route.params.id,
        date: ""
      },
      breadcrumb: [
        {
          name: "Suivi d'Etude",
          link: "/etudes"
        },
        {
          name: "<loading>",
          link: `/etudes/${this.$route.params.id}/voir/`
        },
        {
          name: "Ajouter un commentaire",
          link: `/etudes/${this.$route.params.id}/commentaires/${this.$route.params.realisateur_id}/ajouter`
        }
      ]
    }
  },
  created () {
    this.loading = true
    axios.get(
      `/api/etudes/${this.$route.params.id}/`,
      {withCredentials: true}
    ).then((res) => {
      this.etude = res.data
      this.breadcrumb[1].name = res.data.name
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer l'étude pour le moment: "+err, type: "error"})
    }).finally(() => {
      this.loading = false
    })
    axios.get(
      `/api/realisateurs/${this.$route.params.realisateur_id}/`,
      {withCredentials: true}
    ).then((res) => {
      this.realisateur = res.data
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer le réalisateur pour le moment: "+err, type: "error"})
    }).finally(() => {
      this.loading = false
    })
  },
  methods: {
    checkRate (rule, value, callback) {
      if (value == -1) {
        callback(new Error("Note obligatoire"))
      } else {
        callback()
      }
    },
    getDisplayNote () {
      return this.comment.rating == -1 ? "" : "{value} / 10"
    },
    validateForm () {
      this.$refs.devisNC.validate((r) => {
        if(r) {
          this.saveComment()
        } else {
          this.$message({message: "Le formulaire présente des erreurs.", type: "error"})
        }
      })
    },
    saveComment () {
      this.loading = true
      axios.post(
        "/api/realisateurs/cmts/",
        this.comment,
        { withCredentials: true }
      ).then((res) => {
        const newID = res.data.id
        this.realisateur.comments.push(newID)
        axios.put(
          `/api/realisateurs/${this.$route.params.realisateur_id}/`,
          this.realisateur,
          { withCredentials: true }
        ).then(() => {
          this.$message({message: "Commentaire sauvegardé avec succès.", type: "success"})
          this.$router.push(`/etudes/${this.$route.params.id}/voir?active=Avancement`)
        }).catch(() => {
          this.$message({message: "Il y a déjà un commentaire pour ce réa et cette étude ! ", type: "error"})
          axios.delete(
            `/api/realisateurs/cmts/${newID}/`,
            { withCredentials: true }
          ).then(() => {
            this.$message({message: "Action annulée. ", type: "warning"})
          }).catch((err) => {
            this.$message({message: "Impossible de supprimer le commentaire : " +err, type: "error"})
          }).finally(() => {
            this.$router.push(`/etudes/${this.$route.params.id}/voir?active=Avancement`)
          })
        })
      }).catch((err) => {
        this.$message({message: "Impossible de sauvegarder le commentaire : " +err, type: "error"})
        this.loading = false
      })
    }
  }
}
</script>