<script setup lang="ts">
defineProps({
  message: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <div class="bg-red-100 text-red-700 p-4 rounded-lg mb-6">
    {{ message }}
  </div>
</template>
