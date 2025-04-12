from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import BackgroundTasks  # Add BackgroundTasks for async saving

import pandas as pd
import os

app = FastAPI()

# CORS settings to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://timely-cajeta-699adc.netlify.app/", "*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#FILE_PATH = os.path.abspath("word.xlsx")  # Converts relative path to absolute

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR,"word.xlsx")



# Load Excel data
def load_data():
    print(os.path.exists(FILE_PATH))
    if os.path.exists(FILE_PATH):
        return pd.read_excel(FILE_PATH)
    else:
        raise HTTPException(status_code=404, detail="File not found")

# Save to Excel
def save_data(df):
    df.to_excel(FILE_PATH, index=False)

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

@app.get("/words")
def get_words():
    df = load_data()
    return df.to_dict(orient="records")


@app.post("/update_word")
def update_word(word: str, state: int, background_tasks: BackgroundTasks):
    df = load_data()
    if word in df["Word"].values:
        df.loc[df["Word"] == word, "std_state"] = state
        background_tasks.add_task(save_data, df)  # Save asynchronously
        return {"message": "Updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Word not found")
