<template>
  <el-table
    v-loading="loading"
    class="grid"
    :data="ccs"
    :stripe="true"
    :border="true"
  >
    <el-table-column
      prop="name"
      label="Nom de la CC"
      fixed="left"
      sortable
    >
      <template #default="{row}">
        <router-link :to="`/cc/${row.id}/modifier`">
          <el-button
            type="text"
            :disabled="row.isFinished"
          >
          {{ row.name }}
          </el-button>
        </router-link>
        <span
          v-if="row.confidential"
          class="bigGray"
          style="margin-right: 12px;"
        >
          [Confidentielle]
        </span>
        <span
          v-if="row.isFinished"
          class="bigRed"
        >
          [CC périmée]
        </span>
        <span
          v-if="row.signDate && !row.isFinished"
          class="bigGreen"
        >
          [CC en cours]
        </span>
        <span
          v-if="!row.signDate && !row.isFinished"
          class="bigOrange"
        >
          [CC à signer]
        </span>
      </template>
    </el-table-column>
    <el-table-column
      prop="number"
      label="Numéro de la CC"
      align="center"
      fixed="left"
      width="100px"
      sortable
    />
    <el-table-column
      prop="endDate"
      label="Date de fin"
      align="center"
      fixed="right"
      width="180px"
    />
    <el-table-column
      label="Modifier"
      align="center"
      fixed="right"
      width="100px"
    >
    <template #default="{row}">
        <router-link :to="`/cc/${row.id}/modifier`">
        <el-button
          :disabled="row.isFinished || row.signDate==null"
          type="text"
          icon="Edit"
        >
        </el-button>
      </router-link>
      </template>
    </el-table-column>
    <el-table-column
      label="Docx"
      align="center"
      fixed="right"
      width="100px"
    >
    <template #default="{row}">
      <el-button
        :disabled="row.isFinished"
        type="text"
        icon="Download"
        @click="downloadCC(row)"
      >
      </el-button>
    </template>
    </el-table-column>
    <el-table-column
      label="PDF"
      align="center"
      fixed="right"
      width="100px"
    >
    <template #default="{row}">
      <el-button
        :disabled="row.isFinished"
        type="text"
        icon="Download"
        @click="downloadCCPdf(row)"
      >
      </el-button>
    </template>
    </el-table-column>
    <el-table-column
      align="center"
      fixed="right"
      width="80px"
    >
    <template #default="{row}">
      <el-button
        icon="DocumentChecked"
        type="success"
        plain
        @click="signDateForm = true; form.cc = row;"
        />
    </template>
    </el-table-column>
    <el-table-column
      align="center"
      fixed="right"
      width="80px"
    >
    <template #default="{row}">

      <el-popconfirm 
      title="Etes-vous sûr de vouloir supprimer cette CC ?"
      confirm-button-text="Oui"
      cancel-button-text="Non"
      confirm-button-type="success"
      cancel-button-type="warning"
      hide-icon
      @confirm="deleteCC(row.id)"
      >
        <template #reference>
          <el-button
          :disabled="row.isFinished || (row.signDate!=null && !row.isFinished)"
          icon="Delete"
          type="danger"
          plain
          />
        </template>
    </el-popconfirm>
    </template>
    </el-table-column>


  </el-table>
  <el-dialog v-model="signDateForm" title="Date de signature du document" width="500">
    <el-form :model="form">
      <el-form-item
      label="Référence :"
        prop="ref"
        label-width="140px"
      >
        <el-date-picker
          v-model="form.cc.signDate"
          format="DD/MM/YYYY"
          value-format="YYYY-MM-DD"
          type="date"
          placeholder="Sélectionnez une date"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="signDateForm = false">Annuler</el-button>
        <el-button type="primary" @click="signCC(form.cc.id); signDateForm = false;">
          Confirmer
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script>
import Utils from "@/mixins/Utils"
import Publishing from "@/mixins/Publishing"


const axios = require("axios")
// Configuration d'axios pour CSRF
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.withCredentials = true;

export default {
  name: "CCList",
  mixins: [Utils, Publishing],
  props: {
    ccs: {type : Array, required: true },
    loading: {type : Boolean, required: true },
    discret: {type : Boolean, default () { return false } }
  },
  emits: ["select"],
  data () {
    return {
      signDateForm: false,
      form: {
        cc: {
          id: null,
          name: null,
          confidential: null,
          signDate: null,
        }
      }
    }
  },
  created() {
    const today = new Date();

    this.ccs.forEach(cc => {
      const signDate = cc.signDate ? new Date(cc.signDate) : today;
      const endDate = new Date(signDate);
      endDate.setFullYear(signDate.getFullYear() + cc.period);

      cc.endDate = endDate.toLocaleDateString("fr-FR", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit"
      });
      cc.isFinished = endDate < today;
    });
  },
  watch: {
    ccs () {
      const today = new Date();

      this.ccs.forEach(cc => {
        const signDate = cc.signDate ? new Date(cc.signDate) : today;
        const endDate = new Date(signDate);
        endDate.setFullYear(signDate.getFullYear() + cc.period);

        cc.endDate = endDate.toLocaleDateString("fr-FR", {
          year: "numeric",
          month: "2-digit",
          day: "2-digit"
        });
        cc.isFinished = endDate < today;
      });
    }
  },
  methods: {
    getPercentage (state) {
      if(state == undefined)
        return "width: 0%"
      return "width: "+(state*10)+"%"
    },
    signCC (id) {
      axios.put(
        `/api/etudes/cc/${id}/`,
        this.form.cc,
        { withCredentials: true }
      ).then(() => {
        this.$message({message: "CC signé", type: "success"})
        this.$router.go(0)
      }).catch((err) => {
        this.$message({message: "Impossible de signer la CC : " + err, type: "error"})
      })
    },
    deleteCC (id) {
      axios.delete(
        `/api/etudes/cc/${id}/`,
        { withCredentials: true }
      ).then(() => {
        this.$message({message: "CC supprimé", type: "success"})
        this.$router.go(0)
      }).catch((err) => {
        if (err.response && err.response.status === 500) {
          this.$message({message: "La CC ne peut pas être supprimé car elle est liée à une étude !",
            type: "error",
            offset: 40})
        } else {
          this.$message({message: "Impossible de surrpimer la CC : " + err, type: "error"})
        }
      })
    }
  }
}
</script>

<style scoped>
  .back {
    justify-content: center;
    align-items: center;
    background: #000;
    display: flex;
    height: 100vh;
    padding: 0;
    margin: 0;
  }

  .progress {
    background: rgb(161, 153, 153) !important;
    justify-content: flex-start;
    border-radius: 100px;
    align-items: center;
    position: relative;
    padding: 1px 1px;
    display: flex;
    height: 20px;
    width: 100%;
  }

  .progress-value {
    animation: load 3s normal forwards;
    box-shadow: 0 10px 40px -10px rgba(58, 219, 9, 0.144);
    background: rgb(31, 148, 2);
    border-radius: 100px;
    height: 100%;
  }

  .bigRed {
    color: rgb(165, 27, 27);
    font-weight: bold;
  }
  .bigGreen {
    color: rgb(23, 197, 38);
    font-weight: bold;
  }
  .bigOrange {
    color: rgb(255, 165, 0);
    font-weight: bold;
  }
  .bigGray {
    color: rgb(17, 55, 70);
    font-weight: bold;
  }
</style>