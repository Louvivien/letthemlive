import React,{useState} from 'react'
import PostsGalleryItem from '../postsGalleryItem/postsGalleryIteml'
import "./Feed.css"
const Feed = () => {
  // extract images from api
  const [imagesApi, setimagesApi] = useState([
    {
      img1:"/images/image4@2x.png",
      img2:"/images/image1@2x.png",
      img3:"/images/image2@2x.png"
    },
    {
      img1:"/images/image4@2x.png",
      img2:"/images/image1@2x.png",
      img3:"/images/image2@2x.png"
    }
  ])
  return (
    <div className='feed-container '>
      <div className='d-flex  flex-wrap'>
      {
        imagesApi.map((image)=>{
          return(
            <PostsGalleryItem image={image} />
          )
        })
      }
      </div>
    
    </div>
  )
}

export default Feed