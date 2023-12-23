import { createContext, useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode"
import { useNavigate } from "react-router-dom"

const swal = require('sweetalert2')

const AuthContext = createContext()

export default AuthContext


export const AuthProvider = ({ children }) => {
    const [authTokens, setAuthTokens] = useState(() => localStorage.getItem("authTokens") ? JSON.parse(localStorage.getItem("authTokens")) : null)

    const [user, setUser] = useState(() => localStorage.getItem("authTokens") ? JSON.parse(localStorage.getItem("authTokens")) : null)

    const [loading, setLoading] = useState(true)

    const history = useNavigate()

    const loginUser = async (email, password) => {
        const response = await fetch("http://127.0.0.1:8000/api/token/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'Accept' : 'application/json',
                'Authorization' : `Bearer ${authTokens?.access}`
            },
            body: JSON.stringify({
                email, password
            })
        })

        const data = await response.json() 
        console.log(data)

        if (response.status === 200) {
            console.log("Logged In")
            setAuthTokens(data)
            setUser(jwtDecode(data.access))
            localStorage.setItem("authTokens", JSON.stringify(data))
            history("/")
            swal.fire({
                title: "Login Successfull", 
                icon: "success",
                toast: true, 
                timer: 3000,
                position: 'top-right',
                timerProgressBar: true,
                showConfirmButton: false,
            })
        } else {
            console.log(response.status)
            console.log("There was a server issue")
            swal.fire({
                title: "Username or password does not exists", 
                icon: "error",
                toast: true, 
                timer: 3000,
                position: 'top-right',
                timerProgressBar: true,
                showConfirmButton: false,
            })
        }
    }

    const registerUser = async (email, username, password, password2) => {
        const response = await fetch("http://127.0.0.1:8000/api/register/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email, username, password, password2
            })
        })

        if (response.status === 201) { 
            history("/login")
            swal.fire({
                title: "Registration Sucessful, Login Now", 
                icon: "success",
                toast: true, 
                timer: 3000,
                position: 'top-right',
                timerProgressBar: true,
                showConfirmButton: false,
            })
        } else { 
            console.log(response.status)
            console.log("There was a server issue")
            swal.fire({
                title: "An Error Occured " + response.status, 
                icon: "error",
                toast: true, 
                timer: 3000,
                position: 'top-right',
                timerProgressBar: true,
                showConfirmButton: false,
            })
        }
    }

    const logoutUser = () => {
        setAuthTokens(null)
        setUser(null)
        localStorage.removeItem("authTokens")
        history("/login")
        swal.fire({
            title: "You have been logout...", 
            icon: "success",
            toast: true, 
            timer: 3000,
            position: 'top-rigth',
            timerProgressBar: true,
            showConfirmButton: false,
        })
    }

    const contextData = { 
        user,
        setUser,
        authTokens,
        setAuthTokens,
        registerUser,
        loginUser,
        logoutUser,
    }

    useEffect(() => {
        if (authTokens) { 
            setUser(jwtDecode(authTokens.access))
        }

        setLoading(false)
    }, [authTokens, loading])

    return (
        <AuthContext.Provider value={contextData}>
            {loading ? null: children}
        </AuthContext.Provider>
    )

}
