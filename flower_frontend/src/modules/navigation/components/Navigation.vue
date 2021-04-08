<template>
  <div class="flex min-h-screen">
    <el-menu
      class="menuNavBar flex-shrink-0 min-h-screen"
      background-color="#34495e"
      text-color="#fff"
      :unique-opened="true"
      :collapse="collapse"
    >
      <router-link to="/">
        <el-menu-item index="dashboard">
          <img
            class="inline-block"
            src="@/assets/logo_longueur_crop.png"
            style="max-width: 100%"
          >
        </el-menu-item>
      </router-link>
      <template v-for="(item, index) in menu">
        <el-submenu
          v-if="item.children.length > 0"
          :key="index"
          :index="index.toString()"
        >
          <template slot="title">
            <i :class="item.icon" />
            <span slot="title">{{ item.title }}</span>
          </template>
          <span
            v-for="(subItem, subIndex) in item.children"
            :key="subIndex"
          >
            <el-menu-item-group
              v-if="subItem.title"
              :title="subItem.title"
            >
              <router-link
                v-for="(subSubItem, subSubIndex) in subItem.children"
                :key="subSubIndex"
                :to="subSubItem.url"
              ><el-menu-item :index="subSubItem.url">{{ subSubItem.name }}</el-menu-item></router-link>
            </el-menu-item-group>
            <router-link
              v-else
              :to="subItem.url"
            ><el-menu-item :index="subItem.url">{{ subItem.name }}</el-menu-item></router-link>
          </span>
        </el-submenu>
      </template>
    </el-menu>
    <div class="flex-grow">
      <div class="topbar flex justify-between bg-blue-100">
        <el-button
          type="default"
          class="dark"
          @click="collapse = ! collapse"
        >
          <i
            v-if="collapse"
            class="el-icon-s-unfold"
          /><i
            v-else
            class="el-icon-s-fold"
          />
        </el-button>
        <el-dropdown
          trigger="click"
          @command="handleCommand"
        >
          <el-button
            type="default"
            class="dark"
          >
            <i class="el-icon-s-tools" />
          </el-button>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="profile">
              <i class="el-icon-user" />{{ this.$store.currentUser.username }}
            </el-dropdown-item>
            <el-dropdown-item command="logout">
              <i class="el-icon-close" />Se déconnecter
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
      <router-view />
    </div>
  </div>
</template>

<script>
const axios = require("axios")
import { Permissions } from "@/mixins/Permissions"
export default {
  name: "Navigation",
  mixins: [Permissions],
  data () {
    return {
      menu: [],
      collapse: false
    }
  },
  created () {
    // Accès selon les droits
    this.addCAStuff()
    this.addTresoStuff()
    this.addAdminStuff()
    // Accès réa :
    this.addReaStuff()
  },
  methods: {
    // Correspond aux inputs du dropdown (l'écrou en haut à droite)
    handleCommand (command) {
      if (command === "logout") {
        this.logout()
      } else if (command === "profile") {
        this.$router.push("/profil")
      }
    },
    // Méthode pour se déconnecter du site puis retourner à l'accueil
    logout () {
      axios.get(
        "/api/accounts/logout",
        {withCredentials: true}
      ).then(() => {
        this.$router.push("/login")
      }).catch(() => {
        this.$message({message: "Une erreur est survenue lors de la déconnexion", type: "error"})
      })
    },
    // Si l'utilisateur a des droits d'admin, ajoute ses outils dans la navbar
    addAdminStuff () {
      if ( this.isAdmin() ) {
        this.menu.push({
          icon: "el-icon-setting",
          title: "Administration",
          children: [
            {
              title: "Général",
              children: [
                {name: "Paramètres de la JE",
                  url: "/administration/params"},
                {name: "Liste des postes",
                  url: "/administration/postes"},
                {name: "Gérer les uploads",
                  url: "/administration/uploads"}
              ]
            }
          ]
        })
      }
    },
    // Si l'utilisateur a des droits de trésorier, ajoute ses outils dans la navbar
    addTresoStuff () {
      if ( this.isTreso() ) {
        this.menu.push({
          icon: "el-icon-money",
          title: "Trésorerie",
          children: [
            {
              title: "Études (trésorerie)",
              children: [
                {name: "Gérer les études", url: "/tresorerie/etudes/"},
              ]
            },
            {
              title: "Notes de Frais",
              children: [
                {name: "Lister les NFs", url: "/tresorerie/nfs/voir/"},
                {name: "Ajouter une NF", url: "/tresorerie/nfs/ajouter"},
              ]
            },
            {
              title: "Autres",
              children: [
                {name: "Base Ursaff", url: "/tresorerie/base-ursaff"},
              ]
            }
          ]
        })
      }
    },
    // Si l'utilisateur a des droits de CA, ajoute ses outils dans la navbar
    addCAStuff () {
      if (this.isCA() ) {
        this.menu.push({
          icon: "el-icon-user-solid",
          title: "Gestion Associative",
          children: [
            {
              title: "Membres",
              children: [
                {name: "Lister les membres",
                  url: "/membres"},
                {name: "Ajouter un membre",
                  url: "/membres/ajouter"}
              ]
            },
            {
              title: "Intervenants",
              children: [
                {name: "Lister les réalisateurs",
                  url: "/realisateurs"},
                {name: "Ajouter un réalisateur",
                  url: "/realisateurs/ajouter"}
              ]
            }
          ]
        },
        {
          icon: "el-icon-s-management",
          title: "Suivi d'Etude",
          children: [
            {name: "Voir les études",
              url: "/etudes"},
            {name: "Créer une étude",
              url: "/etudes/ajouter"}
          ]
        },
        {
          icon: "el-icon-data-line",
          title: "Performance",
          children: [
            {name: "Suivi Dev'co",
              url: "/performance/devco"}
          ]
        },
        {
          icon: "el-icon-s-custom",
          title: "Prospection",
          children: [
            {
              title: "Prospects",
              children: [
                {name: "Voir les prospects",
                  url: "/prospects"},
                {name: "Ajouter un prospect",
                  url: "/prospects/ajouter"}
              ]
            },
            {
              title: "Actions commerciales",
              children: [
                {name: "Voir les actions commerciales",
                  url: "/prospects/actionCommerciale/"},
                {name: "Créer une action commerciale",
                  url: "/prospects/actionCommerciale/ajouter"}
              ]
            },
            {
              title: "Génération",
              children: [
                {name: "Devis",
                  url: "/generation/devis"}
              ]
            }
          ]
        })
      }
    },
    // Si l'utilisateur a des droits de réalisateur, ajoute ses outils dans la navbar
    addReaStuff () {
      if ( this.isRea() ) {
        this.menu.push({
          icon: "el-icon-folder-opened",
          title: "Mes études",
          children: [
            {
              title: "Accès réalisateur",
              children: [
                {name: "Liste de mes études", url: "/etudes/acces-rea"},
              ]
            }
          ]
        })
      }
    }
  }
}
</script>

<style scoped>
.menuNavBar:not(.el-menu--collapse) {
  width: 16rem;
}
div.topbar {
  background-color: #2c3e50;
}
div.topbar button {
  height: 40px;
  font-size: 20px;
  @apply py-0 px-4 !important;
}
.el-menu-item, .el-submenu__title {
  height: 40px !important;
  line-height: 40px !important;
}
ul {
  @apply border-0;
}
</style>
