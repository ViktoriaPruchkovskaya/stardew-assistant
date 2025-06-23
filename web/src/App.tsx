import Dialog from "./components/Dialog";

export default function MyApp() {
    return (
        <div className="min-h-screen bg-cover bg-center bg-no-repeat bg-[url(./assets/background-light.png)]">
            <div className="m-auto max-w-7xl px-8 py-6 flex flex-col gap-6" >
                < h1 className="text-4xl font-bold text-amber-50" > Welcome to my app</h1 >
                <Dialog />
            </div >
        </div>

    );
}