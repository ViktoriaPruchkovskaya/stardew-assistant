import { useState } from 'react';
import SettingsButton from './SettingsButton';
import SettingsWindow from './SettingsWindow';

export default function SettingsWrapper() {
    const [isOpen, setIsOpen] = useState<boolean>(false)
    return (<div>
        <div className="flex justify-end-safe">
            <SettingsButton handleOnClick={() => setIsOpen(true)} />
        </div>
        {
            isOpen && (<>
                <div
                    className="fixed inset-0 bg-[rgba(0,0,0,0.3)]  backdrop-blur-sm z-40 transition-colors duration-200"
                />
                <div className='flex justify-center items-center'>
                    <SettingsWindow onSettingsSave={() => setIsOpen(false)} />
                </div>
            </>)
        }
    </div >)

}