import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from chatbot.crew import EcommerceChatbotCrew
import uvicorn
import logging
from logging.handlers import RotatingFileHandler
import time
from chatbot.config import config

# Configure logging
log_directory = os.path.dirname(config.LOG_FILE)
os.makedirs(log_directory, exist_ok=True)

logging.basicConfig(level=config.LOG_LEVEL)
file_handler = RotatingFileHandler(config.LOG_FILE, maxBytes=10485760, backupCount=5)
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

logger = logging.getLogger(__name__)
logger.addHandler(file_handler)

app = FastAPI(debug=config.DEBUG)

class Query(BaseModel):
    text: str
    user_id: str

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Request: {request.method} {request.url} - Status: {response.status_code} - Time: {process_time:.2f}s")
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred. Please try again later."}
    )

@app.post('/chat')
async def chat(query: Query):
    try:
        crew = EcommerceChatbotCrew()
        logger.info(f"Processing query for user {query.user_id}: {query.text}")
        
        # Determine the task based on the query content
        if "recommend" in query.text.lower() or "suggest" in query.text.lower():
            task = crew.personalized_recommendations()
        elif "order" in query.text.lower() and "status" in query.text.lower():
            task = crew.track_order()
        else:
            task = crew.answer_faq()
        
        result = crew.crew().kickoff(inputs={
            "customer_query": query.text,
            "user_id": query.user_id,
            "task": task
        })
        
        logger.info(f"Query processed successfully for user {query.user_id}")
        return {"response": result}
    except Exception as e:
        logger.exception(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request")

@app.get('/health')
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host=config.HOST, port=config.PORT, log_level=config.LOG_LEVEL.lower())