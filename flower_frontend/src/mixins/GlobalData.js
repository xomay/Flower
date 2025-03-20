export default {
  methods: {
    queryData (axios, value) {
      return axios.get(
        `/api/administration/params/${value}/`,
        { withCredentials: true }
      )
    }
  }
}
