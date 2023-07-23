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
      <div className='sidebar-section'>
        <SideBar />
      </div>
      <div className='influencer-section container'>
        <LoggedInUser/>
        <Influencers/>
        <div>
        <h5 className='p-2'>Recent Posts</h5>
        </div>
        <div className='d-flex align-item-center justify-content-between flex-wrap  ' >
          <div className='text-center' >
          <Feed />
          </div>
          <div>
          <Calendar/>
          </div>
        
        

        </div>
       
      </div>
    </div>
  )
}

export default Dashboard