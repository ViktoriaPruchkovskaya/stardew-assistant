<p align="center">
    <img src="web/src/assets/stardew-valley-assistant.png" alt="Stardew Valley Assistant" width="500">
</p>

An AI-powered web assistant for Stardew Valley players, featuring a chat-style interface that provides contextual game information and guidance. Instead of spending hours browsing the official wiki, users can ask questions in natural language and get quick, relevant responses.
## Feautres 
- Chat interface: Natural conversation style interaction for asking game-related questions
- Contextual information: Retrieves and analyzes information from the [official Stardew Valley wiki](https://stardewvalleywiki.com/Stardew_Valley_Wiki)
- Multi-turn Conversations: Maintains conversation context across multiple interactions using Redis caching
- Chats Management: Navigate through chat history and manage past conversations
- Real-time Responses: Fast, responsive AI-powered assistance for gameplay questions
- Apearance Management: UI automatically adapts to system preferences with the ability to manually toggle between light and dark themes
## How It Works
1. **User Flow**: Users navigate to the main page and either create a new chat or select from previous conversations
2. **Question Processing**: When a question is submitted, the server formulates chat context using cached conversation data from Redis
3. **Wiki Integration**: The question and context are sent to MCP (Model Context Protocol), which:
    - Analyzes the topic and determines relevant Wiki pages/sections using a pre-built CSV index of all Wiki content
    - Fetches targeted information from the official Stardew Valley Wiki
    - Filters only necessary data based on the question and conversation context
    - Maintains conversation context for follow-up questions (e.g., "Where does Penny live?" -> "What does she like?")
4. **Response Delivery**: The processed information is returned to the user through the chat interface
5. **Chat Persistence**: Conversations are stored in MongoDB, with active chats cached in Redis for performance
6. **Context Management**: To keep multi-round conversations compact and manageable, the system stores several conversation rounds and automatically summarizes them when the context size reaches the limit, maintaining conversation history while optimizing performance
## Tech Stack
### Backend
- Python
- FastAPI
- MongoDB
- Redis
- MCP (Model Context Protocol)
- Azure AI
### Frontend
- TypeScript
- React
- Tailwind CSS
## Getting Started
### Quick Start (Docker)
1. Clone repository:
```
git clone https://github.com/ViktoriaPruchkovskaya/stardew-assistant.git
cd stardew-assistant
```
2. Run project container
```
docker-compose up
```
The container consists of Redis CLI and web-based MongoDB client for persistences management.
### Manual Setup
#### Prerequisites
- Python 3.12+ (uv)
- Node.js 16+ (pnpm)
- MongoDB
- Redis
1. Clone repository:
```
git clone https://github.com/ViktoriaPruchkovskaya/stardew-assistant.git
cd stardew-assistant
```
2. Backend setup:
```
cd app
uv sync
```
3. Frontend setup:
```
cd web
pnpm install
```
4. Environment setup:
```
cd app
# Copy example environment files
cp template.example .env
# Configure your environment variables
```
#### Running application
1. Start Redis and MongoDB services
2. Start backend:
```
cd app
uv run main.py
```
Backend will be available at http://localhost:8000

3. Start frontend:
```
cd web
pnpm start
```
Frontend will be available at http://localhost:8080
## Other
MCP looks up for available topics crawled from the [official Stardew Valley wiki](https://stardewvalleywiki.com/Stardew_Valley_Wiki) and assembled in pages.csv file.
To rewrite this file:
```
cd app
ur run wiki_crawler.py
```
## Disclaimer
This is an unofficial pet project. Stardew Valley is created by ConcernedApe.
