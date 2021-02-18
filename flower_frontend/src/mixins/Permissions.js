export const Permissions = {
  methods: {
    isAdmin () {
      return this.$store.currentUser.roles.includes("ROLE_ADMIN")
    },
    isUser () {
      return this.$store.currentUser.roles.includes("ROLE_CA")
    },
    isTreso () {
      return this.$store.currentUser.roles.includes("ROLE_TRESO")
    },
    isSI () {
      return this.$store.currentUser.roles.includes("ROLE_SI")
    }
  }
}
