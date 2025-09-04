<script setup lang="ts">
import interact from 'interactjs'
import { ref } from 'vue'

const position = ref({ x: 0, y: 0 })

interact('#canvas-background').draggable({
  listeners: {
    start: (event) => console.log(event),
    move(event) {
      position.value.x += event.dx
      position.value.y += event.dy
    },
  },
})
</script>

<template>
  <svg id="canvas-background" class="absolute w-full h-full bg-black">
    <pattern
      id="canvas-background-pattern"
      :x="position.x"
      :y="position.y"
      width="20"
      height="20"
      patternUnits="userSpaceOnUse"
      patternTransform="translate(-0.5, -0.5)"
    >
      <circle cx="0.5" cy="0.5" r="0.5" fill="white"></circle>
    </pattern>
    <rect
      width="100%"
      height="100%"
      transform="translate(10, 10)"
      fill="url(#canvas-background-pattern)"
    ></rect>
  </svg>
</template>
