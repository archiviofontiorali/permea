<script setup lang="ts"></script>

<template>
  <header
    id="header-debug"
    class="pa-2 bg-debug font-mono flex justify-around"
    :class="$attrs.class"
  >
    <slot />
  </header>
</template>
