


const WhatsAppIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g>
      <circle cx="12" cy="12" r="12" fill="#25D366" />
      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.472-.148-.67.15-.197.297-.767.966-.94 1.164-.173.198-.347.223-.644.075-.297-.149-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.372-.025-.521-.075-.149-.669-1.612-.916-2.206-.242-.579-.487-.5-.67-.51-.173-.007-.372-.009-.57-.009-.198 0-.52.075-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.214 3.073.149.198 2.099 3.206 5.077 4.367.71.306 1.263.488 1.695.624.712.227 1.36.195 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.413-.074-.124-.272-.198-.57-.347z" fill="#fff"/>
    </g>
  </svg>
);

const whatsappLink = "https://wa.me/254740786838"; 

const WhatsAppFloatingButton = () => (
  <a
    href={whatsappLink}
    target="_blank"
    rel="noopener noreferrer"
    className="fixed left-6 bottom-6 z-50 flex items-center px-4 py-3 bg-green-500 text-white rounded-full shadow-lg hover:bg-green-600 transition-colors"
    style={{ minWidth: 180 }}
    aria-label="Chat with us on WhatsApp"
  >
    <span className="mr-3">
      <WhatsAppIcon />
    </span>
    <span className="font-semibold text-base">Chat with us</span>
  </a>
);

export default WhatsAppFloatingButton;
