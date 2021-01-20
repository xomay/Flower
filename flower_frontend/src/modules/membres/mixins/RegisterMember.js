export const registerMemberMixin = {
  methods: {
    mixinRegisterMember (axios, member) {
      axios.put(
        `/api/membres/openaccount/${member.id}/`,
        {},
        {withCredentials: true}
      ).then((res) => {
        member.user = { username: res.data.username }
        this.$message({message: `Le compte utilisateur [${res.data.username}] a bien été créé.`, type: "success"})
      }).catch((err) => {
        this.$message({message: err, type: "error"})
      })
    }
  }
}
