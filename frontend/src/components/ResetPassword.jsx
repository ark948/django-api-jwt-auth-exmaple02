import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';
import { toast } from 'react-toastify';


const ResetPassword = () => {
    const navigate = useNavigate()
    const {uid, token} = useParams()
    const [newpasswords, setNewPasswords] = useState({
        password: "",
        confirm_password: ""
    })

    const handleChange = (e) => {
        setNewPasswords({...newpasswords, [e.target.name]: e.target.value});
    }

    const data = {
        'password': newpasswords.password,
        'confirm_password': newpasswords.confirm_password,
        'uidb64': uid,
        'token': token
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await axiosInstance.patch('/auth/set-new-password/', data)
        const result = response.data
        if (response.status === 200) {
            toast.success(result.message);
            navigate('/login');
        }
        console.log(response);
    }

    return (
        <div>
            <div className='form-container'>
                <div className='wrapper' style={{width: "100%"}}>
                    <h2>Enter your new password:</h2>
                    <form action="" onSubmit={handleSubmit}>
                        <div className='form-group'>
                            <label htmlFor="">New Password:</label>
                            <input type="text" className='email-form' name='password' value={newpasswords.password} onChange={handleChange} />
                        </div>
                        <div className='form-group'>
                            <label htmlFor="">Confirm new password:</label>
                            <input type="text" className='email-form' name='confirm_password' value={newpasswords.confirm_password} onChange={handleChange} />
                        </div>
                        <button type='submit' className='vbtn'>Sumbit</button>
                    </form>
                </div>
            </div>
        </div>
    )
}

export default ResetPassword