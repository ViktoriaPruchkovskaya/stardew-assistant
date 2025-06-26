import Chat from "./components/Chat/Chat";
import Header from "./components/Header";

import NewChatButton from "./components/NewChatButton";
import { BrowserRouter, Route, Routes } from "react-router";

export default function MyApp() {
    return (
        <div className="min-h-screen bg-cover bg-center bg-no-repeat bg-[url(./assets/background-light.png)]">
            <div className="m-auto max-w-5xl px-8 py-6 flex flex-col gap-2 " >
                <BrowserRouter>
                    <Header />
                    <Routes>
                        <Route path="/" Component={NewChatButton} />
                        <Route path='/chat/:id' Component={Chat} />
                    </Routes>
                </BrowserRouter>
            </div >
        </div>

    );
}
