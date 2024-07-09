import { useState } from 'react'
import './App.css'
import ColorPicker from './components/ColorPicker'
import SpeedPicker from './components/SpeedPicker'
import ColorList from './components/ColorList'
import { HSLColor } from './interfaces'
import DirectionPicker from './components/DirectionPicker'
import { hsl2rgb } from './components/hslToRgbColor'

const periodToSpeed = (ms:number) => ms == 0 ? 0 : Math.ceil((1100-ms)/100)*10
const speedToPeriod = (speed:number) => speed == 0 ? 0 : 1100-(Math.ceil(speed/10)*100)

function App() {
  const [colorList, setColorList] = useState<HSLColor[]>([])
  const [color, _setColor] = useState({h:0, s:100, l:100})
  const [speed, setSpeed] = useState(100)
  const [direction, setDirection] = useState(1)
  const [index, setIndex] = useState(0)

  const selectColor = (x:HSLColor, i:number) => {
    setIndex(i)
    _setColor(x)
  }
  const setColor = (x:HSLColor) => {
    const c = [...colorList]
    c[index] = x
    setColorList(c)
    _setColor(x)
  }

  const config = {
    colors: colorList.map(({h,s,l})=>{
      const [r,g,b] = hsl2rgb(h, s, l)
      const n = r<<16 | g<<8 | b | 0x1000000
      return '#' + n.toString(16).substring(1)
    }),
    period_ms: speedToPeriod(speed),
    direction,
  }

  return (<>
    <div className='section'>
      <ColorList colors={colorList} setColors={setColorList} selected={index} selectColor={selectColor}/>
      <ColorPicker color={color} setColor={setColor}/>
      <SpeedPicker speed={speed} setSpeed={setSpeed}/>
      <DirectionPicker direction={direction} setDirection={setDirection}/>
    </div>
    <pre style={{textAlign:'left'}}>{JSON.stringify(config,null,2)}</pre>
  </>)
}

export default App
