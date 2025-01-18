
from fastapi import FastAPI
from app.api import sites, stories, audio, search, user, artifact, auth
from fastapi.security import  OAuth2PasswordBearer, HTTPBearer

app = FastAPI()
security = HTTPBearer()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(sites.router)
app.include_router(stories.router)
app.include_router(audio.router)
app.include_router(search.router)
app.include_router(artifact.router)

@app.get("/")
async def hello():
       return "Hello, This is the API!"


if __name__ == "__main__":
       import uvicorn
       uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
      
