import random
import re
import time

import uvicorn
from faker import Faker
from fastapi import FastAPI

fake = Faker()
app = FastAPI()


@app.get("/paragraph/next")
def next_paragraph():
    pg = fake.paragraph(nb_sentences=5)
    sleep_time = random.randint(1, 5)
    time.sleep(sleep_time)
    return {"word_count": len(re.findall(r"\w+", pg)), "paragraph": pg}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
