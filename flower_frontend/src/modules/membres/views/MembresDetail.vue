<template>
  <BaseComponent
    :title="title"
    :breadcrumb="breadcrumb"
  >
    <template v-slot:action>
      <el-button
        type="primary"
        icon="Edit"
        @click="$router.push(`/membres/${$route.params.id}/modifier`)"
      >
        Modifier
      </el-button>
      <el-button
        v-if="member.is_active"
        type="danger"
        icon="CloseBold"
        @click="toggleActive()"
      >
        Sortir du mandat
      </el-button>
      <el-button
        v-else
        type="warning"
        icon="Select"
        @click="toggleActive()"
      >
        Intégrer au mandat
      </el-button>
    </template>

    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="8" animated />
    </div>

    <div v-else-if="member.id" class="profile-container">
      <!-- Header avec informations principales -->
      <el-card class="profile-header" shadow="hover">
        <div class="header-content">
          <div class="avatar-section">
            <el-avatar :size="80" :src="member.picture">
              {{ member.firstname?.[0] }}{{ member.lastname?.[0] }}
            </el-avatar>
            <el-tag 
              v-if="member.is_active"
              type="success"
              class="status-tag"
            >
              Membre actif
            </el-tag>
            <el-tag 
              v-else
              type="info"
              class="status-tag"
            >
              Ancien membre
            </el-tag>
          </div>
          <div class="basic-info">
            <h2>
              <span v-if="member.gender">{{ member.gender }}</span>
              {{ member.firstname }} {{ member.lastname }}
            </h2>
            <p class="promotion">Promotion {{ member.promotion }}</p>
            <p v-if="member.poste" class="position">
              <el-icon><Briefcase /></el-icon>
              {{ displayPoste(member) }}
            </p>
          </div>
          <div class="stats-section">
            <el-statistic title="Subordonnés" :value="subordinates.length" />
            <el-statistic 
              title="Statut" 
              :value="member.is_active ? 'Actif' : 'Inactif'"
            />
          </div>
        </div>
      </el-card>

      <!-- Corps principal avec deux colonnes -->
      <el-row :gutter="20" class="main-content">
        <!-- Colonne gauche - Informations détaillées -->
        <el-col :xs="24" :lg="12">
          <MemberView :member="member" />
          
          <!-- Section Subordonnés -->
          <el-card 
            v-if="subordinates.length > 0" 
            title="Équipe" 
            shadow="hover" 
            class="subordinates-section"
          >
            <div class="subordinates-list">
              <div 
                v-for="sub in subordinates"
                :key="sub.id"
                class="subordinate-item"
              >
                <el-button
                  type="text"
                  @click="pushToSubordinate(sub.id)"
                  class="subordinate-link"
                >
                  <el-icon><User /></el-icon>
                  {{ nicePeople(sub) }}
                </el-button>
                <el-tag size="small" type="info">{{ sub.poste }}</el-tag>
              </div>
            </div>
          </el-card>
          
          <!-- Section BA -->
          <el-card title="Bulletin d'adhésion" shadow="hover" class="ba-section">
            <div class="ba-content">
              <div class="ba-status">
                <el-icon class="ba-icon">
                  <Document />
                </el-icon>
                <div>
                  <p v-if="member.ba" class="ba-text">
                    <strong>BA généré:</strong> {{ member.ba }}
                  </p>
                  <p v-else class="ba-text">
                    <strong>BA:</strong> Non généré
                  </p>
                </div>
              </div>
              <el-button
                type="primary"
                :disabled="!(member.address && member.postcode && member.town && member.country)"
                @click="downloadBA()"
                :loading="downloading"
              >
                <el-icon><Download /></el-icon>
                Générer BA
              </el-button>
            </div>
            <el-alert
              v-if="!(member.address && member.postcode && member.town && member.country)"
              title="Informations manquantes"
              type="warning"
              description="L'adresse complète est requise pour générer le bulletin d'adhésion"
              show-icon
              :closable="false"
            />
          </el-card>
        </el-col>

        <!-- Colonne droite - Indicateurs -->
        <el-col :xs="24" :lg="12">
          <MemberIndicatorsView :member="member" />
        </el-col>
      </el-row>
    </div>
  </BaseComponent>
</template>

<script>
const axios = require("axios")
// Configuration d'axios pour CSRF
axios.defaults.xsrfCookieName = "csrftoken"
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.withCredentials = true
import Utils from "@/mixins/Utils"
import MemberView from "../components/MemberView"
import MemberIndicatorsView from "../components/MemberIndicatorsView"

export default {
  name: "MembresDetail",
  mixins: [Utils],
  components: { MemberView, MemberIndicatorsView },
  data () {
    return {
      member: {},
      title: "Profil du membre",
      subordinates: [],
      loading: true,
      downloading: false,
      breadcrumb: [
        {
          name: "Liste des membres",
          link: "/membres"
        },
        {
          name: "Chargement...",
          link: `/membres/${this.$route.params.id}/voir`
        }
      ]
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      `/api/membres/${this.$route.params.id}`,
      {withCredentials: true}
    ).then((res) => {
      this.member = res.data
      this.breadcrumb[1].name = this.nicePeople(this.member)
      this.title = `Profil de ${this.nicePeople(this.member)}`
      
      // Chargement des subordonnés :
      if(this.member.poste != undefined) {
        const subs = this.member.poste.subordinates
        axios.get(
          "/api/membres/",
          {withCredentials: true}
        ).then((res) => {
          this.subordinates = res.data.filter((m) => m.poste != undefined && subs.indexOf(m.poste.id) >= 0)
          this.subordinates.forEach(m => m.poste = this.displayPoste(m))
        }).catch((err) => {
          this.$message({message: "Impossible de récupérer les autres membres : " + err, type: "error"})
        }).finally(() => {
          this.loading = false
        })
      } else {
        this.loading = false
      }
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer le membre : " + err, type: "error"})
      this.loading = false
    })
  },
  methods: {
    pushToSubordinate (sub_id) {
      this.$router.push(`/membres/${sub_id}/redirect`)
    },
    toggleActive () {
      this.member.is_active = !this.member.is_active
      const memberToSend = { ...this.member }
      // Si poste est un objet, on envoie juste l'id
      if (memberToSend.poste && typeof memberToSend.poste === "object") {
        memberToSend.poste = memberToSend.poste.id
      }
      this.loading = true
      axios.put(
        `/api/membres/${this.member.id}/`,
        memberToSend,
        {withCredentials: true}
      ).then(() => {
        this.$message({message: `${this.member.is_active ? "Le membre fait partie du mandat" : "Le membre ne fait plus partie du mandat"}.`, type: "success"})
        this.$router.push(`/membres/${this.member.id}/voir`)
      }).catch((err) => {
        this.$message({message: `Impossible de modifier le statut du membre : ${err}`, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
    downloadBA () {
      this.downloading = true
      axios.get(
        `/api/publish/ba/${this.member.id}`,
        {withCredentials: true,
          responseType: "blob"}
      ).then((response) => {
        this.createDownloadElement(
          response.data,
          `BA-${this.member.lastname}-${this.member.firstname}.docx`
        )
        this.$message({
          message: "Bulletin d'adhésion généré avec succès",
          type: "success"
        })
      }).catch((err) => {
        this.$message({message: `Une erreur est survenue lors de la génération du bulletin d'adhésion : ${err}`,
          type: "error"})
      }).finally(() => {
        this.downloading = false
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
  margin: 0 0 5px 0;
  color: #606266;
  font-size: 16px;
}

.position {
  margin: 0;
  color: #409eff;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.stats-section {
  display: flex;
  gap: 30px;
  align-items: center;
}

.main-content {
  margin-top: 20px;
}

.subordinates-section,
.ba-section {
  margin-top: 20px;
}

.subordinates-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.subordinate-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border-left: 3px solid #409eff;
}

.subordinate-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0;
  font-weight: 500;
}

.ba-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
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
  
  .subordinate-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>
