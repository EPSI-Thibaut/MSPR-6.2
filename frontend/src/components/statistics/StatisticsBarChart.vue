<script setup lang="ts">
import { defineProps, computed } from 'vue'
import Chart from 'primevue/chart'
import ChartSkeleton from './ChartSkeleton.vue'

const props = defineProps({
  countriesData: {
    type: Array as () => Array<{
      region: string
      deaths: number
      cases: number
      recovered?: number
    }>,
    required: true,
  },
  selectedPandemic: {
    type: Object,
    default: null,
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

// Données calculées pour le graphique en barres verticales
const barData = computed(() => ({
  labels: props.countriesData.map((country) => country.region),
  datasets: [
    {
      label: 'Morts',
      backgroundColor: '#FF6384',
      data: props.countriesData.map((country) => country.deaths),
    },
    {
      label: 'Cas',
      backgroundColor: '#36A2EB',
      data: props.countriesData.map((country) => country.cases),
    },
    {
      label: 'Guéris',
      backgroundColor: '#4BC0C0',
      data: props.countriesData.map((country) => country.recovered || 0),
    },
  ],
}))
</script>

<template>
  <div class="mb-8">
    <!-- Skeleton pendant le chargement -->
    <ChartSkeleton v-if="loading" type="bar" />

    <!-- Graphique réel quand chargé -->
    <div v-else class="bg-white shadow-lg rounded-xl p-6 mb-8 border border-gray-200">
      <h3 class="text-xl font-semibold text-gray-700 mb-4">
        Nombre de morts, cas ou guéris - {{ selectedPandemic?.name }}
      </h3>
      <Chart type="bar" :data="barData" class="w-full h-[400px]" />
    </div>
  </div>
</template>
