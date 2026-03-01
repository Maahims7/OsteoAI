# 🏥 OsteoAI - AI-Powered Bone Density Analysis System

**Production-Ready Medical AI Application** | Flask Backend | Multi-Page Interactive Frontend | Deep Learning Classification

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual Environment (venv)
- ~500MB disk space (for model + dataset)

### Installation & Run

```bash
# 1. Navigate to project
cd OsteoAI

# 2. Activate virtual environment (Windows)
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run Flask server
python app.py
```

**App launches at:** `http://127.0.0.1:5000`

---

## 📁 Project Structure

```
OsteoAI/
├── app.py                    # Flask backend (main server)
├── requirements.txt          # Python dependencies
├── train.py                  # Model training script
├── split_dataset.py          # Dataset 70/15/15 splitter
├── verify_and_split.py       # Dataset verification tool
│
├── dataset/                  # 1,947 X-ray images (pre-split)
│   ├── train/  (69.9%) - 1,361 images
│   ├── val/    (15.0%) - 293 images
│   └── test/   (15.0%) - 293 images
│
├── models/
│   └── best_model.h5         # Trained MobileNetV2 model
│
├── static/
│   ├── uploads/              # User X-ray uploads
│   ├── heatmaps/             # Grad-CAM visual explanations
│   ├── css/                  # Tailwind styling
│   ├── js/                   # Interactive components
│   └── videos/               # Educational content
│
├── templates/
│   ├── base.html             # Master layout
│   ├── splash.html           # Animated opening page
│   ├── intro.html            # Educational content + video upload
│   ├── index.html            # Patient form + X-ray upload
│   ├── result.html           # Prediction results + prescriptions
│   ├── graph.html            # Bone density visualization
│   ├── report.html           # Printable medical report
│   ├── dashboard.html        # Model performance metrics
│   └── about.html            # About the system
│
├── utils/
│   ├── predict.py            # Model inference
│   ├── preprocessing.py      # Image normalization
│   ├── gradcam.py            # Explainability heatmaps
│   ├── report_logic.py       # Stage classification + prescriptions
│   └── graph_logic.py        # Density calculations
│
└── documentation/
    ├── DEPLOYMENT_GUIDE.md   # This file
    ├── API_REFERENCE.md      # Route documentation
    └── TRAINING_GUIDE.md     # Model retraining steps
```

---

## 🌊 User Flow

```
Homepage (Splash) 
    ↓
    → Intro Page (Educational Content)
    ↓
    → Patient Form (Demographics + X-ray Upload)
    ↓
    → AI Analysis (Prediction + Grad-CAM)
    ↓
    → Bone Density Graph (Visual Results)
    ↓
    → Medical Report (Printable Form)
    ↓
    → Dashboard (Model Metrics)
```

---

## 🔗 API Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Splash screen (animated intro) |
| `/intro` | GET | Educational page + video upload |
| `/patient` | GET | Patient intake form |
| `/predict` | POST | Process X-ray + predict + generate Grad-CAM |
| `/graph` | GET | Bone density graph visualization |
| `/report` | GET | Final printable medical report |
| `/dashboard` | GET | Model training metrics & confusion matrix |
| `/about` | GET | System information |

---

## 📊 Dataset

**1,947 X-ray images** across 3 bone density classes:

| Class | Train | Val | Test | Total |
|-------|-------|-----|------|-------|
| Normal | 545 | 118 | 117 | 780 |
| Osteopenia | 261 | 56 | 57 | 374 |
| Osteoporosis | 555 | 119 | 119 | 793 |
| **TOTAL** | **1,361** | **293** | **293** | **1,947** |

**Split Ratio:** 70% Train / 15% Val / 15% Test ✅

---

## 🧠 Model Architecture

**Base Model:** MobileNetV2 (Transfer Learning)  
**Input:** 224×224 RGB images  
**Output:** 3-class soft max (Normal, Osteopenia, Osteoporosis)  
**Training:** Adam optimizer (lr=0.0001), Categorical Crossentropy loss  
**Val Accuracy:** 72.7% | **Test Accuracy:** 70.0%

**Custom Layers:**
```python
GlobalAveragePooling2D()
→ Dense(128, ReLU)
→ Dropout(0.5)
→ Dense(3, Softmax)
```

---

## 💊 AI-Generated Recommendations

The system automatically generates personalized:
- **Vitamins:** Vitamin D3, Calcium Citrate dosages
- **Foods:** Dairy, greens, fatty fish recommendations
- **Exercise:** Weight-bearing activity guidelines
- **Follow-up:** DEXA scan scheduling

**Eligibility Stages:**
- 🟢 **Normal** → Maintenance recommendations
- 🟡 **Mild** → Enhanced monitoring + supplementation
- 🟠 **Moderate** → Medical consultation + treatment
- 🔴 **Severe** → URGENT specialist referral

---

## 🎨 Frontend Features

✅ **Responsive Design** (Mobile-first Tailwind CSS)  
✅ **Animated Splash Screen** (CSS gradient + scanner effects)  
✅ **Interactive Charts** (Chart.js bone density visualization)  
✅ **Drag-and-Drop Upload** (X-ray + patient photo)  
✅ **Grad-CAM Explainability** (AI transparency heatmaps)  
✅ **Printable Reports** (HIPAA-compliant medical documentation)  
✅ **Dark Mode Ready** (Tailwind utilities)

---

## 🔒 Security & HIPAA

- ✅ **File Upload Validation** (PNG, JPG only; 16MB max)
- ✅ **Secure Filenames** (werkzeug.security)
- ✅ **Session Management** (Flask secure sessions)
- ✅ **Medical Disclaimer** (Displayed on all pages)
- ✅ **No External API Calls** (Local inference only)
- ⚠️ **NOT CERTIFIED for Clinical Use** (Use for screening only)

---

## 🐛 Troubleshooting

### **Issue: Model not loading**
```bash
# Verify model exists
ls models/best_model.h5

# Retrain if missing
python train.py
```

### **Issue: TensorFlow import errors**
```bash
# Reinstall TF
pip install --upgrade tensorflow
```

### **Issue: Static files not loading**
```bash
# Verify static folder exists
mkdir -p static/{uploads,heatmaps,css,js,videos}

# Restart server
python app.py
```

### **Issue: Database/Session errors**
```bash
# Clear session cache and restart
rm -rf __pycache__
python app.py
```

---

## 📈 Performance Tuning

### For Production (Gunicorn)
```bash
pip install gunicorn
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

### For High Load (nginx reverse proxy)
```nginx
upstream flask_app {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://flask_app;
    }
}
```

### GPU Acceleration (Optional)
```bash
pip install tensorflow-gpu  # NVIDIA CUDA required
# Model will auto-detect and use GPU
```

---

## 📚 Extended Reading

- **Medical Background:** See [TRAINING_GUIDE.md](TRAINING_GUIDE.md)
- **API Details:** See [API_REFERENCE.md](API_REFERENCE.md)
- **Model Metrics:** `/dashboard` route shows live training curves
- **Dataset Info:** Run `python verify_and_split.py`

---

## 🤝 Contributing

To extend OsteoAI:

1. **Add new prediction classes:** Modify `dataset/` and retrain `train.py`
2. **Custom prescriptions:** Edit `utils/report_logic.py`
3. **New frontend pages:** Add `.html` to `templates/`, update `app.py` routes
4. **Model improvements:** Experiment with different backbones in `train.py`

---

## ⚖️ License & Disclaimer

**IMPORTANT:** This is a **proof-of-concept AI demonstration tool** and should **NOT** be used for clinical diagnosis without proper regulatory approval (FDA 510k, CE Mark, etc.).

**Always consult qualified healthcare professionals** for bone density assessment and osteoporosis management.

---

## 📞 Support

- **Questions?** Check `/dashboard` for model metrics
- **Data privacy?** All processing is local; no cloud uploads
- **Bug reports?** Enable debug mode: `python app.py --debug`

---

**Built with ❤️ | OsteoAI v4.0.2 | February 2026**
