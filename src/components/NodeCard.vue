<script setup lang="ts">
import type { Node } from '@/stores/storage'

const { node } = defineProps<{ node: Node }>()
</script>

<template>
  <main class="flex flex-col justify-between align-middle text-center">
    {{ node.type }} -- {{ node.id }}<br />
    ({{ node.x.toFixed(2) }}, {{ node.y.toFixed(2) }})
  </main>
</template>

<style scoped></style>
