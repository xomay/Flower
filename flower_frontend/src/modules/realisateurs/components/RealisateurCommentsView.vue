<template>
  <div class="comments-section">
    <el-card title="Évaluations et commentaires" shadow="hover">
      <div v-if="loading" class="loading-state">
        <el-skeleton :rows="3" animated />
      </div>
      
      <div v-else-if="filteredComments.length === 0" class="empty-state">
        <el-empty description="Aucune évaluation disponible">
          <el-icon class="empty-icon"><ChatDotRound /></el-icon>
        </el-empty>
      </div>
      
      <div v-else class="comments-list">
        <div 
          v-for="comment in filteredComments" 
          :key="comment.id"
          class="comment-item"
        >
          <el-card shadow="hover" class="comment-card">
            <!-- En-tête du commentaire -->
            <div class="comment-header">
              <div class="comment-meta">
                <el-button
                  type="primary"
                  plain
                  size="small"
                  @click="$router.push(`/etudes/${comment.etude.id}/voir`)"
                  class="etude-link"
                >
                  <el-icon><FolderOpened /></el-icon>
                  {{ comment.etude.name }}
                </el-button>
                <span class="comment-date">
                  <el-icon><Calendar /></el-icon>
                  {{ formatDate(comment.date) }}
                </span>
              </div>
              <div class="rating-display">
                <el-rate
                  :model-value="comment.rating"
                  :max="10"
                  disabled
                  :allow-half="true"
                  :low-threshold="3.33"
                  :high-threshold="6.66"
                  :colors="['#ff1111', '#ffa200', '#62da05']"
                  show-score
                  score-template="{value}/10"
                />
              </div>
            </div>
            
            <!-- Contenu du commentaire -->
            <div class="comment-content">
              <p v-if="comment.content" class="comment-text">
                {{ comment.content }}
              </p>
              <p v-else class="no-comment">
                <em>Aucun commentaire écrit</em>
              </p>
            </div>
          </el-card>
        </div>
      </div>
      
      <!-- Statistiques -->
      <div v-if="filteredComments.length > 0" class="comments-stats">
        <el-divider />
        <div class="stats-grid">
          <el-statistic title="Total évaluations" :value="filteredComments.length" />
          <el-statistic 
            title="Note moyenne" 
            :value="averageRating" 
            :precision="1"
            suffix="/10"
          />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
const axios = require("axios")

export default {
  name: "RealisateurCommentsView",
  props: {
    realisateur: { type: Object, required: true }
  },
  data () {
    return {
      comments: [],
      etudes: [],
      loading: true
    }
  },
  computed: {
    filteredComments() {
      return this.comments
        .filter(comment => this.realisateur.comments?.includes(comment.id))
        .map(comment => ({
          ...comment,
          etude: this.etudes.find(e => e.id === comment.associatedEtude) || {}
        }))
        .filter(comment => comment.etude.id) // Seulement les commentaires avec une étude valide
    },
    averageRating() {
      if (this.filteredComments.length === 0) return 0
      const total = this.filteredComments.reduce((sum, comment) => sum + comment.rating, 0)
      return total / this.filteredComments.length
    }
  },
  created () {
    this.loading = true
    axios.get(
      "/api/etudes",
      { withCredentials: true }
    ).then((requestEtude) => {
      this.etudes = requestEtude.data
      axios.get(
        "/api/realisateurs/cmts",
        { withCredentials: true }
      ).then((requestComments) => {
        this.comments = requestComments.data
      }).catch((err) => {
        this.$message({message: "Impossible de récupérer les commentaires pour le moment : " + err, type: "error", offset: 40})
      }).finally(() => {
        this.loading = false
      })
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer les études pour le moment : " + err, type: "error", offset: 40})
      this.loading = false
    })
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return 'Date inconnue'
      try {
        return new Date(dateString).toLocaleDateString('fr-FR', {
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        })
      } catch {
        return dateString
      }
    }
  }
}
</script>

<style scoped>
.comments-section {
  height: 100%;
}

.loading-state, .empty-state {
  padding: 20px;
  text-align: center;
}

.empty-icon {
  font-size: 48px;
  color: #c0c4cc;
  margin-bottom: 16px;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 600px;
  overflow-y: auto;
  padding: 0 4px;
}

.comment-item {
  width: 100%;
}

.comment-card {
  transition: transform 0.2s ease;
}

.comment-card:hover {
  transform: translateY(-2px);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 12px;
}

.comment-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
  min-width: 200px;
}

.etude-link {
  align-self: flex-start;
}

.comment-date {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #909399;
}

.rating-display {
  flex-shrink: 0;
}

.comment-content {
  margin-top: 12px;
}

.comment-text {
  margin: 0;
  line-height: 1.6;
  color: #606266;
  background-color: #f8f9fa;
  padding: 12px;
  border-radius: 6px;
  border-left: 3px solid #409eff;
}

.no-comment {
  margin: 0;
  color: #c0c4cc;
  font-style: italic;
  text-align: center;
  padding: 12px;
}

.comments-stats {
  margin-top: 16px;
}

.stats-grid {
  display: flex;
  justify-content: space-around;
  gap: 20px;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .comment-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .rating-display {
    align-self: center;
  }
  
  .comments-list {
    max-height: 500px;
  }
}
</style>