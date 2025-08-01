import { useContext } from "react"
import { ChatsContext } from "../../contexts/chatsContext"
import { useNavigate } from "react-router"

interface SavedChatsProps {
    onSettingsClose: () => void
}


export default function SavedChats({ onSettingsClose }: SavedChatsProps) {
    const { chatIds, deleteChats } = useContext(ChatsContext)!
    const navigate = useNavigate()
    const handleOnClick = (chatId: string) => {
        onSettingsClose()
        navigate(`chat/${chatId}`, { state: { newChat: false } })
    }
    return (<>
        <h3 className="text-yellow-800 text-base mb-2 text-center">Saved Chats</h3>
        <div className="bg-yellow-200 border-2 border-yellow-600 rounded-lg h-[120px] overflow-y-auto pr-2 [&::-webkit-scrollbar]:w-2  [&::-webkit-scrollbar-thumb]:bg-amber-400">
            <ul className="text-sm px-2 py-1 space-y-1">
                {chatIds.map((chatId, order) => <li key={chatId} onClick={() => handleOnClick(chatId)} className="hover:bg-yellow-300 cursor-pointer rounded px-1">Chat {order + 1}</li>)}
            </ul>
        </div>
        <div className="flex justify-center">
            <button onClick={() => deleteChats(chatIds)} disabled={!chatIds.length} className="min-w-30 mt-2 py-1 bg-amber-400 border-2
                 border-yellow-600 hover:bg-yellow-400 rounded-md shadow-sm  cursor-pointer text-center p-3">
                Delete chats
            </button>
        </div></>)
}