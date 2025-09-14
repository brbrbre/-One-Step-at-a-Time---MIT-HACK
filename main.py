from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import asyncio
import httpx
from dotenv import load_dotenv
import requests

load_dotenv()

app = FastAPI()

SUNO_API_TOKEN = os.getenv("SUNO_API_TOKEN")
current_prompt_bpm = 90

last_clip_id = None

class MusicRequest(BaseModel):
    user_bpm: int
    goal_bpm: int

def adjust_bpm(user_bpm, goal_bpm):
    global current_prompt_bpm
    bpm_diff = goal_bpm - user_bpm

    if abs(bpm_diff) < 5:
        adjustment = 3
    elif bpm_diff > 10:
        adjustment = -3
    elif bpm_diff < -10:
        adjustment = -2
    else:
        adjustment = 5

    current_prompt_bpm += adjustment
    current_prompt_bpm = max(60, min(current_prompt_bpm, goal_bpm))
    return current_prompt_bpm

@app.get("/")
def read_root():
    return {"message": "It works!"}

@app.get("/generate-music")
async def generate_music():
    req = MusicRequest(user_bpm=70, goal_bpm=100)
    print(f"Received request: user_bpm={req.user_bpm}, goal_bpm={req.goal_bpm}")
    global last_clip_id
    bpm = adjust_bpm(req.user_bpm, req.goal_bpm)

    topic = "A motivational electronic beat at around {bpm} BPM for walking"
    tags = "instrumental, steady, rhythmic, walking, upbeat"
    make_instrumental = True


    # if not SUNO_API_TOKEN:
    #     # Fallback to mock
    #     mock_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    #     last_clip_id = "mock-clip-id"
    #     return {
    #         "success": True,
    #         "clip": {
    #             "id": "mock-clip-id",
    #             "status": "streaming",
    #             "audio_url": mock_url,
    #             "music_bpm": bpm,
    #             "description": f"Mock 10s song at {bpm} BPM"
    #         }
    #     }

    # Step 1: Request Generation
    async with httpx.AsyncClient() as client:
        payload = {"topic": topic, "tags": tags}
        if last_clip_id:
            payload["cover_clip_id"] = last_clip_id

        print(f"auth token is {SUNO_API_TOKEN}")
        gen_response = await client.post(
            "https://studio-api.prod.suno.com/api/v2/external/hackmit/generate",
            headers={
                "Authorization": f"Bearer {SUNO_API_TOKEN}",
                "Content-Type": "application/json"
            },
            json=payload
        )
        
        print(f"Generation response status: {gen_response.status_code}")
        if gen_response.status_code != 200:
            return {"error": "Failed to generate music from Suno"}, gen_response.status_code
        
        print(gen_response.text)

        clip_data = gen_response.json()
        clip_id = clip_data["id"]
        last_clip_id = clip_id

        # Step 2: Poll /clips
        poll_attempts = 10
        for _ in range(poll_attempts):
            await asyncio.sleep(5)
            status_res = await client.get(
                f"https://studio-api.prod.suno.com/api/v2/external/hackmit/clips?ids={clip_id}",
                headers={"Authorization": f"Bearer {SUNO_API_TOKEN}"}
            )

            if status_res.status_code != 200:
                continue

            clips = status_res.json()
            if not clips or len(clips) == 0:
                continue

            clip = clips[0]
            if clip["status"] in ["streaming", "complete"]:
                return {
                    "success": True,
                    "clip": {
                        "id": clip["id"],
                        "status": clip["status"],
                        "audio_url": clip["audio_url"],
                        "music_bpm": bpm,
                        "description": f"Generated music clip at {bpm} BPM"
                    }
                }

        # Timeout
        return {"error": "Timed out waiting for clip"}, 504
