import React from 'react'
import "./LandingImages.css"
const LandingImages = () => {
  return (
    <div className='d-flex container flex-wrap'>
                <div className='brand-logo-container'>
          <p style={{color:"white",marginTop:"20px"}}>LETTHEMTALK</p>
        </div>
        <div className='left-container'>
            <div>

            <img className='left-main-image img-landing' src="/images/landing-img.png" style={{width:"250px"}} />
            <img className='left-main-image2 img-landing' src="/images/landing-img2.png" style={{width:"200px"}}  />
            </div>
            <div className='mt-5'>
            <h2 className='main-headin'>Being and Influencer has never been so easy!</h2>
            <div className='btn-landing'>
            <button className='start-btn btn btn-primary m-2'> Start For Free</button>
            <button className='login-btn btn btn-primary m-2'>Login</button>
            </div>
            </div>
           
            
            <a />
        </div>
        <div className='d-flex right-container flex-wrap'>
            <div className='d-flex flex-column'>
                <img src="/images/testimonial05-21@2x.png" style={{width:"190px"}} className='img-landing'  />
                <img src="/images/frame-15@2x.png"  style={{width:"200px"}} className='img-landing' />
                <img src="/images/rectangle8@2x.png" style={{width:"130px"}} className='img-landing'  />
                <img src="/images/rectangle-23@2x.png" style={{width:"175px"}} className='img-landing'   />
            </div>
            <div className='d-flex flex-column'>
                <img src="/images/smallpost2@3x.png" style={{width:"210px"}} className='img-landing'  />
                <img src="/images/testimonial05-21@2x.png" style={{width:"190px"}} className='img-landing'  />
                <img src="/images/smallpost3@3x.png" style={{width:"130px"}} className='img-landing'  />
                <img src="/images/testimonial05-21@2x.png" style={{width:"150px"}} className='img-landing' />
                <img src="/images/rectangle8@2x.png" style={{width:"130px"}} className='img-landing'  />
            </div>
        </div>
    </div>
  )
}

export default LandingImages