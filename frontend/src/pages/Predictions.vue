<script setup lang="ts">
import { ref, watchEffect } from 'vue';
import Chart from 'primevue/chart';
import Button from 'primevue/button';
import ProgressSpinner from 'primevue/progressspinner';
import { usePandemicData } from '@/composables/usePandemicData';
import axios from 'axios';

const {
  predictions,
  fetchPredictions,
  loading,
  error,
} = usePandemicData();

const chartData = ref<any>(null);
const chartOptions = ref<any>(null);

// Points clés séparés
const keyCasesData = ref<any>(null);
const keyCasesOptions = ref<any>(null);
const keyDeathsData = ref<any>(null);
const keyDeathsOptions = ref<any>(null);
const keyRecoveredData = ref<any>(null);
const keyRecoveredOptions = ref<any>(null);

const training = ref(false);
const trainingMessage = ref('');

async function launchTraining() {
  training.value = true;
  trainingMessage.value = '';
  try {
    const res = await axios.post('/api/train_predict');
    trainingMessage.value = res.data.message || 'Entraînement terminé.';
    await fetchPredictions();
  } catch (err: any) {
    trainingMessage.value = err.response?.data?.message || 'Erreur lors de l’entraînement du modèle IA.';
  } finally {
    training.value = false;
  }
}

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

    // Points clés séparés
    const maxCases = Math.max(...cases);
    const minCases = Math.min(...cases);
    const maxDeaths = Math.max(...deaths);
    const minDeaths = Math.min(...deaths);
    const maxRecovered = Math.max(...recovered);
    const minRecovered = Math.min(...recovered);

    keyCasesData.value = {
      labels: ['Cas max', 'Cas min'],
      datasets: [
        {
          label: 'Cas 2023',
          backgroundColor: ['#42A5F5', '#90CAF9'],
          data: [maxCases, minCases]
        }
      ]
    };
    keyCasesOptions.value = {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { display: true, text: 'Points clés - Cas', font: { size: 16 } }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            color: '#222',
            callback: (value: number) => value.toLocaleString('fr-FR')
          }
        },
        x: { ticks: { color: '#222' } }
      }
    };

    keyDeathsData.value = {
      labels: ['Décès max', 'Décès min'],
      datasets: [
        {
          label: 'Décès 2023',
          backgroundColor: ['#E53935', '#FFCDD2'],
          data: [maxDeaths, minDeaths]
        }
      ]
    };
    keyDeathsOptions.value = {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { display: true, text: 'Points clés - Décès', font: { size: 16 } }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            color: '#222',
            callback: (value: number) => value.toLocaleString('fr-FR')
          }
        },
        x: { ticks: { color: '#222' } }
      }
    };

    keyRecoveredData.value = {
      labels: ['Guérisons max', 'Guérisons min'],
      datasets: [
        {
          label: 'Guérisons 2023',
          backgroundColor: ['#43A047', '#A5D6A7'],
          data: [maxRecovered, minRecovered]
        }
      ]
    };
    keyRecoveredOptions.value = {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { display: true, text: 'Points clés - Guérisons', font: { size: 16 } }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            color: '#222',
            callback: (value: number) => value.toLocaleString('fr-FR')
          }
        },
        x: { ticks: { color: '#222' } }
      }
    };
  }
});

fetchPredictions();
</script>





<template>
<div>
  <h1>Prédictions COVID</h1>
</div>
</template>



