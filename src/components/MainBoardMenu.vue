<script setup lang="ts">
import {
  FiCrosshair,
  FiZoomIn,
  FiZoomOut,
  FiCircle,
  FiTarget,
  FiPlusCircle,
} from 'vue-icons-plus/fi'

import { useViewStore } from '@/stores/view'
import { useStorageStore } from '@/stores/storage'

const storage = useStorageStore()
const view = useViewStore()
</script>

<template>
  <!-- Menu for canvas position and sizing -->
  <header :class="$attrs.class" class="pb-2 gap-2 bottom-2 flex justify-center">
    <button @click="storage.demoSetup()" class="debug"><FiPlusCircle /></button>
    <button @click="view.zoomIn()"><FiZoomIn /></button>
    <button @click="view.axes = !view.axes">
      <FiCrosshair v-if="view.axes" />
      <FiCircle v-else />
    </button>
    <button @click="view.reset()"><FiTarget /></button>
    <button @click="view.zoomOut()"><FiZoomOut /></button>
  </header>
</template>

<style scoped>
@reference "@/style.css";

button {
  background-color: var(--color-white);
  border-radius: var(--radius-xl);
  padding: var(--radius-xl);

  @apply text-primary-700 border-2 border-primary;
}
button.debug {
  @apply text-purple-500 border-purple-500;
}
</style>
