<script setup lang="ts">
import Map3D from '@/components/Map3D.vue'
</script>

<template>
  <!-- Titre principal -->  
  <h2 class="text-3xl text-gray-700 mb-6 text-center">Statistiques du COVID et SARS</h2>

  <!-- Carte 3D avec un cadre arrondi -->
  <div class="bg-black shadow-xl rounded-2xl p-8 mb-4 border border-gray-200"
  aria-label="Carte 3D des cas de COVID-19 dans le monde"
  role="region"
  >
    <Map3D />
  </div>
</template>
