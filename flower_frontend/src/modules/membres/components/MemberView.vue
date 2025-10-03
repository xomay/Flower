<template>
  <div class="member-info">
    <!-- Informations de contact -->
    <el-card title="Contact" shadow="hover" class="info-card">
      <div class="info-grid">
        <div class="info-item">
          <el-icon class="info-icon"><Message /></el-icon>
          <div class="info-content">
            <span class="info-label">Email personnel</span>
            <div class="info-value-with-copy">
              <span class="info-value">{{ member.email || 'Non renseigné' }}</span>
              <el-button
                v-if="member.email"
                type="text"
                size="small"
                @click="copyToClipboard(member.email)"
                class="copy-button"
              >
                <el-icon><CopyDocument /></el-icon>
              </el-button>
            </div>
          </div>
        </div>
        <div class="info-item">
          <el-icon class="info-icon"><Message /></el-icon>
          <div class="info-content">
            <span class="info-label">Email Junior</span>
            <div class="info-value-with-copy">
              <span class="info-value">{{ member.email_junior || 'Non renseigné' }}</span>
              <el-button
                v-if="member.email_junior"
                type="text"
                size="small"
                @click="copyToClipboard(member.email_junior)"
                class="copy-button"
              >
                <el-icon><CopyDocument /></el-icon>
              </el-button>
            </div>
          </div>
        </div>
        <div class="info-item">
          <el-icon class="info-icon"><Phone /></el-icon>
          <div class="info-content">
            <span class="info-label">Mobile</span>
            <div class="info-value-with-copy">
              <span class="info-value">{{ member.mobile || 'Non renseigné' }}</span>
              <el-button
                v-if="member.mobile"
                type="text"
                size="small"
                @click="copyToClipboard(member.mobile)"
                class="copy-button"
              >
                <el-icon><CopyDocument /></el-icon>
              </el-button>
            </div>
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
            <span class="info-value">{{ member.birth_date || 'Non renseigné' }}</span>
          </div>
        </div>
        <div class="info-item">
          <el-icon class="info-icon"><Location /></el-icon>
          <div class="info-content">
            <span class="info-label">Lieu de naissance</span>
            <span class="info-value">{{ member.birth_place || 'Non renseigné' }}</span>
          </div>
        </div>
        <div class="info-item">
          <el-icon class="info-icon"><MapLocation /></el-icon>
          <div class="info-content">
            <span class="info-label">Adresse</span>
            <span class="info-value">
              {{ formatAddress(member) }}
            </span>
          </div>
        </div>
        <div class="info-item">
          <el-icon class="info-icon"><Place /></el-icon>
          <div class="info-content">
            <span class="info-label">Pays</span>
            <span class="info-value">{{ member.country || 'Non renseigné' }}</span>
          </div>
        </div>
        <div class="info-item">
          <el-icon class="info-icon"><Wallet /></el-icon>
          <div class="info-content">
            <span class="info-label">Nationalité</span>
            <span class="info-value">{{ member.nationality || 'Non renseigné' }}</span>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: "MemberView",
  props: {
    member: { type: Object, required: true }
  },
  methods: {
    formatAddress(member) {
      const parts = [
        member.address,
        member.town,
        member.postcode
      ].filter(Boolean)
      
      return parts.length > 0 ? parts.join(', ') : 'Non renseigné'
    },
    async copyToClipboard(text) {
      try {
        await navigator.clipboard.writeText(text)
        this.$message({
          message: 'Copié dans le presse-papiers',
          type: 'success',
          duration: 2000
        })
      } catch (err) {
        // Fallback pour les navigateurs plus anciens
        const textArea = document.createElement('textarea')
        textArea.value = text
        document.body.appendChild(textArea)
        textArea.select()
        document.execCommand('copy')
        document.body.removeChild(textArea)
        this.$message({
          message: 'Copié dans le presse-papiers',
          type: 'success',
          duration: 2000
        })
      }
    }
  }
}
</script>

<style scoped>
.member-info {
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

.info-value-with-copy {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.copy-button {
  padding: 0;
  min-height: auto;
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.copy-button:hover {
  opacity: 1;
}

.info-item:hover .copy-button {
  opacity: 1;
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
