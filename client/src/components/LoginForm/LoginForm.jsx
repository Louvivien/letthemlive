import React,{useState} from 'react'
import { Link, useNavigate } from "react-router-dom";
import "./LoginForm.css"
import axios from 'axios'; 


const LoginForm = () => {

    const [userDetails, setuserDetails] = useState({
        email:"",
        password:""
    })
    const [isChecked, setIsChecked] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');


    const navigate = useNavigate(); 


    const handleCheckboxChange = () => {
      setIsChecked((prevValue) => !prevValue);
    };


    const handleChange=(e)=>{
        setuserDetails((prev)=>({...prev,[e.target.name]:e.target.value}));
    }

    const handleLogin= async (e)=>{
      e.preventDefault();
    
      // Send a post request to the server
      try {
          const response = await axios.post(process.env.REACT_APP_BASE_URL + '/login', userDetails);
          console.log(response.data); // Log the response from the server
          // If login successful, store user information in session
          if (response.data.message === 'Login successful.') {
              sessionStorage.setItem('logged_in', true);
              sessionStorage.setItem('email', userDetails.email);
              navigate('/dashboard'); 
          }
      } catch (error) {
          console.error(`Error: ${error}`);
          // Set the error message
          if (error.response && error.response.data && error.response.data.message) {
              setErrorMessage(error.response.data.message);
          } else {
              setErrorMessage('No matching user found. Sign up instead?');
          }
      }
    }


  return (
    <div className='register-form-container'>
      <h5 className='register-main-heading'>Welcome Back!</h5>
      
      <div>
        <button className='signup-social-btn'>
        <img src='images/google.png' className='signup-icons' />
            <span className='social-heading'>
            Sign in with Google
            </span>
            
        </button>
        <div>
        <button className='signup-social-btn'>
        <img src='images/facebook.png' className='signup-icons' />
            <span className='social-heading'>
            Sign in with Facebook
            </span>
        </button>
        </div>
       
      </div>
      <h5 className='option-register'>-- OR --</h5>
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

    {errorMessage && <p className="error-message">{errorMessage}</p>} 


        <button type="submit" className='btn btn-primary register-btn'>Sign in</button>
      </form>
      <div>
        <span className='have-acc'>Don't have an account? <Link to="/register">Sign up Now</Link></span>
      </div>

    </div>
  )
}

export default LoginForm