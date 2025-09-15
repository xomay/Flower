<template>
  <el-table :data="etudes" style="width: 80vw;">
    <el-table-column
      prop="name"
      label="Étude"
      width="150"
      fixed
    >
      <template #default="{ row }">
        <el-button
          type="text"
          @click="clicked(row.id)"
        >
          {{ row.name }}
        </el-button>
      </template>
    </el-table-column>

    <el-table-column label="Phases" :width="calculateTimelineWidth()">
      <template #default="{ row }">
        <div style="position: relative; min-height: 140px; border-bottom: 1px solid #ccc;">
          <!-- Repères de dates -->
          <div
            v-for="(date, i) in timelineMarkers"
            :key="i"
            :style="{
              position: 'absolute',
              left: calculateLeft(date) + 'px',
              top: '0px',
              fontSize: '12px',
              color: '#333',
              whiteSpace: 'nowrap'
            }"
          >
            {{ formatDate(date) }}
          </div>

          <!-- Ligne rouge (base date) -->
          <div
            :style="{
              position: 'absolute',
              left: '140px',
              top: '0',
              height: '100%',
              width: '2px',
              backgroundColor: 'red',
              zIndex: 10
            }"
          />

          <!-- Phases de l'étude -->
          <div
            v-for="(phase, index) in row.phases.filter(p => new Date(p.finishDate) >= baseDate)"
            :key="phase.id"
            :style="{
              position: 'absolute',
              left: isPhaseOngoing(phase) ? '0px' : calculateLeft(phase.beginDate) + 'px',
              width: calculateWidth(phase.beginDate, phase.finishDate) - 25 + 'px',
              backgroundColor: '#3CACB6',
              height: '100px',
              top: '20px',
              margin: '10px 100px 10px 0',
              padding: '10px',
              borderTopRightRadius: '10px',
              borderBottomRightRadius: '10px',
              borderTopLeftRadius: isPhaseOngoing(phase) ? '0px' : '10px',
              borderBottomLeftRadius: isPhaseOngoing(phase) ? '0px' : '10px'
            }"
            :title="phase.title"
          >
            <span style="color: white; font-size: medium;">
              Phase {{ index + 1 }} - {{ formatDate(phase.beginDate) }} au {{ formatDate(phase.finishDate) }}
            </span>
            <br />
            <span style="color: white; font-size: medium; white-space: nowrap;">
              <b>{{ phase.title }}</b>
            </span>
            <br />
            <span style="color: white; font-size: medium;">
              {{ Math.ceil(phase.period / 7) }} semaines - {{ phase.nbJEH }} JEH - {{ phase.totalPrice }} HT
            </span>
          </div>
        </div>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
export default {
  name: "EtudesDashboard",
  props: {
    etudes: { type: Array, required: true }
  },
  data() {
    return {
      dayWidth: 20,
      baseDate: new Date(new Date().setDate(new Date().getDate() - 7)),
      timelineMarkers: [],
    }
  },
  created() {
    const bounds = this.getTimelineBounds(this.etudes);
    const start = new Date(this.baseDate);
    const end = new Date(bounds.end);
    end.setDate(end.getDate() + 14);
    const markers = [];

    let cursor = new Date(start);

    while (cursor <= end) {
      markers.push(new Date(cursor));
      cursor.setDate(cursor.getDate() + 7);
    }

    this.timelineMarkers = markers;
  },
   watch: {
    etudes () {
      this.etudes.forEach(etude => {
        var beginDate = etude.docEtude?.signDate || new Date();
        etude.phases.forEach(phase => {
          phase.beginDate = this.truncateStart(beginDate);
          phase.finishDate = new Date(phase.beginDate);
          phase.finishDate.setDate(phase.finishDate.getDate() + phase.period);
          phase.totalPrice = phase.nbJEH * phase.priceJEH;
          beginDate = new Date(phase.finishDate);
        });
      });
      const bounds = this.getTimelineBounds(this.etudes);
      const start = new Date(this.baseDate);
      const end = new Date(bounds.end);
      end.setDate(end.getDate() + 14);
      const markers = [];

      let cursor = new Date(start);

      while (cursor <= end) {
        markers.push(new Date(cursor));
        cursor.setDate(cursor.getDate() + 7);
      }

      this.timelineMarkers = markers;
    }
  },
  methods: {
    clicked (id) {
      this.$emit("select", id)
    },
    truncateStart(dateStr) {
      const start = new Date(dateStr);
      return start < this.baseDate ? this.baseDate : start;
    },
    calculateLeft(start) {
      const date = new Date(start);
      if (date < this.baseDate) return 0;
      const diff = (date - this.baseDate) / (1000 * 3600 * 24);
      return diff * this.dayWidth;
    },
    calculateWidth(start, end) {
      const realStart = new Date(start) < this.baseDate ? this.baseDate : new Date(start);
      const diff = (new Date(end) - realStart) / (1000 * 3600 * 24) + 1;
      return diff * this.dayWidth;
    },
    isPhaseOngoing(phase) {
      const start = new Date(phase.beginDate);
      return start < this.baseDate;
    },
    getTimelineBounds(studies) {
      let minDate = null;
      let maxDate = null;

      studies.forEach(study => {
        study.phases.forEach(phase => {
          const start = new Date(phase.beginDate);
          const end = new Date(phase.finishDate);

          if (!minDate || start < minDate) {
            minDate = start;
          }

          if (!maxDate || end > maxDate) {
            maxDate = end;
          }
        });
      });

      return {
        start: minDate,
        end: maxDate
      };
    },
    formatDate(date) {
      const d = new Date(date)
      return d.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit' })
    },
    calculateTimelineWidth() {
      let maxDate = null;

      this.etudes.forEach(etude => {
        etude.phases.forEach(phase => {
          const end = new Date(phase.finishDate);
          if (!maxDate || end > maxDate) {
            maxDate = end;
          }
        });
      });

      if (!maxDate) return 0;

      maxDate.setDate(maxDate.getDate() + 14);

      const diffInDays = Math.ceil((maxDate - this.baseDate) / (1000 * 60 * 60 * 24));
      return diffInDays * this.dayWidth;
    },
  }
}
</script>

<style scoped>
body {
  margin: 0;
  padding: 0;
  overflow: hidden;
}
</style>
