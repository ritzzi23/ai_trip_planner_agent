// from lovable --> need to modify for python streamlit

import { useState } from "react";
import { TravelPlanningForm } from "@/components/TravelPlanningForm";
import { ItineraryResults } from "@/components/ItineraryResults";
import { TravelPreloader } from "@/components/TravelPreloader";
import { generateMockItinerary } from "@/utils/mockData";
import heroImage from "@/assets/hero-travel.jpg";

interface TravelFormData {
  destination: string;
  startDate: string;
  endDate: string;
  budget: string;
  travelers: string;
  interests: string[];
}

const Index = () => {
  const [showPreloader, setShowPreloader] = useState(true);
  const [itineraryData, setItineraryData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handlePreloaderComplete = () => {
    setShowPreloader(false);
  };

  const handleFormSubmit = async (formData: TravelFormData) => {
    setIsLoading(true);
    
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const mockData = generateMockItinerary(
      formData.destination,
      formData.startDate,
      formData.endDate,
      formData.budget,
      formData.interests
    );
    
    setItineraryData(mockData);
    setIsLoading(false);
  };

  const handleEditTrip = () => {
    setItineraryData(null);
  };

  if (showPreloader) {
    return <TravelPreloader onComplete={handlePreloaderComplete} />;
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-sky">
        <div className="text-center space-y-4">
          <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto"></div>
          <h2 className="text-2xl font-bold text-primary">Creating Your Perfect Itinerary</h2>
          <p className="text-muted-foreground">This won't take long...</p>
        </div>
      </div>
    );
  }

  if (itineraryData) {
    return (
      <div className="min-h-screen bg-gradient-sky py-8 px-4">
        <ItineraryResults data={itineraryData} onEditTrip={handleEditTrip} />
      </div>
    );
  }

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Hero Background */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: `url(${heroImage})` }}
      >
        <div className="absolute inset-0 bg-gradient-hero/70 backdrop-blur-[1px]" />
      </div>
      
      {/* Content */}
      <div className="relative z-10 min-h-screen flex flex-col">
        {/* Header */}
        <header className="py-8 px-4 text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-4 tracking-tight">
            TravelPlan
          </h1>
          <p className="text-xl md:text-2xl text-white/90 max-w-2xl mx-auto">
            Your AI-powered travel companion for unforgettable journeys
          </p>
        </header>

        {/* Main Content */}
        <main className="flex-1 flex items-center justify-center px-4 py-8">
          <TravelPlanningForm onSubmit={handleFormSubmit} />
        </main>

        {/* Footer */}
        <footer className="py-8 text-center">
          <p className="text-white/70">
            Discover amazing destinations • Plan perfect itineraries • Create lasting memories
          </p>
        </footer>
      </div>
    </div>
  );
};

export default Index;
