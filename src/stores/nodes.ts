import { sample } from 'underscore'
import { defineStore } from 'pinia'
import { DemoConfig } from '@/constants'

import { v6 as uuid } from 'uuid'

/** The canvasColor type is used to encode color data for nodes and edges. Colors attributes expect a string. Colors can be specified in hex format e.g. "#FF0000", or using one of the preset colors,  */
export type Color = string
export type Side = 'top' | 'right' | 'bottom' | 'left'
export type End = 'arrow' | 'none'

// For specifics about implementation go to https://jsoncanvas.org/spec/1.0/
export interface GenericNode {
  id: string
  type: 'text' | 'file' | 'link' | 'group'
  x: number
  y: number
  width: number
  height: number
  color?: Color
}

export interface TextNode extends GenericNode {
  type: 'text'
  text: string
}
export interface LinkNode extends GenericNode {
  type: 'link'
  url: string
}
// export interface FileNode extends Node { file: string, subpath?: string }
// export interface GroupNode extends Node { ... }

export type Node = TextNode | LinkNode

// For specifics about implementation go to https://jsoncanvas.org/spec/1.0/
export interface EdgePatch {
  /** is the node id where the connection starts. */
  fromNode?: string
  fromSide?: Side
  fromEnd?: End // default: none

  /** is the node id where the connection ends. */
  toNode?: string
  toSide?: Side
  toEnd?: End // default: arrow

  color?: Color
  label?: string
}
export interface EdgeCreate extends EdgePatch {
  fromNode: string
  toNode: string
}
export interface Edge extends EdgeCreate {
  id: string
}

export const useCanvasStore = defineStore('canvas', {
  state: () => {
    return {
      nodes: [] as Node[],
      edges: [] as Edge[],
    }
  },
  getters: {},
  actions: {
    // Node related CRUD methods and other
    createNode() {
      throw Error('Not Implemented')
    },
    getNode(id: string): Node {
      const result = this.nodes.find((item) => item.id === id)
      if (result === undefined) throw Error()
      return result
    },
    updateNode() {
      throw Error('Not Implemented')
    },
    deleteNode() {
      throw Error('Not Implemented')
    },
    moveNode(id: string, x: number, y: number) {
      const node = this.getNode(id)
      node.x = x
      node.y = y
    },
    moveNodeRelative(id: string, dx: number = 0, dy: number = 0) {
      const node = this.getNode(id)
      node.x += dx
      node.y += dy
    },
    // Edge related CRUD methods
    createEdge(edge: EdgeCreate) {
      this.edges.push({ id: uuid(), ...edge })
    },
    getEdge(id: string) {
      const result = this.edges.find((item) => item.id === id)
      if (result === undefined) throw Error()
      return result
    },
    updateEdge(id: string, patch: EdgePatch) {
      Object.assign(this.getEdge(id), patch)
    },
    deleteEdge(id: string) {
      const index = this.edges.findIndex((item) => item.id === id)
      this.edges.splice(index, 1)
    },
    // Demo related stuff
    demoSetup() {
      const nNodes = this.nodes.length
      for (let i = 0; i < DemoConfig.nodes; i++) {
        const node: Node = {
          id: uuid(),
          type: 'text',
          x: Math.floor((2 * Math.random() - 1) * DemoConfig.offset),
          y: Math.floor((2 * Math.random() - 1) * DemoConfig.offset),
          width: DemoConfig.nodeWidth,
          height: DemoConfig.nodeHeight,
          text: 'Hello World',
        }
        if (nNodes + i > 0)
          this.edges.push({
            id: uuid(),
            fromNode: (sample(this.nodes) || node).id,
            toNode: node.id,
            fromSide: sample<Side[]>(DemoConfig.fromSideValues as Side[]),
            toSide: sample<Side[]>(DemoConfig.toSideValues as Side[]),
          })
        this.nodes.push(node)
      }
    },
  },
})
