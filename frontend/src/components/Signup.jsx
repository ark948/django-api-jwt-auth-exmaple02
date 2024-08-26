import React, { useState } from "react";

const Signup = () => {
    // 05
    return (
        <div>
            <div className="form-container">
                <div className="wrapper">
                    <h2>Create Account</h2>
                    <form>
                        <div className="form-group">
                            <label htmlFor="">Email Address:</label>
                            <input type="text" className="email-form" name="email" />
                        </div>
                        <div className="form-group">
                            <label htmlFor="">First Name:</label>
                            <input type="text" className="email-form" name="first_name" />
                        </div>
                        <div className="form-group">
                            <label htmlFor="">Last Name:</label>
                            <input type="text" className="email-form" name="last_name" />
                        </div>
                        <div className="form-group">
                            <label htmlFor="">Password:</label>
                            <input type="text" className="email-form" name="password" />
                        </div>
                        <div className="form-group">
                            <label htmlFor="">Password Repeat:</label>
                            <input type="text" className="email-form" name="confirm_password" />
                        </div>
                        <input type="submit" value="Submit" className="submitButton" />
                    </form>
                </div>
            </div>
        </div>
    )
};

export default Signup