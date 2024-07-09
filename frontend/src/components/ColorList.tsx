import { HSLColor } from "../interfaces"
import { hsl2rgb } from "./hslToRgbColor"

interface NibProps {
  color: HSLColor
  onClick: ()=>void
  active: boolean
}
const ColorNib = ({color, onClick, active}:NibProps) => {
  const [r,g,b] = hsl2rgb(color.h, color.s, color.l)
  const fill = `rgb(${r},${g},${b})`
  return <button className={active ? 'active' : undefined} onClick={onClick}
    style={{padding:'0.35em', lineHeight:0}}>
    <svg viewBox="0 0 100 100" height='1.55em'>
      <circle cx="50" cy="50" r="50" fill={fill}></circle>
    </svg>
  </button>
}

interface Props {
  colors: HSLColor[]
  setColors: (x:HSLColor[])=>void
  selected: number
  selectColor: (x:HSLColor, i:number)=>void
}
const ColorList = ({colors, setColors, selected, selectColor}:Props) => {
  if (colors.length == 0) {
    colors = [{h:0, s:100, l:0}]
  }
  const addColor = () => {
    const i = colors.length
    const c = [...colors]
    if (selected == undefined) selected = i-1
    const h = (c[selected].h + 360/12) % 360
    const s = c[selected].s
    const l = c[selected].l
    c.splice(selected+1, 0, {h,s,l})
    setColors(c)
    selectColor(c[selected+1],selected+1)
  }
  const delColor = () => {
    const c = [...colors]
    if (selected == undefined) selected = c.length-1
    c.splice(selected, 1)
    setColors(c)
    const i = Math.max(Math.min(selected-1, c.length-1),0)
    selectColor(c[i], i)
  }
  const plusMinusStyle = {
    fontWeight: 'bold',
    fontSize: 'x-large',
    padding: '0em 0.5em 0.15em 0.5em',
  }
  const plusDisabled = colors.length >= 12
  const minusDisabled = colors.length <= 1
  return (
    <div style={{display:'flex', gap:'0.25em', alignItems:'center', justifyContent:'space-between'}}>
      <div style={{display:'flex', gap:'0.25em', alignItems:'center', minHeight:'6em', maxWidth:'18em', flexWrap:'wrap'}}>
        {colors.map((x,i)=><ColorNib key={i} active={i==selected} color={x} onClick={()=>selectColor(x,i)}/>)}
      </div>
      <div style={{display:'flex', flexDirection:'column', gap:'0.25em'}}>
        <button disabled={plusDisabled} style={plusMinusStyle} onClick={addColor}>+</button>
        <button disabled={minusDisabled} style={plusMinusStyle} onClick={delColor}>-</button>
      </div>
    </div>
  )
}
export default ColorList