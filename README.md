# MindMap Emotion Analysis FastAPI Backend

This is a high-performance Python FastAPI backend that provides advanced emotion analysis using the **MiniLM** model fine-tuned on the GoEmotions dataset. The backend is specifically designed for the MindMap application to provide real-time, multi-label emotion detection from text input with exceptional accuracy and speed.

## 🚀 Features

- **🧠 MiniLM-based Emotion Analysis**: Uses the custom-trained `wncelrcn/mindmap-MiniLM-goemotions-v1` model for fast and accurate emotion detection
- **⚡ High Performance**: Lightweight MiniLM architecture provides faster inference than traditional BERT models
- **🎯 Multi-label Classification**: Detect multiple emotions simultaneously with configurable confidence thresholds
- **🔧 FastAPI Framework**: Modern, high-performance async API with automatic interactive documentation
- **🌐 CORS Support**: Fully configured to work seamlessly with Next.js and other frontend frameworks
- **📊 Health Monitoring**: Built-in endpoints to monitor backend status, model loading, and performance
- **🛡️ Robust Error Handling**: Comprehensive error handling with detailed feedback and logging
- **🔥 Smart Loading**: Lazy model loading and warmup capabilities for optimal resource usage

## 🎭 Supported Emotions (GoEmotions Dataset)

The model can detect **28 different emotions** based on the comprehensive GoEmotions dataset:

### Primary Emotions

- **Joy**, **Sadness**, **Anger**, **Fear**, **Surprise**, **Disgust**

### Extended Emotional Range

- **Admiration**, **Amusement**, **Annoyance**, **Approval**, **Caring**
- **Confusion**, **Curiosity**, **Desire**, **Disappointment**, **Disapproval**
- **Embarrassment**, **Excitement**, **Gratitude**, **Grief**, **Love**
- **Nervousness**, **Optimism**, **Pride**, **Realization**, **Relief**
- **Remorse**, **Neutral**

This extensive emotion set provides nuanced emotional understanding perfect for journaling, mood tracking, and psychological applications.

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

## 📚 API Endpoints

All endpoints are prefixed with `/api` for better organization and versioning.

### 🏥 Health Check Endpoints

#### Basic Health Check

```http
GET /api
```

Returns basic API status confirmation.

**Response:**

```json
{
  "message": "Emotion Analysis API is running",
  "status": "healthy"
}
```

#### Detailed Health Check

```http
GET /api/health
```

Returns comprehensive backend status including model loading state.

**Response:**

```json
{
  "status": "healthy",
  "model_status": "loaded",
  "model_name": "wncelrcn/mindmap-MiniLM-goemotions-v1",
  "model_type": "multi-label emotion classification"
}
```

#### Model Warmup

```http
POST /api/warmup
```

Manually triggers model loading for faster subsequent requests. Useful for production deployments.

**Response:**

```json
{
  "message": "Model loaded successfully",
  "status": "ready"
}
```

### 🎯 Emotion Prediction

#### Analyze Text Emotions

```http
POST /api/predict?threshold=0.05
```

**Query Parameters:**

- `threshold` (optional): Minimum confidence score for emotion detection (default: 0.05)

**Request Body:**

```json
{
  "text": "I'm feeling really excited about this new project! It makes me so happy and proud."
}
```

**Response (Multi-label):**

```json
{
  "success": true,
  "emotions": [
    {
      "label": "excitement",
      "score": 0.8945
    },
    {
      "label": "joy",
      "score": 0.7823
    },
    {
      "label": "pride",
      "score": 0.6234
    },
    {
      "label": "optimism",
      "score": 0.4567
    }
  ],
  "text_analyzed": "I'm feeling really excited about this new project! It makes me so happy and proud."
}
```

### 📖 Interactive API Documentation

Once the server is running, you can access comprehensive API documentation:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI Schema**: http://localhost:8000/api/openapi.json

## 🔌 Integration with Frontend Applications

### Next.js Integration

```javascript
// Example API call to the emotion analysis backend
const analyzeEmotion = async (text) => {
  try {
    const response = await fetch("http://localhost:8000/api/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });

    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Error analyzing emotion:", error);
    throw error;
  }
};

// Usage in component
const emotions = await analyzeEmotion("I'm feeling amazing today!");
console.log(emotions.emotions); // Array of detected emotions with scores
```

### React Component Example

```javascript
import { useState } from "react";

export default function EmotionAnalyzer() {
  const [text, setText] = useState("");
  const [emotions, setEmotions] = useState([]);
  const [loading, setLoading] = useState(false);

  const analyzeText = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const result = await response.json();
      setEmotions(result.emotions);
    } catch (error) {
      console.error("Analysis failed:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="emotion-analyzer">
      <h2>Emotion Analysis</h2>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter text to analyze emotions..."
        rows={4}
        cols={50}
      />
      <button onClick={analyzeText} disabled={loading || !text.trim()}>
        {loading ? "Analyzing..." : "Analyze Emotions"}
      </button>

      {emotions.length > 0 && (
        <div className="emotions-result">
          <h3>Detected Emotions:</h3>
          {emotions.map((emotion, index) => (
            <div key={index} className="emotion-item">
              <span className="emotion-label">{emotion.label}</span>
              <span className="emotion-score">
                {(emotion.score * 100).toFixed(1)}%
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

## 🤖 Model Information

- **Model**: `wncelrcn/mindmap-MiniLM-goemotions-v1`
- **Architecture**: MiniLM (Lightweight transformer model)
- **Dataset**: GoEmotions (Google's emotion dataset with 28 emotions)
- **Type**: Multi-label emotion classification
- **Framework**: Hugging Face Transformers
- **Model Size**: ~90MB (significantly smaller than traditional BERT models)
- **Performance**: Optimized for both accuracy and inference speed
- **Special Features**:
  - Multi-label classification (detect multiple emotions simultaneously)
  - Configurable confidence thresholds
  - Fast inference suitable for real-time applications

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

## 🔧 Troubleshooting

### Common Issues

1. **🤖 Model Loading Errors**

   ```bash
   Error loading model: HTTPSConnectionPool(host='huggingface.co'...)
   ```

   - **Solution**: Ensure stable internet connection for initial model download (~90MB)
   - **Disk Space**: Verify you have at least 500MB free space
   - **Cache Location**: Model is cached in `/tmp/transformers_cache` for faster access
   - **Retry**: Use the `/api/warmup` endpoint to manually trigger model loading

2. **🚢 Port Already in Use**

   ```bash
   Error: [Errno 48] Address already in use
   ```

   - **Quick Fix**: Change the port in `start_server.py` or environment variable `PORT`
   - **Find Process**: Use `lsof -i :8000` to find processes using port 8000
   - **Kill Process**: `kill -9 <PID>` to terminate the conflicting process

3. **🌐 CORS Errors**

   ```bash
   Access to fetch blocked by CORS policy
   ```

   - **Current Config**: Backend accepts all origins (`allow_origins=["*"]`)
   - **Debug**: Check browser dev tools for specific CORS error messages
   - **Custom Origins**: Modify `allow_origins` in `main.py` for production use

4. **💾 Memory Issues**

   - **Requirements**: MiniLM model needs only ~512MB RAM (much less than BERT)
   - **Optimization**: Model loads lazily on first request to save memory
   - **Monitoring**: Use `/api/health` to check model loading status

5. **⚡ Slow Performance**
   - **First Request**: Initial prediction may take 3-5 seconds while model loads
   - **Warmup**: Use `/api/warmup` endpoint before receiving traffic
   - **Threshold**: Adjust the `threshold` parameter to reduce processing time

### 🚀 Performance Tips

1. **Model Warmup Strategy**

   ```bash
   # Warm up the model after deployment
   curl -X POST "http://localhost:8000/api/warmup"
   ```

2. **Optimal Threshold Settings**

   - **Default**: 0.05 (balanced accuracy/speed)
   - **High Precision**: 0.15+ (fewer but more confident predictions)
   - **High Recall**: 0.01-0.03 (more emotions detected)

3. **Batch Processing**

   - Process multiple texts by making parallel requests
   - FastAPI handles concurrent requests efficiently
   - Model stays warm in memory between requests

4. **Resource Management**
   - **CPU**: MiniLM is optimized for CPU inference
   - **Memory**: Model loads once and stays in memory
   - **Caching**: Model files cached locally after first download

### 📝 Logs and Debugging

The server provides comprehensive logging:

```bash
INFO: Model loaded successfully in 2.34 seconds!
INFO: Analyzing text: I'm feeling great today...
INFO: Found 3 emotions above threshold 0.05
INFO: Top predictions: [('joy', '0.892'), ('optimism', '0.743'), ('excitement', '0.621')]
```

**Log Levels:**

- **INFO**: Model loading, prediction results
- **DEBUG**: Detailed tokenization and prediction info
- **WARNING**: Configuration mismatches, fallback behaviors
- **ERROR**: Failed predictions, model loading errors

**Enable Debug Logging:**

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 🧪 Testing the API

#### Basic Health Check

```bash
curl -X GET "http://localhost:8000/api"
```

#### Detailed Health Check

```bash
curl -X GET "http://localhost:8000/api/health"
```

#### Model Warmup

```bash
curl -X POST "http://localhost:8000/api/warmup"
```

#### Emotion Prediction (Default Threshold)

```bash
curl -X POST "http://localhost:8000/api/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "I am so excited about this project! It makes me feel proud and happy."}'
```

#### Emotion Prediction (Custom Threshold)

```bash
curl -X POST "http://localhost:8000/api/predict?threshold=0.1" \
     -H "Content-Type: application/json" \
     -d '{"text": "Mixed feelings about this situation."}'
```

#### Test with Complex Emotions

```bash
curl -X POST "http://localhost:8000/api/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "I feel nervous but also excited about starting this new job. There is some anxiety but also hope for the future."}'
```

### Adding New Features

1. **New Endpoints**: Add them to `main.py`
2. **Model Changes**: Update the model name in the startup function
3. **Response Format**: Modify the Pydantic models for different response structures

## 🏗️ Advanced Features

### Why MiniLM?

Our custom **MiniLM** model offers significant advantages over traditional BERT models:

- **🚀 Speed**: 3-4x faster inference time
- **💾 Memory Efficient**: Uses 70% less RAM than BERT-Large
- **📱 Mobile Friendly**: Small enough for edge deployment
- **🎯 Task-Optimized**: Fine-tuned specifically for emotion detection
- **🔧 Production Ready**: Stable, well-tested architecture

### GoEmotions Dataset Advantages

The **GoEmotions** dataset provides superior emotion detection:

- **📊 Comprehensive**: 28 emotions vs traditional 6-7 basic emotions
- **🎭 Nuanced**: Captures subtle emotional states like "realization" and "relief"
- **🔬 Research-Backed**: Developed by Google Research with rigorous validation
- **🌍 Real-World**: Trained on Reddit comments for authentic emotional expression
- **⚖️ Balanced**: Carefully curated to avoid bias and ensure representation

### Multi-Label Classification

Unlike traditional single-emotion models, our system detects **multiple emotions simultaneously**:

```json
{
  "text": "I'm nervous but excited about the interview",
  "emotions": [
    { "label": "nervousness", "score": 0.78 },
    { "label": "excitement", "score": 0.65 },
    { "label": "optimism", "score": 0.42 }
  ]
}
```

This reflects real human emotion complexity where multiple feelings coexist.

## 🚀 Production Deployment

### Docker Deployment

```dockerfile
# Use the provided Dockerfile
docker build -t mindmap-emotion-api .
docker run -p 8000:8000 mindmap-emotion-api
```

### Environment Configuration

```bash
# Production environment variables
export PORT=8000
export FASTAPI_BASE_URL=https://your-domain.com
export PYTHONPATH=/app
export TRANSFORMERS_CACHE=/app/cache
```

### Production Checklist

1. **🛡️ Security**

   - Configure specific CORS origins (remove `allow_origins=["*"]`)
   - Add authentication middleware if needed
   - Use HTTPS in production

2. **⚡ Performance**

   - Use gunicorn with multiple workers: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`
   - Set up model warmup in startup scripts
   - Configure proper cache directories

3. **📊 Monitoring**

   - Monitor `/api/health` endpoint
   - Set up logging aggregation
   - Track response times and error rates

4. **🔄 Load Balancing**

   - Use nginx or cloud load balancer
   - Configure health checks on `/api/health`
   - Set proper timeouts for model loading

5. **💾 Resource Management**
   - Allocate at least 1GB RAM per instance
   - Use SSD storage for model caching
   - Monitor CPU usage during peak loads

## 📞 Support & Troubleshooting

### Quick Diagnostic Steps

1. **🔍 Check Health Status**

   ```bash
   curl http://localhost:8000/api/health
   ```

2. **📋 Review Logs**

   - Check console output for detailed error messages
   - Look for model loading status and timing information

3. **🔄 Force Model Reload**

   ```bash
   curl -X POST http://localhost:8000/api/warmup
   ```

4. **✅ Verify Dependencies**
   ```bash
   pip list | grep -E "(fastapi|transformers|torch)"
   ```

### Getting Help

- **📖 API Docs**: Visit `/api/docs` for interactive testing
- **🐛 Issues**: Check logs for specific error messages
- **🔧 Configuration**: Verify environment variables and CORS settings
- **💡 Performance**: Use the warmup endpoint for production deployments

## 📊 Project Structure

```
Backend-MindMap-v3/
├── main.py                 # FastAPI application with emotion analysis
├── start_server.py         # Server startup script
├── setup.py               # Automated setup for dependencies
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── render.yaml           # Deployment configuration
└── README.md             # This comprehensive guide
```

## 📈 Version History & Updates

### v3.0 - MiniLM Migration (Current)

- ✅ Upgraded from BERT to MiniLM for faster inference
- ✅ Implemented GoEmotions dataset (28 emotions)
- ✅ Added multi-label emotion classification
- ✅ Introduced configurable confidence thresholds
- ✅ Added model warmup endpoint
- ✅ Improved API documentation with /api prefix
- ✅ Enhanced error handling and logging

### Key Improvements Over v2.0

- **Speed**: 3-4x faster emotion predictions
- **Accuracy**: More nuanced emotion detection with 28 categories
- **Reliability**: Better error handling and model loading
- **Usability**: Comprehensive API documentation and testing examples

## 🎯 Use Cases

This emotion analysis backend is perfect for:

- **📔 Journaling Apps**: Analyze daily journal entries for emotional patterns
- **💬 Chat Applications**: Real-time emotion detection in conversations
- **📊 Mental Health Tools**: Track emotional well-being over time
- **🎓 Educational Platforms**: Analyze student feedback and engagement
- **📝 Content Analysis**: Understand emotional tone in text content
- **🤖 Chatbots**: Create emotionally-aware conversational agents

## 🔮 Future Enhancements

Planned improvements include:

- 🌐 Multiple language support
- 📱 Mobile SDK integration
- 🔄 Real-time streaming analysis
- 📊 Emotion trend analytics
- 🎨 Emotion visualization endpoints

---

**Built with ❤️ for the MindMap ecosystem**

_This backend provides the emotional intelligence foundation for creating empathetic, responsive applications that understand human emotions at scale._
