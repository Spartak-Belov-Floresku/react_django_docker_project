import {useEffect, useState} from 'react'
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

function App() {
  return (
    <Router>
      <Header/>
      <main className="py-3">
      <Container>
        <Routes>
          <Route exact path='/' element={<HomeScreen />} />
          <Route path='/product/:productId' element={<ProductScreen />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Container>
      </main>
      <Footer/>
    </Router>
  );
}

export default App;
