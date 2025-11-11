<script setup lang="ts">
import type { Node } from '@/stores/nodes'

const { node } = defineProps<{ node: Node }>()
</script>

<template>
  <article class="card flex flex-col justify-between align-middle text-center">
    {{ node.type }} -- {{ node.id }}<br />
    ({{ node.x.toFixed(2) }}, {{ node.y.toFixed(2) }})
  </article>
</template>

<style scoped></style>
