import React, { useState } from "react";

const VerifyEmail = () => {
    // 06
    return (
        <div>
            <div className="form-container">
                <form action="">
                    <div className="form-group">
                        <label htmlFor="">Enter your OTP code:</label>
                        <input type="text" className="email-form" name="otp"/>
                    </div>
                    <input type="submit" className="vbtn" value="Send"/>
                </form>
            </div>
        </div>
    )
};

export default VerifyEmail