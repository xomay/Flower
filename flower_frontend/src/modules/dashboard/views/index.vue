<template>
  <div class="dashboard-container">
    <!-- Header de bienvenue -->
    <el-card class="welcome-card" shadow="never">
      <div class="welcome-content">
        <div>
          <h1 class="welcome-title">
            Bienvenue {{ getUsername() }} !
          </h1>
          <p class="welcome-subtitle">
            Voici un aperçu de votre activité sur Flower
          </p>
        </div>
        <img 
          src="@/assets/flower.jpg" 
          class="welcome-image"
          fit="contain"
        />
      </div>
    </el-card>

    <!-- Statistiques rapides -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <router-link to="etudes">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <el-icon class="stat-icon etudes-icon"><Document /></el-icon>
              <div class="stat-text">
                <h3>{{ etudes.length }}</h3>
                <p>Études actives</p>
              </div>
            </div>
          </el-card>
        </router-link>
      </el-col>
      
      <el-col :span="6">
        <router-link to="prospects">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <el-icon class="stat-icon prospects-icon"><UserFilled /></el-icon>
              <div class="stat-text">
                <h3>{{ prospects.length }}</h3>
                <p>Prospects</p>
              </div>
            </div>
          </el-card>
        </router-link>
      </el-col>
      
      <el-col :span="6">
        <router-link to="membres">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <el-icon class="stat-icon members-icon"><User /></el-icon>
              <div class="stat-text">
                <h3>{{ membres.length }}</h3>
                <p>Membres</p>
              </div>
            </div>
          </el-card>
        </router-link>
      </el-col>
      
      <el-col :span="6">
        <router-link to="tresorerie/etudes">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <el-icon class="stat-icon factures-icon"><Money /></el-icon>
            <div class="stat-text">
              <h3>{{ factures.length }}</h3>
              <p>Factures</p>
            </div>
          </div>
        </el-card>
        </router-link>
      </el-col>
    </el-row>

    <!-- Actions rapides -->
    <el-card class="actions-card">
      <template #header>
        <h2 class="card-title">
          <el-icon><Lightning /></el-icon>
          Actions rapides
        </h2>
      </template>
      
      <el-row :gutter="16">
        <el-col :span="8">
          <router-link to="/etudes/ajouter">
            <el-button 
            type="primary" 
            size="large" 
            class="action-button"
            >
              <el-icon style="margin: 5px; font-size: 1.2rem;"><Plus /></el-icon>
              Créer une étude
            </el-button>
          </router-link>
        </el-col>
        
        <el-col :span="8">
          <router-link to="/prospects/ajouter">
            <el-button type="success" size="large" class="action-button">
              <el-icon style="margin: 5px; font-size: 1.2rem;"><UserFilled /></el-icon>
              Ajouter un prospect
            </el-button>
          </router-link>
        </el-col>
        
        <el-col :span="8">
          <router-link to="/membres/ajouter">
            <el-button type="info" size="large" class="action-button">
              <el-icon style="margin: 5px; font-size: 1.2rem;"><User /></el-icon>
              Ajouter un membre
            </el-button>
          </router-link>
        </el-col>
      </el-row>
    </el-card>

    <!-- Études récentes -->
    <el-card class="recent-card">
      <template #header>
        <h2 class="card-title">
          <el-icon><Document /></el-icon>
          Études en cours
        </h2>
      </template>

      <EtudesDashboard
        :etudes="recentEtudes"
        :loading="loading"
        @select="goToEtude"
      />

      <div class="table-footer" v-if="etudes.length > 5">
        <router-link to="/etudes">
          <el-button type="text">
            Voir toutes les études →
          </el-button>
        </router-link>
      </div>
    </el-card>

    <!-- Footer version -->
    <div class="version-footer">
      <el-text type="info">
        Version actuelle : <b>mathysdev</b>
      </el-text>
    </div>
  </div>
</template>

<script>
import GraphicsBlock from "../components/GraphicsBlock"
import { Permissions } from "@/mixins/Permissions"
import EtudesDashboard from "../../etudes/components/EtudesDashboard.vue"

const axios = require("axios")
axios.defaults.xsrfCookieName = "csrftoken"
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.withCredentials = true

export default {
  name: "DashboardIndex",
  components: { GraphicsBlock, EtudesDashboard },
  mixins: [Permissions],
  data() {
    return {
      etudes: [],
      prospects: [],
      membres: [],
      factures: [],
      loading: true
    }
  },
  computed: {
    recentEtudes() {
      return this.etudes.slice(0, 5)
    }
  },
  created() {
    this.loadDashboardData()
  },
  methods: {
    getUsername() {
      return this.$store.currentUser.user.name
    },

    goToEtude (id) {
      this.$router.push(`/etudes/${id}/voir`)
    },

    async loadDashboardData() {
      try {
        const [etudesRes, prospectsRes, membresRes, facturesRes] = await Promise.all([
          axios.get("/api/etudes/", { withCredentials: true }),
          axios.get("/api/prospects/", { withCredentials: true }),
          axios.get("/api/membres/", { withCredentials: true }),
          axios.get("/api/tresorerie/factures/", { withCredentials: true })
        ])

        this.etudes = etudesRes.data || []
        this.prospects = prospectsRes.data || []
        this.membres = membresRes.data || []
        this.factures = facturesRes.data || []
        this.etudes = this.etudes.filter(e => e.state >= 0 && e.state < 10 && e.phases.length > 0)
        this.prospects = this.prospects.filter(p => p.advancement !== 'WIN' && p.advancement !== 'LO')
        this.membres = this.membres.filter(m => m.is_active)
      } catch (error) {
        console.error("Erreur lors du chargement des données du dashboard:", error)
        // Valeurs par défaut en cas d'erreur
        this.etudes = []
        this.prospects = []
        this.membres = []
        this.factures = []
      } finally {
        this.loading = false
      }
    },

    getEtudeStateType(state) {
      const stateTypes = {
        0: 'default',
        1: 'success',     // En cours
        2: 'success',     // En cours
        3: 'warning',  // En attente
        4: 'danger',
        5: 'warning',
        6: 'danger',
        7: 'warning',
        8: 'success',
        9: 'success',
        10: 'success'     // Terminée
      }
      return stateTypes[state] || 'info'
    },

    getEtudeStateName(state) {
      const stateNames = {
        0: 'PC en rédaction',
        1: 'CE en rédaction',
        2: 'RM en rédaction', 
        3: 'FA à payer',
        4: 'PVRI en rédaction',
        5: 'FI à payer',
        6: 'PVRF en rédaction',
        7: 'FS à payer',
        8: 'Retour d\'expérience',
        9: 'BV à envoyer',
        10: 'Terminée'
      }
      return stateNames[state] || 'Inconnu'
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.welcome-card {
  margin-bottom: 20px;
  border: none;
}

.welcome-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.welcome-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #303133;
  margin: 0 0 10px 0;
}

.welcome-subtitle {
  font-size: 1.1rem;
  color: #606266;
  margin: 0;
}

.welcome-image {
  max-width: 200px;
  height: auto;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  height: 120px;
  cursor: pointer;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.stat-icon {
  font-size: 3rem;
  margin-right: 15px;
}

.etudes-icon {
  color: #409eff;
}

.prospects-icon {
  color: #67c23a;
}

.members-icon {
  color: #e6a23c;
}

.factures-icon {
  color: #f56c6c;
}

.stat-text h3 {
  font-size: 2rem;
  font-weight: bold;
  margin: 0;
  color: #303133;
}

.stat-text p {
  margin: 5px 0 0 0;
  color: #606266;
  font-size: 0.9rem;
}

.actions-card,
.recent-card {
  margin-bottom: 20px;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.3rem;
  font-weight: bold;
  margin: 0;
  color: #303133;
}

.action-button {
  width: 100%;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.table-footer {
  text-align: center;
  padding-top: 15px;
  border-top: 1px solid #ebeef5;
  margin-top: 15px;
}

.version-footer {
  text-align: center;
  padding: 20px;
  border-top: 1px solid #ebeef5;
  margin-top: 20px;
}

/* Responsive */
@media (max-width: 768px) {
  .welcome-content {
    flex-direction: column;
    text-align: center;
  }
  
  .welcome-image {
    margin-top: 20px;
  }
  
  .stats-row .el-col {
    margin-bottom: 10px;
  }
}
</style>
