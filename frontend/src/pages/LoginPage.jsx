
import React, { useState } from "react";

import api from "../services/api";

export default function LoginPage() {

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [message, setMessage] =
    useState("");

  async function handleLogin(e) {

    e.preventDefault();

    try {

      const response =
        await api.post(
          "/login",
          {
            email,
            password,
          }
        );

      setMessage(
        response.data.message
      );

    } catch (error) {

      setMessage(
        "Login failed"
      );
    }
  }

  return (

    <div style={{ padding: "40px" }}>

      <h1>Login</h1>

      <form onSubmit={handleLogin}>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) =>
            setEmail(e.target.value)
          }
        />

        <br />
        <br />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
        />

        <br />
        <br />

        <button type="submit">
          Login
        </button>

      </form>

      <br />

      <p>{message}</p>

    </div>
  );
}

