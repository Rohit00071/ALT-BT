# AI-Powered Manim Animator 🎬✨

Generate beautiful educational math animation videos using AI and [Manim](https://www.manim.community/). Type a math concept, choose a language, and watch AI create an animation in seconds.

**100% free and open-source. No paid APIs required.**

---

## 🏗 Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────┐
│   Next.js UI    │────▶│  FastAPI Backend  │────▶│  Manim CLI  │
│  (React + TW)   │◀────│  (Python)        │◀────│  (Renderer) │
└─────────────────┘     └───────┬──────────┘     └─────────────┘
                                │
                        ┌───────▼──────────┐
                        │  Gemini / Groq   │
                        │  (Free Tier LLM) │
                        └──────────────────┘
```

- **Frontend**: Next.js + Tailwind CSS + React Hook Form + Axios
- **Backend**: FastAPI + Pydantic
- **AI Engine**: Google Gemini (free) or Groq (free)
- **Renderer**: Manim Community Edition (local, open-source)

## 📋 Prerequisites

- **Python 3.10+** with pip
- **Node.js 18+** with npm
- **FFmpeg** (required by Manim — [install guide](https://ffmpeg.org/download.html))
- **Manim system deps**: Cairo, Pango (usually installed with Manim pip package)
- A free API key from [Google AI Studio](https://aistudio.google.com/apikey) OR [Groq Cloud](https://console.groq.com/)

## 🚀 Quick Start

### 1. Clone and configure

```bash
cd hhackathon
cp .env.example .env
# Edit .env and add your free-tier API key
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

### 4. Start the backend

```bash
uvicorn app.main:app --reload --port 8000
```

### 5. Start the frontend (separate terminal)

```bash
cd frontend
npm run dev
```

### 6. Open in browser

Navigate to **http://localhost:3000**

## 🔧 Environment Variables

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `gemini` | `"gemini"` or `"groq"` |
| `GEMINI_API_KEY` | — | Google Gemini free-tier API key |
| `GEMINI_MODEL_NAME` | `gemini-2.0-flash` | Gemini model to use |
| `GROQ_API_KEY` | — | Groq free-tier API key |
| `GROQ_MODEL_NAME` | `llama-3.3-70b-versatile` | Groq model to use |
| `VIDEO_OUTPUT_DIR` | `./videos` | Where rendered MP4s are saved |
| `TEMP_SCENE_DIR` | `./tmp_scenes` | Where temp .py files are written |
| `NON_LATIN_FONT_NAME` | `Noto Sans` | Font for non-Latin scripts |

## 🧪 API Reference

### POST `/api/generate_video`

```bash
curl -X POST http://localhost:8000/api/generate_video \
  -H "Content-Type: application/json" \
  -d '{"concept": "Pythagorean Theorem", "language": "English"}'
```

**Success response:**
```json
{
  "status": "success",
  "video_url": "/videos/abc123_output.mp4",
  "message": "Video generated successfully!"
}
```

**Error response:**
```json
{
  "status": "error",
  "message": "AI generated invalid Manim code. Please try a different prompt.",
  "details": "..."
}
```

### GET `/health`

```json
{"status": "ok"}
```

## 🔮 Future Work

These are planned enhancements (not implemented yet):

- **Job Queue**: Add a local Redis-based job queue for async rendering
- **n8n + Twilio Integration**: Use n8n Cloud (free tier) + Twilio Sandbox for WhatsApp delivery of generated videos
- **Video Gallery**: Persist metadata and MP4 URLs in Supabase (free plan) for a browsable gallery
- **Caching**: Cache LLM responses for identical concept+language pairs
- **Sandboxing**: Run Manim in a Docker container for enhanced security
- **Multiple Scenes**: Support multi-scene animations with chapter markers

## ⚠️ Known Limitations

- AI-generated Manim code may occasionally fail to render — retry with a different wording
- Non-Latin fonts require the font to be installed on the system
- Render times are 20–60 seconds (using low-quality preset for speed)
- No persistent storage — generated videos are ephemeral
- Free-tier API rate limits apply (Gemini: ~15 RPM, Groq: ~30 RPM)

## 📄 License

MIT — free for any use.
