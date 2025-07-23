import { Chat } from "./ChatService"

type Theme = 'dark' | 'light'

export default class StorageService {
    public createChat({ id }: {
        id: string,
        // createdAt: string
    }): void {
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

    public setTheme(theme: Theme): void {
        localStorage.setItem("theme", theme)
    }

    public getTheme(): Theme | null {
        return localStorage.getItem("theme") as Theme
    }
}