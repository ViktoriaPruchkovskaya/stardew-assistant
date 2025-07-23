import { useState } from 'react';
import SettingsButton from './SettingsButton';
import SettingsWindow from './SettingsWindow';

export default function SettingsWrapper() {
    const [isOpen, setIsOpen] = useState<boolean>(false)
    return (<div>
        <div className="flex justify-end-safe">
            <SettingsButton handleOnClick={() => setIsOpen(true)} >
                <svg fill="currentColor" className=" w-7 h-7 text-yellow-900" viewBox="0 0 1920 1920" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier"></g>
                    <g id="SVGRepo_tracerCarrier"></g>
                    <g id="SVGRepo_iconCarrier">
                        <path d="M1703.534 960c0-41.788-3.84-84.48-11.633-127.172l210.184-182.174-199.454-340.856-265.186 88.433c-66.974-55.567-143.323-99.389-223.85-128.415L1158.932 0h-397.78L706.49 269.704c-81.43 29.138-156.423 72.282-223.962 128.414l-265.073-88.32L18 650.654l210.184 182.174C220.39 875.52 216.55 918.212 216.55 960s3.84 84.48 11.633 127.172L18 1269.346l199.454 340.856 265.186-88.433c66.974 55.567 143.322 99.389 223.85 128.415L761.152 1920h397.779l54.663-269.704c81.318-29.138 156.424-72.282 223.963-128.414l265.073 88.433 199.454-340.856-210.184-182.174c7.793-42.805 11.633-85.497 11.633-127.285m-743.492 395.294c-217.976 0-395.294-177.318-395.294-395.294 0-217.976 177.318-395.294 395.294-395.294 217.977 0 395.294 177.318 395.294 395.294 0 217.976-177.317 395.294-395.294 395.294" fillRule="evenodd"></path>
                    </g></svg>
            </SettingsButton>
        </div>
        {
            isOpen && (<>
                <div
                    className="fixed inset-0 bg-[rgba(0,0,0,0.3)]  backdrop-blur-sm z-40 transition-colors duration-200"
                />
                <div className='flex justify-center items-center'>
                    <SettingsWindow onSettingsClose={() => setIsOpen(false)} />
                </div>
            </>)
        }
    </div >)

}