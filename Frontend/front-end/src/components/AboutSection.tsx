import { Users, Shield, Sparkles } from "lucide-react";

const AboutSection = () => (
  <section id="about" className="px-4 lg:px-6 py-16 bg-white">
    <div className="max-w-7xl mx-auto">
      <div className="grid lg:grid-cols-2 gap-12 items-center">
        <div>
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-6">Why Choose Milele Cleaning Services?</h2>
          <p className="text-lg text-gray-600 mb-8">With over 5 years of experience and 10,000+ satisfied customers, we've built our reputation on reliability, quality, and exceptional customer service.</p>
          <div className="space-y-6">
            <div className="flex items-start space-x-4">
              <div className="bg-blue-100 p-2 rounded-lg flex-shrink-0"><Users className="h-6 w-6 text-blue-600" /></div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Trained Professionals</h3>
                <p className="text-gray-600">Our team is thoroughly vetted, trained, and insured for your peace of mind.</p>
              </div>
            </div>
            <div className="flex items-start space-x-4">
              <div className="bg-green-100 p-2 rounded-lg flex-shrink-0"><Shield className="h-6 w-6 text-green-600" /></div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Fully Insured & Bonded</h3>
                <p className="text-gray-600">Complete protection for your property and belongings during every cleaning.</p>
              </div>
            </div>
            <div className="flex items-start space-x-4">
              <div className="bg-yellow-100 p-2 rounded-lg flex-shrink-0"><Sparkles className="h-6 w-6 text-yellow-600" /></div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Eco-Friendly Products</h3>
                <p className="text-gray-600">Safe, non-toxic cleaning solutions that protect your family and the environment.</p>
              </div>
            </div>
          </div>
        </div>
        <div className="relative">
          <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-3xl p-8 shadow-xl">
            <div className="grid grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-2xl shadow-lg text-center">
                <div className="text-3xl font-bold text-blue-600 mb-2">5+</div>
                <div className="text-sm text-gray-600">Years Experience</div>
              </div>
              <div className="bg-white p-6 rounded-2xl shadow-lg text-center">
                <div className="text-3xl font-bold text-green-600 mb-2">10K+</div>
                <div className="text-sm text-gray-600">Happy Clients</div>
              </div>
              <div className="bg-white p-6 rounded-2xl shadow-lg text-center">
                <div className="text-3xl font-bold text-purple-600 mb-2">4.9</div>
                <div className="text-sm text-gray-600">Star Rating</div>
              </div>
              <div className="bg-white p-6 rounded-2xl shadow-lg text-center">
                <div className="text-3xl font-bold text-yellow-600 mb-2">24/7</div>
                <div className="text-sm text-gray-600">Support</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
);

export default AboutSection;
