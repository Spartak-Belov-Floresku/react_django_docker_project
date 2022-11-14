import {Container, Navbar, Nav, Row} from 'react-bootstrap'

export default function Header() {
  return (
    <header>
    <Navbar bg="light" expand="lg" collapseOnSelect fixed="top">
        <Container>
            <Navbar.Brand href="/">Play Game Ecommerce</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="ms-auto">
                    <Nav.Link href="/cart"><i className="fas fa-shopping-cart"></i>Cart</Nav.Link>
                    <Nav.Link href="/login"><i className="fas fa-user"></i>Login</Nav.Link>
                </Nav>
            </Navbar.Collapse>
        </Container>
    </Navbar>
    </header>
  )
}
