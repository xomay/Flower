<template>
  <div class="indicators-section">
    <el-card title="Indicateurs de performance" shadow="hover">
      <div v-if="loading" class="loading-state">
        <el-skeleton :rows="3" animated />
      </div>
      
      <div v-else class="indicators-content">
        <!-- Statistiques générales -->
        <div class="stats-overview">
          <el-row :gutter="16">
            <el-col :span="12">
              <el-statistic 
                title="Études gérées" 
                :value="memberStats.totalStudies"
                prefix="📊"
              />
            </el-col>
            <el-col :span="12">
              <el-statistic 
                title="Projets actifs" 
                :value="memberStats.activeProjects"
                prefix="🔄"
              />
            </el-col>
          </el-row>
        </div>

        <el-divider />

        <!-- Graphiques ou indicateurs visuels -->
        <div class="visual-indicators">
          <h4>Activité par mois</h4>
          <div class="activity-chart">
            <div 
              v-for="(activity, month) in memberStats.monthlyActivity" 
              :key="month"
              class="activity-bar"
            >
              <div class="bar-container">
                <div 
                  class="bar-fill" 
                  :style="{ height: `${activity * 10}px` }"
                ></div>
              </div>
              <span class="month-label">{{ month }}</span>
            </div>
          </div>
        </div>

        <el-divider />

        <!-- Performance ratings -->
        <div class="performance-section">
          <h4>Évaluations</h4>
          <div class="performance-grid">
            <div class="performance-item">
              <span class="performance-label">Communication</span>
              <el-progress 
                :percentage="memberStats.communicationScore * 10" 
                :color="getScoreColor(memberStats.communicationScore)"
              />
            </div>
            <div class="performance-item">
              <span class="performance-label">Respect des délais</span>
              <el-progress 
                :percentage="memberStats.timelinessScore * 10" 
                :color="getScoreColor(memberStats.timelinessScore)"
              />
            </div>
            <div class="performance-item">
              <span class="performance-label">Qualité du travail</span>
              <el-progress 
                :percentage="memberStats.qualityScore * 10" 
                :color="getScoreColor(memberStats.qualityScore)"
              />
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { useTransition } from '@vueuse/core'
export default {
  name: "MemberIndicatorsView",
  props: {
    member: { type: Object, required: true }
  },
  data() {
    return {
      loading: false,
      memberStats: {
        totalStudies: 12,
        activeProjects: 3,
        monthlyActivity: {
          'Jan': 5,
          'Fév': 8,
          'Mar': 6,
          'Avr': 9,
          'Mai': 7,
          'Jun': 4
        },
        communicationScore: 8.5,
        timelinessScore: 7.2,
        qualityScore: 9.1
      }
    }
  },
  methods: {
    getScoreColor(score) {
      if (score >= 8) return '#67c23a'
      if (score >= 6) return '#e6a23c'
      return '#f56c6c'
    }
  }
}
</script>

<style scoped>
.indicators-section {
  height: 100%;
}

.loading-state {
  padding: 20px;
  text-align: center;
}

.indicators-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.stats-overview {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
  border-radius: 8px;
}

.visual-indicators h4,
.performance-section h4,
.quick-actions h4 {
  margin: 0 0 16px 0;
  color: #303133;
  font-size: 16px;
}

.activity-chart {
  display: flex;
  justify-content: space-between;
  align-items: end;
  height: 120px;
  padding: 20px;
  background-color: #fafbfc;
  border-radius: 6px;
  border: 1px solid #e4e7ed;
}

.activity-bar {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.bar-container {
  height: 80px;
  width: 20px;
  background-color: #f0f0f0;
  border-radius: 3px;
  display: flex;
  align-items: end;
  position: relative;
}

.bar-fill {
  width: 100%;
  background: linear-gradient(to top, #409eff, #67c23a);
  border-radius: 3px;
  min-height: 5px;
  transition: height 0.3s ease;
}

.month-label {
  font-size: 12px;
  color: #909399;
}

.performance-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.performance-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.performance-label {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

.actions-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

@media (max-width: 768px) {
  .activity-chart {
    height: 100px;
    padding: 15px;
  }
  
  .bar-container {
    height: 60px;
    width: 15px;
  }
  
  .actions-grid {
    flex-direction: column;
  }
}
</style>
