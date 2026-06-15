import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import path from "path";
import { fileURLToPath } from "url";
import connectDB from "./config/db.js";
import routes from "./routes/index.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config({ path: path.join(__dirname, ".env") });

const app = express();
const PORT = process.env.PORT || 8082;

// Middlewares
// Enable Cross-Origin Resource Sharing for frontend access
app.use(cors());
// Parse incoming JSON request bodies
app.use(express.json());

// Health Check route to verify backend status
app.get("/api/health", (req, res) => {
  res.send("BookMyTable backend is running!");
});

// Initialize connection to MongoDB database
connectDB();

// All API routes
app.use("/api", routes);

// Global Error Handler Middleware
app.use((err, req, res, next) => {
  console.error("Global Error Log:", err.stack);

  const statusCode = err.statusCode || 500;
  res.status(statusCode).json({
    success: false,
    message: err.message || "Internal Server Error",
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running successfully on PORT: ${PORT}`);
});
