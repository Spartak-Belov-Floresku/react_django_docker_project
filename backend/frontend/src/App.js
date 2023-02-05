import {
  HashRouter,
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
import PaymentScreen from './screens/PaymentScreen'
import PlaceOrderScreen from './screens/PlaceOrderScreen'
import OrderScreen from './screens/OrderScreen'
import UserListScreen from './screens/UserListScreen'
import UserEditScreen from './screens/UserEditScreen'
import ProductListScreen from './screens/ProductListScreen'
import {ProductEditScreen} from './screens/ProductEditScreen'
import OrderListSreen from './screens/OrderListScreen'

function App() {
  return (
    <HashRouter>
      <Header/>
      <main className="py-3">
      <Container>
        <Routes>
          <Route exact path='/' element={<HomeScreen />} />
          <Route path='/:keyword' element={<HomeScreen />} />
          <Route path='/product/:productId' element={<ProductScreen />} />
          <Route exact path='/cart' element={<CartScreen />} />
          <Route path='/cart/:productId/:qty' element={<CartScreen />} />
          <Route exact path='/login' element={<LoginScreen />} />
          <Route exact path='/register' element={<RegisterScreen />} />
          <Route path='/register/:redirect' element={<RegisterScreen />} />
          <Route path='/profile' element={<ProfileScreen />} />
          <Route path='/shipping' element={<ShippingScreen />} />
          <Route path='/payment' element={<PaymentScreen />} />
          <Route path='/placeorder' element={<PlaceOrderScreen />} />
          <Route path='/order/:orderId' element={<OrderScreen />} />

          <Route path='admin/userlist' element={<UserListScreen />} />
          <Route exact path='admin/user/:userId/edit' element={<UserEditScreen />} />

          <Route exact path='/admin/productlist' element={<ProductListScreen/>} />
          <Route path='/admin/product/:productId/edit' element={<ProductEditScreen />} />
          <Route exact path='/admin/orderlist' element={<OrderListSreen/>} />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Container>
      </main>
      <Footer/>
    </HashRouter>
  );
}

export default App;
