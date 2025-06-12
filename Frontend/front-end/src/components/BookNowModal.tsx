import React from "react";
import { useFormik } from "formik";
import * as Yup from "yup";

interface BookNowModalProps {
  open: boolean;
  onClose: () => void;
}

const serviceOptions = [
  "Residential Cleaning",
  "Commercial Cleaning",
  "Fumigation Services",
  "Deep Cleaning",
  "Move-in/Move-out",
];

const BookNowModal: React.FC<BookNowModalProps> = ({ open, onClose }) => {
  const [submitted, setSubmitted] = React.useState(false);

  const formik = useFormik({
    initialValues: {
      serviceType: "Residential Cleaning",
      location: "",
      date: "",
      time: "",
      email: "",
      phone: "",
      notes: "",
    },
    validationSchema: Yup.object({
      serviceType: Yup.string().required("Service type is required"),
      location: Yup.string().required("Location is required"),
      date: Yup.string().required("Date is required"),
      time: Yup.string().required("Time is required"),
      email: Yup.string().email("Invalid email").required("Email is required"),
      phone: Yup.string().required("Phone is required"),
    }),
    onSubmit: async (_values, { resetForm }) => {
      setSubmitted(true);
      resetForm();
      setTimeout(onClose, 2000); // Auto-close after 2s
    },
  });

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-white bg-opacity-80">
      <div className="bg-white rounded-2xl shadow-xl max-w-md w-full p-8 relative">
        <button
          className="absolute top-3 right-3 text-gray-400 hover:text-gray-700 text-2xl"
          onClick={onClose}
        >
          &times;
        </button>
        <h2 className="text-2xl font-bold mb-4 text-blue-700">Book Your Service</h2>
        {submitted ? (
          <div className="text-green-600 text-center font-semibold text-lg py-8">
            Thank you! You should receive a call from us soon.
          </div>
        ) : (
          <form onSubmit={formik.handleSubmit} className="space-y-5">
            <div>
              <label className="block mb-1 font-medium">Type of Service</label>
              <select
                name="serviceType"
                value={formik.values.serviceType}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                className={`w-full px-4 py-2 rounded-lg border ${formik.touched.serviceType && formik.errors.serviceType ? 'border-red-500' : 'border-gray-300'} focus:ring-2 focus:ring-blue-500`}
              >
                {serviceOptions.map(opt => (
                  <option key={opt} value={opt}>{opt}</option>
                ))}
              </select>
              {formik.touched.serviceType && formik.errors.serviceType && (
                <div className="text-red-500 text-xs mt-1">{formik.errors.serviceType}</div>
              )}
            </div>
            <div>
              <label className="block mb-1 font-medium">Location</label>
              <input
                type="text"
                name="location"
                value={formik.values.location}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                className={`w-full px-4 py-2 rounded-lg border ${formik.touched.location && formik.errors.location ? 'border-red-500' : 'border-gray-300'} focus:ring-2 focus:ring-blue-500`}
                placeholder="e.g. Nairobi, Westlands"
              />
              {formik.touched.location && formik.errors.location && (
                <div className="text-red-500 text-xs mt-1">{formik.errors.location}</div>
              )}
            </div>
            <div className="flex gap-3">
              <div className="flex-1">
                <label className="block mb-1 font-medium">Date</label>
                <input
                  type="date"
                  name="date"
                  value={formik.values.date}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                  className={`w-full px-4 py-2 rounded-lg border ${formik.touched.date && formik.errors.date ? 'border-red-500' : 'border-gray-300'} focus:ring-2 focus:ring-blue-500`}
                />
                {formik.touched.date && formik.errors.date && (
                  <div className="text-red-500 text-xs mt-1">{formik.errors.date}</div>
                )}
              </div>
              <div className="flex-1">
                <label className="block mb-1 font-medium">Time</label>
                <input
                  type="time"
                  name="time"
                  value={formik.values.time}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                  className={`w-full px-4 py-2 rounded-lg border ${formik.touched.time && formik.errors.time ? 'border-red-500' : 'border-gray-300'} focus:ring-2 focus:ring-blue-500`}
                />
                {formik.touched.time && formik.errors.time && (
                  <div className="text-red-500 text-xs mt-1">{formik.errors.time}</div>
                )}
              </div>
            </div>
            <div>
              <label className="block mb-1 font-medium">Email</label>
              <input
                type="email"
                name="email"
                value={formik.values.email}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                className={`w-full px-4 py-2 rounded-lg border ${formik.touched.email && formik.errors.email ? 'border-red-500' : 'border-gray-300'} focus:ring-2 focus:ring-blue-500`}
                placeholder="you@email.com"
              />
              {formik.touched.email && formik.errors.email && (
                <div className="text-red-500 text-xs mt-1">{formik.errors.email}</div>
              )}
            </div>
            <div>
              <label className="block mb-1 font-medium">Phone</label>
              <input
                type="tel"
                name="phone"
                value={formik.values.phone}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                className={`w-full px-4 py-2 rounded-lg border ${formik.touched.phone && formik.errors.phone ? 'border-red-500' : 'border-gray-300'} focus:ring-2 focus:ring-blue-500`}
                placeholder="e.g. +254700000000"
              />
              {formik.touched.phone && formik.errors.phone && (
                <div className="text-red-500 text-xs mt-1">{formik.errors.phone}</div>
              )}
            </div>
            <div>
              <label className="block mb-1 font-medium">Additional Notes</label>
              <textarea
                name="notes"
                rows={3}
                value={formik.values.notes}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500"
                placeholder="Any special requests?"
              ></textarea>
            </div>
            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold text-lg hover:bg-blue-700 transition-colors"
              disabled={!formik.isValid || !formik.dirty}
            >
              Send
            </button>
          </form>
        )}
      </div>
    </div>
  );
};

export default BookNowModal;
