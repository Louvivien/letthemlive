import React from 'react'
import "./Register.css"
import RegisterForm from "../../components/RegisterForm/RegisterForm";
const Register = () => {
  return (
    <div className='register-section'>
      <img  alt="" class="left-side" src="images/register.png" />
     

      <div class="right-side">
        <div className='brand-logo-container'>
          <p style={{color:"white",marginTop:"20px"}}>letthemtalk</p>
        </div>
        <div className='register-form-section'>
        <RegisterForm/>
        </div>
      
    </div>
      
    </div>
  )
}

export default Register