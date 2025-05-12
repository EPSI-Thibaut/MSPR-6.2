<script setup lang="ts">
import ContinentsComparison from '../components/comparaison/ContinentsComparison.vue'
</script>

<template>
  <div class="p-4">
    <!-- Titre de la page -->
    <div class="mb-6">
      <h1 class="text-3xl font-bold mb-2">Analyse par continents</h1>
      <p>
        Comparaison détaillée de l'impact des pandémies SARS et COVID-19 par continent
      </p>
    </div>

    <!-- Composant de comparaison des continents -->
    <section role="region" aria-label="Comparaison des pandémies par continent">
      <ContinentsComparison />
    </section>
  </div>
</template>
