import { motion } from 'framer-motion';
import { InformationCircleIcon } from '@heroicons/react/24/outline';

const FormField = ({
  label,
  name,
  type = 'text',
  value,
  onChange,
  placeholder,
  min,
  max,
  step,
  required = false,
  className = '',
  isSlider = false,
  unit,
  tooltip,
  ...props
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`relative mb-4 ${className}`}
    >
      <label
        htmlFor={name}
        className="block mb-2 text-sm font-medium text-gray-700 dark:text-gray-200"
      >
        {label} {required && <span className="text-red-500">*</span>}
        {tooltip && (
          <div className="group relative inline-block ml-1">
            <InformationCircleIcon className="h-4 w-4 text-gray-400 inline cursor-help" />
            <div className="absolute bottom-full mb-2 hidden group-hover:block w-48 p-2 bg-gray-800 text-white text-xs rounded shadow-lg z-50">
              {tooltip}
            </div>
          </div>
        )}
      </label>

      {isSlider ? (
        <div className="space-y-2">
          <input
            type="range"
            id={name}
            name={name}
            min={min}
            max={max}
            value={value}
            onChange={onChange}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
            {...props}
          />
          <div className="flex justify-between text-xs text-gray-600 dark:text-gray-400">
            <span>{min}{unit}</span>
            <span>{value}{unit}</span>
            <span>{max}{unit}</span>
          </div>
        </div>
      ) : (
        <input
          type={type}
          id={name}
          name={name}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          min={min}
          max={max}
          step={step}
          required={required}
          className="input-field"
          {...props}
        />
      )}
    </motion.div>
  );
};

export default FormField;
