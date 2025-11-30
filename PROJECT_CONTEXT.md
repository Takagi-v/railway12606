# Project Context & Startup Guide

## Project Overview
This project is a high-fidelity clone of a subset of the 12306 railway ticketing system.
**Goal:** The UI implementation must be highly consistent with the original 12306 interface, and key functionalities must be implemented.

## Startup Instructions

### Frontend
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```

### Backend
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Activate the Conda environment:
   ```bash
   conda activate 12606
   ```
3. Start the application using Uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```
