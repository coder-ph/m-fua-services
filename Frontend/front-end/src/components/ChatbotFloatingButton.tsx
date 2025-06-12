import React, { useState, useRef, useEffect } from "react";

// Simple Message Icon SVG
const MessageIcon = () => (
  <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
    <g>
      <circle cx="16" cy="16" r="16" fill="#3B82F6" />
      <path d="M9 11c0-1.657 1.343-3 3-3h8c1.657 0 3 1.343 3 3v6c0 1.657-1.343 3-3 3h-3.448l-3.61 3.61A1.25 1.25 0 0 1 10 22v-3h2c-1.657 0-3-1.343-3-3v-5zm3-2a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h4v3.448L17.552 19H20a2 2 0 0 0 2-2v-6a2 2 0 0 0-2-2h-8z" fill="#fff"/>
    </g>
  </svg>
);

const ChatbotFloatingButton = () => {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hi! How can I help you today?" },
  ]);
  const inputRef = useRef<HTMLInputElement>(null);
  const chatBodyRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (open && inputRef.current) {
      inputRef.current.focus();
    }
  }, [open]);

  useEffect(() => {
    if (chatBodyRef.current) {
      chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight;
    }
  }, [messages, open]);

  function handleSend(e?: React.FormEvent) {
    if (e) e.preventDefault();
    if (!input.trim()) return;
    setMessages((msgs) => [
      ...msgs,
      { sender: "user", text: input },
      { sender: "bot", text: "Thanks for your message! (This is a demo bot.)" },
    ]);
    setInput("");
    if (inputRef.current) inputRef.current.focus();
  }

  return (
    <>
      {/* Floating Button */}
      <button
        className="fixed right-6 bottom-6 z-50 flex items-center justify-center w-16 h-16 bg-blue-500 text-white rounded-full shadow-lg hover:bg-blue-600 transition-colors"
        onClick={() => setOpen((prev) => !prev)}
        aria-label="Open chatbot"
        style={{ boxShadow: "0 4px 16px rgba(59,130,246,0.15)" }}
      >
        <MessageIcon />
      </button>
      {/* Chatbot Modal */}
      {open && (
        <div className="fixed right-6 bottom-24 z-50 w-80 max-w-full bg-white rounded-2xl shadow-2xl border border-gray-200 flex flex-col" style={{ minHeight: 320 }}>
          <div className="flex items-center justify-between px-4 py-3 bg-blue-500 rounded-t-2xl">
            <span className="text-white font-semibold">Chatbot</span>
            <button className="text-white text-xl" onClick={() => setOpen(false)} aria-label="Close chatbot">&times;</button>
          </div>
          <div ref={chatBodyRef} className="flex-1 p-4 overflow-y-auto text-gray-800 text-sm">
            {messages.map((msg, i) => (
              <div key={i} className={`mb-2 flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}>
                <div className={`px-3 py-2 rounded-lg max-w-[80%] ${msg.sender === "user" ? "bg-blue-100 text-blue-900" : "bg-gray-100 text-gray-900"}`}>
                  {msg.text}
                </div>
              </div>
            ))}
          </div>
          <form className="flex items-center border-t border-gray-100 p-2" onSubmit={handleSend}>
            <input
              ref={inputRef}
              type="text"
              className="flex-1 px-3 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-400"
              placeholder="Type your message..."
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => { if (e.key === "Enter" && !e.shiftKey) handleSend(e as any); }}
              autoFocus
            />
            <button type="submit" className="ml-2 px-3 py-2 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-600 transition-colors disabled:opacity-50" disabled={!input.trim()}>
              Send
            </button>
          </form>
        </div>
      )}
    </>
  );
};

export default ChatbotFloatingButton;
