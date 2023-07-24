import React from 'react'
import Feed from "../../components/RecentPosts/Feed.jsx";
import Calendar from "../../components/Calendar/Calendar.jsx";
import Influencers from "../../components/Influencers/Influencer.jsx";
const Main = () => {
  return (
    <div>
        <Influencers/>
        <div>
        <h5 className='p-2 recent-text'>Recent Posts</h5>
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
  )
}

export default Main;