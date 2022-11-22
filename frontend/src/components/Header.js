import { useDispatch, useSelector } from 'react-redux'
import {Container, Navbar, Nav} from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'

export default function Header() {

  const { cartItems } = useSelector(state => state.cart)

  return (
    <header className='mb-3 pb-5'>
    <Navbar bg="light" expand="lg" collapseOnSelect fixed="top">
        <Container>
            <LinkContainer to='/'>
              <Navbar.Brand>Play Game Ecommerce</Navbar.Brand>
            </LinkContainer>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="ms-auto">
                  <LinkContainer to='/cart'>
                    <Nav.Link>{cartItems.length? `(${cartItems.length})`:''} <i className="fas fa-shopping-cart"></i>Cart</Nav.Link>
                  </LinkContainer>
                  <LinkContainer to='/login'>
                    <Nav.Link href="/login"><i className="fas fa-user"></i>Login</Nav.Link>
                  </LinkContainer>
                </Nav>
            </Navbar.Collapse>
        </Container>
    </Navbar>
    </header>
  )
}
