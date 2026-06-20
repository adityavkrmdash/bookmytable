from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)


OUTPUT = "output/pdf/bookmytable-frontend-interview-explanation.pdf"


def page_chrome(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFont("Helvetica-Bold", 9)
    canvas.setFillColor(colors.HexColor("#111827"))
    canvas.drawString(0.62 * inch, height - 0.42 * inch, "BookMyTable Frontend Interview Notes")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.drawRightString(width - 0.62 * inch, 0.36 * inch, f"Page {doc.page}")
    canvas.restoreState()


def p(text, style):
    return Paragraph(text, style)


def b(text, style):
    return Paragraph("- " + text, style)


def file_block(story, styles, file_name, role, explain, flow=None, code=None, interview=None):
    story.append(p(file_name, styles["file"]))
    story.append(p("<b>Role:</b> " + role, styles["body"]))
    story.append(p("<b>Simple explanation:</b> " + explain, styles["body"]))
    if flow:
        story.append(p("Execution / logic order", styles["h3"]))
        for item in flow:
            story.append(b(item, styles["body"]))
    if code:
        story.append(Preformatted(code, styles["code"]))
    if interview:
        story.append(p("Interview answer", styles["h3"]))
        story.append(p(interview, styles["callout"]))
    story.append(Spacer(1, 8))


def api_table(styles):
    rows = [
        ["Frontend Function", "Backend Endpoint", "Purpose"],
        ["createBooking(data)", "POST /api/bookings", "Sends final booking data to backend."],
        ["getAllBookings()", "GET /api/bookings", "Loads booking list for admin dashboard."],
        ["getBookingById(id)", "GET /api/bookings/:id", "Fetches one booking by bookingId."],
        ["deleteBooking(id)", "DELETE /api/bookings/:id", "Cancels/deletes a booking from admin dashboard."],
        ["getWeatherForDate(date, location)", "GET /api/weather", "Gets weather for seating suggestion."],
        ["getAvailableSlots(date)", "GET /api/bookings/available-slots", "Gets free slots for selected date."],
    ]
    table = Table(rows, colWidths=[2.05 * inch, 2.0 * inch, 2.45 * inch], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111827")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 7.6),
                ("LEADING", (0, 0), (-1, -1), 9.8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#CBD5E1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def step_table(styles):
    rows = [
        ["Step", "Meaning", "Data Captured / Action"],
        ["null", "Assistant not started", "Shows Start New Booking button."],
        ["-1", "Intent check", "Checks if user wants booking/reservation/table."],
        ["0", "Guest count", "Parses number using textToNumber."],
        ["1", "Date", "Parses natural date, fetches weather and slots."],
        ["2", "Seating", "Stores indoor/outdoor preference."],
        ["3", "Time", "Normalizes time and checks against availableSlots."],
        ["4", "Cuisine", "Stores cuisinePreference."],
        ["5", "Email", "Typed email or skip; stores customerEmail."],
        ["6", "Requests", "Stores specialRequests."],
        ["7", "Confirm", "Calls createBooking and shows success."],
    ]
    table = Table(rows, colWidths=[0.55 * inch, 1.55 * inch, 4.4 * inch], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F766E")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 7.6),
                ("LEADING", (0, 0), (-1, -1), 9.8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#CBD5E1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def qa_table(styles):
    rows = [
        ["Question", "Answer to give"],
        ["What starts the frontend?", "npm start runs react-scripts start, then index.html loads the React bundle."],
        ["Where does React mount?", "src/index.js mounts <App /> into public/index.html's div with id root."],
        ["How routing works?", "App.js uses BrowserRouter, Routes, and Route to show Home at / and AdminDashboard at /admin."],
        ["What is useState used for?", "It stores changing UI data like step, bookingData, loading, slots, and success state."],
        ["What is the voice flow?", "Home.js uses a step-based conversation. Each step captures one booking field."],
        ["How is speech converted to text?", "VoiceAssistant uses react-speech-recognition and sends final transcript to Home.js."],
        ["How are dates parsed?", "chrono-node parses natural phrases like next Friday, then formatLocalDate converts it to YYYY-MM-DD."],
        ["Why Promise.all?", "It fetches weather and available slots at the same time, improving speed."],
        ["How does frontend call backend?", "services/api.js creates an Axios instance and exports API helper functions."],
        ["How does admin dashboard work?", "It loads bookings and analytics, displays cards, a Chart.js bar chart, and a reservation table."],
        ["Main limitation?", "API base URL must match backend port; also admin route has no frontend auth protection."],
    ]
    table = Table(rows, colWidths=[2.15 * inch, 4.35 * inch], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#7C2D12")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 7.6),
                ("LEADING", (0, 0), (-1, -1), 9.8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#CBD5E1")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def build():
    sample = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle("title", parent=sample["Title"], fontName="Helvetica-Bold", fontSize=21, leading=26, alignment=TA_CENTER, textColor=colors.HexColor("#111827"), spaceAfter=6),
        "sub": ParagraphStyle("sub", parent=sample["Normal"], fontSize=9.5, leading=13, alignment=TA_CENTER, textColor=colors.HexColor("#4B5563"), spaceAfter=14),
        "h2": ParagraphStyle("h2", parent=sample["Heading2"], fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=colors.HexColor("#111827"), spaceBefore=10, spaceAfter=5),
        "h3": ParagraphStyle("h3", parent=sample["Heading3"], fontName="Helvetica-Bold", fontSize=9.5, leading=12, textColor=colors.HexColor("#334155"), spaceBefore=5, spaceAfter=3),
        "file": ParagraphStyle("file", parent=sample["Heading2"], fontName="Helvetica-Bold", fontSize=12.3, leading=15.5, textColor=colors.HexColor("#075985"), backColor=colors.HexColor("#E0F2FE"), borderColor=colors.HexColor("#38BDF8"), borderWidth=0.5, borderPadding=5, spaceBefore=9, spaceAfter=5),
        "body": ParagraphStyle("body", parent=sample["BodyText"], fontSize=9.1, leading=12.25, textColor=colors.HexColor("#1F2937"), spaceAfter=4),
        "callout": ParagraphStyle("callout", parent=sample["BodyText"], fontSize=9, leading=12.2, textColor=colors.HexColor("#0F172A"), backColor=colors.HexColor("#ECFDF5"), borderColor=colors.HexColor("#34D399"), borderWidth=0.5, borderPadding=6, spaceAfter=6),
        "warn": ParagraphStyle("warn", parent=sample["BodyText"], fontSize=9, leading=12.2, textColor=colors.HexColor("#451A03"), backColor=colors.HexColor("#FEF3C7"), borderColor=colors.HexColor("#F59E0B"), borderWidth=0.5, borderPadding=6, spaceAfter=6),
        "code": ParagraphStyle("code", fontName="Courier", fontSize=7.4, leading=9.4, textColor=colors.HexColor("#111827"), backColor=colors.HexColor("#F3F4F6"), borderColor=colors.HexColor("#CBD5E1"), borderWidth=0.4, borderPadding=5, leftIndent=4, rightIndent=4, spaceBefore=3, spaceAfter=6),
    }

    doc = BaseDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=0.62 * inch,
        rightMargin=0.62 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.58 * inch,
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=page_chrome)])

    story = []
    story.append(p("BookMyTable Frontend Explanation", styles["title"]))
    story.append(p("Simple interview notes, ordered by execution hierarchy", styles["sub"]))
    story.append(p("Read this from top to bottom. It follows how the React app loads, routes pages, manages voice booking state, calls the backend, and shows admin analytics.", styles["body"]))

    story.append(p("Frontend Execution Hierarchy", styles["h2"]))
    for item in [
        "frontend/package.json defines scripts and frontend dependencies.",
        "public/index.html contains the root div where React is mounted.",
        "src/index.js creates the React root and renders App.",
        "src/App.js sets up React Router navigation and page routes.",
        "src/pages/Home.js is the main voice booking page and conversation state machine.",
        "src/components/VoiceAssistant.js listens to speech and sends transcript to Home.",
        "src/components/AgentBubble.js, BookingSummary.js, and LoadingIndicator.js render reusable UI pieces.",
        "src/services/api.js centralizes Axios calls to the Express backend.",
        "src/pages/AdminDashboard.js loads bookings and analytics for admin view.",
        "src/index.css and App.css contain styling; public manifest/assets support browser/PWA metadata.",
    ]:
        story.append(b(item, styles["body"]))

    story.append(p("Frontend API Map", styles["h2"]))
    story.append(api_table(styles))

    file_block(
        story,
        styles,
        "1. frontend/package.json",
        "Defines how the React frontend runs and which libraries it uses.",
        "The app is a Create React App project. The most important script is npm start, which starts the development server.",
        flow=[
            "react-scripts start launches the local frontend dev server.",
            "react-scripts build creates production-ready static files.",
            "axios is used for backend API calls.",
            "react-router-dom is used for page navigation.",
            "react-speech-recognition is used for microphone speech-to-text.",
            "chrono-node parses natural language dates.",
            "chart.js and react-chartjs-2 render admin charts.",
        ],
        code='"scripts": {\n  "start": "react-scripts start",\n  "build": "react-scripts build",\n  "test": "react-scripts test"\n}',
        interview="package.json is the frontend configuration file. It tells me how to start, build, and test the React app, and it lists the libraries used by the booking UI.",
    )

    file_block(
        story,
        styles,
        "2. frontend/public/index.html",
        "The HTML template used by Create React App.",
        "It contains a div with id root. React does not manually write full HTML pages; it injects the app inside this root element.",
        flow=[
            "Browser loads index.html.",
            "React bundle is attached during development/build.",
            "The app renders inside <div id='root'></div>.",
            "Title and manifest links are defined here.",
        ],
        code='<div id="root"></div>',
        interview="index.html is the shell. The actual UI comes from React components mounted into the root div.",
    )

    file_block(
        story,
        styles,
        "3. frontend/src/index.js",
        "JavaScript entry point for the React app.",
        "It imports React, ReactDOM, CSS, App, and reportWebVitals. Then it renders <App /> into the root element from index.html.",
        flow=[
            "document.getElementById('root') finds the root div.",
            "ReactDOM.createRoot creates a React root.",
            "root.render displays App inside React.StrictMode.",
            "reportWebVitals can measure performance if a logging function is passed.",
        ],
        code="const root = ReactDOM.createRoot(document.getElementById('root'));\nroot.render(\n  <React.StrictMode>\n    <App />\n  </React.StrictMode>\n);",
        interview="This file connects the HTML page to the React component tree. After this, App.js controls which page appears.",
    )

    file_block(
        story,
        styles,
        "4. frontend/src/App.js",
        "Sets up client-side routing and navigation.",
        "It uses BrowserRouter, Routes, Route, Link, and useLocation from react-router-dom. The user can move between the booking page and admin panel without full page reloads.",
        flow=[
            "Navigation reads current URL with useLocation.",
            "Two Links are rendered: Booking and Admin Panel.",
            "Route / renders Home.",
            "Route /admin renders AdminDashboard.",
            "BrowserRouter wraps everything so routing works.",
        ],
        code='<Route path="/" element={<Home />} />\n<Route path="/admin" element={<AdminDashboard />} />',
        interview="App.js is the frontend router. It does not contain booking logic; it decides which page component should be shown for each URL.",
    )

    story.append(PageBreak())
    story.append(p("5. frontend/src/pages/Home.js", styles["file"]))
    story.append(p("<b>Role:</b> Main customer booking page. It controls the voice assistant flow, stores booking state, fetches weather and available slots, and submits the final booking.", styles["body"]))
    story.append(p("Important imports", styles["h3"]))
    for item in [
        "useState stores changing UI and booking values.",
        "VoiceAssistant captures spoken input.",
        "BookingSummary shows final review before confirmation.",
        "AgentBubble displays assistant messages.",
        "LoadingIndicator shows loading while API calls run.",
        "createBooking, getWeatherForDate, and getAvailableSlots call the backend.",
        "parseDate from chrono-node understands natural date phrases.",
    ]:
        story.append(b(item, styles["body"]))

    story.append(p("Helper functions", styles["h3"]))
    for item in [
        "textToNumber converts words like three or digits like 3 into a number.",
        "normalizeTime converts spoken time into format like 8:00 PM.",
        "formatLocalDate converts Date object into YYYY-MM-DD without UTC day shifting.",
        "speak uses browser speechSynthesis to speak assistant messages out loud.",
    ]:
        story.append(b(item, styles["body"]))

    story.append(p("Main state variables", styles["h3"]))
    for item in [
        "step controls the current conversation stage.",
        "assistantActivated decides whether the voice assistant UI is active.",
        "isSuccess decides whether to show booking confirmation screen.",
        "agentMessage stores the assistant's latest message.",
        "bookingData stores all collected reservation fields.",
        "isLoading shows async loading state.",
        "availableSlots stores backend slot response.",
        "emailInput stores typed email because voice is unreliable for email addresses.",
    ]:
        story.append(b(item, styles["body"]))

    story.append(p("Conversation step map", styles["h3"]))
    story.append(step_table(styles))
    story.append(
        p(
            "Interview answer: Home.js is a step-based state machine. Every user response is processed based on the current step, then the app updates bookingData and moves to the next step.",
            styles["callout"],
        )
    )

    story.append(p("Booking flow example", styles["h3"]))
    story.append(
        Preformatted(
            "User clicks Start New Booking\n"
            "-> step becomes -1\n"
            "-> user says book table\n"
            "-> step 0 asks guest count\n"
            "-> step 1 parses date and calls weather + slots APIs\n"
            "-> step 2 stores seating\n"
            "-> step 3 validates selected time\n"
            "-> step 4 stores cuisine\n"
            "-> step 5 stores email or skip\n"
            "-> step 6 stores special requests\n"
            "-> step 7 calls createBooking(bookingData)",
            styles["code"],
        )
    )

    story.append(p("Important async part in Home.js", styles["h3"]))
    story.append(
        Preformatted(
            "const [weather, slots] = await Promise.all([\n"
            "  getWeatherForDate(dateStr),\n"
            "  getAvailableSlots(dateStr),\n"
            "]);",
            styles["code"],
        )
    )
    story.append(p("Promise.all runs both API calls together. This is faster than waiting for weather first and then slots.", styles["body"]))

    story.append(p("Final booking submit", styles["h3"]))
    story.append(
        Preformatted(
            "if (input.includes('yes') || input.includes('confirm')) {\n"
            "  setIsLoading(true);\n"
            "  await createBooking(bookingData);\n"
            "  setIsSuccess(true);\n"
            "  setAssistantActivated(false);\n"
            "}",
            styles["code"],
        )
    )
    story.append(p("If backend returns an error, Home.js reads e.response?.data?.message and speaks/shows that error.", styles["body"]))

    file_block(
        story,
        styles,
        "6. frontend/src/components/VoiceAssistant.js",
        "Reusable component for microphone speech recognition.",
        "It uses react-speech-recognition. When the user stops speaking, it sends the final transcript to Home.js using onUserMessage.",
        flow=[
            "useSpeechRecognition gives transcript, listening, resetTranscript, and support check.",
            "useEffect watches listening and transcript.",
            "When listening becomes false and transcript has text, it calls onUserMessage(transcript.trim()).",
            "Then resetTranscript clears the old text.",
            "Button toggles startListening and stopListening.",
            "Language is set to en-IN for Indian English recognition.",
        ],
        code="if (!listening && transcript.trim().length > 0) {\n  onUserMessage(transcript.trim());\n  resetTranscript();\n}",
        interview="VoiceAssistant does not decide booking logic. It only converts voice into text and passes that text back to Home.js.",
    )

    file_block(
        story,
        styles,
        "7. frontend/src/components/AgentBubble.js",
        "Small display component for assistant messages.",
        "It receives a message prop and renders it inside a styled bubble.",
        flow=["Home.js controls agentMessage.", "AgentBubble only displays that message."],
        code="<strong>Agent:</strong> {message}",
        interview="This is a presentational component. It has no state and no business logic.",
    )

    file_block(
        story,
        styles,
        "8. frontend/src/components/BookingSummary.js",
        "Shows collected booking data before final confirmation.",
        "It receives bookingData as data prop and displays guests, date, time, seating, cuisine, and special requests.",
        flow=[
            "Rendered only when step === 7.",
            "Uses optional chaining for bookingDate because date may be null initially.",
            "Helps user review before saying yes/confirm.",
        ],
        code="{data.bookingDate?.toDateString()}",
        interview="BookingSummary is a reusable review table. It reads props and renders the final booking details before submission.",
    )

    file_block(
        story,
        styles,
        "9. frontend/src/components/LoadingIndicator.js",
        "Shows a loading/status message during async work.",
        "It accepts a message prop and renders it in blue bold text.",
        flow=["Used when isLoading is true in Home.js.", "Current Home.js renders it without message, so the loading area may be empty."],
        code="const LoadingIndicator = ({ message }) => (\n  <div>{message}</div>\n);",
        interview="This component is meant for loading feedback. A small improvement is passing a default message like Loading... or Confirming booking...",
    )

    story.append(PageBreak())
    file_block(
        story,
        styles,
        "10. frontend/src/services/api.js",
        "Centralized API communication layer.",
        "Instead of writing Axios calls everywhere, this file creates one Axios instance and exports helper functions for backend endpoints.",
        flow=[
            "API is created with baseURL http://localhost:5000/api.",
            "createBooking sends POST /bookings.",
            "getAllBookings sends GET /bookings.",
            "getBookingById sends GET /bookings/:id.",
            "deleteBooking sends DELETE /bookings/:id.",
            "getWeatherForDate sends GET /weather with date and location query params.",
            "getAvailableSlots sends GET /bookings/available-slots with date query param.",
            "Weather and slot functions return fallback values if API fails.",
        ],
        code='export const API = axios.create({\n  baseURL: "http://localhost:5000/api",\n});',
        interview="api.js separates backend communication from UI components. If the backend URL changes, I only need to update this service file.",
    )
    story.append(
        p(
            "Important configuration note: backend server.js defaults to port 8082, but frontend api.js points to 5000. This works only if backend .env sets PORT=5000. Otherwise frontend requests will fail until the ports match.",
            styles["warn"],
        )
    )

    story.append(p("11. frontend/src/pages/AdminDashboard.js", styles["file"]))
    story.append(p("<b>Role:</b> Admin page for viewing bookings, analytics cards, chart, CSV export, and cancellation.", styles["body"]))
    story.append(p("Important imports", styles["h3"]))
    for item in [
        "useEffect runs loadDashboardData when page opens.",
        "useState stores bookings, stats, and loading.",
        "API from api.js calls backend endpoints.",
        "Bar from react-chartjs-2 renders the chart.",
        "ChartJS.register enables required Chart.js parts.",
    ]:
        story.append(b(item, styles["body"]))

    story.append(p("loadDashboardData()", styles["h3"]))
    for item in [
        "Sets loading true.",
        "Uses Promise.all to fetch /bookings and /bookings/analytics together.",
        "Stores booking list in bookings state.",
        "Stores analytics response in stats state.",
        "Uses finally to set loading false even if request fails.",
    ]:
        story.append(b(item, styles["body"]))
    story.append(
        Preformatted(
            "const [bookingsRes, statsRes] = await Promise.all([\n"
            "  API.get('/bookings'),\n"
            "  API.get('/bookings/analytics'),\n"
            "]);",
            styles["code"],
        )
    )

    story.append(p("handleDelete(bookingId)", styles["h3"]))
    for item in [
        "Shows browser confirm dialog.",
        "Calls DELETE /bookings/:bookingId.",
        "Refreshes list and analytics after deletion.",
    ]:
        story.append(b(item, styles["body"]))

    story.append(p("exportToCSV()", styles["h3"]))
    for item in [
        "Builds CSV headers and rows from bookings state.",
        "Creates a Blob with text/csv type.",
        "Creates temporary object URL.",
        "Creates an anchor tag and triggers click to download CSV.",
    ]:
        story.append(b(item, styles["body"]))

    story.append(p("Chart data", styles["h3"]))
    for item in [
        "labels come from stats.popularCuisines _id values.",
        "data values come from stats.popularCuisines count values.",
        "Bar chart displays cuisine preference distribution.",
        "Optional chaining prevents crashing before stats loads.",
    ]:
        story.append(b(item, styles["body"]))
    story.append(p("Interview answer: AdminDashboard is a data-driven page. It loads backend data, stores it in state, and renders summary cards, chart, CSV export, and the booking table.", styles["callout"]))

    file_block(
        story,
        styles,
        "12. frontend/src/index.css and src/App.css",
        "Contain global styling for the frontend.",
        "index.css holds most of the app styling: navigation, assistant card, buttons, status dot, summary table, admin table, hero background, feature cards, and footer. App.css mostly contains default Create React App styles.",
        flow=[
            "index.js imports index.css globally.",
            "Class names like nav-bar, assistant-card, btn-primary, btn-talk, summary-table, admin-table are used by components.",
            "pulse-active animation visually shows microphone listening state.",
            "hero-wrapper applies the restaurant background image and layout.",
        ],
        code='import "./index.css";',
        interview="CSS is global in this app. Components use className values that are styled mainly in index.css.",
    )

    file_block(
        story,
        styles,
        "13. frontend/src/reportWebVitals.js",
        "Optional performance measurement helper from Create React App.",
        "It dynamically imports web-vitals only if a callback is passed. In current index.js, reportWebVitals() is called without a callback, so it does not log anything.",
        flow=[
            "Can measure CLS, FID, FCP, LCP, and TTFB.",
            "Useful if you want frontend performance analytics.",
            "Currently harmless and optional.",
        ],
        code="reportWebVitals();",
        interview="This is CRA's optional performance hook. The app does not depend on it for booking functionality.",
    )

    file_block(
        story,
        styles,
        "14. frontend/src/setupTests.js and src/App.test.js",
        "Testing setup and sample test files.",
        "setupTests.js imports jest-dom matchers. App.test.js is still the default Create React App test looking for learn react text.",
        flow=[
            "setupTests.js improves DOM assertions in tests.",
            "App.test.js likely fails because the app no longer renders learn react.",
            "A better test would check that BookMyTable or Start New Booking renders.",
        ],
        code="expect(element).toBeInTheDocument();",
        interview="I should update the default CRA test to match my real UI. Current test file is a known cleanup item.",
    )

    file_block(
        story,
        styles,
        "15. frontend/public/manifest.json, robots.txt, icons",
        "Static browser and PWA metadata files.",
        "manifest.json defines app name, icons, colors, display mode, and start URL. robots.txt tells search engines crawling rules. Icons are used by browser tabs and install prompts.",
        flow=[
            "index.html links manifest.json.",
            "favicon.ico is used as browser tab icon.",
            "logo192.png and logo512.png support mobile/PWA install metadata.",
            "robots.txt currently allows all crawlers.",
        ],
        interview="These files are not core React logic, but they support browser metadata and app install behavior.",
    )

    story.append(PageBreak())
    story.append(p("Complete User Booking Flow To Speak", styles["h2"]))
    story.append(
        p(
            "When the user opens the frontend, index.html provides the root div, index.js renders App, and App routes / to Home. "
            "On Home, the user clicks Start New Booking. The assistant starts at step -1 and asks for booking intent. Then each step captures one field: guests, date, seating, time, cuisine, email, and special requests. "
            "For the date step, the frontend parses natural language using chrono-node, calls the backend for weather and available slots using Promise.all, and gives seating advice. "
            "At the confirmation step, if the user says yes, Home calls createBooking from api.js, which sends POST /api/bookings to the backend. If successful, the frontend shows Booking Confirmed.",
            styles["callout"],
        )
    )

    story.append(p("Important Limitations To Be Honest About", styles["h2"]))
    for item in [
        "API baseURL is hardcoded to http://localhost:5000/api. It must match backend PORT or be moved to an environment variable.",
        "Admin panel has no login/auth UI. In production, protect /admin and backend admin endpoints.",
        "Voice recognition depends on browser support and microphone permission.",
        "Email is typed manually because speech-to-text is unreliable for email addresses. That is a practical design choice.",
        "LoadingIndicator is rendered without a message in Home.js, so it may display blank loading text.",
        "App.test.js is default CRA sample test and should be updated to test BookMyTable UI.",
        "CSV export does not escape every possible comma/newline perfectly; production CSV should sanitize values more carefully.",
        "Some UI text/assets include encoding issues for icons in the source display; replacing them with normal text/icons would look cleaner.",
    ]:
        story.append(b(item, styles["body"]))

    story.append(p("Interview Questions And Short Answers", styles["h2"]))
    story.append(qa_table(styles))

    story.append(p("Final 60-Second Frontend Explanation", styles["h2"]))
    story.append(
        p(
            "The frontend is a Create React App application. Execution starts from index.html, which contains the root div. "
            "src/index.js mounts the React app by rendering App into that root. App.js sets up React Router with two pages: Home for booking and AdminDashboard for admin. "
            "Home.js is the main voice booking flow. It uses useState to track the current conversation step, booking data, loading state, available slots, and success state. "
            "VoiceAssistant converts microphone speech into text and sends it to Home.js. Home.js processes each step, calls api.js for weather and available slots, and finally submits the booking through createBooking. "
            "AdminDashboard loads bookings and analytics from the backend, renders summary cards, a Chart.js bar chart, a reservation table, delete actions, and CSV export. "
            "The reusable components keep the UI organized, and api.js keeps backend communication centralized.",
            styles["callout"],
        )
    )

    doc.build(story)


if __name__ == "__main__":
    build()
