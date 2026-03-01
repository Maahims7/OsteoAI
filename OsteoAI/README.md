# OsteoAI

Early Osteoporosis Detection using Deep Learning

This project uses transfer learning (MobileNetV2) to classify X-ray images into Normal, Osteopenia, or Osteoporosis.

It includes a Flask web application that allows users to upload images, view predictions with confidence scores, generate Grad-CAM explainability heatmaps, and produce a professional patient report with AI-generated recommendations.

## Structure

```
OsteoAI/
│
├── dataset/
│   ├── train/
│   │   ├── Normal/
│   │   ├── Osteopenia/
│   │   ├── Osteoporosis/
│   │
│   ├── val/
│   └── test/
│
├── models/
│   └── best_model.h5
│
├── static/
│   ├── uploads/
│   ├── heatmaps/
│   ├── css/
│   │   └── style.css
│   ├── js/
│
├── templates/
│   ├── index.html
│   ├── result.html
│   ├── dashboard.html
│
├── utils/
│   ├── preprocessing.py
│   ├── predict.py
│   ├── gradcam.py
│   ├── report_logic.py
│
├── train.py
├── app.py
├── requirements.txt
└── README.md
```

Refer to project blueprint provided by the user for detailed functionality.