import { BrowserRouter, Route, Routes } from "react-router";
import { useEffect } from "react"

import Chat from "./components/Chat/Chat";
import Header from "./components/Header";
import NewChatButton from "./components/NewChatButton";
import SettingsWrapper from "./components/Settings/SettingsWrapper";
import { useTheme } from "./hooks/useTheme";
import ThemeProvider from "./contexts/themeContext";

export default function MyApp() {
    const { isDark, setIsDark, toggleTheme } = useTheme()

    useEffect(toggleTheme, [isDark]);
    return (
        <div className="min-h-screen bg-cover bg-center bg-no-repeat bg-[url(./assets/background-light.png)] dark:bg-[url(./assets/background-dark.png)]">
            <div className="m-auto max-w-5xl px-8 py-6 flex flex-col gap-2 " >
                <BrowserRouter>
                    <ThemeProvider isDark={isDark} setIsDark={setIsDark}>
                        <Header />
                        <SettingsWrapper />
                        <Routes>
                            <Route path="/" Component={NewChatButton} />
                            <Route path='/chat/:id' Component={Chat} />
                        </Routes>
                    </ThemeProvider>

                </BrowserRouter>
            </div >
        </div>

    );
}
