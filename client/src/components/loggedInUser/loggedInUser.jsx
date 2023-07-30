import React, { useContext } from 'react'
import UserContext from '../../context/UserContext'; 
import "./loggedInUser.css"

const LoggedInUser = () => { // Renamed from loggedInUser to LoggedInUser
  const { user } = useContext(UserContext); // extract user from context

  return (
    <div className='loggedin-container'>
      <h5 className='text-center'>Hello, {user.fullname}</h5> {/* Display user's full name */}
      <div>
      <img src={user.avatar || '/images/loggedInImage.png'} className='loggedin-img'/> {/* Display user's avatar image or default image */}
      <div className='Online-dot'></div>
      </div>
    </div>
  )
}

export default LoggedInUser 
