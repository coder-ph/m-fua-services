import { useState, useEffect } from 'react';
import HeroSection from "../components/HeroSection";
import QuickStats from "../components/QuickStats";
import ServicesSection from "../components/ServicesSection";
import AboutSection from "../components/AboutSection";
import TestimonialsSection from "../components/TestimonialsSection";
import CTASection from "../components/CTASection";
import ContactSection from "../components/ContactSection";
import Footer from "../components/Footer";
import WhatsAppFloatingButton from "../components/WhatsAppFloatingButton";
import ChatbotFloatingButton from "../components/ChatbotFloatingButton";
import Navbar from "../Navbar";

export default function HomePage() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  // Scroll to top when the page mounts
  useEffect(() => {
    window.scrollTo(0, 0);
    if (window.location.hash) {
      history.replaceState(null, '', window.location.pathname);
    }
  }, []);

  return (
    <div className="min-h-screen bg-white">
      <Navbar isMenuOpen={isMenuOpen} setIsMenuOpen={setIsMenuOpen} />
      <HeroSection />
      <QuickStats />
      <ServicesSection />
      <AboutSection />
      <TestimonialsSection />
      <CTASection />
      <ContactSection />
      <Footer />
      <WhatsAppFloatingButton />
      <ChatbotFloatingButton />
    </div>
  );
}
