import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useParams } from 'react-router-dom'
import { Row, Col } from 'react-bootstrap'
import Product from '../components/Product'
import Loader from '../components/Loader'
import Message from '../components/Message'
import Paginate from '../components/Paginate';
import { listProducts } from '../actions/productActions'
import { ProductCarousel } from '../components/ProductCarousel'

export default function HomeScreen() {

    const {keyword} = useParams()

    const dispatch = useDispatch()
    const { error, loading, products, page, pages } = useSelector( state => state.productList )

    useEffect(() => {dispatch(listProducts(`user/${keyword}`))}, [dispatch, keyword])

    return (
        <div>
            {!keyword && <ProductCarousel />}
            <h3>Lates Products:</h3>
            { loading ? <Loader/>
                : error ? <Message variant='danger'>{error}</Message>
                    :   <>
                            <Row>
                                { products.map(product => (
                                    <Col key={product.id} sm={12} md={6} lg={4} xl={3}>
                                        <Product product={product}/>
                                    </Col>
                                )) }
                            </Row>
                            <Paginate page={page} pages={pages} keyword={keyword}/>
                        </>
            }
        </div>
    )
}
