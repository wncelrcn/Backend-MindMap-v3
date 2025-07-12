from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import logging
from typing import List, Dict
import os
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app with /api prefix
app = FastAPI(
    title="Emotion Analysis API",
    version="1.0.0",
    docs_url="/api/docs",  # Swagger UI at /api/docs
    redoc_url="/api/redoc",  # ReDoc at /api/redoc
    openapi_url="/api/openapi.json"  # OpenAPI schema at /api/openapi.json
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and tokenizer
model = None
tokenizer = None
model_loading = False
model_load_error = None

# GoEmotions emotion labels (27 emotions + neutral)
GOEMOTIONS_LABELS = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring",
    "confusion", "curiosity", "desire", "disappointment", "disapproval", "disgust",
    "embarrassment", "excitement", "fear", "gratitude", "grief", "joy",
    "love", "nervousness", "optimism", "pride", "realization", "relief",
    "remorse", "sadness", "surprise", "neutral"
]

class TextInput(BaseModel):
    text: str

class EmotionPrediction(BaseModel):
    label: str
    score: float

class EmotionResponse(BaseModel):
    success: bool
    emotions: List[EmotionPrediction]
    text_analyzed: str

async def load_model_async():
    """Load the emotion analysis model asynchronously"""
    global model, tokenizer, model_loading, model_load_error
    
    if model is not None and tokenizer is not None:
        return  # Already loaded
    
    if model_loading:
        return  # Already loading
    
    model_loading = True
    model_load_error = None
    
    try:
        logger.info("Starting model download and loading...")
        start_time = time.time()
        
        # Load the model and tokenizer with timeout handling
        model_name = "wncelrcn/mindmap-MiniLM-goemotions-v1"
        
        logger.info("Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir="/tmp/transformers_cache"  # Use tmp for faster access
        )
        
        logger.info("Loading model...")
        model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            cache_dir="/tmp/transformers_cache"
        )
        model.eval()  # Set to evaluation mode
        
        # Fix the model's label configuration
        if hasattr(model.config, 'id2label') and len(GOEMOTIONS_LABELS) == len(model.config.id2label):
            logger.info("Updating model config with proper GoEmotions labels...")
            model.config.id2label = {i: label for i, label in enumerate(GOEMOTIONS_LABELS)}
            model.config.label2id = {label: i for i, label in enumerate(GOEMOTIONS_LABELS)}
            logger.info("Model config updated successfully!")
        else:
            logger.warning(f"Could not update model config - size mismatch: model has {len(model.config.id2label) if hasattr(model.config, 'id2label') else 'unknown'} labels, expected {len(GOEMOTIONS_LABELS)}")
        
        load_time = time.time() - start_time
        logger.info(f"Model loaded successfully in {load_time:.2f} seconds!")
        logger.info(f"Model config: {model.config}")
        
    except Exception as e:
        model_load_error = str(e)
        logger.error(f"Error loading model: {str(e)}")
        raise e
    finally:
        model_loading = False

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    logger.info("Application starting up...")
    # Don't load model on startup to avoid timeout
    # Model will be loaded on first request instead

@app.get("/api")
async def root():
    """Health check endpoint"""
    return {"message": "Emotion Analysis API is running", "status": "healthy"}

@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    global model, tokenizer, model_loading, model_load_error
    
    status = "healthy"
    model_status = "not_loaded"
    
    if model_load_error:
        status = "unhealthy"
        model_status = f"error: {model_load_error}"
    elif model_loading:
        model_status = "loading"
    elif model is not None and tokenizer is not None:
        model_status = "loaded"
    
    return {
        "status": status,
        "model_status": model_status,
        "model_name": "wncelrcn/mindmap-MiniLM-goemotions-v1",
        "model_type": "multi-label emotion classification"
    }

@app.post("/api/warmup")
async def warmup_model():
    """Manually trigger model loading for faster subsequent requests"""
    global model, tokenizer, model_loading, model_load_error
    
    if model is not None and tokenizer is not None:
        return {"message": "Model already loaded", "status": "ready"}
    
    if model_loading:
        return {"message": "Model is currently loading", "status": "loading"}
    
    try:
        await load_model_async()
        return {"message": "Model loaded successfully", "status": "ready"}
    except Exception as e:
        return {"message": f"Failed to load model: {str(e)}", "status": "error"}

@app.post("/api/predict", response_model=EmotionResponse)
async def predict_emotions(input_data: TextInput, threshold: float = 0.05):
    """
    Predict emotions from the input text using wncelrcn/mindmap-deBERTa-small-goemotions-v2 model
    Supports multi-label classification with configurable threshold
    """
    global model, tokenizer
    
    # Load model on first request if not already loaded
    if model is None or tokenizer is None:
        if model_load_error:
            raise HTTPException(status_code=500, detail=f"Model failed to load: {model_load_error}")
        
        try:
            await load_model_async()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")
    
    if not input_data.text.strip():
        raise HTTPException(status_code=400, detail="Text input cannot be empty")
    
    try:
        logger.info(f"Analyzing text: {input_data.text[:100]}...")
        
        # Tokenize input
        inputs = tokenizer(
            input_data.text, 
            return_tensors="pt", 
            truncation=True, 
            padding=True, 
            max_length=512
        )
        
        # Get prediction
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            # Apply sigmoid for multi-label classification
            probs = torch.sigmoid(logits)[0]
        
        # Use model's config labels if available, otherwise use our predefined labels
        labels = getattr(model.config, 'id2label', None)
        if labels and len(labels) == len(probs) and not any(label.startswith('LABEL_') for label in labels.values()):
            # Model config has proper labels
            logger.debug("Using model config labels")
            label_list = [labels[i] for i in range(len(labels))]
        else:
            # Fall back to our predefined labels
            logger.debug("Using predefined GoEmotions labels")
            label_list = GOEMOTIONS_LABELS
            if len(probs) != len(GOEMOTIONS_LABELS):
                logger.warning(f"Model output size ({len(probs)}) doesn't match expected labels ({len(GOEMOTIONS_LABELS)})")
        
        # Filter predictions above threshold and create emotion predictions
        emotions = []
        for i, prob in enumerate(probs):
            prob_value = float(prob)
            if prob_value > threshold and i < len(label_list):
                label = label_list[i]
                emotions.append(EmotionPrediction(label=label, score=prob_value))
        
        # Sort by score (highest first)
        emotions.sort(key=lambda x: x.score, reverse=True)
        
        logger.info(f"Found {len(emotions)} emotions above threshold {threshold}")
        logger.info(f"Top predictions: {[(e.label, f'{e.score:.3f}') for e in emotions[:5]]}")
        
        return EmotionResponse(
            success=True,
            emotions=emotions,
            text_analyzed=input_data.text
        )
        
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port) 