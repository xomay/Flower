export default {
  methods: {
    // @param 'date': date de format dd-mm-yyyy
    // @returns une date de format yyyy/mm/dd
    niceDate (date) {
      const tokens = date.split("-", 3)
      return tokens[2] + "/" + tokens[1] + "/" + tokens[0]
    }
  }
}
