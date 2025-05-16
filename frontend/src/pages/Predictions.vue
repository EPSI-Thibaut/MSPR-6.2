<script setup lang="ts">
import { ref, watchEffect } from 'vue';
import Chart from 'primevue/chart';
import { usePandemicData } from '@/composables/usePandemicData';

const {
  predictions,
  fetchPredictions,
  loading,
  error,
} = usePandemicData();

const chartData = ref<any>(null);
const chartOptions = ref<any>(null);

watchEffect(() => {
  if (predictions.value && predictions.value.length > 0) {
    const sorted = [...predictions.value].sort((a, b) => new Date(a.predictionDate).getTime() - new Date(b.predictionDate).getTime());
    const labels = sorted.map((item: any) => item.predictionDate);
    const cases = sorted.map((item: any) => item.predictedCases ?? null);
    const deaths = sorted.map((item: any) => item.predictedDeaths ?? null);
    const recovered = sorted.map((item: any) => item.predictedRecovered ?? null);

    chartData.value = {
      labels,
      datasets: [
        {
          label: 'Cas prédits',
          data: cases,
          borderColor: '#42A5F5',
          backgroundColor: 'rgba(66,165,245,0.2)',
          tension: 0.3,
          fill: false,
        },
        {
          label: 'Décès prédits',
          data: deaths,
          borderColor: '#E53935',
          backgroundColor: 'rgba(229,57,53,0.2)',
          tension: 0.3,
          fill: false,
        },
        {
          label: 'Guérisons prédites',
          data: recovered,
          borderColor: '#43A047',
          backgroundColor: 'rgba(67,160,71,0.2)',
          tension: 0.3,
          fill: false,
        },
      ],
    };
    chartOptions.value = {
      responsive: true,
      plugins: {
        legend: {
          display: true,
          labels: {
            color: '#222',
            font: { size: 14 }
          }
        },
        title: {
          display: true,
          text: 'Prédictions COVID 2023 (Cas, Décès, Guérisons)',
          font: { size: 18 }
        },
        tooltip: {
          mode: 'index',
          intersect: false,
        },
      },
      interaction: {
        mode: 'nearest',
        axis: 'x',
        intersect: false
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Date',
            color: '#222',
            font: { size: 14 }
          },
          ticks: {
            color: '#222',
            maxTicksLimit: 12,
            autoSkip: true
          }
        },
        y: {
          title: {
            display: true,
            text: 'Nombre',
            color: '#222',
            font: { size: 14 }
          },
          ticks: {
            color: '#222',
            callback: (value: number) => value.toLocaleString('fr-FR')
          }
        }
      }
    };
  }
});

fetchPredictions();
</script>


<template>
  <div>
    <h1>Prédictions COVID</h1>
    <div v-if="loading" class="p-mt-4">Chargement des données...</div>
    <div v-else>
      <div v-if="error" class="p-mt-4" style="color: red;">{{ error }}</div>
      <Chart v-else-if="chartData" type="line" :data="chartData" :options="chartOptions" style="min-height:400px" />
      <div v-else class="p-mt-4">Aucune donnée de prédiction disponible.</div>
    </div>
  </div>
</template>
