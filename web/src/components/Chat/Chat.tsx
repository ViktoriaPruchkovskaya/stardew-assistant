import { useEffect, useState } from "react";
import { useParams, useLocation, Location } from "react-router";
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
        const data = new ChatService().getChat({ id: id! }) // check if chat exists
        setMessages(data.messages)
    }, [])
    const onMessageSent = (msg: ChatMessage) => {
        setMessages(prevMessages => [...prevMessages, msg]);
    };
    return (<div className="flex flex-col min-h-[calc(80vh)]">
        <MessageList messages={messages} />
        <ChatForm onMessageSent={onMessageSent} chatId={id!} />
    </div>)
}