<script setup lang="ts">
import Canvas from './components/CanvasModule.vue'
</script>

<template>
  <Canvas class="w-full h-full debug" />
</template>

<style>
.debug {
  /* var(--color-purple-500) with opacity: 0.5 */
  background-color: hsla(273.41, 100%, 63.73%, 0.5);
}

#app {
  min-height: 100vh;
}
</style>
