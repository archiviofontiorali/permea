<script setup lang="ts">
import { useSPARQLStore } from '@/stores/sparql'
import { computed } from 'vue'
import { FaTrash } from 'vue-icons-plus/fa'

const sparql = useSPARQLStore()

const { name } = defineProps<{ name: string }>()

const property = defineModel('property')
const value = defineModel('value')
const operation = defineModel('operation')

const emit = defineEmits<{ delete: [] }>()

const pName = computed(() => `property-${name}`)
const oName = computed(() => `operation-${name}`)
const properties = computed(() => [...sparql.properties].sort())
</script>

<template>
  <select :id="pName" :name="pName" v-model="property" class="p-1 outline-1">
    <option :key="index" :value="p" v-for="(p, index) in properties">{{ p }}</option>
  </select>
  <select :id="oName" :name="oName" class="p1 outline-1 text-center" v-model="operation">
    <option value="eq">eq</option>
    <option value="in">in</option>
  </select>
  <input v-model="value" class="p-1 outline-1" />
  <section class="icons text-primary-700 flex flex-row gap-2 justify-end items-center">
    <fa-trash class="active:text-primary" @click="emit('delete')" />
  </section>
</template>

<style scoped>
div.icons > svg > path {
  stroke: white;
}
div.icons > :active {
  color: var(--color-primary-700);
}
</style>
