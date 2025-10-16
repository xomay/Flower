<template>
  <div class="employe-info">
    <!-- Header avec avatar -->
    <el-card shadow="hover" class="info-card">
      <div class="employe-header">
        <div class="employe-avatar">
          <span class="avatar-text">{{ getInitials() }}</span>
        </div>
        <div class="employe-basic-info">
          <h3 class="employe-name">{{ formatFullName(employe) }}</h3>
          <p class="employe-position">{{ employe.position || 'Poste non renseigné' }}</p>
          <div class="employe-badges">
            <el-tag v-if="employe.alumni" type="success" size="small">Alumni</el-tag>
          </div>
        </div>
        <div class="copy-all-section">
          <el-button
            type="text"
            size="small"
            @click="copyToClipboard(formatFullName(employe))"
            class="copy-button"
          >
            <el-icon><CopyDocument /></el-icon>
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- Informations de contact -->
    <el-card title="Contact" shadow="hover" class="info-card">
      <div class="info-grid">
        <div class="info-item">
          <el-icon class="info-icon"><Message /></el-icon>
          <div class="info-content">
            <span class="info-label">Email</span>
            <div class="info-value-with-copy">
              <span class="info-value">{{ employe.email || 'Non renseigné' }}</span>
              <el-button
                v-if="employe.email"
                type="text"
                size="small"
                @click="copyToClipboard(employe.email)"
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
              <span class="info-value">{{ employe.mobile || 'Non renseigné' }}</span>
              <el-button
                v-if="employe.mobile"
                type="text"
                size="small"
                @click="copyToClipboard(employe.mobile)"
                class="copy-button"
              >
                <el-icon><CopyDocument /></el-icon>
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: "EmployesView",
  props: {
    employe: { type: Object, required: true }
  },
  methods: {
    getInitials() {
      const firstname = this.employe.firstname || ''
      const lastname = this.employe.lastname || ''
      return (firstname.charAt(0) + lastname.charAt(0)).toUpperCase()
    },
    formatFullName(employe) {
      const parts = [
        employe.gender,
        employe.firstname,
        employe.lastname
      ].filter(Boolean)
      
      return parts.length > 0 ? parts.join(' ') : 'Non renseigné'
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
.employe-info {
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

.header-card {
  background: white;
}

.employe-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.employe-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.avatar-text {
  color: white;
  font-weight: bold;
  font-size: 20px;
}

.employe-basic-info {
  flex: 1;
}

.employe-name {
  margin: 0 0 4px 0;
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

.employe-position {
  margin: 0 0 8px 0;
  color: #666;
  font-size: 14px;
}

.employe-badges {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.copy-all-section {
  flex-shrink: 0;
}

@media (max-width: 768px) {
  .info-item {
    flex-direction: column;
    gap: 8px;
  }
  
  .info-icon {
    align-self: flex-start;
  }
  
  .employe-header {
    flex-direction: column;
    text-align: center;
    align-items: center;
    gap: 12px;
  }
  
  .employe-avatar {
    margin-bottom: 0;
  }
}
</style>
