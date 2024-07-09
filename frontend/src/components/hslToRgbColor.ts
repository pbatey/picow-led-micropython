export const hsl2rgb = (h:number, s:number, l:number) => {
  s /= 100
  l /= 100
  const k = (n:number) => (n + h / 30) % 12
  const a = s * Math.min(l, 1 - l)
  const f = (n:number) =>
    l - a * Math.max(-1, Math.min(k(n) - 3, Math.min(9 - k(n), 1)))
  const r = 255 * f(0)
  const g = 255 * f(8)
  const b = 255 * f(4)
  return [r,g,b]
}
