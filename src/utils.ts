import type { Target } from '@/components/EdgePath.vue'
import type { Side } from '@/stores/nodes'

export function side(node: Target, dx: number, dy: number): Side | undefined {
  if (!node.width || !node.height) return undefined

  const [w, h] = [node.width, node.height]
  if (dy < Math.min((h / w) * dx, (-h / w) * dx)) return 'top'
  if (dy > Math.max((h / w) * dx, (-h / w) * dx)) return 'bottom'
  return dx > 0 ? 'right' : 'left'
}
