
import React from "react";

import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import LoginPage from "../pages/LoginPage";
import ContactsPage from "../generated/ContactsPage";
import DashboardPage from "../generated/DashboardPage";

export default function AppRoutes() {

  return (

    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={
            <Navigate to="/login" />
          }
        />

        <Route
          path="/login"
          element={<LoginPage />}
        />

        <Route
          path="/contacts"
          element={<ContactsPage />}
        />

        <Route
          path="/dashboard"
          element={<DashboardPage />}
        />

      </Routes>

    </BrowserRouter>
  );
}

