import * as React from 'react';
import { useState } from 'react';
import ChatService, { ChatMessage } from '../../services/ChatService';

interface ChatFormProps {
    chatId: string,
    onMessageSent: (message: ChatMessage) => void
}

export default function ChatForm({ chatId, onMessageSent }: ChatFormProps) {
    const [inputValue, setInputValue] = useState("");
    const handleForm = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        let { question } = event.target as HTMLFormElement;
        question = question.value.trim();
        if (!question) return;

        const newMessage: ChatMessage = { sender: 'user', text: question }
        onMessageSent(newMessage);
        setInputValue('');

        (async () => {
            const res = await new ChatService().sendMessage({ id: chatId, message: question });
            onMessageSent(res)
        })();
    };

    return (<div className="mb-6">
        <form onSubmit={handleForm} className='flex w-full items-center gap-2'>
            <input type="text" id="question" value={inputValue} onChange={(e) => setInputValue(e.target.value)} className="flex-grow min-w-[200px] rounded-md border-2 border-yellow-600 bg-amber-50 text-sm text-gray-800 p-2.5 shadow-inner focus:outline-none focus:ring-2 focus:ring-amber-400 focus:border-amber-500 placeholder:text-yellow-800 placeholder:opacity-70" placeholder="Ask anything..." required />

            <button
                className="px-4 py-2 rounded-md font-press-start bg-amber-400 border-2
                 border-yellow-600 text-yellow-900 font-bold shadow-md hover:bg-amber-500 
                 active:translate-y-[1px] transition-all duration-200 cursor-pointer"
            >
                Send
            </button>
        </form>
    </div >
    )
}