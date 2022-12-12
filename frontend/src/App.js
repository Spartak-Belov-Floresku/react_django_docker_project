import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate
} from 'react-router-dom'
import {Container} from 'react-bootstrap'

import Header from './components/Header'
import Footer from './components/Footer'

import HomeScreen from './screens/HomeScreen'
import ProductScreen from './screens/ProductScreen'
import CartScreen from './screens/CartScreen'
import LoginScreen from './screens/LoginScreen'
import RegisterScreen from './screens/RegisterScreen'
import ProfileScreen from './screens/ProfileScreen'
import ShippingScreen from './screens/ShippingScreen'

function App() {
  return (
    <Router>
      <Header/>
      <main className="py-3">
      <Container>
        <Routes>
          <Route exact path='/' element={<HomeScreen />} />
          <Route path='/product/:productId' element={<ProductScreen />} />
          <Route exact path='/cart' element={<CartScreen />} />
          <Route path='/cart/:productId/:qty' element={<CartScreen />} />
          <Route exact path='/login' element={<LoginScreen />} />
          <Route exact path='/register' element={<RegisterScreen />} />
          <Route path='/register/:redirect' element={<RegisterScreen />} />
          <Route path='/profile' element={<ProfileScreen />} />
          <Route path='/shipping' element={<ShippingScreen />} />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Container>
      </main>
      <Footer/>
    </Router>
  );
}

export default App;
