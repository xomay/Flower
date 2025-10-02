<template>
  <div class="realisateur-info">
    <!-- Informations de contact -->
    <el-card title="Contact" shadow="hover" class="info-card">
      <div class="info-grid">
        <div class="info-item">
          <el-icon class="info-icon"><Message /></el-icon>
          <div class="info-content">
            <span class="info-label">Email</span>
            <span class="info-value">{{ realisateur.email || 'Non renseigné' }}</span>
          </div>
        </div>
        <div class="info-item">
          <el-icon class="info-icon"><Message /></el-icon>
          <div class="info-content">
            <span class="info-label">Email INSA</span>
            <span class="info-value">{{ realisateur.email_insa || 'Non renseigné' }}</span>
          </div>
        </div>
        <div class="info-item">
          <el-icon class="info-icon"><Phone /></el-icon>
          <div class="info-content">
            <span class="info-label">Mobile</span>
            <span class="info-value">{{ realisateur.mobile || 'Non renseigné' }}</span>
          </div>
        </div>
      </div>
    </el-card>

    <!-- Informations personnelles -->
    <el-card title="Informations personnelles" shadow="hover" class="info-card">
      <div class="info-grid">
        <div class="info-item">
          <el-icon class="info-icon"><Calendar /></el-icon>
          <div class="info-content">
            <span class="info-label">Date de naissance</span>
            <span class="info-value">{{ realisateur.birth_date || 'Non renseigné' }}</span>
          </div>
        </div>
        <div class="info-item">
          <el-icon class="info-icon"><Location /></el-icon>
          <div class="info-content">
            <span class="info-label">Lieu de naissance</span>
            <span class="info-value">{{ realisateur.birth_place || 'Non renseigné' }}</span>
          </div>
        </div>
        <div class="info-item">
          <el-icon class="info-icon"><MapLocation /></el-icon>
          <div class="info-content">
            <span class="info-label">Adresse</span>
            <span class="info-value">
              {{ formatAddress(realisateur) }}
            </span>
          </div>
        </div>
        <div 
          v-if="$store.currentUser.roles.includes('ROLE_ADMIN')" 
          class="info-item"
        >
          <el-icon class="info-icon"><FirstAidKit /></el-icon>
          <div class="info-content">
            <span class="info-label">N° de sécurité sociale</span>
            <span class="info-value">{{ realisateur.security_social_number || 'Non renseigné' }}</span>
          </div>
        </div>
      </div>
    </el-card>

    <!-- Compétences -->
    <el-card title="Compétences" shadow="hover" class="info-card" v-if="realisateur.skillsArray?.length">
      <div class="skills-container">
        <el-tag 
          v-for="skill in realisateur.skillsArray" 
          :key="skill"
          type="info"
          class="skill-tag"
        >
          {{ skill }}
        </el-tag>
      </div>
    </el-card>

    <!-- Description -->
    <el-card title="Présentation" shadow="hover" class="info-card" v-if="realisateur.description">
      <p class="description-text">{{ realisateur.description }}</p>
    </el-card>
  </div>
</template>

<script>
export default {
  name: "RealisateurView",
  props: {
    realisateur: { type: Object, required: true }
  },
  methods: {
    formatAddress(realisateur) {
      const parts = [
        realisateur.address,
        realisateur.town,
        realisateur.postcode && `(${realisateur.postcode})`,
        realisateur.country
      ].filter(Boolean)
      
      return parts.length > 0 ? parts.join(', ') : 'Non renseigné'
    }
  }
}
</script>

<style scoped>
.realisateur-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-card {
  width: 100%;
}

.info-grid {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.info-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child {
  border-bottom: none;
}

.info-icon {
  font-size: 18px;
  color: #409eff;
  margin-top: 2px;
  min-width: 18px;
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.info-label {
  font-size: 14px;
  font-weight: 600;
  color: #606266;
}

.info-value {
  font-size: 14px;
  color: #303133;
  word-break: break-word;
}

.skills-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.skill-tag {
  margin: 0;
}

.description-text {
  margin: 0;
  line-height: 1.6;
  color: #606266;
}

@media (max-width: 768px) {
  .info-item {
    flex-direction: column;
    gap: 8px;
  }
  
  .info-icon {
    align-self: flex-start;
  }
}
</style>
