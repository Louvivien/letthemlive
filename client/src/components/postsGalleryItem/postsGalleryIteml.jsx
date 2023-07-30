import React from 'react'
import "./postsGalleryItem.css"
const postsGalleryIteml = ({image}) => {
  return (
    <div className='image-container'>
         <div className='images-gallery'>
          <img src={image.img1} className='vertical-img' />
          <div className='images-flex'>
            <img src={image.img2} className='vertical-half'/>
            <img src={image.img3} className='vertical-half'/>
          </div>
      </div>
    </div>
  )
}

export default postsGalleryIteml