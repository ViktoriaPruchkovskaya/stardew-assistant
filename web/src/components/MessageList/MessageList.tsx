import { useEffect, useRef } from "react";
import { ChatMessage } from "../../services/ChatService";
import MessageBubble from "./MessageBubble";

interface MessageListProps {
    messages: ChatMessage[]
}

export default function MessageList({ messages }: MessageListProps) {
    const bottomRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    return (
        <div className="flex-1 overflow-y-auto p-4 bg-amber-50 border-4 scroll-smooth my-2
         border-yellow-600 rounded-md shadow-inner space-y-4 text-yellow-900 max-h-[50vh] min-h-[56px] sm:max-h-[60vh] lg:max-h-[70vh]
          [&::-webkit-scrollbar]:w-2 [&::-webkit-scrollbar-track]:bg-amber-100 [&::-webkit-scrollbar-thumb]:bg-amber-400 ">{
                messages.map((msg, index) => (
                    <MessageBubble key={index} message={msg} />
                ))
            }
            <div ref={bottomRef} />
        </div>
    );
}