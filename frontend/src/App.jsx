import { useState } from 'react'
import { ToastContainer } from 'react-toastify';
import "react-toastify/dist/ReactToastify.css";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Signup, Login, Profile, VerifyEmail, ForgotPassword } from './components'

import './App.css'

function App() {

  return (
    <>
    {/* 01 */}
      <Router>
        <ToastContainer 
          position='top-right'
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme='colored'
        />
          <Routes>
              <Route path='/' element={<Signup />} />
              <Route path='/login' element={<Login />} />
              <Route path='/dashboard' element={<Profile />} />
              <Route path='/otp/verify' element={<VerifyEmail />} />
              <Route path='/forgot_password' element={<ForgotPassword />} />
          </Routes>
      </Router>
    </>
  )
}

export default App
