import React from 'react'
import Influencers from "../../components/Influencers/Influencer.jsx";
import SideBar from "../../components/SideBar/SideBar.jsx";
import LoggedInUser from "../../components/loggedInUser/loggedInUser.jsx";
import Feed from "../../components/RecentPosts/Feed.jsx";
import Calendar from "../../components/Calendar/Calendar.jsx";

import "./Dashboard.css"
const Dashboard = () => {
  return (
    <div className='dashboard-container'>
      <div style={{width:"7vw"}}>
        <SideBar />
      </div>
      
      <div className='influencer-section container'>
        <div className="loggedInUser">

        <LoggedInUser/>
        </div>
        
        <Influencers/>
        <div>
        <h5 className='p-2 recent-text'>Recent Posts</h5>
        </div>
        <div className='feed-calendar ' >

          <div className='feed-container'>
          <Feed />

          </div>
          <div className='calendar-container'>
          <Calendar/>

          </div>

        

        </div>
       
      </div>
    </div>
  )
}

export default Dashboard