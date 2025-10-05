<template>
  <BaseComponent
    title="Profil du réalisateur"
    :breadcrumb="breadcrumb"
  >
    <template v-slot:action>
      <el-button
        type="primary"
        icon="Edit"
        @click="$router.push(`/realisateurs/${$route.params.id}/modifier`)"
      >
        Modifier
      </el-button>
    </template>

    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="8" animated />
    </div>

    <div v-else-if="realisateur" class="profile-container">
      <!-- Header avec informations principales -->
      <el-card class="profile-header" shadow="hover">
        <div class="header-content">
          <div class="avatar-section">
            <el-avatar :size="80" :src="realisateur.avatar">
              {{ realisateur.firstname?.[0] }}{{ realisateur.lastname?.[0] }}
            </el-avatar>
            <el-tag 
              v-if="!(realisateur.ba && realisateur.security_social_number)"
              type="warning"
              class="status-tag"
            >
              Pool d'intervenants
            </el-tag>
            <el-tag 
              v-else
              type="success"
              class="status-tag"
            >
              Réalisateur actif
            </el-tag>
          </div>
          <div class="basic-info">
            <h2>{{ realisateur.gender }} {{ realisateur.firstname }} {{ realisateur.lastname }}</h2>
            <p class="promotion">{{ realisateur.filiere }} - Promotion {{ realisateur.promotion }}</p>
            <div class="rating-section">
              <StarRate 
                v-if="realisateur.rating >= 0"
                :model-value="realisateur.rating"
                :disabled="true"
              />
              <span v-else class="no-rating">Pas encore de notation</span>
            </div>
          </div>
          <div class="stats-section">
            <el-statistic title="Nombre d'études" :value="realisateur.etudesAmount" />
            <el-statistic 
              title="Note moyenne" 
              :value="realisateur.rating >= 0 ? realisateur.rating : 0" 
              suffix="/ 10"
              :precision="1"
            />
          </div>
        </div>
      </el-card>

      <!-- Corps principal avec deux colonnes -->
      <el-row :gutter="20" class="main-content">
        <!-- Colonne gauche - Informations détaillées -->
        <el-col :xs="24" :lg="12">
          <RealisateurView :realisateur="realisateur" />
          
          <!-- Section BA -->
          <el-card title="Bulletin d'adhésion" shadow="hover" class="ba-section">
            <div class="ba-content">
              <div class="ba-status">
                <el-icon class="ba-icon">
                  <Document />
                </el-icon>
                <div>
                  <p v-if="realisateur.ba" class="ba-text">
                    <strong>BA généré:</strong> {{ realisateur.ba }}
                  </p>
                  <p v-else class="ba-text">
                    <strong>BA:</strong> Non généré
                  </p>
                </div>
              </div>
              <el-button
                type="primary"
                :disabled="!(realisateur.address && realisateur.postcode && realisateur.town && realisateur.country)"
                @click="downloadBA()"
                :loading="downloading"
              >
                <el-icon><Download /></el-icon>
                Générer BA
              </el-button>
            </div>
            <el-alert
              v-if="!(realisateur.address && realisateur.postcode && realisateur.town && realisateur.country)"
              title="Informations manquantes"
              type="warning"
              description="L'adresse complète est requise pour générer le bulletin d'adhésion"
              show-icon
              :closable="false"
            />
          </el-card>
        </el-col>

        <!-- Colonne droite - Commentaires et évaluations -->
        <el-col :xs="24" :lg="12">
          <RealisateurCommentsView :realisateur="realisateur" />
        </el-col>
      </el-row>
    </div>
  </BaseComponent>
</template>

<script>
import RealisateurView from "../components/RealisateurView"
import RealisateurCommentsView from "../components/RealisateurCommentsView"
import StarRate from "../components/StarRate.vue"

const axios = require("axios")

export default {
  name: "RealisateursDetail",
  components: { RealisateurView, RealisateurCommentsView, StarRate },
  data () {
    return {
      realisateur: null,
      loading: true,
      downloading: false,
      breadcrumb: [
        {
          name: "Liste des réalisateurs",
          link: "/realisateurs"
        },
        {
          name: "Chargement...",
          link: `/realisateurs/${this.$route.params.id}/voir`
        }
      ]
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      `/api/realisateurs/${this.$route.params.id}`,
      {withCredentials: true}
    ).then((res) => {
      this.realisateur = res.data
      this.breadcrumb[1].name = `${this.realisateur.firstname} ${this.realisateur.lastname}`
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer le réalisateur pour le moment : " + err,
        type: "error",
        offset: 40})
    }).finally(() => {
      this.loading = false
    })
  },
  methods: {
    downloadBA () {
      axios.get(
        `/api/publish/barea/${this.realisateur.id}`,
        {withCredentials: true,
          responseType: "blob"}
      ).then((response) => {
        this.createDownloadElement(
          response.data,
          `BA-${this.realisateur.lastname}-${this.realisateur.firstname}.docx`
        )
      }).
        catch((err) => {
          this.$message({message: `Une erreur est survenue lors de la génération du bulletin d'adhésion : ${err}`,
            type: "error"})
        }).
        finally(() => {
          this.loading = false
        })
    },
    createDownloadElement (data, filename) {
      const fileURL = window.URL.createObjectURL(new Blob([data]))
      const fileLink = document.createElement("a")
      fileLink.href = fileURL
      fileLink.setAttribute("download", filename)
      document.body.appendChild(fileLink)
      fileLink.click()
      document.body.removeChild(fileLink)
      window.URL.revokeObjectURL(fileURL)
    }
  }
}
</script>

<style scoped>
.loading-container {
  padding: 20px;
}

.profile-container {
  max-width: 1400px;
  margin: 40px auto;
}

.profile-header {
  margin-bottom: 20px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  min-width: 120px;
}

.status-tag {
  font-size: 12px;
}

.basic-info {
  flex: 1;
  min-width: 250px;
}

.basic-info h2 {
  margin: 0 0 5px 0;
  color: #303133;
  font-size: 24px;
}

.promotion {
  margin: 0 0 10px 0;
  color: #606266;
  font-size: 16px;
}

.rating-section {
  margin-top: 10px;
}

.no-rating {
  color: #909399;
  font-style: italic;
}

.stats-section {
  display: flex;
  gap: 30px;
  align-items: center;
}

.main-content {
  margin-top: 20px;
}

.ba-section {
  margin-top: 20px;
}

.ba-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  flex-wrap: wrap;
  gap: 15px;
}

.ba-status {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
}

.ba-icon {
  font-size: 24px;
  color: #409eff;
}

.ba-text {
  margin: 0;
  color: #606266;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    text-align: center;
  }
  
  .stats-section {
    justify-content: center;
  }
  
  .ba-content {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
