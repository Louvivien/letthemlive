import React from 'react'
import InstagramForm from "../../components/InstagramForm/InstagramForm.jsx";
import TwitterForm from "../../components/TwitterForm/TwitterForm.jsx";
import SideBar from "../../components/SideBar/SideBar.jsx";
import LoggedInUser from "../../components/loggedInUser/loggedInUser.jsx";
import "./Auth.css"
const Auth = () => {
    return (
        <section>
            <div className='dashboard-container'>
                <div className='sidebar-section'>
                    <SideBar />
                </div>

                <div className='influencer-section container'>
                    <div className="loggedInUser">

                        <LoggedInUser />
                    </div>
                    <div class="flex1">
                        <h3 class="ele1">Your Virtual Influencer: Sandra Lane LIVE</h3>
                    </div>
                    <div class="flex2">
                        <div class="inside-flex">
                            <div class="main_container  box1">
                                <h3 class="dm-sans-paragraph inlogin ">
                                    Login into your
                                    Instagram account
                                </h3>
                            </div>
                            <div class="main_container  ">
                                <div class="container">
                                    <div class="col content">
                                        <InstagramForm />
                                    </div>

                                </div>

                            </div>
                        </div>
                        <div class="inside-flex">
                            <div class="main_container  box1">
                                <h3 class="dm-sans-paragraph inlogin ">
                                    Login into your <br /> Twitter account
                                </h3>
                            </div>
                            <div class="main_container  ">
                                <div class="container">
                                    <div class="col content">
                                        <TwitterForm />
                                    </div>

                                </div>

                            </div>
                        </div>



                    </div>
                </div>
            </div>
        </section>
    )
}

export default Auth