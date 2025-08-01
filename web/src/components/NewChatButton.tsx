import { useNavigate } from "react-router"
import { useContext } from "react"
import { ChatsContext } from "../contexts/chatsContext"

export default function NewChatButton() {
    const navigate = useNavigate()
    const { createChat } = useContext(ChatsContext)!
    const handleOnClick = async () => {
        const { id } = await createChat()
        navigate(`chat/${id}`, { state: { newChat: true } })
    }
    return <button
        className="px-4 py-2 rounded-md font-press-start bg-amber-400 border-2
                 border-yellow-600 text-yellow-900 font-bold shadow-md hover:bg-amber-500 
                 active:translate-y-[1px] transition-all duration-200 cursor-pointer"
        onClick={async () => handleOnClick()}
    >
        New Chat
    </button>
}