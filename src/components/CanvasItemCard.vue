<script setup lang="ts">
import type { LODItem } from './CanvasModule.vue'

const { item } = defineProps<{ item: LODItem }>()
</script>

<template>
  <article id="card" class="flex flex-col justify-between align-middle text-center">
    {{ item.title }}
  </article>
</template>

<style scoped></style>
