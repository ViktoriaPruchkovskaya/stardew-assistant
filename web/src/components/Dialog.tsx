import * as React from 'react';
import ChatService from '../services/ChatService';

export default function Dialog() {
    const handleForm = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const { question } = event.target as HTMLFormElement;

        (async () => {
            const res = await new ChatService().sendQuestion(question.value);
            console.log(res.message)
        })();
    };
    return (<div className="mb-6">
        <form onSubmit={handleForm} className='flex w-full items-center gap-2'>
            <input type="text" id="question" className="w-full min-w-[200px] bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5" placeholder="Ask anything" required />
            <button type="submit" className='p-1 border border-gray-300 rounded-lg hover:bg-gray-200 cursor-pointer'>
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="32"
                    height="32"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                >
                    <path d="M5 12l14 0" />
                    <path d="M13 18l6 -6" />
                    <path d="M13 6l6 6" />
                </svg>
            </button>
        </form>
    </div >
    )
}