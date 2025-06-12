
import { Home, Building, Zap, CheckCircle } from "lucide-react";

const ServicesSection = () => (
  <section id="services" className="px-4 lg:px-6 py-16 bg-gray-50">
    <div className="max-w-7xl mx-auto">
      <div className="text-center mb-16">
        <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
          Our Cleaning Services
        </h2>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          From regular maintenance to deep cleaning, we offer comprehensive
          solutions for every space
        </p>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-4 gap-8">
        {/* Residential Cleaning */}
        <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow duration-300">
          <div className="bg-blue-100 p-4 rounded-2xl w-fit mb-6">
            <Home className="h-8 w-8 text-blue-600" />
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-4">
            Residential Cleaning
          </h3>
          <p className="text-gray-600 mb-6">
            Complete home cleaning services including kitchens, bathrooms,
            bedrooms, and living areas.
          </p>
          <ul className="space-y-2 mb-6">
            <li className="flex items-center text-sm text-gray-600">
              <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
              Weekly, bi-weekly, or monthly service
            </li>
            <li className="flex items-center text-sm text-gray-600">
              <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
              Eco-friendly cleaning products
            </li>
            <li className="flex items-center text-sm text-gray-600">
              <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
              Customizable cleaning checklist
            </li>
          </ul>
          <button className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium">
            Starting at Ksh.##
          </button>
        </div>

        {/* Fumigation services */}
        <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow duration-300">
          <div className="bg-blue-100 p-4 rounded-2xl w-fit mb-6">
            <Home className="h-8 w-8 text-blue-600" />
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-4">
            Fumigation Services
          </h3>
          <p className="text-gray-600 mb-6">
            Thoroughfumigation services including kitchens, bedrooms, and living
            areas.
          </p>
          <ul className="space-y-2 mb-6">
            <li className="flex items-center text-sm text-gray-600">
              <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
              Weekly, bi-weekly, or monthly service
            </li>
            <li className="flex items-center text-sm text-gray-600">
              <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
              Eco-friendly fumigation products
            </li>
            <li className="flex items-center text-sm text-gray-600">
              <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
              Budget-friendly
            </li>
            <li className="flex items-center text-sm text-gray-600">
              <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
              Customizable cleaning checklist
            </li>
          </ul>
          <button className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium">
            Starting at Ksh.##
          </button>
        </div>
        {/* Commercial Cleaning */}
        <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow duration-300">
          <div className="bg-green-100 p-4 rounded-2xl w-fit mb-6">
            <Building className="h-8 w-8 text-green-600" />
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-4">
            Commercial Cleaning
          </h3>
          <p className="text-gray-600 mb-6">
            Professional office and commercial space cleaning to maintain a
            productive work environment.
          </p>
          <ul className="space-y-2 mb-6">
            <li className="flex items-center text-sm text-gray-600">
              <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
              Daily, weekly, or monthly schedules
            </li>
            <li className="flex items-center text-sm text-gray-600">
              <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
              After-hours cleaning available
            </li>
            <li className="flex items-center text-sm text-gray-600">
              <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
              Sanitization and disinfection
            </li>
          </ul>
          <button className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 transition-colors font-medium">
            Get Quote
          </button>
        </div>
        {/* Deep Cleaning */}
        <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow duration-300">
          <div className="bg-purple-100 p-4 rounded-2xl w-fit mb-6">
            <Zap className="h-8 w-8 text-purple-600" />
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-4">
            Deep Cleaning
          </h3>
          <p className="text-gray-600 mb-6">
            Intensive cleaning service that reaches every corner and surface for
            a thorough refresh.
          </p>
          <ul className="space-y-2 mb-6">
            <li className="flex items-center text-sm text-gray-600">
              <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
              Inside appliances and cabinets
            </li>
            <li className="flex items-center text-sm text-gray-600">
              <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
              Pocket-friendly 
            </li>
            <li className="flex items-center text-sm text-gray-600">
              <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
              Baseboards and window sills
            </li>
            <li className="flex items-center text-sm text-gray-600">
              <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
              Light fixtures and ceiling fans
            </li>
          </ul>
          <button className="w-full bg-purple-600 text-white py-3 rounded-lg hover:bg-purple-700 transition-colors font-medium">
            Starting at Ksh.##
          </button>
        </div>
      </div>
    </div>
  </section>
);

export default ServicesSection;
