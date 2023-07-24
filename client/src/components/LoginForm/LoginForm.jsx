import React,{useState} from 'react'
import { useNavigate } from 'react-router-dom';

import "./LoginForm.css"

const LoginForm = () => {

  const navigate = useNavigate();


    const [userDetails, setuserDetails] = useState({
        email:"",
        password:""
    })
    const [isChecked, setIsChecked] = useState(false);

    const handleCheckboxChange = () => {
      setIsChecked((prevValue) => !prevValue);
    };


    const handleChange=(e)=>{
        setuserDetails((prev)=>({...prev,[e.target.name]:e.target.value}));
    }

    const handleLogin = (e) => {
      e.preventDefault();
      // Add your login logic here
      // If login is successful, navigate to the dashboard
      navigate('/dashboard');
    }
  return (
    <div className='register-form-container'>
      <h5 className='register-main-heading'>Welcome Back!</h5>
      
      <div>
        <button className='signup-social-btn'>
        <img src='images/google.png' className='signup-icons' />
            <span className='social-heading'>
            Signin with Google
            </span>
            
        </button>
        <div>
        <button className='signup-social-btn'>
        <img src='images/facebook.png' className='signup-icons' />
            <span className='social-heading'>
            Signin with Facebook
            </span>
        </button>
        </div>
       
      </div>
      <h5 className='option-register'>--OR--</h5>
      <form onSubmit={handleLogin}>
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

        <div className='forget-cont'>
            <div>
                <label  className='remember-input' style={{fontSize:"13px", padding:"5px", margin:"3px"}}>
                <input 

            
                type="checkbox"
                checked={isChecked}
                onChange={handleCheckboxChange}
                />
                Remember me!
            </label>
            <span className='forget-pass'>
                <a style={{color:"blue",fontSize:"12px"}}>forget password?</a>

            </span>

            </div>
    
    </div>

        <button type="submit" className='btn btn-primary register-btn'>Sign In</button>
      </form>
      <div>
        <span className='have-acc'>Don't have an account? <a>Register Now</a></span>
      </div>

    </div>
  )
}

export default LoginForm
