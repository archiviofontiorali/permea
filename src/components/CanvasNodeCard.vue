<script setup lang="ts">
import type { Node } from '../stores/nodes.ts'

const { node } = defineProps<{ node: Node }>()
</script>

<template>
  <article id="card" class="flex flex-col justify-between align-middle text-center">
    {{ node.type }} -- {{ node.id }}
  </article>
</template>

<style scoped></style>
