<template>
  <div>
    <span><u>Nom de l'action :</u> {{ actionCommerciale.name }}</span><br>
    <br>
    <span><u>Type d'action :</u> {{ getActionType (actionCommerciale.type) }}</span><br>
    <br>
    <span><u>Participants :</u> {{ participantsToContent (actionCommerciale.participants) }}</span><br>
    <br>
    <span><u>Nombre de rendez-vous issus de l'action :</u> {{ actionCommerciale.appointments }}</span><br>
    <span><u>Nombre d'études issues de l'action :</u> {{ actionCommerciale.studies }}</span><br>
  </div>
</template>

<script>
export default {
  name: "ACView",
  props: {
    actionCommerciale: { type: Object, required: true },
    membresList: { type: Array, required: true },
    actionsTypes: { type: Array, required: true }
  },
  methods: {
    getActionType (id) {
      const at = this.actionsTypes.find(a => a.id === id)
      return at == undefined ? "<ERROR>" : at.type
    },
    participantsToContent (array) {
      var str = ""
      if(array != undefined) {
        array.forEach(p => {
          if(str !== "")
            str += ", "
          str += this.getMembre(p)
        })
      }
      return str
    },
    getMembre (id) {
      const mb = this.membresList.find(m => m.id === id)
      return mb == undefined ? "<ERROR>" : mb.firstname + " " + mb.lastname
    }
  }
}
</script>
