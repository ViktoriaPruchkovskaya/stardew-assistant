import { Chat, ChatMessage } from "./ChatService"


export default class StorageService {
    public createChat({ id }: {
        id: string,
        // createdAt: string
    }) {
        const record: string | null = localStorage.getItem("chats")
        let chats: string[] = []
        if (record) {
            chats = JSON.parse(record)
        }
        chats.push(id)
        localStorage.setItem("chats", JSON.stringify(chats))
    }

    public getChat({ id }: {
        id: string
    }): Chat {
        const record = localStorage.getItem(id)
        if (!record) {
            throw new Error('Could not retrieve chat')
        }
        const chat = JSON.parse(record)
        return {
            id: chat.id,
            createdAt: chat.createdAt,
            messages: chat.messages
        }
    }
}