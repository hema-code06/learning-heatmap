import { useState } from "react";
import API from "../api";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      await API.post("/auth/register", {
        email,
        password,
      });

      alert("Registration successful. Login Here..");
      navigate("/");
    } catch (err) {
      alert(err.response?.data?.detail || "Registration failed!!");
    }
  };

  return (
    <div>
      <h2>Register</h2>
      <input placeholder="Email" onChange={(e) => setEmail(e.target.value)} />

      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />

      <button onClick={handleRegister}>Register</button>

      <p>
        Already have an account?{" "}
        <button onClick={() => navigate("/")}>Login</button>
      </p>
    </div>
  );
}
