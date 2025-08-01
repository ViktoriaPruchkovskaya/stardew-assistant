import { createContext, ReactNode } from "react";

export interface ThemeContextProps {
    isDark: boolean;
    setIsDark: React.Dispatch<React.SetStateAction<boolean>>;
}
interface ThemeContextPropsWithChildren extends ThemeContextProps {
    children: ReactNode
}

export const ThemeContext = createContext<ThemeContextProps | null>(null);

export default function ThemeProvider({ children, isDark, setIsDark }: ThemeContextPropsWithChildren) {
    return (<ThemeContext.Provider value={{ isDark, setIsDark }}>
        {children}
    </ThemeContext.Provider >)
}