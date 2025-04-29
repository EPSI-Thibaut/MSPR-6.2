<script setup lang="ts">
import HeaderMenu from '@/components/HeaderMenu.vue'
import FooterMenu from '@/components/Footer.vue'
</script>

<template>
  <!-- Header -->
  <HeaderMenu />

  <!-- Contenu principal -->
  <div class="min-h-screen p-2">
    <!-- Router View pour afficher les différentes pages -->
    <router-view />
  </div>

  <!-- Footer -->
  <FooterMenu />
</template>
