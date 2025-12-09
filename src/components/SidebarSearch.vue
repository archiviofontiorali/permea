<script setup lang="ts">
import { onMounted } from 'vue'
import { FaPlusCircle } from 'vue-icons-plus/fa'

import { useSPARQLStore } from '@/stores/sparql'

import SidebarSearchForm from './SidebarSearchForm.vue'

const sparql = useSPARQLStore()

onMounted(() => {
  sparql.updateNamespaces()
  sparql.updateProperties()
})
</script>

<template>
  <aside :class="$attrs.class" class="bg-slate-300">
    <section id="search-form" class="p-2 grid gap-2">
      <sidebar-search-form
        :key="index"
        :name="`query-${index}`"
        v-model:property="q.property"
        v-model:value="q.value"
        v-model:operation="q.operation"
        v-for="(q, index) in sparql.queries"
        @delete="sparql.queries.splice(index, 1)"
      />
      <button
        class="p-1 outline-1 active:outline-2 flex flex-row justify-center"
        @click="sparql.addQuery()"
      >
        <fa-plus-circle />
      </button>
      <button class="p-1 outline-1 active:outline-2" @click="sparql.search(sparql.queries)">
        Search
      </button>
    </section>
    <section id="search-results">
      <p class="text-nowrap overflow-scroll" :key="index" v-for="(r, index) in sparql.results">
        {{ r.property.value }} | {{ r.value.value }}
      </p>
    </section>
  </aside>
</template>

<style scoped>
#search-form {
  grid-template-columns: 1fr auto 2fr auto;
}
</style>
