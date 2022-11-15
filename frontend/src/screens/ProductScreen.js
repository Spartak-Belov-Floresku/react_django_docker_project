import { useEffect, useState } from 'react'
import { Link, useParams, useNavigate } from 'react-router-dom'
import { Row, Col, Image, ListGroup, Button, Card, Form } from 'react-bootstrap'
import Rating from '../components/Rating'

import products from '../products'

export default function ProductScreen() {

    const [qty, setQty] = useState(1)
    const { productId } = useParams()

    const product = products.find(p => p._id === productId)
    
    return (
        <div className='opacity'>
            <Link to='/' className='btn btn-light my-3 rounded boxshadow'>Go Back</Link>
            <Row>
                              
            <Col md={6}>
                <Image src={product.image} alt={product.name} fluid className='boxshadow mb-3 rounded'/>
            </Col>

            <Col md={3}>
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

            <Col md={3}>

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
