import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import { Activity, Target, AlertCircle, CheckCircle } from "lucide-react";
import { motion } from "framer-motion";

interface DashboardStats {
  accuracy: number;
  precision: number;
  recall: number;
  f1Score: number;
  trainingHistory: { epoch: number; accuracy: number; loss: number }[];
  classDistribution: { name: string; value: number }[];
  confusionMatrix: number[][];
}

const COLORS = ["#10b981", "#f59e0b", "#ef4444"];

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch("/api/dashboard-stats");
        if (response.ok) {
          const data = await response.json();
          setStats(data);
        }
      } catch (error) {
        console.error("Failed to fetch dashboard stats", error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="text-center text-red-600 p-8">
        Failed to load dashboard data.
      </div>
    );
  }

  const metrics = [
    { label: "Accuracy", value: `${stats.accuracy}%`, icon: Target, color: "text-indigo-600", bg: "bg-indigo-50" },
    { label: "Precision", value: `${stats.precision}%`, icon: CheckCircle, color: "text-emerald-600", bg: "bg-emerald-50" },
    { label: "Recall", value: `${stats.recall}%`, icon: AlertCircle, color: "text-amber-600", bg: "bg-amber-50" },
    { label: "F1 Score", value: `${stats.f1Score}%`, icon: Activity, color: "text-rose-600", bg: "bg-rose-50" },
  ];

  const classes = ["Normal", "Osteopenia", "Osteoporosis"];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-7xl mx-auto space-y-8"
    >
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          Model Performance Dashboard
        </h1>
        <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-indigo-100 text-indigo-800">
          MobileNetV2
        </span>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {metrics.map((metric) => (
          <div
            key={metric.label}
            className="bg-white overflow-hidden shadow-sm rounded-2xl border border-slate-200"
          >
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className={`p-3 rounded-xl ${metric.bg}`}>
                    <metric.icon className={`h-6 w-6 ${metric.color}`} aria-hidden="true" />
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-slate-500 truncate uppercase tracking-wider">
                      {metric.label}
                    </dt>
                    <dd>
                      <div className="text-2xl font-bold text-slate-900">
                        {metric.value}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Training Curve */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
          <h3 className="text-lg font-semibold text-slate-900 mb-6">
            Training Curve (Accuracy vs Loss)
          </h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={stats.trainingHistory}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="epoch" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis yAxisId="left" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis yAxisId="right" orientation="right" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip
                  contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                />
                <Legend wrapperStyle={{ paddingTop: '20px' }} />
                <Line
                  yAxisId="left"
                  type="monotone"
                  dataKey="accuracy"
                  stroke="#4f46e5"
                  strokeWidth={3}
                  dot={{ r: 4, strokeWidth: 2 }}
                  activeDot={{ r: 6 }}
                  name="Accuracy (%)"
                />
                <Line
                  yAxisId="right"
                  type="monotone"
                  dataKey="loss"
                  stroke="#f43f5e"
                  strokeWidth={3}
                  dot={{ r: 4, strokeWidth: 2 }}
                  activeDot={{ r: 6 }}
                  name="Loss"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Class Distribution */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
          <h3 className="text-lg font-semibold text-slate-900 mb-6">
            Dataset Class Distribution
          </h3>
          <div className="h-80 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={stats.classDistribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={80}
                  outerRadius={120}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {stats.classDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                />
                <Legend verticalAlign="bottom" height={36} iconType="circle" />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Confusion Matrix */}
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 lg:col-span-2">
          <h3 className="text-lg font-semibold text-slate-900 mb-6">
            Confusion Matrix
          </h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-200 text-sm text-left">
              <thead>
                <tr>
                  <th className="px-6 py-4 font-medium text-slate-500 bg-slate-50">
                    True \ Predicted
                  </th>
                  {classes.map((c) => (
                    <th key={c} className="px-6 py-4 font-medium text-slate-900 bg-slate-50">
                      {c}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 bg-white">
                {stats.confusionMatrix.map((row, i) => (
                  <tr key={i}>
                    <td className="px-6 py-4 font-medium text-slate-900 bg-slate-50">
                      {classes[i]}
                    </td>
                    {row.map((val, j) => {
                      const isDiagonal = i === j;
                      const intensity = Math.min(val / 1000, 1);
                      return (
                        <td
                          key={j}
                          className="px-6 py-4 text-center font-mono"
                          style={{
                            backgroundColor: isDiagonal
                              ? `rgba(16, 185, 129, ${intensity * 0.5 + 0.1})`
                              : `rgba(239, 68, 68, ${intensity * 2 + 0.05})`,
                            color: isDiagonal && intensity > 0.5 ? 'white' : 'inherit',
                            fontWeight: isDiagonal ? 'bold' : 'normal',
                          }}
                        >
                          {val}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="text-xs text-slate-500 mt-4 text-center">
            Diagonal cells (green) represent correct predictions. Off-diagonal cells (red) represent misclassifications.
          </p>
        </div>
      </div>
    </motion.div>
  );
}
