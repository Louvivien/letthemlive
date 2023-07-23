import React, { useState, useEffect } from 'react'

import "./PostsProgressBar.css"

const PostsProgressBar = ({ count,title }) => {
  // I am taking % of 30000
  const [progressPrecentage, setprogressPrecentage] = useState(0);

  useEffect(() => {
    setprogressPrecentage((count * 100) / 30000);
  }, [])


  return (
    <div className='progress-container'>
      <div className='count-container'>
        <div className='post-title'>{title}</div>
        <div className='posts-count'>{count} posts</div>
      </div>
      <div className="progress progress-bar-container" >
        <div className="progress-bar" role="progressbar" aria-valuenow={`${progressPrecentage}` } 
          aria-valuemin="0" aria-valuemax="100" style={{width:`${progressPrecentage}%`}}>
        </div>
      </div>
    </div>
  )
}

export default PostsProgressBar