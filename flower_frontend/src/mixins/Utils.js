export default {
  methods: {
    // @param 'date': date de format dd-mm-yyyy
    // @returns une date de format yyyy/mm/dd
    niceDate (date) {
      const tokens = date.split("-", 3)
      return tokens[2] + "/" + tokens[1] + "/" + tokens[0]
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
