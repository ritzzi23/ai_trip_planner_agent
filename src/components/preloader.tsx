// from lovable --> need to modify for python streamlit


import { useState, useEffect } from "react";
import { Plane, MapPin, Calendar, Users } from "lucide-react";

interface TravelPreloaderProps {
  onComplete: () => void;
}

export const TravelPreloader = ({ onComplete }: TravelPreloaderProps) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [isVisible, setIsVisible] = useState(true);

  const steps = [
    { icon: Plane, text: "Discovering destinations", color: "text-primary" },
    { icon: MapPin, text: "Finding perfect locations", color: "text-secondary" },
    { icon: Calendar, text: "Planning your journey", color: "text-accent" },
    { icon: Users, text: "Creating memories", color: "text-primary" }
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev < steps.length - 1) {
          return prev + 1;
        } else {
          // Start fade out after showing all steps
          setTimeout(() => {
            setIsVisible(false);
            setTimeout(onComplete, 500);
          }, 800);
          clearInterval(interval);
          return prev;
        }
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [onComplete, steps.length]);

  if (!isVisible) {
    return (
      <div className="fixed inset-0 bg-gradient-hero flex items-center justify-center opacity-0 transition-opacity duration-500 pointer-events-none">
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-gradient-hero flex items-center justify-center z-50 transition-opacity duration-500">
      <div className="text-center space-y-8 animate-fade-in">
        {/* Logo Animation */}
        <div className="relative">
          <h1 className="text-6xl md:text-7xl font-bold text-white mb-4 tracking-tight">
            TravelPlan
          </h1>
          <div className="absolute -top-2 -right-2 w-4 h-4 bg-secondary rounded-full animate-pulse"></div>
        </div>

        {/* Animated Icons Circle */}
        <div className="relative w-32 h-32 mx-auto">
          <div className="absolute inset-0 rounded-full border-2 border-white/20 animate-spin"></div>
          {steps.map((step, index) => {
            const Icon = step.icon;
            const angle = (index * 90) - 90; // Start from top
            const x = Math.cos((angle * Math.PI) / 180) * 40;
            const y = Math.sin((angle * Math.PI) / 180) * 40;
            
            return (
              <div
                key={index}
                className={`absolute w-12 h-12 rounded-full bg-white/10 backdrop-blur-sm flex items-center justify-center transition-all duration-500 ${
                  index <= currentStep ? 'scale-110 bg-white/20 shadow-glow' : 'scale-100'
                }`}
                style={{
                  left: '50%',
                  top: '50%',
                  transform: `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`
                }}
              >
                <Icon 
                  className={`w-6 h-6 transition-colors duration-500 ${
                    index <= currentStep ? step.color : 'text-white/60'
                  }`} 
                />
              </div>
            );
          })}
        </div>

        {/* Current Step Text */}
        <div className="h-16 flex items-center justify-center">
          <p className="text-xl text-white/90 font-medium animate-fade-in">
            {steps[currentStep]?.text}
          </p>
        </div>

        {/* Progress Dots */}
        <div className="flex space-x-2 justify-center">
          {steps.map((_, index) => (
            <div
              key={index}
              className={`w-2 h-2 rounded-full transition-all duration-300 ${
                index <= currentStep ? 'bg-white scale-125' : 'bg-white/30'
              }`}
            />
          ))}
        </div>

        {/* Tagline */}
        <p className="text-white/70 text-lg max-w-md mx-auto leading-relaxed">
          Your AI-powered travel companion is preparing the perfect planning experience
        </p>
      </div>
    </div>
  );
};
