import { HSLColor } from "../interfaces"
import { HueSlider, LightnessSlider, SaturationSlider } from "../react-slider-color-picker"
import { Color as HSLAlphaColor } from "../react-slider-color-picker/interfaces"
import { hsl2rgb } from "./hslToRgbColor"

interface Props {
  color: HSLColor
  setColor: (c:HSLColor)=>void
  size?: string | number
}
const ColorPicker = ({color, setColor, size='3em'}:Props) => {
  const setHue = (c:HSLAlphaColor) => {
    c.h = Math.round(c.h/12)*12
    setColor(c)
  }
  const setSaturation = (c:HSLAlphaColor) => {
    c.s = Math.round(c.s/10)*10
    setColor(c)
  }
  const setLightness = (c:HSLAlphaColor) => {
    c.l = Math.round(c.l/10)*10
    setColor(c)
  }
  const [r,g,b] = hsl2rgb(color.h, color.s, color.l)
  const fill = `rgb(${r},${g},${b})`
  return <div style={{display:'flex', gap:'1em', alignItems:'center'}}>
    <svg viewBox="0 0 100 100" height={size} style={{minWidth:size}}>
      <circle cx="50" cy="50" r="50" fill={fill}></circle>
    </svg>
    <div style={{paddingTop: '.5em'}}>
      <HueSlider handleChangeColor={setHue} color={color as HSLAlphaColor} />
      <SaturationSlider handleChangeColor={setSaturation} color={color as HSLAlphaColor} />
      <LightnessSlider handleChangeColor={setLightness} color={color as HSLAlphaColor} />
    </div>
  </div>
}
export default ColorPicker