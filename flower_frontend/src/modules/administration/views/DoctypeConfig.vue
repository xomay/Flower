<template>
  <BaseComponent
    title="Ajout de doctype"
    :breadcrumb="breadcrumb"
  >
  <el-card class="doctype-config" shadow="always">
    <el-radio-group v-model="selectedType" size="large" :max="1">
      <el-row :gutter="20">
        <el-col :span="8" v-for="(type, index) in documentTypes" :key="index" align="center" justify="center">
          <el-radio-button style="margin: 5px;" border :label="type">
            <el-icon><Document /></el-icon>
            {{ type }}
          </el-radio-button>
        </el-col>
      </el-row>
    </el-radio-group>

    <div class="file-upload" style="margin-top: 20px">
      <el-upload
        :auto-upload="false"
        :show-file-list="false"
        :before-upload="handleFileUpload"
        @change="onFileChange"
      >
        <el-button type="primary">Choisir un fichier</el-button>
        <span v-if="selectedFile" style="margin-left: 10px">{{ selectedFile.name }}</span>
      </el-upload>

      <el-button
        type="success"
        @click="uploadFile"
        :disabled="!selectedFile || !selectedType"
        style="margin-top: 10px"
      >
        Uploader
      </el-button>

      <el-button
        type="success"
        @click="downloadFile"
        :disabled="!selectedType && !loading"
        style="margin-top: 10px"
      >
        Télécharger
      </el-button>
    </div>
  </el-card>
  </BaseComponent>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const documentTypes = ['CE', 'CCA', 'BC', 'PVR', 'RDM', 'BCR', 'BA', 'BV', 'NF', 'FA']
const selectedType = ref('')
const selectedFile = ref(null)
const loading = ref(false)
const breadcrumb = ref([
  { name: 'Administration', link: '/administration/doctypes' },
  { name: 'Gérer les doctypes', link: '/administration/doctypes' },
])

const handleFileUpload = (file) => {
  selectedFile.value = file
  return false // empêche l'upload auto d'el-upload
}

const onFileChange = (file) => {
  selectedFile.value = file.raw || file
}

const getCSRFToken = () => {
  const name = 'csrftoken'
  const match = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`))
  return match ? match[2] : null
}

const uploadFile = async () => {
  loading.value = true
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)

    const res = await axios.post(
      `/api/administration/doctypes/${selectedType.value}.docx/`,
      formData,
      {
        withCredentials: true,
        headers: {
          'X-CSRFToken': getCSRFToken(),
          'Content-Type': 'multipart/form-data',
        },
      }
    )

    ElMessage.success('Fichier uploadé avec succès.')
    window.location.reload()
  } catch (err) {
    console.error('Erreur d\'upload :', err)
    ElMessage.error('Échec de l\'upload.')
  } finally {
    loading.value = false
  }
}

const downloadFile = async () => {
  loading.value = true
  try {
    const res = await axios.get(
      `/api/administration/doctypes/${selectedType.value}.docx/`,
      {
        withCredentials: true,
        responseType: 'blob',
        headers: {
          'X-CSRFToken': getCSRFToken(),
        },
      }
    )

    const url = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${selectedType.value}.docx`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)

    ElMessage.success('Fichier téléchargé avec succès.')
  } catch (err) {
    console.error('Erreur de téléchargement :', err)
    ElMessage.error('Échec du téléchargement.')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.doctype-config {
  max-width: 600px;
  margin: 30px auto;
  padding: 20px;
}
</style>