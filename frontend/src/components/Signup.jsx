import React, { useState } from "react";

const Signup = () => {
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
    };

    const {email, first_name, last_name, password, password2} = formdata;

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!email || !first_name || !last_name || !password || !password2) {
            // if any of the fields was not provided, throw error
            setError("All fields are required.");
        }
        console.log(formdata);
    }

    
    return (
        // 05
        <div>
            <div className="form-container">
                <div className="wrapper">
                    <h2>Create Account</h2>
                    <p style={{color: "red", padding:'1px'}}>{error ? error : ""}</p>
                    <form onSubmit={handleSubmit}>
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