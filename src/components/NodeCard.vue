<script setup lang="ts">
import type { Node } from '@/stores/storage'
import { computed } from 'vue'

const { node } = defineProps<{ node: Node }>()
const title = computed(() => {
  return node.metadata ? node.metadata.get('dcterms:title')?.value || node.id : node.id
})
</script>

<template>
  <header class="flex flex-col justify-between align-middle text-center">
    <p class="text-xs text-left">{{ node.type }}</p>
    <h1>{{ title }}</h1>
  </header>
</template>

<style scoped></style>
