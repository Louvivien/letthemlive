import React,{useState} from 'react'
import PostsProgressBar from '../PostsProgressBar/PostsProgressBar'
import { FiMoreHorizontal } from 'react-icons/fi';
import "./InCard.css"

const InCard = ({influencer}) => {
  
  return (
    <div className='influencer-card-container'>
      <div className='influencer-info-container'>
        <img src={influencer.image} className='influencer-img' />
        <div className='influencer-name-container' >
          <h5 className='influencer-name'>{influencer.name}</h5>
          <h5 className='influencer-title'>{influencer.title}</h5>
        </div>
        <FiMoreHorizontal size={20} className='vertical-icon'/>
        
      </div>
      <div className='progress-bars'>
      
            <PostsProgressBar count={influencer.instagramPostsCount} title="Instagram"/>
            <PostsProgressBar count={influencer.facebookPostsCount} title="Facebook"/>
            <PostsProgressBar count={influencer.twitterPostsCount} title="Twitter"/>
     
    </div>


    </div>
    
  )
}

export default InCard