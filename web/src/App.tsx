import Dialog from "./components/Dialog";

export default function MyApp() {
    return (
        <div className="min-h-screen bg-cover bg-center bg-no-repeat bg-[url(./assets/background-light.png)]">
            <div className="m-auto max-w-5xl px-8 py-6 flex flex-col gap-2 " >
                < h1 className="text-center font-press-start text-3xl font-bold text-amber-50" >Stardew Valley Assistant</h1 >
                <Dialog />
            </div >
        </div>

    );
}
