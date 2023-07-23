import React,{useState,useEffect} from 'react'
import InCard from '../InfluencerCard/InCard.jsx'
import "./Influencer.css"
const Influencer = () => {
  // Extract influencers data from database
  const [InfluencerInfoApi, setInfluencerInfoApi] = useState([])

  useEffect(() => {
   const InfluAPI=[
    {
      name:"Javier Sands",
      title:"Running",
      image:"/images/photo1.svg",
      facebookPostsCount:3540,
      instagramPostsCount:5000,
      twitterPostsCount:1000
    },
    {
      name:"Amanda Peek",
      title:"Running",
      image:"/images/photo2.svg",
      facebookPostsCount:10000,
      instagramPostsCount:4000,
      twitterPostsCount:4520
    },
    {
      name:"Sandra Lane",
      title:"Running",
      image:"/images/photo3.svg",
      facebookPostsCount:5034,
      instagramPostsCount:20030,
      twitterPostsCount:3020
    }
  ]

  setInfluencerInfoApi(InfluAPI);
  }, [])
  

  return (
    <div className='influencers-container'>
      <h2 className='influencer-head'>Your Virtual Influencers</h2>
      <div className='virtual-Influencers'>
        {
          InfluencerInfoApi.map((inf,index)=>{
            return(
              <InCard  influencer={inf} />
            )
          })
        }
      </div>
    </div>
  )
}

export default Influencer;