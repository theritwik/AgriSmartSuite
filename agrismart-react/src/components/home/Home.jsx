import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  ChartBarIcon,
  LightBulbIcon,
  ArrowTrendingUpIcon,
} from '@heroicons/react/24/outline';

const features = [
  {
    name: 'Smart Crop Recommendations',
    description:
      'Get AI-powered suggestions for the best crops to grow based on soil conditions and climate data.',
    icon: LightBulbIcon,
    link: '/crop-recommendation',
  },
  {
    name: 'Yield Predictions',
    description:
      'Predict your crop yields accurately using advanced machine learning models and historical data.',
    icon: ChartBarIcon,
    link: '/yield-prediction',
  },
  {
    name: 'Maximize Productivity',
    description:
      'Make data-driven decisions to optimize your farming operations and increase productivity.',
    icon: ArrowTrendingUpIcon,
    link: '/yield-prediction',
  },
];

const Home = () => {
  return (
    <div className="space-y-16 py-8">
      {/* Hero Section */}
      <section className="relative">
        <div
          className="absolute inset-0 bg-[url('/farm-pattern.svg')] opacity-10 dark:opacity-5"
          style={{ backgroundSize: '100px 100px' }}
        />
        <div className="relative max-w-4xl mx-auto text-center">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-4xl sm:text-5xl font-bold text-gray-900 dark:text-white mb-6"
          >
            Smart Agriculture Solutions
            <span className="text-primary-600 dark:text-primary-400"> for Tomorrow</span>
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-xl text-gray-600 dark:text-gray-300 mb-8"
          >
            Harness the power of AI and machine learning to make better farming decisions
            and increase your agricultural productivity.
          </motion.p>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="flex flex-wrap justify-center gap-4"
          >
            <Link
              to="/crop-recommendation"
              className="btn-primary"
            >
              Get Crop Recommendations
            </Link>
            <Link
              to="/yield-prediction"
              className="px-6 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 
                     rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-all duration-200 
                     transform hover:scale-105"
            >
              Predict Yields
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.name}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >                <Link
                  to={feature.link}
                  className="group p-6 h-full rounded-xl transition-transform duration-200 transform hover:scale-105"
                >
                  <div className="inline-flex items-center justify-center">
                    <feature.icon className="h-10 w-10 text-primary-600 dark:text-primary-400" /></div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                    {feature.name}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300">{feature.description}</p>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
