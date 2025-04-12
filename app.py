from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static data loaded from Excel originally
words_data = [
    {'Word': 'yes', 'Translation': 'כן', 'Sentence': 'yes, it is me', 'std_state': 1},
    {'Word': 'panda', 'Translation': 'פנדה', 'Sentence': 'this is a oanda', 'std_state': 0},
    {'Word': 'Segev', 'Translation': 'שגב', 'Sentence': 'Segev is a name', 'std_state': 1},
    # המשך הרשימה...
]

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

@app.get("/words")
def get_words():
    return words_data

@app.post("/update_word")
def update_word(word: str, state: int):
    for w in words_data:
        if w["Word"] == word:
            w["std_state"] = state
            return {"message": "Updated successfully"}
    raise HTTPException(status_code=404, detail="Word not found")
