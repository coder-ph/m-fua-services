import React from "react";
import { ArrowRight, Phone, Mail, MapPin } from "lucide-react";

const ContactSection = () => (
  <section id="contact" className="px-4 lg:px-6 py-16 bg-white">
    <div className="max-w-7xl mx-auto">
      <div className="text-center mb-16">
        <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
          Get In Touch
        </h2>
        <p className="text-xl text-gray-600">
          Ready to schedule your cleaning? We're here to help!
        </p>
      </div>
      <div className="grid lg:grid-cols-2 gap-12">
        {/* Contact Form */}
        <div className="bg-gray-50 rounded-2xl p-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-6">
            Request a Free Quote
          </h3>
          <form className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  First Name
                </label>
                <input
                  type="text"
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="John"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Last Name
                </label>
                <input
                  type="text"
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Doe"
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email
              </label>
              <input
                type="email"
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="john@example.com"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Phone
              </label>
              <input
                type="tel"
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="+254740786838"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Service Type
              </label>
              <select className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                <option>Residential Cleaning</option>
                <option>Commercial Cleaning</option>
                <option>Fumigation Services</option>
                <option>Deep Cleaning</option>
                <option>Move-in/Move-out</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Message
              </label>
              <textarea
                rows={4}
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Tell us about your cleaning needs..."
              ></textarea>
            </div>
            <button className="w-full bg-blue-600 text-white py-4 rounded-lg hover:bg-blue-700 transition-colors font-semibold text-lg">
              <ArrowRight className="h-5 w-5 inline mr-2" />
              Get Free Quote
            </button>
          </form>
        </div>
        {/* Contact Info */}
        <div className="space-y-8">
          <div>
            <h3 className="text-2xl font-bold text-gray-900 mb-6">
              Contact Information
            </h3>
            <div className="space-y-6">
              <div className="flex items-start space-x-4">
                <div className="bg-blue-100 p-3 rounded-lg">
                  <Phone className="h-6 w-6 text-blue-600" />
                </div>
                <div>
                  <p className="font-semibold text-gray-900">Phone</p>
                  <p className="text-gray-600">+254740786838</p>
                  <p className="text-sm text-gray-500">
                    Available 24/7 for emergencies
                  </p>
                </div>
              </div>
              <div className="flex items-start space-x-4">
                <div className="bg-green-100 p-3 rounded-lg">
                  <Mail className="h-6 w-6 text-green-600" />
                </div>
                <div>
                  <p className="font-semibold text-gray-900">Email</p>
                  <p className="text-gray-600">
                    info@Milele Cleaning Services.com
                  </p>
                  <p className="text-sm text-gray-500">
                    We'll respond within 2 hours
                  </p>
                </div>
              </div>
              <div className="flex items-start space-x-4">
                <div className="bg-purple-100 p-3 rounded-lg">
                  <MapPin className="h-6 w-6 text-purple-600" />
                </div>
                <div>
                  <p className="font-semibold text-gray-900">Service Area</p>
                  <p className="text-gray-600">Nairobi</p>
                  <p className="text-sm text-gray-500">
                    Free estimates within 25 miles
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div className="bg-blue-50 rounded-2xl p-6">
            <h4 className="font-bold text-gray-900 mb-4">Business Hours</h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Monday - Friday</span>
                <span className="font-medium">8:00 AM - 6:00 PM</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Saturday</span>
                <span className="font-medium">9:00 AM - 4:00 PM</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Sunday</span>
                <span className="font-medium">Emergency Only</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
);

export default ContactSection;
