from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import asyncio
import httpx
from dotenv import load_dotenv
import requests
import time

#### start of first song
if (TimeoutError):
    
    load_dotenv()

    app = FastAPI()
    print("\n\n\n\n\n")

    SUNO_API_TOKEN = os.getenv("SUNO_API_TOKEN")
    current_prompt_bpm = 70
    ### given vars from kj code
    givenSongBPM = 70
    playTime =30 #seconds





    last_clip_id = None

    # class MusicRequest(BaseModel):
    #     user_bpm: int
    #     goal_bpm: int

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
    async def generate_music(currentPromt):
        # req = MusicRequest(user_bpm=70, goal_bpm=100)
        # print(f"Received request: user_bpm={req.user_bpm}, goal_bpm={req.goal_bpm}")
        global last_clip_id
        # bpm = adjust_bpm(req.user_bpm, req.goal_bpm)
        
        topic = currentPromt
        tags = "instrumental, steady, rhythmic, walking, upbeat"
        make_instrumental = True

       
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
            
            audio_url = clip_data["audio_url"]
            print(audio_url)

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
                    audio_url = clip["audio_url"]
                    print(f"\n\\AUDIO URL: {audio_url}\n")
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
#asyncio.run(generate_music())


### end of first song

### start of song extension


#following or set mode
yn = "abcd"
while (yn != "y" and yn != "n"):
    print ("Is following mode on? (y/n)")
    yn = input()
    if (yn != "y" and yn != "n"):
        print("Sorry please answer 'y' or 'n'\n\n")
    if (yn == "y") :
        followingMode = True
    if (yn == "n"):
        followingMode = False


#psitive reinforcement for this cycle
yn = "abcd"
while (yn != "y" and yn != "n"):
    print ("Has the patient met a goal in this period? (y/n)")
    yn = input()
    if (yn != "y" and yn != "n"):
        print("Sorry please answer 'y' or 'n'\n\n")
    if (yn == "y") :
        EventFlagged = True
    if (yn == "n"):
        EventFlagged = False


#request bpm percent change
if (not(followingMode)) :
    print ("What percent would you like to change BPM by:")
    PTIdeal = input()
    PTIdeal = int(PTIdeal)
    PTIdeal = givenSongBPM*(1+PTIdeal/100)


# recording steps and time elapsed
if (True):
    print ("recording")
    input ()
    tStart = time.time()
    steps = 1
    while (steps<=4):
        input ()
        steps+=1

    tFin = time.time()


#33% time increase reduction
timeCalibrate = 2/3

#finding average speed in bpm
averageTime = 60*(steps+1)/((tFin-tStart)/timeCalibrate)
averageTime = round(averageTime)

print ("recording stopped")




# creates prompt for music extension
if (True):
    prompt1 = "Create song with pauses imbetween beats"
    #by "+str(playTime)+" seconds"
    promptBPMFol = ", gradually change the BPM from 70 to "+str(averageTime)+" over a period of "+str(playTime)+" seconds"
    promptEvent =", and add an upbeat flourish near the start of this section"
    if (not(followingMode)) :
        promptBPMPT = ", gradually change the BPM to "+str(PTIdeal)+" over a period of "+str(playTime)+" seconds"

    currentPromt = prompt1
    if (followingMode) :
        currentPromt = currentPromt+promptBPMFol
    else :
        currentPromt = currentPromt+promptBPMPT
    if (EventFlagged) :
        currentPromt = currentPromt+promptEvent

print (currentPromt)

#song extension
if (TimeoutError):
    load_dotenv()

    app = FastAPI()
    print("\n\n\n\n\n")

    SUNO_API_TOKEN = os.getenv("SUNO_API_TOKEN")
  
    playTime =30 #seconds





    last_clip_id = None



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

        # print(f"Received request: user_bpm={req.user_bpm}, goal_bpm={req.goal_bpm}")
        global last_clip_id


        topic = currentPromt
        tags = "instrumental, steady, rhythmic, walking, upbeat"
        make_instrumental = True


        
        # Step 1: Request Generation
        async with httpx.AsyncClient() as client:
            payload = {"topic": topic, "tags": tags}
            if last_clip_id:
                payload["cover_clip_id"] = last_clip_id
                print("\n\nis last cilp iid?\n\n")

            #print(f"auth token is {SUNO_API_TOKEN}")
            gen_response = await client.post(
                "https://studio-api.prod.suno.com/api/v2/external/hackmit/generate",
                headers={
                    "Authorization": f"Bearer {SUNO_API_TOKEN}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            
            #print(f"Generation response status: {gen_response.status_code}")
            if gen_response.status_code != 200:
                return {"error": "Failed to generate music from Suno"}, gen_response.status_code
            
            #print(gen_response.text)

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
                    print(clip["audio_url"])
                    return {
                        "success": True,
                        "clip": {
                            "id": clip["id"],
                            "status": clip["status"],
                            "audio_url": clip["audio_url"],
                            #"music_bpm": bpm,
                            # "description": f"Generated music clip at {bpm} BPM"
                            
                        }
                    
                    }
                

            # Timeout
            return {"error": "Timed out waiting for clip"}, 504
print("Working on song generation...")
asyncio.run(generate_music())
