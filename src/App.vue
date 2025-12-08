<script setup lang="ts">
import HeaderDebugView from './components/HeaderDebugView.vue'
import BoardCanvas from './components/BoardCanvas.vue'
</script>

<template>
  <header-debug-view class="absolute w-full z-20" />
  <BoardCanvas class="w-full h-full" />
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
