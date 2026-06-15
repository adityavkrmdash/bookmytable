# 🎙️ BookMyTable – Voice-Based Restaurant Booking App

## Overview

BookMyTable is a full-stack MERN application that allows users to book a restaurant table using their voice.
The app guides the user through a natural step-by-step conversation, collecting all necessary booking details like number of guests, date, time, cuisine preference, and any 
special requests.

It also checks the real-time weather for the chosen date and suggests indoor or outdoor seating accordingly. Once the user confirms the booking, the details are saved in the 
database and a confirmation email is sent automatically.

For admins, BookMyTable provides a simple Admin Dashboard where they can view all bookings, track analytics such as total bookings, popular cuisines, and peak booking hours, and 
export the booking data to CSV for offline use.

This project demonstrates voice interaction, backend integration, real-world API usage, and clean data handling, making it fully functional and assessment-ready.

---

## ✨ Features

### 🎙️ Voice Interaction Logic
- **Speech-to-Text (Input):** Uses the Web Speech API to transcribe user voice into real-time text data.
- **Text-to-Speech (Output):** Uses the browser’s SpeechSynthesis interface to generate the Agent’s verbal responses.
- **Natural Language Input:** Users can speak naturally (e.g., "Table for two tomorrow evening") instead of using rigid commands.


### 🗓️ Smart Date & Number Handling
- Converts spoken dates like “tomorrow” or “next Monday” into real dates using chrono-node.
- Converts spoken numbers like “two guests” into numeric values before saving.

### 🌦️ Weather-Aware Seating Suggestions
- **Fetches** real weather data from **OpenWeatherMap**.
- If rain is expected, the assistant suggests indoor seating.
- If the weather is clear, it suggests outdoor seating.
- Weather suggestions are spoken to the user as part of the conversation.

### 💾 Booking Management
- Bookings are stored in MongoDB.
- **REST APIs** support:
  - Create booking
  - Get all bookings
  - Get booking by ID
  - Cancel booking
 
### 📧 Booking Confirmation
- Email confirmation sent using Nodemailer (test SMTP)

### 📊 Admin Insights
- View all bookings in one place.
- **Analytics** for:
  - Total Bookings
  - Popular cuisines
  - Peak booking hours
- **Export** booking data to **CSV**.

---

## 🧰 Tech Stack

### 💻 Frontend
- React.js
- Web Speech API
- react-speech-recognition
- Axios
- Chart.js
- CSS (for styling components and layout)

### ⚙️ Backend
- Node.js
- Express.js

### 🗄️ Database 
- MongoDB Atlas
- Mongoose

### 🌐 External APIs 
- OpenWeatherMap API

### 🛠️ Tools

- Git + GitHub
- Postman (API testing)
- npm

---

## 📦 Installation & Setup

To get started with **BookMyTable**, follow these steps:

### 1. Clone the repository

  ```bash
  git clone https://github.com/adityavkrmdash/bookmytable.git
  cd bookmytable
  ```

### 2. Backend Setup

   ```bash
   cd backend
   npm install
   ```
   Create a `.env` file in the `backend` directory:

   ```env
   PORT=5000
   MONGODB_URI=your_mongodb_connection_string
   OPEN_WEATHER_API_KEY=your_openweathermap_key
   ```
   Run the server:

   ```bash
   npm run dev
   ```

### 3. Frontend Setup

   ```bash
   cd frontend
   npm install
   ```

   Start the React development server:

   ```bash
   npm start
   ```

---

## 🏗 App Structure

```bash
bookmytable/
│
├── backend/                       # Server-side Node.js + Express code
│   ├── server.js                  # Main Express server file, sets up middleware, DB, and routes
│   ├── config/                    # Configuration files
│   │   ├── db.js                  # MongoDB connection setup
│   │   └── weather.js             # Fetches weather data from OpenWeatherMap API
│   ├── models/                    # Database schemas
│   │   └── booking.model.js       # Booking schema for MongoDB
│   ├── controllers/               # Functions handling API logic
│   │   └── booking.controller.js  # Handles bookings, availability, analytics, weather, and emails
│   ├── routes/                    # API route definitions
│   │   ├── index.js               # Combines all backend routes
│   │   ├── booking.route.js       # Booking CRUD, availability, and analytics routes
│   │   └── weather.route.js       # Weather route used by the frontend
│   ├── .env                       # Environment variables such as MongoDB URI and API keys
│   ├── package.json               # Backend dependencies and scripts
│   └── package-lock.json          # Locked backend dependency versions
│
├── frontend/                      # Client-side React app
│   ├── public/                    # Static files such as HTML, favicon, and manifest
│   │   ├── index.html             # Main HTML template
│   │   └── manifest.json          # App metadata for browser/PWA behavior
│   ├── src/                       # React source code
│   │   ├── components/            # Reusable UI components
│   │   │   ├── AgentBubble.js     # Displays assistant messages
│   │   │   ├── BookingSummary.js  # Shows booking summary before confirmation
│   │   │   ├── LoadingIndicator.js # Shows loading state while processing
│   │   │   └── VoiceAssistant.js  # Handles speech recognition and microphone input
│   │   ├── services/              # API communication layer
│   │   │   └── api.js             # Axios functions for bookings, slots, and weather
│   │   ├── pages/                 # Main application pages
│   │   │   ├── AdminDashboard.js  # Admin view for bookings, analytics, and CSV export
│   │   │   └── Home.js            # Main voice-based booking page
│   │   ├── App.js                 # Main React app and routing
│   │   ├── index.js               # React entry point
│   │   └── setupTests.js          # Test setup file
│   ├── package.json               # Frontend dependencies and scripts
│   ├── package-lock.json          # Locked frontend dependency versions
│   └── README.md                  # Frontend-specific notes
│
├── README.md                      # Main project overview, features, setup, and explanation
└── .gitignore                     # Files and folders ignored by Git
```

---

## ⚠️ Limitations

- Voice recognition depends on browser support and microphone permissions.
- Weather forecasts are limited to the next 5 days due to API restrictions.
- Speech accuracy may vary with background noise or accents.

---

## 📈 Future Enhancements

- 🤖 **Advanced NLP Integration**  
  Moving beyond basic state management to use the OpenAI GPT API for more intelligent, free-flowing conversations.

- 🇮🇳 **Multi-language Support**  
  Adding support for Hindi + English voice commands.

- 🔀 **Code-Switching Capability**  
  Allowing the AI to understand "Hinglish" (mixing Hindi and English) seamlessly during a single conversation.

- 💬 **SMS & WhatsApp Confirmations**  
  Integrating Twilio or WhatsApp APIs to send real-time booking receipts and location pins.

- 🍱 **Live Menu Integration**  
  Connecting to the restaurant's POS system to check dish availability during the voice call.

---
