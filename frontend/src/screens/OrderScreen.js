import {useState, useEffect} from 'react'
import {Row, Col, ListGroup, Image, Card, Button} from 'react-bootstrap'
import {Link, useNavigate, useParams} from 'react-router-dom'
import { PayPalButton } from 'react-paypal-button-v2'
import {useDispatch, useSelector} from 'react-redux'
import Message from '../components/Message'
import Loader from '../components/Loader'
import { getOrderDetails, payOrder, deliverOrder } from '../actions/orderActions'
 import { ORDER_PAY_RESET, ORDER_DELIVER_RESET } from '../constants/orderConstants'

export default function OrderScreen() {

    const { orderId } = useParams()
    const dispatch = useDispatch()

    const [sdkReady, setSdkReady] = useState(false)

    const navigate = useNavigate()

    const {loading, order, error} = useSelector(state => state.orderDetails)
    const {loading: loadingPay, success: successPay } = useSelector(state => state.orderPay)
    const {loading: loadingDeliver, success: successDeliver } = useSelector(state => state.orderDeliver)
    const { userInfo } = useSelector(state => state.userLogin)

    if(!loading && !error){
        order.itemsPrice = order.orderItems.reduce((acc, item) => acc + item.qty*item.price, 0).toFixed(2)
    }

    const addPayPalScript = () => {
        const script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = 'https://www.paypal.com/sdk/js?client-id=AeZBQbX98l0CsmyvcPbBdR_JIB8gu8NRTmu-OQWAN45zdyT3dyNUJ3gis7ZzetfNMzvuWgwPkzFkVuDX'
        script.async = true;
        script.onload = () => {setSdkReady(true)}
        document.body.appendChild(script);
    }

    useEffect(() => {

        if(!userInfo){
            navigate(`/login/order`);
        }

        if(!order || successPay || order.id !== Number(orderId) || successDeliver){
            dispatch({type: ORDER_PAY_RESET})
            dispatch({type: ORDER_DELIVER_RESET})
            dispatch(getOrderDetails(orderId))
        }else if(!order.isPaid){
            if(!window.paypal){
                addPayPalScript()
            }else(
                setSdkReady(true)
            )
        }

    }, [dispatch, userInfo, order, orderId, successPay, successDeliver])

    const successPaymentHandler = paymentResult => {dispatch(payOrder(orderId, paymentResult))}
    const deliverHandler = () => {dispatch(deliverOrder(order))}

    return loading?
    (
        <Loader />
    ): error ? (
        <Message variant='danger'>{error}</Message>
    ):(
        <>  <h3>Order #{order.id}</h3>
            <Row className='opacity'>
                <Col md={8}>
                    <ListGroup variant='flush'>
                        <ListGroup.Item>
                            <h4>Shipping</h4>
                            <div><strong>Name:</strong> {order.user.name}</div>
                            <div><strong>Email:</strong> <a href={`mailto:${order.user.email}`}>{order.user.email}</a></div>
                            <div>
                                <strong>Shipping: </strong>
                                {order.shippingAddress.address}, {order.shippingAddress.city}
                                {' '}
                                {order.shippingAddress.zipCode}
                            </div>
                            {order.isDelivered ? (
                                <Message variant='success'>Delivered on {order.deliveredAt.substring(0, 10)}</Message>
                            ) : (
                                <Message variant='warning'>Not Delivered</Message>
                            )}
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <h4>Payment Method</h4>
                            <div>
                                <strong>Method: </strong>
                                {order.paymentMethod}
                            </div>
                            {order.isPaid ? (
                                <Message variant='success'>Paid on {order.paidAt.substring(0, 10)}</Message>
                            ) : (
                                <Message variant='warning'>Not Paid</Message>
                            )}
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <h4>Order Items</h4>
                            <div>
                                {
                                    !order.orderItems.length ?
                                        <Message variant='info'>
                                            Order is empty
                                        </Message> : (
                                            <ListGroup variant='flush'>
                                                {order.orderItems.map((item, index) => (
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
                                    <Col>Item{order.orderItems.length>1?'s':''}:</Col>
                                    <Col>${order.itemsPrice}</Col>
                                </Row>
                            </ListGroup.Item>
                            <ListGroup.Item>
                                <Row>
                                    <Col>Shipping:</Col>
                                    <Col>${order.shippingPrice}</Col>
                                </Row>
                            </ListGroup.Item>
                            <ListGroup.Item>
                                <Row>
                                    <Col>Total:</Col>
                                    <Col>${order.totalPrice}</Col>
                                </Row>
                            </ListGroup.Item>
                            {!order.isPaid && (
                                <ListGroup.Item>
                                    {loadingPay && <Loader/>}
                                    {!sdkReady? (
                                        <Loader/>
                                    ) : (
                                        <PayPalButton
                                            amount={order.totalPrice}
                                            onSuccess={successPaymentHandler}
                                        />
                                    )}
                                </ListGroup.Item>
                            )}
                        </ListGroup>
                        {loadingDeliver && <Loader/>}
                        {userInfo && userInfo.isAdmin && order.isPaid && !order.isDelivered && (
                            <ListGroup.Item>
                                <Button
                                    type='button'
                                    className='btn btn-block'
                                    style={{width: '100%'}}
                                    onClick={deliverHandler}
                                >
                                    Mark as Deliver
                                </Button>
                            </ListGroup.Item>
                        )}
                    </Card>
                </Col>
            </Row>
        </>
    )
}