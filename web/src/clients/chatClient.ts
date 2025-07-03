export default class ChatClient {
    public async sendMessage(message: string): Promise<string> {
        const res = await fetch("http://localhost:8000/api/chat/", {
            method: "POST", headers: {
                'Content-Type': 'application/json'
            }, body: JSON.stringify({ message })
        })
        const parsed = await res.json()
        return parsed.message
    }

    public async createChat(): Promise<string> {
        const res = await fetch("http://localhost:8000/api/chat/", {
            method: "POST", headers: {
                'Content-Type': 'application/json'
            }
        })
        const parsed = await res.json()
        return parsed.id
    }
}