import React from 'react'
import "./loggedInUser.css"
const loggedInUser = () => {
  // extract name and image from api
  return (
    <div className='loggedin-container'>
      <h5 className='text-center'>Hello</h5>
      <div>
      <img src='/images/loggedInImage.png' className='loggedin-img'/>
      <div className='Online-dot'></div>
      </div>
      
    </div>
  )
}

export default loggedInUser