import {useEffect} from 'react'
import { Link, useParams, useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { Row, Col, ListGroup, Image, Form, Button, Card } from 'react-bootstrap'
import  Message  from '../components/Message'
import { addToCart, removeFromCart } from '../actions/cartActions'

export default function CartScreen() {
  let { productId, qty } = useParams()
  const navigate = useNavigate()
  qty = qty == 0? 1: qty;

  const dispatch = useDispatch()

  const { cartItems } = useSelector(state => state.cart)

  useEffect(() => {
    if(productId){
      dispatch(addToCart(productId, qty))
    }else if(cartItems){
      cartItems.map(item => dispatch(addToCart(item.product, item.qty)))
    }
  }, [dispatch, productId, qty])

  const removeFromCartHandler = id => {
    dispatch(removeFromCart(id))
  }

  const checkOutHandler = () => {
    navigate('/shipping')
  }

  return (
    <Row className='opacity'>
      <Col md={8}>
        <h1>Shopping Cart</h1>
        {!cartItems.length? (
          <Message variant='info'>
            Your cart is empty <Link to='/'>Go Back</Link>
          </Message>
        ) : (
          <ListGroup variant='flush'>
              {cartItems.map(item=>
                (
                  <ListGroup.Item key={item.product}>
                    <Row>
                      <Col md={2}>
                        <Image src={item.image} alt={item.name} fluid rounded className='boxshadow mb-2'/>
                      </Col>
                      <Col md={3} className='mb-2'>
                        <Link to={`/product/${item.product}`}>{item.name}</Link>
                      </Col>
                      <Col md={2}>
                        ${item.price}
                      </Col>
                      <Col md={3} className='mb-2'>
                        <Form.Control
                          as="select"
                          value={item.qty}
                          onChange={e=> dispatch(addToCart(item.product, Number(e.target.value)))}
                        >
                          {
                            [...Array(item.countInStock).keys()]
                                  .map((e,i) => (i < 5)
                                      ?(
                                          <option key={i} value={i+1}>
                                            {i+1}
                                          </option>
                                      )
                                    : '')
                          }
                        </Form.Control>
                      </Col>
                      <Col md={1}>
                        <Button
                          type='button'
                          variant='light'
                          onClick={() => removeFromCartHandler(item.product)}
                        >
                          <i className='fas fa-trash'></i>
                        </Button>
                      </Col>
                    </Row>
                  </ListGroup.Item>
                ))}
          </ListGroup>
        ) }
      </Col>
      <Col md={4}>
        <Card>

          <ListGroup variant='flush'>
            <ListGroup.Item>
              <h4>Subtotal Items({cartItems.reduce((acc,item) => acc + item.qty, 0)})</h4>
              ${cartItems.reduce((acc,item) => acc + item.qty*item.price, 0).toFixed(2)}
            </ListGroup.Item>
          </ListGroup>

          <ListGroup.Item className='p-2'>
            <Button
              onClick={checkOutHandler}
              className='btn-block bg-dark'
              style={{width: '100%'}}
              type='button'
              disabled={!cartItems.length}>
                Proceed to Checkout
            </Button>
          </ListGroup.Item>

        </Card>
      </Col>
    </Row>
  )
}