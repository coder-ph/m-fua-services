import { useEffect, useRef, useState } from "react";
import { Star, Quote, Users, Building, Home, ChevronLeft, ChevronRight } from "lucide-react";

const testimonials = [
  {
    id: 1,
    rating: 5,
    text: "Milele Cleaning Services transformed our home! Their attention to detail is incredible, and the team is always professional and friendly.",
    name: "Phelix M.",
    role: "Homeowner",
    icon: Users,
    bgColor: "bg-blue-100",
    iconColor: "text-blue-600",
  },
  {
    id: 2,
    rating: 5,
    text: "Reliable, thorough, and affordable. We've been using Milele Cleaning Services for our office for 2 years now. Highly recommended!",
    name: "Victor O.",
    role: "Business Owner",
    icon: Building,
    bgColor: "bg-green-100",
    iconColor: "text-green-600",
  },
  {
    id: 3,
    rating: 5,
    text: "The deep cleaning service was amazing! They cleaned areas I didn't even know needed attention. Worth every penny.",
    name: "Emily R.",
    role: "Apartment Resident",
    icon: Home,
    bgColor: "bg-purple-100",
    iconColor: "text-purple-600",
  },
  {
    id: 4,
    rating: 5,
    text: "Prompt, efficient, and left our office spotless. The team is courteous and always on time.",
    name: "Sarah K.",
    role: "Office Manager",
    icon: Building,
    bgColor: "bg-pink-100",
    iconColor: "text-pink-600",
  },
  {
    id: 5,
    rating: 5,
    text: "My allergies have improved so much since we started using Milele! Highly recommend their deep cleaning service.",
    name: "John D.",
    role: "Homeowner",
    icon: Users,
    bgColor: "bg-yellow-100",
    iconColor: "text-yellow-600",
  },
  {
    id: 6,
    rating: 5,
    text: "Professional and friendly staff. They go above and beyond every time.",
    name: "Faith L.",
    role: "Business Owner",
    icon: Building,
    bgColor: "bg-indigo-100",
    iconColor: "text-indigo-600",
  },
  {
    id: 7,
    rating: 5,
    text: "Their flexible scheduling is perfect for my busy family. Always a great job!",
    name: "Lucy W.",
    role: "Homeowner",
    icon: Home,
    bgColor: "bg-green-50",
    iconColor: "text-green-500",
  },
  {
    id: 8,
    rating: 5,
    text: "Consistently excellent service. Our workspace has never looked better.",
    name: "Daniel T.",
    role: "Office Admin",
    icon: Building,
    bgColor: "bg-blue-50",
    iconColor: "text-blue-500",
  },
];

const CARDS_PER_VIEW = {
  base: 1,
  md: 2,
  lg: 4,
};

const getCardsPerView = () => {
  if (typeof window === "undefined") return CARDS_PER_VIEW.base;
  if (window.innerWidth >= 1024) return CARDS_PER_VIEW.lg;
  if (window.innerWidth >= 768) return CARDS_PER_VIEW.md;
  return CARDS_PER_VIEW.base;
};

const TestimonialsSection = () => {
  const [current, setCurrent] = useState(0);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const [cardsPerView, setCardsPerView] = useState(getCardsPerView());
  const trackRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleResize = () => setCardsPerView(getCardsPerView());
    handleResize(); // Ensure correct cardsPerView on mount
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);


  const total = testimonials.length;
  // Clamp current index between 0 and total - cardsPerView
  const maxIndex = Math.max(0, total - cardsPerView);
  

  // Seamless infinite loop logic
  useEffect(() => {
    if (!trackRef.current) return;
    const handleTransitionEnd = () => {
      if (current >= total) {
        trackRef.current!.style.transition = "none";
        setCurrent(0);
        setTimeout(() => {
          if (trackRef.current) trackRef.current.style.transition = "transform 0.7s cubic-bezier(0.4,0,0.2,1)";
        }, 20);
      } else if (current < 0) {
        trackRef.current!.style.transition = "none";
        setCurrent(total - 1);
        setTimeout(() => {
          if (trackRef.current) trackRef.current.style.transition = "transform 0.7s cubic-bezier(0.4,0,0.2,1)";
        }, 20);
      }
    };
    const node = trackRef.current;
    node?.addEventListener("transitionend", handleTransitionEnd);
    return () => node?.removeEventListener("transitionend", handleTransitionEnd);
  }, [current, cardsPerView, total]);

  // Navigation handlers
  const handlePrev = () => {
    setCurrent((prev) => Math.max(0, prev - 1));
  };
  const handleNext = () => {
    setCurrent((prev) => Math.min(maxIndex, prev + 1));
  };


  // Auto-swiping effect
  useEffect(() => {
    if (timerRef.current) clearTimeout(timerRef.current);
    if (current < maxIndex) {
      timerRef.current = setTimeout(() => {
        setCurrent((prev) => Math.min(maxIndex, prev + 1));
      }, 5000);
    } else {
      // Loop to start
      timerRef.current = setTimeout(() => {
        setCurrent(0);
      }, 5000);
    }
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, [current, maxIndex]);

  return (
    <section id="testimonials" className="px-4 lg:px-6 py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-10">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-2">What Our Customers Say</h2>
          <p className="text-lg text-gray-600">Don't just take our word for it - hear from our satisfied customers</p>
        </div>
        <div className="relative flex items-center">
          {/* Left arrow */}
          <button
            aria-label="Previous testimonials"
            onClick={handlePrev}
            className="absolute left-0 z-10 bg-white rounded-full shadow-md p-2 hover:bg-gray-100 transition disabled:opacity-50"
            style={{ top: '50%', transform: 'translateY(-50%)' }}
            disabled={current === 0}
          >
            <ChevronLeft className="h-7 w-7 text-blue-600" />
          </button>

          {/* Cards */}
          {/* DEBUG: Show cardsPerView value */}
          <div className="text-xs text-gray-400 absolute top-0 right-0">cardsPerView: {cardsPerView}</div>
          <div className="w-full overflow-hidden">
            <div
              ref={trackRef}
              className="flex gap-6 w-full"
              style={{
                width: `${(100 / cardsPerView) * testimonials.length}%`,
                transform: `translateX(-${current * (100 / testimonials.length)}%)`,
                transition: "transform 0.7s cubic-bezier(0.4,0,0.2,1)",
              }}
            >
              {testimonials.map((t, idx) => (
                <TestimonialCard
                  key={idx + t.id}
                  testimonial={t}
                                  />
              ))}
            </div>
          </div>

          {/* Right arrow */}
          <button
            aria-label="Next testimonials"
            onClick={handleNext}
            className="absolute right-0 z-10 bg-white rounded-full shadow-md p-2 hover:bg-gray-100 transition disabled:opacity-50"
            style={{ top: '50%', transform: 'translateY(-50%)' }}
            disabled={current >= maxIndex}
          >
            <ChevronRight className="h-7 w-7 text-blue-600" />
          </button>
        </div>
      </div>
    </section>
  );
};

// Read More Card Component
const MAX_PREVIEW_LENGTH = 120;

function TestimonialCard({ testimonial }: { testimonial: typeof testimonials[0] }) {
  const [expanded, setExpanded] = useState(false);
  const isLong = testimonial.text.length > MAX_PREVIEW_LENGTH;
  const displayText = expanded || !isLong ? testimonial.text : testimonial.text.slice(0, MAX_PREVIEW_LENGTH) + "...";
  const Icon = testimonial.icon;

  return (
    <div
      className="bg-white rounded-2xl p-5 sm:p-6 md:p-6 shadow-lg flex flex-col justify-between min-h-[220px]"
      style={{
        minHeight: 180,
        boxSizing: "border-box",
        flex: "1 1 0",
        minWidth: 320,
        maxWidth: 400,
        width: '100%',
      }}
    >
      <div className="flex items-center mb-2">
        {[...Array(testimonial.rating)].map((_, i) => (
          <Star key={i} className="h-4 w-4 text-yellow-500 fill-current" />
        ))}
      </div>
      <Quote className="h-7 w-7 text-blue-600 mb-2" />
      <p className="text-gray-600 mb-4 text-sm italic">
        {`"${displayText}"`}
        {isLong && !expanded && (
          <span
            className="text-gray-400 cursor-pointer ml-2"
            onClick={() => setExpanded(true)}
          >
            Read more
          </span>
        )}
      </p>
      <div className="flex items-center mt-auto">
        <div className={`${testimonial.bgColor} p-2 rounded-full mr-3`}>
          <Icon className={`h-5 w-5 ${testimonial.iconColor}`} />
        </div>
        <div>
          <p className="font-semibold text-gray-900 text-sm">{testimonial.name}</p>
          <p className="text-xs text-gray-600">{testimonial.role}</p>
        </div>
      </div>
    </div>
  );
}

export default TestimonialsSection;
