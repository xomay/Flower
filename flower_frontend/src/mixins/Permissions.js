export const Permissions = {
  methods: {
    isAdmin () {
      return this.$store.currentUser.roles.includes("ROLE_ADMIN")
    },
    isCA () {
      return this.$store.currentUser.roles.includes("ROLE_CA")
    },
    isTreso () {
      return this.$store.currentUser.roles.includes("ROLE_TRESO")
    },
    isSI () {
      return this.$store.currentUser.roles.includes("ROLE_SI")
    },
    isRea () {
      return this.$store.currentUser.roles.includes("ROLE_REA")
    }
  }
}
