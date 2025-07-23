import { ReactNode } from "react";

interface SettingsButtonProps {
    handleOnClick: () => void;
    children: ReactNode
}

export default function SettingsButton({ handleOnClick, children }: SettingsButtonProps) {
    return (
        <button onClick={handleOnClick} className="flex items-center justify-center
                 h-10 w-10 sm:h-12 sm:w-12
                 p-2 bg-amber-400 border-2 border-yellow-600 rounded-md
                 hover:bg-amber-500 transition cursor-pointer">
            {children}
        </button>
    )
}
