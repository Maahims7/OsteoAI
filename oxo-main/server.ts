import express from "express";
import { createServer as createViteServer } from "vite";
import multer from "multer";
import path from "path";
import fs from "fs";

const uploadDir = path.join(process.cwd(), "uploads");
const heatmapsDir = path.join(process.cwd(), "heatmaps");

if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir, { recursive: true });
if (!fs.existsSync(heatmapsDir)) fs.mkdirSync(heatmapsDir, { recursive: true });

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + "-" + file.originalname);
  },
});

const upload = multer({ storage });

async function startServer() {
  const app = express();
  const PORT = parseInt(process.env.PORT || '3000', 10);

  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));
  app.use("/uploads", express.static(uploadDir));
  app.use("/heatmaps", express.static(heatmapsDir));

  // API routes
  app.get("/api/health", (req, res) => {
    res.json({ status: "ok" });
  });

  app.post("/api/predict", upload.single("image"), (req, res) => {
    try {
      if (!req.file) {
        return res.status(400).json({ error: "No image uploaded" });
      }

      // Mock prediction logic
      const classes = ["Normal", "Osteopenia", "Osteoporosis"];
      const predictedClass = classes[Math.floor(Math.random() * classes.length)];
      const confidence = (Math.random() * 20 + 80).toFixed(2); // 80-100%

      // Mock heatmap generation (just returning the original image for now, or a placeholder)
      // In a real app, you would run the model and save the heatmap to heatmapsDir
      const heatmapUrl = `/uploads/${req.file.filename}`; // Mocking heatmap with original image

      res.json({
        success: true,
        originalImage: `/uploads/${req.file.filename}`,
        heatmapImage: heatmapUrl,
        prediction: predictedClass,
        confidence: confidence,
        recommendation:
          predictedClass === "Osteoporosis"
            ? "High risk of reduced bone density detected. Recommend clinical evaluation."
            : predictedClass === "Osteopenia"
              ? "Moderate risk detected. Recommend lifestyle changes and follow-up."
              : "Bone density appears normal. Maintain a healthy lifestyle.",
      });
    } catch (error) {
      console.error("Prediction error:", error);
      res.status(500).json({ error: "Prediction failed" });
    }
  });

  app.get("/api/dashboard-stats", (req, res) => {
    try {
      res.json({
        accuracy: 94.5,
        precision: 93.2,
        recall: 95.1,
        f1Score: 94.1,
        trainingHistory: [
          { epoch: 1, accuracy: 65, loss: 1.2 },
          { epoch: 2, accuracy: 75, loss: 0.9 },
          { epoch: 3, accuracy: 82, loss: 0.7 },
          { epoch: 4, accuracy: 86, loss: 0.5 },
          { epoch: 5, accuracy: 89, loss: 0.4 },
          { epoch: 6, accuracy: 91, loss: 0.35 },
          { epoch: 7, accuracy: 92, loss: 0.3 },
          { epoch: 8, accuracy: 93, loss: 0.25 },
          { epoch: 9, accuracy: 93.5, loss: 0.22 },
          { epoch: 10, accuracy: 94, loss: 0.2 },
          { epoch: 11, accuracy: 94.2, loss: 0.18 },
          { epoch: 12, accuracy: 94.5, loss: 0.15 },
        ],
        classDistribution: [
          { name: "Normal", value: 1200 },
          { name: "Osteopenia", value: 800 },
          { name: "Osteoporosis", value: 600 },
        ],
        confusionMatrix: [
          [1150, 40, 10],
          [30, 740, 30],
          [5, 25, 570],
        ],
      });
    } catch (error) {
      console.error("Dashboard stats error:", error);
      res.status(500).json({ error: "Failed to fetch dashboard stats" });
    }
  });

  // Error handling middleware
  app.use((err: any, req: any, res: any, next: any) => {
    console.error("Server error:", err);
    res.status(500).json({ error: "Internal server error" });
  });

  // 404 handler for API routes
  app.use("/api", (req, res) => {
    res.status(404).json({ error: "Not found" });
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);

    // SPA fallback
    app.get("*", (req, res) => {
      res.redirect("/");
    });
  } else {
    app.use(express.static(path.join(process.cwd(), "dist")));
    app.get("*", (req, res) => {
      res.sendFile(path.join(process.cwd(), "dist", "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`🚀 Server running on http://0.0.0.0:${PORT}`);
  });
}

startServer().catch((err) => {
  console.error("Failed to start server:", err);
  process.exit(1);
});
