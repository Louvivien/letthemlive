import React, { useState } from 'react'
import { RiHome2Line } from 'react-icons/ri';
import { FaUser } from 'react-icons/fa';
import { RiCloudLine } from 'react-icons/ri';
import { FaCog } from 'react-icons/fa';
import { FaPlusCircle } from 'react-icons/fa';
import { BsCalendar } from 'react-icons/bs';
import { Link, useNavigate } from "react-router-dom";
import "./SideBar.css"
const SideBar = () => {
  const [showNav, setShowNav] = useState(false);

  const toggleNav = () => {
    setShowNav(!showNav);
  };

  return (
    <nav className="navbar bg-light sidebar-container">
      <Link className="navbar-brand text-white" to="/dashboard">L</Link>

      
      <div style={{ backgroundColor: "black", color: "black", width: "50px", textAlign: "center" }}>

      </div>
        

      <ul className="navbar-nav">

        <li className="nav-item">
          <Link className="nav-link text-white" to="/dashboard">
            <FaUser className='icon' />
          </Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link text-white" to="/auth">
            <RiCloudLine className='icon' />
          </Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link text-white" to="/dashboard">
            <BsCalendar className='icon' />
          </Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link text-white add-influencer" to="/createInfluencer">
            <FaPlusCircle className='icon' />
          </Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link text-white" to="/dashboard">
            <FaCog className='icon' />
          </Link>
        </li>
      </ul>
    </nav>
  );
}

export default SideBar