import { useContext } from "react"
import { ThemeContext } from "../../contexts/themeContext"

interface SettingsWindowProps {
    onSettingsSave: () => void
}

export default function SettingsWindow({ onSettingsSave }: SettingsWindowProps) {
    const { isDark, setIsDark } = useContext(ThemeContext)!

    return (
        <div className="absolute w-100 bg-amber-100 border-4 border-yellow-700 rounded-lg shadow-lg px-4 py-3 font-press-start text-lg text-yellow-900 z-50">
            <h2 className="text-xl mb-2 text-center">Settings</h2>
            <label className='flex justify-start text-sm'>
                <span>Dark theme</span>
                <div onClick={() => setIsDark(prev => !prev)} className='bg-amber-400 w-14 h-6 border-1 border-yellow-600 rounded-xs cursor-pointer'>
                    <div className={`w-5.5 h-5.5 bg-yellow-900 rounded-xs transition-transform duration-300 ${isDark ? 'translate-x-8' : 'translate-x-0'}`} />
                </div>
            </label>
            <div className='flex justify-center'>
                <button type='button' onClick={onSettingsSave} className="min-w-30 mt-2 py-1 bg-amber-400 border-2
                 border-yellow-600 hover:bg-yellow-400 rounded-md shadow-sm cursor-pointerbg-amber-400 cursor-pointer">
                    Close
                </button>
            </div>
        </div>
    )

}
