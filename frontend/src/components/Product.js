import {Card} from 'react-bootstrap'
import Rating from './Rating'
import { Link } from "react-router-dom"

export default function Product({product}) {
  return (
    <Card className="my-3 p-3 rounded boxshadow opacity">
      <Link to={`/product/${product._id}`}>
        <Card.Img src={product.image}/>
      </Link>

      <Card.Body>
            <Link to={`/product/${product._id}`}>
                <Card.Title as='span'>
                    <strong>{product.name.length <= 26 
                                ? product.name
                                : product.name.substring(0,26) + '...' }</strong>
                </Card.Title>
            </Link>

            <Card.Text as='div'>
                <div className="my-3">
                  <Rating value={product.rating} text={`${product.numReviews} review${product.numReviews > 1?'s':''}`} color={'#f8e825'} />
                </div>
            </Card.Text>

            <Card.Text as='h4'>
                ${product.price}
            </Card.Text>
      </Card.Body>
    </Card>
  )
}
