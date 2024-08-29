import axios from 'axios';
import { jwtDecode } from "jwt-decode";
import dayjs from "dayjs";

// #12

const token = localStorage.getItem('access') ? JSON.parse(localStorage.getItem('access')) : "";
const refresh_token = localStorage.getItem('refresh') ? JSON.parse(localStorage.getItem('refresh')) : "";

const baseUrl = "http://localhost:8000/api/v1";
const axiosInstance = axios.create({
    baseURL: baseUrl,
    'Content-Type': 'application/json',
    headers: {'Authorization': localStorage.getItem('access') ? `Bearer ${token}` : null}
});

axiosInstance.interceptors.request.use(async req => {
    if (token) {
        req.headers.Authorization = `Bearer ${token}`;
        const user = jwtDecode(token)
        const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1;
        if (!isExpired) {
            console.log("[axiosInstance.js]: Token is not expired.");
            return req;
        } else {
            console.log("[axiosInstance.js]: Token is expired. Refreshing now...");
            const res = await axios.post(`${baseUrl}/auth/token/refresh/`, {refresh: refresh_token}).catch((e) => {
                console.log(e);
            });
            console.log(res.data);
            if (res.status === 200) {
                console.log("[axiosInstace.js]: Token successfully refreshed.");
                localStorage.setItem('access', JSON.stringify(res.data.access));
                req.headers.Authorization = `Bearer ${res.data.access}`;
                return req;
            } else {
                console.log("[axiosInstance.js]: Failed to refresh token. logging out...");
                const res = await axios.post(`${baseUrl}/auth/logout`, {"refresh_token": refresh_token}).catch((e) => {
                    console.log(e);
                });
                // the code from handleLogout
                if (res.status === 200) {
                    localStorage.removeItem('access');
                    localStorage.removeItem('refresh');
                    localStorage.removeItem('user');
                    console.log("[axiosInstance.js]: Logout successful.");
                }
            }
        }
    }
    return req;
});

export default axiosInstance