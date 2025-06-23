interface ChatResult {
    message: string
}

export default class ChatService {
    public async sendQuestion(question: string): Promise<ChatResult> {
        const res = await fetch("http://localhost:8000/api/chat/", {
            method: "POST", headers: {
                'Content-Type': 'application/json'
            }, body: JSON.stringify({ "message": question })
        })
        return res.json()
    }
}