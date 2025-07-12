import { useEffect, useState } from "react";
import { useParams, useLocation, Location, useNavigate } from "react-router";
import ChatForm from "./ChatForm";
import MessageList from "../MessageList/MessageList";
import ChatService, { ChatMessage } from "../../services/ChatService";

interface LocationState {
    newChat: boolean;
}

export default function Chat() {
    const { state } = useLocation() as Location<LocationState>;
    let { id } = useParams();
    const [messages, setMessages] = useState<ChatMessage[]>([])
    useEffect(() => {
        if (state?.newChat) {
            return
        }
        const fetchData = async () => {
            const chatService = new ChatService()
            const data = await chatService.getChat({ id: id! }) // check if chat exists
            setMessages(data.messages)
        }
        fetchData()

    }, [])
    const navigate = useNavigate()
    const onMessageSent = (msg: ChatMessage) => {
        if (state?.newChat) {
            navigate(location.pathname, { replace: true });
        }
        setMessages(prevMessages => [...prevMessages, msg]);
    };
    return (<div className="flex flex-col min-h-[calc(80vh)]">
        <MessageList messages={messages} />
        <ChatForm onMessageSent={onMessageSent} chatId={id!} />
    </div>)
}