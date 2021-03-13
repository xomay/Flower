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
    // À utiliser en 'formatter' dans les tableaux.
    // Renvoie la valeur normale suivie de ' €'.
    euroFormatter (row, column, cellValue) {
      return cellValue + " €"
    },
    niceDateFormatter (row, column, cellValue) {
      return this.niceDate(cellValue)
    }
  }
}
