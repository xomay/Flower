<template>
  <BaseComponent
    title="Voir le réalisateur"
    :breadcrumb="breadcrumb"
  >
    <!--( Nom prénom )-->
    <table class="styled-table">
      <tbody>
        <tr>
          <td class="rowStyle noRight">
            {{ realisateur.gender }}. {{ realisateur.firstname }} {{ realisateur.lastname }}
          </td>
        </tr>
      </tbody>
    </table>
    <!--( Infos importantes )-->
    <table class="styled-table">
      <tbody>
        <tr>
          <td>
            <i class="el-icon-notebook-2 percent" />
          </td>
          <td class="rowStyle">
            Promotion
          </td>
          <td>{{ realisateur.promotion }}</td>
        </tr>
        <tr>
          <td>
            <i class="el-icon-first-aid-kit percent" />
          </td>
          <td class="rowStyle">
            N° de sécurité sociale
          </td>
          <td>{{ realisateur.security_social_number }}</td>
        </tr>
        <tr>
          <td>
            <i class="el-icon-folder-opened percent" />
          </td>
          <td
            class="rowStyle"
          >
            Fillière
          </td>
          <td>
            <font
              class="fontStyled"
            >
              {{ realisateur.filiere }}
            </font>
          </td>
        </tr>
      </tbody>
    </table>
    <!--( Contacts )-->
    <table class="styled-table">
      <tbody>
        <tr>
          <td>
            <i class="el-icon-message percent" />
          </td>
          <td class="rowStyle">
            Email
          </td>
          <td>{{ realisateur.email }}</td>
        </tr>
        <tr>
          <td>
            <i class="el-icon-message percent" />
          </td>
          <td class="rowStyle">
            Email INSA
          </td>
          <td>{{ realisateur.email_insa }}</td>
        </tr>
        <tr>
          <td>
            <i class="el-icon-phone percent" />
          </td>
          <td class="rowStyle">
            Mobile
          </td>
          <td>{{ realisateur.mobile }}</td>
        </tr>
      </tbody>
    </table>
    <!--( Infos osef )-->
    <table class="styled-table">
      <tbody>
        <tr>
          <td>
            <i class="el-icon-map-location percent" />
          </td>
          <td class="rowStyle">
            Addresse
          </td>
          <td>{{ realisateur.address+", "+realisateur.town+" ("+realisateur.postcode+")" }}</td>
        </tr>
        <tr>
          <td>
            <i class="el-icon-date percent" />
          </td>
          <td class="rowStyle">
            Date de naissance
          </td>
          <td>{{ realisateur.birth_date }}</td>
        </tr>
        <tr>
          <td>
            <i class="el-icon-location-outline percent" />
          </td>
          <td class="rowStyle">
            Lieu de naissance
          </td>
          <td>{{ realisateur.birth_place }}</td>
        </tr>
      </tbody>
    </table>
  </BaseComponent>
</template>

<script>
const axios = require("axios")

export default {
  name: "RealisateursVoir",
  data () {
    return {
      realisateur: {},
      loading: true,
      breadcrumb: [
        {
          name: "Liste des réalisateurs",
          link: "/realisateurs"
        },
        {
          name: "<loading>",
          link: `/realisateurs/${this.$route.params.id}/voir`
        }
      ]
    }
  },
  beforeCreate () {
    this.loading = true
    axios.get(
      `/api/realisateurs/${this.$route.params.id}`,
      {withCredentials: true}
    ).then((res) => {
      this.realisateur = res.data
      this.breadcrumb[1].name = `${this.realisateur.firstname} ${this.realisateur.lastname}`
    }).catch((err) => {
      this.$message({message: "Impossible de récupérer le réalisateur pour le moment : " + err,
        type: "error",
        offset: 40})
    }).finally(() => {
      this.loading = false
    })
  },
  methods: {
    getRatingColor (rating) {
      if(rating < 1) {
        return "red"
      } else if(rating < 3) {
        return "orange"
      } else {
        return "green"
      }
    },
    niceArray (array) {
      var str = ""
      const MAX = 5
      var count = 1
      for (const c of array) {
        if(str !== "")
          str += ", "
        if(count > MAX) {
          const remaining = array.length - MAX
          str += remaining + " autre"+(remaining>1?"s":"")+"."
          break
        }
        str += c
        count ++
      }
      return str
    }
  }
}
</script>

<style>
  .styled-table {
    border-collapse: collapse;
    margin: 25px 0;
    font-size: 0.9em;
    font-family: sans-serif;
    min-width: 40%;
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
