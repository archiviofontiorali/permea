<script setup lang="ts">
import { FaSearch } from 'vue-icons-plus/fa'
import { Fa6HelmetSafety } from 'vue-icons-plus/fa6'

const state = defineProps<{ debug: boolean; search: boolean }>()

const emit = defineEmits<{
  'toggle-debug': []
  'toggle-search': []
}>()
</script>

<template>
  <nav :class="$attrs.class" class="text-white p-2 flex flex-row justify-between items-center">
    <fa-search :class="{ 'text-primary': !state.search }" @click="emit('toggle-search')" />
    <h1 class="text-xl">PerMeA</h1>
    <fa6-helmet-safety :class="{ 'text-primary': !state.debug }" @click="emit('toggle-debug')" />
  </nav>
</template>
