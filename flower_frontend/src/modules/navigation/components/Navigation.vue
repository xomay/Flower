<template>
  <div class="flex min-h-screen">
    <el-menu
      ref="menu"
      class="menuNavBar flex-shrink-0 min-h-screen"
      background-color="#EBEBEB"
      text-color="#000"
      active-text-color="#1351aa"
      :unique-opened="true"
      :collapse="collapse"
      :default-active="$route.path"
      router
    >
    <el-row class="menuItem" :style="collapse ? 'justify-content: center;' : 'justify-content: space-between;'">
      <router-link to="/">
        <el-menu-item v-if="!collapse" index="/" class="logo-menu-item" style="display: flex; justify-content: flex-start;">
          <img
          src="@/assets/logo_bold.png"
          class="logoImg"
          >
        </el-menu-item>
      </router-link>
        <el-button
        type="default"
        @click="collapse = !collapse;"
        size="large"
        style="height: 56px; width: 56px; border: 0;"
        class="logo-menu-item"
        >
          <el-icon color="#000"><component :is="collapse ? 'DArrowRight' : 'DArrowLeft'" /></el-icon>
        </el-button>
    </el-row>
      <template v-for="(item, index) in menu" :key="index">
        
          <router-link
            v-if="!item.children || item.children.length === 0"
            :key="index"
            :index="index.toString()"
            :to="item.url"
          >
            <el-menu-item :index="item.url">
              <el-icon><component :is="item.icon" /></el-icon>
              <template #title><b>{{ item.title }}</b></template>
            </el-menu-item>
          </router-link>
        <el-sub-menu
          v-if="item.children ? item.children.length > 0 : false"
          :key="index"
          :index="index.toString()"
        >
          <template #title>
            <el-icon><component :is="item.icon" /></el-icon>
            <span><b>{{ item.title }}</b></span>
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
        </el-sub-menu>
      </template>
      
      <!-- Dropdown utilisateur en bas du menu -->
      <div class="user-dropdown-container">
        <el-dropdown
          trigger="click"
          @command="handleCommand"
          placement="top-start"
        >
          <el-button
            type="info"
            plain
            class="user-dropdown-btn"
          >
            <el-icon><UserFilled /></el-icon>
            <span v-if="!collapse" class="user-name">{{ this.$store.currentUser.user.name }}</span>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">
                <el-icon><User /></el-icon>{{ this.$store.currentUser.user.name }}
              </el-dropdown-item>
              <el-dropdown-item command="logout">
                <el-icon><Close /></el-icon>Se déconnecter
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-menu>
    <div class="flex-grow">
      <div class="topbar flex justify-between bg-blue-100">
      </div>
      <router-view />
    </div>
  </div>
</template>

<script>
const axios = require("axios")
import { Permissions } from "@/mixins/Permissions"
import Ticket from "../../performances/views/Ticket.vue"
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
    this.addPiousCAStuff()
    this.addCAStuff()
    this.addTresoStuff()
    this.addAdminStuff()
    // Accès réa :
    this.addReaStuff()
    // Si écran pas assez large, on replie le menu
    if (window.innerWidth < 1405) {
      this.collapse = true
    }
  },
  watch: {
    $route(to) {
      // Force la mise à jour de l'état actif quand la route change
      this.$nextTick(() => {
        const menu = this.$refs.menu
        if (menu) {
          menu.activeIndex = to.path
        }
      })
    }
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
          icon: "Tools",
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
                  url: "/administration/uploads"},
                {name: "Gérer les doctypes",
                  url: "/administration/doctypes"}
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
          icon: "Money",
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
    // Si l'utilisateur a des droits de Pious, ajoute ses outils dans la navbar
    addPiousCAStuff () {
      if (this.isPious() || this.isCA() ) {
        /*this.menu.push({
          icon: "Monitor",
          title: "Simulation",
          children: [
            {
              title: "Membres",
              children: [
                {name: "Gestion Associative",
                  url: "/simulation/membres"}
              ]
            },
            {
              title: "Affaires",
              children: [
                {name: "Suivi d'Etude",
                  url: "/simulation/etudes"}
              ]
            },
            {
              title: "Dev'Co",
              children: [
                {name: "Prospection",
                  url: "/simulation/prospects"}
              ]
            }
          ]
        })*/
       this.menu.push({
          icon: "UserFilled",
          title: "Gestion Associative",
          url: "/membres"
        },
        {
          icon: "Files",
          title: "Suivi d'Etude",
          url: "/etudes"
        },
        {
          icon: "Phone",
          title: "Prospection",
          url: "/prospects"
        })
      }
    },
    // Si l'utilisateur a des droits de CA, ajoute ses outils dans la navbar
    addCAStuff () {
      if (this.isCA() ) {
        this.menu.push(
        {
          icon: "DataLine",
          title: "Performance",
          url: "/performance/devco" 
        },
        {
          icon: "ChatDotSquare",
          title: "Signalement",
          url: "/performance/ticket"
        })
      }
    },
    // Si l'utilisateur a des droits de réalisateur, ajoute ses outils dans la navbar
    addReaStuff () {
      if ( this.isRea() ) {
        this.menu.push({
          icon: "FolderOpened",
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
.logoImg {
  max-height: 100%; 
  max-width: 60%;
  margin: 0;
}
.menuItem {
  display: flex; 
  flex-wrap: nowrap; 
  align-items: center; 
  margin-bottom: 20px;
  margin-top: 5px;
}
.menuNavBar:not(.el-menu--collapse) {
  width: 16rem;
  border-right: 1.5px solid #D7D7D7;
}

.menuNavBar {
  position: relative;
  display: flex;
  flex-direction: column;
}
div.topbar {
  background-color: #ffffff;
  display: flex;
  justify-content: flex-end;

}
div.topbar button {
  height: 40px;
  font-size: 20px;
  padding: 0 16px !important;
}
ul {
  border: 0;
}

.user-dropdown-container {
  position: sticky;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 10px;
  background-color: #EBEBEB;
  border-top: 1px solid #D7D7D7;
  margin-top: auto;
  z-index: 1000;
}

.user-dropdown-btn {
  width: 100%;
  justify-content: flex-start !important;
  background-color: transparent !important;
  border: none !important;
  color: #000 !important;
  padding: 8px 12px !important;
}

.user-dropdown-btn:hover {
  background-color: rgba(0, 0, 0, 0.1) !important;
}

.user-name {
  margin-left: 8px;
  font-size: 14px;
}

/* Enlever l'effet hover du logo */
.logo-menu-item:hover {
  background-color: transparent !important;
}

.logo-menu-item.is-active {
  background-color: transparent !important;
}

.logo-menu-item {
  background-color: transparent !important;
}
</style>
