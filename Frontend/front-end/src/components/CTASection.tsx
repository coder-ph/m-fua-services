import { useState } from "react";
import { Calendar, Phone } from "lucide-react";
import BookNowModal from "./BookNowModal";

const CTASection = () => {
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <section className="px-4 lg:px-6 py-16 bg-blue-600  ">
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="text-3xl lg:text-4xl font-bold text-white mb-6">Ready for a Sparkling Clean Space?</h2>
        <p className="text-xl text-blue-100 mb-8">Book your cleaning service today and experience the Milele Cleaning Services difference</p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            className="bg-white text-blue-600 px-8 py-4 rounded-xl font-semibold text-lg hover:bg-gray-100 transform hover:scale-105 transition-all duration-200 shadow-lg"
            onClick={() => setModalOpen(true)}
          >
            <Calendar className="h-5 w-5 inline mr-2" />
            Book Now - 20% Off First Clean
          </button>
          <button className="border-2 border-white text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-white hover:text-blue-600 transition-all duration-200">
            <Phone className="h-5 w-5 inline mr-2" />
            Call +254740786838
          </button>
        </div>
      </div>
      <BookNowModal open={modalOpen} onClose={() => setModalOpen(false)} />
    </section>
  );
};

export default CTASection;
