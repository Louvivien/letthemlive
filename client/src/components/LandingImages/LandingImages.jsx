import React from 'react'
import "./LandingImages.css"
import { Link, useNavigate } from "react-router-dom";
const LandingImages = () => {
  return (
    <div className='d-flex container flex-wrap align-items-center justify-content-center'>
      <div className='brand-logo-container'>
      <img src="/images/logo512.svg" width={"30rem"} style={{marginRight:"10px"}}/>
        <p style={{ color: "white", marginTop: "20px" }}>LETTHEMTALK</p>
      </div>
      <div className='left-container'>
        <div>

          <img className='left-main-image img-landing' src="/images/landing-img.png" style={{ width: "25vw" }} />
          <img className='left-main-image2 img-landing' src="/images/landing-img2.png" style={{ width: "15vw" }} />
        </div>
        <div className='mt-5 d-flex flex-column align-items-center'>
          <h2 className='main-headin'>Being an Influencer
            has never been
            so easy!</h2>
          <div className='btn-landing'>
            <Link to="/register" className='start-btn btn btn-primary m-2'> Start For Free</Link>
            <Link to="/login" className='login-btn btn btn-primary m-2'>Login</Link>
            <Link className='text-center mt-2' style={{color:"white"}}>Forget password?</Link>
          </div>
        </div>


        <a />
      </div>
      <div className='d-flex right-container flex-wrap'>
        <div className='d-flex flex-column'>
          <img src="/images/testimonial05-21@2x.png" style={{ width: "16vw" }} className='img-landing' />
          <img src="/images/frame-15@2x.png" style={{ width: "19vw" }} className='img-landing' />
          <img src="/images/rectangle8@2x.png" style={{ width: "17vw" }} className='img-landing' />
          <img src="/images/rectangle-23@2x.png" style={{ width: "20vw" }} className='img-landing' />
        </div>
        <div className='d-flex flex-column'>
          <img src="/images/smallpost2@3x.png" style={{ width: "20vw" }} className='img-landing' />
          <img src="/images/testimonial05-21@2x.png" style={{ width: "16vw" }} className='img-landing' />
          <img src="/images/smallpost3@3x.png" style={{ width: "16vw" }} className='img-landing' />
          <img src="/images/testimonial05-21@2x.png" style={{ width: "18vw" }} className='img-landing' />
          <img src="/images/rectangle8@2x.png" style={{ width: "16vw" }} className='img-landing' />
        </div>
      </div>
    </div>
  )
}

export default LandingImages