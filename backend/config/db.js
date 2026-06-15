import mongoose from "mongoose";

/**
 * Establishing connection to MongoDB using Mongoose
 */
const connectDB = async () => {
  const uri = process.env.MONGODB_URI;

  if (!uri) {
    console.error("MongoDB URI is not defined. Set MONGODB_URI in .env or environment variables.");
    process.exit(1);
  }

  try {
    const conn = await mongoose.connect(uri);

    console.log(`MongoDB Connected successfully`);
  } catch (error) {
    console.error(`Error connecting to MongoDB: ${error.message}`);
    process.exit(1);
  }
};

export default connectDB;
