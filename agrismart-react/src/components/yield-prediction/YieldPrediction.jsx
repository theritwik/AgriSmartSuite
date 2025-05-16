import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';
import FormField from '../common/FormField';
import LoadingSpinner from '../common/LoadingSpinner';

const YieldPrediction = () => {
  const [formData, setFormData] = useState({
    Year: new Date().getFullYear(),
    average_rain_fall_mm_per_year: '',
    pesticides_tonnes: '',
    avg_temp: '',
    Area: '',
    Crop: '',
  });

  const [availableOptions, setAvailableOptions] = useState({
    areas: [],
    crops: [],
    yearRange: { min: 1990, max: 2024 },
    stats: {
      avg_rainfall: 0,
      max_rainfall: 0,
      min_rainfall: 0,
      avg_temp: 0,
      max_temp: 0,
      min_temp: 0,
      avg_pesticides: 0,
      max_pesticides: 0,
      min_pesticides: 0,
      yield_stats: {
        avg_yield: 0,
        max_yield: 0,
        min_yield: 0
      }
    }
  });

  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [optionsLoadFailed, setOptionsLoadFailed] = useState(false);

  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const response = await fetch('/api/available-options');
        if (!response.ok) {
          throw new Error('Failed to fetch options');
        }
        const data = await response.json();
        setAvailableOptions(data);
        setFormData(prev => ({
          ...prev,
          Area: data.areas[0] || '',
          Crop: data.crops[0] || '',
        }));
        setOptionsLoadFailed(false);
      } catch (err) {
        console.error('Error fetching options:', err);
        setOptionsLoadFailed(true);
        setError(null); // Don't show error in red at top
      }
    };
    fetchOptions();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    // Convert empty strings to '0' for number fields
    const processedValue = (
      e.target.type === 'number' && value === '' 
        ? '0' 
        : value
    );
    
    setFormData(prev => ({
      ...prev,
      [name]: processedValue
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    
    // Validate form data before submission
    const numericFields = ['Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp'];
    const formDataToSubmit = {
      ...formData,
      // Convert string values to numbers for numeric fields
      ...Object.fromEntries(
        numericFields.map(field => [field, parseFloat(formData[field] || '0')])
      )
    };
    
    try {
      const response = await fetch('/predict-yield', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(formDataToSubmit),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to get prediction');
      }

      const result = await response.json();
      setPrediction(result);
    } catch (err) {
      setError(err.message || 'Failed to get prediction. Please try again.');
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
          Crop Yield Prediction
        </h1>
        <p className="text-gray-600 dark:text-gray-300">
          Enter location and environmental parameters to get AI-powered yield predictions.
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
          {availableOptions.top_combinations?.length > 0 && (
            <div className="mb-6 p-4 bg-green-50 dark:bg-green-900 rounded-md">
              <h3 className="text-lg font-semibold text-green-800 dark:text-green-100 mb-2">Top Performers</h3>
              <div className="space-y-2">
                {availableOptions.top_combinations.slice(0, 3).map((combo, index) => (
                  <div key={index} className="text-sm flex items-center space-x-2">
                    <span className="text-green-600 dark:text-green-400 font-medium">{index + 1}.</span>
                    <span className="text-green-800 dark:text-green-200">{combo.crop}</span>
                    <span className="text-green-600 dark:text-green-400">in</span>
                    <span className="text-green-800 dark:text-green-200">{combo.area}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {optionsLoadFailed && (
              <div className="mb-4 p-4 bg-yellow-50 dark:bg-yellow-900 rounded-md text-yellow-800 dark:text-yellow-200 text-center border border-yellow-300 dark:border-yellow-700">
                <span className="font-semibold">Could not load area/crop options.</span><br/>
                <span>Please check your connection or try refreshing the page.</span>
              </div>
            )}
            <FormField
              label="Area"
              name="Area"
              type="select"
              value={formData.Area}
              onChange={handleChange}
              options={availableOptions.areas}
              required
            />
            <FormField
              label="Crop"
              name="Crop"
              type="select"
              value={formData.Crop}
              onChange={handleChange}
              options={availableOptions.crops}
              required
            />
            <FormField
              label="Year"
              name="Year"
              type="number"
              value={formData.Year}
              onChange={handleChange}
              min={availableOptions.yearRange.min}
              max={availableOptions.yearRange.max}
              required
            />
            <FormField
              label="Average Rainfall (mm/year)"
              name="average_rain_fall_mm_per_year"
              type="number"
              value={formData.average_rain_fall_mm_per_year}
              onChange={handleChange}
              placeholder="Enter rainfall from dataset (e.g. 657)"
              min={undefined}
              max={undefined}
              step="0.01"
              required
            />
            <FormField
              label="Pesticides (tonnes)"
              name="pesticides_tonnes"
              type="number"
              value={formData.pesticides_tonnes}
              onChange={handleChange}
              placeholder="Enter pesticides from dataset (e.g. 121)"
              min={undefined}
              max={undefined}
              step="0.01"
              required
            />
            <FormField
              label="Average Temperature (°C)"
              name="avg_temp"
              type="number"
              value={formData.avg_temp}
              onChange={handleChange}
              placeholder="Enter temperature from dataset (e.g. 16)"
              min={undefined}
              max={undefined}
              step="0.01"
              required
            />

            {error && (
              <div className="text-red-500 dark:text-red-400 text-sm mt-2">{error}</div>
            )}

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              type="submit"
              className="btn-primary w-full"
              disabled={isLoading}
            >
              {isLoading ? <LoadingSpinner size="sm" /> : 'Get Prediction'}
            </motion.button>
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
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-bold text-primary-600 dark:text-primary-400 mb-2">
                  {formData.Crop} in {formData.Area}
                </h3>
                <p className="text-gray-600 dark:text-gray-300">
                  {prediction.message}
                </p>
              </div>

              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={prediction.data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" angle={-45} textAnchor="end" height={60} />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="value" fill="#0ea5e9" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {prediction.historical_data?.length > 0 && (
                <div>
                  <h4 className="text-lg font-semibold mb-4 text-gray-700 dark:text-gray-300">Historical Trends</h4>
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={prediction.historical_data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="year" />
                        <YAxis yAxisId="left" />
                        <YAxis yAxisId="right" orientation="right" />
                        <Tooltip />
                        <Legend />
                        <Line yAxisId="left" type="monotone" dataKey="yield" stroke="#0ea5e9" name="Yield (hg/ha)" />
                        <Line yAxisId="right" type="monotone" dataKey="temperature" stroke="#f59e0b" name="Temperature (°C)" />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              )}

              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <h4 className="font-semibold mb-2 text-gray-700 dark:text-gray-300">Prediction Details</h4>
                  <ul className="space-y-1 text-gray-600 dark:text-gray-400">
                    <li>Predicted Yield: {prediction.prediction.toLocaleString()} hg/ha</li>
                    <li>Avg. Historical: {prediction.metadata.average_historical_yield.toLocaleString()} hg/ha</li>
                    <li>Change: {prediction.metadata.yield_difference_percent.toFixed(1)}%</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-semibold mb-2 text-gray-700 dark:text-gray-300">Environmental Factors</h4>
                  <ul className="space-y-1 text-gray-600 dark:text-gray-400">
                    <li>Temperature: {formData.avg_temp}°C</li>
                    <li>Rainfall: {formData.average_rain_fall_mm_per_year} mm/year</li>
                    <li>Pesticides: {formData.pesticides_tonnes} tonnes</li>
                  </ul>
                </div>
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default YieldPrediction;
