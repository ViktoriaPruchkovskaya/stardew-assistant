import { ChatMessage } from "../../services/ChatService";

interface MessageBubbleProps {
    message: ChatMessage
}

export default function MessageBubble({ message }: MessageBubbleProps) {
    const isUser = message.sender === 'user';
    return (
        <div className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'}`} >
            <div
                className={`w-fit max-w-[70%] p-3 px-4 border-2 rounded-lg shadow-sm text-sm break-words whitespace-pre ${isUser
                    ? 'bg-yellow-100 border-yellow-500 self-end text-yellow-900 '
                    : 'bg-white border-yellow-700 self-start text-gray-800'
                    }`}
            >
                <p>{message.text}</p>
            </div>
        </ div >

    )
};