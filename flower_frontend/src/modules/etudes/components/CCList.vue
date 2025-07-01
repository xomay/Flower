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
      </template>
    </el-table-column>
    <el-table-column
      prop="number"
      label="Numéro de la CC"
      align="center"
      fixed="left"
      width="180px"
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
      width="120px"
    >
    <template #default="{row}">
        <router-link :to="`/cc/${row.id}/modifier`">
        <el-button
          :disabled="row.isFinished"
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
      width="120px"
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
      width="120px"
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
  </el-table>
</template>

<script>
import Utils from "@/mixins/Utils"
import Publishing from "@/mixins/Publishing"

export default {
  name: "CCList",
  mixins: [Utils, Publishing],
  props: {
    ccs: {type : Array, required: true },
    loading: {type : Boolean, required: true },
    discret: {type : Boolean, default () { return false } }
  },
  watch: {
    ccs () {
      const today = new Date();

      this.ccs.forEach(cc => {
        const signDate = new Date(cc.signDate);
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
    clicked (id) {
      this.$emit("select", id)
    },
    getPercentage (state) {
      if(state == undefined)
        return "width: 0%"
      return "width: "+(state*10)+"%"
    },
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
  .bigGray {
    color: rgb(17, 55, 70);
    font-weight: bold;
  }
</style>