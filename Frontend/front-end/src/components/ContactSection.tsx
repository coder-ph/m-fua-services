import React from "react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { ArrowRight, Phone, Mail, MapPin } from "lucide-react";

const ContactSection = () => {
  const [status, setStatus] = React.useState<null | "success" | "error">(null);
  const [loading, setLoading] = React.useState(false);

  const formik = useFormik({
    initialValues: {
      firstName: "",
      lastName: "",
      email: "",
      phone: "",
      serviceType: "Residential Cleaning",
      message: "",
    },
    validationSchema: Yup.object({
      firstName: Yup.string().required("First Name is required"),
      lastName: Yup.string().required("Last Name is required"),
      email: Yup.string().email("Invalid email address").required("Email is required"),
      phone: Yup.string().required("Phone is required"),
      serviceType: Yup.string().required("Service Type is required"),
      message: Yup.string().required("Message is required"),
    }),
    onSubmit: async (values, { resetForm }) => {
      setLoading(true);
      setStatus(null);
      try {
        const res = await fetch("/api/send-quote", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(values),
        });
        if (res.ok) {
          setStatus("success");
          resetForm();
        } else {
          setStatus("error");
        }
      } catch {
        setStatus("error");
      } finally {
        setLoading(false);
      }
    },
  });

  return (
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
            <form className="space-y-6" onSubmit={formik.handleSubmit} noValidate>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    First Name
                  </label>
                  <input
                    type="text"
                    name="firstName"
                    value={formik.values.firstName}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    className={`w-full px-4 py-3 rounded-lg border ${formik.touched.firstName && formik.errors.firstName ? 'border-red-500' : 'border-gray-300'} focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
                    placeholder="John"
                  />
                  {formik.touched.firstName && formik.errors.firstName && (
                    <div className="text-red-500 text-xs mt-1">{formik.errors.firstName}</div>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Last Name
                  </label>
                  <input
                    type="text"
                    name="lastName"
                    value={formik.values.lastName}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    className={`w-full px-4 py-3 rounded-lg border ${formik.touched.lastName && formik.errors.lastName ? 'border-red-500' : 'border-gray-300'} focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
                    placeholder="Doe"
                  />
                  {formik.touched.lastName && formik.errors.lastName && (
                    <div className="text-red-500 text-xs mt-1">{formik.errors.lastName}</div>
                  )}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email
                </label>
                <input
                  type="email"
                  name="email"
                  value={formik.values.email}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                  className={`w-full px-4 py-3 rounded-lg border ${formik.touched.email && formik.errors.email ? 'border-red-500' : 'border-gray-300'} focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
                  placeholder="john@example.com"
                />
                {formik.touched.email && formik.errors.email && (
                  <div className="text-red-500 text-xs mt-1">{formik.errors.email}</div>
                )}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Phone
                </label>
                <input
                  type="tel"
                  name="phone"
                  value={formik.values.phone}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                  className={`w-full px-4 py-3 rounded-lg border ${formik.touched.phone && formik.errors.phone ? 'border-red-500' : 'border-gray-300'} focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
                  placeholder="+254740786838"
                />
                {formik.touched.phone && formik.errors.phone && (
                  <div className="text-red-500 text-xs mt-1">{formik.errors.phone}</div>
                )}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Service Type
                </label>
                <select
                  name="serviceType"
                  value={formik.values.serviceType}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                  className={`w-full px-4 py-3 rounded-lg border ${formik.touched.serviceType && formik.errors.serviceType ? 'border-red-500' : 'border-gray-300'} focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
                >
                  <option>Residential Cleaning</option>
                  <option>Commercial Cleaning</option>
                  <option>Fumigation Services</option>
                  <option>Deep Cleaning</option>
                  <option>Move-in/Move-out</option>
                </select>
                {formik.touched.serviceType && formik.errors.serviceType && (
                  <div className="text-red-500 text-xs mt-1">{formik.errors.serviceType}</div>
                )}
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Message
                </label>
                <textarea
                  name="message"
                  rows={4}
                  value={formik.values.message}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                  className={`w-full px-4 py-3 rounded-lg border ${formik.touched.message && formik.errors.message ? 'border-red-500' : 'border-gray-300'} focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
                  placeholder="Tell us about your cleaning needs..."
                ></textarea>
                {formik.touched.message && formik.errors.message && (
                  <div className="text-red-500 text-xs mt-1">{formik.errors.message}</div>
                )}
              </div>
              <button
                type="submit"
                className="w-full bg-blue-600 text-white py-4 rounded-lg hover:bg-blue-700 transition-colors font-semibold text-lg"
                disabled={loading || !formik.isValid || !formik.dirty}
              >
                <ArrowRight className="h-5 w-5 inline mr-2" />
                {loading ? "Sending..." : "Get Free Quote"}
              </button>
              {status === "success" && (
                <div className="text-green-600 text-center mt-4 font-semibold">Thank you! We received your request.</div>
              )}
              {status === "error" && (
                <div className="text-red-600 text-center mt-4 font-semibold">Sorry, something went wrong. Please try again.</div>
              )}
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
};

export default ContactSection;
