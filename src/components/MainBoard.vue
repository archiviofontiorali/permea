<script setup lang="ts">
import interact from 'interactjs'

import { computed, onMounted } from 'vue'

import MainBoardMenu from './MainBoardMenu.vue'
import NodeContainer from './NodeContainer.vue'
import EdgeContainer from './EdgeContainer.vue'
import EdgeBuilder from './EdgeBuilder.vue'

import { BackgroundGrid as BG } from '@/constants'
import { useViewStore } from '@/stores/view'

const view = useViewStore()

interact('#canvas-background').draggable({
  listeners: {
    move: (event) => {
      view.center.x += event.dx
      view.center.y += event.dy
    },
  },
})

const translateView = computed(() => ({
  transform: `translate(${view.center.x}px, ${view.center.y}px)`,
}))

const scaleTranslateView = computed(() => ({
  transform: `translate(${view.center.x}px, ${view.center.y}px) scale(${view.scale})`,
}))

onMounted(() => view.reset())
</script>

<template>
  <main-board-menu class="absolute z-20 navbar navbar-bottom" />

  <!-- Canvas Background -->
  <svg id="canvas-background" class="absolute w-full h-full bg-[#262626]">
    <pattern
      id="canvas-background-pattern"
      class="color-[#D1D1D1]"
      :x="view.center.x"
      :y="view.center.y"
      :width="BG.gap * view.scale"
      :height="BG.gap * view.scale"
      patternUnits="userSpaceOnUse"
      :patternTransform="`translate(-${BG.radius}, -${BG.radius})`"
    >
      <circle :cx="BG.radius" :cy="BG.radius" :r="BG.radius" fill="grey"></circle>
    </pattern>

    <rect width="100%" height="100%" fill="url(#canvas-background-pattern)"></rect>

    <g id="canvas-axes" :class="{ hidden: !view.axes }" :style="translateView">
      <circle cx="0" cy="0" r="7"></circle>
      <line x1="-40" x2="40" y1="0" y2="0" />
      <line x1="0" x2="0" y1="-40" y2="40" />
    </g>

    <g id="canvas-edges-wrapper" :style="scaleTranslateView">
      <EdgeContainer />
      <EdgeBuilder />
    </g>
  </svg>

  <!-- Canvas Card Nodes -->
  <section id="canvas-nodes-wrapper">
    <NodeContainer />
  </section>
</template>

<style scoped>
@reference "@/style.css";

svg g#canvas-axes line {
  stroke: var(--color-gray-500);
  stroke-width: 2;
}
svg g#canvas-axes circle {
  fill: var(--color-gray-500);
}

.navbar.navbar-bottom,
.navbar.navbar-top {
  left: 50%;
  transform: translate(-50%, 0);
}
</style>
