import { useState, useRef } from "react";
import ChatForm from "./ChatForm";
import MessageList from "./MessageList/MessageList";
import { ChatMessage } from "../services/ChatService";

export default function Dialog() {
    const [messages, setMessages] = useState<ChatMessage[]>([])
    const onMessageSent = (msg: ChatMessage) => {
        setMessages(prevMessages => [...prevMessages, msg]);
    };
    return (<div className="flex flex-col min-h-[calc(80vh)]">
        <MessageList messages={messages} />
        <ChatForm onMessageSent={onMessageSent} />
    </div>)
}