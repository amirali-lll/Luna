simlpe_voic_assistance/
├── config.py
├── main.py
├── requirements.txt
├── agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── api/
│   └── tools/
├── interfaces/           # NEW: Input/Output interfaces
│   ├── __init__.py
│   ├── base.py          # Abstract base classes
│   ├── voice/           # Voice-specific interfaces
│   │   ├── __init__.py
│   │   ├── input.py     # Voice input (STT)
│   │   ├── output.py    # Voice output (TTS)
│   │   └── config.py    # Voice-specific config
│   ├── web/             # Web-specific interfaces
│   │   ├── __init__.py
│   │   ├── server.py    # FastAPI/Flask server
│   │   ├── routes.py    # API endpoints
│   │   └── websocket.py # Real-time communication
│   └── cli/             # CLI interface (current implementation)
│       ├── __init__.py
│       └── terminal.py
├── services/            # NEW: Business logic layer
│   ├── __init__.py
│   ├── conversation.py  # Conversation management
│   ├── audio.py         # Audio processing utilities
│   └── session.py       # Session management
└── docs/