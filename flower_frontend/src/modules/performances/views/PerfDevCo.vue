<template>
  <BaseComponent
    title="Performance - Dev'co"
    :breadcrumb="breadcrumb"
  >
    <h1>
      Il n'y a pas encore grand chose pour le moment...
    </h1>
    <div>
      Revenez plus tard ! :D
    </div>
  </BaseComponent>
</template>

<script>

export default {
  name: "PerfDevCo",
  data () {
    return {
      breadcrumb: [
        {
          name: "Performances Dev'co",
          link: "/performances dev'co"
        }
      ]
    }
  }
}
</script>