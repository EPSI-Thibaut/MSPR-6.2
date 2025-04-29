<script setup lang="ts">
import { defineProps } from 'vue'
import Skeleton from 'primevue/skeleton'

defineProps({
  type: {
    type: String,
    default: 'bar',
    validator: (value: string) => ['bar', 'pie', 'line'].includes(value),
  },
})
</script>

<template>
  <div class="bg-white shadow-lg rounded-xl p-6 mb-8 border border-gray-200">
    <Skeleton height="24px" width="350px" class="mb-6" />

    <div v-if="type === 'pie'" class="flex justify-center">
      <Skeleton shape="circle" size="300px" class="mb-2" />
    </div>

    <div v-else-if="type === 'bar'" class="flex flex-col gap-4">
      <Skeleton v-for="i in 7" :key="i" height="40px" />
    </div>

    <div v-else-if="type === 'line'">
      <Skeleton height="300px" class="mb-2" />
    </div>
  </div>
</template>
