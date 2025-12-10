<script setup lang="ts">
import { useSPARQLStore, type Binding } from '@/stores/sparql'
import { onMounted, reactive, ref } from 'vue'

interface Table {
  headers: string[]
  rows: Binding[]
}

const query = ref<string>('SELECT ?s ?v ?o WHERE { ?s ?v ?o . }')
const table: Table = reactive({ headers: [], rows: [] })
const errors: string[] = reactive([])

const sparql = useSPARQLStore()

onMounted(() => {
  sparql.updateNamespaces()
  sparql.updateProperties()
})

function search(query: string) {
  errors.splice(0)
  sparql
    .query(query)
    .then((response) => {
      table.headers = response.head.vars
      table.rows = response.results.bindings
    })
    .catch((error) => errors.push(error.response.data))
}
</script>

<template>
  <aside :class="$attrs.class" class="bg-slate-300">
    <section id="search-form" class="p-2 grid gap-2 w-full">
      <textarea name="query" id="query" v-model="query" class="outline-1 min-h-50" />
      <button class="p-1 outline-1 active:outline-2" @click="search(query)">Search</button>
    </section>
    <section id="search-results" class="w-full overflow-x-auto">
      <p class="border-2 border-red-800" :key="index" v-for="(e, index) of errors">{{ e }}</p>
      <table class="table-auto">
        <thead>
          <th :key="h" v-for="h in table.headers">{{ h }}</th>
        </thead>
        <tbody>
          <tr :key="i" v-for="(row, i) in table.rows" class="_w-full">
            <td :key="j" v-for="(b, j) in row" class="px-2 text-nowrap">
              <a
                class="link block text-nowrap overflow-x-auto max-w-[40ch]"
                :href="b.value"
                v-if="b.type === 'uri'"
                >{{ sparql.namespace(b.value) }}</a
              >
              <template v-else>{{ b.value }}</template>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </aside>
</template>
