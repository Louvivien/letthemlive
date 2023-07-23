import React,{useState} from 'react'
import { RiHome2Line } from 'react-icons/ri';
import { FaUser } from 'react-icons/fa';
import { RiCloudLine } from 'react-icons/ri';
import { FaCog } from 'react-icons/fa';
import { FaPlusCircle } from 'react-icons/fa';
import { BsCalendar } from 'react-icons/bs';
import "./SideBar.css"
const SideBar = () => {
  const [showNav, setShowNav] = useState(false);

  const toggleNav = () => {
    setShowNav(!showNav);
  };

  return (
    <nav className="navbar bg-dark sidebar-container">
      <a className="navbar-brand text-white">L</a>
      <ul className="navbar-nav">
        <li className="nav-item">
          <a className="nav-link text-white" href="#home">
          <FaUser className='icon' />
          </a>
        </li>
        <li className="nav-item">
          <a className="nav-link text-white" href="#authentication">
          <RiCloudLine className='icon'  />
          </a>
        </li>
        <li className="nav-item">
          <a className="nav-link text-white" href="#calendar">
          <BsCalendar className='icon' />
          </a>
        </li>
        <li className="nav-item">
          <button className="nav-link text-white add-influencer">
          <FaPlusCircle className='icon' />
          </button>
        </li>
        <li className="nav-item">
          <a className="nav-link text-white" href="#setting">
          <FaCog className='icon'/>
          </a>
        </li>
      </ul>
    </nav>
  );
}

export default SideBar