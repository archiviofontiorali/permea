<script setup lang="ts">
import Board from '@/components/BoardCanvas.vue'
</script>

<template>
  <Board class="w-full h-full" />
</template>

<style>
#app {
  background-color: var(--color-slate-700);
  min-height: 100vh;
  max-height: 100vh;
  overflow: hidden;
}
</style>

<style scoped></style>
