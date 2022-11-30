import '../css/product.css'
import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Link, useParams, useNavigate } from 'react-router-dom'
import { Row, Col, ListGroup, Button, Card, Form } from 'react-bootstrap'
import ReactImageMagnify from 'react-image-magnify'
import Rating from '../components/Rating'
import { listProductDetails } from '../actions/productActions'
import Loader from '../components/Loader'
import Message from '../components/Message'

export default function ProductScreen() {

    const [qty, setQty] = useState(1)
    const { productId } = useParams()
    const navigate = useNavigate()

    const dispatch =  useDispatch()

    let { error, loading, product } = useSelector( state => state.productDetails )

    if(!error && 'id' in product && product.id != productId ){
        product = {}
        loading = true
        console.log('Id trigeg')
    }

    useEffect(() => { dispatch(listProductDetails(productId)) }, [productId])

    const addToCartHandler = () => { navigate(`/cart/${productId}/${qty}`)}

    return (
        loading ?   <Loader/>
        : error ?   <Message variant='danger'>{error}</Message>
                :   <div className='opacity'>
                        <Link to='/' className='btn btn-light my-3 rounded boxshadow'>Go Back</Link>
                        <Row>

                        <Col md={6} className='imageZoom'>
                                      <ReactImageMagnify {...{
                                          smallImage: {
                                            src: `${product.image}`,
                                            alt: product.name,
                                            isFluidWidth: true,
                                          },
                                          largeImage: {
                                            src: `${product.image}`,
                                            width: 1000,
                                            height: 900,
                                            opacity:'.15s',
                                          }
                                      }} />
                        </Col>

                        <Col md={3} className='siblingOne'>
                            <ListGroup variant='flush'>

                                <ListGroup.Item>
                                <h5><strong>{product.name}</strong></h5>
                                </ListGroup.Item>

                                <ListGroup.Item>
                                <Rating
                                    value={product.rating}
                                    text={`${product.numReviews}
                                    review${product.numReviews > 1?'s':''}`} color={'#f8e825'}
                                />
                                </ListGroup.Item>

                                <ListGroup.Item>
                                <strong>Price:</strong> ${product.price}
                                </ListGroup.Item>

                                <ListGroup.Item>
                                <strong>Description:</strong> {product.description}
                                </ListGroup.Item>

                            </ListGroup>
                        </Col>

                        <Col md={3} className='siblingTwo'>

                            <Card>
                                <ListGroup variant='flush'>

                                <ListGroup.Item>
                                    <Row>
                                    <Col>Price:</Col>
                                    <Col>${product.price}</Col>
                                    </Row>
                                </ListGroup.Item>

                                <ListGroup.Item>
                                    <Row>
                                    <Col>Status:</Col>
                                    <Col>{product.countInStock?'In stock':'Out of stock'}</Col>
                                    </Row>
                                </ListGroup.Item>

                                {product.countInStock > 0 && (
                                    <ListGroup.Item>
                                    <Row>
                                        <Col>Qty:</Col>
                                        <Col xs='auto' className='my-1'>
                                        <Form.Control
                                            as="select"
                                            value={qty}
                                            onChange={e=>setQty(e.target.value)}
                                        >
                                            {
                                            [...Array(product.countInStock).keys()]
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
                                    </Row>
                                    </ListGroup.Item>
                                )}

                                <ListGroup.Item>
                                    <Button
                                        onClick={addToCartHandler}
                                        className='btn-block bg-dark'
                                        style={{width: '100%'}}
                                        type='button'
                                        disabled={!product.countInStock}
                                    >
                                        Add to cart
                                    </Button>
                                </ListGroup.Item>

                                </ListGroup>
                            </Card>

                        </Col>

                        </Row>

                    </div>

    )
}
