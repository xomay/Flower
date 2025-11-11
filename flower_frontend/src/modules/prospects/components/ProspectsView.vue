<template>
  <div class="prospect-container">
    <!-- Header avec informations principales -->
    <el-card class="prospect-header" shadow="hover">
      <div class="header-content">
        <div class="company-icon">
          <el-icon size="40">
            <OfficeBuilding />
          </el-icon>
        </div>
        <div class="basic-info">
          <h2>{{ prospect.name }}</h2>
          <p class="company-type">{{ prospect.type }}</p>
          <p class="domain">
            <el-icon><PieChart /></el-icon>
            {{ prospect.domain }}
          </p>
        </div>
      </div>
    </el-card>

    <!-- Corps principal avec deux colonnes -->
    <el-row :gutter="20" class="main-content">
      <!-- Colonne gauche - Informations de contact -->
      <el-col :xs="24" :lg="12">
        <!-- Informations générales -->
        <el-card title="Informations de l'entreprise" shadow="hover" class="company-section">
          <div class="info-item">
            <el-icon><OfficeBuilding /></el-icon>
            <span class="label">Nom de l'entreprise :</span>
            <span class="value">{{ prospect.name }}</span>
            <el-button
              type="text"
              size="small"
              @click="copyToClipboard(prospect.name)"
              class="copy-button"
            >
              <el-icon><CopyDocument /></el-icon>
            </el-button>
          </div>
          <div class="info-item">
            <el-icon><Location /></el-icon>
            <span class="label">Adresse :</span>
            <span class="value">{{ prospect.address }}, {{ prospect.postcode }} {{ prospect.town }}</span>
            <el-button
              type="text"
              size="small"
              @click="copyToClipboard(`${prospect.address}, ${prospect.postcode} ${prospect.town}`)"
              class="copy-button"
            >
              <el-icon><CopyDocument /></el-icon>
            </el-button>
          </div>
          <div v-if="prospect.address_tresorerie" class="info-item">
            <el-icon><CreditCard /></el-icon>
            <span class="label">Adresse de trésorerie :</span>
            <span class="value">{{ prospect.address_tresorerie }}</span>
            <el-button
              type="text"
              size="small"
              @click="copyToClipboard(prospect.address_tresorerie)"
              class="copy-button"
            >
              <el-icon><CopyDocument /></el-icon>
            </el-button>
          </div>
        </el-card>

        <!-- Moyens de contact -->
         <DatePopup
          popup-title="Entrez la nouvelle date"
          :date-name="tampon.dateTitle"
          v-model:visibility="popupVisible"
          :placeholder="tampon.nextDate"
          @finish="popupClosed"
          style="width: 25vw; min-width: 300px;"
        />
        <el-card 
          v-if="prospect.contactWay && prospect.contactWay.length > 0"
          title="Moyens de contact" 
          shadow="hover" 
          class="contact-section"
        >
          <div class="contact-list">
            <div 
              v-for="contact in prospect.contactWay"
              :key="contact"
              class="contact-item"
            >
              <el-icon><Service /></el-icon>
              <span>{{ contact }}</span>
              <el-button
                type="text"
                size="small"
                @click="copyToClipboard(contact)"
                class="copy-button"
              >
                <el-icon><CopyDocument /></el-icon>
              </el-button>
            </div>
          </div>
        </el-card>
        <!-- Chargé dev'co -->
          <el-card v-if="displayCharge" title="Chargé de développement commercial" shadow="hover" class="devco-section">
            <div class="devco-member">
              <el-avatar :size="40" :src="member.picture">
                {{ member.firstname?.[0] }}{{ member.lastname?.[0] }}
              </el-avatar>
              <div class="member-info">
                <span class="member-role">Chargé dev'co</span>
                <el-link
                  type="primary"
                  @click="$router.push('/membres/'+prospect.charge+'/voir')"
                  class="member-name"
                >
                  {{ chargeName }}
                </el-link>
              </div>
              <el-tag type="primary" size="small">Dev'co</el-tag>
            </div>
          </el-card>
      </el-col>


      <!-- Colonne droite - Suivi commercial -->
      <el-col :xs="24" :lg="12">

        <!-- Suivi commercial -->
        <el-card title="Suivi commercial" shadow="hover" class="tracking-section">
          <div class="tracking-grid">
            <div class="tracking-item">
              <el-icon><Flag /></el-icon>
              <div>
                <span class="tracking-label">Statut actuel</span>
                <el-tag :type="typeMap[prospect.advancement]" size="small">
                  {{ statusMap[prospect.advancement] }}
                </el-tag>
              </div>
            </div>
            
            <div v-if="prospect.nextDate" class="tracking-item">
              <el-icon>
                <View v-if="prospect.advancement === 'NC'" />
                <Date v-else-if="prospect.advancement === 'AR'" />
                <Calendar v-else-if="prospect.advancement === 'PC'" />
                <Clock v-else />
              </el-icon>
              <div>
                <span class="tracking-label">Date de dernier contact</span>
                <span class="tracking-value">
                  <el-button
                  @click="changeDate(prospect)"
                  >
                    {{ prospect.nextDate ? niceDate(prospect.nextDate) : "non défini." }}
                  </el-button>
                </span>
              </div>
            </div>
          </div>
        </el-card>

        <!-- Actions recommandées -->
        <el-card title="Actions recommandées" shadow="hover" class="actions-section">
          <div class="action-item" v-if="prospect.advancement === 'NC'">
            <el-icon class="action-icon"><Phone /></el-icon>
            <div>
              <h4>Prise de contact nécessaire</h4>
              <p>Le dernier contact remonte au {{ niceDate(prospect.nextDate) }}</p>
            </div>
          </div>
          <div class="action-item" v-else-if="prospect.advancement === 'AR'">
            <el-icon class="action-icon"><Calendar /></el-icon>
            <div>
              <h4>Relance du prospect nécessaire</h4>
              <p>Le dernier contact remonte au {{ niceDate(prospect.nextDate) }}</p>
            </div>
          </div>
          <div class="action-item" v-else-if="prospect.advancement === 'PC'">
            <el-icon class="action-icon"><Document /></el-icon>
            <div>
              <h4>Devis en attente</h4>
              <p>Le dernier contact remonte au {{ niceDate(prospect.nextDate) }}</p>
            </div>
          </div>
          <div class="action-item" v-else-if="prospect.advancement === 'WIN' ||  prospect.advancement === 'LO' ">
            <el-icon class="action-icon"><Document /></el-icon>
            <div>
              <h4>Traitement du prospect terminée</h4>
              <p>Fidélisation possible : le dernier contact remonte au {{ niceDate(prospect.nextDate) }}</p>
            </div>
          </div>
          <div v-else class="action-item">
            <el-icon class="action-icon"><Plus /></el-icon>
            <div>
              <h4>Aucune action définie</h4>
              <p>Définir la prochaine étape du processus commercial</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
const axios = require("axios")
import DatePopup from "../components/DatePopup"


export default {
  name: "ProspectView",
  props: {
    prospect: { type: Object, required: true }
  },
  emits: ['updated-prospect'],
  components: {DatePopup},
  data () {
    return {
      chargeName: "",
      member: {},
      displayCharge: false,
      popupVisible: false,
      tampon: {
        item: {},
        listID: "",
        dateTitle: "Dernier contact :",
        nextDate: new Date().toISOString().split("T")[0]
      },
      statusMap: {
        'NC': 'Nouveau contact',
        'AR': 'A relancer',
        'PC': 'Devis à envoyer',
        'WIN': 'Prospect gagné',
        'LO' : 'Prospect perdu'
      },
      typeMap: {
        'NC': 'info',
        'AR': 'danger',
        'PC': 'warning',
        'WIN': 'success',
        'LO': 'danger'
      }
    }
  },
  watch: {
    prospect (nv) {
      if(nv.charge != null && nv.charge != undefined && nv.charge > 0) {
        axios.get(
          `/api/membres/${nv.charge}/`,
          {withCredentials: true}
        ).then((res) => {
          this.chargeName = res.data.firstname + " " + res.data.lastname
          this.member = res.data
          this.displayCharge = true
        }).catch((err) => {
          this.$message({message: "Impossible de récupérer le dev'co : "+err, type: "error", offset: 40})
        })
      }
    }
  },
  methods: {
    niceDate (dateString) {
      if(dateString == undefined || dateString == null) {
        return "non défini."
      } else {
        const tokens = dateString.split("-")
        return tokens[2] + "/" + tokens[1] + "/" + tokens[0]
      }
    },
    copyToClipboard(text) {
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(() => {
          this.$message({
            message: "Copié dans le presse-papiers",
            type: "success",
            duration: 2000
          })
        }).catch(() => {
          this.fallbackCopyTextToClipboard(text)
        })
      } else {
        this.fallbackCopyTextToClipboard(text)
      }
    },
    fallbackCopyTextToClipboard(text) {
      const textArea = document.createElement("textarea")
      textArea.value = text
      textArea.style.top = "0"
      textArea.style.left = "0"
      textArea.style.position = "fixed"
      document.body.appendChild(textArea)
      textArea.focus()
      textArea.select()
      try {
        document.execCommand("copy")
        this.$message({
          message: "Copié dans le presse-papiers",
          type: "success",
          duration: 2000
        })
      } catch (err) {
        this.$message({
          message: "Impossible de copier",
          type: "error",
          duration: 2000
        })
      }
      document.body.removeChild(textArea)
    },
    changeDate (prospect, listID, forced) {
      // Mise à jour du "tampon"
      this.tampon = {
        item: prospect,
        dateTitle: "Dernier contact :",
        nextDate: new Date().toISOString().split("T")[0]
      }
      this.startPopup()
    },
    // ouvre le popup
    startPopup () {
      this.popupVisible = true
    },
    // Referme le popup
    popupClosed (success, out) {
      const prospect = this.tampon.item
      if(success) {
        prospect.nextDate = out
        this.updateProspect(prospect)
      }
      this.popupVisible = false
    },
    // Met à jour le prospect sur le back
    updateProspect (prospect) {
      this.loading = true
      axios.put(
        `/api/prospects/${prospect.id}/`,
        prospect,
        {withCredentials: true}
      ).then((res) => {
        this.$emit('updated-prospect', res.data)
        this.$message({message: "Le prospect a bien été mis à jour", type: "success"})
      }).catch((err) => {
        this.$message({message: "Impossible d'update le prospect : "+err, type: "error"})
      }).finally(() => {
        this.loading = false
      })
    },
  }
}
</script>

<style scoped>
.prospect-container {
  max-width: 1400px;
  margin: 0 auto;
}

.prospect-header {
  margin-bottom: 20px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.company-icon {
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

.company-type {
  margin: 0 0 8px 0;
  color: #606266;
  font-size: 16px;
}

.domain {
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

.company-section,
.contact-section,
.devco-section,
.tracking-section,
.actions-section {
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
  padding: 12px 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #409eff;
  transition: all 0.3s ease;
  position: relative;
}

.info-item:hover {
  background-color: #e3f2fd;
  transform: translateX(2px);
}

.info-item:hover .copy-button {
  opacity: 1;
}

.label {
  font-weight: 500;
  color: #606266;
  min-width: 140px;
  flex-shrink: 0;
}

.value {
  color: #303133;
  line-height: 1.4;
}

.contact-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border-left: 3px solid #67c23a;
  position: relative;
}

.contact-item:hover .copy-button {
  opacity: 1;
}

.copy-button {
  opacity: 0;
  transition: opacity 0.3s ease;
  margin-left: auto;
  padding: 4px;
  color: #409eff;
  flex-shrink: 0;
}

.copy-button:hover {
  background-color: rgba(64, 158, 255, 0.1);
}

.copy-all-section {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e4e7ed;
  text-align: center;
}

.copy-all-button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.devco-member {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #67c23a;
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

.tracking-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.tracking-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background-color: #fafafa;
  border-radius: 8px;
  border-left: 4px solid #e6a23c;
}

.tracking-item > div {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.tracking-label {
  font-size: 12px;
  color: #909399;
  text-transform: uppercase;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.tracking-value {
  font-weight: 600;
  color: #303133;
  font-size: 15px;
}

.action-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #f56c6c;
}

.action-icon {
  font-size: 24px;
  color: #f56c6c;
  margin-top: 2px;
  flex-shrink: 0;
}

.action-item h4 {
  margin: 0 0 4px 0;
  color: #303133;
  font-size: 16px;
  font-weight: 600;
}

.action-item p {
  margin: 0;
  color: #606266;
  font-size: 14px;
  line-height: 1.4;
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
  
  .devco-member {
    flex-direction: column;
    align-items: flex-start;
    text-align: center;
  }
  
  .action-item {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
