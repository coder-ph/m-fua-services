import { Sparkles, Facebook, Twitter, Instagram, Phone, Mail, MapPin } from "lucide-react";

const Footer = () => (
  <footer className="bg-gray-900 text-white px-4 lg:px-6 py-12">
    <div className="max-w-7xl mx-auto">
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-8">
        <div>
          <div className="flex items-center space-x-2 mb-4">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Sparkles className="h-6 w-6 text-white" />
            </div>
            <span className="text-xl font-bold">Milele Cleaning Services</span>
          </div>
          <p className="text-gray-400 mb-4">Professional cleaning services that make your space sparkle. Trusted by thousands of customers.</p>
          <div className="flex space-x-4">
            <Facebook className="h-6 w-6 text-gray-400 hover:text-white cursor-pointer transition-colors" />
            <Twitter className="h-6 w-6 text-gray-400 hover:text-white cursor-pointer transition-colors" />
            <Instagram className="h-6 w-6 text-gray-400 hover:text-white cursor-pointer transition-colors" />
          </div>
        </div>
        <div>
          <h4 className="font-bold mb-4">Services</h4>
          <ul className="space-y-2 text-gray-400">
            <li><a href="#" className="hover:text-white transition-colors">Residential Cleaning</a></li>
            <li><a href="#" className="hover:text-white transition-colors">Commercial Cleaning</a></li>
            <li><a href="#" className="hover:text-white transition-colors">Deep Cleaning</a></li>
            <li><a href="#" className="hover:text-white transition-colors">Move-in/Move-out</a></li>
          </ul>
        </div>
        <div>
          <h4 className="font-bold mb-4">Company</h4>
          <ul className="space-y-2 text-gray-400">
            <li><a href="#" className="hover:text-white transition-colors">About Us</a></li>
            <li><a href="#" className="hover:text-white transition-colors">Our Team</a></li>
            <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
            <li><a href="#" className="hover:text-white transition-colors">Reviews</a></li>
          </ul>
        </div>
        <div>
          <h4 className="font-bold mb-4">Contact</h4>
          <ul className="space-y-2 text-gray-400">
            <li className="flex items-center"><Phone className="h-4 w-4 mr-2" />+254740786838</li>
            <li className="flex items-center"><Mail className="h-4 w-4 mr-2" />info@Milele Cleaning Services.com</li>
            <li className="flex items-center"><MapPin className="h-4 w-4 mr-2" />Greater Metro Area</li>
          </ul>
        </div>
      </div>
      <div className="border-t border-gray-800 pt-8 text-center text-gray-400">
        <p>&copy; 2024 Milele Cleaning Services. All rights reserved. | Privacy Policy | Terms of Service</p>
      </div>
    </div>
  </footer>
);

export default Footer;
