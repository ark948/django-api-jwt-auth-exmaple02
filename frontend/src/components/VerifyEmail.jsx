import React, { useState } from "react";
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';

const VerifyEmail = () => {
    // 06
    // 09
    const [otp, setOtp] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (otp) {
            const response = await axios.post("http://127.0.0.1:8000/api/v1/auth/verify-email/", {'otp': otp});
            if (response.status === 200) {
                navigate("/login");
                toast.success(response.data.message);
            } else {
                toast.error(response.data.message);
            }
        }
    }

    return (
        <div>
            <div className="form-container">
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="">Enter your OTP code:</label>
                        <input type="text" className="email-form" name="otp" value={otp} onChange={(e) => setOtp(e.target.value)}/>
                    </div>
                    <input type="submit" className="vbtn" value="Send"/>
                </form>
            </div>
        </div>
    )
};

export default VerifyEmail