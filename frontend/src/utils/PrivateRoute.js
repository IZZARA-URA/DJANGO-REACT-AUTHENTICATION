import { Route, Navigate, Routes } from "react-router-dom";
import { useContext } from "react";
import AuthContext from "../context/AuthContext";
import Dashboard from "../views/Dashboard";
import HomePage from "../views/HomePage";

const PrivateRoute = ({children, ...rest}) => {
    let user = useContext(AuthContext)
    return user ? <Navigate to='/homepage'/> : <Navigate to="/login" replace/>;
    
}

export default PrivateRoute
