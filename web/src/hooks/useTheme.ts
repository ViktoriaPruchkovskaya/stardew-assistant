import { useEffect, useState } from "react";
import StorageService from "../services/storageService";

interface Theme {
    isDark: boolean;
    setIsDark: React.Dispatch<React.SetStateAction<boolean>>;
}

export function useTheme(): Theme {
    const storageService = new StorageService()

    const [isDark, setIsDark] = useState(() => {
        return storageService.getTheme() === 'dark' ||
            (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
    });

    const toggleTheme = () => {
        const theme = isDark ? 'dark' : 'light';
        storageService.setTheme(theme)
        document.documentElement.classList.toggle('dark', isDark);
    }

    useEffect(toggleTheme, [isDark]);

    return { isDark, setIsDark }
}