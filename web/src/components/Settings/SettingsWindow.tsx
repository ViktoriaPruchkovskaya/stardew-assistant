import { useContext } from "react"
import { ThemeContext } from "../../contexts/themeContext"
import SettingsButton from "./SettingsButton"

interface SettingsWindowProps {
    onSettingsClose: () => void
}

export default function SettingsWindow({ onSettingsClose }: SettingsWindowProps) {
    const { isDark, setIsDark } = useContext(ThemeContext)!

    return (
        <div className="absolute z-50">
            <div className="relative">
                <div className="absolute -top-15 -right-0 z-10">
                    <SettingsButton handleOnClick={onSettingsClose}><span className="font-press-start text-xl">X</span></SettingsButton>
                </div>
            </div>

            < div className="w-100 bg-amber-100 border-4 border-yellow-700 rounded-lg shadow-lg px-4 py-3 font-press-start text-lg text-yellow-900" >
                <h2 className="text-xl mb-2 text-center">Settings</h2>
                <label className='flex justify-start text-sm'>
                    <span>Dark theme</span>
                    <div onClick={() => setIsDark(prev => !prev)} className='bg-amber-400 ml-1 w-14 h-6 border-1 border-yellow-600 rounded-xs cursor-pointer'>
                        <div className={`w-5.5 h-5.5 bg-yellow-900 rounded-xs transition-transform duration-300 ${isDark ? 'translate-x-8' : 'translate-x-0'}`} />
                    </div>
                </label>
                <div className='flex justify-center'>
                </div>
            </div >
        </div >

    )

}
