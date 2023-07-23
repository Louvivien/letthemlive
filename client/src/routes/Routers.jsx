import {React,useEffect,useState,useContext} from "react";
import { Router,Routes, Route, Navigate,useNavigate } from "react-router-dom";

import Login from "../pages/Login/Login.jsx";
import Register from "../pages/Register/Register.jsx";
import Dashboard from "../pages/Dashboard/Dashboard.jsx";
// import Dashboard from "../pages/Dashboard/LandingPage.jsx";
import LandingPage from "../pages/LandingPage/LandingPage.jsx";


const Routers = () => {

  
  return (
    <Routes>
      {/* <Route path="/" element={<Navigate to="/home" />} /> */}
      {/* <Route path="/home" element={<Home />} /> */}
      <Route
        path="/login"
        element={<Login/>}
      />
      <Route path="/register" element={<Register />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/" element={<LandingPage />} />
    </Routes>
  );
}

export default Routers;
