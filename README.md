# Emotion Analysis FastAPI Backend

This is a Python FastAPI backend that provides emotion analysis using the Hugging Face `boltuix/bert-emotion` model. It's designed to work with your Next.js frontend to provide real-time emotion detection from text input.

## Features

- **BERT-based Emotion Analysis**: Uses the `boltuix/bert-emotion` model for accurate emotion detection
- **FastAPI Framework**: High-performance async API with automatic documentation
- **CORS Support**: Configured to work seamlessly with your Next.js frontend
- **Health Checks**: Built-in endpoints to monitor backend status and model loading
- **Error Handling**: Comprehensive error handling with detailed feedback
- **Real-time Processing**: Fast inference with pre-loaded model

## Supported Emotions

The model can detect the following emotions:

- Joy
- Sadness
- Anger
- Fear
- Surprise
- Disgust
- Neutral

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Quick Setup

1. **Navigate to the backend directory:**

   ```bash
   cd backend
   ```

2. **Run the setup script:**

   ```bash
   python setup.py
   ```

3. **Start the server:**
   ```bash
   python start_server.py
   ```

### Manual Setup

If you prefer to set up manually:

1. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment:**

   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Start the server:**
   ```bash
   python start_server.py
   ```

## Usage

### Starting the Server

```bash
cd backend
python start_server.py
```

The server will start on `http://localhost:8000`

### API Endpoints

#### Health Check

```
GET /health
```

Returns the backend status and model loading state.

#### Root Endpoint

```
GET /
```

Basic health check endpoint.

#### Emotion Prediction

```
POST /predict
```

**Request Body:**

```json
{
  "text": "I'm feeling really happy today!"
}
```

**Response:**

```json
{
  "success": true,
  "emotions": [
    {
      "label": "joy",
      "score": 0.8945
    },
    {
      "label": "neutral",
      "score": 0.0823
    }
  ],
  "text_analyzed": "I'm feeling really happy today!"
}
```

### API Documentation

Once the server is running, you can access:

- **Interactive API docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

## Integration with Next.js Frontend

Your Next.js app can use the backend through the provided API endpoint:

```javascript
// pages/api/analyze-journal/journal_emotions_fastapi.js
const response = await axios.post(
  "/api/analyze-journal/journal_emotions_fastapi",
  {
    journal_text: "Your text here",
  }
);
```

## Example Frontend Usage

```javascript
import EmotionAnalyzer from "../components/EmotionAnalyzer";

export default function EmotionPage() {
  return (
    <div>
      <h1>Emotion Analysis</h1>
      <EmotionAnalyzer />
    </div>
  );
}
```

## Model Information

- **Model**: `boltuix/bert-emotion`
- **Type**: BERT-based sequence classification
- **Framework**: Hugging Face Transformers
- **Performance**: Optimized for accuracy and speed

## Configuration

### Environment Variables

You can configure the backend using environment variables:

- `FASTAPI_BASE_URL`: Backend URL (default: http://localhost:8000)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)

### CORS Configuration

The backend is configured to accept requests from:

- `http://localhost:3000` (Next.js development server)
- `http://127.0.0.1:3000`

To add more origins, modify the `allow_origins` list in `main.py`.

## Troubleshooting

### Common Issues

1. **Model Loading Errors**

   - Ensure you have sufficient disk space (model is ~500MB)
   - Check internet connection for initial model download
   - Verify Python version compatibility

2. **Port Already in Use**

   ```bash
   Error: [Errno 48] Address already in use
   ```

   - Change the port in `start_server.py` or kill the existing process
   - Use `lsof -i :8000` to find processes using port 8000

3. **CORS Errors**

   - Verify your frontend is running on an allowed origin
   - Check the `allow_origins` configuration in `main.py`

4. **Memory Issues**
   - The model requires ~2GB RAM
   - Close other applications if experiencing memory pressure

### Performance Tips

1. **First Request Delay**: The first prediction may take longer as the model loads into memory
2. **Model Caching**: The model stays loaded in memory for subsequent requests
3. **Concurrent Requests**: FastAPI handles multiple requests efficiently

### Logs and Debugging

The server provides detailed logging:

- Model loading status
- Request processing times
- Error details with stack traces

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing the API

You can test the API using curl:

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "I am so excited about this project!"}'
```

### Adding New Features

1. **New Endpoints**: Add them to `main.py`
2. **Model Changes**: Update the model name in the startup function
3. **Response Format**: Modify the Pydantic models for different response structures

## Production Deployment

For production deployment, consider:

1. **Process Manager**: Use gunicorn or similar
2. **Environment Variables**: Set proper environment variables
3. **Resource Limits**: Configure memory and CPU limits
4. **Health Monitoring**: Set up monitoring for the `/health` endpoint
5. **Load Balancing**: Use nginx or similar for load balancing

## Support

If you encounter issues:

1. Check the console logs for detailed error messages
2. Verify the model is properly loaded via `/health` endpoint
3. Ensure all dependencies are correctly installed
4. Check the GitHub issues for similar problems

## License

This backend is part of your MindMap application and follows the same licensing terms.
