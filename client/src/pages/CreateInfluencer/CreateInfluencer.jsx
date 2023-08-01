import React from 'react'
import SideBar from "../../components/SideBar/SideBar.jsx";
import LoggedInUser from "../../components/loggedInUser/loggedInUser.jsx";
import AddInfluencerForm from '../../components/AddInfluencerForm/AddInfluencerForm.jsx';
import "./CreateInfluencer.css"
const CreateInfluencer = () => {
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

            <div className='d-flex flex-wrap influencer_container '>
            <img src='/images/smallpost2@3x.png' style={{ width: "30vw" }} />
            <AddInfluencerForm/>

            </div>

        </div>


    </div>
</section>
  )
}

export default CreateInfluencer