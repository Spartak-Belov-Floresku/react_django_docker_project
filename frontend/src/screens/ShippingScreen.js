import {useState} from 'react'
import { Form, Button } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import FormContainer from '../components/FormContainer'
import { saveShippingAddress } from '../actions/cartActions'
import CheckoutSteps from '../components/CheckoutSteps'

export default function ShippingScreen() {

  const navigate = useNavigate()

  const { shippingAddress } = useSelector(state => state.cart)

  const dispatch = useDispatch()

  const [address, setAddress] = useState(shippingAddress.address)
  const [city, setCity] = useState(shippingAddress.city)
  const [zipCode, setZipCode] = useState(shippingAddress.zipCode)

  const submitHandler = e => {
    e.preventDefault()
    dispatch(saveShippingAddress({
      address,
      city,
      zipCode,
    }))
    navigate('/payment')
  }

  return (
    <FormContainer>
      <CheckoutSteps step1 step2/>
      <h1>Shipping</h1>
      <Form onSubmit={submitHandler}>

        <Form.Group controlId='address'>
            <Form.Label>Address</Form.Label>
            <Form.Control
                required
                type='text'
                placeholder='Enter address'
                value={address? address: ''}
                onChange={e => setAddress(e.target.value)}
            >
            </Form.Control>
        </Form.Group>

        <Form.Group controlId='city'>
            <Form.Label>City</Form.Label>
            <Form.Control
                required
                type='text'
                placeholder='Enter city'
                value={city? city: ''}
                onChange={e => setCity(e.target.value)}
            >
            </Form.Control>
        </Form.Group>

        <Form.Group controlId='zipCode'>
            <Form.Label>Zip Code</Form.Label>
            <Form.Control
                required
                type='text'
                placeholder='Enter zip code'
                value={zipCode? zipCode: ''}
                onChange={e => setZipCode(e.target.value)}
            >
            </Form.Control>
        </Form.Group>

        <Button type='submit' className='mt-2' variant='primary'>
          Continue
        </Button>

      </Form>
    </FormContainer>
  )
}