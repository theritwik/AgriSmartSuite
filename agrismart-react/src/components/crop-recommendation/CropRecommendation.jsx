import { useState } from 'react';
import { motion } from 'framer-motion';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import FormField from '../common/FormField';
import LoadingSpinner from '../common/LoadingSpinner';

const COLORS = ['#22c55e', '#64748b', '#3b82f6', '#f59e0b'];

const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
  const RADIAN = Math.PI / 180;
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);

  return (
    <text
      x={x}
      y={y}
      fill="white"
      textAnchor={x > cx ? 'start' : 'end'}
      dominantBaseline="central"
    >
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  );
};

const CropRecommendation = () => {
  const [formData, setFormData] = useState({
    Nitrogen: '',
    Phosporus: '', // <-- must match backend spelling
    Potassium: '',
    Temperature: '',
    Humidity: '',
    pH: '',
    Rainfall: '',
  });
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);    try {
      const response = await fetch('/predict-crop', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to get prediction');
      }

      const result = await response.json();
      setPrediction(result);
    } catch (err) {
      setError('Failed to get prediction. Please try again.');
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center mb-8"
      >
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          Crop Recommendation
        </h1>
        <p className="text-gray-600 dark:text-gray-300">
          Enter your soil and environmental parameters to get AI-powered crop recommendations.
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Form Section */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="card p-6"
        >
          <form onSubmit={handleSubmit} className="space-y-4">
            <FormField
              label="Nitrogen (N)"
              name="Nitrogen"
              type="number"
              value={formData.Nitrogen}
              onChange={handleChange}
              placeholder="Enter nitrogen content"
              required
            />
            <FormField
              label="Phosphorus (P)"
              name="Phosporus" // <-- must match backend spelling
              type="number"
              value={formData.Phosporus}
              onChange={handleChange}
              placeholder="Enter phosphorus content"
              required
            />
            <FormField
              label="Potassium (K)"
              name="Potassium"
              type="number"
              value={formData.Potassium}
              onChange={handleChange}
              placeholder="Enter potassium content"
              required
            />
            <FormField
              label="Temperature (°C)"
              name="Temperature"
              type="number"
              value={formData.Temperature}
              onChange={handleChange}
              placeholder="Enter temperature"
              step="0.1"
              required
            />
            <FormField
              label="Humidity (%)"
              name="Humidity"
              type="number"
              value={formData.Humidity}
              onChange={handleChange}
              placeholder="Enter humidity"
              required
            />
            <FormField
              label="pH Level"
              name="pH"
              type="number"
              value={formData.pH}
              onChange={handleChange}
              placeholder="Enter pH level"
              step="0.1"
              min="0"
              max="14"
              required
            />
            <FormField
              label="Rainfall (mm)"
              name="Rainfall"
              type="number"
              value={formData.Rainfall}
              onChange={handleChange}
              placeholder="Enter rainfall"
              required
            />
            <button
              type="submit"
              className="btn-primary w-full"
              disabled={isLoading}
            >
              {isLoading ? <LoadingSpinner size="sm" className="mx-auto" /> : 'Get Recommendation'}
            </button>
          </form>
        </motion.div>

        {/* Results Section */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="card p-6"
        >
          {error && (
            <div className="text-red-500 dark:text-red-400 text-center p-4">
              {error}
            </div>
          )}
            {prediction && !error && (
            <div className="text-center space-y-6">              <div className="relative h-64 mb-8">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={prediction.data}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={80}
                      fill="#8884d8"
                      paddingAngle={3}
                      dataKey="value"
                      labelLine={false}
                      label={renderCustomizedLabel}
                      nameKey="name"
                    >
                      {prediction.data.map((entry, index) => (
                        <Cell 
                          key={`cell-${index}`} 
                          fill={COLORS[index % COLORS.length]}
                          strokeWidth={2}
                        />
                      ))}
                    </Pie>
                    <Tooltip 
                      formatter={(value, name) => [`${value}%`, name]}
                      contentStyle={{
                        backgroundColor: 'rgba(255, 255, 255, 0.9)',
                        borderRadius: '0.5rem',
                        padding: '0.5rem',
                        border: 'none',
                        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
                      }}
                    />
                    <Legend 
                      verticalAlign="bottom" 
                      align="center"
                      layout="horizontal"
                      wrapperStyle={{
                        paddingTop: '1rem'
                      }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="p-6 bg-gray-50 dark:bg-gray-800 rounded-xl shadow-inner">
                <h3 className="text-2xl font-bold text-primary-600 dark:text-primary-400 mb-4">
                  Recommended Crop: {prediction.cropName}
                </h3>
                <p className="text-gray-700 dark:text-gray-300 text-lg">
                  {prediction.message}
                </p>
              </div>
            </div>
          )}

          {!prediction && !error && !isLoading && (
            <div className="text-center text-gray-500 dark:text-gray-400 p-8">
              Enter soil parameters to get crop recommendations
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default CropRecommendation;
