
import './App.css';
import { BrowserRouter as Router, Route, Routes  } from 'react-router-dom';

import PrivateRoute from './utils/PrivateRoute'
import { AuthProvider } from './context/AuthContext';

import Dashboard from './views/Dashboard';
import HomePage from './views/HomePage';
import LoginPage from './views/LoginPage';
import RegisterPage from './views/RegisterPage';
import NavBar from './views/NavBar';
import Mesaage from './views/Message'
import MessageDetail from './views/MessageDetail';

function App() {
  return (
    <div className="App">
      <Router>
        <AuthProvider>
          <NavBar/>

          <Routes>
            <Route exact path='/' element={<PrivateRoute/>}/>

            <Route Component={LoginPage} path='/login'/>
            <Route Component={RegisterPage} path='/register'/>
            <Route Component={HomePage} path='/homepage'/>
            <Route Component={Dashboard} path='/dashboard'/>

            <Route Component={Mesaage} element={<PrivateRoute/>} exact path='/inbox'/>
            <Route Component={MessageDetail} element={<PrivateRoute/>}  exact path="/inbox/:id"/>
            {/* <Route component={SearchUsers} path="/search/:username" exact /> */}

            <Route path="*" element={<NotFoundPage />} />

          </Routes>
        </AuthProvider>
      </Router>
    </div>
  );
}

export default App;
