import React, {useState} from "react";
import axiosInstance from "../utils/axiosInstance";
import { toast } from "react-toastify";
import axios from "axios";

const ForgotPassword = () => {
    const [email, setEmail] = useState(" ");

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (email) {
            const res = await axiosInstance.post("/auth/password-reset/", {"email": email});
            if (res.status == 200) {
                toast.success("Reset link has been sent to your email.");
            }
            console.log(res);
            setEmail("");
        }
    }

    return (
        <div>
            <h2>Enter your email to reset your password:</h2>
            <div className="wrapper">
                <form action="" onSubmit={handleSubmit}>
                    <div className="form-group">
                    <label htmlFor="">Email Address:</label>
                    <input type="text" className="email-form" name="email" value={email} onChange={(e) => setEmail(e.target.value)}/>
                    </div>
                    <button className="vbtn">Send request</button>
                </form>
            </div>
        </div>
    )
};

export default ForgotPassword