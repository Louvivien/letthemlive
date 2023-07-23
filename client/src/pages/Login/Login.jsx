import React from 'react'
import "./Login.css"
import LoginForm from "../../components/LoginForm/LoginForm";
const Login = () => {
  return (
    <div className='register-section'>
      <img  alt="" className="left-side" src="images/register.png" />
     

      <div className="right-side">
        <div className='brand-logo-container'>
          <p style={{color:"white",marginTop:"20px"}}>letthemtalk</p>
        </div>
        <div className='register-form-section'>
        <LoginForm/>
        </div>
      
    </div>
      
    </div>
  )
}

export default Login