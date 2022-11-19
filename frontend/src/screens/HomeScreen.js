import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Row, Col } from 'react-bootstrap'
import Product from '../components/Product'
import Loader from '../components/Loader'
import Message from '../components/Message'
import { listProducts } from '../actions/productActions'

export default function HomeScreen() {

    const dispatch = useDispatch()

    const { error, loading, products } = useSelector( state => state.productList )

    useEffect(() => {
      dispatch(listProducts())
    }, [dispatch])

    return (
        <div>
            <h3>Lates Products</h3>
            { loading ? <Loader/>
                : error ? <Message variant='danger'>{error}</Message>
                    : <Row>
                        { products.map(product => (
                            <Col key={product.id} sm={12} md={6} lg={4} xl={3}>
                                <Product product={product}/>
                            </Col>
                        ))}
                    </Row>
            }
        </div>
    )
}
