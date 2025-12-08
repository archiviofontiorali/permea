<script setup lang="ts">
import { reactive } from 'vue'

import HeaderDebug from './components/HeaderDebug.vue'
import MainBoard from './components/MainBoard.vue'
import MainNavbar from './components/MainNavbar.vue'
// import SearchPage from './SearchPage.vue'

import { useStorageStore } from './stores/storage'
import { useViewStore } from './stores/view'

interface State {
  debug: boolean
  search: boolean
}

const state = reactive<State>({ debug: false, search: false })

const view = useViewStore()
const storage = useStorageStore()
</script>

<template>
  <main-navbar
    class="absolute w-full h-10 z-50 bg-primary-700"
    :search="state.search"
    :debug="state.debug"
    @toggle-search="state.search = !state.search"
    @toggle-debug="state.debug = !state.debug"
  ></main-navbar>

  <div class="absolute w-full z-20 top-10" v-if="state.debug">
    <header-debug>
      Nodes: {{ storage.nodes.length }} | Edges: {{ storage.edges.length }}
    </header-debug>
    <header-debug>{{ view.$state }}</header-debug>
    <header-debug>{{ state }}</header-debug>
  </div>

  <main-board />

  <!-- <SearchPage /> -->
</template>

<style>
#app {
  /*background-color: var(--color-slate-700);*/
  height: 100vh;
  min-height: 100vh;
  max-height: 100vh;
  overflow: hidden;
}
</style>

<style scoped></style>
