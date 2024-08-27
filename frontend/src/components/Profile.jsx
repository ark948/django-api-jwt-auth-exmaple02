import React, { useEffect } from "react";
import { useNavigate } from 'react-router-dom';

const Profile = () => {
    // #11
    // reminder: useEffect allows for some side code to run upon a render (dependancy)
    const navigate = useNavigate()
    const user = JSON.parse(localStorage.getItem('user'));
    const jwt_access = localStorage.getItem('access');

    useEffect(() => {
        if (jwt_access === null && !user) {
            navigate('/login')
        }
    }, []);

    return (
        <div className="container">
            <h2>hi {user && user.names}</h2>
            <p style={{textAlign: "center"}}>welcome to your profile</p>
            <button className="logout-btn">Logout</button>
        </div>
    );
};

export default Profile