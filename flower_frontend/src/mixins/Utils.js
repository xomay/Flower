export default {
  methods: {
    // @param 'date': date de format dd-mm-yyyy
    // @returns une date de format yyyy/mm/dd
    niceDate (date) {
      if(date == undefined || date == "")
        return ""
      const tokens = date.split("-", 3)
      return tokens[2] + "/" + tokens[1] + "/" + tokens[0]
    },
    nicePeople (entity) {
      if(entity == undefined)
        return "undefined"
      return entity.firstname + " " + entity.lastname
    },
    displayPoste (membre) {
      if(membre.poste == undefined)
        return ""
      if(membre.gender == "Mme.") {
        if(membre.poste.name_feminine != "") {
          return membre.poste.name_feminine
        }
      }
      return membre.poste.name
    },
    // @returns date formatted as yyyy-mm-dd
    generateDateToday () {
      return this.generateDate(new Date())
    },
    generateDate (date) {
      return date.getFullYear() +"-"+ (date.getMonth() < 9 ? "0" : "")+ (date.getMonth()+1) +"-"+(date.getDate() < 10 ? "0" : "")+ (date.getDate())
    },
    // @returns today's last two digits of the year. ("21" if the year is 2021)
    generateYearDigits () {
      const date_now = new Date()
      return String(date_now.getFullYear()).slice(-2)
    },// @returns today's last two digits of the month. ("05" if the year is may)
    generateMonthDigits () {
      const date_now = new Date()
      return String((date_now.getMonth() < 9 ? "0" : "")+ (date_now.getMonth()+1)).slice(-2)
    },// Get date in format yyy-mm-dd and @returns dd/mm/yyyy
    sqlToDisplayDate (date) {
      if(date == null)
        return "[ERREUR: date non défine.]"
      const tokens = date.split("-")
      return tokens[2] + "/" + tokens[1] + "/" + tokens[0]
    },
    niceFileSize (size) {
      if(size < 1000)
        return size + " o"
      else if(size < 1000000)
        return (size / 1000).toFixed(2) + " Ko"
      else if(size < 1000000000)
        return (size / 1000000).toFixed(2) + " Mo"
      else
        return (size / 1000000000).toFixed(2) + " Go"
    },
    // À utiliser en 'formatter' dans les tableaux.
    // Renvoie la valeur normale suivie de ' €'.
    euroFormatter (row, column, cellValue) {
      return Number(cellValue).toFixed(2) + " €"
    },
    niceDateFormatter (row, column, cellValue) {
      return this.niceDate(cellValue)
    },
    arrayAmountFormatter (row, column, cellValue) {
      return cellValue.length
    },
    // Date utils
    addDaysToDate (date, days) {
      var result = new Date(date)
      result.setDate(result.getDate() + days)
      return result
    },
  }
}
