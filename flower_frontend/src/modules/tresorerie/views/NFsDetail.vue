<template>
  <BaseComponent
    :title="title"
    :breadcrumb="breadcrumb"
  >
    <table class="styled-table">
      <tbody>
        <tr>
          <td>
            Demandeur : {{ nicePeople(nf.demandeur) }}
          </td>
          <td>
            Date : {{ niceDate(nf.date) }}
          </td>
        </tr>
      </tbody>
    </table>
  </BaseComponent>
</template>

<script>
const axios = require("axios")
import UtilsMixin from "@/mixins/Utils"
export default {
  name: "NFsVoir",
  mixins: [UtilsMixin],
  data () {
    return {
      nf: {},
      title: "NF <loading>",
      loading: true,
      breadcrumb: [
        {
          name: "Liste des NF normales",
          link: "tresorerie/nfs/voir/normales"
        },
        {
          name: "<loading>",
          link: `tresorerie/nfs/${this.$route.params.id}/voir/`
        }
      ]
    }
  },
  beforeCreate () {
    axios.get(
      `api/ndfs/${this.$route.params.id}/`,
      { withCredentials: true }
    ).then((res) => {
      this.nf = res.data
      this.breadcrumb[1].name = this.nf.reference
      this.title = "NF " + this.nf.reference
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer la NF : " + err, type: "error"})
    })
  }
}
</script>

<style>
  .styled-table {
    border-collapse: collapse;
    margin: 25px 0;
    font-size: 0.9em;
    font-family: sans-serif;
    min-width: 100%;
    box-shadow: 10px 5px 20px rgba(0, 0, 0, 0.15);
  }
  .styled-table thead tr {
    background-color: #009879;
    color: #ffffff;
    text-align: left;
  }
  .styled-table th,
  .styled-table td {
      padding: 12px 15px;
  }
  .styled-table tbody tr {
    border-bottom: 1px solid #dddddd;
  }

  .styled-table tbody tr:nth-of-type(even) {
      background-color: #f3f3f3;
  }
  .styled-table tbody tr.active-row {
      font-weight: bold;
      color: #009879;
  }
  .styled-table tbody tr td.rowStyle {
    border-right: solid 1px rgba(120, 120, 120, 0.8);
    text-align: center;
    font-weight: bold;
    width: 30%;
  }
  .styled-table tbody tr td.noRight {
    border-right: solid 0px;
  }
  .fontStyled {
    font: 1em "Lucida Console";
    background-color: lightgray;
    border-radius: .25em;
  }
  .percent {
    width: 5%;
  }
</style>
