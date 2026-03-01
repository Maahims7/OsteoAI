import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { Upload, FileImage, AlertCircle, Loader2 } from "lucide-react";
import { motion } from "framer-motion";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      if (!selectedFile.type.startsWith("image/")) {
        setError("Please select an image file.");
        return;
      }
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setError(null);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files?.[0];
    if (droppedFile) {
      if (!droppedFile.type.startsWith("image/")) {
        setError("Please drop an image file.");
        return;
      }
      setFile(droppedFile);
      setPreview(URL.createObjectURL(droppedFile));
      setError(null);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("image", file);

    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        body: formData,
      });

      if (response.status !== 200) {
        const errorData = await response.json();
        alert(errorData.error || "Invalid image uploaded.");
        return;
      }

      const data = await response.json();
      navigate("/result", { state: { result: data } });
    } catch (err: any) {
      setError(err.message || "An error occurred during prediction.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="max-w-3xl mx-auto space-y-8"
    >
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-extrabold tracking-tight text-slate-900 sm:text-5xl">
          Early Osteoporosis Detection
        </h1>
        <p className="text-lg text-slate-600 max-w-2xl mx-auto">
          Upload a knee X-ray image to get an instant prediction of bone density
          health using our advanced MobileNetV2 deep learning model.
        </p>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 sm:p-10">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div
            className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors ${preview
                ? "border-indigo-300 bg-indigo-50"
                : "border-slate-300 hover:border-indigo-400 hover:bg-slate-50"
              }`}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept="image/*"
              className="hidden"
            />

            {preview ? (
              <div className="space-y-4">
                <img
                  src={preview}
                  alt="Preview"
                  className="max-h-64 mx-auto rounded-lg shadow-sm"
                />
                <p className="text-sm text-indigo-600 font-medium">
                  Click or drag to change image
                </p>
              </div>
            ) : (
              <div className="space-y-4 py-8 cursor-pointer">
                <div className="mx-auto w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center">
                  <Upload className="w-8 h-8 text-indigo-600" />
                </div>
                <div>
                  <p className="text-base font-medium text-slate-900">
                    Click to upload or drag and drop
                  </p>
                  <p className="text-sm text-slate-500 mt-1">
                    SVG, PNG, JPG or GIF (max. 10MB)
                  </p>
                </div>
              </div>
            )}
          </div>

          {error && (
            <div className="bg-red-50 text-red-700 p-4 rounded-lg flex items-start gap-3">
              <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
              <p className="text-sm font-medium">{error}</p>
            </div>
          )}

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={!file || loading}
              className="inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-lg text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-sm w-full sm:w-auto"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                  Analyzing Image...
                </>
              ) : (
                <>
                  <FileImage className="w-5 h-5 mr-2" />
                  Run Prediction
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-8 border-t border-slate-200">
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="font-semibold text-slate-900 mb-2">Multi-class CNN</h3>
          <p className="text-sm text-slate-600">
            Classifies X-rays into Normal, Osteopenia, or Osteoporosis using
            Transfer Learning (MobileNetV2).
          </p>
        </div>
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="font-semibold text-slate-900 mb-2">Explainable AI</h3>
          <p className="text-sm text-slate-600">
            Grad-CAM heatmaps highlight the specific regions of the X-ray that
            influenced the model's decision.
          </p>
        </div>
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="font-semibold text-slate-900 mb-2">Real-time Screening</h3>
          <p className="text-sm text-slate-600">
            Fast, accurate predictions deployed via a Flask backend for immediate
            clinical assistance.
          </p>
        </div>
      </div>
    </motion.div>
  );
}
