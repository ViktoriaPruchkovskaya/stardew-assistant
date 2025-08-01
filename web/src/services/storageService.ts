type Theme = 'dark' | 'light'



export default class StorageService {
    public addChatId(chatId: string): void {
        const record: string | null = localStorage.getItem("chats")
        let chats: string[] = []
        if (record) {
            chats = JSON.parse(record)
        }
        chats.push(chatId)
        localStorage.setItem("chats", JSON.stringify(chats))
    }

    public getChatIds(): string[] {
        const record: string | null = localStorage.getItem("chats")
        if (!record) {
            return []
        }
        const records = JSON.parse(record)
        return records
    }

    public deleteChats(): void {
        localStorage.removeItem('chats')
    }

    public setTheme(theme: Theme): void {
        localStorage.setItem("theme", theme)
    }

    public getTheme(): Theme | null {
        return localStorage.getItem("theme") as Theme
    }
}