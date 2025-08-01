import { useContext } from "react"
import { ThemeContext } from "../../contexts/themeContext"

export default function ThemeToggle() {
    const { isDark, setIsDark } = useContext(ThemeContext)!

    return (
        <div className='flex justify-start text-sm'>
            <span>Dark theme</span>
            <div onClick={() => setIsDark(prev => !prev)} className='bg-amber-400 ml-1 w-14 h-6 border-1 border-yellow-600 rounded-xs cursor-pointer'>
                <div className={`w-5.5 h-5.5 bg-yellow-900 rounded-xs transition-transform duration-300 ${isDark ? 'translate-x-8' : 'translate-x-0'}`} />
            </div>
        </div>
    )

}