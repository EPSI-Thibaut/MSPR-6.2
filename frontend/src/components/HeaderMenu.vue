<script setup lang="ts">
import Menubar from 'primevue/menubar'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const menuItems = ref([
  {
    label: 'Accueil',
    icon: 'pi pi-home',
    command: () => router.push('/'),
  },
  {
    label: 'Statistiques',
    icon: 'pi pi-chart-bar',
    command: () => router.push('/statistiques'),
  },
  {
    label: 'Comparaison COVID vs SRAS',
    icon: 'pi pi-chart-line',
    command: () => router.push('/comparaison'),
  },
  {
    label: 'Comparaison des continents',
    icon: 'pi pi-chart-line',
    command: () => router.push('/continents'),
  },
  {
    label: 'À propos',
    icon: 'pi pi-info-circle',
    command: () => router.push('/about'),
  },
])
</script>

<template>
  <header class="mb-2 text-gray-800 shadow-md rounded-lg">
    <Menubar :model="menuItems" class="rounded-lg" />
  </header>
</template>
