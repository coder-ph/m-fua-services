import { Star, Calendar, Shield, Clock, CheckCircle } from "lucide-react";

const HeroSection = () => (
  <main className="pt-16 px-4 lg:px-6 py-12 lg:py-20 bg-gradient-to-br from-blue-50 via-white to-cyan-50">
    <div className="max-w-7xl mx-auto">
      <div className="grid lg:grid-cols-2 gap-12 items-center">
        {/* Left Column - Content */}
        <div className="space-y-8">
          <div className="space-y-4">
            <div className="inline-flex items-center bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
              <Star className="h-4 w-4 mr-1 fill-current" />
              5-Star Rated Service
            </div>
            <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 leading-tight font-sans md:font-serif">
              Your Home
              <span className="block text-blue-600">Sparkling Clean</span>
              <span className="block">Every Time</span>
            </h1>
            <p className="text-xl text-black-600 leading-relaxed">
              Professional cleaning services that transform your space into a pristine sanctuary. Trusted by 10,000+ satisfied customers across the city.
            </p>
          </div>
          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4">
            <button className="bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-blue-700 transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl">
              <Calendar className="h-5 w-5 inline mr-2" />
              Book Now - 20% Off
            </button>
            <button className="border-2 border-gray-300 text-gray-700 px-8 py-4 rounded-xl font-semibold text-lg hover:border-blue-600 hover:text-blue-600 transition-all duration-200">
              Get Free Quote
            </button>
          </div>
          {/* Trust Indicators */}
          <div className="grid grid-cols-3 gap-6 pt-8 border-t border-gray-200">
            <div className="text-center">
              <div className="bg-green-100 p-3 rounded-full w-fit mx-auto mb-2">
                <Shield className="h-6 w-6 text-green-600" />
              </div>
              <p className="text-sm font-medium text-gray-900">Fully Insured</p>
            </div>
            <div className="text-center">
              <div className="bg-blue-100 p-3 rounded-full w-fit mx-auto mb-2">
                <Clock className="h-6 w-6 text-blue-600" />
              </div>
              <p className="text-sm font-medium text-gray-900">Same Day Service</p>
            </div>
            <div className="text-center">
              <div className="bg-yellow-100 p-3 rounded-full w-fit mx-auto mb-2">
                <CheckCircle className="h-6 w-6 text-yellow-600" />
              </div>
              <p className="text-sm font-medium text-gray-900">100% Guarantee</p>
            </div>
          </div>
        </div>
        {/* Right Column - Visual Elements */}
        <div className="relative">
          <div className="relative bg-gradient-to-br rounded-3xl shadow-2xl">
            <img src="https://i.pinimg.com/736x/b6/b3/27/b6b327069abe320eed84ba7c3b721970.jpg" />
            <div className="absolute -bottom-4 -right-4 bg-green-500 text-white p-4 rounded-2xl shadow-lg">
              <div className="text-center">
                <p className="text-2xl font-bold">2min</p>
                <p className="text-sm opacity-90">Response Time</p>
              </div>
            </div>
          </div>
          {/* Background decorative elements */}
          <div className="absolute -z-10 top-10 right-10 w-20 h-20 bg-blue-200 rounded-full opacity-50"></div>
          <div className="absolute -z-10 bottom-10 left-10 w-16 h-16 bg-cyan-200 rounded-full opacity-50"></div>
          <div className="absolute -z-10 top-1/2 left-0 w-12 h-12 bg-yellow-200 rounded-full opacity-50"></div>
        </div>
      </div>
    </div>
  </main>
);

export default HeroSection;
