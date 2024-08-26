import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Signup, Login, Profile, VerifyEmail, ForgotPassword } from './components'

import './App.css'

function App() {

  return (
    <>
    {/* 01 */}
      <Router>
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
