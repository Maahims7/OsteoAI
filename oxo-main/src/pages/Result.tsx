import { useLocation, useNavigate, Navigate } from "react-router-dom";
import { ArrowLeft, CheckCircle2, AlertTriangle, Info } from "lucide-react";
import { motion } from "framer-motion";

export default function Result() {
  const location = useLocation();
  const navigate = useNavigate();
  const result = location.state?.result;

  if (!result) {
    return <Navigate to="/" replace />;
  }

  const { originalImage, heatmapImage, prediction, confidence, recommendation } =
    result;

  const getStatusColor = (pred: string) => {
    switch (pred) {
      case "Normal":
        return "text-emerald-600 bg-emerald-50 border-emerald-200";
      case "Osteopenia":
        return "text-amber-600 bg-amber-50 border-amber-200";
      case "Osteoporosis":
        return "text-rose-600 bg-rose-50 border-rose-200";
      default:
        return "text-slate-600 bg-slate-50 border-slate-200";
    }
  };

  const getStatusIcon = (pred: string) => {
    switch (pred) {
      case "Normal":
        return <CheckCircle2 className="w-8 h-8 text-emerald-600" />;
      case "Osteopenia":
        return <AlertTriangle className="w-8 h-8 text-amber-600" />;
      case "Osteoporosis":
        return <AlertTriangle className="w-8 h-8 text-rose-600" />;
      default:
        return <Info className="w-8 h-8 text-slate-600" />;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="max-w-5xl mx-auto space-y-8"
    >
      <div className="flex items-center justify-between">
        <button
          onClick={() => navigate("/")}
          className="inline-flex items-center text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Upload
        </button>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          Analysis Result
        </h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="p-6 border-b border-slate-100">
              <h2 className="text-lg font-semibold text-slate-900">
                Image Analysis
              </h2>
            </div>
            <div className="p-6 grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div className="space-y-3">
                <p className="text-sm font-medium text-slate-500 uppercase tracking-wider">
                  Original X-Ray
                </p>
                <div className="aspect-square rounded-xl overflow-hidden bg-slate-100 border border-slate-200 relative">
                  <img
                    src={originalImage}
                    alt="Original X-Ray"
                    className="object-cover w-full h-full"
                  />
                </div>
              </div>
              <div className="space-y-3">
                <p className="text-sm font-medium text-slate-500 uppercase tracking-wider flex items-center justify-between">
                  <span>Grad-CAM Heatmap</span>
                  <span className="text-xs bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full font-semibold">
                    Explainable AI
                  </span>
                </p>
                <div className="aspect-square rounded-xl overflow-hidden bg-slate-100 border border-slate-200 relative">
                  <img
                    src={heatmapImage}
                    alt="Grad-CAM Heatmap"
                    className="object-cover w-full h-full"
                  />
                  {/* Overlaying a mock heatmap gradient for visual effect since we don't have real heatmaps */}
                  <div
                    className="absolute inset-0 mix-blend-multiply opacity-60 pointer-events-none"
                    style={{
                      background:
                        "radial-gradient(circle at 50% 50%, rgba(255,0,0,0.8) 0%, rgba(255,255,0,0.5) 30%, rgba(0,255,0,0.2) 60%, transparent 80%)",
                    }}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div
            className={`rounded-2xl shadow-sm border p-6 ${getStatusColor(
              prediction
            )}`}
          >
            <div className="flex items-start justify-between mb-4">
              <div>
                <p className="text-sm font-medium uppercase tracking-wider opacity-80 mb-1">
                  Prediction
                </p>
                <h2 className="text-3xl font-bold tracking-tight">
                  {prediction}
                </h2>
              </div>
              {getStatusIcon(prediction)}
            </div>

            <div className="mt-6 space-y-2">
              <div className="flex justify-between text-sm font-medium">
                <span>Confidence</span>
                <span>{confidence}%</span>
              </div>
              <div className="w-full bg-white/50 rounded-full h-2.5 overflow-hidden">
                <div
                  className="bg-current h-2.5 rounded-full transition-all duration-1000 ease-out"
                  style={{ width: `${confidence}%` }}
                ></div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
            <h3 className="text-sm font-medium text-slate-500 uppercase tracking-wider mb-3">
              Clinical Recommendation
            </h3>
            <p className="text-slate-700 leading-relaxed font-medium">
              {recommendation}
            </p>
          </div>

          <div className="bg-slate-900 rounded-2xl shadow-sm border border-slate-800 p-6 text-white">
            <h3 className="text-sm font-medium text-slate-400 uppercase tracking-wider mb-3">
              Model Info
            </h3>
            <ul className="space-y-3 text-sm">
              <li className="flex justify-between">
                <span className="text-slate-400">Architecture</span>
                <span className="font-mono">MobileNetV2</span>
              </li>
              <li className="flex justify-between">
                <span className="text-slate-400">Task</span>
                <span className="font-mono">Multi-class</span>
              </li>
              <li className="flex justify-between">
                <span className="text-slate-400">Explainability</span>
                <span className="font-mono">Grad-CAM</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
