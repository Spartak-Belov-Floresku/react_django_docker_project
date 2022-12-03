import { useDispatch, useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import { Navbar, Nav, Container, NavDropdown, } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'
import { logout } from '../actions/userActions'
import SearchBox from './SearchBox'

export default function Header() {

    const navigate = useNavigate()
    const { userInfo } = useSelector(state => state.userLogin)
    const { cartItems } = useSelector(state => state.cart)

    const dispatch = useDispatch()

    const logoutHandler = () => {
        dispatch(logout())
        navigate('/login')
    }

    return (
        <header className='mb-3 pb-5'>
            <Navbar
                bg="dark"
                variant='dark'
                expand="lg"
                className="text-uppercase boxshadow"
                fixed="top"
                collapseOnSelect
            >
                <Container>
                    <LinkContainer to='/'>
                        <Navbar.Brand>Game Land</Navbar.Brand>
                    </LinkContainer>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                    <SearchBox/>
                    <Nav className="ms-auto">
                        <LinkContainer to='/cart'>
                            <Nav.Link>{cartItems.length? `(${cartItems.length})`:''} <i className='fas fa-shopping-cart'></i> Cart</Nav.Link>
                        </LinkContainer>

                        {userInfo ? (
                            <NavDropdown title={userInfo.name} id='username'>

                                <LinkContainer to='/profile'>
                                    <NavDropdown.Item>Profile</NavDropdown.Item>
                                </LinkContainer>

                                <NavDropdown.Item onClick={logoutHandler}>Logout</NavDropdown.Item>

                            </NavDropdown>
                        ) : (
                            <LinkContainer to='/login'>
                                <Nav.Link><i className='fas fa-user'></i> Login</Nav.Link>
                            </LinkContainer>
                        )}

                        {userInfo && userInfo.isAdmin && (
                            <NavDropdown title='Admin' id='adminmenu'>

                                <LinkContainer to='/admin/userlist'>
                                    <NavDropdown.Item>Users</NavDropdown.Item>
                                </LinkContainer>

                                <LinkContainer to='/admin/productlist'>
                                    <NavDropdown.Item>Products</NavDropdown.Item>
                                </LinkContainer>

                                <LinkContainer to='/admin/orderlist'>
                                    <NavDropdown.Item>Orders</NavDropdown.Item>
                                </LinkContainer>

                            </NavDropdown>
                        )}

                    </Nav>

                    </Navbar.Collapse>
                </Container>
            </Navbar>
        </header>
    )
}