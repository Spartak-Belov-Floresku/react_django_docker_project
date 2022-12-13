import { useEffect, useState} from 'react'
import { Form, Col, Button } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import FormContainer from '../components/FormContainer'
import { savePaymentMethod } from '../actions/cartActions'
import CheckoutSteps from '../components/CheckoutSteps'

export default function PaymentScreen() {

    const navigate = useNavigate()

    const [paymentMethod, setPaymentMethod] = useState('PayPal')

    const { shippingAddress } = useSelector(state => state.cart)

    const dispatch = useDispatch()

    useEffect(()=>{
        if(!Object.keys(shippingAddress).length)
            navigate('/shipping')
    },[])

    const submitHandler = e => {
        e.preventDefault()
        dispatch(savePaymentMethod(paymentMethod))
        navigate('/placeorder')
    }

    return (
        <FormContainer>
            <CheckoutSteps step1 step2 step3 />

            <Form onSubmit={submitHandler}>
                <Form.Group>
                    <Form.Label as='legend'>Select Method</Form.Label>
                    <Col>
                        <Form.Check
                            type='radio'
                            label='PayPal or Credit Card'
                            id='paypal'
                            name='paymentmethod'
                            checked
                            onChange={e=>setPaymentMethod(e.target.value)}
                        ></Form.Check>
                    </Col>
                </Form.Group>

                <Button type='submit' className='mt-2' variant='primary'>
                    Continue
                </Button>
            </Form>
        </FormContainer>
    )
}