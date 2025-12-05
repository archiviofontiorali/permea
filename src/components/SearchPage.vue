<script setup lang="ts">
import axios from 'axios'
import { reactive } from 'vue'

function ns(value: string): string {
  return value
    .replace(`http://localhost:8000/api/`, 'permea:')
    .replace('http://www.w3.org/1999/02/22-rdf-syntax-ns#', 'rdf-syntax:')
    .replace('http://www.w3.org/2000/01/rdf-schema#', 'rdf-schema:')
    .replace('http://purl.org/dc/terms/', 'dcterms:')
    .replace('http://omeka.org/s/vocabs/o#', 'omeka:')
}

interface Query {
  property: string
  value: string
  operation: 'eq' | 'in'
}

interface Result {
  resource: { value: string }
  property: { value: string }
  value: { value: string }
}

const properties = ['omeka:title', 'dcterms:title']
const query = reactive<Query[]>([{ property: 'omeka:title', value: '', operation: 'eq' }])
const results = reactive<Result[]>([])

function search() {
  // const endpoint = 'http://localhost:8080/sparql'
  const endpoint = 'http://localhost:3030/triplestore/sparql'

  const constraints = query.map(
    (q, index) => `?resource ${q.property} ${q.value ? `"${q.value}"` : `?value${index}`} .`,
  )
  const q = `
    PREFIX omeka:   <http://omeka.org/s/vocabs/o#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX fuseki:  <http://jena.apache.org/fuseki#>
    PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX tdb2:    <http://jena.apache.org/2016/tdb#>
    PREFIX tdb1:    <http://jena.hpl.hp.com/2008/tdb#>
    PREFIX ja:      <http://jena.hpl.hp.com/2005/11/Assembler#>
    PREFIX :        <#>

    SELECT ?resource ?property ?value
    WHERE {
        ?resource ?property ?value .
        ${constraints.join('\n')}
    }
    ORDER BY ASC(?resource)
    LIMIT 10
  `
  // const q = 'SELECT * WHERE { ?resource ?property ?value . } LIMIT 10'

  const params = { params: { query: q, format: 'json' } }
  axios
    .get(endpoint, params)
    .then((response) => {
      console.debug(response.data)
      results.push(...response.data.results.bindings)
    })
    .catch(console.error)
    .finally(() => console.debug(q))
}
</script>

<template>
  <aside class="absolute w-[50%] h-full p-8 bg-slate-700 z-10">
    <section id="search-form" class="grid grid-cols-2 gap-4">
      <template :key="index" v-for="(q, index) in query">
        <select
          :name="`query-${index}`"
          :id="`query-${index}`"
          v-model="q.property"
          class="p-1 bg-yellow-500"
        >
          <option
            :value="p"
            :selected="p === q.property"
            :key="index"
            v-for="(p, index) in properties"
          >
            {{ p }}
          </option>
        </select>

        <input v-model="q.value" class="p-1 bg-red-400" />
      </template>

      <button class="bg-green-700 active:bg-green-500" @click="search">Search</button>
    </section>

    <section class="text-white grid grid-cols-3 gap-2">
      <template :key="index" v-for="(r, index) of results">
        <div class="py-2 overflow-auto">{{ ns(r.resource.value) }}</div>
        <div class="py-2 overflow-auto">{{ ns(r.property.value) }}</div>
        <div class="py-2 overflow-auto">{{ ns(r.value.value) }}</div>
      </template>
    </section>
  </aside>
</template>

<style scoped></style>
