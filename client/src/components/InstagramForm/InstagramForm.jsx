import React from 'react'
import { Link, useNavigate } from "react-router-dom";
import "./InstagramForm.css"
const InstagramForm = () => {
    return (
        <div>
            <div className="box">
                <div className="title">
                    <Link to="https://ibb.co/XtKd6c7"><img alt="logoname"
                        border="0" src="https://i.ibb.co/2dCLRGv/logoname.png" /></Link>
                </div>
                <form className="login-form">
                    <div className="form-content">
                        <input name="uname" required type="text" />
                        <label for="uname">Phone number, username, or email</label>
                    </div>
                    <div className="form-content">
                        <input name="password" required type="password" />
                        <label for="password">Password</label>
                    </div>
                    <div className="form-content">
                        <button type="submit">Log in</button>
                    </div>
                    <div className="form-ending">
                        <center>
                            <p id="OR">OR</p>
                            <span id="line"></span>
                        </center>
                        <p id="facebook"><i className="fab fa-facebook-square"></i>Login with Facebook</p>
                        <Link to="#" className="forgot-pass">Forgot password?</Link>
                    </div>
                </form>
            </div>
            <div className="mini-box">
                <div className="text">Don't have an account? <Link to="/register">Sign up</Link></div>
            </div>
            <div className="download-section">
                <p>Get the app.</p>
                <div className="images">
                    <Link to="https://imgbb.com/"><img alt="appstore" border="0"
                        src="https://i.ibb.co/5KyMHpd/appstore.png" /></Link>
                    <Link to="https://imgbb.com/"><img alt="playstore"
                        border="0" src="https://i.ibb.co/ZTHhz0b/playstore.png" /></Link>
                </div>
            </div>
        </div>
  )
}

export default InstagramForm