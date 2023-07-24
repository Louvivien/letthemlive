import React from 'react'
import "./TwitterForm.css"
import { Link, useNavigate } from "react-router-dom";
const TwitterForm = () => {
  return (
    <div>
        <div className="main_container  ">
            <div className="container_tw">
                <div className="boxy box-one">
                    <i className="fab fa-twitter"><img src="https://img.icons8.com/color/50/000000/twitter--v1.png"/></i>
                    <button>
                        <img src="/images/google.png" width="19"/>
                        <span>Sign in with Google</span>
                    </button>
                    <button>
                        <img src="/images/apple.png" width="19"/>
                        <span>Sign in with Apple</span>
                    </button>
                </div>
                <h5>Or</h5>
                <div className="boxy box-two">
                    <form>
                        <input type="text" placeholder="Phone,email, or username"/>
                    </form>
                    <button className="next-btn">Next</button>
                    <button>Forget password</button>
                </div>
                <p>Don't have an account? <Link to="/register">Sign Up</Link></p>
            </div>
        </div>
    </div>
  )
}

export default TwitterForm