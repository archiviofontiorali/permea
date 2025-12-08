<script setup lang="ts">
import { useViewStore } from '@/stores/view'

const view = useViewStore()
</script>

<template>
  <header
    id="header-debug"
    class="pa-2 bg-debug font-mono flex justify-around"
    :class="$attrs.class"
    :v-if="view.debug"
  >
    {{ view.$state }}
  </header>
</template>
