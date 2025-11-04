import {} from 'vue'
import { defineStore } from 'pinia'

/** The canvasColor type is used to encode color data for nodes and edges. Colors attributes expect a string. Colors can be specified in hex format e.g. "#FF0000", or using one of the preset colors,  */
type canvasColor = string
type canvasSide = 'top' | 'right' | 'bottom' | 'left'

// For specifics about implementation go to https://jsoncanvas.org/spec/1.0/
export interface AbstractNode {
  id: string
  type: 'text' | 'file' | 'link' | 'group'
  x: number
  y: number
  width: number
  height: number
  color?: canvasColor
}
export interface TextNode extends AbstractNode {
  type: 'text'
  text: string
}
export interface LinkNode extends AbstractNode {
  type: 'link'
  url: string
}
// export interface FileNode extends Node { file: string, subpath?: string }
// export interface GroupNode extends Node { ... }

export type Node = TextNode | LinkNode

// For specifics about implementation go to https://jsoncanvas.org/spec/1.0/
export interface Edge {
  id: string

  /** is the node id where the connection starts. */
  fromNode: string
  fromSide?: canvasSide
  fromEnd?: 'none' | 'arrow' // default: none

  /** is the node id where the connection ends. */
  toNode: string
  toSide?: canvasSide
  toEnd?: 'none' | 'arrow' // default: arrow

  color?: canvasColor
  label?: string
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
    getNodeById(id: string) {
      return this.nodes.find((item) => item.id === id)
    },
    asMap() {
      this.nodes.reduce((acc, item) => ({ ...acc, [item.id]: item }), {})
    },
    demoSetup() {
      for (let i = 0; i < 3; i++)
        this.nodes.push({
          id: `card-${i}`,
          type: 'text',
          x: Math.floor(Math.random() * 100),
          y: Math.floor(Math.random() * 100),
          width: 200,
          height: 300,
          text: 'Hello World',
        })
    },
    moveNode(id: string, x: number, y: number) {
      const node = this.getNodeById(id)
      if (node === undefined) throw Error()

      node.x = x
      node.y = y
    },
  },
})
