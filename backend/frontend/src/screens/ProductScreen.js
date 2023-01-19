import '../css/product.css'
import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Link, useParams, useNavigate } from 'react-router-dom'
import { Row, Col, ListGroup, Button, Card, Form } from 'react-bootstrap'
import ReactImageMagnify from 'react-image-magnify'
import Rating from '../components/Rating'
import { listProductDetails, createProductReview } from '../actions/productActions'
import Loader from '../components/Loader'
import Message from '../components/Message'
import { PRODUCT_CREATE_REVIEW_RESET } from '../constants/productConstants'


export default function ProductScreen() {

  const { productId } = useParams()
  const navigate = useNavigate()

  const [qty, setQty] = useState(1)
  const [rating, setRating] = useState(0)
  const [comment, setComment] = useState('')
  const [reviewExist, setReviewExist] = useState(false)

  const dispatch =  useDispatch()

  let { loading, product, error } = useSelector( state => state.productDetails )
  let { userInfo } = useSelector( state => state.userLogin )
  let {
    loading: loadingProductReview,
    success: successProductReview,
    error: errorProductReview
  } = useSelector( state => state.productReviewCreate )


  if(!error && 'id' in product && product.id != productId ){
    product = {}
    loading = true
  }

  useEffect(() => {

    dispatch({type: PRODUCT_CREATE_REVIEW_RESET})
    dispatch(listProductDetails(productId))

    if(successProductReview){
      setRating(0)
      setComment('')
    }

    if(typeof product === 'object' && Object.keys(product).length){
      if(product.reviews){
          product.reviews.map(review => {
            if(userInfo){
              if(review.name == userInfo.name){
                setReviewExist(true)
              }
            }
          })
      }
    }

  }, [dispatch, productId, successProductReview, loading])

  const addToCartHandler = () => { navigate(`/cart/${productId}/${qty}`)}

  const submitHandler = e =>{
    e.preventDefault()
    dispatch(createProductReview(
      productId,
      {rating, comment}
    ))
  }

  return (
            loading ? <Loader/>
                    : error ? <Message variant='danger'>{error}</Message>
                            : <div className='opacity'>
                                <Button onClick={() => navigate(-1)} className='btn btn-light my-3 rounded boxshadow'>Go Back</Button>
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
                                                disabled={!product.countInStock}>
                                                    Add to cart
                                                </Button>
                                            </ListGroup.Item>

                                            </ListGroup>
                                        </Card>
                                    </Col>
                                </Row>

                                <Row>
                                    <Col md={6}>
                                        <h4>Reviews</h4>
                                        {!product.reviews.length && <Message variant='info'>No Reviews</Message>}
                                        <ListGroup variant='flush'>
                                            {product.reviews.map(review => (
                                                <ListGroup.Item key={review.id}>
                                                    <strong>{review.name}</strong>
                                                    <Rating value={review.rating} color='#f8e825' />
                                                    <div><strong>Date:</strong> {review.createdAt.substring(0,10)}</div>
                                                    {review.comment && <div><strong>Comment:</strong> {review.comment}</div>}
                                                </ListGroup.Item>
                                            ))}

                                            {!reviewExist && <ListGroup.Item>
                                                <h4>Write a review</h4>
                                                {loadingProductReview && <Loader/>}
                                                {successProductReview && <Message variant='success'>Review Submitted</Message>}
                                                {errorProductReview && <Message variant='danger'>{errorProductReview}</Message>}

                                                {userInfo? (
                                                    <Form onSubmit={submitHandler}>
                                                        <Form.Group controlId='rating'>
                                                            <Form.Label>Rating</Form.Label>
                                                            <Form.Select
                                                                size='sm'
                                                                value={rating}
                                                                onChange={e => setRating(e.target.value) }
                                                            >
                                                                <option value=''>Select...</option>
                                                                <option value='1'>1 - Poor</option>
                                                                <option value='2'>2 - Fair</option>
                                                                <option value='3'>3 - Good</option>
                                                                <option value='4'>4 - Very Good</option>
                                                                <option value='5'>5 - Excellent</option>
                                                            </Form.Select>
                                                            <Form.Group controlId='comment'>
                                                            <Form.Label>Review</Form.Label>
                                                            <Form.Control
                                                                as='textarea'
                                                                row={5}
                                                                value={comment}
                                                                onChange={e => setComment(e.target.value)}
                                                            >
                                                            </Form.Control>
                                                            </Form.Group>
                                                        </Form.Group>
                                                        <Button
                                                            disabled={loadingProductReview}
                                                            type='submit'
                                                            variant='primary'
                                                            className='mt-2'
                                                        >
                                                            Submit
                                                        </Button>
                                                    </Form>
                                                ) : (
                                                    <Message variant='info'>Please <Link to='/login'>login</Link> to write a review</Message>
                                                )}
                                                </ListGroup.Item>
                                            }
                                        </ListGroup>
                                    </Col>
                                </Row>
                            </div>
    )
}
