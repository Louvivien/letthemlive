import React, { useState } from "react";
import "./AddInfluencerForm.css";
const AddInfluencerForm = () => {
  const [influencerDetails, setinfluencerDetails] = useState({
    full_name: "",
    insta_username: "",
    insta_password: "",
    gender: "",
    description: "",
  });

  const handleChange = (e) => {
    setinfluencerDetails((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleCreateInfluencer = (e) => {
    e.preventDefault();
    // API for adding influencer to DB
  };
  return (
    <div className="create_influencer_form_container">
      <h5 className="create_influencer_main_heading">Create New Influencer!</h5>
      <form onSubmit={handleCreateInfluencer}>
        <div>
          <input
            type="text"
            id="full_name"
            name="full_name"
            value={influencerDetails.full_name}
            onChange={handleChange}
            className="input_field_create_influencer input_field"
            placeholder="Enter Full Name"
            required
          />
        </div>
        <div>
          <input
            type="text"
            id="insta_username"
            name="insta_username"
            value={influencerDetails.insta_username}
            onChange={handleChange}
            className="input_field_create_influencer input_field"
            placeholder="Enter Instagram Username"
            required
          />
        </div>
        <div>
          <input
            type="password"
            id="insta_password"
            name="insta_password"
            value={influencerDetails.insta_password}
            className="input_field_create_influencer input_field"
            onChange={handleChange}
            placeholder="Enter Instagram Password"
            required
          />
        </div>
        <div>
          <input
            type="text"
            id="description"
            name="description"
            value={influencerDetails.description}
            className="input_field_create_influencer input_field"
            onChange={handleChange}
            placeholder="Enter description"
            required
          />
        </div>
        <div className="">
          <span>
            <input
              type="radio"
              name="gender"
              value="male"
              className="input_field_create_influencer"
              onChange={handleChange}
            />
            Male
          </span>
          <span>
            <input
              type="radio"
              name="gender"
              value="female"
              className="input_field_create_influencer"
              onChange={handleChange}
            />
            Female
          </span>
        </div>

        <button type="submit" className="btn btn-primary add_influencer_btn">
          Create Influencer
        </button>
      </form>
    </div>
  );
};

export default AddInfluencerForm;
