import Dialog from "./components/Dialog";
import image from 'url:./assets/stardew-valley-assistant.png';

export default function MyApp() {
    return (
        <div className="min-h-screen bg-cover bg-center bg-no-repeat bg-[url(./assets/background-light.png)]">
            <div className="m-auto max-w-5xl px-8 py-6 flex flex-col gap-2 " >
                <img
                    src={image}
                    className="w-lg mx-auto drop-shadow-lg"
                />
                <Dialog />
            </div >
        </div>

    );
}
