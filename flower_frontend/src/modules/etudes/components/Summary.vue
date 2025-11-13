<template>
  <div class="summary-container">
    <EtudeSteps
      v-if="!etude.isAborted"
      :etude="etude"
      :descriptions="false"
    />
    
    <!-- Header avec informations principales -->
    <el-card class="etude-header" shadow="hover">
      <div class="header-content">
        <div class="etude-icon">
          <el-icon size="40">
            <Document />
          </el-icon>
        </div>
        <div class="basic-info">
          <h2>Étude {{ etude.number }}</h2>
          <p class="mandat">Mandat {{ etude.mandat }}</p>
          <p v-if="etude.projectManager" class="manager">
            <el-icon><User /></el-icon>
            Chargé d'étude : {{ etude.projectManager.firstname }} {{ etude.projectManager.lastname }}
          </p>
        </div>
        <div class="stats-section">
          <el-tag :type="etude.isAborted ? 'danger' : 'success'" size="small">
            {{ etude.isAborted ? 'Avortée' : 'Active' }}
          </el-tag>
        </div>
      </div>
    </el-card>

    <!-- Corps principal avec deux colonnes -->
    <el-row :gutter="20" class="main-content">
      <!-- Colonne gauche - Informations client et description -->
      <el-col :xs="24" :lg="12">
        <!-- Informations client -->
        <el-card v-if="!reaVue && (etude.prospect || etude.clientContact)" title="Informations client" shadow="hover" class="client-section">
          <div v-if="etude.prospect" class="info-item">
            <el-icon><OfficeBuilding /></el-icon>
            <span class="label">Prospect :</span>
            <el-link
              type="primary"
              @click="$router.push(`/prospects/${etude.prospect.id}/voir`)"
              class="link-button"
            >
              {{ etude.prospect.name }}
            </el-link>
          </div>
          <div v-if="etude.clientContact" class="info-item">
            <el-icon><UserFilled /></el-icon>
            <span class="label">Contact client :</span>
            <el-link
              type="primary"
              @click="$router.push(`/prospects/${etude.prospect.id}/employes/${etude.clientContact.id}/voir`)"
              class="link-button"
            >
              {{ etude.clientContact.firstname }} {{ etude.clientContact.lastname }}
            </el-link>
          </div>
        </el-card>

        <!-- Description de l'étude -->
        <el-card title="Description de l'étude" shadow="hover" class="description-section">
          <div class="description-content">
            <el-icon class="description-icon"><Document /></el-icon>
            <p class="description-text"><b>Description : </b>{{ etude.description }}</p>
          </div>
        </el-card>
      </el-col>

      <!-- Colonne droite - Équipe et informations supplémentaires -->
      <el-col :xs="24" :lg="12">
        
        <!-- Équipe -->
        <el-card title="Équipe projet" shadow="hover" class="team-section">
          <div v-if="etude.projectManager" class="team-member">
            <el-avatar :size="40" :src="etude.projectManager.picture">
              {{ etude.projectManager.firstname?.[0] }}{{ etude.projectManager.lastname?.[0] }}
            </el-avatar>
            <div class="member-info">
              <span class="member-role">Chargé d'étude</span>
              <el-link
                v-if="!reaVue"
                type="primary"
                @click="$router.push('/membres/'+etude.projectManager.id+'/voir')"
                class="member-name"
              >
                {{ etude.projectManager.firstname }} {{ etude.projectManager.lastname }}
              </el-link>
              <span v-else class="member-name">
                {{ etude.projectManager.firstname }} {{ etude.projectManager.lastname }}
              </span>
            </div>
            <el-tag type="primary" size="small">Chef de projet</el-tag>
          </div>
          <div v-if="etude.qualityManager && !reaVue" class="team-member">
            <el-avatar :size="40" :src="etude.qualityManager.picture">
              {{ etude.qualityManager.firstname?.[0] }}{{ etude.qualityManager.lastname?.[0] }}
            </el-avatar>
            <div class="member-info">
              <span class="member-role">Suiveur qualité</span>
              <el-link
                type="primary"
                @click="$router.push('/membres/'+etude.qualityManager.id+'/voir')"
                class="member-name"
              >
                {{ etude.qualityManager.firstname }} {{ etude.qualityManager.lastname }}
              </el-link>
            </div>
            <el-tag type="success" size="small">Qualité</el-tag>
          </div>
          
          <!-- Si pas d'équipe définie -->
          <div v-if="!etude.projectManager && !etude.qualityManager" class="no-team">
            <el-icon size="40"><User /></el-icon>
            <p>Aucune équipe assignée pour le moment</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import EtudeSteps from "./graphics/EtudeSteps"

export default {
  name: "Summary",
  components: { EtudeSteps },
  props: {
    etude: { type: Object, required: true },
    getgantt: { type: Boolean, default: false },
    reaVue: { type: Boolean, default: false }
  }
}
</script>

<style scoped>
.summary-container {
  max-width: 1400px;
  margin: 0 auto;
}

.etude-header {
  margin-bottom: 20px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.etude-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  background-color: #f0f9ff;
  border-radius: 50%;
  color: #409eff;
  flex-shrink: 0;
}

.basic-info {
  flex: 1;
  min-width: 250px;
}

.basic-info h2 {
  margin: 0 0 5px 0;
  color: #303133;
  font-size: 24px;
  font-weight: 600;
}

.mandat {
  margin: 0 0 8px 0;
  color: #606266;
  font-size: 16px;
}

.manager {
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

.client-section,
.description-section,
.team-section,
.technical-section {
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  padding: 12px 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #409eff;
  transition: all 0.3s ease;
}

.info-item:hover {
  background-color: #e3f2fd;
  transform: translateX(2px);
}

.label {
  font-weight: 500;
  color: #606266;
  min-width: 120px;
}

.link-button {
  font-weight: 500;
  font-size: 15px;
}

.description-section {
  min-height: 120px;
}

.description-content {
  display: flex;
  gap: 15px;
  align-items: flex-start;
}

.description-icon {
  font-size: 20px;
  color: #409eff;
  margin-top: 2px;
  flex-shrink: 0;
}

.description-text {
  line-height: 1.7;
  color: #606266;
  margin: 0;
  white-space: pre-wrap;
  font-size: 15px;
}

.team-member {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #67c23a;
  margin-bottom: 12px;
  transition: all 0.3s ease;
}

.team-member:hover {
  background-color: #f0f9ff;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.member-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.member-role {
  font-size: 12px;
  color: #909399;
  text-transform: uppercase;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.member-name {
  font-weight: 500;
  color: #409eff;
  font-size: 15px;
}

.no-team {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #909399;
  gap: 15px;
}

.no-team p {
  margin: 0;
  font-size: 14px;
  text-align: center;
}

.technical-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.technical-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background-color: #fafafa;
  border-radius: 8px;
  border-left: 4px solid #e6a23c;
}

.technical-item > div {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.technical-label {
  font-size: 12px;
  color: #909399;
  text-transform: uppercase;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.technical-value {
  font-weight: 600;
  color: #303133;
  font-size: 15px;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    text-align: center;
  }
  
  .stats-section {
    justify-content: center;
    flex-wrap: wrap;
    gap: 20px;
  }
  
  .info-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .label {
    min-width: auto;
  }
  
  .team-member {
    flex-direction: column;
    align-items: flex-start;
    text-align: center;
  }
  
  .description-content {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
