import React from 'react';
import { Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';

const LoadingSpinner = ({ message = "Analyzing cinematic patterns..." }) => {
    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="status-container"
        >
            <div className="loader-orbit">
                <Loader2 className="animate-spin-slow" size={64} />
            </div>
            <p>{message}</p>
        </motion.div>
    );
};

export default LoadingSpinner;
