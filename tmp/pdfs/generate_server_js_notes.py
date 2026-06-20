from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)


OUTPUT = "output/pdf/bookmytable-server-js-explanation.pdf"


def header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(colors.HexColor("#1F2937"))
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(0.65 * inch, height - 0.42 * inch, "BookMyTable Backend Notes")
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(width - 0.65 * inch, 0.38 * inch, f"Page {doc.page}")
    canvas.restoreState()


def para(text, style):
    return Paragraph(text, style)


def bullet(text, style):
    return Paragraph(f"- {text}", style)


def build_pdf():
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=27,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#111827"),
        spaceAfter=8,
    )
    subtitle = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#4B5563"),
        spaceAfter=18,
    )
    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#111827"),
        spaceBefore=12,
        spaceAfter=6,
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1F2937"),
        spaceAfter=6,
    )
    small = ParagraphStyle(
        "Small",
        parent=body,
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#374151"),
    )
    code = ParagraphStyle(
        "Code",
        fontName="Courier",
        fontSize=8.5,
        leading=11,
        leftIndent=8,
        rightIndent=8,
        textColor=colors.HexColor("#111827"),
        backColor=colors.HexColor("#F3F4F6"),
        borderColor=colors.HexColor("#D1D5DB"),
        borderWidth=0.5,
        borderPadding=7,
        spaceBefore=4,
        spaceAfter=8,
    )
    callout = ParagraphStyle(
        "Callout",
        parent=body,
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#E0F2FE"),
        borderColor=colors.HexColor("#38BDF8"),
        borderWidth=0.6,
        borderPadding=8,
        spaceBefore=6,
        spaceAfter=10,
    )

    doc = BaseDocTemplate(
        OUTPUT,
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.72 * inch,
        bottomMargin=0.62 * inch,
    )
    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        id="normal",
    )
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=header_footer)])

    story = []
    story.append(para("BookMyTable Code Explanation", title))
    story.append(para("File 1: backend/server.js - backend execution start point", subtitle))
    story.append(
        para(
            "This PDF explains the first backend file in an interview-friendly way: what it does, "
            "how execution flows, and what answers you can give when asked about the server setup.",
            body,
        )
    )

    story.append(para("One-Line Interview Answer", h2))
    story.append(
        para(
            "server.js is the backend bootstrap file. It loads environment variables, creates the "
            "Express app, enables middleware, connects to MongoDB, mounts all API routes under /api, "
            "adds a global error handler, and starts listening on a port.",
            callout,
        )
    )

    story.append(para("Execution Flow", h2))
    flow_rows = [
        ["Step", "Code Area", "Purpose"],
        ["1", "Imports", "Loads Express, CORS, dotenv, path helpers, database connection, and routes."],
        ["2", "__dirname setup", "Recreates __dirname because ES modules do not provide it automatically."],
        ["3", "dotenv.config()", "Loads values from backend/.env such as PORT, MongoDB URI, and API keys."],
        ["4", "express()", "Creates the Express application object."],
        ["5", "Middleware", "Enables CORS and parses JSON request bodies."],
        ["6", "/api/health", "Simple route to verify that the backend is running."],
        ["7", "connectDB()", "Initializes the MongoDB connection."],
        ["8", "app.use('/api', routes)", "Mounts all backend API routes under the /api prefix."],
        ["9", "Error handler", "Returns consistent JSON errors instead of exposing raw failures."],
        ["10", "app.listen()", "Starts the server on the configured port."],
    ]
    table = Table(flow_rows, colWidths=[0.42 * inch, 1.55 * inch, 4.55 * inch], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111827")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("LEADING", (0, 0), (-1, -1), 11),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D1D5DB")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F9FAFB")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#F9FAFB"), colors.white]),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(table)

    story.append(para("Important Code Blocks", h2))
    story.append(para("1. Environment variables", body))
    story.append(Preformatted('dotenv.config({ path: path.join(__dirname, ".env") });', code))
    story.append(
        para(
            "This loads backend/.env. In interviews, say that sensitive values such as MongoDB URI "
            "and API keys are kept outside source code.",
            small,
        )
    )

    story.append(para("2. Middleware", body))
    story.append(Preformatted("app.use(cors());\napp.use(express.json());", code))
    story.append(
        para(
            "cors() allows the React frontend to call the backend from another port. express.json() "
            "converts incoming JSON request bodies into req.body.",
            small,
        )
    )

    story.append(para("3. Health check route", body))
    story.append(
        Preformatted(
            'app.get("/api/health", (req, res) => {\n'
            '  res.send("BookMyTable backend is running!");\n'
            "});",
            code,
        )
    )
    story.append(
        para(
            "This route is useful for quickly confirming that the backend server is live.",
            small,
        )
    )

    story.append(para("4. Route mounting", body))
    story.append(Preformatted('app.use("/api", routes);', code))
    story.append(
        para(
            "Every route exported from routes/index.js receives the /api prefix. For example, "
            "if booking routes are mounted as /bookings, the final URL becomes /api/bookings.",
            small,
        )
    )

    story.append(para("5. Global error handler", body))
    story.append(
        Preformatted(
            "app.use((err, req, res, next) => {\n"
            '  console.error("Global Error Log:", err.stack);\n'
            "  const statusCode = err.statusCode || 500;\n"
            "  res.status(statusCode).json({\n"
            "    success: false,\n"
            '    message: err.message || "Internal Server Error",\n'
            "  });\n"
            "});",
            code,
        )
    )
    story.append(
        para(
            "This middleware catches errors passed with next(err) and sends a standard JSON response.",
            small,
        )
    )

    story.append(para("End-To-End Request Example", h2))
    story.append(
        Preformatted(
            "React frontend\n"
            "  -> POST http://localhost:8082/api/bookings\n"
            "  -> server.js receives the request\n"
            "  -> cors and express.json middleware run\n"
            "  -> routes/index.js forwards the request\n"
            "  -> booking.route.js matches the endpoint\n"
            "  -> booking.controller.js handles business logic\n"
            "  -> booking.model.js saves or reads data in MongoDB\n"
            "  -> JSON response returns to the frontend",
            code,
        )
    )

    story.append(para("Questions Interviewers May Ask", h2))
    questions = [
        ("Why use cors?", "Because frontend and backend may run on different origins, such as different localhost ports."),
        ("Why use express.json()?", "To parse JSON sent by the frontend and make it available inside req.body."),
        ("Why use dotenv?", "To keep configuration and secrets outside the codebase."),
        ("What does app.use('/api', routes) mean?", "It prefixes all imported routes with /api."),
        ("What is the global error handler for?", "It centralizes error responses and avoids repeating error response code in every controller."),
        ("What happens when app.listen runs?", "The Express app starts accepting HTTP requests on the selected port."),
    ]
    q_rows = [["Question", "Best Short Answer"]] + [list(item) for item in questions]
    q_table = Table(q_rows, colWidths=[2.3 * inch, 4.2 * inch], repeatRows=1)
    q_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F766E")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("LEADING", (0, 0), (-1, -1), 11),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D1D5DB")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(q_table)

    story.append(para("Final Interview Script", h2))
    story.append(
        para(
            "In BookMyTable, server.js is the starting point of the backend. It loads environment "
            "variables with dotenv, creates an Express app, applies CORS and JSON middleware, exposes "
            "a health-check route, connects to MongoDB, and mounts all routes under /api. When a "
            "frontend request comes in, middleware runs first, then the request is passed to the route "
            "layer, then to the controller, and finally the controller talks to the MongoDB model. "
            "Any errors are handled by a global error middleware, and app.listen starts the backend "
            "on the configured port.",
            callout,
        )
    )

    doc.build(story)


if __name__ == "__main__":
    build_pdf()
