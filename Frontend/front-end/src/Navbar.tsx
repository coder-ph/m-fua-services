// components/Header/Header.tsx
// Updated: Added Signup button (desktop & mobile)
import { useState, useRef } from "react";
import { Link } from "react-router-dom";
import { Phone, Menu, X, ChevronDown, ChevronUp, } from "lucide-react";
import logo from "../src/assets/logo.svg";

interface HeaderProps {
  isMenuOpen: boolean;
  setIsMenuOpen: (isOpen: boolean) => void;
}

export default function Navbar({ isMenuOpen, setIsMenuOpen }: HeaderProps) {
  const [isServicesHovered, setIsServicesHovered] = useState(false);
  const [isMobileServicesOpen, setIsMobileServicesOpen] = useState(false);
  const hoverTimeout = useRef<ReturnType<typeof setTimeout> | null>(null);

  const cleaningServices = [
    "Recurring Cleaning",
    "One Time Cleaning",
    "Home Cleaning",
    "Move-In Cleaning",
    "Special Event Cleaning",
    "Apartment Cleaning",
    "Move-Out Cleaning",
    "Office Cleaning",
  ];

  const handleMouseEnter = () => {
    if (hoverTimeout.current) clearTimeout(hoverTimeout.current);
    setIsServicesHovered(true);
  };

  const handleMouseLeave = () => {
    hoverTimeout.current = setTimeout(() => {
      setIsServicesHovered(false);
    }, 200); 
  };

  return (
    <header className="fixed top-0 w-full bg-white/95 backdrop-blur-sm border-b border-gray-100 z-50">
      <div className="max-w-7xl mx-auto px-4 lg:px-6 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className=" p-2 rounded-lg">
            <img src={logo} alt="Logo" className="p-5 h-30 w-30" />
          </div>
          <span className="text-xl font-bold text-gray-900">
            Milele Cleaning Services
          </span>
        </div>

        <nav className="hidden md:flex space-x-8">
         
          <div
            className="relative"
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
          >
            <button className="flex items-center text-gray-700 hover:text-blue-600 transition-colors font-medium">
              Services
              {isServicesHovered ? (
                <ChevronUp className="ml-1 h-4 w-4" />
              ) : (
                <ChevronDown className="ml-1 h-4 w-4" />
              )}
            </button>

            {/* Dropdown */}
            <div
              className={`absolute left-0 mt-2 w-96 bg-white rounded-lg shadow-xl border border-gray-200 z-50 p-4 transition-opacity duration-200 ${
                isServicesHovered
                  ? "opacity-100 visible"
                  : "opacity-0 invisible"
              }`}
            >
              <div className="grid grid-cols-2 gap-4">
                {cleaningServices.map((service, index) => (
                  <a
                    key={index}
                    href="#"
                    className="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded transition-colors"
                  >
                    {service}
                  </a>
                ))}
              </div>
            </div>
          </div>

          <a
            href="#about"
            className="text-gray-700 hover:text-blue-600 transition-colors font-medium"
          >
            About
          </a>
          <a
            href="#testimonials"
            className="text-gray-700 hover:text-blue-600 transition-colors font-medium"
          >
            Reviews
          </a>
          <a
            href="#contact"
            className="text-gray-700 hover:text-blue-600 transition-colors font-medium"
          >
            Contact
          </a>
        </nav>

        <div className="flex items-center space-x-4">
          <button className="hidden sm:flex bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium items-center">
            <Phone className="h-4 w-4 mr-2" />
            +254740786838
          </button>
          {/* <Link to="/login" className="hidden md:flex bg-white border border-blue-600 text-blue-600 px-4 py-2 rounded-lg font-medium hover:bg-blue-50 transition-colors" style={{marginLeft: 8}}>
            Login
          </Link>
          <Link to="/signup" className="hidden md:flex bg-blue-500 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-600 transition-colors" style={{marginLeft: 8}}>
            Sign Up
          </Link> */}
          <button
            className="md:hidden p-2"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? (
              <X className="h-6 w-6" />
            ) : (
              <Menu className="h-6 w-6" />
            )}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden bg-white border-t border-gray-100">
          <nav className="px-4 py-4 space-y-4">
            <div className="space-y-2">
              <Link
                to="/signup"
                className="block w-full bg-blue-500 text-white px-4 py-2 rounded-lg font-medium text-center hover:bg-blue-600 transition-colors mb-2"
              >
                Sign Up
              </Link>
              <button
                className="w-full flex justify-between items-center text-gray-700 hover:text-blue-600 transition-colors font-medium"
                onClick={() => setIsMobileServicesOpen((open) => !open)}
                aria-expanded={isMobileServicesOpen}
                aria-controls="mobile-services-list"
              >
                Services
                {isMobileServicesOpen ? (
                  <ChevronUp className="h-4 w-4" />
                ) : (
                  <ChevronDown className="h-4 w-4" />
                )}
              </button>
              {isMobileServicesOpen && (
                <div id="mobile-services-list" className="grid grid-cols-2 gap-2 pl-4">
                  {cleaningServices.map((service, index) => (
                    <a
                      key={index}
                      href="#"
                      className="block text-sm py-2 text-gray-700 hover:text-blue-600"
                    >
                      {service}
                    </a>
                  ))}
                </div>
              )}
            </div>
            <a
              href="#about"
              className="block text-gray-700 hover:text-blue-600 transition-colors font-medium"
            >
              About
            </a>
            <a
              href="#testimonials"
              className="block text-gray-700 hover:text-blue-600 transition-colors font-medium"
            >
              Reviews
            </a>
            <a
              href="#contact"
              className="block text-gray-700 hover:text-blue-600 transition-colors font-medium"
            >
              Contact
            </a>
            <button className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium flex items-center justify-center">
              <Phone className="h-4 w-4 mr-2" />
              +254740786838
            </button>
            <Link to="/login" className="w-full mt-2 bg-white border border-blue-600 text-blue-600 px-4 py-2 rounded-lg font-medium hover:bg-blue-50 transition-colors block text-center">
              Login
            </Link>
          </nav>
        </div>
      )}
    </header>
  );
}
