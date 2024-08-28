import React, { useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';
import { toast } from 'react-toastify';
import axios from "axios";

const Profile = () => {
    // #11
    // reminder: useEffect allows for some side code to run upon a render (dependancy)
    const navigate = useNavigate()
    const user = JSON.parse(localStorage.getItem('user'));
    const jwt_access = localStorage.getItem('access');

    useEffect(() => {
        // upon change in value of access token and user, 
        // check if access token or user data exists
        // if not, redirect to login, since this page is protected
        // if yes, try to get some data from protected backend view
        if (jwt_access === null && !user) {
            navigate('/login')
        } else {
            getSomeData();
        }
    }, [jwt_access, user]);

    const refresh = JSON.parse(localStorage.getItem('refresh'));

    const getSomeData = async () => {
        const resp = await axiosInstance.get('/auth/profile');
        if (resp.status === 200) {
            console.log(resp.data);
        }
    }

    const handleLogout = async () => {
        const res = await axiosInstance.post("/auth/logout/", {"refresh_token": refresh})
        if (res.status === 204) {
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            localStorage.removeItem('user');
            navigate("/login");
            toast.success('logout successful');
        }
    }

    return (
        <div className="container">
            <h2>hi {user && user.names}</h2>
            <p style={{textAlign: "center"}}>welcome to your profile</p>
            <button onClick={handleLogout} className="logout-btn">Logout</button>
        </div>
    );
};

export default Profile