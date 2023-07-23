import React,{useState} from 'react'
import "./RegisterForm.css"

const RegisterForm = () => {

    const [userDetails, setuserDetails] = useState({
        fullName:"",
        email:"",
        password:"",
        confirmPassword:""
    })

    const handleRegister=(e)=>{
        e.preventDefault();
    }

    const handleChange=(e)=>{
        setuserDetails((prev)=>({...prev,[e.target.name]:e.target.value}));
    }
  return (
    <div className='register-form-container'>
      <h5 className='register-main-heading'>Create Account</h5>
      
      <div>
        <button className='signup-social-btn'>
        <img src='images/google.png' className='signup-icons' />
            <span className='social-heading'>
            Signup with Google
            </span>
            
        </button>
        <div>
        <button className='signup-social-btn'>
        <img src='images/facebook.png' className='signup-icons' />
            <span className='social-heading'>
            Signup with Google
            </span>
        </button>
        </div>
       
      </div>
      <h5 className='option-register'>--OR--</h5>
      <form onSubmit={handleRegister}>
        <div className=''>
          <input
            type="text"
            id="fullName"
            name="fullName"
            className='input-field-register'
            value={userDetails.fullName}
            onChange={handleChange}
            placeholder='Fullname'
            required
          />
        </div>
        <div>
          <input
            type="email"
            id="email"
            name="email"
            value={userDetails.email}
            onChange={handleChange}
            className='input-field-register'
            placeholder='Email Address'
            required
          />
        </div>
        <div>
          <input
            type="password"
            id="password"
            name="password"
            value={userDetails.password}
            className='input-field-register'
            onChange={handleChange}
           
            placeholder='Password'
            required
          />
        </div>
        <div>
          <input
            type="password"
            id="confirmPassword"
            name="confirmPassword"
            value={userDetails.confirmPassword}
            className='input-field-register'
            onChange={handleChange}
            placeholder='Confirm Password'
            required
          />
        </div>
        <button type="submit" className='btn btn-primary register-btn'>Create Account</button>
      </form>
      <div>
        <span className='have-acc'>Already Have an account?<a>Login</a></span>
      </div>

    </div>
  )
}

export default RegisterForm