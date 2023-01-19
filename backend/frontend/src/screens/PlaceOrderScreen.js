import {useEffect} from 'react'
import {Row, Col, ListGroup, Image, Card, Button} from 'react-bootstrap'
import {Link, useNavigate} from 'react-router-dom'
import {useDispatch, useSelector} from 'react-redux'
import Message from '../components/Message'
import CheckoutSteps from '../components/CheckoutSteps'
import {createOrder} from '../actions/orderActions'
import {ORDER_CREATE_RESET} from '../constants/orderConstants'
import { logout, getUserDetails } from '../actions/userActions'

export default function PlaceOrderScreen() {

    const navigate = useNavigate()

    const {order, error, success} = useSelector(state => state.orderCreate)

    const dispatch = useDispatch()

    const cart = useSelector(state => state.cart)

    const { userInfo } = useSelector(state => state.userLogin)
    const { user: userProfile, error: errorProfile } = useSelector(state => state.userDetails)

    cart.itemsPrice = (cart.cartItems.reduce((acc, item) => acc + item.price * item.qty, 0)).toFixed(2)
    cart.shippingPrice = (cart.itemsPrice > 100? 0 : 10).toFixed(2)
    cart.totalPrice = (Number(cart.itemsPrice) + Number(cart.shippingPrice)).toFixed(2)

    useEffect(() => {

        if(success){
            dispatch({type: ORDER_CREATE_RESET});
            navigate(`/order/${order.id}`);
        }

        if(!cart.paymentMethod){
            navigate('/payment');
        }

        if(!userInfo){
            navigate(`/login/placeorder`);
        }else if(userInfo){
            if(!userProfile || !userProfile.name || userInfo.id !== userProfile.id)
                dispatch(getUserDetails('profile'))
            if(errorProfile == 'Given token not valid for any token type')
                dispatch(logout())
        }

    }, [dispatch, userInfo, userProfile, success])

    const placeOrder = () => {
       dispatch(createOrder({
        orderItems: cart.cartItems,
        shippingAddress: cart.shippingAddress,
        paymentMethod: cart.paymentMethod,
        itemsPrice: cart.itemsPrice,
        shippingPrice: cart.shippingPrice,
        totalPrice: cart.totalPrice,
       })) 
    }
    return (
        <>
            <CheckoutSteps step1 step2 step3 step4 />
            <Row className='opacity'>
                <Col md={8}>
                    <ListGroup variant='flush'>
                        <ListGroup.Item>
                            <h4>Shipping</h4>
                            <div>
                                <strong>Shipping: </strong>
                                {cart.shippingAddress.address}, {cart.shippingAddress.city}
                                {' '}
                                {cart.shippingAddress.zipCode}
                            </div>
                        </ListGroup.Item>
                
                        <ListGroup.Item>
                            <h4>Payment Method</h4>
                            <div>
                                <strong>Method: </strong>
                                {cart.paymentMethod}
                            </div>
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <h4>Order Items</h4>
                            <div>
                                {
                                    !cart.cartItems.length ?
                                        <Message variant='info'>
                                            Your cart is empty
                                        </Message> : (
                                            <ListGroup variant='flush'>
                                                {cart.cartItems.map((item, index) => (
                                                    <ListGroup.Item key={index}>
                                                        <Row>
                                                            <Col md={1}>
                                                                <Image src={item.image} alt={item.name} fluid rounded /> 
                                                            </Col>
                                                            <Col>
                                                                <Link to={`/product/${item.product}`}>{item.name}</Link>
                                                            </Col>
                                                            <Col md={4}>
                                                                {item.qty} x ${item.price} = ${(item.qty * item.price).toFixed(2)}
                                                            </Col>
                                                        </Row>
                                                    </ListGroup.Item>
                                                ))}
                                            </ListGroup>
                                        )
                                }
                            </div>
                        </ListGroup.Item>
                    </ListGroup>
                </Col>

                <Col md={4}>
                    <Card>
                        <ListGroup variant='flush'>
                            <ListGroup.Item>
                                <h3>Order Summary</h3>
                            </ListGroup.Item>
                            <ListGroup.Item>
                                <Row>
                                    <Col>Item{cart.cartItems.length>1?'s':''}:</Col>
                                    <Col>${cart.itemsPrice}</Col>
                                </Row>
                            </ListGroup.Item>
                            <ListGroup.Item>
                                <Row>
                                    <Col>Shipping:</Col>
                                    <Col>${cart.shippingPrice}</Col>
                                </Row>
                            </ListGroup.Item>
                            <ListGroup.Item>
                                <Row>
                                    <Col>Total:</Col>
                                    <Col>${cart.totalPrice}</Col>
                                </Row>
                            </ListGroup.Item>

                            {error && <ListGroup.Item><Message varian='danger'>{error}</Message></ListGroup.Item>}

                            <ListGroup.Item className='p-2'>
                                <Button
                                    type='button'
                                    className='btn-block'
                                    disabled={!cart.cartItems}
                                    style={{width: '100%'}} 
                                    onClick={placeOrder}
                                >
                                    Place Order
                                </Button>
                            </ListGroup.Item>
                        </ListGroup>
                    </Card>
                </Col>
            </Row>
        </>
    )
}