import React,{useState} from 'react'
import "./RegisterForm.css"
import Axios from "axios";
import { Link, useNavigate } from "react-router-dom";

const RegisterForm = () => {

    const [userDetails, setuserDetails] = useState({
        fullName:"",
        email:"",
        password:"",
        confirmPassword:""
    })

    const [errorMessage, setErrorMessage] = useState(''); 

    const navigate = useNavigate();


    const handleRegister= async (e)=>{
      e.preventDefault();

    // Check if passwords match
    if (userDetails.password !== userDetails.confirmPassword) {
      setErrorMessage("Passwords do not match!"); // Set the error message
      return;
  }

      // Send a post request to the server
      try {
        const response = await Axios.post(`${process.env.REACT_APP_BASE_URL}/signup`, {
            email: userDetails.email,
            password: userDetails.password,
            fullname: userDetails.fullName
        });
        console.log(response.data); 
        if (response.data.message === 'Signup successful.') {
            navigate('/dashboard'); 
          }
        } catch (error) {
            console.error(`Error: ${error}`);
            // Set the error message
            if (error.response && error.response.data && error.response.data.message) {
                setErrorMessage(error.response.data.message);
            } else {
                setErrorMessage('Error signing up. Please try again later.');
            }
        }
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
            Sign up with Google
            </span>
            
        </button>
        <div>
        <button className='signup-social-btn'>
        <img src='images/facebook.png' className='signup-icons' />
            <span className='social-heading'>
            Sign up with Facebook
            </span>
        </button>
        </div>
       
      </div>
      <h5 className='option-register'>-- OR --</h5>
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

        {errorMessage && <p className="error-message">{errorMessage}</p>} 

        <button type="submit" className='btn btn-primary register-btn'>Create Account</button>
      </form>
      <div>
        <span className='have-acc'>Already Have an account? <Link to="/login">Log in</Link></span>
      </div>

    </div>
  )
}

export default RegisterForm