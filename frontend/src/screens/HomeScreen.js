import {Row, Col} from 'react-bootstrap';
import Product from '../components/Product'

import products from '../products'

export default function HomeScreen() {

    return (
        <div>
            <h3>Lates Products</h3>
            <Row>
                {products.map(product => (
                    <Col sm={12} md={6} lg={4} xl={3} key={product._id}>
                        <Product product={product} />
                    </Col>
                ))}
            </Row>
        </div>
    )
}
