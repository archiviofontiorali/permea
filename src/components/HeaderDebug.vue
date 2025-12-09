<script setup lang="ts"></script>

<template>
  <header
    id="header-debug"
    class="p-1 bg-debug border-debug font-mono flex justify-around"
    :class="$attrs.class"
  >
    <slot />
  </header>
</template>
