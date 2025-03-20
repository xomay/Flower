<template>
  <div class="doctype-config">
    <h1>Veuillez sélectionner le doctype à mettre à jour :</h1>
    <div class="doctype-options">
      <div v-for="(type, index) in documentTypes" :key="index" class="doctype-option">
        <input 
          type="radio" 
          :id="type" 
          :value="type" 
          v-model="selectedType"
        />
        <label :for="type">{{ type }}</label>
      </div>
    </div>
    <div class="file-upload">
      <input type="file" @change="handleFileUpload" />
      <button @click="uploadFile" :disabled="!selectedFile || !selectedType">Uploader</button>
    </div>
  </div>
</template>

<script>
const axios = require("axios");

export default {
  data() {
    return {
      documentTypes: ["CE", "CC", "BC", "PVRF", "PVRI", "Avenant", "RM", "BCR"],
      selectedType: "",
      selectedFile: null
    };
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0]; // Récupère le fichier sélectionné
    },
    async uploadFile() {
      if (!this.selectedFile) {
        alert("Veuillez sélectionner un fichier");
        return;
      }

      let formData = new FormData();
      formData.append("file", this.selectedFile);

      axios.post(`/api/administration/doctypes/${this.selectedType}.docx/`, formData, {
          withCredentials: true, 
          headers: {
            "X-CSRFToken": this.$cookies.get("csrftoken"),//ne fonctionne pas
            "Content-Type": "multipart/form-data",
            "enctype": "multipart/form-data" // pour Django
          },
        }).then((res) => {
          alert("Fichier uploadé :", res);
          location.reload();
        }).catch((err) => {
          console.error("Erreur d'upload :", err);
        });
    }
  }
};
</script>

<style scoped>
.doctype-config {
  max-width: 600px;
  margin: 0 auto;
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.doctype-options {
  margin-bottom: 20px;
}

.doctype-option {
  margin-bottom: 10px;
}

.file-upload {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.file-upload input[type="file"] {
  margin-bottom: 10px;
}

.file-upload button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.file-upload button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>