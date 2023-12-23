
import './App.css';
import { BrowserRouter as Router, Route, Routes  } from 'react-router-dom';

import PrivateRoute from './utils/PrivateRoute'
import { AuthProvider } from './context/AuthContext';

import Dashboard from './views/Dashboard';
import HomePage from './views/HomePage';
import LoginPage from './views/LoginPage';
import RegisterPage from './views/RegisterPage';
import NavBar from './views/NavBar';

function App() {
  return (
    <div className="App">
      <Router>
        <AuthProvider>
          <NavBar/>

          <Routes>
            <Route exact path='/' element={<PrivateRoute/>}/>
            <Route Component={LoginPage} path='/login'/>
            <Route exact Component={RegisterPage} path='/register'/>
            <Route exact Component={HomePage} path='/homepage'/>
            <Route exact Component={Dashboard} path='/dashboard'/>
          </Routes>
        </AuthProvider>
      </Router>
    </div>
  );
}

export default App;
