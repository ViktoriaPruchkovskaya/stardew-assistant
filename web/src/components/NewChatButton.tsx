import { useNavigate } from "react-router"
import ChatService from "../services/ChatService"

export default function NewChatButton() {
    const navigate = useNavigate()
    const handleOnClick = () => {
        const id = new ChatService().createChat()
        navigate(`chat/${id}`)
    }
    return <button
        className="px-4 py-2 rounded-md font-press-start bg-amber-400 border-2
                 border-yellow-600 text-yellow-900 font-bold shadow-md hover:bg-amber-500 
                 active:translate-y-[1px] transition-all duration-200 cursor-pointer"
        onClick={handleOnClick}
    >
        New Chat
    </button>
}