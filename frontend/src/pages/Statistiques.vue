<script setup lang="ts">
import { onMounted, watch } from 'vue'
import StatisticsFilters from '@/components/statistics/StatisticsFilters.vue'
import StatisticsPieChart from '@/components/statistics/StatisticsPieChart.vue'
import StatisticsBarChart from '@/components/statistics/StatisticsBarChart.vue'
import StatisticsTimelineChart from '@/components/statistics/StatisticsTimelineChart.vue'
import StatisticsComparisonChart from '@/components/statistics/StatisticsComparisonChart.vue'
import LoadingIndicator from '@/components/common/LoadingIndicator.vue'
import { usePandemicData } from '@/composables/usePandemicData'

// Récupérer toutes les données et fonctions liées aux pandémies
const {
  loading,
  error,
  pandemies,
  regions,
  selectedPandemic,
  selectedRegion,
  countriesData,
  allCountriesData,
  timelineData,
  comparisonData,
  loadingPandemicData,
  loadingTimelineData,
  loadingComparisonData,
  fetchPandemics,
  fetchRegions,
  fetchPandemicData,
  fetchTimelineData,
  fetchComparisonData,
} = usePandemicData()

// Observer les changements de sélection
watch([selectedPandemic, selectedRegion], () => {
  if (selectedPandemic.value && selectedRegion.value) {
    loadingPandemicData.value = true
    loadingTimelineData.value = true
    loadingComparisonData.value = true

    fetchPandemicData()
    fetchTimelineData()
    fetchComparisonData()
  }
})

// Charger les données initiales
onMounted(async () => {
  try {
    await Promise.all([fetchPandemics(), fetchRegions()])

    if (selectedPandemic.value && selectedRegion.value) {
      fetchPandemicData()
      fetchTimelineData()
      fetchComparisonData()
    }
  } catch (error) {
    console.error("Erreur lors de l'initialisation des données:", error)
  }
})
</script>

<template>
  <div class="p-6">
    <h2 class="text-3xl font-bold text-gray-800 mb-6 text-center">Statistiques des maladies</h2>

    <!-- Filtres (sélecteurs de pandémie et région) -->
    <StatisticsFilters
      :pandemies="pandemies"
      :regions="regions"
      v-model:selectedPandemic="selectedPandemic"
      v-model:selectedRegion="selectedRegion"
      :loading="loading"
    />

    <!-- Chargement initial des données -->
    <LoadingIndicator v-if="loading" message="Chargement des données..." />

    <!-- Message d'erreur global -->
    <div
      v-else-if="error"
      class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6"
    >
      <p>{{ error }}</p>
    </div>

    <!-- Message quand aucune sélection -->
    <div v-else-if="!selectedPandemic || !selectedRegion" class="text-center py-12">
      <p class="text-gray-600 text-lg">Veuillez sélectionner une pandémie et une région.</p>
    </div>

    <!-- Message quand aucune donnée n'est disponible -->
    <div v-else-if="countriesData.length === 0 && !loadingPandemicData" class="text-center py-12">
      <p class="text-gray-600 text-lg">Aucune donnée disponible pour cette pandémie.</p>
    </div>

    <!-- Spinner central pendant le chargement des données après sélection -->
    <LoadingIndicator
      v-else-if="loadingPandemicData && loadingTimelineData && loadingComparisonData"
      :fullScreen="true"
      message="Chargement des données..."
    />

    <!-- Contenu principal avec les graphiques -->
    <div v-else>
      <!-- Graphique en camembert -->
      <StatisticsPieChart
        :allCountriesData="allCountriesData"
        :selectedPandemic="selectedPandemic"
        :loading="loadingPandemicData"
      />

      <!-- Graphique en barres -->
      <StatisticsBarChart
        :countriesData="countriesData"
        :selectedPandemic="selectedPandemic"
        :loading="loadingPandemicData"
      />

      <!-- Graphique timeline -->
      <StatisticsTimelineChart
        v-if="timelineData.length > 0 || loadingTimelineData"
        :timelineData="timelineData"
        :selectedPandemic="selectedPandemic"
        :selectedRegion="selectedRegion"
        :loading="loadingTimelineData"
      />

      <!-- Graphique comparaison -->
      <StatisticsComparisonChart
        v-if="comparisonData || loadingComparisonData"
        :comparisonData="comparisonData"
        :pandemies="pandemies"
        :selectedRegion="selectedRegion"
        :loading="loadingComparisonData"
      />
    </div>
  </div>
</template>
