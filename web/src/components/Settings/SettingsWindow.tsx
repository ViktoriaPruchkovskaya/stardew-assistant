import SavedChats from "./SavedChats"
import SettingsButton from "./SettingsButton"
import ThemeToggle from "./ThemeToggle"

interface SettingsWindowProps {
    onSettingsClose: () => void
}


export default function SettingsWindow({ onSettingsClose }: SettingsWindowProps) {
    return (
        <div className="absolute top-0 left-0 w-full h-full z-50 flex items-center justify-center font-press-start">
            <div className="relative">
                <div className="absolute -top-15 -right-0 text-xl">
                    <SettingsButton handleOnClick={onSettingsClose}><span className=" text-xl">X</span></SettingsButton>
                </div>


                <div className="w-100 h-100 max-w-md bg-amber-100 border-4 border-yellow-700 rounded-lg shadow-lg px-4 py-3 text-xl text-yellow-900">
                    <h2 className="mb-2 text-center">Settings</h2>
                    <ThemeToggle />
                    <SavedChats onSettingsClose={onSettingsClose} />

                </div>
            </div>
        </div>


    )

}
