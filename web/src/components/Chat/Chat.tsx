import { useEffect, useState } from "react";
import { useParams } from "react-router";
import ChatForm from "./ChatForm";
import MessageList from "../MessageList/MessageList";
import ChatService, { ChatMessage } from "../../services/ChatService";

export default function Chat() {
    let { id } = useParams();
    const [messages, setMessages] = useState<ChatMessage[]>([])
    useEffect(() => {
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