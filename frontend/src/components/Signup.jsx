import React, { useState } from "react";
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';

const Signup = () => {
    const navigate = useNavigate();
    const [formdata, setFormData] = useState({
        email:"",
        first_name:"",
        last_name:"",
        password:"",
        password2:""
    });

    const [error, setError] = useState("");

    const handleChange = (e) => {
        setFormData({...formdata, [e.target.name]: e.target.value})
        // upon value change of any of the stated variables
        // destructure everything with its corresponding name field
        // e.g. setFormData(formdata['email']='email'.target.value)
    };

    const {email, first_name, last_name, password, password2} = formdata;
    // get all the values from formdata (using destructuring) ...
    // so they can be accessed in handleSubmit function

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!email || !first_name || !last_name || !password || !password2) {
            // if any of the fields was not provided, throw error
            setError("All fields are required.");
        } else {
            console.log(formdata);
            // make call to api
            const res = await axios.post("http://127.0.0.1:8000/api/v1/auth/register/", formdata);
            // check response
            const response = res.data;
            console.log(response);
            if (res.status === 201) {
                // redirect to verifyemail component
                navigate("/otp/verify");
                toast.success(response.message);
            } else {
                toast.error(response.message);
            }
        }
    }
    
    return (
        // 05
        <div>
            <div className="form-container">
                <div className="wrapper">
                    <h2>Create Account</h2>
                    <form onSubmit={handleSubmit}>
                    <p style={{color: "red", padding:'1px'}}>{error ? error : ""}</p>
                        <div className="form-group">
                            <label htmlFor="">Email Address:</label>
                            <input type="text" className="email-form" name="email" value={email} onChange={handleChange} />
                        </div>
                        <div className="form-group">
                            <label htmlFor="">First Name:</label>
                            <input type="text" className="email-form" name="first_name" value={first_name} onChange={handleChange} />
                        </div>
                        <div className="form-group">
                            <label htmlFor="">Last Name:</label>
                            <input type="text" className="email-form" name="last_name" value={last_name} onChange={handleChange} />
                        </div>
                        <div className="form-group">
                            <label htmlFor="">Password:</label>
                            <input type="password" className="email-form" name="password" value={password} onChange={handleChange} />
                        </div>
                        <div className="form-group">
                            <label htmlFor="">Password Repeat:</label>
                            <input type="password" className="email-form" name="password2" value={password2} onChange={handleChange} />
                        </div>
                        <input type="submit" value="Submit" className="submitButton" />
                    </form>
                </div>
            </div>
        </div>
    )
};

export default Signup