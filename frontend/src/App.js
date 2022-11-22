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
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Container>
      </main>
      <Footer/>
    </Router>
  );
}

export default App;
